# v_s1a edit notes

## Scope (17 Nov 2026)
- Output: **long-form only**, plus thumbnail and description. No Shorts requested.
- Title (your pick): **My AI Removed One Form Field. It Never Mentioned the Price**
- Description info: 10a https://youtu.be/4x5w0DcKOPw · S1b https://youtu.be/cC2F-ovAl_8 · Claude Code 2.1.326 (Nov 2026).
- Section 7 uses the `07_*` clips (not the hook footage).
- Script: `raw\v_s1a\script.md` (sections 1-8, 0:00-8:10), plus `raw\v_s1a\notes.txt` (animation/blur/clip instructions).

## Sources (raw\v_s1a\, untouched)
- `voice\Recording.wav`: PCM s16, 48 kHz, stereo, 503.2 s (8:23).
- `screen\*.mp4`: 20 clips, all H.264, constant 30 fps (r_frame_rate = avg_frame_rate = 30/1), no VFR. Cropped captures at odd sizes:

| Clip | Size | Length |
|---|---|---|
| 01_hook_naive | 910x992 | 36.8 |
| 02_code_diff_bookings_js | 1576x522 | 5.2 |
| 02_code_diff_index_html | 1642x588 | 5.1 |
| 03_app_folder_tree | 1848x896 | 13.8 |
| 03_check_blast_radius | 1500x952 | 11.2 |
| 03_grep_pet_fee | 1426x448 | 13.4 |
| 03_trigger_body | 790x440 | 6.5 |
| 04_code_diffs_all | 1414x972 | 29.3 |
| 04_hook_ben | 904x1026 | 33.1 |
| 04_mcp_connection | 1444x438 | 20.5 |
| 05_sql_editor | 1524x880 | 10.1 |
| 06_admin_js_fixed | 1774x1018 | 9.1 |
| 06_blast_radius | 1490x962 | 8.5 |
| 06_drop_tests | 1486x946 | 8.4 |
| 06_grep_has_pets | 1386x268 | 9.4 |
| 06_matching_js_fixed | 1798x972 | 5.9 |
| 07_auto_assign_to_ben | 1154x152 | 5.6 |
| 07_booking_process | 926x910 | 25.7 |
| 07_dropdown_to_yes | 1344x528 | 10.0 |
| 07_old_entries_keep_info | 1618x628 | 6.3 |

- `screen\05_old_admin_js.png`: 1060x327.

## Ingest (work\v_s1a\ingest\)
- Screen: re-encoded H.264 CRF 16, 30 fps CFR, yuv420p, audio dropped. **Kept at native size** (not padded to 1920x1080 yet): the clips are crops at very different sizes, so the scale and placement on the #0D1117 canvas is a per-clip layout choice in the cut list.
- Voice: `voice.wav` (48 kHz copy, unprocessed), `voice16k.f32` for Whisper.
- Contact sheets: `frames\<clip>.png`.

## Transcript
- faster-whisper small.en, int8, CPU, prompt with script names (Supabase, MCP, pet_fee, has_pets, file names, Ana, Ben).
- `tools\transcribe.py` gained an optional 4th argument (prompt override). Older calls behave as before.

## Flags from the screen review (before transcript)
- **Privacy (blur):** the terminal path in 03_grep_pet_fee and 06_grep_has_pets; the MCP URL (project_ref) and config path in 04_mcp_connection, and the "Project MCPs (C:\Users\taylo\...)" line at ~18 s; VS Code "Recent" list with OneDrive paths in 03_app_folder_tree 0-5 s.
- **03_grep_pet_fee:** hits are admin.js **plus `supabase/migrations/20261117000000_init.sql`** (lines 22, 54, 55: column, view select, `base_price + pet_fee as total`). Script says "Hits only where it's displayed in admin.js".
- **03_app_folder_tree:** the app folder *does* contain a SQL file (`supabase/migrations/..._init.sql`, tables, view, RLS). It doesn't contain the trigger. Script cue says "no SQL file containing the trigger"; correct, but the VO wording needs to match.
- **06_grep_has_pets:** typed `git grep -E "has_?pets|haspets"` (no `-n -i`); script and blast-radius.sql say `git grep -n -i -E "has_?pets|haspets"`.
- **07:** the booking is typed as "Jane Doe", but the staff-page row that gets "We have a dog." shows customer "test / test@test.com".
- **07:** Jane Smith's row is Yes / $165 / Chloe in 07_dropdown_to_yes but Unknown / $150 / Ben in 07_old_entries_keep_info.

## Cut list v1 (17 Nov 2026), awaiting review gate 1
- `cutlist-v1.md`; timings from `cutplan.py` -> `cutplan.json`. Speech edges from `transcript\speech-regions.txt` (silencedetect -42 dB / 0.25 s). Pauses > 0.7 s inside a line shortened to 0.4 s.
- Length: voice ends 5:57.5, outro 20 s, total ~6:17 (voice ~5:05 + 1 series card, 7 chapter cards, demo/prompt-card holds 33 s).
- Exceptions to "last complete take": 0:21 take 1 ("couldn't see", F1); 1:40 take 1 (take 2 stumbles); 5:48.9 take 1 (take 2 has a 3 s mid-line pause).
- Open flags F1-F9 listed in the cut list (very common setup claim, "Null"/"No", grep hits in init.sql, SQL file in the app folder tree, grep flags, 07 footage continuity, Prompt 1/3 numbering, untested prompts).

