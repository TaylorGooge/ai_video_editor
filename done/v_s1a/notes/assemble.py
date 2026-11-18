r"""Join rendered scenes, add voice + typing sound -> preview or final.
Run: tools\.venv\Scripts\python.exe -I work\v_s1a\assemble.py preview <N>   -> work\v_s1a\preview-vN.mp4 (720p)
     tools\.venv\Scripts\python.exe -I work\v_s1a\assemble.py final         -> done\v_s1a\long\v_s1a.mp4 (1080p)
Typing sound: generated soft key clicks (no sound file in the project), placed on build\typing.json ranges."""
import json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "build")
SR = 48000
mode = sys.argv[1]
scenes = json.load(open(os.path.join(B, "scenes.json"), encoding="utf-8"))
plan = json.load(open(os.path.join(HERE, "cutplan.json")))
sdir = os.path.join(B, "scenes-720" if mode == "preview" else "scenes-1080")

# 1. picture: concat scenes (same codec/size/fps), re-timed to exact scene starts
lst = os.path.join(B, f"concat-{mode}.txt")
with open(lst, "w") as f:
    for s in scenes:
        f.write(f"file '{os.path.join(sdir, s['id'] + '.mp4').replace(os.sep, '/')}'\n")
video = os.path.join(B, f"video-{mode}.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video], check=True)

# 2. typing sound
rng = np.random.default_rng(7)
def key():
    n = int(SR * rng.uniform(0.018, 0.035))
    noise = rng.standard_normal(n)
    env = np.exp(-np.linspace(0, rng.uniform(7, 11), n))
    click = np.convolve(noise * env, [1, -0.85], "same")          # thin, high click
    thump = np.sin(2 * np.pi * rng.uniform(140, 220) * np.arange(n) / SR) * env * 0.6
    return (click * 0.5 + thump) * rng.uniform(0.6, 1.0)
sfx = np.zeros(int(plan["total"] * SR) + SR, dtype=np.float64)
for t0, t1 in json.load(open(os.path.join(B, "typing.json"))):
    t = t0
    while t < t1:
        k = key(); i = int(t * SR); sfx[i:i + len(k)] += k
        t += rng.uniform(0.055, 0.13) + (rng.uniform(0.15, 0.35) if rng.random() < 0.06 else 0)
sfx *= 10 ** (-30 / 20) / max(1e-9, np.abs(sfx).max())   # peaks about -30 dBFS: well under the voice
sfx_path = os.path.join(B, "typing.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", sfx_path],
               input=sfx.astype(np.float64).tobytes(), check=True)

# 3. mix + mux
voice = os.path.join(B, "voice-proc.wav")
mix = "[1][2]amix=inputs=2:normalize=0:duration=first[a]"
if mode == "preview":
    n = sys.argv[2] if len(sys.argv) > 2 else "1"
    out = os.path.join(HERE, f"preview-v{n}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", voice, "-i", sfx_path, "-filter_complex", mix,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(plan["total"]), out], check=True)
else:
    out_dir = os.path.join(HERE, "..", "..", "done", "v_s1a", "long"); os.makedirs(out_dir, exist_ok=True)
    out = os.path.normpath(os.path.join(out_dir, "v_s1a.mp4"))
    mixed = os.path.join(B, "mix.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", sfx_path, "-filter_complex", "[0][1]amix=inputs=2:normalize=0:duration=first",
                    "-ar", str(SR), mixed], check=True)
    # two-pass loudnorm to -14 LUFS / -1 dBTP
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", mixed, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", mixed, "-af", ln, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-t", str(plan["total"]), "-movflags", "+faststart", out], check=True)
print(out)
