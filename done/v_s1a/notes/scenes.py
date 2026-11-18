r"""v_s1a scene list -> build\scenes.json (for remotion\render-scenes.mjs) + build\typing.json (typing-sound ranges).
Run: tools\.venv\Scripts\python.exe -I work\v_s1a\scenes.py
Scene boundaries are anchored to words in the edited voice (transcript\edited-words.json) and card times (cutplan.json).
Rects are source pixels [x, y, w, h]; scene times are seconds from the scene start."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "build"); os.makedirs(B, exist_ok=True)
plan = json.load(open(os.path.join(HERE, "cutplan.json")))
WORDS = json.load(open(os.path.join(HERE, "transcript", "edited-words.json"), encoding="utf-8"))
CARDS = {c["label"].split(" ")[0] + ("" if not c["label"].startswith("HOLD") else c["label"][5:12]): c for c in plan["cards"]}
norm = lambda s: re.sub(r"[^a-z0-9$]", "", s.lower())

def N(t):
    """v1 edited time -> v2 edited time (preview-v2 audio cuts: um+restart, false start, sniffle)"""
    return t + (-1.99 if t > 122.0 else 0) + (-0.98 if t > 132.3 else 0) + (-0.33 if t > 207.1 else 0)

def A(word, near, tol=1.5):
    """edited time of `word` nearest to `near` (near is given in v1 time)"""
    near = N(near)
    c = [w["v"] for w in WORDS if norm(w["w"]) == norm(word) and abs(w["v"] - near) <= tol]
    if not c: raise SystemExit(f"anchor not found: {word} ~{near}")
    return min(c, key=lambda v: abs(v - near))

def card(key): return CARDS[key]
SRC = "v_s1a/"
SIZES = {"01_hook_naive": (910, 992), "02_code_diff_bookings_js": (1576, 522), "02_code_diff_index_html": (1642, 588),
         "03_app_folder_tree": (1848, 896), "03_check_blast_radius": (1500, 952), "03_grep_pet_fee": (1426, 448),
         "03_trigger_body": (790, 440), "04_code_diffs_all": (1414, 972), "04_hook_ben": (904, 1026), "04_mcp_connection": (1444, 438),
         "05_sql_editor": (1524, 880), "06_admin_js_fixed": (1774, 1018), "06_blast_radius": (1490, 962), "06_drop_tests": (1486, 946),
         "06_grep_has_pets": (1386, 268), "06_matching_js_fixed": (1798, 972), "07_auto_assign_to_ben": (1154, 152),
         "07_booking_process": (926, 910), "07_dropdown_to_yes": (1344, 528), "07_old_entries_keep_info": (1618, 628)}

def screen(clip, **k):
    w, h = SIZES[clip]
    return dict(kind="screen", src=f"{SRC}{clip}.mp4", w=w, h=h, **k)
def freeze(t): return [dict(d=999, from_=t, rate=0)]
def hl(t0, t1, r, kind="box", dim=True): return dict(t0=t0, t1=t1, r=r, kind=kind, dim=dim)

PROMPT0 = 'Remove the "Do you have pets?" question from the booking form.'
PROMPT1 = ("Before changing anything: list every file, query, type, component, test, email template and API call that "
           "reads, writes or displays `has_pets` (also search for `hasPets`, `pets` and `pet_`). For each one, tell me what "
           "happens for new records where the value is null. Then tell me what you could NOT check, such as database "
           "functions, triggers or third-party services. Don't edit anything yet.")
PROMPT3 = ('We\'re removing the "[question]" question from the form. Existing records keep their value. New records store '
           'null, which means "unknown", not "no". Before removing the input, update every place that reads `[column]` so '
           'that null shows "Unknown", is flagged for a person to confirm, and never gets the "no" behaviour automatically. '
           "Then remove the input. Don't drop the column. Show me each change.")
QUERY = chr(10).join(l for l in open(os.path.join(HERE, "blast-radius.sql"), encoding="utf-8").read().strip().splitlines()[6:-3])  # no banner / trailing hand-check

RESP1 = [
    dict(text="I'll find the booking form in your app folder and remove that question.", gap=0),
    dict(text="I've removed the pets question from the booking form. The change is saved in your app folder but not committed to git.", gap=22),
    dict(text="**`index.html`:** the \"Do you have pets?\" Yes/No block is gone.", bullet=True, gap=16),
    dict(text="**`js/booking.js`:** the form no longer sends `has_pets`, which would break once the question is gone. The `has_pets` column already allows blank values, so the database needs no change. New bookings will save it as unknown.", bullet=True),
    dict(text="**The catch: pet homes can go to cat-allergic cleaners.** The rest of the app still uses the pets answer:", gap=22),
    dict(text="Auto-assign in `js/matching.js` keeps homes with pets away from cleaners with a cat allergy. With no answer, it treats every new booking as pet-free, so it could send a cleaner with a cat allergy to a home that has pets.", bullet=True, gap=16),
    dict(text="The staff page will show \"No\" in the Pets column. It also won't show the \"Needs pet-friendly cleaner\" badge.", bullet=True),
    dict(text="Staff can still set pets by hand with the edit checkbox on each booking.", bullet=True),
]
RESP2 = [
    dict(text="I removed the \"Do you have pets?\" question from the booking form. That answer was also used to keep cleaners with a cat allergy away from homes with pets, so I changed two other places to keep that protection working. I haven't run the app to check these changes.", gap=0),
    dict(text="`index.html`: the question and its Yes/No buttons are gone.", bullet=True, gap=14),
    dict(text="`js/booking.js`: the form no longer sends a pets answer. New bookings now have no pets answer saved, which means \"unknown\".", bullet=True, gap=4),
    dict(text="`js/matching.js`: auto-assign now treats \"unknown\" as \"may have pets\" and only allows an allergic cleaner when a booking is marked as having no pets.", bullet=True, gap=4),
    dict(text="`js/admin.js`: the staff page shows Unknown instead of No when there's no pets answer.", bullet=True, gap=4),
    dict(text="What this means for staff:", gap=16),
    dict(text="**Allergic cleaners are skipped by default:** auto-assign won't pick a cleaner with a cat allergy for a new booking until someone sets the pets answer with the staff page's existing edit checkbox.", bullet=True, gap=4),
    dict(text="**Marking \"no pets\" takes two clicks:** the checkbox starts unticked for unknown bookings, so a staff member has to tick it and then untick it.", bullet=True, gap=4),
    dict(text="**No pet-friendly badge:** the \"Needs pet-friendly cleaner\" badge only appears when a booking is marked as having pets.", bullet=True, gap=4),
    dict(text="The database still has the pets column, the pet fee and the Pets column on the staff page. I left them alone so staff can still record pets.", gap=16),
]
STEPS = ["Decide", "Map everything that uses it", "Handle “unknown” first", "Remove the question", "Drop the column later. Or never."]

S = []   # (start, props)
TYPING = []  # absolute [t0, t1] ranges for the typing sound
def add(t0, props): S.append([round(t0, 3), props])
def chapter(key, label, title): add(card(key)["v0"], dict(kind="chapter", label=label, title=title))

# ---------- 1. Hook ----------
add(0.0, screen("01_hook_naive", pieces=[dict(d=2.6, from_=0, rate=7.0), dict(d=1.7, from_=18.2, rate=2.0), dict(d=9, from_=21.6, rate=3.0)],
                cam=[dict(t=0, r=[0, 0, 910, 992]), dict(t=2.4, r=[30, 300, 740, 420])]))
t_staff = A("On", 4.95) - 0.1
ana = A("allergic", 10.38) - 0.6  # Ana lands just before "allergic"
add(t_staff, screen("01_hook_naive", pieces=[dict(d=99, from_=32.75 - (ana - t_staff), rate=1)],
                    cam=[dict(t=0, r=[0, 180, 910, 720]), dict(t=0.6, r=[0, 640, 910, 150])],
                    hl=[hl(A("no", 6.77) - t_staff, A("no", 7.85) - t_staff, [405, 690, 50, 70], "soft"),
                        hl(A("no", 7.85) - t_staff, ana - t_staff, [626, 690, 100, 32], "soft"),
                        hl(ana - t_staff + 0.2, 99, [745, 690, 125, 65], "box")]))
t_prompt = A("Ten", 11.87) - 0.15
add(t_prompt, dict(kind="claudePrompt", text=PROMPT0, typeStart=0.6, cps=24, enterAt=A("It", 16.01) - t_prompt))
TYPING.append([t_prompt + 0.6, t_prompt + 0.6 + len(PROMPT0) / 24])
t_money = A("not", 19.71) - 0.1
add(t_money, screen("01_hook_naive", pieces=freeze(35.5), cam=[dict(t=0, r=[0, 640, 910, 150]), dict(t=A("Let's", 21.55) - t_money, r=[0, 180, 910, 720])],
                    hl=[hl(0.15, A("Let's", 21.55) - t_money + 0.3, [626, 690, 100, 32], "circle")]))
add(card("SERIES")["v0"], dict(kind="series", title="My AI Removed One Form Field. It Never Mentioned the Price",
                                 beats=["The request", "It works", "What quietly broke", "The decision you were making", "The question that would have caught it"]))

# ---------- 2. What the AI did ----------
chapter("CH2", "It works", "What the AI did, and what it said")
t = A("Here's", 35.45) - 0.15
add(t, screen("02_code_diff_index_html", pieces=freeze(2.0), cam=[dict(t=0, r=[0, 0, 1642, 588]), dict(t=A("Two", 36.99) - t, r=[0, 110, 900, 190])],
              hl=[hl(A("The", 38.06) - t, 99, [70, 143, 690, 120])]))
t = A("and", 40.02) - 0.1
add(t, screen("02_code_diff_bookings_js", pieces=freeze(2.0), cam=[dict(t=0, r=[0, 300, 800, 120])], hl=[hl(0.3, 99, [62, 352, 690, 25])]))
t_r1 = A("it", 43.61) - 0.5
add(t_r1, dict(kind="claudeResponse", prompt=PROMPT0, blocks=RESP1, streamStart=0.1, streamDur=1.6,
               hl=[dict(t0=A("It", 44.87) - t_r1, t1=A("It", 48.19) - t_r1, blocks=[3]),
                   dict(t0=A("It", 48.19) - t_r1, t1=A("And", 55.04) - t_r1, blocks=[4, 5]),
                   dict(t0=A("And", 55.04) - t_r1, t1=A("That's", 58.89) - t_r1, blocks=[6])]))
t = A("look", 62.10) - 0.45
add(t, screen("01_hook_naive", pieces=freeze(35.5), cam=[dict(t=0, r=[0, 640, 910, 150])],
              hl=[hl(0.3, 99, [626, 690, 100, 32], "circle")],
              labels=[dict(t0=A("$150", 65.90) - t, text="$150.00 + $15.00 pet fee = $165.00", sub="what this booking should cost", x=560, y=760, kind="mono", size=40),
                      dict(t0=A("The", 70.02) - t, text="No pet fee", x=1450, y=300, kind="red")]))

# ---------- 3. Where the fee lives ----------
chapter("CH3", "What quietly broke", "Where the fee lives")
t = A("So", 75.43) - 0.15
add(t, screen("03_grep_pet_fee", pieces=[dict(d=2.4, from_=1.5, rate=2.5), dict(d=99, from_=7.5, rate=1)], cam=[dict(t=0, r=[0, 0, 1426, 140])],
              masks=[dict(r=[0, 70, 1426, 64], color="#17181B"), dict(r=[0, 134, 1426, 30], color="#17181B")],
              hl=[hl(A("displayed", 77.72) - t, 99, [8, 27, 1060, 44])]))
t_q = A("This", 83.38) - 0.15
res = 1.7
add(t_q, screen("03_check_blast_radius", pieces=[dict(d=res, from_=2.0, rate=(6.9 - 2.0) / res), dict(d=4.3, from_=6.9, rate=1), dict(d=99, from_=11.1, rate=0)],
                cam=[dict(t=0, r=[0, 0, 1500, 952]), dict(t=res + 0.1, r=[0, 540, 760, 240])],
                hl=[hl(A("view", 87.64) - t_q, A("trigger,", 89.64) - t_q, [0, 722, 713, 42]),
                    hl(A("trigger,", 89.64) - t_q, 99, [0, 634, 713, 86])]))
t = A("Here", 92.28) - 0.2
add(t, screen("03_trigger_body", pieces=freeze(1.0), cam=[dict(t=0, r=[0, 0, 790, 440]), dict(t=0.2, r=[0, 110, 640, 150]), dict(t=A("put", 100.58) - t, r=[0, 0, 790, 440])],
              hl=[hl(0.3, A("put", 100.58) - t, [18, 177, 615, 26]),
                  hl(A("Otherwise,", 95.68) - t, A("put", 100.58) - t, [520, 176, 72, 28], "circle")]))
t = A("So", 110.05) - 0.15
add(t, screen("03_app_folder_tree", pieces=[dict(d=1.8, from_=0.7, rate=1), dict(d=99, from_=2.5, rate=0)], cam=[dict(t=0, r=[0, 0, 430, 440])]))

# ---------- 4. Same prompt, database connected ----------
chapter("CH4", "The decision you were making", "Same prompt, database connected")
t = card("CH4")["v1"] + 0.25  # first word (the cut-and-kept retake has no whisper word time)
add(t, screen("04_mcp_connection", pieces=[dict(d=99, from_=8.5, rate=1)], hl=[hl(1.0, 99, [976, 126, 176, 24])]))
t_p2 = A("Fresh", 125.85) - 0.15
add(t_p2, dict(kind="claudePrompt", text=PROMPT0, typeStart=-10, cps=24, enterAt=A("prompt.", 127.27) - t_p2 + 0.2, title="claude · ~/app · supabase (read-only)"))
t = A("This", 128.43) - 0.15
add(t, screen("04_code_diffs_all", pieces=freeze(25.0), cam=[dict(t=0, r=[0, 0, 1414, 420]), dict(t=0.6, r=[690, 20, 724, 200])],
              hl=[hl(A("it", 130.81) - t, A("means", 134.19) - 0.9 - t, [750, 164, 664, 26]),
                  hl(A("means", 134.19) - 0.9 - t, 99, [750, 69, 664, 26])]))
t = A("the", 136.07) - 0.1
add(t, screen("04_code_diffs_all", pieces=freeze(9.5), cam=[dict(t=0, r=[700, 470, 714, 100])],
              hl=[hl(0.2, 99, [1272, 503, 104, 26], "box")]))
t_ben = A("cat", 139.30) - 0.25
ben = A("Ben", 140.3)
add(t_ben, screen("04_hook_ben", pieces=[dict(d=99, from_=29.9 - (ben - 0.1 - t_ben), rate=1)], cam=[dict(t=0, r=[0, 650, 904, 160])],
                  hl=[hl(ben - t_ben, 99, [755, 696, 120, 40])]))
t_r2 = A("But", 141.65) - 0.15
t_price = A("price", 155.9, 2) - 0.6
t_back = A("It", 158.54) - 0.15
r2hl = [dict(t0=0.3, t1=t_price - t_r2, blocks=[6])]
add(t_r2, dict(kind="claudeResponse", prompt=PROMPT0, blocks=RESP2, streamStart=-5, streamDur=1, hl=r2hl, size=25, title="claude · ~/app · supabase (read-only)"))
add(t_price, screen("04_hook_ben", pieces=freeze(31.0), cam=[dict(t=0, r=[0, 650, 904, 160])], hl=[hl(0.2, 99, [645, 700, 82, 30], "circle")]))
t_short = A("Which", 164.84) - 0.1
add(t_back, dict(kind="claudeResponse", prompt=PROMPT0, blocks=RESP2, streamStart=-5, streamDur=1, size=25, title="claude · ~/app · supabase (read-only)",
                 hl=[dict(t0=0.2, t1=99, blocks=[9])],
                 labels=[dict(t0=t_short - t_back, text="Your AI Knows Where. Only You Know Why.", sub="Link in the description", x=96, y=890, kind="lower")]))

# ---------- 5. Null is not "no" ----------
chapter("CH5", "The decision you were making", "Null is not “no”")
t = A("Here's", 172.33) - 0.15
t_nothing = A("Now", 176.81)
add(t, screen("05_sql_editor", pieces=[dict(d=t_nothing - t, from_=5.0 - (t_nothing - t), rate=1), dict(d=99, from_=5.0, rate=1)],
              cam=[dict(t=0, r=[0, 0, 1524, 520]), dict(t=t_nothing - t, r=[0, 490, 620, 230])],
              hl=[hl(t_nothing - t + 0.6, 99, [0, 576, 242, 42])]))
t_cs = A("And", 179.78) - 0.15
add(t_cs, dict(kind="codeStack", title="Every place that reads the answer", pillAt=A("each", 185.52) - t_cs,
               items=[dict(file="js/admin.js · staff page", code="b.has_pets ? '🐾 Yes' : 'No'", on=A("staff", 182.9) - t_cs, pill="null → “No”"),
                      dict(file="js/matching.js · auto-assign", code="booking.has_pets ? !c.cat_allergy : true", on=A("matching,", 183.82) - t_cs, pill="null → any cleaner"),
                      dict(file="trigger set_booking_price · price", code="case when new.has_pets then 15 else 0 end", on=A("price,", 184.54) - t_cs, pill="null → $0 fee")]))
t_cl = A("Remove", 187.9, 1.5) - 0.2
add(t_cl, dict(kind="checklist", title="“Remove the question” is four changes", done=2, doneAt=A("The", 197.91) - t_cl,
               items=[dict(text="Stop asking", at=A("Stop", 191.75) - t_cl), dict(text="Stop saving", at=A("stop", 192.93) - t_cl),
                      dict(text="Stop using it", at=A("stop", 194.11) - t_cl), dict(text="Decide about the old answers", at=A("And", 195.29) - t_cl)]))

# ---------- 6. The fix ----------
chapter("CH6", "The question that would have caught it", "Remove a field in order")
t_st = A("here's", 203.99) - 0.4
t_ask = A("Ask", 225.79) - 0.1
add(t_st, dict(kind="steps", title="Remove a field in order", steps=STEPS,
               active=[dict(t=A("One,", 207.45) - t_st, i=0), dict(t=A("Two,", 222.99) - t_st, i=1)],
               subs=[dict(text="Stop asking on the form", at=A("stop", 215.01) - t_st), dict(text="Staff confirm pets when they confirm the booking", at=A("Staff", 216.81) - t_st),
                     dict(text="Keep the old answers", at=A("Keep", 219.37) - t_st), dict(text="No pet fee until it's confirmed", at=A("no", 220.99) - t_st)]))
add(t_ask, dict(kind="claudePrompt", text=PROMPT1, typeStart=0.2, cps=160, enterAt=99, size=26))
TYPING.append([t_ask + 0.2, t_ask + 0.2 + len(PROMPT1) / 160])
t = A("search", 229.52) - 0.6
add(t, screen("06_grep_has_pets", pieces=[dict(d=99, from_=3.0, rate=0)],
              labels=[dict(t0=0.1, text='git grep -n -i -E "has_?pets|haspets"', x=96, y=230, kind="mono", size=38)], area=[96, 360, 1728, 560]))
t = A("run", 231.13) - 0.3
add(t, screen("06_blast_radius", pieces=[dict(d=99, from_=4.2, rate=1)], cam=[dict(t=0, r=[0, 540, 760, 240])],
              hl=[hl(A("trigger.", 233.6, 1.5) - t, 99, [0, 672, 713, 44])]))
t_three = A("make", 235.84) - 0.85
add(t_three, dict(kind="steps", title="Remove a field in order", steps=STEPS, active=[dict(t=0, i=2)]))
t = A("Only", 240.77) - 0.9
add(t, screen("06_matching_js_fixed", pieces=freeze(3.0), cam=[dict(t=0, r=[880, 20, 918, 200])],
              hl=[hl(0.3, A("can", 242.6, 1.5) - t, [935, 70, 740, 24]), hl(A("can", 242.6, 1.5) - t, 99, [970, 165, 700, 25])]))
t = A("Staff", 244.36) - 0.2
add(t, screen("06_admin_js_fixed", pieces=freeze(4.0), cam=[dict(t=0, r=[880, 0, 894, 740])],
              hl=[hl(A("Unknown.", 245.58) - t, A("A", 246.30) - t, [945, 89, 829, 24]),
                  hl(A("A", 246.30) - t, A("And", 248.84) - t, [945, 705, 829, 25]),
                  hl(A("And", 248.84) - t, 99, [945, 110, 829, 216])]))
t = A("The", 252.64) - 0.15
add(t, screen("03_trigger_body", pieces=freeze(1.0), hl=[hl(0.3, A("And", 257.09) - t, [18, 177, 615, 26], "soft"), hl(A("And", 257.09) - t, 99, [30, 296, 430, 22])]))
t_four = A("Four,", 259.85) - 0.2
add(t_four, dict(kind="steps", title="Remove a field in order", steps=STEPS, active=[dict(t=0, i=3)]))
t = A("That's", 262.08) - 0.15
add(t, screen("02_code_diff_index_html", pieces=freeze(2.0), cam=[dict(t=0, r=[0, 110, 900, 190])], hl=[hl(0.2, 99, [70, 143, 690, 120])]))
t_five = A("Five,", 264.56) - 0.2
add(t_five, dict(kind="steps", title="Remove a field in order", steps=STEPS, active=[dict(t=0, i=4)]))
t_drop = A("If", 272.18) - 0.15
add(t_drop, screen("06_drop_tests", pieces=[dict(d=0.8, from_=3.1, rate=1), dict(d=99, from_=3.9, rate=1)], cam=[dict(t=0, r=[0, 590, 1380, 262])],
                   hl=[hl(A("run", 273.80) - t_drop, A("never", 275.62) - t_drop, [0, 633, 1370, 42]),
                       hl(A("never", 275.62) - t_drop, 99, [0, 764, 1370, 42])]))

# ---------- 7. Verify ----------
chapter("CH7", "Check it", "Verify")
t_v = card("CH7")["v1"]
t_unk = A("Unknown.", 288.28) - 0.25
book = (t_unk - t_v)
add(t_v, screen("07_booking_process", pieces=[dict(d=book, from_=0, rate=25.5 / book)],
                cam=[dict(t=0, r=[0, 0, 926, 910]), dict(t=book * 0.68, r=[20, 300, 640, 330])]))
TYPING.append([t_v + 0.2, t_v + book * 0.85])
t_conf = A("Staff", 292.8) - 0.3
ana2 = A("Anna.", 291.9)
aa_from = max(0, 2.93 - (ana2 - 0.2 - t_unk))
click = 2.85 - aa_from  # table re-lays out when Ben is assigned (columns shift ~25 px right)
add(t_unk, screen("07_auto_assign_to_ben", pieces=[dict(d=99, from_=aa_from, rate=1)],
                  hl=[hl(0.15, A("Flag", 289.68) - t_unk, [134, 62, 94, 30]),
                      hl(A("Flag", 289.68) - t_unk, click, [914, 67, 210, 32]),
                      hl(click + 0.05, 99, [854, 66, 248, 34])]))
t_old = A("bookings", 297.81) - 0.6
fee = A("$165.", 296.0)
dd_from = max(0, 5.37 - (fee - 0.2 - t_conf))
closed = 4.85 - dd_from  # menu closes; from then on also hide Jane Smith's Pets cell
add(t_conf, screen("07_dropdown_to_yes", pieces=[dict(d=99, from_=dd_from, rate=1)], cam=[dict(t=0, r=[240, 0, 1060, 228])],
                   masks=[dict(r=[240, 137, 92, 96], color="#FFFFFF"), dict(r=[458, 137, 842, 96], color="#FFFFFF"),
                          dict(r=[330, 137, 128, 96], color="#FFFFFF", t0=closed)],
                   hl=[hl(fee - 0.1 - t_conf, 99, [800, 46, 200, 50])]))
t_q2 = A("And", 299.34) - 0.15
add(t_old, screen("07_old_entries_keep_info", pieces=freeze(3.0), cam=[dict(t=0, r=[30, 0, 1445, 400])],
                  hl=[hl(0.2, 99, [495, 6, 680, 90], "soft", False), hl(0.2, 99, [495, 306, 680, 90], "soft", False)]))
add(t_q2, screen("06_blast_radius", pieces=freeze(8.0), cam=[dict(t=0, r=[0, 590, 1300, 180])],
                 labels=[dict(t0=0.3, text="✓ by decision: unknown = $0 fee", x=1080, y=514, kind="panel", size=30),
                         dict(t0=0.6, text="✓ unchanged, fine", x=1080, y=602, kind="panel", size=30)]))

# ---------- 8. Paste these ----------
chapter("CH8", "Paste these", "Before you remove a field")
t_p1 = card("CH8")["v1"]
t_then = A("Then", 317.5) - 0.2
add(t_p1, dict(kind="prompt", label="Paste this prompt", title="Prompt 1 · Map it", body=PROMPT1, cps=140, size=32))
TYPING.append([t_p1 + 0.4, t_p1 + 0.4 + len(PROMPT1) / 140])
add(t_then, dict(kind="prompt", label="Run this in the Supabase SQL editor", title="Prompt 2 · The blast-radius query", body=QUERY, cps=300, size=18,
                 note="Full query in the description"))
TYPING.append([t_then + 0.4, t_then + 0.4 + len(QUERY) / 330])
t_p3 = card("HOLD Prompt 3")["v0"] if "HOLD Prompt 3" in CARDS else [c for c in plan["cards"] if c["label"].startswith("HOLD Prompt 3")][0]["v0"]
add(t_p3, dict(kind="prompt", label="Paste this prompt", title="Prompt 3 · Make it safe", body=PROMPT3, cps=140, size=32))
TYPING.append([t_p3 + 0.4, t_p3 + 0.4 + len(PROMPT3) / 140])
t_end = [c for c in plan["cards"] if c["label"].startswith("HOLD Prompt 3")][0]["v1"] + 0.3
add(t_end, screen("07_auto_assign_to_ben", pieces=freeze(5.5), cam=[dict(t=0, r=[0, 0, 1154, 152]), dict(t=0.1, r=[100, 20, 1054, 132])]))
add(plan["voice_end"], dict(kind="outro"))

# ---------- durations ----------
S.sort(key=lambda s: s[0])
out = []
for i, (t0, p) in enumerate(S):
    t1 = S[i + 1][0] if i + 1 < len(S) else plan["total"]
    p["dur"] = (round(t1 * 30) - round(t0 * 30)) / 30  # frame-exact, so joined scenes never drift
    assert p["dur"] > 0.3, (i, t0, p["kind"])
    for pc in p.get("pieces", []):
        pc["from"] = round(pc.pop("from_"), 3)
    out.append(dict(id=f"s{i + 1:02d}", start=t0, props=p))
json.dump(out, open(os.path.join(B, "scenes.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(TYPING, open(os.path.join(B, "typing.json"), "w"), indent=1)
for s in out: print(f"{s['id']} {s['start']:7.2f} {s['props']['dur']:6.2f} {s['props']['kind']:14s} {s['props'].get('src', s['props'].get('title', s['props'].get('label', '')))}")
print("total", plan["total"])
