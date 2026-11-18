r"""Build the edited voice track from cutplan.json.
Run: tools\.venv\Scripts\python.exe -I work\v_s1a\build_voice.py
Writes build\voice-edit.wav (cuts only, mono 48k) and build\voice-proc.wav (HPF, NR, compression;
single-pass loudnorm -14 LUFS for preview; final render re-does loudness two-pass on the full mix)."""
import json, os, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "build"); os.makedirs(B, exist_ok=True)
SR = 48000
plan = json.load(open(os.path.join(HERE, "cutplan.json")))

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(HERE, "ingest", "voice.wav"),
                      "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
src = np.frombuffer(raw, dtype=np.float32)
out = np.zeros(int((plan["total"] + 1) * SR), dtype=np.float32)
fi, fo = int(0.015 * SR), int(0.030 * SR)
for s in plan["segments"]:
    a = int((s["raw0"] - plan["pad_in"]) * SR); b = int((s["raw1"] + plan["pad_out"]) * SR)
    clip = src[a:b].copy()
    clip[:fi] *= np.linspace(0, 1, fi); clip[-fo:] *= np.linspace(1, 0, fo)
    o = int((s["v0"] - plan["pad_in"]) * SR)
    out[o:o + len(clip)] += clip
out = out[:int(plan["total"] * SR)]
edit = os.path.join(B, "voice-edit.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                "-c:a", "pcm_s16le", edit], input=out.tobytes(), check=True)
chain = "highpass=f=80,afftdn=nr=10:nf=-50,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=11"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", edit, "-af", chain, "-ar", str(SR), "-c:a", "pcm_s16le",
                os.path.join(B, "voice-proc.wav")], check=True)
print("voice", plan["voice_end"], "total", plan["total"])
