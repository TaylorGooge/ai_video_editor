import asyncio
from playwright.async_api import async_playwright
exec(open('gen.py').read().split('V={}')[0])
html=page(f'''<div class=grid></div><div class=safe>
<div id=mk style="width:420px">{MARK}</div>
<div id=wd class=word style="margin-top:40px"><span class=g>Public</span> by Default</div>
<div class="handle mono"><span id=hd></span><span id=cur style="display:inline-block;width:20px;height:44px;background:#3FB950;vertical-align:-8px;margin-left:6px"></span></div></div>
<div id=bar class=bar></div>
<script>
const H="@publicbydefault";
function c(x){{return Math.max(0,Math.min(1,x))}}
function eo(x){{return 1-Math.pow(1-x,3)}}
function back(x){{const s=2.2;x=x-1;return x*x*((s+1)*x+s)+1}}
function setT(t){{
 const a=c(t/0.45); mk.style.opacity=a; mk.style.transform=`scale(${{0.85+0.15*eo(a)}})`;
 const s=c((t-0.55)/0.4); document.querySelector('.shackle').style.transform=`translateY(${{56*(1-back(s))}}px)`;
 const w=c((t-0.9)/0.45); wd.style.opacity=w; wd.style.transform=`translateY(${{40*(1-eo(w))}}px)`;
 const n=Math.floor(c((t-1.4)/0.8)*H.length); hd.textContent=H.slice(0,n);
 cur.style.opacity=(t<1.35)?0:((Math.floor(t*2.5)%2==0)?1:0);
 bar.style.transform=`scaleX(${{eo(c((t-0.2)/1.2))}})`; bar.style.transformOrigin='left';
}}
</script>''')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1920})
        await pg.set_content(html); await pg.wait_for_timeout(200)
        fps=30
        for i in range(int(3.5*fps)):
            await pg.evaluate(f"setT({i/fps})")
            await pg.screenshot(path=f"frames/{i:04d}.png")
        await b.close()
asyncio.run(main())
