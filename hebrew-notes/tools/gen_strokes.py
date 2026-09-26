import re
# y: 上外线 8, 上点线 28, 上基线 44, 下基线 104, 下点线 120, 下外线 140
LINES=[(8,"上外线","o"),(28,"上点线","d"),(44,"上基线","b"),(104,"下基线","b"),(120,"下点线","d"),(140,"下外线","o")]
G={ # ch: (width, [strokes], extras)
'א':(64,["M52,44 Q54,62 40,72","M10,44 L56,104","M26,70 Q14,82 10,104"]),
'ב':(62,["M8,44 H42 Q50,44 50,52 V104","M58,104 H6"]),
'ג':(44,["M10,44 H22 Q32,44 32,56 V104","M32,80 L10,104"]),
'ד':(58,["M4,44 H52","M44,44 V104"]),
'ה':(58,["M6,44 H42 Q50,44 50,52 V104","M12,68 V104"]),
'ו':(26,["M6,44 H12 Q18,44 18,50 V104"]),
'ז':(38,["M6,44 L32,50","M19,48 V104"]),
'ח':(58,["M8,44 H42 Q50,44 50,52 V104","M8,50 V104"]),
'ט':(60,["M10,46 V86 Q10,104 30,104 Q50,104 50,84 V62 Q50,48 38,48 Q28,48 26,58"]),
'י':(24,["M6,44 H10 Q16,44 16,50 V72"]),
'כ':(54,["M6,44 H32 Q48,44 48,60 V88 Q48,104 32,104 H6"]),
'ל':(54,["M8,8 V58 H40 Q46,58 46,64 V74 Q46,92 26,104"]),
'מ':(62,["M6,44 L16,54 Q24,44 36,44 Q54,44 54,62 V104 H30","M14,104 L22,62"]),
'נ':(38,["M6,44 H16 Q24,44 24,52 V104 H4"]),
'ס':(60,["M6,44 H38 Q52,44 52,58 V90 Q52,104 38,104 H22 Q8,104 8,90 V46"]),
'ע':(58,["M50,44 Q50,90 10,104","M8,44 L32,84"]),
'פ':(58,["M6,44 H36 Q52,44 52,60 V88 Q52,104 36,104 H6","M16,50 Q22,50 22,58 V72"]),
'צ':(56,["M48,44 Q48,66 32,76","M8,44 L42,98 Q44,104 36,104 H6"]),
'ק':(58,["M6,44 H40 Q50,44 50,54 V72 Q50,90 34,104","M10,66 V140"]),
'ר':(52,["M6,44 H34 Q44,44 44,54 V104"]),
'ש':(68,["M58,44 V80 Q58,104 34,104 Q12,104 10,86 L8,46|L","M33,46 V68 Q33,82 16,86","DOT:64,26"]),
'ת':(60,["M4,44 H40 Q50,44 50,54 V104","M16,50 V96 Q16,104 6,104"]),
'ך':(50,["M6,44 H30 Q40,44 40,54 V140"]),
'ם':(60,["M8,44 H44 Q52,44 52,52 V104 H8 V50"]),
'ן':(28,["M6,44 H12 Q18,44 18,50 V140"]),
'ף':(56,["M6,44 H34 Q46,44 46,56 V140","M14,50 Q20,50 20,58 V72"]),
'ץ':(56,["M48,44 Q48,62 30,72","M8,44 L24,72 V140"]),
}
def start(d):
    m=re.match(r"M([\d.]+),([\d.]+)",d); return float(m.group(1)),float(m.group(2))
def staff(x0,x1,labels=False):
    s=f'<rect x="{x0}" y="44" width="{x1-x0}" height="60" class="band"/>'
    for y,n,k in LINES:
        s+=f'<line x1="{x0}" x2="{x1}" y1="{y}" y2="{y}" class="l{k}"/>'
    return s
