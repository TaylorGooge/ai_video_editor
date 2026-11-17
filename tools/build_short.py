"""Build Public by Default Shorts from a per-video spec.

ffmpeg cuts/crops the footage + audio, Remotion (remotion/src/pbd/ShortOverlay) renders the
transparent overlay (header, cards, pane labels, captions), ffmpeg composites.

usage:
  tools/.venv/Scripts/python.exe -I tools/build_short.py <spec.json> <short_id|all> preview|final [preview_version]

spec: see tools/examples/10_blob-shorts-spec.json. Paths in it are relative to the project root.
  piece: {"a": in, "b": out, "v": picture}  (seconds of source; audio always comes from a..b)
  picture "t": card (Remotion card: title|rows|end) | crop {rect:[x,y,w,h]} |
               freeze {at, rect} | split (uses short.split + short.labels; optional vsrc:[in,out] speeds video to fit)
  "end_card_seconds": appends a silent end card to every Short (spec section 10); 0 = none.
  "header": false (spec-wide or per short) drops the label/title header and centres crops vertically,
            for footage that already fills a 9:16 frame.
  piece "cy": [[source_t, y], ...] caption centre y (1080x1920 px) from each source time on; omitted = default.
Preview  -> work/<slug>/shorts/preview-<id>-<version>.mp4 (720p)
Final    -> done/<slug>/shorts/<slug>-short-<id>.mp4 (1080p, two-pass loudnorm)
The raw source is only read, never written.
"""
import json, os, subprocess, sys, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REMOTION = os.path.join(ROOT, "remotion")
FPS = 30
INK = "0x0D1117"
PANEL_CY = 720          # centre of the screen panel in the 1080x1920 frame
PANEL_MAX_H = 860

# Whisper's usual misspellings of tool names; a spec can add its own under "caption_fixes".
FIXES = {"superbase": "Supabase", "superbase's": "Supabase's", "sukabase": "Supabase", "sukabase's": "Supabase's",
         "lovable's": "Lovable's"}

SPEC = json.load(open(sys.argv[1], encoding="utf-8"))
FIXES.update(SPEC.get("caption_fixes", {}))
SLUG = SPEC["slug"]
WORK = os.path.join(ROOT, "work", SLUG)
SRC = os.path.join(ROOT, SPEC["source"])
VOICE = os.path.join(ROOT, SPEC["voice"])
TRANSCRIPT = os.path.join(ROOT, SPEC["transcript"])
LABEL = SPEC["label"]
SHORTS = SPEC["shorts"]
if SPEC.get("end_card_seconds", 0):
    for _s in SHORTS.values():
        _s["pieces"].append({"silent": SPEC["end_card_seconds"], "v": {"t": "card", "card": {"kind": "end"}}})


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(" ".join(cmd)); print(r.stderr[-3000:]); sys.exit(1)
    return r


HEADER = True  # set per short in main()


def place(h):
    if not HEADER:
        return max(0, (1920 - h) // 2)
    return max(290, PANEL_CY - h // 2)


def build_piece(short, p, n, out, q):
    v = p["v"]
    enc = ["-c:v", "libx264", "-preset", q["preset"], "-crf", str(q["crf_mid"]), "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-frames:v", str(n), "-an", out]
    dur = n / FPS
    if v["t"] == "card":
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c={INK}:s=1080x1920:r={FPS}", *enc])
        return
    if v["t"] == "crop":
        x, y, w, h = v["rect"]
        oh = int(round(h * 1080 / w / 2) * 2)
        vf = f"crop={w}:{h}:{x}:{y},scale=1080:{oh}:flags=lanczos,pad=1080:1920:0:{place(oh)}:color={INK},fps={FPS}"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{p['a']:.3f}", "-t", f"{dur + 0.5:.3f}", "-i", SRC, "-vf", vf, *enc])
        return
    if v["t"] == "freeze":
        x, y, w, h = v["rect"]
        oh = int(round(h * 1080 / w / 2) * 2)
        vf = (f"trim=end_frame=1,setpts=PTS-STARTPTS,crop={w}:{h}:{x}:{y},scale=1080:{oh}:flags=lanczos,"
              f"pad=1080:1920:0:{place(oh)}:color={INK},fps={FPS},tpad=stop_mode=clone:stop_duration={dur + 1:.3f}")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{v['at']:.3f}", "-i", SRC, "-vf", vf, *enc])
        return
    if v["t"] == "split":
        sp = short["split"]
        vs, ve = v.get("vsrc", [p["a"], p["b"]])
        k = (ve - vs) / (p["b"] - p["a"])  # speed factor (1.0 = normal)
        tx, ty, tw, th = sp["top"]; bx, by, bw, bh = sp["bottom"]; ph = sp["pane_h"]
        fc = (f"[0:v]setpts=(PTS-STARTPTS)/{k:.4f},fps={FPS},split[a][b];"
              f"[a]crop={tw}:{th}:{tx}:{ty},scale=1080:{ph}:flags=lanczos[t];"
              f"[b]crop={bw}:{bh}:{bx}:{by},scale=1080:{ph}:flags=lanczos[u];"
              f"[t][u]vstack,pad=1080:1920:0:290:color={INK}[v]")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{vs:.3f}", "-t", f"{(ve - vs) + 0.5:.3f}", "-i", SRC,
             "-filter_complex", fc, "-map", "[v]", *enc])
        return
    raise ValueError(v["t"])


