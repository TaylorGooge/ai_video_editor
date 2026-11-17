# v_s1b edit notes

## Sources (raw\v_s1b\, untouched)
- `script.md`: S1b "Your AI Knows Where. Only You Know Why." Written as a 9:16 Short (~90 s) with an optional ~2:30 extended cut.
- `notes.md`: animation cue sheet (clip → script line, event times, 9:16 crop column x=656–1264).
- `screen\s1b-01 … s1b-16*.mp4`: 16 animation clips, all 1920x1080, constant 30 fps, H.264, no audio. 01–14 = main cut, 15–16 = extended only (insert after 11).
  - `s1b-04-…_1.mp4` and `s1b-11-…_1.mp4` are pixel-identical to the originals (checked frame by frame; only container bytes differ). Using the originals.
- `voice\v_s1b.wav`: 48 kHz, 16-bit PCM, stereo, 135.94 s. Covers the main cut **and** the extended lines (recorded after the ending).

## Transcript
- `transcript\voice-small.{json,txt}`: faster-whisper small.en, int8, CPU.
- Retakes found (keep last complete take): "So I asked my AI tool…" (10.8 / 15.7), "Remove the question…" (31.5 / 35.7), "It can't know why…" (64.6 / 71.6; the first take says "what you want to know"), "Yes, still match. Ask about pets on the phone instead." (112.6 / 117.3 / 121.6 area).

## Flags
- 59.5 s ad-lib "every page, every rule" is not in script.md but matches the cue sheet for clip 09. Minor.
- Script fact-check: the pasted prompt is marked **not verified** (test it before publishing).
- Script story rule: ask the client before telling the anonymized version.

## Decisions
- 17 Nov 2026: output is 16:9 long-form (main + extended cut) first; Shorts get cut from the long-form later.
- Cut list v1 written (`cutlist-v1.md`, timings from `cutplan.py` -> `cutplan-main.json`, `cutplan-extended.json`). Awaiting review gate 1.
- Freeze/trim points checked frame by frame (no motion). Clip 05 freeze moved to 1.96 s (strike still easing at 1.8–1.9 s).
- 17 Nov 2026, cut list v2 (your notes): ad-lib "every page, every rule" cut; corner logo added (top-right corner verified empty in all clips); prompt card 9.0 s (spec says 11 s, your override); outro 12 s (spec says 20 s, your override for this video).

## Preview renders (v1, 17 Nov 2026)
- `build_long.py <main|extended> preview 1` -> `preview-main-v1.mp4` (1:29.6), `preview-extended-v1.mp4` (1:52.3).
- Video: ffmpeg frame-mapped trims/freezes from `cutplan-*.json`, logo `brand\descript-kit\pbd-badge-A-padlock.png` 80 px, 40 px margin, 75% opacity (off during outro), outro `brand\descript-kit\pbd-scene-bg-1920x1080.png`. Preview 720p, x264 veryfast CRF 23.
- Voice: segments with 60 ms/100 ms pads, 15/30 ms fades, mono, highpass 80 Hz, afftdn nr=10, compressor 2.5:1 @ -20 dB, single-pass loudnorm -14 LUFS / -1 dBTP. Measured: main -14.3 LUFS, peak -3.9 dBFS; extended -14.4 LUFS.
- Not Remotion: no designed elements needed beyond the supplied animations.

## Final (approved 17 Nov 2026)
- `build_long.py <cut> final` -> `done\v_s1b\long\v_s1b.mp4` (1:29.6) and `v_s1b-extended.mp4` (1:52.3): 1080p30, x264 slow CRF 18 High, AAC 320k target (encoder averages ~175k on this sparse voice), BT.709. Two-pass loudnorm: main -14.1 LUFS, extended -14.2 LUFS, peaks about -4 dBFS.
- Captions: `make_captions.py` -> `v_s1b.srt` (24 cues), `v_s1b-extended.srt` (31 cues). Text from script-proofed segment text, Whisper word timing, max 2 lines of 42 chars, breaks at sentence/clause ends.
- Chapters: `chapters.txt`, `chapters-extended.txt`. YouTube rules checked against YouTube Help 17 Nov 2026: first at 0:00, at least 3, each at least 10 s. All chapters pass (shortest is 13 s).
- Open before publishing: test the prompt (script fact-check), confirm client permission.
- work\v_s1b\ not cleaned up yet (ask first). Keep cutplan/build scripts if Shorts will be cut from this.

## Shorts (previews v1, 17 Nov 2026)
- Spec: `shorts-spec.json`. Source = approved extended final + its processed voice; captions from `transcript\edited-extended.json` (`remap_transcript.py`).
- Crop: 9:16-safe column x=656 w=608, full height, scaled to 1080x1918, no header. Captions moved per scene (`cy`) into empty space.
- Shared tool changes: `tools\build_short.py` gained `"header": false` and per-piece `"cy"`; `remotion\src\pbd\ShortOverlay.tsx` accepts `header: null` and `captionY` ranges. Older specs behave as before.
- 01: 0:00–0:24 + prompt 1:19.76–1:27.26 (prompt 7.5 s) = 34.0 s with end card. 02: 0:00–0:04.95 + 0:33.36–0:56.94 + statement 1:34.60–1:40.0 = 36.4 s. 03: 0:00–0:04.95 + 0:24.28–0:33.2 + 0:57.14–1:19.7 = 38.9 s.
- Previews about -13.9 LUFS (single pass). Titles and descriptions drafted in `shorts\titles-descriptions-draft.md`.

## Thumbnails + descriptions (drafts, 17 Nov 2026)
- `thumbs\thumb-A-where-why.png` (main) and `thumbs\thumb-B-just-paste.png` (extended): 1280x720, HTML in `thumbs\*.html` + `common.css`, rendered with headless Edge. Style matches `references\src\thumb*.html`. Fonts copied from `raw\v_s1b\screen\src\fonts`. Bottom-right kept clear (timestamp).
- `thumbs\v_s1b-description.txt`, `thumbs\v_s1b-extended-description.txt`: title options, description, chapters (match chapters*.txt), hashtags, pinned comment with the prompt.
- Still open: prompt not tested (script fact-check); client permission. Thumbnail B and title 2 name Claude (script says fine, it's the real quote).
- Approved 17 Nov 2026. Copied to done\v_s1b\long as v_s1b-thumbnail.png, v_s1b-extended-thumbnail.png, v_s1b-description.txt, v_s1b-extended-description.txt.
- Final Shorts (approved 17 Nov 2026): `done\v_s1b\shorts\v_s1b-short-01/02/03.mp4`, 1080x1920 30 fps, x264 slow CRF 18, AAC 320k, two-pass loudnorm -14.0 LUFS (peaks about -4 dBFS). Lengths 34.0 / 36.4 / 38.9 s. Titles and descriptions in `v_s1b-short-NN.txt` (long-form link still a placeholder).
