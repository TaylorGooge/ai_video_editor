import asyncio
from playwright.async_api import async_playwright
MARK='''<svg viewBox="130 115.5 540 540" xmlns="http://www.w3.org/2000/svg"><path class="shackle" d="M310 392 V262 A90 90 0 0 1 490 262 V318" fill="none" stroke="#E6EDF3" stroke-width="46" stroke-linecap="round"/><rect x="240" y="372" width="320" height="250" rx="40" fill="#3FB950"/><circle cx="400" cy="470" r="30" fill="#0D1117"/><rect x="386" y="480" width="28" height="74" rx="10" fill="#0D1117"/></svg>'''
BASE='''*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#0D1117;color:#E6EDF3;font-family:Inter,sans-serif;overflow:hidden;position:relative}
body.clear{background:transparent}
.grid{position:absolute;inset:0;background-image:linear-gradient(#30363D33 1px,transparent 1px),linear-gradient(90deg,#30363D33 1px,transparent 1px);background-size:80px 80px}
.mono{font-family:"JetBrains Mono","DejaVu Sans Mono",monospace}
.g{color:#3FB950}.m{color:#8B949E}
/* safe column: clear of right-side buttons and bottom caption area */
.safe{position:absolute;left:100px;width:780px;top:0;height:1920px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding-bottom:160px}
.word{font-weight:700;font-size:96px;letter-spacing:-2.5px;line-height:1}
.handle{margin-top:36px;font-size:44px;color:#8B949E}
.pill{display:inline-block;margin-top:56px;background:#3FB950;color:#0D1117;font-weight:700;font-size:44px;padding:26px 56px;border-radius:999px;letter-spacing:.02em}
.kicker{font-size:34px;font-weight:700;letter-spacing:.16em;color:#3FB950;text-transform:uppercase}
.bar{position:absolute;left:0;right:0;bottom:0;height:10px;background:#3FB950}
.card{background:#161B22;border-left:6px solid #3FB950;border-radius:14px;text-align:left;padding:44px 48px;width:780px}
'''
def page(body, cls=""):
    return f"<html><head><style>{BASE}</style></head><body class='{cls}'>{body}</body></html>"
V={}
# 1 Classic stacked lockup
V["pbd-endcard-01-stacked"]=page(f'''<div class=grid></div><div class=safe>
<div style="width:420px">{MARK}</div>
<div class=word style="margin-top:40px"><span class=g>Public</span> by Default</div>
<div class="handle mono">@publicbydefault</div></div><div class=bar></div>''')
# 2 Follow CTA
V["pbd-endcard-02-follow"]=page(f'''<div class=grid></div><div class=safe>
<div style="width:300px">{MARK}</div>
<div class=word style="margin-top:36px;font-size:84px"><span class=g>Public</span> by Default</div>
<div style="margin-top:56px;font-size:52px;font-weight:600;line-height:1.25">Find the hole<br>before someone else does.</div>
<div class=pill>Follow @publicbydefault</div></div><div class=bar></div>''')
# 3 Series
V["pbd-endcard-03-series"]=page(f'''<div class=grid></div><div class=safe>
<div class=kicker>A Public by Default series</div>
<div style="margin-top:36px;font-size:96px;font-weight:700;line-height:1.05;letter-spacing:-2.5px">The AI Did<br>What You <span class=g>Asked</span></div>
<div style="width:180px;margin-top:80px">{MARK}</div>
<div class="handle mono" style="margin-top:28px">@publicbydefault</div></div><div class=bar></div>''')
# 4 Terminal / prompt card
V["pbd-endcard-04-terminal"]=page(f'''<div class=grid></div><div class=safe>
<div style="display:flex;align-items:center;gap:28px;margin-bottom:64px"><div style="width:130px">{MARK}</div>
<div class=word style="font-size:64px;letter-spacing:-1.5px;text-align:left;line-height:1.05"><span class=g>Public</span><br>by Default</div></div>
<div class=card><div style="font-size:26px;font-weight:700;letter-spacing:.14em;color:#3FB950;margin-bottom:22px">NEXT STEP</div>
<div class=mono style="font-size:40px;line-height:1.5"><span class=m>$</span> follow <span class=g>@publicbydefault</span><span style="display:inline-block;width:22px;height:44px;background:#3FB950;vertical-align:-6px;margin-left:8px"></span></div>
<div class=mono style="font-size:30px;color:#8B949E;margin-top:16px">› security for vibe coders</div></div></div><div class=bar></div>''')
# 5 Transparent overlay (stacked, with soft panel for readability over footage)
V["pbd-endcard-05-overlay-transparent"]=page(f'''<div class=safe>
<div style="background:#0D1117E6;border-radius:40px;padding:72px 80px;display:flex;flex-direction:column;align-items:center">
<div style="width:300px">{MARK}</div>
<div class=word style="margin-top:32px;font-size:80px"><span class=g>Public</span> by Default</div>
<div class="handle mono" style="font-size:40px">@publicbydefault</div></div></div>''',"clear")
# Safe-zone check versions
GUIDE='''<div style="position:absolute;right:0;top:700px;width:150px;height:900px;background:#F8514955"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:380px;background:#F8514933"></div>
<div style="position:absolute;left:0;right:0;top:0;height:160px;background:#F8514933"></div>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1920})
        for k,h in V.items():
            await pg.set_content(h); await pg.wait_for_timeout(150)
            await pg.screenshot(path=f"out/{k}.png",omit_background=("transparent" in k))
            await pg.set_content(h.replace("</body>",GUIDE+"</body>")); await pg.wait_for_timeout(100)
            await pg.screenshot(path=f"check/{k}.png")
        await b.close()
asyncio.run(main())
