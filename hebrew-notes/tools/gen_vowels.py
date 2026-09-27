# Generates hebrew-notes/vowels.html: vector chart of Hebrew vowel points.
ALEF=["M52,44 Q52,62 35,74","M12,44 L56,104","M24,60 Q12,78 12,104"]
VAV="M6,44 H12 Q18,44 18,50 V104"
C=32  # centre of alef
def dot(x,y,r=4.6): return f'<circle cx="{x}" cy="{y}" r="{r}" class="mk"/>'
def bar(cx,y=117,w=20): return f'<rect x="{cx-w/2}" y="{y-2.6}" width="{w}" height="5.2" rx="1.2" class="mk"/>'
def stem(cx,y=117): return f'<rect x="{cx-2.4}" y="{y}" width="4.8" height="10" rx="1" class="mk"/>'
M={
 'patah':lambda c:bar(c),
 'qamets':lambda c:bar(c)+stem(c),
 'segol':lambda c:dot(c-7,116)+dot(c+7,116)+dot(c,128),
 'tsere':lambda c:dot(c-7,119)+dot(c+7,119),
 'hireq':lambda c:dot(c,120),
 'shva':lambda c:dot(c,114)+dot(c,127),
 'qibbuts':lambda c:dot(c-9,113)+dot(c,120)+dot(c+9,127),
}
M['hpatah']=lambda c:bar(c-6)+dot(c+11,114)+dot(c+11,127)
M['hsegol']=lambda c:dot(c-12,116)+dot(c+2,116)+dot(c-5,128)+dot(c+13,114)+dot(c+13,127)
M['hqamets']=lambda c:bar(c-6)+stem(c-6)+dot(c+11,114)+dot(c+11,127)
def alef(x=0):
    return f'<g transform="translate({x},0)">'+''.join(f'<path d="{d}" class="ghost"/>' for d in ALEF)+'</g>'
def svg(kind):
    if kind in ('holemvav','shureq'):
        # RTL: alef on the right, vav to its left
        ax=38
        s=alef(ax)+f'<path d="{VAV}" class="vav"/>'
        s+=dot(8,30) if kind=='holemvav' else dot(-4,74)
        return f'<svg viewBox="-16 20 134 118" class="v" aria-hidden="true">{s}</svg>'
    s=alef()
    s+=dot(4,30) if kind=='holem' else M[kind](C)
    return f'<svg viewBox="-14 20 92 118" class="v" aria-hidden="true">{s}</svg>'
def cell(kind,name,sound,cls,span=1):
    sp=f' colspan="{span}"' if span>1 else ''
    return f'<td{sp}><div class="c">{svg(kind)}<div class="n">{name}</div><div class="s {cls}">{sound}</div></div></td>'
E='<td class="empty"></td>'
rows=[
 ('a','ra',[cell('hpatah','Hateph Patah','a','ca'),cell('patah','Patah','a','ca'),cell('qamets','Qamets','a','ca'),E]),
 ('e','re',[cell('hsegol','Hateph Segol','e','ce'),cell('segol','Segol','e','ce'),cell('tsere','Tsere','e','ce'),E]),
 ('i','ri',[E,cell('hireq','Hireq','i','ci'),E,E]),
 ('o','ro',[cell('hqamets','Hateph Qamets','o','co'),cell('qamets','Qamets Hatuf','o','co'),cell('holem','Holem','o','co'),cell('holemvav','Holem Vav','o','co')]),
 ('u','ru',[E,cell('qibbuts','Qibbuts','u','cu'),E,cell('shureq','Shureq','u','cu')]),
 ('轻音<br><small>（静音）</small>','rs',[cell('shva','有声 Shva','轻读 ə','cs'),cell('shva','无声 Shva','不发音','cs',3)]),
]
trs=''.join(f'<tr><th class="rh {c}">{h}</th>{"".join(cs)}</tr>' for h,c,cs in rows)
strip=[('qibbuts','呜','u','cu'),('shureq','呜','u','cu'),('hireq','咿','i','ci'),('holemvav','哦','o','co'),('shva','轻','e/ə','cs'),
       ('segol','唉','e','ce'),('tsere','唉','e','ce'),('patah','啊','a','ca'),('qamets','啊','a','ca')]
