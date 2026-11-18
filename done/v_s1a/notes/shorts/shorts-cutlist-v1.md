# v_s1a Shorts: cut list v1 (review gate 1)

Source: `done\v_s1a\long\v_s1a.mp4` (the approved final). Times below are long-form times.
Every Short: 9:16, header label + title on top, burned-in captions, ends on the Shorts end card (~2.5 s).
Long-form link for descriptions: https://youtu.be/mHklVwrxhj8

**Why these three (funnel):** each one opens a question the Short doesn't fully answer, and the answer is in the full video.
01 = "why did it miss the fee?", 02 = "so how *do* you check?", 03 = "how do you do the four changes in order?".
"Null is not 'no'" (2:47) is the best fit as a swap, but it answers itself in 30 s, so it gives viewers less reason to click through.

---

## Short 01: "It never mentioned the price" (~33 s)
Hook first, then the story, then the price.

| # | Long-form | Voice | Picture (9:16) |
|---|---|---|---|
| 1 | 0:11.9–0:17.6 | "Ten minutes ago, I asked my AI to remove one question from this form. It did exactly that." | Claude Code prompt typing "Remove the 'Do you have pets?' question…", cropped to the prompt box |
| 2 | 0:00.0–0:11.9 | "A customer books a cleaning… 'We have two cats.' …no pets, no pet fee, and it just sent the cleaner who's allergic to cats." | Booking form → staff table → Jane Smith row, Ana "cat allergy" highlight (crops follow the long-form zooms) |
| 3 | 0:17.7–0:21.2 | "It even warned me about part of this, not the part that costs money." | Jane Smith row, $150.00 circled |
| 4 | 1:03.2–1:12.9 | "This booking should be $165. $150 for two bedrooms, plus a $15 pet fee. The fee is gone, and the AI never mentioned it." | Same row + "$150 + $15 pet fee = $165" + NO PET FEE tag |
| 5 | — | (silent) | End card |

Editing note: 1 and 2 are swapped compared with the long-form so the hook ("I asked my AI to remove one question") lands in the first 2 s.
The Short ends on an open question (why didn't it see the fee?), which the full video answers.

## Short 02: "It could see the database. Still $150." (~47 s)

| # | Long-form | Voice | Picture (9:16) |
|---|---|---|---|
| 1 | 1:10.1–1:12.9 | "The fee is gone, and the AI never mentioned it." | Row with $150 circled + NO PET FEE |
| 2 | 1:50.1–1:52.7 | "So when the AI searched my project, there was nothing to find." | Long-form picture at that moment, cropped |
| 3 | 1:59.8–2:03.3 | "I gave it read access to the database and asked the exact same thing." | MCP server screen, "read_only=true" (see flag 1: frozen past the path) |
| — | ~~2:04.0–2:05.9~~ | ~~"Fresh session, same prompt."~~ | cut: saves 2 s, adds nothing in a Short |
| 4 | 2:06.3–2:41.7 | "This time it went further… Unknown now means 'might have pets'… goes to Ben now. Better. But… Ana… gets no new jobs until someone on staff fills in the pets answer by hand. That's a reasonable call. It's also a business decision about your staff's work. The AI made it for you, and the price is still $150. It had access to the database. It didn't look at what uses the column. Having access isn't the same as checking." | matching.js diff → admin.js diff → row (Unknown, Ben) → Claude's reply → row with $150 circled |
| 5 | — | (silent) | End card |

## Short 03: "'Remove the question' is four changes" (~31 s)

| # | Long-form | Voice | Picture (9:16) |
|---|---|---|---|
| 1 | 3:04.8–3:17.9 | "'Remove the question' sounds like one change. It's four. Stop asking, stop saving, stop using it. And decide what happens to the answers you already have. The AI did the first two, because that's what I asked for." | The four-item checklist building in, first two ticked, last two "not done" (cropped from the long-form) |
| 2 | 5:00.0–5:09 | "Before you remove any field, paste this. It's in the description." + ~5 s hold | **Prompt 1 · Map it**, re-rendered as a 9:16 card. The long-form card is too wide to crop: its text would be ~20 px tall on a phone |
| 3 | 5:40.9–5:47.6 | "The AI can find a lot of where. Make sure it can see everywhere. And decide what 'remove' means before it does." | Long-form picture at that moment, cropped |
| 4 | — | (silent) | End card |

"It's in the description" stays true: Prompt 1 goes in this Short's description. The query (Prompt 2) and Prompt 3 are left for the full video.

---

## Thumbnails (one per Short, 1080x1920 PNG)
Same style as `v_s1a-thumbnail.png` (HTML → PNG via headless Edge). Text stays in the middle of the frame, because YouTube crops Shorts thumbnails differently in different places.
- **01:** The staff-page row with **$150.00** circled, and above it "It never mentioned the price."
- **02:** "Read access to the database", then "**$150**" still circled: "Access isn't checking."
- **03:** The checklist, two ticked and two open: "'Remove the question' = 4 changes."

Titles and descriptions get drafted at gate 2, next to the previews (spec §11).

## Captions: Whisper fixes
"Anna" → Ana, "bed" → Ben (2:16), "for" → four (3:07), "150" → $150.

## Flags
1. **The published long-form shows a local path for about 0.3 s at 1:59.7–2:00.0.** The "Manage MCP servers" screen has `Project MCPs (C:\Users\taylo\OneDrive\Documents\Professional Development\YouTube Concepts\…)` unblurred. It was on the blur list in the edit notes, but this frame got through. It's very short, but someone can pause on it. In Short 02 I'll freeze a later frame over that moment. For the long-form, you could blur it with YouTube Studio's Editor ("Blur" → custom blur) without re-uploading, or I can re-render and you can re-upload.
2. Short 03 is cut from two places 2 minutes apart in the long-form. The voice jumps from "that's what I asked for" to "Before you remove any field". I think it reads fine. Tell me if it feels abrupt in the preview.
