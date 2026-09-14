from PIL import Image
from pathlib import Path
import math, html

src=Path('data/source-prepped.png')
out=Path('avi-ascii.svg')
img=Image.open(src).convert('L')
# crop a little from empty sides
w,h=img.size
img=img.crop((20,0,w-20,h-10))
cols,rows=86,58
# character cells are wider than tall, so resize to compensate
small=img.resize((cols,rows))
ramp=' .`:-=+*cs#%@'
chars=[]
for y in range(rows):
    line=[]
    for x in range(cols):
        v=small.getpixel((x,y))
        idx=round((255-v)/255*(len(ramp)-1))
        line.append(ramp[idx])
    chars.append(''.join(line))

font=10.5; cw=6.0; lh=11.8
W=cols*cw+36; H=rows*lh+58
parts=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">
<rect width="100%" height="100%" rx="14" fill="#09080a"/>
<rect x="1" y="1" width="{W-2:.0f}" height="{H-2:.0f}" rx="14" fill="none" stroke="#641f32" stroke-width="1"/>
<style>
.ascii{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:{font}px;fill:#9d5268;white-space:pre;}}
@keyframes print{{from{{transform:translateX(-105%);}}to{{transform:translateX(0);}}}}
.row{{animation:print .42s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:left center;}}
</style>
<text x="18" y="28" fill="#a85a70" font-family="ui-monospace,monospace" font-size="12">777reet@github ~ $ whoami</text>
''']
for y,line in enumerate(chars):
    yy=49+y*lh
    delay=y*0.035
    safe=html.escape(line)
    parts.append(f'<text class="ascii row" x="18" y="{yy:.1f}" style="animation-delay:{delay:.2f}s">{safe}</text>')
parts.append(f'<text x="18" y="{H-14:.0f}" fill="#6f3347" font-family="ui-monospace,monospace" font-size="10">&gt; still building... ♡</text></svg>')
out.write_text(''.join(parts),encoding='utf-8')
print(out)
