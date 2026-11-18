r"""Long-form .srt + chapters.txt from the edited voice.
Run: tools\.venv\Scripts\python.exe -I work\v_s1a\make_captions.py
Word timing: Whisper small.en run on build\voice-edit.wav (already in the edited timeline: build\check\edit-v3.json).
Text: proofed against script.md (FIX below; every fix keeps the word count so times map 1:1).
Cues: one sentence per cue where it fits, else split at the comma (or word) nearest the middle; max 2 lines x 42 chars."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "done", "v_s1a", "long")); os.makedirs(OUT, exist_ok=True)
plan = json.load(open(os.path.join(HERE, "cutplan.json")))
d = json.load(open(os.path.join(HERE, "build", "check", "edit-v3.json"), encoding="utf-8"))
words = [dict(w=w["word"].strip(), s=w["start"], e=w["end"]) for seg in d["segments"] for w in seg["words"] if w["start"] < plan["voice_end"]]

NB = " "   # joins two words into one token (keeps word count)
DROP = "~DROP~"  # placeholder token removed from the output
Q = '"'
FIX = [
    ("Superbase", "Supabase"), ("Anna", "Ana"), ("goes to bed now", "goes to Ben now"), ("The cat booking", "The cats booking"),
    ("pet's answers blank", f"pets answer{NB}as blank"), ("say nothing. No.", "say nothing. Null."),
    ("It's for stop asking", "It's four. Stop asking"), ("Each one treats, we didn't ask, as no.", f"Each one treats {Q}we didn't ask{Q} as {Q}no{Q}."),
    ("treats blank as no pets", f"treats blank as {Q}no pets{Q}"), ("needs pet-friendly cleaner badge", f"{Q}Needs pet-friendly cleaner{Q} badge"),
    ("Unknown now means might have pets", f"Unknown now means {Q}might have pets{Q}"), ("shows unknown instead of no", f"shows {Q}Unknown{Q} instead of {Q}No{Q}"),
    ("Auto-assigned skips", "Auto-assign skips"), ("Unknown, flag for staff", "Unknown. Flagged for staff"), ("Staff confirmed the dog", "Staff confirm the dog"),
    ("we have two cats.", f"{Q}We have two cats.{Q}"), ("And otherwise includes, we never asked", f"And {Q}otherwise{Q} includes {Q}we never asked{Q}"),
    ("Its map of where is this used", f"Its map of {Q}where is this used{Q}"), ("Remove the question sounds", f"{Q}Remove the question{Q} sounds"),
    ("handle unknown first", f"handle {Q}unknown{Q} first"), ("a confirm pets with customer badge", f"a {Q}Confirm pets with customer{Q} badge"),
    ("Matching, only", "Matching: only"), ("Staff page, unknown,", f"Staff page: {Q}Unknown{Q},"),
    ("drop down", f"dropdown {DROP}"), ("never add cascade", f"never add {Q}cascade{Q}"), ("decide what remove means", f"decide what {Q}remove{Q} means"),
    ("a lot of where, make sure", "a lot of where. Make sure"), ("everywhere, and decide", "everywhere. And decide"),
]

toks = []
for w in words:  # Whisper splits "pet-friendly" as "pet" + "-friendly": glue those back
    if toks and w["w"].startswith("-"): toks[-1] = dict(w=toks[-1]["w"] + w["w"], s=toks[-1]["s"], e=w["e"])
    else: toks.append(w)
text = " ".join(t["w"] for t in toks)
for a, b in FIX:
    if a not in text: print("proof fix not applied:", a)
    text = text.replace(a, b)
fixed = text.split(" ")
assert len(fixed) == len(toks), (len(fixed), len(toks))
def time_at(i, end=False): return toks[i]["e"] if end else toks[i]["s"]

def wrap(t):
    if len(t) <= 42: return t
    best = None
    for k, ch in enumerate(t):
        if ch == " ":
            a, b = t[:k], t[k + 1:]
            if len(a) <= 42 and len(b) <= 42:
                score = abs(len(a) - len(b)) - (8 if re.search(r"[,.:?!]\"?$", a) else 0)
                if best is None or score < best[0]: best = (score, a + "\n" + b)
    return best[1] if best else t

txt = lambda ids: " ".join(fixed[i] for i in ids).replace(NB, " ")
def fits(ids):
    lines = wrap(txt(ids)).split("\n")
    return len(lines) <= 2 and all(len(l) <= 42 for l in lines)
def split(ids):
    if fits(ids) or len(ids) < 2: return [ids]
    best = None
    for k in range(1, len(ids)):
        a, b = ids[:k], ids[k:]
        score = abs(len(txt(a)) - len(txt(b))) - (25 if re.search(r"[,:;]\"?$", fixed[ids[k - 1]]) else 0) + (40 if min(len(a), len(b)) < 3 else 0)
        if best is None or score < best[0]: best = (score, a, b)
    return split(best[1]) + split(best[2])

idx = [i for i, w in enumerate(fixed) if w != DROP]
sents, cur = [], []
for i in idx:
    cur.append(i)
    if re.search(r"[.?!]\"?$", fixed[i]): sents.append(cur); cur = []
if cur: sents.append(cur)
chunks = []
for sn in sents:
    for ch in split(sn):
        prev = chunks[-1] if chunks else None
        if prev and len(txt(prev)) + len(txt(ch)) < 44 and time_at(ch[0]) - time_at(prev[-1], True) < 0.5 and fits(prev + ch):
            chunks[-1] = prev + ch
        else:
            chunks.append(ch)
cues = [[time_at(c[0]), time_at(c[-1], True), txt(c)] for c in chunks]

def ts(t):
    ms = int(round(max(0, t) * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

with open(os.path.join(OUT, "v_s1a.srt"), "w", encoding="utf-8") as f:
    for n, (a, b, t) in enumerate(cues, 1):
        nxt = cues[n][0] if n < len(cues) else b + 2
        b = min(max(b + 0.25, a + 1.0), nxt - 0.05)
        f.write(f"{n}\n{ts(a)} --> {ts(b)}\n{wrap(t)}\n\n")
print(len(cues), "cues; not fitting 2x42:", [c[2] for c in cues if not fits([0]) and False] or [t for _, _, t in cues if any(len(l) > 42 for l in wrap(t).split("\n")) or wrap(t).count("\n") > 1])

titles = ["Two cats, no fee, wrong cleaner", "What the AI did, and what it said", "Where the fee lives", "Same prompt, database connected",
          "Null is not \"no\"", "Remove a field in order", "Verify", "Paste these"]
starts = [0] + [c["v0"] for c in plan["cards"] if c["label"].startswith("CH")]
with open(os.path.join(OUT, "chapters.txt"), "w", encoding="utf-8") as f:
    for t, name in zip(starts, titles):
        f.write(f"{int(t // 60)}:{int(t % 60):02d} {name}\n")
