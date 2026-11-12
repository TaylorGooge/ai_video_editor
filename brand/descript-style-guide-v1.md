# Descript style guide v1: Public by Default (11 Nov 2026)

What this is: the brand brief for Descript's Brand Studio (fonts, colors, logo, and the "generate a layout pack" prompt). Descript asks for a **design**, the **types of videos**, and **other instructions**, so sections 1 to 3 below are written to paste straight into those fields. Sections 4 onward are the reference specs behind them.

Assumes the name "Public by Default" and the padlock mark (A). If the toggle mark (B) wins the A/B test, swap the B files in; nothing else changes.

---

## 1. Paste into "Design"

> Dark, calm, technical. Think a developer's terminal or code editor at night, not a hacker movie. Near-black background (#0D1117) with one green accent (#3FB950) used sparingly for the thing that matters on screen: a highlight, a "fixed" state, a key word. Light grey-white text (#E6EDF3), muted grey (#8B949E) for secondary text, and slightly raised dark panels (#161B22) for cards and lower thirds. Red (#F85149) appears only to mark the problem or the hole; green marks the fix.
>
> Typography: Inter for titles and body text (bold titles, regular body). JetBrains Mono for anything that is code, a command, a file name, or a prompt to paste. Flat, clean shapes with rounded corners (about 12px). Subtle faint grid backgrounds are fine. No gradients, glows, neon, glitch effects, skulls, hooded figures, Matrix rain or padlock clip-art. Plenty of empty space; one idea per screen.
>
> Logo: open green padlock with a light shackle, plus the wordmark "Public by Default" with "Public" in green. Watermark sits bottom-right, small.

## 2. Paste into "Types of videos"

> A YouTube channel about practical security for people who build apps with AI tools (Lovable, Bolt, Cursor, Replit, Claude Code), plus small business owners who had someone build their app with AI. All videos are a voice-over on screen recordings. There's no face cam, so layouts never need a speaker box or picture-in-picture.
>
> 1. **Fix videos (main format, 8 to 15 minutes, 16:9).** Show a security hole in my own demo app, explain why AI tools create it, fix it, verify the fix, and end with a "paste this prompt" recap. Mostly full-screen screen recording with chapter title cards between sections.
> 2. **"The AI Did What You Asked" series (16:9).** Each episode follows the same five beats: the request, it works, what quietly broke, the decision you were actually making, and the question that would have caught it. Needs a consistent series title card and beat labels.
> 3. **Concept explainers (short, 3 to 6 minutes, 16:9).** No demo. An analogy or simple animated diagram explains one idea in plain English.
> 4. **Shorts / TikTok cuts (9:16, under 60 seconds).** A vertical cut of a hook or explainer, with big captions in the middle third.

## 3. Paste into "Other instructions"

