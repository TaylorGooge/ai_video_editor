# Cut list v2: 10_blob Shorts (approved: all three)

Changes from v1:
- All three Shorts approved.
- Flag 2 (Short 02): **option (a)**, the default. The source picture is kept: the Table Editor stays on screen during the "network tab / F12" line. You didn't pick an option, so I took the one that changes nothing. Say (b) at the preview and I'll switch it.
- Short 01: the 3.3 s pause after the first line is **cut** rather than sped up. The title card covers the line before it, so the typing in the gap isn't needed.
- Short 01: segment 2 now starts at "here's a bad connection" (drops a leading "So").
- Short 02: segment 2 drops the leading "One,". **Freeze frame:** the line "only my phone number. Nobody else's." (5:37–5:41) holds on the frame from **5:44.0**. That's where the profiles response `[{"display_name":"Dev","phone":"555-0102"}]` is actually open; during the line itself the screen still shows the posts response. The "I forgot to record it again :(" text appears ≈5:45, so it isn't in the frame.
- New **flag 5** (below) affects Short 03.

Layout (all three): 1080x1920 Ink. Header (green label + Short title) at top. Screen panel centred at y≈720, max 860 tall, cropped and scaled to 1080 wide. Captions in the middle third, box centred at y≈1225. Bottom ≈600 px left clear for the YouTube Shorts UI.

## Short 01: "One bad save" (≈ 37.3 s)
| # | Audio (source) | Picture |
|---|---|---|
| 1 | 0:00.00–0:03.21 | VerticalTitleCard: "FIX VIDEO · SUPABASE" / "One bad save" (green) "deleted my entire app" |
| 2 | 0:06.10–0:12.47 | crop x100 y340 1140×400 (Dev post box) |
| 3 | 0:12.47–0:15.60 | crop x500 y40 900×700 (empty board + trash can) |
| 4 | 3:16.75–3:33.85 | crop x480 y0 980×780 (Corkboard column) |
| 5 | 4:19.95–4:27.45 | RowsCard (payoff): "THE FIX / Give every post its own row" |

## Short 02: "Hidden isn't private" (≈ 18.2 s)
| # | Audio | Picture |
|---|---|---|
| 1 | 1:43.95–1:47.97 | crop x1140 y480 620×420 (Response JSON with phones) |
| 2 | 1:47.97–1:55.45 | crop x0 y130 920×300 (Table Editor, `app_state`): flag 2 (a) |
| 3 | 5:35.20–5:37.10 | crop x460 y250 1000×560 (fixed posts response) |
| 4 | 5:37.10–5:41.90 | **freeze @5:44.0**, crop x730 y262 500×70 (profiles response: Dev only) |

## Short 03: "Two people, one save" (≈ 42.6 s)
| # | Audio | Picture |
|---|---|---|
| 1 | 2:15.55–2:36.30 | split: top = Maria (source right, x1000 y0 920×366); bottom = Dev (source left, x10 y0 920×366); name pills on each |
| 2 | 2:36.30–2:37.30 (room tone) | split, video 2:36.30–2:41.50 sped up 5.2× (both refreshes) |
| 3 | 2:41.50–2:57.20 | split, normal speed (the reveal) |
| 4 | 4:19.95–4:25.30 | RowsCard (same payoff) |

## Flags
1. 5:42–5:50: the two-window test is described, not shown. Not used.
2. ≈1:47–1:55: the network-tab line plays over the Table Editor. Used as is in Short 02, option (a).
3. ≈5:12–5:24: the backups line plays over the Auth docs. Not used.
4. Whisper spelled Supabase three different ways. The captions spell it correctly (not said in these ranges anyway).
5. **New, 2:17–2:20: left/right swapped.** The voice says "Maria on the left, Dev on the right", but the screen has **Dev on the left and Maria on the right**. This is in the published long-form too. In Short 03 the windows are stacked, so "left/right" doesn't match either way. I've put **MARIA** / **DEV** name pills on each pane so it's clear who's who, but the words still say left/right. Your options: keep it, trim the line to "Two people have the app open." (drops 2.7 s), or re-record that phrase.

## Changes after preview v1 (→ preview v2)
- Short 03: trimmed "Maria on the left, Dev on the right." Audio 2:17.55–2:20.30 removed, cut placed in the pauses on both sides. Short 03 is now 40.1 s.
- Captions: words Whisper timed across a cut are now kept ("deleted" in 01, "Both" in 03), and a word after a full stop is capitalized ("Here's" in 01).
- Preview v3: 2.5 s silent end card (call to action to the channel) appended to all three.