## Cut list v2 (17 Nov 2026, your answers)
- F1 take 1 ok; F2 softer take ("but it's a common setup."); F3 "null" confirmed; F4 grep shows admin.js only (migration lines masked, crop); F5 folder tree before migrations opens; F6 full `git grep -n -i -E` command as a label; F7 crops around continuity slips; F8 Prompt 1 / Prompt 2 (blast-radius query card) / Prompt 3.
- Fixed a duplicate: "Here we're keeping it" was inside the "Five, drop the column later. Or never." segment (raw end 419.52 -> 418.18). Checked by re-transcribing each kept snippet.
- Typing sound requested. No sound file in the project, so `assemble.py` generates soft key clicks (peaks about -30 dBFS) under the animated prompts, the booking re-type in section 7, and the three section 8 cards.

## Build (preview v1, 17 Nov 2026)
- Voice: `build_voice.py` -> `build\voice-edit.wav` (cuts, 15/30 ms fades, mono) -> `build\voice-proc.wav` (HPF 80 Hz, afftdn nr=10, compressor 2.5:1 @ -20 dB, single-pass loudnorm).
- Picture: `scenes.py` -> `build\scenes.json` (53 scenes, anchored to word times) -> `remotion\render-scenes.mjs` (bundle once, concurrency 2, 720p = scale 2/3, x264 veryfast CRF 20) -> `build\scenes-720\`. Sources copied to `remotion\public\v_s1a\` (blurs baked into 03_grep_pet_fee and 04_mcp_connection). Render about real time (~6 min).
- New shared Remotion components in `remotion\src\pbd\`: `LongScene` (composition "LongScene"), `ScreenScene` (trim/speed/freeze, eased zooms, highlight/dim, circles, masks, labels, corner logo), `ClaudeUI` (ClaudePrompt, ClaudeResponse), `Cards` (Series, Chapter, Prompt, CodeStack, Checklist, StepList, Outro).
- `assemble.py preview 1` -> `preview-v1.mp4` (6:12.1, 1280x720).
- Thumbnail + description drafts: `thumbs\thumb-A-price.png` (HTML in `thumbs\`, headless Edge), `thumbs\v_s1a-description.txt`.

## Preview v1 notes (17 Nov 2026) -> preview v2
- 1:16 grep cut off on the right (camera was 1110 px wide, the command runs to ~1290): camera now shows the full 1426 px line width.
- 2:00 "um" + restart after "read access to" (raw 202.69-203.80) cut. 2:12 false start "Unknown." (raw 214.50-215.50) cut. 3:27 sniffle (raw 313.36-313.49) cut. Voice now ends 5:49.4, total 6:09.4.
- 2:47 lower third now reads "Your AI Knows Where. Only You Know Why." (no "S1b").
- 4:47 highlights: the staff table re-lays out when Auto-assign is clicked (columns shift ~25 px right); boxes now use the before-click positions until the click, then the after-click ones.
- 4:52 dropdown menu was cut off: crop is taller (228 px of source) so the menu shows; Jane Smith's row is masked white (F7 still holds), her Pets cell is masked once the menu closes.
- `scenes.py` anchors take v1 times through N() so they land on the v2 timeline. Description chapter times updated.
- Preview v2 note: 2:00 still had the flub. The first take (raw 200.30-201.89) is "So I gave it read acc- ugh"; the piece cut in v2 (202.69-203.80) was the clean retake "So I gave it read access to". v3 keeps 202.69-213.70 and drops 200.30-201.89. Verified by re-transcribing the whole edited voice (no repeats). Total 6:08.8.

## Final (approved 17 Nov 2026, preview v3)
- `render-scenes.mjs ... 1` -> `build\scenes-1080\` (x264 slow CRF 18), `assemble.py final` -> `done\v_s1a\long\v_s1a.mp4`: 1920x1080, 30 fps, 6:08.8, AAC 320k target (encoder averages ~136k on this voice), faststart. Two-pass loudnorm I=-14 / TP=-1.5 (TP -1 gave a -0.9 dBFS peak after AAC): measured -14.5 LUFS integrated (20 s silent outro included), peak -1.4 dBFS.
- Captions: `make_captions.py` -> `v_s1a.srt` (114 cues, max 2 x 42). Timing from Whisper run on the edited voice (`build\check\edit-v3.json`); text proofed against script.md (Supabase, Ana, Ben, "Null.", "It's four.", quotes). Whisper hallucinated "Thank you for watching." in the silent outro; excluded.
- `chapters.txt`: 0:00 / 0:33 / 1:13 / 1:57 / 2:47 / 3:18 / 4:33 / 4:58 (all >= 10 s apart). Same as the description.
- `v_s1a-thumbnail.png`, `v_s1a-description.txt` copied from `work\v_s1a\thumbs\`.
- Not cleaned up yet: `work\v_s1a\` (~ingest, build, previews) and `remotion\public\v_s1a\` (source copies). Ask first.