> - Screen recordings are the hero. Leave them full-frame wherever possible. Branding is a thin frame around them, not on top of them.
> - Text on screen must be readable on a phone: titles at least 64px at 1080p, body at least 36px. Never place text over code that the viewer needs to read.
> - Code, commands, file names and prompts are always in JetBrains Mono, on a #161B22 panel with a 4px green left edge ("prompt card").
> - Problem vs. fix uses color: red (#F85149) labels for "the hole," green (#3FB950) labels for "the fix" and "verified." Use them only for that.
> - Lower thirds: dark panel (#161B22), green 4px left bar, white title in Inter Bold, grey subtitle. Bottom-left, inside title-safe margins.
> - Captions: Inter Bold, white with a soft dark box behind them, current word highlighted in green. Bottom-center for 16:9 and the middle third for 9:16.
> - Calm tone. No alarm sounds, flashing red, shaking text or "you've been hacked" imagery. Name the risk plainly, then fix it.
> - Keep the bottom-right corner clear in 16:9 (YouTube's watermark and end-screen elements go there). Keep the last 20 seconds of 16:9 videos clean for YouTube end-screen elements.
> - Layouts needed: title card, chapter card, full-screen recording with small corner logo, recording + caption, prompt card, side-by-side "before / after," big-quote/statement card, and outro.

---

## 4. Logo: what to upload, and what size

**Recommendation: transparent PNGs, master files at 1024px (square) and 2264×600 (horizontal).** Descript only scales them down, so these stay sharp even if you export in 4K. A corner logo in a 1080p video only ends up about 100–150px tall, so anything bigger than 1024 just adds file weight.

| Upload to Descript | File | Size | Use it for |
|---|---|---|---|
| **Primary logo** | `pbd-lockup-A-padlock-on-dark.png` | 2264 × 600, transparent | Title cards, outro, lower thirds, share-page logo |
| **Square logo / corner bug** | `pbd-badge-A-padlock.png` | 1024 × 1024 | Small corner logo on screen recordings. The dark circle keeps it readable over any footage, including white browser pages |
| Bare mark | `pbd-mark-A-padlock-on-dark.png` | 1024 × 1024, transparent | Big centered mark on dark scenes |
| Light-background versions | `*-on-light.png` | same sizes | Only if you ever put the logo on a white or light layout |
| Scene background | `pbd-scene-bg-1920x1080.png` | 1920 × 1080 | Intro, outro and chapter backgrounds |

SVG versions of the marks, badges and lockups are kept alongside the PNGs as vector masters. Upload PNGs to Descript.

**Corner-bug placement in Descript:** about 6–8% of frame height (roughly 64–88px tall at 1080p), top-right, 40px from the edges, 70–80% opacity. Put it top-right rather than bottom-right, because YouTube's own watermark and end-screen elements sit in the bottom-right.

**Why padlock (A) for video:** at very small sizes the padlock keeps its shape, while the eye on the toggle turns into a blob (see `pbd-AB-compare.png` at 40px). The profile-picture A/B test can still go either way.

## 5. Colors

| Role | Name | Hex | Notes |
|---|---|---|---|
| Background | Ink | `#0D1117` | Default for every scene |
| Raised surface | Panel | `#161B22` | Cards, lower thirds, prompt cards |
| Lines / grid | Border | `#30363D` | Dividers, faint grid |
| Primary text | Paper | `#E6EDF3` | Titles, body |
| Secondary text | Muted | `#8B949E` | Subtitles, captions under titles |
| Accent / fix / verified | Green | `#3FB950` | Brand color. Used sparingly |
| Problem / the hole | Red | `#F85149` | Only for marking the problem |
| Caution (optional) | Amber | `#D29922` | "Partly fixed" / "check this." Small use only, never as a main color (black + amber was rejected) |

In Descript's layout remixer, set **Background = #0D1117, Accent = #3FB950, Text = #E6EDF3**.

## 6. Fonts

| Use | Font | Weight | How to add |
|---|---|---|---|
| Titles | Inter | Bold (700) | Brand Studio → add Google Font by name: "Inter" |
| Subtitles / body | Inter | Medium (500) / Regular (400) | same |
| Code, commands, prompts | JetBrains Mono | Regular / Bold | add Google Font by name: "JetBrains Mono" |

In the remixer: **Title = Inter Bold, Subtitle = Inter Medium, Text = Inter Regular.** Descript's remixer only has those three slots, so add JetBrains Mono to the kit and pick it by hand on prompt cards.

## 7. Size and layout specs (1080p, 16:9)

| Element | Spec |
|---|---|
| Safe margins | 96px left/right, 54px top/bottom (title-safe ~5%) |
| Title card title | Inter Bold 96px, Paper; optional green keyword |
| Chapter card | Small green label ("STEP 2 · THE FIX") Inter Bold 28px, uppercase, letter-spaced; title Inter Bold 72px |
| Body text on screen | ≥ 36px |
| Lower third | Panel #161B22, radius 12, 4px green left bar; title Inter Bold 40px, subtitle Inter Medium 28px Muted |
| Prompt card | Panel #161B22, 4px green left bar, label "PASTE THIS PROMPT" Inter Bold 24px green, body JetBrains Mono 30–34px Paper |
| Hole / fix labels | Pill, radius 999, Inter Bold 24px uppercase; red or green fill with Ink text |
| Captions (16:9) | Inter Bold 48px, Paper, box #0D1117 at ~75% opacity, active word green, bottom-center |
| Captions (9:16) | Inter Bold 64–72px, max 2 lines, middle third of frame |
| Zoom/highlight on recordings | Green 4px rounded rectangle around the thing that matters; dim the rest of the frame to ~40% |
| End screen | Last 20s clean; use `pbd-scene-bg-1920x1080.png` |

## 8. Also in the kit (outside Descript)

| File | Size | Where it goes |
|---|---|---|
| `pbd-yt-watermark-A-padlock.png` | 300 × 300 | YouTube Studio → Customization → video watermark (YouTube needs a square of at least 150×150 under 1 MB) |
| `pbd-yt-banner-2560x1440.png` | 2560 × 1440 | YouTube channel banner. Logo and tagline sit inside the centered safe area |
| Existing `branding/profile-pic/*-800.png` | 800 × 800 | Profile picture (unchanged) |

## 9. Still open / to check

- Brand Studio is a Business/Enterprise plan feature. If a field is missing in your plan, the colors and fonts can still go into the layout-pack remixer.
- Descript doesn't publish a recommended logo size. The 1024px / 2264×600 sizes are my recommendation, not a Descript spec.
- Red/amber are new additions to the palette (only green was decided). Drop them if you want a single-accent brand.
- JetBrains Mono wasn't rendered in any asset yet. Check that it looks right in Descript.

## Fact-check

| Claim | Source | Verified |
|---|---|---|
| Brand Studio needs a Business or Enterprise plan; one brand kit per Drive | help.descript.com/branding/brand-studio | Yes |
| Brand Studio accepts Google Fonts by name or .ttf/.otf/.woff uploads; saves colors and gradients | help.descript.com/branding/brand-studio | Yes |
| Layout packs can be generated from brand files plus a prompt, and set as default | help.descript.com/branding/brand-studio; /templates-and-presets/layouts-default | Yes |
| Remixer has Title / Subtitle / Text font slots | help.descript.com/templates-and-presets/layouts-remix | Yes |
| YouTube watermark: square, min 150×150, under 1 MB | support.google.com/youtube/answer/2897336 | Yes |
| YouTube banner: min 2048×1152, 16:9; safe area 1235×338 at that size; 2560×1440 recommended | support.google.com/youtube/answer/10456525 (+ secondary for 2560) | Yes |
| Descript recommended logo dimensions | none published | **No** (my recommendation) |
