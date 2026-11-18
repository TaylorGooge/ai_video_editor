# v_s1a cut list v2

**Length: about 6:13** (the voice now ends at 5:53.5, then the 20 s outro). Everything not listed here is unchanged from `cutlist-v1.md`. From 1:43 on, every time is about 3 s earlier than in v1.

## Your answers (17 Nov 2026)
| # | Decision | What changes |
|---|---|---|
| F1 | OK | Take 1, "what it couldn't see", stays. |
| F2 | Use the softer take | 1:40.5 "I put this pricing logic in the database for this demo," + 1:43.3 "**but it's a common setup.**" (raw 164.45–165.32). "But it's a very common setup in AI-built apps on Supabase" is cut. |
| F3 | You said "null" | No change. Captions read "Null." |
| F4 | Show only admin.js | In `03_grep_pet_fee`, the three `supabase/migrations/…_init.sql` result lines are masked with the terminal background. Only the command and the admin.js line show. |
| F5 | Skip the init.sql display | `03_app_folder_tree` is used only before `supabase/migrations` opens (folder tree with `js/` expanded), then frozen. No label. |
| F6 | Overlay the full command | A label over `06_grep_has_pets`: `git grep -n -i -E "has_?pets\|haspets"`. |
| F7 | Cut around the slips | `07_dropdown_to_yes` is cropped to the Pets → Cleaner columns (no customer name). `07_old_entries_keep_info` is cropped to the top 4 rows (Jane Smith's row out of frame). |
| F8 | Prompt numbering | **Prompt 1** (map it) card · **Prompt 2** = the blast-radius query card (condensed on screen, full query in the description) · **Prompt 3** (make it safe) card. |

## New: typing sound
Quiet keyboard typing under the animated Claude Code prompts (0:11.9, 1:59.7-ish, 3:46) and while the three cards in section 8 build in. There's no typing-sound file in the project, so I'm generating a soft keyboard sound with ffmpeg: short filtered clicks at a natural typing rhythm, about −30 LUFS, well under the voice. If last time's sound came from a file, send it and I'll use that instead.
