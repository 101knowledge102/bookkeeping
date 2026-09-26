# Generates hebrew-notes/hands.html: letters and paleo-Hebrew glyphs on two pairs of hands.
import os
W=240  # hand group width
# finger centre x, finger top y (hand with thumb on the right, i.e. the viewer's right hand of the pair)
F={'index':(150,62),'middle':(110,30),'ring':(70,48),'pinky':(30,92)}
def hand_shapes():
    s=''
    for x,t in F.values(): s+=f'<rect x="{x-18}" y="{t}" width="36" height="{230-t}" rx="18"/>'
    s+='<rect x="12" y="150" width="170" height="180" rx="60"/>'
    s+='<rect x="-20" y="-78" width="40" height="156" rx="20" transform="translate(192,226) rotate(38)"/>'
    return s
def hand(x0,mirror):
    tr=f'translate({x0+W},0) scale(-1,1)' if mirror else f'translate({x0},0)'
    shapes=hand_shapes()
    lines='<path d="M50,104 V196 M90,64 V196 M130,64 V196"/>'
    return (f'<g transform="{tr}"><g class="ho">{shapes}</g><g class="hf">{shapes}</g><g class="hl">{lines}</g></g>')
# positions (x,y) in the unmirrored hand; key -> slot
SLOT={'thumb':(226,182),'i1':(150,92),'i2':(150,136),'i3':(150,176),'m1':(110,62),'m2':(110,104),'m3':(110,146),
      'r1':(70,80),'r2':(70,122),'r3':(70,164),'p1':(30,124),'p2':(30,166),'base':(160,252),'base2':(160,292),'palm':(84,262)}
RIGHT={'thumb':'א','i1':'ב','m1':'ג','r1':'ד','p1':'ה','base':'כ','base2':'ך','i2':'ל','m2':'מ','m3':'ם','r2':'נ','r3':'ן','p2':'ס','palm':'ע'}
LEFT ={'p1':'ו','r1':'ז','m1':'ח','i1':'ט','thumb':'י','p2':'פ','p3':'ף','r2':'צ','r3':'ץ','m2':'ק','i2':'ר','base':'ש','palm':'ת'}
SLOT['p3']=(30,206)
FINALS='ךםןףץ'
# paleo-Hebrew glyphs drawn in a 40x40 box
P={
'א':'<ellipse cx="20" cy="26" rx="9" ry="8"/><path d="M12,21 Q4,10 11,3 M28,21 Q36,10 29,3"/>',
'ב':'<path d="M31,26 V10 H8 V32 H33"/>',
'ג':'<path d="M11,5 V33 H31"/>',
'ד':'<path d="M11,3 V37 M11,9 H29 V31 H11"/>',
'ה':'<path d="M20,6 V32 Q20,38 27,36 M7,7 Q7,19 20,19 Q33,19 33,7"/>',
'ו':'<path d="M20,15 V37 M20,15 L10,5 M20,15 L29,6"/>',
'ז':'<path d="M8,5 H32 L8,35 H32 Z"/>',
'ח':'<path d="M9,4 H31 V36 H9 Z M9,20 H31"/>',
'ט':'<circle cx="20" cy="20" r="14"/><path d="M11,11 L29,29 M29,11 L11,29"/>',
'י':'<path d="M3,22 Q9,17 14,24 H35 V12"/>',
'כ':'<path d="M8,6 V24 Q8,35 20,35 Q32,35 32,24 V6 M16,5 V27 M24,5 V27"/>',
'ל':'<path d="M27,5 L14,30 Q12,37 19,34"/>',
'מ':'<path d="M2,25 L8,15 L14,25 L20,15 L26,25 L32,15 L38,25"/>',
'נ':'<path d="M3,9 Q10,5 14,13 Q20,27 28,22 Q34,19 37,33"/>',
'ס':'<path d="M20,4 V36 M8,10 H32 M10,18 H30 M12,26 H28"/>',
'ע':'<ellipse cx="20" cy="20" rx="17" ry="8.5"/><circle cx="20" cy="20" r="3.8" class="fill"/>',
'פ':'<path d="M2,20 Q20,8 38,20 Q20,32 2,20 Z"/>',
'צ':'<path d="M7,11 V23 H26 L19,33 H35"/>',
'ק':'<circle cx="20" cy="13" r="8"/><path d="M20,21 V38 M10,13 H30"/>',
'ר':'<path d="M29,35 V17 Q29,5 18,5 Q8,5 8,15 Q8,24 17,24 H29"/>',
'ש':'<path d="M4,11 Q5,30 13,29 Q20,28 20,15 Q20,28 27,29 Q35,30 36,11"/>',
'ת':'<path d="M20,4 V36 M5,18 H35"/>',
}
def put_letters(x0,mirror,mapping,paleo):
    out=''
    for k,ch in mapping.items():
        x,y=SLOT[k]
        if mirror: x=W-x
        X=x0+x
        big=k=='palm'
        if paleo:
            if ch in FINALS: continue
            sc=1.25 if big else 0.8
            out+=f'<g class="pg" transform="translate({X},{y}) scale({sc}) translate(-20,-20)">{P[ch]}</g>'
        else:
            cls='fin' if ch in FINALS else 'lt'
            fs=52 if big else 30
            out+=f'<text x="{X}" y="{y+fs*0.36}" class="{cls}" font-size="{fs}">{ch}</text>'
    return out
