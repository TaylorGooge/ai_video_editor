# Edit spec v1: Public by Default (12 Nov 2026)

**What changed:** replaces the editing parts of `brand/descript-style-guide-v1.md`. That guide was written as paste-in fields for Descript's Brand Studio. This version says the same things without being tied to any tool, so the AI editor (ffmpeg + Remotion) can follow it, and it adds what Descript used to handle automatically: pacing, voiceover sync, audio levels and caption files. The branding kit (logos, colors, fonts, banner, watermark) is **unchanged**. Section 4 of the old guide is still the reference for which logo file to use where.

**Update (12 Nov 2026):** Shorts now end on a call-to-action end card by default (§6, §10). Every Short also gets a title and description file for review (§11).

---

## 1. Brand (unchanged from v1)

| Role | Hex | Use |
|---|---|---|
| Ink | `#0D1117` | Background of every designed scene |
| Panel | `#161B22` | Cards, lower thirds, prompt cards, caption box |
| Border | `#30363D` | Dividers, faint grid |
| Paper | `#E6EDF3` | Titles, body, captions |
| Muted | `#8B949E` | Subtitles, secondary text |
| Green | `#3FB950` | Accent: the fix, "verified", the key word. Use sparingly |
| Red | `#F85149` | Only for marking the problem/hole |
| Amber | `#D29922` | Optional, "partly fixed / check this". Small use only |

Fonts: **Inter** (Bold 700 titles, Medium 500 subtitles, Regular 400 body) and **JetBrains Mono** for anything that is code, a command, a file name or a prompt. Rounded corners about 12px. No gradients, glows, neon, glitch effects, skulls, hooded figures or Matrix rain.

## 2. Formats

| Format | Size | Length | Captions |
|---|---|---|---|
| Fix video | 1920×1080, 30 fps | 8–15 min | .srt upload, no burned-in captions |
| "The AI Did What You Asked" | 1920×1080, 30 fps | per episode | .srt upload; series title card + five beat labels |
| Concept explainer | 1920×1080, 30 fps | 3–6 min | .srt upload |
| Short | 1080×1920, 30 fps | target under 60 s | Burned-in, middle third |

The editor **asks which format(s)** if I haven't said.

## 3. Ingest
- Snipping Tool recordings are probably variable frame rate. Always convert screen footage to **constant 30 fps** before cutting, or sound and picture will drift.
- Voiceover comes from DaVinci Resolve as a separate WAV (48 kHz). Keep it separate from the screen recording until the final mix.
- If the screen recording isn't 16:9 (or is bigger than 1080p), scale it to fit 1920×1080 with an Ink background. **Don't crop away UI the viewer needs.**