def main(sid, mode):
    global HEADER
    short = SHORTS[sid]
    HEADER = short.get("header", SPEC.get("header", True))
    q = {"preview": {"preset": "veryfast", "crf_mid": 18, "scale": 0.6667, "size": "720x1280", "crf": 23, "abr": "160k"},
         "final": {"preset": "slow", "crf_mid": 12, "scale": 1, "size": "1080x1920", "crf": 18, "abr": "320k"}}[mode]
    d = os.path.join(WORK, "shorts", sid)
    os.makedirs(d, exist_ok=True)
    words_all = [w for s in json.load(open(TRANSCRIPT, encoding="utf-8"))["segments"] for w in s["words"]]

    # 1) timeline
    off, total, pieces, words, cards, labels, areas = 0.0, 0, [], [], [], [], []
    cap_y = []
    for i, p in enumerate(short["pieces"]):
        n = round((p["silent"] if "silent" in p else p["b"] - p["a"]) * FPS)
        dur = n / FPS
        pieces.append((p, n, off))
        cys = p.get("cy", [])
        for k, (st, y) in enumerate(cys):
            fr = off + max(0.0, st - p["a"])
            to = off + (min(dur, cys[k + 1][0] - p["a"]) if k + 1 < len(cys) else dur)
            cap_y.append({"from": round(fr, 4), "to": round(to, 4), "y": y})
        for w in ([] if "silent" in p else words_all):
            # keep words that start in the piece, or that Whisper timed early but are still
            # being spoken when the piece starts (e.g. "Both" at 2:20)
            if (w["start"] >= p["a"] or w["end"] > p["a"] + 0.2) and w["start"] < p["a"] + dur - 0.05 and not (p["v"].get("vsrc")):
                txt = w["word"].strip()
                core = txt.rstrip(".,?!")
                if core.lower() in FIXES:
                    txt = FIXES[core.lower()] + txt[len(core):]
                if (not words or words[-1]["w"][-1] in ".?!") and txt[:1].islower():
                    txt = txt[0].upper() + txt[1:]
                words.append({"w": txt, "start": round(off + max(w["start"], p["a"]) - p["a"], 3),
                              "end": round(off + min(w["end"], p["a"] + dur) - p["a"], 3)})
        if p["v"]["t"] == "card":
            cards.append({**p["v"]["card"], "from": round(off, 4), "to": round(off + dur, 4)})
        if p["v"]["t"] == "split":
            for l in short.get("labels", []):
                labels.append({**l, "from": round(off, 4), "to": round(off + dur, 4)})
        off += dur
        total += n
    # merge consecutive labels
    merged = []
    for l in labels:
        m = next((x for x in merged if x["text"] == l["text"] and abs(x["to"] - l["from"]) < 1e-3), None)
        if m: m["to"] = l["to"]
        else: merged.append(dict(l))
    props = {"durationInFrames": total, "header": {"label": LABEL, "title": short["title"]} if HEADER else None,
             "words": words, "cards": cards, "labels": merged, "captionY": cap_y}
    json.dump(props, open(os.path.join(d, "overlay-props.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"Short {sid}: {total} frames = {total / FPS:.2f} s, {len(words)} caption words")

    # 2) video pieces
    lst = os.path.join(d, "pieces.txt")
    with open(lst, "w") as f:
        for i, (p, n, _) in enumerate(pieces):
            out = os.path.join(d, f"piece_{i:02d}.mp4")
            build_piece(short, p, n, out, q)
            f.write(f"file '{out.replace(os.sep, '/')}'\n")
    base = os.path.join(d, "base.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base])

    # 3) audio: cut each range with 20 ms fades, concat, loudness
    ins, fc = [], ""
    for i, (p, n, _) in enumerate(pieces):
        dur = n / FPS
        if "silent" in p:
            fc += f"anullsrc=r=48000:cl=stereo,atrim=0:{dur:.4f}[a{i}];"
            continue
        fc += (f"[0:a]atrim={p['a']:.4f}:{p['a'] + dur:.4f},asetpts=PTS-STARTPTS,"
               f"afade=t=in:d=0.02,afade=t=out:st={dur - 0.02:.4f}:d=0.02[a{i}];")
    fc += "".join(f"[a{i}]" for i in range(len(pieces))) + f"concat=n={len(pieces)}:v=0:a=1[cat]"
    raw_audio = os.path.join(d, "voice-cut.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-filter_complex", fc, "-map", "[cat]", "-c:a", "pcm_s24le", raw_audio])
    norm = os.path.join(d, "voice-norm.wav")
    if mode == "final":
        r = run(["ffmpeg", "-hide_banner", "-i", raw_audio, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"])
        js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
        af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
              f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    else:
        af = "loudnorm=I=-14:TP=-1:LRA=11"
    run(["ffmpeg", "-v", "error", "-y", "-i", raw_audio, "-af", af + ",aresample=48000", "-c:a", "pcm_s24le", norm])

    # 4) Remotion overlay (transparent PNG sequence)
    ov = os.path.join(d, f"overlay-{mode}")
    shutil.rmtree(ov, ignore_errors=True)
    r = subprocess.run(f'npx remotion render src/index.ts ShortOverlay "{ov}" --sequence --image-format=png '
                       f'--props="{os.path.join(d, "overlay-props.json")}" --concurrency=2 --scale={q["scale"]}',
                       cwd=REMOTION, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
    pngs = sorted(f for f in os.listdir(ov) if f.endswith(".png"))
    pad = len(pngs[0].split("-")[-1].split(".")[0])
    pattern = os.path.join(ov, pngs[0].rsplit("-", 1)[0] + f"-%0{pad}d.png")

    # 5) composite
    w, h = q["size"].split("x")
    if mode == "preview":
        out = os.path.join(WORK, "shorts", f"preview-{sid}-{VERSION}.mp4")
    else:
        os.makedirs(os.path.join(ROOT, "done", SLUG, "shorts"), exist_ok=True)
        out = os.path.join(ROOT, "done", SLUG, "shorts", f"{SLUG}-short-{sid}.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", base, "-framerate", str(FPS), "-start_number", pngs[0].split("-")[-1].split(".")[0].lstrip("0") or "0",
         "-i", pattern, "-i", norm,
         "-filter_complex", f"[0:v]scale={w}:{h}:flags=lanczos[b];[1:v]scale={w}:{h}[o];[b][o]overlay=0:0:format=auto,format=yuv420p[v]",
         "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", "fast" if mode == "preview" else "slow",
         "-crf", str(q["crf"]), "-r", str(FPS), "-c:a", "aac", "-b:a", q["abr"], "-ar", "48000",
         "-movflags", "+faststart", "-shortest", out])
    print("wrote", out)


if __name__ == "__main__":
    VERSION = sys.argv[4] if len(sys.argv) > 4 else "v1"
    ids = list(SHORTS) if sys.argv[2] == "all" else [sys.argv[2]]
    for sid in ids:
        main(sid, sys.argv[3] if len(sys.argv) > 3 else "preview")
