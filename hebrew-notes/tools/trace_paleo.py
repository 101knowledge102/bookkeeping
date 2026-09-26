# Traces the paleo-Hebrew glyphs from the course handout photos into SVG paths (40x40 box).
# Usage: python3 trace_paleo.py <photo 1-10> <photo 11-22>  -> writes paleo_paths.json next to this file
import sys, json, os
import numpy as np, potrace
from PIL import Image, ImageFilter
S=1932/1500
A=Image.open(sys.argv[1]).convert('L'); B=Image.open(sys.argv[2]).convert('L')
ra=[(210,385),(392,575),(582,765),(772,950),(958,1135),(1142,1315),(1322,1490),(1497,1665),(1672,1835),(1842,2000)]
rb=[(300,445),(448,585),(590,725),(728,860),(862,995),(998,1130),(1133,1260),(1263,1390),(1393,1525),(1528,1655),(1658,1785),(1788,1912)]
boxes=[(A,125+20*i/9,y0,125+20*i/9+230,y1) for i,(y0,y1) in enumerate(ra)]+[(B,45+60*i/11,y0,45+60*i/11+170,y1) for i,(y0,y1) in enumerate(rb)]
letters='אבגדהוזחטיכלמנסעפצקרשת'
out={}
for ch,(im,x0,y0,x1,y1) in zip(letters,boxes):
    c=im.crop(tuple(int(v*S) for v in (x0,y0,x1,y1))).filter(ImageFilter.MedianFilter(3))
    c=c.resize((c.width*2,c.height*2),Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
    bw=np.array(c)<105
    ys,xs=np.nonzero(bw); bw=np.pad(bw[ys.min():ys.max()+1,xs.min():xs.max()+1],4)
    h,w=bw.shape; sc=36/max(h,w); ox=(40-w*sc)/2; oy=(40-h*sc)/2
    tr=potrace.Bitmap(~bw).trace(turdsize=40,alphamax=1.0,opticurve=True,opttolerance=0.3)
    P=lambda p:f'{ox+p.x*sc:.2f},{oy+p.y*sc:.2f}'
    d=''
    for curve in tr:
        d+=f'M{P(curve.start_point)}'
        for seg in curve.segments:
            if seg.is_corner: d+=f'L{P(seg.c)}L{P(seg.end_point)}'
            else: d+=f'C{P(seg.c1)} {P(seg.c2)} {P(seg.end_point)}'
        d+='Z'
    out[ch]=d
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'paleo_paths.json'),'w'),ensure_ascii=False)
print({k:len(v) for k,v in out.items()})