## 4. Cutting the voiceover (this is the main edit)
- Transcribe with word-level timestamps and compare to `script.md`.
- **Retakes:** when a line is said more than once, keep the **last complete take** unless I say otherwise.
- **Pauses:** shorten silences longer than about 0.7 s to about 0.35 s. Leave about 0.6 s before a new chapter or after a key point.
- **Filler words** ("um", "uh"): remove them when it's clean to do so. Never cut in the middle of a word or a breath that makes the result sound clipped.
- Flag (don't fix) anything that differs from the script in meaning: a different command, setting or number.

## 5. Fitting the screen to the voice
The voice sets the timing. The screen fits around it.
- The script's `[SCREEN: ...]` cues are the map: each cue starts at the line it sits before.
- **Waiting and typing** (page loads, deploys, long typing): speed up 2–4×, or cut with a short 6-frame crossfade.
- **Voice longer than the action:** hold on a freeze frame of the result, or use a zoom (section 7) to fill the time with something useful.
- **Never speed up** the moment the viewer has to read: the hole appearing, the fix, the verification.
- No audio from the screen recording, except a UI sound that matters (rare).

## 6. Designed elements (Remotion components)

| Component | Spec (1080p) |
|---|---|
| Title card | Ink + faint grid or `pbd-scene-bg-1920x1080.png`; title Inter Bold 96px, optional green keyword; 3–4 s |
| Chapter card | Label "STEP 2 · THE FIX", Inter Bold 28px, uppercase, letter-spaced, green; title Inter Bold 72px; about 2 s |
| Lower third | Panel, radius 12, 4px green left bar; title Inter Bold 40px, subtitle Inter Medium 28px Muted; bottom-left inside safe margins |
| Prompt card | Panel, 4px green left bar; label "PASTE THIS PROMPT" Inter Bold 24px green; body JetBrains Mono 30–34px Paper; on screen long enough to pause and read (at least 5 s, plus about 1 s per line) |
| Hole / fix label | Pill, Inter Bold 24px uppercase; red or green fill with Ink text |
| Before / after | Side by side, red "BEFORE" / green "AFTER" labels |
| Statement card | One sentence, Inter Bold 64–72px, centered |
| Series card | "The AI Did What You Asked" + beat labels: the request · it works · what quietly broke · the decision you were making · the question that would have caught it |
| Corner logo | `pbd-badge-A-padlock.png`, 64–88px tall, top-right, 40px from edges, 75% opacity, on screen recordings only |
| Outro | Last 20 s: scene background only, nothing in the end-screen areas |
| Shorts end card | `EndCard` (Remotion), styled like `brand/shorts-endcards` #2: padlock, "Want the full fix?", one line pointing to the channel, green pill "Learn more on the channel", `@publicbydefault`, wordmark. About 2.5 s, silent, no captions. |

Safe margins: 96px left/right, 54px top/bottom. Body text at least 36px. Never put text over code the viewer has to read.

## 7. Zooms and highlights
- Zoom into the part of the screen being talked about whenever the text would be too small to read on a phone (most code, most dashboard settings).
- Zoom: ease in and out over about 0.5 s, scale 1.5–2.5×. Hold while the thing is being discussed. Don't zoom in and out more than about once every 4 s.
- Highlight: green 4px rounded rectangle around the item, with the rest of the frame dimmed to about 40%.

## 8. Audio
- Voice: light noise reduction, gentle compression, high-pass about 80 Hz.
- Loudness: target about **−14 LUFS integrated, true peak no higher than −1 dBTP** (see the fact-check table).
- Music, if used: very quiet bed (about −28 LUFS under the voice), none under prompt cards. No alarm or "hacked" sound effects.

## 9. Captions
- **Long-form:** export an `.srt` from the final cut (timed to the edited voice, not the raw voice). Max 2 lines, about 42 characters per line. Proof against `script.md` for the spelling of tool names (Supabase, Lovable, `.env`, RLS).
- **Shorts:** burned in. Inter Bold 64–72px, Paper on a Panel box at about 75% opacity, current word in green, max 2 lines, middle third of the frame. 2–4 words per caption.

## 10. Shorts
- Cut from the long-form (the hook, a single fix, or a "paste this prompt" moment) or from a concept explainer.
- Reframe to 9:16: zoom into the relevant part of the screen. Don't letterbox a whole desktop.
- The hook is in the first 2 seconds.
- Put the payoff last in the edit, then **end on the Shorts end card** (§6) with a call to action to visit the channel. This is the default **unless I say otherwise** for a given Short. Keep the card short: Shorts loop, so a long silent tail costs watch time.

## 11. Delivery (`done\<slug>\`)
- `long\<slug>.mp4`: H.264, 1080p30, high quality (CRF about 18), AAC 320 kbps
- `long\<slug>.srt`, `long\chapters.txt` (YouTube chapter timestamps, starting at 0:00)
- `shorts\<slug>-short-NN.mp4` (one per Short)
- `shorts\<slug>-short-NN.txt`: the Short's **title and description** (one per Short). Call these "title and description", never "caption": captions are the burned-in subtitles and the `.srt`.
  - **Title:** under about 60 characters, built on the Short's hook. Same calm tone as the videos: no "HACKED", alarm words or all-caps.
  - **Description:** 1–2 plain sentences on what the Short shows, a line pointing to the full video (`Full fix: <long-form link>`), then 2–3 hashtags.
  - **Related video:** name the long-form to link in YouTube Studio's "Related video" field.
  - Drafted at review gate 2, next to the preview, and approved with it. The editor never uploads or publishes.

## Fact-check

| Claim | Source | Verified |
|---|---|---|
| Brand colors, fonts, sizes, logo placement | `descript-style-guide-v1.md` | Yes (carried over) |
| YouTube normalizes playback to about −14 LUFS, so −14 LUFS / −1 dBTP is a sensible target | common practice; not checked against YouTube docs in this session | **No**: verify before relying on it |
| YouTube chapters need a first timestamp at 0:00 | from memory | **No**: verify |
| Snipping Tool records at a variable frame rate | from memory; the ingest step checks this with ffprobe on every file anyway | **No** |
| Pause lengths, zoom timing, caption line lengths | my editing defaults, not a standard | n/a: adjust to taste |
| YouTube Studio lets a Short link to a "Related video" | from memory | **No**: verify in Studio |
| A long silent end card on a Short lowers watch time, because Shorts loop | editing judgement, not measured | n/a: check in analytics |
