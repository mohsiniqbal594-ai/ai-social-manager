"""Render the 20 Velmore Inn December posts (1080x1350) from HTML templates.

Usage:  python3 velmore-inn/render/build_posts.py   (needs Node + playwright)
Output: velmore-inn/posts/post-XX.png  (+ velmore-inn/posts/all-posts.pdf)
"""
import pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = (ROOT / "assets").as_uri()
OUT = ROOT / "posts"
OUT.mkdir(exist_ok=True)

PHONE = "+92 345 1000329"
ADDRESS = "Plaza 13, I&amp;T Centre, G-9/4, Islamabad"

IMG = {k: f"{A}/{v}" for k, v in {
    "reception": "reception.png", "lift": "lobby-lift.png", "stair": "floating-staircase.png",
    "deluxe": "deluxe-lounge-room.png", "family": "family-room.png", "twin": "twin-room-zebra.png",
    "logo": "logo-velmore-inn-transparent.png"}.items()}

# ---------- icons (thin line, gold) ----------
def ico(name, s=46):
    p = {
     "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
     "pin": '<path d="M12 22s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="10" r="2.6"/>',
     "bed": '<path d="M3 18V7M3 14h18v4M21 14v-2a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="11" r="2"/>',
     "bell": '<path d="M4 17h16M6 17a6 6 0 0 1 12 0M12 9V7M10 7h4M3 20h18"/>',
     "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
     "snow": '<path d="M12 2v20M4 7l16 10M20 7L4 17"/>',
     "lift": '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M12 3v18M8.5 9l-1.5 2h3zM15.5 11l-1.5-2 -1.5 2z"/>',
     "cam": '<path d="M3 7h12l3 3-3 3H3zM6 13v4M3 17h6"/><circle cx="18.5" cy="10" r="1"/>',
     "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
     "family": '<circle cx="8" cy="6" r="2.2"/><circle cx="16" cy="6" r="2.2"/><circle cx="12" cy="12" r="1.8"/><path d="M4 20v-6a4 4 0 0 1 8 0M12 20v-4M12 14a4 4 0 0 1 8 0v6"/>',
     "spark": '<path d="M12 3l2 6 6 2-6 2-2 6-2-6-6-2 6-2z"/>',
     "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
     "brief": '<rect x="3" y="7" width="18" height="13" rx="1.5"/><path d="M9 7V5h6v2M3 12h18"/>',
     "moon": '<path d="M20 14A8 8 0 1 1 10 4a6.5 6.5 0 0 0 10 10z"/>',
     "clean": '<path d="M5 21l3-9h8l3 9M9 12V4h6v8M7 16h10"/>',
    }[name]
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Great+Vibes&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Montserrat:wght@400;500;600;700&display=swap');
:root{--esp:#2B1D14;--bronze:#8A5A2B;--gold:#C9A04E;--amber:#F2B33D;--trav:#EDE3D1;--marble:#F7F4EE;}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden;background:var(--esp)}
.post{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Montserrat,sans-serif;color:var(--marble)}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.shade-top{position:absolute;left:0;right:0;top:0;height:560px;background:linear-gradient(rgba(25,16,10,.92),rgba(25,16,10,.55) 55%,rgba(25,16,10,0))}
.shade-bot{position:absolute;left:0;right:0;bottom:0;height:640px;background:linear-gradient(rgba(25,16,10,0),rgba(25,16,10,.75) 45%,rgba(25,16,10,.96))}
.logo{position:absolute;top:54px;left:50%;transform:translateX(-50%);width:400px;filter:drop-shadow(0 2px 10px rgba(0,0,0,.55))}
.logo-line{position:absolute;top:128px;left:50%;transform:translateX(-50%);width:120px;height:1px;background:var(--gold);opacity:.7}
.cinzel{font-family:Cinzel,serif;font-weight:600;letter-spacing:.04em;line-height:1.08;text-transform:uppercase}
.script{font-family:'Great Vibes',cursive;color:var(--gold);line-height:1;font-weight:400}
.corm{font-family:'Cormorant Garamond',serif}
.gold{color:var(--gold)}
.center{text-align:center}
.abs{position:absolute}
.footer{position:absolute;left:0;right:0;bottom:0;height:150px;background:var(--esp);border-top:2px solid var(--gold);
  display:flex;align-items:center;justify-content:space-between;padding:0 56px;gap:24px}
.footer .item{display:flex;align-items:center;gap:18px;color:var(--gold)}
.footer .t1{font-size:17px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);font-weight:600}
.footer .t2{font-size:30px;font-weight:600;color:var(--marble);letter-spacing:.02em;margin-top:4px}
.footer .t3{font-size:23px;font-weight:500;color:var(--marble);margin-top:4px}
.footer .sep{width:1px;height:78px;background:rgba(201,160,78,.5)}
.btn{display:inline-block;background:var(--gold);color:var(--esp);font-weight:700;letter-spacing:.18em;text-transform:uppercase;font-size:22px;padding:18px 38px;border-radius:60px}
.tile{position:absolute;border:6px solid #fff;border-radius:34px;overflow:hidden;box-shadow:0 18px 40px rgba(0,0,0,.45)}
.tile img{width:100%;height:100%;object-fit:cover;display:block}
.divider{display:flex;align-items:center;justify-content:center;gap:16px;color:var(--gold)}
.divider:before,.divider:after{content:"";width:150px;height:1px;background:currentColor}
"""

def footer():
    return f"""<div class="footer">
  <div class="item">{ico('phone',54)}<div><div class="t1">Call / WhatsApp</div><div class="t2">{PHONE}</div></div></div>
  <div class="sep"></div>
  <div class="item">{ico('pin',54)}<div><div class="t1">Visit Us</div><div class="t3">{ADDRESS}</div></div></div>
</div>"""

def logo(top=54, w=400):
    return f'<img class="logo" style="top:{top}px;width:{w}px" src="{IMG["logo"]}">'

def page(body, extra_css=""):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{extra_css}</style></head><body><div class='post'>{body}{footer()}</div></body></html>"

# ---------- layouts ----------
def hero(img, pos, script, head, sub="", where="top", cta=None, sparkle=False, after=""):
    if where == "top":
        txt = f"""<div class="shade-top" style="height:720px"></div>
        <div class="abs center" style="top:190px;left:60px;right:60px">
          {f'<div class="script" style="font-size:120px;margin-bottom:-6px">{script}</div>' if script else ''}
          <div class="cinzel" style="font-size:66px">{head}</div>
          {f'<div class="corm" style="font-size:40px;font-style:italic;margin-top:18px;color:var(--trav)">{sub}</div>' if sub else ''}
        </div>"""
        bot = '<div class="shade-bot" style="height:300px"></div>'
    else:
        txt = f"""<div class="shade-top" style="height:300px"></div><div class="shade-bot" style="height:760px"></div>
        <div class="abs center" style="bottom:200px;left:60px;right:60px">
          {f'<div class="script" style="font-size:112px;line-height:1.15;margin-bottom:14px">{script}</div>' if script else ''}
          <div class="cinzel" style="font-size:64px">{head}</div>
          {f'<div class="script" style="font-size:140px;margin-top:4px">{after}</div>' if after else ''}
          {f'<div class="corm" style="font-size:40px;font-style:italic;margin-top:16px;color:var(--trav)">{sub}</div>' if sub else ''}
          {f'<div style="margin-top:34px"><span class="btn">{cta}</span></div>' if cta else ''}
        </div>"""
        bot = ""
    sp = SPARKLE if sparkle else ""
    return page(f'<img class="bg" style="object-position:{pos}" src="{IMG[img]}">{bot}{txt}{sp}{logo()}')

SPARKLE = "".join(
    f'<div class="abs" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;background:#E9C978;opacity:{o};box-shadow:0 0 {r*3}px #E9C978"></div>'
    for x, y, r, o in [(40,40,5,.9),(90,110,3,.8),(150,60,4,.7),(60,190,3,.6),(210,140,2,.8),(120,260,3,.5),
                       (260,50,3,.6),(30,320,2,.5),(190,230,2,.6),(310,110,2,.5),(80,380,2,.4),(240,300,2,.4)])

def split(img, pos, head, script, side="left"):
    panel = f"""<div class="abs" style="top:0;bottom:150px;{side}:0;width:440px;background:linear-gradient(160deg,#3a271a,var(--esp));"></div>
    <div class="abs" style="top:300px;{side}:0;width:440px;padding:0 50px">
      <div style="width:70px;height:2px;background:var(--gold);margin-bottom:34px"></div>
      <div class="cinzel" style="font-size:52px;line-height:1.15">{head}</div>
      <div class="script" style="font-size:96px;margin-top:26px">{script}</div>
    </div>"""
    other = "right" if side == "left" else "left"
    photo = f'<img class="abs" style="top:0;{other}:0;width:640px;height:1200px;object-fit:cover;object-position:{pos}" src="{IMG[img]}">'
    return page(photo + panel + '<div class="shade-top" style="height:230px"></div>' + logo())

def trio(imgs, head, sub, script, bg="family"):
    t = ""
    xs = [(70, 270, -4), (390, 250, 0), (710, 270, 4)]
    for (x, y, r), im in zip(xs, imgs):
        t += f'<div class="tile" style="left:{x}px;top:{y}px;width:300px;height:400px;transform:rotate({r}deg)"><img src="{IMG[im]}"></div>'
    return page(f"""<img class="bg" style="filter:blur(3px) brightness(.45)" src="{IMG[bg]}">
    <div class="abs" style="inset:0;background:linear-gradient(rgba(43,29,20,.55),rgba(43,29,20,.85))"></div>{SPARKLE}
    {logo()}{t}
    <div class="abs center" style="top:745px;left:70px;right:70px">
      <div class="cinzel" style="font-size:58px">{head}</div>
      <div style="font-size:24px;letter-spacing:.35em;text-transform:uppercase;color:var(--trav);margin-top:22px">{sub}</div>
      <div class="script" style="font-size:96px;margin-top:22px">{script}</div>
    </div>""")

def cream(img, pos, head, sub, icons):
    cells = "".join(f'<div style="flex:1;text-align:center;color:var(--bronze)">{ico(i,64)}<div style="margin-top:12px;font-size:24px;color:var(--esp);font-weight:500;letter-spacing:.06em">{l}</div></div>'
                    + ('<div style="width:1px;background:rgba(138,90,43,.35)"></div>' if n < len(icons)-1 else '')
                    for n, (i, l) in enumerate(icons))
    return page(f"""<div class="abs" style="inset:0;background:var(--trav)"></div>
    <div class="abs" style="left:200px;right:200px;top:0;height:640px;background:linear-gradient(#C8AE8A,#E6D7BF)"></div>
    <div class="abs" style="left:50%;top:60px;transform:translateX(-50%);width:400px;height:90px;border-radius:50px;background:var(--esp)"></div>
    <img class="logo" style="top:83px;width:330px;filter:none" src="{IMG['logo']}">
    <div class="abs center" style="top:205px;left:80px;right:80px;color:var(--esp)">
      <div class="cinzel" style="font-size:60px">{head}</div>
      <div class="divider" style="margin:20px 0 14px">◆</div>
      <div class="corm" style="font-size:40px;font-style:italic">{sub}</div>
    </div>
    <img class="abs" style="left:90px;right:90px;width:900px;top:430px;height:540px;object-fit:cover;object-position:{pos};border-radius:6px;box-shadow:0 20px 50px rgba(43,29,20,.35)" src="{IMG[img]}">
    <div class="abs" style="left:90px;right:90px;top:1010px;display:flex;gap:10px">{cells}</div>""")

def newspaper(img, pos, mast, head, sub, footerline, kicker="DAILY EDITION", bg="reception"):
    return page(f"""<img class="bg" style="filter:blur(6px) brightness(.5)" src="{IMG[bg]}">
    {logo(40, 360)}
    <div class="abs" style="left:110px;top:150px;width:860px;height:1010px;background:#F4F0E6;transform:rotate(-1.2deg);
         box-shadow:0 30px 60px rgba(0,0,0,.6);padding:34px 44px;color:#1d1d1d;font-family:'Cormorant Garamond',serif">
      <div style="font-family:Cinzel,serif;font-weight:700;font-size:62px;text-align:center;letter-spacing:.02em">{mast}</div>
      <div style="border-top:3px double #333;border-bottom:1px solid #333;margin-top:10px;padding:6px 0;display:flex;justify-content:space-between;font-size:19px;font-family:Montserrat;letter-spacing:.08em">
        <span>EST. 2026</span><span>Islamabad's Boutique Stay · G-9</span><span>{kicker}</span></div>
      <div style="font-weight:600;font-size:66px;line-height:1.02;text-align:center;margin-top:22px">{head}</div>
      <div class="divider" style="color:#444;margin-top:14px;font-size:30px;font-style:italic">{sub}</div>
      <img style="width:100%;height:520px;object-fit:cover;object-position:{pos};margin-top:22px;filter:saturate(.9)" src="{IMG[img]}">
      <div style="border-top:1px solid #333;margin-top:18px;padding-top:12px;text-align:center;font-size:28px">{footerline}</div>
    </div>""")

def bubbles(img, pos, head, items):
    spots = [(70, 560, -8), (190, 300, -6), (430, 205, 0), (680, 300, 6), (820, 560, 8)]
    b = "".join(f'<div class="abs center" style="left:{x}px;top:{y}px;width:190px;height:190px;background:#fff;border-radius:42px;transform:rotate({r}deg);'
                f'box-shadow:0 14px 30px rgba(0,0,0,.4);color:var(--esp);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px">'
                f'<div style="color:var(--bronze)">{ico(i,66)}</div><div style="font-weight:700;font-size:21px;line-height:1.15">{l}</div></div>'
                for (x, y, r), (i, l) in zip(spots, items))
    return page(f"""<img class="bg" style="object-position:{pos}" src="{IMG[img]}">
    <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 55%,rgba(43,29,20,.25),rgba(43,29,20,.8))"></div>
    {logo()}{b}
    <div class="abs center cinzel" style="top:820px;left:100px;right:100px;font-size:56px;text-shadow:0 3px 18px rgba(0,0,0,.7)">{head}</div>""")

def doorhanger(img, pos, l1, l2, l3):
    return page(f"""<div class="abs" style="left:0;top:0;bottom:0;width:480px;background:repeating-linear-gradient(90deg,#3b2618 0 22px,#341f13 22px 44px)"></div>
    <img class="abs" style="left:480px;top:0;width:600px;height:1200px;object-fit:cover;object-position:{pos}" src="{IMG[img]}">
    <div class="abs" style="left:470px;top:0;width:18px;height:1200px;background:linear-gradient(90deg,#1c120b,#4a3020);box-shadow:4px 0 16px rgba(0,0,0,.5)"></div>
    <div class="abs" style="left:-40px;top:420px;width:400px;height:58px;border-radius:30px;background:linear-gradient(#e3c27a,#a97f33);box-shadow:0 8px 16px rgba(0,0,0,.5)"></div>
    <div class="abs" style="left:300px;top:395px;width:110px;height:110px;border-radius:50%;background:radial-gradient(#e9cb85,#9b742f);box-shadow:0 8px 16px rgba(0,0,0,.5)"></div>
    <div class="abs" style="left:120px;top:340px;width:330px;height:640px;background:#FBF8F2;border-radius:26px;box-shadow:0 20px 40px rgba(0,0,0,.55);transform:rotate(-2deg);color:var(--esp);text-align:center;padding:220px 26px 0">
      <div class="abs" style="left:105px;top:36px;width:120px;height:120px;border-radius:50%;background:#3b2618;box-shadow:inset 0 4px 10px rgba(0,0,0,.6)"></div>
      <div style="font-family:Cinzel;font-weight:700;font-size:44px;line-height:1.05">{l1}</div>
      <div class="script" style="font-size:78px;margin-top:14px;color:var(--bronze)">{l2}</div>
      <div style="font-family:Montserrat;font-weight:700;font-size:23px;letter-spacing:.22em;margin-top:12px">{l3}</div>
      <img style="width:240px;margin-top:40px" src="{IMG['logo']}">
    </div>
    <div class="shade-top" style="height:220px;left:480px"></div>{logo(54,360).replace('left:50%','left:780px')}""")

def stack(main, mpos, side, head, script, sub):
    s = "".join(f'<div class="tile" style="left:700px;top:{150+i*340}px;width:340px;height:310px;border-width:4px;border-radius:26px"><img src="{IMG[im]}"></div>'
                for i, im in enumerate(side))
    return page(f"""<div class="abs" style="inset:0;background:linear-gradient(135deg,#3a2416,#22160f)"></div>
    <img class="abs" style="left:0;top:0;width:670px;height:1200px;object-fit:cover;object-position:{mpos}" src="{IMG[main]}">
    <div class="abs" style="left:0;top:0;width:670px;height:1200px;background:linear-gradient(rgba(25,16,10,.85),rgba(25,16,10,.1) 30%,rgba(25,16,10,.1) 50%,rgba(25,16,10,.95))"></div>
    {s}{logo(54,330).replace('left:50%','left:335px')}
    <div class="abs" style="left:50px;width:600px;bottom:200px">
      <div class="script" style="font-size:96px">{script}</div>
      <div class="cinzel" style="font-size:46px;line-height:1.15">{head}</div>
      <div style="font-size:22px;letter-spacing:.28em;text-transform:uppercase;color:var(--trav);margin-top:18px">{sub}</div>
    </div>""")

def glass(bg, head, sub, icons, tiles):
    cells = "".join(f'<div style="flex:1;text-align:center;color:#fff">{ico(i,62)}<div style="margin-top:10px;font-size:22px;line-height:1.25">{l}</div></div>'
                    + ('<div style="width:1px;background:rgba(255,255,255,.45)"></div>' if n < len(icons)-1 else '')
                    for n, (i, l) in enumerate(icons))
    t = "".join(f'<div class="tile" style="left:{70+i*320}px;top:830px;width:300px;height:300px;border-width:5px;border-radius:30px"><img src="{IMG[im]}"></div>' for i, im in enumerate(tiles))
    return page(f"""<img class="bg" style="filter:blur(8px) brightness(.7)" src="{IMG[bg]}">
    <div class="abs" style="inset:0;background:rgba(43,29,20,.35)"></div>
    {logo()}
    <div class="abs" style="left:50px;right:50px;top:170px;height:610px;border-radius:40px;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.4);backdrop-filter:blur(10px)"></div>
    <div class="abs center" style="top:205px;left:80px;right:80px">
      <div class="cinzel" style="font-size:50px">{head}</div>
      <div class="corm" style="font-size:32px;font-style:italic;margin-top:8px;color:var(--trav)">{sub}</div>
    </div>
    <div class="abs center" style="top:470px;left:50%;transform:translateX(-50%);background:linear-gradient(90deg,#5b3a22,#8A5A2B);padding:12px 46px;border-radius:40px;font-family:Cinzel;font-weight:700;font-size:28px;letter-spacing:.12em">AMENITIES</div>
    <div class="abs" style="left:90px;right:90px;top:500px;height:250px;border:2px solid rgba(255,255,255,.7);border-radius:30px;display:flex;align-items:center;padding:30px 20px 10px">{cells}</div>
    {t}""")

def mapcard():
    roads = "".join(f'<path d="M{a}" stroke="#fff" stroke-width="{w}" fill="none"/>' for a, w in [
        ("0 330 L900 300", 22), ("80 0 L120 620", 10), ("330 0 L360 620", 10), ("600 0 L620 620", 10), ("0 150 L900 140", 8),
        ("0 470 L900 455", 8), ("180 0 L200 620", 5), ("470 0 L490 620", 5), ("750 0 L770 620", 5), ("0 80 L900 70", 4), ("0 240 L900 228", 4), ("0 400 L900 385", 4), ("0 560 L900 545", 4)])
    labels = """
      <text x="40" y="318" font-size="22" fill="#8a8a8a" font-family="Montserrat" transform="rotate(-2 40 318)">Srinagar Highway</text>
      <text x="380" y="210" font-size="26" fill="#0f8a5f" font-family="Montserrat" font-weight="600">G-9 Markaz</text>
      <text x="390" y="240" font-size="18" fill="#0f8a5f" font-family="Montserrat">Karachi Company</text>
      <text x="660" y="110" font-size="24" fill="#c0392b" font-family="Montserrat" font-weight="600">PIMS · G-8</text>
      <text x="30" y="110" font-size="22" fill="#0f8a5f" font-family="Montserrat">F-9 Park ↑</text>
      <text x="40" y="540" font-size="22" fill="#8a8a8a" font-family="Montserrat">G-10 ←</text>
      <text x="690" y="540" font-size="22" fill="#8a8a8a" font-family="Montserrat">→ Blue Area</text>"""
    return f"""<svg width="900" height="620" viewBox="0 0 900 620"><rect width="900" height="620" fill="#EEF0EC"/>
      <rect x="370" y="160" width="220" height="140" fill="#dff1e6"/>{roads}{labels}
      <g transform="translate(510 380)"><path d="M0 0c-26-34-40-52-40-72a40 40 0 0 1 80 0c0 20-14 38-40 72z" fill="#C9A04E" stroke="#2B1D14" stroke-width="3"/><circle cx="0" cy="-72" r="14" fill="#2B1D14"/></g>
      <text x="560" y="350" font-size="30" font-weight="700" fill="#2B1D14" font-family="Montserrat">Velmore Inn</text>
      <text x="560" y="380" font-size="22" fill="#555" font-family="Montserrat">G-9/4 · I&amp;T Centre</text></svg>"""

def mappost():
    return page(f"""<img class="bg" style="filter:blur(10px) brightness(.4)" src="{IMG['reception']}">
    <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(120,40,20,.25),rgba(20,12,8,.7))"></div>{logo()}
    <div class="abs" style="left:90px;top:580px;transform:perspective(1400px) rotateX(38deg) rotateZ(-4deg) scale(.92);transform-origin:50% 0;box-shadow:0 40px 80px rgba(0,0,0,.7)">{mapcard()}</div>
    <svg class="abs" style="left:170px;top:170px" width="740" height="470" viewBox="0 0 740 470" fill="none" stroke="#C9A04E" stroke-linecap="round" stroke-linejoin="round">
      <path d="M40 40 C200 20 520 15 700 35 C715 120 712 230 690 300 C560 315 470 318 420 320 L380 450 L330 322 C220 322 110 318 50 305 C30 220 28 120 40 40Z" stroke-width="14" opacity=".95"/>
      <path d="M55 52 C210 35 520 30 688 48 C700 130 698 225 680 290 C560 302 470 305 410 308 L382 420 L340 310 C220 310 110 306 62 295 C45 215 44 125 55 52Z" stroke-width="4" opacity=".6"/>
    </svg>
    <div class="abs center" style="top:225px;left:240px;right:240px">
      <div style="display:flex;align-items:baseline;justify-content:center;gap:16px"><span class="corm" style="font-size:64px;font-weight:600">Find</span><span style="font-size:24px;letter-spacing:.2em;font-weight:600">US IN THE HEART OF</span></div>
      <div class="script" style="font-size:120px;color:#fff;line-height:1.2;margin-top:4px">G-9</div>
      <div style="display:inline-block;border:2px solid #fff;padding:6px 18px;font-size:20px;letter-spacing:.3em;font-weight:600;margin-top:2px">VELMORE INN</div>
    </div>""")

def greeting(script, head, sub, img="reception"):
    return page(f"""<img class="bg" style="filter:blur(4px) brightness(.35)" src="{IMG[img]}">
    <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(43,29,20,.3),rgba(25,16,10,.95))"></div>
    {SPARKLE}<div style="transform:scaleX(-1);position:absolute;inset:0">{SPARKLE}</div>
    <div class="abs" style="left:90px;right:90px;top:90px;bottom:240px;border:2px solid rgba(201,160,78,.7)"></div>
    <div class="abs" style="left:110px;right:110px;top:110px;bottom:260px;border:1px solid rgba(201,160,78,.35)"></div>
    <img class="logo" style="top:200px;width:460px" src="{IMG['logo']}">
    <div class="abs center" style="top:400px;left:120px;right:120px">
      <div class="script" style="font-size:150px">{script}</div>
      <div class="cinzel" style="font-size:60px;margin-top:20px">{head}</div>
      <div class="divider" style="margin:34px 0 24px">◆</div>
      <div class="corm" style="font-size:40px;font-style:italic;color:var(--trav)">{sub}</div>
    </div>""")

# ---------- the 20 posts ----------
POSTS = [
 hero("reception", "50% 40%", "", "This isn't a<br>5-star lobby.", "", "bottom", after="It's G-9."),
 mappost(),
 hero("stair", "50% 55%", "Crafted", "Floating timber.<br>Hidden light.", "Every step glows.", "top"),
 trio(["deluxe", "family", "twin"], "Where are you staying<br>this weekend?", "Deluxe · Family · Twin", "Book Your Stay Now"),
 split("family", "40% 50%", "Tired of rooms that don't match the photos?", "These are real."),
 cream("twin", "50% 60%", "Visiting PIMS?", "Stay just minutes away.", [("pin", "Close By"), ("clean", "Spotless"), ("moon", "Calm Nights")]),
 newspaper("deluxe", "50% 55%", "THE VELMORE TIMES", "Your Perfect Stay<br>Starts in G-9", "Experience Premium Comfort", "Comfort · Elegance · Hospitality"),
 hero("lift", "50% 50%", "Welcome", "POV: You walked in<br>expecting an inn.", "", "bottom"),
 bubbles("family", "50% 60%", "Everything you need.<br>Nothing you don't.", [("snow", "AC Rooms"), ("lift", "Lift Access"), ("family", "Family Rooms"), ("cam", "CCTV Security"), ("pin", "Prime G-9")]),
 doorhanger("twin", "35% 50%", "DO NOT DISTURB", "comfort", "IN PROGRESS"),
 stack("reception", "50% 40%", ["lift", "deluxe", "stair"], "Your meeting is 10 minutes away.<br>Your bed is 10 steps away.", "Business Stays", "Check in · Rest · Show up sharp"),
 glass("lift", "Marble floors.<br>Coffered light.", "Quiet nights, designed in.", [("snow", "Air-<br>conditioned"), ("lift", "Lift<br>Access"), ("cam", "CCTV<br>Security"), ("family", "Family<br>Rooms")], ["deluxe", "family", "twin"]),
 trio(["family", "deluxe", "twin"], "3 beds. 1 room.<br>Zero compromise.", "Family rooms in G-9", "Book Your Stay Now", bg="family"),
 hero("deluxe", "50% 50%", "This Winter", "Weekends are<br>filling up.", "Lock in your December dates.", "bottom", "Book Now"),
 split("twin", "45% 50%", "Twin beds or one big one?", "We've got both.", side="right"),
 cream("lift", "50% 45%", "Peace of mind", "Lift access · CCTV security", [("lift", "Lift Access"), ("cam", "CCTV"), ("shield", "Safe Stays")]),
 hero("family", "50% 55%", "Home for the holidays?", "Make it Velmore.", "", "bottom", None, sparkle=True),
 greeting("Happy Quaid Day", "& Merry Christmas", "25 December · Warm wishes from Velmore Inn"),
 newspaper("deluxe", "50% 50%", "THE VELMORE TIMES", "Breaking: NYE Rooms<br>Almost Gone", "Only a few rooms left for 31 December", "Call or WhatsApp to reserve today", kicker="NYE EDITION", bg="stair"),
 greeting("Happy New Year", "2027 starts with a<br>good night's sleep", "Thank you for a wonderful first season", img="stair"),
]

def main():
    for i, html in enumerate(POSTS, 1):
        (OUT / f"post-{i:02d}.html").write_text(html)
    subprocess.run(["node", str(pathlib.Path(__file__).with_name("render.js")), str(OUT), str(len(POSTS))], check=True)
    for i in range(1, len(POSTS) + 1):
        (OUT / f"post-{i:02d}.html").unlink()
    from PIL import Image
    files = [OUT / f"post-{i:02d}.png" for i in range(1, len(POSTS) + 1)]
    ims = [Image.open(x).convert("RGB") for x in files]
    ims[0].save(OUT / "all-posts.pdf", save_all=True, append_images=ims[1:], resolution=72)
    sheet = Image.new("RGB", (5 * 272 + 8, 4 * 340 + 8), (43, 29, 20))
    for n, im in enumerate(ims):
        sheet.paste(im.resize((260, 325)), (10 + (n % 5) * 272, 10 + (n // 5) * 340))
    sheet.save(OUT / "contact-sheet.jpg", quality=88)

main()
