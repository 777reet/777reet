import json
from pathlib import Path
from datetime import date,timedelta

D=json.loads(Path('data/contributions.json').read_text())
days={x['date']:x for x in D['days']}
end=date.today(); start=end-timedelta(days=370)
start=start-timedelta(days=(start.weekday()+1)%7)
weeks=53; cell=11; gap=3; left=38; top=38
W=weeks*(cell+gap)+left+165; H=7*(cell+gap)+top+46
palette=['#160f13','#34121e','#4a1827','#612033','#7a2940','#9d5268']
svg=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" rx="14" fill="#09080a"/><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="#641f32"/>
<style>.t{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}@keyframes in{{from{{opacity:0;transform:translateY(-8px)}}to{{opacity:1;transform:translateY(0)}}}}.c{{animation:in .35s ease both}}</style>
<text class="t" x="18" y="24" font-size="11" fill="#a85a70">777reet@github ~ $ ./contributions.sh</text>
''']
# month labels
for m in range(13):
    dt=start+timedelta(days=m*28)
    if dt>end: break
    x=left+m*4*(cell+gap)
    svg.append(f'<text class="t" x="{x}" y="{top-12}" font-size="9" fill="#8b6672">{dt.strftime("%b")}</text>')
for r,label in [(1,'Mon'),(3,'Wed'),(5,'Fri')]:
    svg.append(f'<text class="t" x="7" y="{top+r*(cell+gap)+9}" font-size="9" fill="#8b6672">{label}</text>')
for col in range(weeks):
    for row in range(7):
        dt=start+timedelta(days=col*7+row)
        if dt>end: continue
        x=left+col*(cell+gap); y=top+row*(cell+gap)
        item=days.get(dt.isoformat(),{'level':0})
        lvl=max(0,min(5,int(item.get('level',0))))
        delay=(col+row)*0.012
        svg.append(f'<rect class="c" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{palette[lvl]}" style="animation-delay:{delay:.2f}s"><title>{item.get("count",0)} contributions on {dt.isoformat()}</title></rect>')
legend_x=left+weeks*(cell+gap)+12
svg.append(f'<text class="t" x="{legend_x}" y="{top+5}" font-size="9" fill="#8b6672">Less</text>')
for i in range(6): svg.append(f'<rect x="{legend_x+i*14}" y="{top+12}" width="10" height="10" rx="3" fill="{palette[i]}"/>')
svg.append(f'<text class="t" x="{legend_x+88}" y="{top+21}" font-size="9" fill="#8b6672">More</text>')
sy=top+53
svg.append(f'<text class="t" x="{legend_x}" y="{sy}" font-size="11" fill="#c9aab6">{D["total"]} contributions</text>')
svg.append(f'<text class="t" x="{legend_x}" y="{sy+18}" font-size="9" fill="#8b6672">last year</text>')
svg.append(f'<text class="t" x="{legend_x}" y="{sy+40}" font-size="9" fill="#8b6672">current streak: <tspan fill="#a85a70">{D["current_streak"]} days</tspan></text>')
svg.append(f'<text class="t" x="{legend_x}" y="{sy+58}" font-size="9" fill="#8b6672">longest streak: <tspan fill="#a85a70">{D["longest_streak"]} days</tspan></text>')
svg.append(f'<text class="t" x="18" y="{H-12}" font-size="9" fill="#6f3347">less noise · more code ♡</text></svg>')
Path('contrib-heatmap.svg').write_text(''.join(svg),encoding='utf-8')
print('rendered contrib-heatmap.svg')
