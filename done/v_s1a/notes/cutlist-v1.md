# v_s1a cut list v1: "My AI Removed One Form Field. It Never Mentioned the Price"

**Format:** 16:9 long-form, 1920×1080, 30 fps, series "The AI Did What You Asked". Captions go in an .srt file (nothing burned in).
**Estimated length: about 6:17.** That's 5:56 of picture (voice plus card and demo holds) and the 20 s outro. The script estimated 8:10, but that included demo pauses. Your read is tight, and with retakes and long pauses removed the voice is about 5:05.

Times are in the **edited** timeline. Raw = seconds in `Recording.wav`. The voice EDL is in `cutplan.py` and `cutplan.json`.

---

## ⚑ Flags: please decide on these

| # | Where | What | My suggestion |
|---|---|---|---|
| F1 | 0:21 | **Retake choice.** Take 1 says "what it **couldn't** see" (matches the script and the video's point). Take 2, the last take, says "what it **didn't** see". | I used **take 1**, against the "last take" rule, because "couldn't see" is the point of section 3. Say if you want take 2. |
| F2 | 1:43 | **Unverified claim.** The VO says "it's a **very** common setup in AI-built apps on Supabase". The script's fact-check table marks this as unsourced ("soften … or cut 'very common'"). | You also recorded a softer take: "I put this pricing logic in the database for this demo, **but it's a common setup.**" I can use that and drop the "AI-built apps on Supabase" sentence. **A:** keep "very common" (current). **B:** use the softer take. |
| F3 | 3:02 | Whisper heard "Now new bookings say nothing. **No.**" The script says "**Null.**" If you actually said "no", it says the opposite of the point. | I'll listen in the preview. If it's "no", re-record that one word or cut it ("…say nothing."). |
| F4 | 1:15–1:23 | **Screen vs VO.** "The pet fee is displayed on the staff page, but nothing in the code calculates it." The `git grep "pet_fee"` result shows `admin.js` **plus 3 hits in `supabase/migrations/20261117000000_init.sql`**: the column, the view, and `b.base_price + b.pet_fee as total`. The script said the hits were "only … in admin.js". | It's still true that nothing *calculates the fee* in code. I'll highlight the admin.js line and leave the migration lines visible but dimmed. You may want to know that a sharp viewer will see SQL hits. |
| F5 | 1:53 | **Screen vs VO.** "When the AI searched my project, there was nothing to find." In `03_app_folder_tree`, the app folder **does** have a SQL file (`supabase/migrations/…_init.sql`, with tables, view and RLS but no trigger), and the clip opens it. | Use only the first 4 s (folder tree with `supabase/migrations` expanded) and add a label: "`init.sql`: tables, view, RLS · **no pricing trigger**". Or skip the file-opening part entirely. |
| F6 | 3:52 | **Command differs.** On screen you typed `git grep -E "has_?pets\|haspets"`. The script and `blast-radius.sql` (and so the description) say `git grep -n -i -E "has_?pets\|haspets"`. The VO doesn't read it out. | Keep the footage and put the full `-n -i` version in the description. Or I can overlay the full command as a label. |
| F7 | 4:55–5:02 | **Footage continuity.** (a) The verify booking is typed as "Jane **Doe**", but the staff row that gets "We have a dog." shows customer "**test** / test@test.com". (b) Jane **Smith**'s row is Yes / $165 / Chloe in `07_dropdown_to_yes` but Unknown / $150 / Ben in `07_old_entries_keep_info`. | Crop around both: for 07_dropdown, zoom on the Pets → Cleaner columns so the customer name is out of frame; for 07_old_entries, zoom on the top 4 rows (Jordan, Priya, Alex, Sam) so Jane Smith's row is out of frame. Nothing needs re-recording. |
| F8 | 5:21–5:48 | The cards are "Prompt 1" and "Prompt 3". There's no Prompt 2 in the video, and the VO doesn't introduce Prompt 3 (it's a silent 14 s card). | Label them "Prompt 1: map it" and "Prompt 2: make it safe" on screen and in the description. Say if you'd rather keep the script's numbering. |
| F9 | (whole video) | The fact-check still says Prompt 1 and Prompt 3 are **not tested**. Nothing in the VO claims they work (good). | No change. The description won't claim the prompt finds the trigger either. |

**Blurs (from your notes plus what I found):** the terminal path (`C:\Users\taylo\OneDrive\…`) in `03_grep_pet_fee` and `06_grep_has_pets`. In `04_mcp_connection`, the URL's `project_ref` value and the "Config location" path, keeping `read_only=true` readable because the VO says "read access". The VS Code "Recent" list in `03_app_folder_tree` (0–4 s) shows OneDrive paths. I'll blur that list or cut past it.

---

## Voiceover edit

Pauses longer than 0.7 s inside a kept line are shortened to 0.4 s (spec §4). There's 0.6 s before each new section. "Mm-hmm" at raw 360.8 is removed.

| Edited | Raw | Line | Note |
|---|---|---|---|
| 0:00.4 | 1.62 | A customer books a cleaning. In the notes, they write: "We have two cats." | |
| | 6.66 | ~~On the staff page, the app says: no pets. No pet fee. And it just sent the cleaner who's allergic to cats.~~ | retake |
| 0:05.0 | 14.68 | On the staff page, the app says: no pets. No pet fee. And it just sent the cleaner who's allergic to cats. | |
| 0:11.9 | 22.22 | Ten minutes ago, I asked my AI to remove one question from this form. It did exactly that. It even warned me about part of this. Not the part that cost(s) money. | |
| 0:21.6 | 32.48 | Let's look at what it saw, what it **couldn't** see, and how to remove a field without breaking the things that depend on it. | **F1** (take 1) |
| | 43.77 | ~~Let's look at what it saw, what it didn't see, and how…~~ | F1 |
| 0:27.4 | 49.84 | Prompts and a check query are at the end. | |
| 0:29.8 | | *[series card 3.5 s, chapter card 2 s]* | |
| 0:35.4 | 54.72 | Here's the change. Two files. The question is gone from the form, and the line that saved the answer is gone too. Clean. | |
| | 63.77 | ~~And it didn't stay quiet. It told me new bookings would save the pets answer as blank. It told me the cleaner matching…~~ | incomplete take |
| 0:43.5 | 74.97 | And it didn't stay quiet. It told me new bookings would save the pets answer as blank. It told me the cleaner matching treats blank as "no pets". So a cleaner with a cat allergy could get a home with pets. | |
| | 87.05 | ~~And the "needs pet-friendly cleaner" badge would stop showing.~~ | retake |
| 0:55.0 | 91.53 | And the "needs pet-friendly cleaner" badge would stop showing. | |
| 0:58.9 | 96.22 | That's a good answer. Everything it mentioned was true. But look at the price. This booking should be $165. $150 for two bedrooms, plus a $15 pet fee. The fee is gone, and the AI never mentioned it. | |
| 1:13.2 | | *[chapter card 2 s]* | |
| 1:15.4 | 114.12 | So I searched the code. The pet fee is displayed on the staff page, but nothing in the code calculates it. It's calculated in the database. | F4 |
| | 123.39 | ~~This query lists everything in the database that uses the pet column.~~ | retake ("pet column") |
| 1:23.4 | 127.99 | This query lists everything in the database that uses the pets column. | |
| | 134.62 | ~~There's a view the staff page reads.~~ | retake |
| 1:27.3 | 138.66 | There's a view the staff page reads. And there's a trigger, a little function that runs on every booking. Here it is. If the customer has pets, $15. Otherwise, zero. And "otherwise" includes "we never asked." | |
| 1:40.4 | 155.73 | I put this pricing logic in the database for this demo. | take 1 (take 2 has a 2.5 s stumble) |
| | 158.94–172.98 | ~~I put this… but it's a common setup. / But it's a very common setup… (×2, one with "and in")~~ | retakes; **F2 option B** uses 158.94–165.32 |
| 1:43.3 | 174.75 | But it's a very common setup in AI-built apps on Supabase. | **F2** (take 4) |
| 1:47.5 | 179.24 | Your AI tells you to paste some SQL into the dashboard, you do, and it never ends up in your code. So when the AI searched my project, there was nothing to find. Its map of "where is this used" stops at what it can read. | F5 |
| 2:00.3 | | *[chapter card 2 s]* | |
| | 194.39 | ~~So I gave it access to the database… Fresh session, same prompt.~~ | retake (no "read") |
| 2:02.7 | 200.30 | So I gave it read access to the database and asked the exact same thing. Fresh session, same prompt. This time it went further. Without asking, it changed the cleaner matching. Unknown now means "might have pets". And the staff page shows "Unknown" instead of "No". The cats booking goes to Ben now. Better. | |
| 2:24.6 | 226.50 | But look at what that decision means. Ana, the cleaner with the allergy, now gets no new jobs until someone on staff fills in the pets answer by hand. That's a reasonable call. | |
| | 237.09 | ~~It's also a business decision about your staff's work.~~ | retake |
| 2:34.6 | 239.83 | It's also a business decision about your staff's work. The AI made it for you. And the price is still 150. It had access to the database. It didn't look at what uses the column. Having access isn't the same as checking. | |
| | 256.74 | ~~Which questions are yours to answer? I made a short about that. It's linked above.~~ | retake |
| 2:47.9 | 262.65 | Which questions are yours to answer? I made a short about that. It's linked in the description. | "linked in the description": S1b goes in the description |
| 2:53.3 | | *[chapter card 2 s]* | |
| 2:55.7 | 270.33 | Here's the core of the problem. Before, every booking said yes or no. Now new bookings say nothing. Null. | **F3** |
| | 279.12 | ~~And every place that reads the answer was written for yes or no.~~ | retake |
| 3:02.8 | 283.17 | And every place that reads the answer was written for yes or no. The staff page, the matching, the price. Each one treats "we didn't ask" as "no". "Remove the question" sounds like one change. It's four. Stop asking. Stop saving. Stop using it. And decide what happens to the answers you already have. The AI did the first two, because that's what I asked for. | |
| 3:24.5 | | *[chapter card 2 s]* | |
| 3:26.9 | 308.28 | So here's how to remove a field without this. The order matters. One: decide. … Two: map out everything that uses it. Ask your AI for a full list, and ask what it couldn't check. Then search the code yourself, and run this query in your database. That's the one that finds the trigger. | |
| | 345.92 | ~~Three, make everything handle unknown first, before you remove the question.~~ | retake |
| 3:58.1 | 351.13 | Three: make everything handle "unknown" first, before you remove the question. | |
| | 357.57–378.30 | ~~Matching only a confirmed… / Mm-hmm / Matching. Only… Staff page… (two earlier takes)~~ | retakes, filler |
| 4:03.0 | 379.83 | Matching: only a confirmed no-pets home can go to a cleaner with an allergy. | last take |
| | 384.58–389.29 | ~~Staff page. Unknown. A "Confirm pets with customer" badge.~~ | retake |
| 4:07.4 | 390.80 | Staff page: "Unknown", a "Confirm pets with customer" badge, and a dropdown so staff can set yes, no or unknown. | last take |
| 4:15.6 | 399.75 | The trigger can stay as it is. Unknown means no automatic fee, which is our decision. And it re-runs whenever staff update the booking. Four: then remove the question. | |
| | 410.53 | ~~That's the part the AI already did.~~ | retake |
| 4:25.1 | 412.89 | That's the part the AI already did. | |
| 4:27.6 | 415.77 | Five: drop the column later. Or never. | |
| | 419.96 | ~~Here we're keeping it, because staff still record pets.~~ | retake |
| 4:30.2 | 422.42 | Here we're keeping it, because staff still record pets. If you do drop it, run the dependency query first, and never add "cascade" just to make an error go away. | |
| 4:41.6 | | *[chapter card 2 s]* | |
| | 436.56 | ~~Don't trust the summary. Check it. Same booking as the start.~~ | retake |
| | 448.17 | ~~Don't trust.~~ | false start |
| 4:44.0 | 449.20 | Don't trust the summary. Check it. Same booking process as the start. | then a 3 s hold for the booking |
| 4:51.6 | 454.52 | Unknown. Flagged for staff. Auto-assign skips Ana. Staff confirm the dog. The pet fee appears: $165. Old bookings keep their answers. And everything the query found, you've made a decision about. | |
| 5:05.7 | | *[chapter card 2 s]* | |
| 5:08.1 | 473.63 | Before you remove any field, paste this. It's in the description. | then a 10 s hold on Prompt 1 |
| 5:21.8 | 478.38 | Then run this yourself, in the Supabase SQL editor. Change the table and column names. It's in the description too. | then a 6 s hold on the query, and a 14 s silent Prompt 3 card |
| 5:48.9 | 487.65 | The AI can find a lot of *where*. | take 1 (take 2 has a 3 s pause mid-line) |
| 5:51.0 | 497.53 | Make sure it can see everywhere. And decide what "remove" means before it does. | take 2 |
| 5:57.5 | | *[outro 20 s: scene background, no logo, end screen: S1b + 10a]* | ends **6:17** |

---

## Picture

**Layout:** every clip is a crop at a different size. I'll scale each one to fit inside the 96/54 px safe margins on Ink (#0D1117), never cropping UI the viewer needs (except where F7 says to zoom past it). **Zoom** means ease 0.5 s, 1.5–2.5×. **Highlight** means a green 4 px rounded box with the rest dimmed to 40%. **Circle** means a red ring, used only on the problem ($150.00, Ana). **Corner logo** goes top-right on screen recordings only, once I've checked the corner is empty in each clip.

### 1. Hook (0:00–0:29.8)
| Edited | Screen | Treatment |
|---|---|---|
| 0:00.0–0:05.0 | `01_hook_naive` 0:00–0:24 (typing the booking) | **Speed up ~5×.** Ease to "We have 2 cats." in the notes on "two cats" (0:03.9), then submit. |
| 0:05.0–0:11.9 | `01_hook_naive` 0:27–0:36 (staff page, Jane Smith row) | Zoom on the row. Click **Auto-assign → Ana · cat allergy** timed so Ana lands on "allergic to cats" (~0:10). Soft emphasis on **No** (0:06.8) and **$150.00** (0:07.9), then freeze. |
| 0:11.9–0:21.5 | **Remotion: Claude Code prompt** (new `ClaudePrompt` component) | Types: Remove the "Do you have pets?" question from the booking form. Enter on "It did exactly that" (0:16.0). |
| 0:21.5–0:29.8 | same prompt screen, idle | Calm hold. *Optional:* on "Not the part that cost money" (0:19.7), cut to the frozen row with **$150.00 circled**. |
| 0:29.8–0:33.3 | **Series card** | "THE AI DID WHAT YOU ASKED" + episode title + the five beat labels (spec §6). |

### 2. What the AI did (0:33.3–1:13.2)
| Edited | Screen | Treatment |
|---|---|---|
| 0:33.3 | **Chapter card** | IT WORKS · What the AI did, and what it said |
| 0:35.4–0:40.0 | `02_code_diff_index_html` | Zoom on the red `<fieldset>…Do you have pets?` block. Freeze to fill. |
| 0:40.0–0:43.0 | `02_code_diff_bookings_js` | Zoom on the red `has_pets: f.pets.value === 'yes',` line. |
| 0:43.5–1:01.3 | **Remotion: Claude Code response** (new `ClaudeResponse` component), text from your notes | Streams in quickly (~1.5 s). Highlights: the **`js/booking.js`** bullet on "save the pets answer as blank" (0:44.9). **"The catch: pet homes can go to cat-allergic cleaners."** plus the matching.js bullet on "cleaner matching" (0:48.2). The **badge line** on "badge would stop showing" (0:55.0). Unhighlight on "That's a good answer". |
| 1:01.9–1:12.7 | `01_hook_naive` freeze (Jane Smith row: No · $150.00 · Ana) | **Circle $150.00** on "look at the price". On "$150 for two bedrooms plus a $15 pet fee", a small Panel label under it: "should be **$150.00 + $15.00 pet fee = $165.00**". Red pill "NO PET FEE" on "The fee is gone". |

### 3. Where the fee lives (1:13.2–2:00.3)
| Edited | Screen | Treatment |
|---|---|---|
| 1:13.2 | **Chapter card** | WHAT QUIETLY BROKE · Where the fee lives |
| 1:15.4–1:23.2 | `03_grep_pet_fee` | **Blur path.** Typing 0:00–0:07 at 3×, then results. Highlight the **admin.js** hit on "displayed on the staff page". Migration hits stay visible but dimmed (**F4**). |
| 1:23.4–1:32.2 | `03_check_blast_radius` | Pasting and Run at 2×, so results appear at ~1:26. Highlight **view admin_bookings** on "a view" (1:27.5), then **function set_booking_price + trigger** rows on "trigger" (1:29.6). Freeze. |
| 1:32.2–1:53.0 | `03_trigger_body` (static) | Zoom and highlight `new.pet_fee := case when new.has_pets then 15 else 0 end;`. Extra emphasis on `else 0` at "Otherwise, zero". Ease back out at 1:40 ("I put this pricing logic…") and hold. |
| 1:53.0–2:00.3 | `03_app_folder_tree` 0:00–0:04 (folder tree, migrations expanded) | **Blur the Recent list.** **F5**: label it "`init.sql`: tables, view, RLS · no pricing trigger", or skip it. |

### 4. Same prompt, database connected (2:00.3–2:53.3)
| Edited | Screen | Treatment |
|---|---|---|
| 2:00.3 | **Chapter card** | THE DECISION YOU WERE MAKING · Same prompt, database connected |
| 2:02.7–2:09.5 | `04_mcp_connection` 0:08–0:16 (`/mcp` → supabase: connected) | **Blur `project_ref` and Config location.** Highlight `read_only=true` on "read access". |
| 2:09.5–2:11.4 | Remotion `ClaudePrompt` (same prompt, already typed) | On "Fresh session, same prompt." |
| 2:11.4–2:19.0 | `04_code_diffs_all` 0:18–0:27 (matching.js diff) | Zoom on `booking.has_pets === false ? true : !c.cat_allergy` and the comment "treat that as 'may have pets'". |
| 2:19.0–2:22.3 | `04_code_diffs_all` 0:06–0:09 (admin.js diff) | Zoom on `'Unknown'` on line 101. |
| 2:22.3–2:24.6 | `04_hook_ben` ~0:26.5–0:31 | Zoom on Jane Smith row: Unknown · $150.00. Click Auto-assign so **Ben** lands on "Ben" (2:23.1). |
| 2:24.6–2:39.4 | **Remotion `ClaudeResponse`** (run-2 text from your notes) | Highlight **"Allergic cleaners are skipped by default: … edit checkbox."** from "But look at what that decision means" (2:24.6) to "made it for you". |
| 2:39.4–2:41.4 | `04_hook_ben` freeze | **Circle $150.00** on "the price is still 150". |
| 2:41.5–2:47.4 | `ClaudeResponse` (same) | Highlight **"The database still has the pets column, the pet fee … I left them alone."** |
| 2:47.9–2:53.3 | same, plus a **lower third** | "S1b · Your AI Knows Where. Only You Know Why." / "Link in the description". Bottom-left. |

### 5. Null is not "no" (2:53.3–3:24.5)
| Edited | Screen | Treatment |
|---|---|---|
| 2:53.3 | **Chapter card** | THE DECISION YOU WERE MAKING · Null is not "no" |
| 2:55.7–3:02.8 | `05_sql_editor` | Run is clicked at ~0:05, so results land on "Now new bookings say nothing" (2:59.8). Zoom on the results. Highlight **NULL · 1** on "Null" (3:02.2, **F3**). |
| 3:02.8–3:11.0 | **Remotion: three stacked code cards** (JetBrains Mono, re-typeset from the original code, not screenshots) | `admin.js`: `b.has_pets ? '🐾 Yes' : 'No'`. `matching.js`: `booking.has_pets ? !c.cat_allergy : true`. Trigger: `case when new.has_pets then 15 else 0 end`. Each lights up on "staff page" (3:05.8), "matching" (3:06.8) and "price" (3:07.5). On "treats we didn't ask as no", the `'No'` / `true` / `else 0` branches get small red pills reading "null → no". |
| 3:11.4–3:24.5 | **Remotion: checklist** | The four lines appear on their words: Stop asking (3:14.7) · Stop saving (3:15.9) · Stop using (3:17.1) · Decide what happens to the old answers (3:18.3). On "The AI did the first two", lines 1–2 get green checks and lines 3–4 an amber "not done". |

### 6. The fix (3:24.5–4:41.6)
| Edited | Screen | Treatment |
|---|---|---|
| 3:24.5 | **Chapter card** | THE QUESTION THAT WOULD HAVE CAUGHT IT · Remove a field in order |
| 3:26.9–3:46.0 | **Remotion: five-step list** (Decide · Map everything · Handle "unknown" first · Remove the question · Drop the column later, or never) | Each step lights up on its number. On step 1, the four "for this business" sub-points fade in on their words (3:36.7–3:45.1). |
| 3:46.0–3:48.8 | five-step list | Step 2 lit. |
| 3:48.8–3:52.0 | Remotion `ClaudePrompt` typing **Prompt 1** (fast) | On "Ask your AI for a full list". |
| 3:52.0–3:54.1 | `06_grep_has_pets` 0:02–0:05 | **Blur path.** Results. **F6** |
| 3:54.1–3:58.1 | `06_blast_radius` 0:04–0:08 | Highlight the **trigger** row on "finds the trigger". |
| 3:58.1–4:03.0 | five-step list | Step 3 lit. |
| 4:03.0–4:07.4 | `06_matching_js_fixed` | Zoom on the filter line. **Normal speed** (it's the fix). Freeze to fill. |
| 4:07.4–4:15.6 | `06_admin_js_fixed` | Zoom on `petsCell` ('Unknown' label + `<select>` options), then the `badge warn` "Confirm pets with customer" line on "badge". |
| 4:15.6–4:22.9 | `03_trigger_body` (reuse) | Highlight `before insert or update` on "re-runs whenever staff update". |
| 4:22.9–4:26.8 | five-step list (step 4) → `02_code_diff_index_html` | On "That's the part the AI already did". |
| 4:27.6–4:32.8 | five-step list | Step 5 lit. |
| 4:32.8–4:41.0 | `06_drop_tests` 0:04–0:08 | Zoom on the results. Highlight row **A** ("cannot drop column…") on "dependency query", and row **D** (CASCADE drops the staff view) on "cascade". |

### 7. Verify (4:41.6–5:05.7)
| Edited | Screen | Treatment |
|---|---|---|
| 4:41.6 | **Chapter card** | CHECK IT · Verify |
| 4:44.0–4:51.1 | `07_booking_process` 0:00–0:25.7 | **Speed up ~3.6×** (typing). Ease to "We have a dog." in the notes, end on "Thanks!". |
| 4:51.6–4:55.8 | `07_auto_assign_to_ben` | Real speed. **Unknown** (4:51.6), highlight the **Confirm pets with customer** badge (4:52.7), click Auto-assign → **Ben** (~4:54.6). |
| 4:55.8–5:00.4 | `07_dropdown_to_yes` 0:01–0:06 | **F7a: crop to Pets → Cleaner.** Dropdown → Yes. Highlight **$165.00 · $150.00 + $15.00 pet fee** on "$165" (4:59.0), and the badge flips to "Needs pet-friendly cleaner". Real speed (it's the verification). |
| 5:00.4–5:02.3 | `07_old_entries_keep_info` | **F7b: top 4 rows only.** Highlight the 🐾 Yes + $15.00 pet fee rows. |
| 5:02.3–5:05.7 | `06_blast_radius` freeze + Remotion notes | Next to each row: view `admin_bookings`: "unchanged, fine". Function and trigger `set_booking_price`: "unknown = $0, by decision". |

### 8. Paste these (5:05.7–5:57.5)
| Edited | Screen | Treatment |
|---|---|---|
| 5:05.7 | **Chapter card** | PASTE THESE · Before you remove a field |
| 5:08.1–5:21.6 | **Prompt card: Prompt 1 "map it"** (≈13.5 s) | "PASTE THIS PROMPT". Prompt 1 text from the script. |
| 5:21.8–5:33.8 | **Query card: blast-radius query** | Too long for one card at a readable size (35 lines), so it shows the four `select` blocks in two columns at 26–28 px, with the comments as headings, plus a pill "Full query in the description". **F8** label: "CHECK QUERY". |
| 5:34.4–5:48.4 | **Prompt card: Prompt 3 / "Prompt 2: make it safe"** (14 s, no voice) | **F8** |
| 5:48.9–5:57.5 | `07_auto_assign_to_ben` freeze (flagged booking: Unknown · Confirm pets with customer · Ben) | Slow push-in. |
| 5:57.5–6:17.5 | **Outro** | `pbd-scene-bg-1920x1080.png`, no logo, no sound, end-screen areas empty. Suggested end-screen elements: S1b + 10a. |

---

## New Remotion components (shared, in `remotion\src\pbd\`)
- `ClaudePrompt`: Claude Code style input box (dark, monospace), typing animation. Used 3 times.
- `ClaudeResponse`: streamed Claude Code style response with markdown bold, bullets and inline code, plus timed highlight ranges. Used 2 times.
- `SeriesCard`, `ChapterCard`, `PromptCard`, `CodeStack` (three snippets), `Checklist`, `StepList`, `LowerThird`, `ZoomHighlight` (zoom + green box + dim, rendered over a still or short clip).

These are styled *after* Claude Code, re-typeset in brand fonts, not a pixel copy of the app.

## Audio
Cuts with 15 ms / 30 ms fades, mono, high-pass 80 Hz, light noise reduction (afftdn), compressor 2.5:1, loudness to −14 LUFS / −1 dBTP (two-pass at the final). No music.

## Thumbnail and description
Drafted at review gate 2, next to the preview:
- **Thumbnail:** the staff-page row from `01_hook_naive` ("We have 2 cats." · No · **$150.00** · **Ana · cat allergy**), with $150.00 and Ana circled in red. Text along the lines of "It never mentioned the price". 1280×720.
- **Description:** your title, Prompt 1, Prompt 3 and the generic blast-radius query, the `git grep -n -i -E` line, chapters, links to S1b (https://youtu.be/cC2F-ovAl_8) and 10a (https://youtu.be/4x5w0DcKOPw), and "Behaviour varied between runs. This is what happened when I tried it, with Claude Code 2.1.326, November 2026."
