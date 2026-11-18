r"""v_s1a cut plan: voice EDL + edited-timeline anchors for the long-form cut.
Run: tools\.venv\Scripts\python.exe -I work\v_s1a\cutplan.py  -> prints the timeline, writes cutplan.json
raw = seconds in raw voice WAV; V = seconds in the edited timeline.
Speech edges: ffmpeg silencedetect (-42 dB, 0.25 s) in transcript\speech-regions.txt. Words: Whisper small.en.
Inside each kept range, pauses <= MAX_GAP stay as recorded; longer ones are shortened to CAP_GAP (spec 4)."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PAD_IN, PAD_OUT = 0.06, 0.10
MAX_GAP, CAP_GAP = 0.70, 0.40

# ("say", raw_start, raw_end, gap_before, label)  or  ("card", seconds, gap_before, label)
EDL = [
 ("say", 1.62, 5.63, 0.40, "S1 A customer books a cleaning. ... two cats."),
 ("say", 14.68, 21.35, 0.60, "S1 On the staff page ... allergic to cats. (take 2)"),
 ("say", 22.22, 31.66, 0.60, "S1 Ten minutes ago ... Not the part that cost money."),
 ("say", 32.48, 37.94, 0.60, "S1 Let's look at what it saw, what it couldn't see ... (take 1, see flags)"),
 ("say", 49.84, 51.61, 0.35, "S1 Prompts and a check query are at the end."),
 ("card", 3.5, 0.60, "SERIES CARD"),
 ("card", 2.0, 0.00, "CH2 card"),
 ("say", 54.72, 62.44, 0.40, "S2 Here's the change ... Clean."),
 ("say", 74.97, 86.23, 0.60, "S2 And it didn't stay quiet ... home with pets. (take 2)"),
 ("say", 91.53, 94.95, 0.35, "S2 And the badge would stop showing. (take 2)"),
 ("say", 96.22, 112.71, 0.50, "S2 That's a good answer ... never mentioned it."),
 ("card", 2.0, 0.60, "CH3 card"),
 ("say", 114.12, 122.73, 0.40, "S3 So I searched the code ... calculated in the database."),
 ("say", 127.99, 131.23, 0.40, "S3 This query lists ... pets column. (take 2)"),
 ("say", 138.66, 140.21, 0.50, "S3 There's a view the staff page reads. (take 2)"),
 ("say", 141.30, 153.41, 0.35, "S3 And there's a trigger ... we never asked."),
 ("say", 155.73, 158.22, 0.60, "S3 I put this pricing logic in the database for this demo. (take 1)"),
 ("say", 164.45, 165.32, 0.30, "S3 but it's a common setup. (F2 option B, v2)"),
 ("say", 179.24, 192.71, 0.40, "S3 Your AI tells you ... stops at what it can read."),
 ("card", 2.0, 0.60, "CH4 card"),
 ("say", 202.69, 213.70, 0.40, "S4 So I gave it read access to the database ... cleaner matching. (take 3; v3: flub 'read acc- ugh' 200.3-201.9 cut)"),
 ("say", 215.58, 225.01, 0.50, "S4 Unknown now means ... Better. (v3: false start 214.5-215.5 cut)"),
 ("say", 226.50, 236.45, 0.50, "S4 But look at what that decision means ... reasonable call."),
 ("say", 239.83, 254.93, 0.35, "S4 It's also a business decision ... isn't the same as checking. (take 2)"),
 ("say", 262.65, 267.18, 0.60, "S4 Which questions are yours ... linked in the description. (take 2)"),
 ("card", 2.0, 0.60, "CH5 card"),
 ("say", 270.33, 277.58, 0.40, "S5 Here's the core ... Null."),
 ("say", 283.17, 305.58, 0.50, "S5 And every place ... what I asked for. (take 2)"),
 ("card", 2.0, 0.60, "CH6 card"),
 ("say", 308.28, 311.16, 0.40, "S6 So here's how ... The order matters."),
 ("say", 314.39, 345.02, 0.60, "S6 One: decide ... finds the trigger. (v3: sniffle 313.4 cut)"),
 ("say", 351.13, 355.58, 0.60, "S6 Three, make everything handle unknown first ... (take 2)"),
 ("say", 379.83, 383.87, 0.50, "S6 Matching. Only a confirmed no-pets home ... (last take)"),
 ("say", 390.80, 398.49, 0.40, "S6 Staff page. Unknown ... yes, no, or unknown. (last take)"),
 ("say", 399.75, 409.87, 0.60, "S6 The trigger can stay ... Four, then remove the question."),
 ("say", 412.89, 414.79, 0.35, "S6 That's the part the AI already did. (take 2)"),
 ("say", 415.77, 418.18, 0.60, "S6 Five, drop the column later. Or never."),
 ("say", 422.42, 431.70, 0.40, "S6 Here we're keeping it ... error go away. (take 2)"),
 ("card", 2.0, 0.60, "CH7 card"),
 ("say", 449.20, 453.24, 0.40, "S7 Don't trust the summary ... as the start. (take 2)"),
 ("card", 3.0, 0.00, "HOLD booking (07_booking_process sped up)"),
 ("say", 454.52, 470.65, 0.50, "S7 Unknown ... you've made a decision about."),
 ("card", 2.0, 0.60, "CH8 card"),
 ("say", 473.63, 477.06, 0.40, "S8 Before you remove any field, paste this. It's in the description."),
 ("card", 10.0, 0.00, "HOLD Prompt 1 card"),
 ("say", 478.38, 484.67, 0.40, "S8 Then run this yourself ... in the description too."),
 ("card", 6.0, 0.00, "HOLD blast-radius query card"),
 ("card", 14.0, 0.60, "HOLD Prompt 3 card (no voice)"),
 ("say", 487.65, 489.22, 0.80, "S8 The AI can find a lot of where. (take 1)"),
 ("say", 497.53, 501.88, 0.40, "S8 Make sure it can see everywhere. And decide ... (take 2)"),
]
OUTRO = 20.0

def regions():
    txt = open(os.path.join(HERE, "transcript", "speech-regions.txt"), encoding="utf-8").read()
    return [(float(a), float(b)) for a, b in re.findall(r"([\d.]+)-([\d.]+)", txt) if float(b) > float(a)]

def build():
    R = regions()
    v = 0.0; segs = []; cards = []
    for e in EDL:
        if e[0] == "card":
            _, dur, gap, label = e
            v += gap; cards.append({"label": label, "v0": round(v, 3), "v1": round(v + dur, 3)}); v += dur
            continue
        _, a, b, gap, label = e
        rs = [(max(x, a), min(y, b)) for x, y in R if y > a and x < b]
        # merge regions with short pauses
        groups = [list(rs[0])]
        for x, y in rs[1:]:
            if x - groups[-1][1] <= MAX_GAP: groups[-1][1] = y
            else: groups.append([x, y])
        v += gap
        for i, (x, y) in enumerate(groups):
            if i: v += CAP_GAP
            segs.append({"label": label if i == 0 else "", "raw0": round(x, 3), "raw1": round(y, 3),
                         "v0": round(v, 3), "v1": round(v + y - x, 3)})
            v += y - x
    v_end = v + 1.0
    return segs, cards, round(v_end, 3), round(v_end + OUTRO, 3)

def raw_to_v(segs, t, tol=0.3):
    for s in segs:
        if s["raw0"] - tol <= t <= s["raw1"] + tol:
            return round(s["v0"] + (t - s["raw0"]), 2)
    return None

def fmt(t):
    m, s = divmod(t, 60); return f"{int(m)}:{s:05.2f}"

if __name__ == "__main__":
    segs, cards, voice_end, total = build()
    json.dump({"pad_in": PAD_IN, "pad_out": PAD_OUT, "segments": segs, "cards": cards,
               "voice_end": voice_end, "total": total}, open(os.path.join(HERE, "cutplan.json"), "w"), indent=1)
    rows = [(s["v0"], f"{fmt(s['v0'])}  raw {s['raw0']:7.2f}-{s['raw1']:7.2f}  {s['label']}") for s in segs if s["label"]]
    rows += [(c["v0"], f"{fmt(c['v0'])}  [{c['label']} {c['v1']-c['v0']:.1f}s]") for c in cards]
    for _, r in sorted(rows): print(r)
    print(f"segments={len(segs)}  voice ends {fmt(voice_end)}  outro to {fmt(total)}")