tiles=''.join(f'<figure class="t">{svg(k)}<figcaption><span class="zh {c}">{z}</span><span class="lat {c}">{l}</span></figcaption></figure>' for k,z,l,c in strip)
html=f'''<title>希伯来元音符号</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@600&display=swap">
<style>
.he{{font-family:"Noto Serif Hebrew","SBL Hebrew","Times New Roman",serif;font-size:1.2em}}
:root{{--bg:#f3f5f9;--card:#ffffff;--ink:#1a2030;--muted:#5b647a;--line:#dde2ec;--head:#3d6fb6;--headink:#ffffff;--rowh:#f2c14e;--rowhink:#3b3220;
--cell:#eef2f9;--cell2:#e4eaf5;--ghost:#c9ced8;--mark:#d8342b;--vav:#2a63d6;
--a:#c9861a;--e:#2a63d6;--i:#c2185b;--o:#c9861a;--u:#1d9bb5;--s:#8a3fc9;
--ui:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Noto Sans SC","Segoe UI",sans-serif}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{color-scheme:dark;--bg:#10131a;--card:#191e29;--ink:#e7eaf2;--muted:#9aa3b8;--line:#2a3142;--head:#2f4f86;--headink:#e7eaf2;--rowh:#8a6a1c;--rowhink:#fff4d6;
--cell:#1c2230;--cell2:#212839;--ghost:#3d4558;--mark:#ff6b5f;--vav:#7da2ff;--a:#f0b44a;--e:#7da2ff;--i:#ff7aa8;--o:#f0b44a;--u:#5fd0e6;--s:#c49bff}}}}
:root[data-theme="dark"]{{color-scheme:dark;--bg:#10131a;--card:#191e29;--ink:#e7eaf2;--muted:#9aa3b8;--line:#2a3142;--head:#2f4f86;--headink:#e7eaf2;--rowh:#8a6a1c;--rowhink:#fff4d6;
--cell:#1c2230;--cell2:#212839;--ghost:#3d4558;--mark:#ff6b5f;--vav:#7da2ff;--a:#f0b44a;--e:#7da2ff;--i:#ff7aa8;--o:#f0b44a;--u:#5fd0e6;--s:#c49bff}}
body{{background:var(--bg);color:var(--ink);font-family:var(--ui);line-height:1.55}}
.wrap{{max-width:980px;margin:0 auto;padding-inline:16px;padding-block:28px 48px;display:grid;gap:20px}}
h1{{margin:0;font-size:26px;text-wrap:balance}} h2{{margin:0;font-size:19px}}
p{{margin:0;color:var(--muted);max-width:66ch}}
section{{display:grid;gap:12px}}
.scroll{{overflow-x:auto;border-radius:10px;border:1px solid var(--line);background:var(--card)}}
table{{border-collapse:separate;border-spacing:3px;width:100%;min-width:600px}}
thead th{{background:var(--head);color:var(--headink);font-size:20px;padding:10px 6px;border-radius:4px;letter-spacing:.1em}}
thead th.corner{{font-size:14px;letter-spacing:.04em}}
.rh{{background:var(--rowh);color:var(--rowhink);font-size:30px;font-weight:700;width:84px;border-radius:4px;line-height:1.1}}
.rh small{{font-size:13px;font-weight:600}}
.rs{{font-size:18px}}
td{{background:var(--cell);border-radius:4px;padding:6px 4px;vertical-align:top}}
tbody tr:nth-child(even) td{{background:var(--cell2)}}
td.empty{{background:transparent!important}}
.c{{display:grid;justify-items:center;gap:0}}
.v{{height:96px;width:auto;max-width:100%;display:block}}
.ghost{{fill:none;stroke:var(--ghost);stroke-width:8;stroke-linecap:round;stroke-linejoin:round}}
.vav{{fill:none;stroke:var(--vav);stroke-width:8;stroke-linecap:round;stroke-linejoin:round}}
.mk{{fill:var(--mark)}}
.n{{font-size:12.5px;color:var(--muted);text-align:center}}
.s{{font-size:16px;font-weight:700}}
.ca{{color:var(--a)}} .ce{{color:var(--e)}} .ci{{color:var(--i)}} .co{{color:var(--o)}} .cu{{color:var(--u)}} .cs{{color:var(--s)}}
.strip{{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:8px}}
.t{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 6px;display:grid;justify-items:center;gap:2px}}
.t .v{{height:88px}}
.t figcaption{{display:flex;gap:6px;align-items:baseline}}
.zh{{font-size:14px}} .lat{{font-size:22px;font-weight:700}}
ul{{margin:0;padding-inline-start:20px;display:grid;gap:4px;color:var(--muted);max-width:70ch}}
</style>
<div class="wrap">
<header style="display:grid;gap:6px"><h1>希伯来元音符号</h1>
<p>元音符号写在辅音字母的下面、上面或左边。这里用浅灰色的 <span class="he">א</span> 代替任意辅音，红色是元音符号，蓝色的 <span class="he">ו</span> 是元音的一部分。</p></header>

<section><h2>一、元音总表</h2>
<div class="scroll"><table>
<thead><tr><th class="corner">元音总类</th><th>轻</th><th>短</th><th>长</th><th>长（加 <span class="he">ו</span>）</th></tr></thead>
<tbody>{trs}</tbody></table></div>
<ul>
<li><b>轻</b>元音（Hateph）是在短元音旁边加上 Shva 的两点，读得又短又轻。</li>
<li><b>Qamets</b>（长 a）和 <b>Qamets Hatuf</b>（短 o）是同一个符号，要看音节判断读法。</li>
<li><b>Holem</b> 的点写在字母左上方的上点线上；加 <span class="he">ו</span> 时写成 <b class="he">וֹ</b>。<b>Shureq</b> 是 <span class="he">ו</span> 左边中间加一点，写成 <b class="he">וּ</b>。</li>
<li><b>Shva</b> 两点在有的位置轻读 ə（有声），有的位置不发音（无声）。</li>
</ul>
</section>

<section><h2>二、读音对照</h2>
<div class="strip">{tiles}</div>
</section>
</div>
'''
import os
out=os.path.join(os.path.dirname(__file__),'..','vowels.html')
open(out,'w').write(html); print(len(html))