def letter_svg(ch):
    w,strokes=G[ch]; pad=22; W=w+2*pad
    s=f'<svg viewBox="0 0 {W} 150" class="lsvg" role="img" aria-label="{ch} 的笔顺">'+staff(0,W)
    s+=f'<g transform="translate({pad},0)">'
    marks=''
    for i,d in enumerate(strokes,1):
        if d.startswith("DOT:"):
            x,y=map(float,d[4:].split(",")); s+=f'<circle cx="{x}" cy="{y}" r="5" class="s{i} f"/>'
            marks+=f'<g class="num"><circle cx="{x+13}" cy="{y-2}" r="7" class="b{i}"/><text x="{x+13}" y="{y+1.5}">{i}</text></g>'
            continue
        left=d.endswith("|L"); d=d.replace("|L","")
        s+=f'<path d="{d}" class="st s{i}" marker-end="url(#a{i})"/>'
        x,y=start(d)
        if y<=46 and y>=20 and not left: y-=12
        else: x-=12
        marks+=f'<g class="num"><circle cx="{x}" cy="{y}" r="7" class="b{i}"/><text x="{x}" y="{y+3.5}">{i}</text></g>'
    s+=marks+'</g></svg>'
    return s
def word_svg(items,gap=6):
    # items: list of (ch, vowels) in reading order (RTL)
    widths=[G[c][0] for c,_ in items]; total=sum(widths)+gap*(len(items)-1)
    return widths,total
def ink_letter(ch,x):
    w,strokes=G[ch]; out=f'<g transform="translate({x},0)">'
    for d in strokes:
        if d.startswith("DOT:"):
            a,b=map(float,d[4:].split(",")); out+=f'<circle cx="{a}" cy="{b}" r="5" class="inkf"/>'
        else: out+=f'<path d="{d.replace("|L","")}" class="ink"/>'
    return out+'</g>'
def qamets(cx): return f'<path d="M{cx-8},116 H{cx+8} M{cx},116 V128" class="inkv"/>'
def example():
    # שָׁלוֹם לָךְ ; draw right to left
    labw=70; x=640-labw  # right edge before labels
    s=f'<svg viewBox="0 0 720 150" class="ex" role="img" aria-label="שָׁלוֹם לָךְ 写在六线格上">'+staff(0,640)
    for y,n,k in LINES: s+=f'<text x="652" y="{y+4}" class="lab">{n}</text>'
    x=620
    def put(ch,extra=None):
        nonlocal x,s
        w=G[ch][0]; x-=w; s+=ink_letter(ch,x)
        if extra: s+=extra(x,w)
        x-=6
    put('ש',lambda x,w:qamets(x+w/2-4))
    put('ל'); put('ו',lambda x,w:f'<circle cx="{x+14}" cy="28" r="5" class="inkf"/>'); put('ם')
    x-=34
    put('ל',lambda x,w:qamets(x+w/2))
    put('ך',lambda x,w:f'<circle cx="{x+18}" cy="66" r="4.5" class="inkf"/><circle cx="{x+18}" cy="82" r="4.5" class="inkf"/>')
    return s+'</svg>'
NAMES=[("א","Alef"),("ב","Bet"),("ג","Gimel"),("ד","Dalet"),("ה","He"),("ו","Vav"),("ז","Zayin"),("ח","Chet"),("ט","Tet"),("י","Yod"),
("כ","Kap","ך"),("ל","Lamed"),("מ","Mem","ם"),("נ","Nun","ן"),("ס","Samek"),("ע","Ayin"),("פ","Pey","ף"),("צ","Tsadik","ץ"),("ק","Qop"),("ר","Resh"),("ש","Shin"),("ת","Tav")]
def zone(ch):
    if ch=="ל": return ("上外线 → 下基线","up")
    if ch in "קךןףץ": return ("上基线 → 下外线","down")
    if ch=="י": return ("只占上半格","")
    return ("上基线 → 下基线","")
def fig(ch,cap):
    z,c=zone(ch); n=len(G[ch][1])
    return f'<figure class="stk">{letter_svg(ch)}<figcaption><span class="he" lang="he">{ch}</span>{f"<span class=cap>{cap}</span>" if cap else ""}<span class="cnt">{n} 笔</span><span class="zone {c}">{z}</span></figcaption></figure>'