def pair(paleo):
    L=hand(20,True)+put_letters(20,True,LEFT,paleo)
    R=hand(380,False)+put_letters(380,False,RIGHT,paleo)
    if paleo:
        mid=(f'<g class="pg" transform="translate(300,300) scale(0.95) translate(-20,-20)">{P["פ"]}</g>'
             f'<g class="pg" transform="translate(342,300) scale(0.95) translate(-20,-20)">{P["כ"]}</g>')
    else:
        mid=('<text x="300" y="296" class="lt" font-size="30">פ</text><text x="300" y="336" class="fin" font-size="30">ף</text>'
             '<text x="342" y="296" class="lt" font-size="30">כ</text><text x="342" y="336" class="fin" font-size="30">ך</text>')
    return f'<svg viewBox="0 0 640 350" class="hands" role="img" aria-label="{"古体" if paleo else "字母"}手掌图">{L}{R}<g class="mid">{mid}</g></svg>'
html=f'''<title>看图识字母和古体</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Hebrew:wght@500&family=Noto+Serif+Hebrew:wght@600&display=swap">
<style>
:root{{--bg:#f3f5f9;--card:#ffffff;--ink:#1a2030;--muted:#5b647a;--line:#dde2ec;--fin:#8a93a6;--accent:#2a4aa8;--hl:#c0392b;--midbg:#fff4d6;
--ui:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Noto Sans SC","Segoe UI",sans-serif;
--heb:"Noto Sans Hebrew","Arial Hebrew","Segoe UI",sans-serif;--hebs:"Noto Serif Hebrew","SBL Hebrew",serif}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{color-scheme:dark;--bg:#10131a;--card:#191e29;--ink:#e7eaf2;--muted:#9aa3b8;--line:#2a3142;--fin:#6e7890;--accent:#93aaff;--hl:#ff8f80;--midbg:#3a3220}}}}
:root[data-theme="dark"]{{color-scheme:dark;--bg:#10131a;--card:#191e29;--ink:#e7eaf2;--muted:#9aa3b8;--line:#2a3142;--fin:#6e7890;--accent:#93aaff;--hl:#ff8f80;--midbg:#3a3220}}
body{{background:var(--bg);color:var(--ink);font-family:var(--ui);line-height:1.65}}
.wrap{{max-width:820px;margin:0 auto;padding-inline:16px;padding-block:28px 48px;display:grid;gap:18px}}
h1{{margin:0;font-size:26px}}
p{{margin:0;color:var(--muted);max-width:64ch}}
.panel{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}}
.hands{{width:100%;height:auto;display:block}}
.ho rect{{fill:var(--ink);stroke:var(--ink);stroke-width:9}}
.hf rect{{fill:var(--card)}}
.hl path{{fill:none;stroke:var(--ink);stroke-width:4.5;stroke-linecap:round}}
.lt{{fill:var(--ink);font-family:var(--heb);text-anchor:middle;font-weight:500}}
.fin{{fill:var(--fin);font-family:var(--heb);text-anchor:middle;font-weight:500}}
.pg{{fill:none;stroke:var(--ink);stroke-width:3.4;stroke-linecap:round;stroke-linejoin:round}}
.pg .fill{{fill:var(--ink);stroke:none}}
.verse{{font-size:17px;font-weight:600;line-height:1.8}}
.verse .he{{font-family:var(--hebs);color:var(--hl);font-size:1.15em}}
.notes{{display:grid;gap:8px}}
.note{{background:var(--midbg);border-radius:8px;padding:10px 12px;font-size:15px}}
.note .he{{font-family:var(--heb);font-size:1.25em}}
.label{{font-size:13px;color:var(--muted);letter-spacing:.06em;margin:0 0 4px 4px}}
</style>
<div class="wrap">
<header style="display:grid;gap:6px"><h1>看图识字母和古体</h1>
<p>从右手拇指开始，从右往左数：十个指尖是第 1–10 个字母（א 到 י），第二排和掌心是第 11–22 个字母（כ 到 ת）。灰色是词尾形式。</p></header>

<div class="panel"><p class="label">字母</p>{pair(False)}</div>

<p class="verse">【创 18:14】耶和华岂有难成的事吗？到了所定的日期<span class="he" lang="he">מוֹעֵד</span>，明年这时候<span class="he" lang="he">עֵת</span>，我必回到你这里，撒拉必生一个儿子。”</p>

<div class="panel"><p class="label">古体</p>{pair(True)}</div>

<div class="notes">
<div class="note"><b>小注 1：</b>古体没有词尾形式。古体的“掌”同时对应 <span class="he">כ</span> 和 <span class="he">ך</span>，古体的“口”同时对应 <span class="he">פ</span> 和 <span class="he">ף</span>。</div>
<div class="note"><b>小注 2：</b>两个字母合起来是 <span class="he" lang="he">כַּף</span>，意思是“手掌”。</div>
</div>
</div>
'''
open(os.path.join(os.path.dirname(__file__),'..','hands.html'),'w').write(html)
print(len(html))
