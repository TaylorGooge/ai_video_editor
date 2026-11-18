"""Transcribe with faster-whisper on CPU (int8). PyAV has no Python 3.15 build,
so `av` is stubbed and audio is passed in as float32 16 kHz mono decoded by ffmpeg.
VAD is off (it needs onnxruntime, which also has no 3.15 build)."""
import json, sys, types
sys.modules["av"] = types.ModuleType("av")
import numpy as np
from faster_whisper import WhisperModel

src, out_base, model_name = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "small.en")
audio = np.fromfile(src, dtype=np.float32)
model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=4)
prompt = "Public by Default. Supabase, Lovable, Bolt, Cursor, Replit, Claude Code, RLS, row level security, blob, storage bucket, .env, API key."
if len(sys.argv) > 4:  # optional per-video prompt (tool names, file names from script.md)
    prompt = sys.argv[4]
segments, info = model.transcribe(audio, language="en", word_timestamps=True,
                                  initial_prompt=prompt, vad_filter=False, beam_size=5)
segs = []
for s in segments:
    segs.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                 "words": [{"start": w.start, "end": w.end, "word": w.word} for w in (s.words or [])]})
    print(f"[{s.start:7.2f} -> {s.end:7.2f}] {s.text.strip()}", flush=True)
json.dump({"model": model_name, "duration": info.duration, "segments": segs},
          open(out_base + ".json", "w", encoding="utf-8"), indent=1)
with open(out_base + ".txt", "w", encoding="utf-8") as f:
    for s in segs:
        m, sec = divmod(s["start"], 60)
        f.write(f"[{int(m)}:{sec:05.2f}] {s['text']}\n")