cards=''
for i,r in enumerate(NAMES):
    inner=fig(r[0],"一般形式" if len(r)>2 else "")
    if len(r)>2: inner+=fig(r[2],"词尾形式")
    cards+=f'<article class="card{" wide" if len(r)>2 else ""}"><header><span class="ord">{i+1}</span><span class="nm">{r[1]}</span></header><div class="figs">{inner}</div></article>'
defs='<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'+''.join(f'<marker id="a{i}" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="2.3" markerHeight="2.3" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="m{i}"/></marker>' for i in (1,2,3))+'</defs></svg>'
html=f'''<title>希伯来字母笔顺</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@600&display=swap">
<style>
:root{{--bg:#f3f5f9;--card:#ffffff;--ink:#1a2030;--muted:#5b647a;--line:#dde2ec;--chip:#eaeef7;--accent:#2a4aa8;--up:#1f7a55;--down:#a8372b;
--band:#eef3fc;--rule:#b9c3d6;--base:#7d8aa5;--c1:#2a55c9;--c2:#e0662b;--c3:#1f8a5b;
--ui:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Noto Sans SC","Segoe UI",sans-serif;--heb:"Noto Serif Hebrew","SBL Hebrew","Times New Roman",serif}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{color-scheme:dark;--bg:#10131a;--card:#191e29;--ink:#e7eaf2;--muted:#9aa3b8;--line:#2a3142;--chip:#232a3a;--accent:#93aaff;--up:#6fd3a5;--down:#ff8f80;--band:#1d2436;--rule:#3a4560;--base:#7384a8;--c1:#7d9cff;--c2:#ff9a5e;--c3:#5fd49b}}}}
:root[data-theme="dark"]{{color-scheme:dark;--bg:#10131a;--card:#191e29;--ink:#e7eaf2;--muted:#9aa3b8;--line:#2a3142;--chip:#232a3a;--accent:#93aaff;--up:#6fd3a5;--down:#ff8f80;--band:#1d2436;--rule:#3a4560;--base:#7384a8;--c1:#7d9cff;--c2:#ff9a5e;--c3:#5fd49b}}
body{{background:var(--bg);color:var(--ink);font-family:var(--ui);line-height:1.6}}
.wrap{{max-width:1080px;margin:0 auto;padding-inline:16px;padding-block:28px 48px;display:grid;gap:22px}}
h1{{margin:0;font-size:26px}} h2{{margin:0;font-size:19px}}
p{{margin:0;color:var(--muted);max-width:64ch}}
section{{display:grid;gap:12px}}
.panel{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}}
.scroll{{overflow-x:auto}}
.band{{fill:var(--band)}}
line.lo{{stroke:var(--rule);stroke-width:1}} line.ld{{stroke:var(--rule);stroke-width:1;stroke-dasharray:4 4}} line.lb{{stroke:var(--base);stroke-width:1.4}}
.lab{{fill:var(--ink);font:700 12px var(--ui)}}
.ink{{fill:none;stroke:var(--ink);stroke-width:7;stroke-linecap:round;stroke-linejoin:round}}
.inkv{{fill:none;stroke:var(--ink);stroke-width:4.5;stroke-linecap:round}} .inkf{{fill:var(--ink)}}
.st{{fill:none;stroke-width:7;stroke-linecap:round;stroke-linejoin:round}}
.s1{{stroke:var(--c1)}} .s2{{stroke:var(--c2)}} .s3{{stroke:var(--c3)}}
.f.s1{{fill:var(--c1);stroke:none}} .f.s2{{fill:var(--c2);stroke:none}} .f.s3{{fill:var(--c3);stroke:none}}
.m1{{fill:var(--c1)}} .m2{{fill:var(--c2)}} .m3{{fill:var(--c3)}}
.b1{{fill:var(--c1)}} .b2{{fill:var(--c2)}} .b3{{fill:var(--c3)}}
.num circle{{stroke:var(--card);stroke-width:1.5}}
.num text{{fill:#fff;font:700 9.5px var(--ui);text-anchor:middle}}
.ex{{width:100%;min-width:560px;display:block}}
table{{border-collapse:collapse;width:100%}}
th,td{{text-align:left;padding:8px 10px;border-top:1px solid var(--line);vertical-align:top}}
th{{white-space:nowrap}} thead th{{border-top:0;color:var(--muted);font-size:13px}}
.he{{font-family:var(--heb);font-size:1.3em;color:var(--accent)}}
.legend{{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:13.5px;color:var(--muted);align-items:center}}
.dotc{{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;color:#fff;font-size:11px;font-weight:700;margin-right:4px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px;display:grid;gap:8px;align-content:start}}
.card.wide{{grid-column:span 2}}
@media (max-width:440px){{.card.wide{{grid-column:span 1}}}}
.card header{{display:flex;gap:8px;align-items:baseline}}
.ord{{font-weight:700;font-variant-numeric:tabular-nums;min-width:1.6em}} .nm{{color:var(--muted);font-size:14px}}
.figs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}}
.stk{{margin:0;display:grid;gap:6px}}
.lsvg{{width:100%;height:auto;max-height:190px;display:block}}
.stk figcaption{{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;font-size:12.5px}}
.stk .he{{font-size:24px;line-height:1}}
.cap,.cnt{{color:var(--muted)}}
.zone{{background:var(--chip);border-radius:5px;padding:1px 7px;font-size:12px}}
.zone.up{{color:var(--up);font-weight:700}} .zone.down{{color:var(--down);font-weight:700}}
@media print{{.card{{break-inside:avoid}}}}
</style>
{defs}
<div class="wrap">
<header style="display:grid;gap:6px"><h1>希伯来字母笔顺</h1>
<p>按照讲义的六线格，整理 22 个字母（含 5 个词尾形式）的手写印刷体笔顺。每一笔用不同颜色，圆圈里的数字是第几笔，也是下笔的位置，箭头是写的方向。</p></header>

<section><h2>一、六条书写线</h2>
<div class="panel scroll">{example()}</div>
<p>例子：<span class="he" lang="he">שָׁלוֹם לָךְ</span>（愿你平安）。שׁ 的点和 וֹ 的点在上点线；Qamets 在下点线；ל 向上到上外线；词尾 ך 向下到下外线，里面写 Shva 的两点。</p>
<div class="panel scroll"><table>
<thead><tr><th>线</th><th>写什么</th></tr></thead><tbody>
<tr><th>上外线</th><td>最高的线。只有 <span class="he">ל</span>（Lamed）的竖笔向上伸到这里。</td></tr>
<tr><th>上点线</th><td>字母上方的点写在这里，例如 <span class="he">שׁ</span> 的点、Holem 点 <span class="he">וֹ</span>。</td></tr>
<tr><th>上基线</th><td>大部分字母的顶部。</td></tr>
<tr><th>下基线</th><td>大部分字母的底部。字母主体写在上基线和下基线之间（浅色区域）。</td></tr>
<tr><th>下点线</th><td>字母下方的元音写在这里，例如 Qamets <span class="he">בָ</span>、Tsere <span class="he">בֵ</span>、Shva <span class="he">בְ</span>（以 ב 为例）。</td></tr>
<tr><th>下外线</th><td>最低的线。<span class="he">ק ך ן ף ץ</span> 的竖笔向下伸到这里。</td></tr>
</tbody></table></div>
</section>

<section><h2>二、22 个字母的笔顺</h2>
<div class="legend"><span><span class="dotc" style="background:var(--c1)">1</span>第一笔</span><span><span class="dotc" style="background:var(--c2)">2</span>第二笔</span><span><span class="dotc" style="background:var(--c3)">3</span>第三笔</span>
<span>标签：<b style="color:var(--up)">绿色</b>＝向上伸出，<b style="color:var(--down)">红色</b>＝向下伸出</span></div>
<div class="grid">{cards}</div>
<p>笔顺依据课程讲义整理。横笔一般从左往右写，竖笔从上往下写。</p>
</section>
</div>
'''
open('/home/user/bookkeeping/hebrew-notes/alphabet-strokes.html','w').write(html)
print(len(html))
