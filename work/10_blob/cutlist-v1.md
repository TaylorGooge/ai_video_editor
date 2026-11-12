# Cut list v1: 10_blob Shorts (from the finished long-form)

Source: `raw\v_10b_youtube.mov` (7:07, 1920x1080 CFR 30, voice and picture already edited).
Times are **source** times (m:ss.ss), taken from Whisper word timestamps.
Because the long-form is already edited, there are no retakes or filler to remove. The only voice cuts are range in/out points and one or two pauses.

Common to all three:
- 1080x1920, 30 fps. Burned-in captions per spec §9: Inter Bold 68px, Paper on a Panel box at 75%, current word green, 2–4 words, middle third.
- Captions spell **Supabase** correctly (Whisper heard "Superbase"/"Sukabase"). None of the three ranges below says the word anyway.
- No corner logo (the source has none, and the spec only puts it on 16:9 screen recordings). No subscribe end card: the Short ends on the payoff.
- Audio: taken from the finished mix. Loudness-normalize to −14 LUFS / −1 dBTP (the source is −23.9 LUFS). 4-frame audio fades at every join.

---

## Short 01: "One bad save" (≈ 37 s), recommended first

| # | Source in → out | Voice | Picture (9:16 treatment) |
|---|---|---|---|
| 1a | 0:00.00 → 0:02.86 | "This app had 20 posts from five users." | **New vertical title card** (Remotion): "One bad save deleted my entire app". The source title card is 16:9 and would be cut off by a crop. |
| — | ~~0:02.86 → 0:06.16~~ | *(3.3 s pause)* | Cut down to 0.35 s. The screen action in the gap (typing a post) gets sped up ~3× under 1b. |
| 1b | 0:06.16 → 0:15.30 | "I clicked post once. Now it has zero. It wasn't a hacker and nobody broke in. The app deleted itself because of how it stores its data." | Crop on the Corkboard column: the post box, then the empty board with the green trash can. |
| 2 | 3:16.38 → 3:33.60 | "So here's a bad connection for one second. The page loads empty. Then I post like anyone would… everything gone in one request, no hacker and no typo in the code." | Crop on the Corkboard column: "No posts yet" → typing "Hey where did everyone go???" → the board with just that post. The desert-road meme (≈3:31) is inside the crop, so it stays. |
| 3 | 4:20.08 → 4:27.30 | "The fix is to stop storing the app in one box. Each post gets its own row. Each profile gets its own row." | **Payoff.** The source shows the 16:9 "Give every post its own row" card. Rebuild it vertically (one box → grid of rows), or scale it to fit width on Ink. Recommend rebuilding. |

Why this one: the hook ("I clicked post once. Now it has zero.") lands inside 2 s, and the bad-connection demo is visual on its own.

## Short 02: "Hidden isn't private" (≈ 19 s)

| # | Source in → out | Voice | Picture |
|---|---|---|---|
| 1 | 1:44.10 → 1:55.32 | "Here's every user's private phone number. The app just doesn't display it. Hidden on the screen is not the same as private. If it's in the network tab, anyone who presses F12 can read it." | 1:44–1:47: zoom ~2× on the Network → Response JSON showing `"phone": "555-0101"…"555-0105"`. **See flag 2:** from ≈1:47 the source cuts to the Supabase Table Editor while the voice is still talking about the network tab. |
| 2 | 5:35.28 → 5:41.56 | "Open the network tab. The page now gets the posts and only my phone number. Nobody else's." | **Payoff.** Zoom on the fixed Response: `[{"display_name":"Dev","phone":"555-0102"}]`. |

Option: start earlier at 1:35.90 ("So this is what every user's browser receives…"), which runs ≈ 27 s but gives a weaker first 2 s.

## Short 03: "Two people, one save" (≈ 42 s)

| # | Source in → out | Voice | Picture |
|---|---|---|---|
| 1 | 2:15.68 → 2:35.90 | "Two people have the app open. Maria on the left, Dev on the right… His app adds his post to his old copy and saves the whole thing." | **Stacked split-screen:** Maria's window (left in the source) on top, Dev's (right) on the bottom. Each is cropped to the banner, the post box and the top 3–4 posts. This 2-up layout suits 9:16 well. The pink arrows at ≈2:16 stay. |
| — | ~~2:35.90 → 2:41.62~~ | *(5.7 s pause while both windows refresh)* | Cut to ~1.0 s. Screen sped up ~4× so both refreshes stay visible. |
| 2 | 2:41.62 → 2:56.30 | "Maria's post is gone. Overwritten. No error message. No bug in the code… So it gets worse as you succeed." | Same split. Both boards now show only "Where is everybody?". The googly-eyes overlay is inside the crop. **Don't speed this up:** this is the reveal. |
| 3 | 4:20.08 → 4:25.06 | "The fix is to stop storing the app in one box. Each post gets its own row." | Same payoff card as Short 01 (reuse it). |

The ideal payoff would be the fixed two-window test passing, but it wasn't recorded (flag 1).

---

## Flags (voice vs screen in the published long-form, not fixed here)

1. **5:42–5:50: two-window test not shown.** The voice says "Maria posts, Dev posts, refresh. Both are still there," but the screen shows the text "I forgot to record it again :(" over the fixed app and console. Viewers are told the verification passed without seeing it. The finished video says it this way on purpose, but no Short should use this range.
2. **≈1:47–1:55: network tab talk over the Table Editor.** "If it's in the network tab, anyone who presses F12 can read it" plays over the Supabase Table Editor (`app_state`), not the network tab. For Short 02 you choose: (a) keep the source picture as is, or (b) hold the network-response shot through this line. I won't do (b) unless you say so.
3. **≈5:12–5:24: backups talk over unrelated screens.** "Export your data on a schedule… Supabase keeps daily backups for seven days" plays over the Supabase Auth docs page and a Table Editor context menu. It isn't in any Short. Noting it only.
4. **Pronunciation of Supabase.** Whisper wrote it three different ways (Superbase ×2, Sukabase ×4) despite the prompt. That's probably just Whisper, but listen to 1:55, 4:06 and 5:17 if you care how it sounds.

## Build notes (affect effort, not the edit)

- `remotion\` has no source yet. Building these Shorts means creating, as reusable components: **ShortCaptions** (word-highlight), **VerticalTitleCard**, and **VerticalStatementCard / one-box-vs-rows card**. Inter and JetBrains Mono aren't in `brand\`, so I'd add `@remotion/google-fonts` (one npm package) unless you have font files to drop in.
- Everything else (crops, speed-ups, joins, loudness) is ffmpeg. The renders are short, so the 720p previews should take a few minutes each on this machine.

## Approve / edit
Tell me which Shorts to make (01, 02, 03, or all three), and for Short 02, flag 2 option (a) or (b). I'll apply your changes as `cutlist-v2.md`, then build the 720p previews.
