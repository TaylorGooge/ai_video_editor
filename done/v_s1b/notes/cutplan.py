r"""v_s1b cut plan: voice EDL + clip timing for the main and extended long-form cuts.
Run: tools\.venv\Scripts\python.exe -I work\v_s1b\cutplan.py  -> prints tables, writes cutplan-<cut>.json
Times: raw = seconds in raw voice WAV; V = seconds in the edited timeline; file = seconds in a clip file.
Segment edges come from ffmpeg silencedetect (-42 dB, 0.25 s); word anchors from Whisper small.en."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PAD_IN, PAD_OUT = 0.06, 0.10   # audio kept before/after each segment's speech edges

# name, raw_start, raw_end, gap_before (silence between speech in the edited voice), text
SEGS = {
 "s01": (0.99, 4.06, 0.30, 'A client asked me to remove one question from a booking form.'),
 "s02": (5.89, 6.77, 0.55, '"Do you have pets?"'),
 "s03": (8.00, 9.53, 0.50, 'One question. Should take a minute.'),
 "s04": (15.91, 19.89, 0.65, 'So I asked my AI tool what removing it would touch. And it found something.'),
 "s05": (22.10, 29.86, 0.50, 'That answer was being used on the admin page. It put a paw icon on the booking. It picked which cleaner got the job. It added a fee.'),
 "s06": (35.77, 39.23, 0.60, 'Remove the question, and all of that quietly stops working.'),
 "s07a": (40.61, 41.60, 0.65, 'So I asked the client:'),
 "s07b": (42.44, 43.86, 0.50, 'Why did you start asking this?'),
 "s07c": (44.69, 45.74, 0.50, 'What is the fee for?'),
 "s07d": (46.69, 48.06, 0.50, 'Should cleaners still be matched?'),
 "s07e": (49.01, 50.71, 0.50, 'And what about the answers you already have?'),
 "s08": (52.06, 55.62, 0.55, 'They said: "Just paste my email into Claude. It\'ll handle it."'),
 "s09": (57.43, 58.70, 0.65, "Here's what I couldn't get across."),
 "s10": (59.56, 61.86, 0.40, 'The AI can find where the answer is used.'),  # ad-lib "every page, every rule" removed (v2)
 "s11": (71.89, 77.54, 0.50, "It can't know why you wanted it, or what you want now. That's not in the code. It's in your head."),
 "s12": (79.09, 86.71, 0.60, "It's like asking a contractor to knock out a wall. A good one checks if it's load-bearing. Only you know if you still need the room upstairs."),
 "s13": (87.66, 91.31, 0.65, "Before you remove anything, paste this. That's the where."),
 "s14": (92.55, 97.74, 0.50, "Then answer the why yourself. If you can't, that's the real problem, and no prompt fixes it."),
 "s15": (99.03, 103.03, 0.65, 'Every field in your app is a decision somebody made. Make sure it\'s you.'),
 "e01": (104.57, 106.10, 0.65, "Here's what a good answer sounds like."),
 "e02": (107.06, 111.33, 0.50, '"We started asking because cleaners with allergies kept getting sent to homes with cats."'),
 "e03": (112.61, 114.34, 0.50, '"The fee covers extra vacuuming."'),
 "e04": (119.62, 123.26, 0.50, '"Yes, still match. Ask about pets on the phone instead."'),
 "e05": (124.71, 128.51, 0.50, '"Keep the old answers for existing bookings; stop asking new customers."'),
 "e06": (130.01, 134.51, 0.65, "That email, the AI can work with. Now it knows the where and the why."),
}
ORDER = {
 "main": ["s01","s02","s03","s04","s05","s06","s07a","s07b","s07c","s07d","s07e","s08","s09","s10","s11","s12","s13","s14","s15"],
}
ORDER["extended"] = ORDER["main"][:ORDER["main"].index("s12")+1] + ["e01","e02","e03","e04","e05","e06"] + ORDER["main"][ORDER["main"].index("s13"):]

PROMPT_MIN = 9.0       # prompt card on screen (spec asks 11 s for 6 lines; shortened at your request, v2)
END_HOLD = 1.6         # statement card hold after the last word
OUTRO = 12.0           # clean end-screen tail (spec says 20 s; shortened for this video, v2)

# Clip plan. start: ("cut", seg, lead) = hard cut `lead` s before that segment's speech,
#                    ("cont",) = continuation clip; starts so its first anchor lands (in = 0).
# anchors: (file_t, where) where = ("seg", name, offset) or ("w", raw_word_time).
# freeze_lead: freeze is inserted this many s before the later event.
CLIPS = [
 dict(id="01", f="s1b-01-email-request.mp4", dur=8, start=("cut","s01",0.30), anchors=[(1.0,("seg","s01",-0.30))]),
 dict(id="02", f="s1b-02-form-strike.mp4", dur=8, start=("cut","s03",0.35), anchors=[(2.6,("seg","s03",0.0))]),
 dict(id="03", f="s1b-03-arrow-to-admin.mp4", dur=7, start=("cont",), anchors=[(2.55,("w",19.18))]),
 dict(id="04", f="s1b-04-admin-items-light-up.mp4", dur=9, start=("cont",), anchors=[(1.8,("w",25.06)),(3.6,("w",27.62)),(5.4,("w",29.54))]),
 dict(id="05", f="s1b-05-admin-items-go-grey.mp4", dur=6, start=("cut","s06",0.20), anchors=[(1.2,("seg","s06",0.0)),(2.0,("w",37.82))], freeze_lead=0.04),
 dict(id="06", f="s1b-06-four-questions.mp4", dur=12, start=("cut","s07a",0.15), anchors=[(2.2,("seg","s07b",0)),(4.2,("seg","s07c",0)),(6.2,("seg","s07d",0)),(8.4,("seg","s07e",0))]),
 dict(id="07", f="s1b-07-reply-just-paste.mp4", dur=8, start=("cut","s08",0.15), anchors=[(2.9,("w",53.20))]),
 dict(id="08", f="s1b-08-where-why-split.mp4", dur=5, start=("cut","s09",0.15), anchors=[(1.0,("seg","s09",-0.15))]),
 dict(id="09", f="s1b-09-where-ai-finds-it.mp4", dur=8, start=("cut","s09",-0.95), anchors=[(1.0,("seg","s09",0.95))]),
 dict(id="10", f="s1b-10-why-only-owner-knows.mp4", dur=8, start=("cut","s11",0.20), anchors=[(1.2,("seg","s11",0))]),
 dict(id="11", f="s1b-11-load-bearing-wall.mp4", dur=10, start=("cut","s12",0.15), anchors=[(3.2,("w",80.52)),(5.0,("w",82.36)),(6.4,("w",84.24))]),
 dict(id="15", f="s1b-15-ext-good-answers.mp4", dur=14, ext=True, start=("cut","e01",0.15), anchors=[(2.2,("seg","e02",0)),(5.0,("seg","e03",0)),(7.8,("seg","e04",0)),(10.6,("seg","e05",0))], freeze_lead=0.75),
 dict(id="16", f="s1b-16-ext-answers-under-email.mp4", dur=8, ext=True, start=("cut","e06",0.45), anchors=[(1.8,("seg","e06",-0.20)),(4.4,("w",132.92))]),
 dict(id="12", f="s1b-12-paste-this-prompt.mp4", dur=14, start=("cut","s13",0.30), anchors=[(1.0,("seg","s13",-0.30))]),
 dict(id="13", f="s1b-13-questions-you-stamp.mp4", dur=8, start=("cut","s14",0.15), anchors=[(1.8,("w",93.56))]),
 dict(id="14", f="s1b-14-statement-every-field.mp4", dur=6, start=("cut","s15",0.15), anchors=[(1.2,("seg","s15",-0.05))]),
]


def build(cut):
    order = ORDER[cut]
    segs, t = [], 0.0
    for name in order:
        rs, re_, gap, text = SEGS[name]
        vs = t + gap if segs else gap
        if name == "s14":  # hold the prompt card long enough to read
            p_start = seg_v["s13"][0] - 0.30
            vs = max(vs, p_start + PROMPT_MIN + 0.15)
        if name == "s11":  # let clip 09 finish its chain + check badge (plays file 1.0-4.9) before clip 10
            vs = max(vs, seg_v["s09"][0] + 0.95 + 3.9 + 0.2)
        segs.append(dict(name=name, raw=(rs, re_), v=(round(vs, 3), round(vs + re_ - rs, 3)), text=text))
        t = vs + (re_ - rs)
        seg_v = {s["name"]: s["v"] for s in segs}
    seg_v = {s["name"]: s["v"] for s in segs}
    seg_raw = {s["name"]: s["raw"] for s in segs}
    voice_end = segs[-1]["v"][1]

    def to_v(where):
        if where[0] == "seg":
            return seg_v[where[1]][0] + where[2]
        rt = where[1]
        for s in segs:
            if s["raw"][0] - 0.3 <= rt <= s["raw"][1]:
                return s["v"][0] + max(0.0, rt - s["raw"][0])
        raise ValueError(f"raw time {rt} not in a kept segment of {cut}")

    clips = [dict(c) for c in CLIPS if cut == "extended" or not c.get("ext")]
    for c in clips:
        a_file, a_where = c["anchors"][0]
        a_v = to_v(a_where)
        if c["start"][0] == "cut":
            c["v_start"] = seg_v[c["start"][1]][0] - c["start"][2]
            c["in"] = a_file - (a_v - c["v_start"])
        else:
            c["in"] = 0.0
            c["v_start"] = a_v - a_file
    end_v = voice_end + END_HOLD
    for i, c in enumerate(clips):
        c["v_end"] = clips[i + 1]["v_start"] if i + 1 < len(clips) else end_v
        # piecewise: freezes between anchors so each event lands on its word
        fl = c.get("freeze_lead", 0.1)
        c["freezes"], c["warn"] = [], []
        for (f0, w0), (f1, w1) in zip(c["anchors"], c["anchors"][1:]):
            dv, df = to_v(w1) - to_v(w0), f1 - f0
            # +d = freeze d s at file time t; -d = cut d s of static hold ending at t
            if abs(dv - df) > 0.03:
                c["freezes"].append((round(f1 - fl, 2), round(dv - df, 2)))
            if dv - df < -(f1 - fl - f0 - 0.6):
                c["warn"].append(f"cut before {f1}s eats into the previous event's animation")
        if c["in"] < 0:
            c["warn"].append(f"needs {-c['in']:.2f}s freeze on first frame before start")
        frz = sum(d for _, d in c["freezes"])
        length = c["v_end"] - c["v_start"]
        play = length - frz                      # file seconds actually played
        c["out"] = c["in"] + play
        c["hold"] = max(0.0, c["out"] - c["dur"])  # freeze last frame for this long
        if c["out"] > c["dur"]:
            c["out"] = c["dur"]
        last_event = c["anchors"][-1][0]
        if c["out"] < last_event + 0.3:
            c["warn"].append(f"clip cut at {c['out']:.2f}s, before its last event ({last_event}s) finishes")
        for k in ("v_start", "v_end", "in", "out", "hold"):
            c[k] = round(c[k], 2)
    total = end_v + OUTRO
    plan = dict(cut=cut, segments=segs, clips=clips, voice_end=round(voice_end, 2),
                outro=(round(end_v, 2), round(total, 2)), total=round(total, 2))
    json.dump(plan, open(os.path.join(HERE, f"cutplan-{cut}.json"), "w"), indent=1)
    return plan


def mmss(t):
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:05.2f}"


if __name__ == "__main__":
    for cut in ("main", "extended"):
        p = build(cut)
        print(f"\n===== {cut}: total {mmss(p['total'])} (voice ends {mmss(p['voice_end'])}, outro {mmss(p['outro'][0])}-{mmss(p['outro'][1])})")
        for s in p["segments"]:
            print(f"  {s['name']:5} raw {s['raw'][0]:6.2f}-{s['raw'][1]:6.2f}  ->  {mmss(s['v'][0])}-{mmss(s['v'][1])}  {s['text'][:60]}")
        for c in p["clips"]:
            fz = ", ".join((f"freeze {d}s @{t}" if d > 0 else f"trim {-d}s before {t}") for t, d in c["freezes"]) or "-"
            print(f"  clip {c['id']} {mmss(c['v_start'])}-{mmss(c['v_end'])} ({c['v_end']-c['v_start']:.2f}s)  file {c['in']:.2f}-{c['out']:.2f}  freezes {fz}  hold {c['hold']:.2f}  {'; '.join(c['warn'])}")
