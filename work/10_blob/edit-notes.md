# Edit notes: 10_blob

## Source
- `raw\v_10b_youtube.mov`: finished long-form, not raw footage. 7:07.03, H.264 1920x1080, **constant** 30 fps, PCM s24le 48 kHz stereo (final mix), plus a timecode data track (dropped). 234 MB.
- Identical in size to `references\v_10b_youtube.mov` (probably the same file).
- Loudness of the source mix: **−23.9 LUFS integrated**, LRA 4.5 LU. Needs ≈ +10 dB to reach −14.
- No `script.md` and no separate screen/voice files, so the skill's script alignment, retake/filler cuts, `[SCREEN]` cue mapping, voice processing and long-form .srt/chapters don't apply.
- Slug `10_blob` assumed (not confirmed by any folder).

## Output requested
Short(s) only.

## Tooling (12 Nov 2026)
- ffmpeg/ffprobe 9.0.2, Node 26.13, Remotion CLI 4.0.543 (the project has no source/components yet).
- Python 3.15.2 via `py` only. faster-whisper 1.2.1 is installed in `work\10_blob\.venv` **without PyAV or onnxruntime**: neither has a Python 3.15 build. `transcribe.py` stubs `av`, feeds float32 16 kHz audio decoded by ffmpeg, and runs with VAD off.
- ffmpeg `drawtext` can't find a default font here (fontconfig), so label frames another way or pass `fontfile=`.

## Ingest / transcript
- `ingest\audio-48k.wav` (copy of the mix), `ingest\audio-16k.f32` (Whisper input).
- `transcript.json` / `.txt`: small.en, int8, CPU, word timestamps, tool-name prompt. Accurate except Supabase spelled "Superbase"/"Sukabase".

## Decisions
- Gate 1: all three Shorts approved → `cutlist-v2.md`. Flag 2 defaulted to option (a), keeping the source picture, because no option was picked.
- Short 02 payoff holds a freeze of 5:44.0 (profiles response) under the 5:37–5:41 line.
- Short 03 split crops start at the "Signed in as" line (v1 of the build cut off the posts).

## Build (preview v1)
- `build_short.py <id|all> preview|final`: ffmpeg pieces (crop → 1080 wide, Ink pad, panel centred y≈720) → concat; audio cut from `ingest\audio-48k.wav` with 20 ms fades; loudnorm −14/−1 (single pass for preview, two-pass for final).
- Remotion `ShortOverlay` (new reusable components in `remotion\src\pbd\`: theme, ShortCaptions, VerticalTitleCard, RowsCard, ShortOverlay) rendered as a transparent PNG sequence, concurrency 2, scale 0.6667 for preview.
- Preview encode: 720x1280, x264 fast CRF 23, AAC 160k. All three build in ≈3 min total.
- Lengths: 01 = 37.3 s, 02 = 18.2 s, 03 = 42.8 s. Measured loudness: −14.2 / −13.6 / −13.9 LUFS.
- Added deps in `remotion\package.json`: remotion, react, react-dom, @remotion/google-fonts (pinned). Logo copied to `remotion\public\brand\`.

## Flagged
- 5:42–5:50: the two-window fix test is described but not shown ("I forgot to record it again :(").
- ≈1:47–1:55: network-tab line plays over the Table Editor.
- ≈5:12–5:24: backups line plays over the Auth docs / Table Editor menu.
- 2:17–2:20: voice says "Maria on the left, Dev on the right"; the screen shows Dev left, Maria right. Trimmed from Short 03 (your call at gate 2). Still in the published long-form.

## Preview v3 (12 Nov 2026)
- Added a 2.5 s silent end card to all three (new `remotion\src\pbd\EndCard.tsx`, matching brand/shorts-endcards #2): "Want the full fix?" / "The step-by-step video is on the channel." / green pill "Learn more on the channel" / @publicbydefault. Captions are hidden on the end card.
- **Overrides spec §10** ("end on the payoff, not on a 'subscribe' card"), at your request. The card comes after the payoff. Update the spec if this is the new default.
- Lengths: 01 = 39.8 s, 02 = 20.7 s, 03 = 42.6 s. Loudness −14.2 / −13.6 / −13.9 LUFS.

## Final (12 Nov 2026), approved at gate 2
- `build_short.py all final`: intermediates x264 slow CRF 12; final 1080x1920 30 fps H.264 slow CRF 18, AAC 320k 48 kHz, faststart; two-pass loudnorm I=−14, TP=−1, LRA=11.
- Delivered to `done\10_blob\shorts\`:
  - 10_blob-short-01.mp4: 39.8 s, −14.0 LUFS, peak −1.1 dBFS
  - 10_blob-short-02.mp4: 20.7 s, −14.0 LUFS, peak −4.0 dBFS
  - 10_blob-short-03.mp4: 42.6 s, −13.9 LUFS, peak −2.8 dBFS
  - 10_blob-short-0N.txt: approved title, description and related video (https://youtu.be/4x5w0DcKOPw)
- Spec and CLAUDE.md updated: end card by default, title and description step at gate 2.

## Cleanup (12 Nov 2026, approved)
- Moved to shared `tools\`: `.venv` (faster-whisper), `transcribe.py`, `build_short.py` (now reads `shorts-spec.json`; checked by rebuilding Short 02: identical 621 frames / 52 caption words).
- Deleted: `ingest\`, `frames\`, `shorts\` (pieces, overlays, previews), `__pycache__`, about 750 MB.
- Kept: notes, cut lists, `shorts-spec.json`, transcript, `titles-draft.md`. To rebuild, re-extract `ingest\audio-48k.wav` from raw first.
