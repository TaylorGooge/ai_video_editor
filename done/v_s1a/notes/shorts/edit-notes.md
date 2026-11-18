# v_s1a Shorts: edit notes
(Long-form notes: `done\v_s1a\notes\edit-notes.md`.)

## Scope (17 Nov 2026)
- 3 Shorts cut from the published long-form (https://youtu.be/mHklVwrxhj8), with titles, descriptions and custom thumbnails. End card on all three.
- Picked to send viewers to the full video: 01 hook (price), 02 database access, 03 four changes + Prompt 1. Approved at gate 1 (`shorts-cutlist-v1.md`).

## Source
- `done\v_s1a\long\v_s1a.mp4` (approved final, so the blurs and masks are already baked in). Audio -> `ingest\long-audio-48k.wav`.
- Transcript: faster-whisper small.en int8 on the long-form audio -> `transcript.json` (long-form times).

## Build
- `shorts-spec.json` + `tools\build_short.py`. New in the shared tools:
  - `ShortOverlay` card kind `prompt` (the long-form `PromptCard` at 34 px, pinned at top=420 so it doesn't drift while it types). `PromptCard` gained an optional `top` prop; long-form behaviour is unchanged.
  - `build_short.py` `word_fixes`: one-off caption fixes keyed by source time ("It's four.", "Ben", "$150", quotes).
- Designed cards in place of unreadable crops: 01 opens on a title card with the typed prompt; 02 shows Claude's reply as two quote cards (text copied exactly from the screen, including the cut-off "I left them…"); 03 shows Prompt 1 as a 9:16 card.
- Short 02 MCP shot: a freeze of 2:00.35, so the "Project MCPs (C:\Users\…)" frame (1:59.7–2:00.0) never shows.

## Previews
- preview-01-v2 (33.2 s), preview-02-v3 (46.9 s), preview-03-v2 (29.8 s). 720p.
- Thumbnails: `thumbs\v_s1a-short-NN-thumbnail.png` (1080x1920, HTML in `thumbs\`, headless Edge; Inter copied from raw\v_s1b fonts).
- Titles and descriptions: `shorts\v_s1a-short-NN.txt` (drafts, no angle brackets).

## Flags
- The published long-form shows the local path `C:\Users\taylo\OneDrive\...` for about 0.3 s at 1:59.7. Fix it in YouTube Studio's Editor with Blur, or re-render.

## Final (approved 17 Nov 2026: preview-01-v2, preview-02-v3, preview-03-v2)
- `build_short.py ... all final`: 1080x1920, 30 fps, x264 slow CRF 18, AAC 320k, two-pass loudnorm I=-14 / TP=-1.
- Measured: 01 33.2 s -13.9 LUFS / -1.0 dBTP; 02 46.9 s -14.0 / -1.0; 03 29.8 s -13.9 / -1.0.
- Delivered to `done\v_s1a\shorts\`: `v_s1a-short-NN.mp4`, `.txt` (title + description), `-thumbnail.png`.
- Not cleaned up: `work\v_s1a\` (ingest audio, transcript, previews, piece files). Ask first.
