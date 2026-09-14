from pathlib import Path

out=Path('info-card.svg')
W,H=760,430
rows=[
('currently','BSc IT Student'),
('stack','Python  ·  Java  ·  JavaScript  ·  PHP  ·  MySQL'),
('full stack','React  ·  Node.js  ·  Next.js  ·  REST APIs'),
('ai / ml','Machine Learning  ·  LLMs  ·  LangChain  ·  OpenAI'),
('dsa','Problem solving  ·  Data Structures & Algorithms'),
('learning','System Design  ·  ML  ·  Scalable Applications'),
('projects','Cancer Cell Prediction  ·  ERP System  ·  More...'),
]
svg=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" rx="16" fill="#09080a"/>
<rect x="1" y="1" width="758" height="428" rx="16" fill="none" stroke="#641f32"/>
<style>
.t{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;}}
.fade{{animation:fade .55s ease both;}}
@keyframes fade{{from{{opacity:0;transform:translateY(7px)}}to{{opacity:1;transform:translateY(0)}}}}
</style>
<circle cx="22" cy="23" r="6" fill="#9d5268"/><circle cx="42" cy="23" r="6" fill="#733247"/><circle cx="62" cy="23" r="6" fill="#4d2433"/>
<text class="t" x="84" y="28" font-size="13" fill="#a85a70">reet.exe</text>
<line x1="22" y1="48" x2="738" y2="48" stroke="#4f1d2d"/>
<text class="t fade" x="28" y="91" font-size="32" font-weight="700" fill="#d5a1b1" style="animation-delay:.05s">&gt; reet ♡</text>
<text class="t fade" x="28" y="120" font-size="14" fill="#b9899b" style="animation-delay:.10s">Software Developer   |   Full Stack   |   AI Engineer</text>
<line x1="28" y1="141" x2="732" y2="141" stroke="#641f32"/>
''']
for i,(k,v) in enumerate(rows):
    y=174+i*34
    delay=.16+i*.055
    svg.append(f'<text class="t fade" x="28" y="{y}" font-size="12" fill="#a85a70" style="animation-delay:{delay:.2f}s">{k.upper():<11}</text>')
    svg.append(f'<text class="t fade" x="150" y="{y}" font-size="12" fill="#c9aab6" style="animation-delay:{delay:.2f}s">:  {v}</text>')
svg.append('''<line x1="28" y1="410" x2="732" y2="410" stroke="#641f32"/>
<text class="t" x="28" y="426" font-size="10" fill="#6f3347">build · learn · create · repeat   ♡</text>
<text class="t" x="704" y="426" font-size="12" fill="#6f3347">◢</text>
</svg>''')
out.write_text(''.join(svg),encoding='utf-8')
print(out)
