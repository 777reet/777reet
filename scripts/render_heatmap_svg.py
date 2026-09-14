import json
from pathlib import Path
from datetime import date, timedelta

DATA = Path("data/contributions.json")

D = json.loads(DATA.read_text(encoding="utf-8"))

days = {x["date"]: x for x in D["days"]}

end = date.today()
start = end - timedelta(days=370)

start = start - timedelta(days=(start.weekday() + 1) % 7)

weeks = 53
cell = 11
gap = 3
left = 38
top = 38

W = weeks * (cell + gap) + left + 165
H = 7 * (cell + gap) + top + 46

PALETTE = [
    "#160d12",
    "#2b111c",
    "#421725",
    "#5b2033",
    "#762b43",
    "#963c58",
]

svg = [
    f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{W}"
height="{H}"
viewBox="0 0 {W} {H}">

<rect width="100%" height="100%" rx="16" fill="#080709"/>

<rect
x="1"
y="1"
width="{W-2}"
height="{H-2}"
rx="16"
fill="none"
stroke="#5b2637"/>

<style>
.t {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}}

@keyframes reveal {{
    from {{
        opacity: 0;
        transform: translateY(-7px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.cell {{
    animation: reveal .35s ease both;
}}
</style>

<text
class="t"
x="18"
y="24"
font-size="11"
fill="#9a4b64">
777reet@github ~ $ ./contributions.sh
</text>
'''
]

# month labels
for month in range(13):

    dt = start + timedelta(days=month * 28)

    if dt > end:
        break

    x = left + month * 4 * (cell + gap)

    svg.append(
        f'<text class="t" '
        f'x="{x}" y="{top-12}" '
        f'font-size="9" fill="#80616d">'
        f'{dt.strftime("%b")}</text>'
    )

# weekday labels
for row, label in [
    (1, "Mon"),
    (3, "Wed"),
    (5, "Fri")
]:

    y = top + row * (cell + gap) + 9

    svg.append(
        f'<text class="t" '
        f'x="7" y="{y}" '
        f'font-size="9" fill="#80616d">'
        f'{label}</text>'
    )

# contribution cells
for col in range(weeks):

    for row in range(7):

        dt = start + timedelta(days=col * 7 + row)

        if dt > end:
            continue

        x = left + col * (cell + gap)
        y = top + row * (cell + gap)

        item = days.get(
            dt.isoformat(),
            {"level": 0, "count": 0}
        )

        level = max(
            0,
            min(5, int(item.get("level", 0)))
        )

        delay = (col + row) * 0.012

        svg.append(
            f'''
<rect
class="cell"
x="{x}"
y="{y}"
width="{cell}"
height="{cell}"
rx="3"
fill="{PALETTE[level]}"
style="animation-delay:{delay:.2f}s">

<title>
{item.get("count", 0)} contributions on {dt.isoformat()}
</title>

</rect>
'''
        )

# legend
legend_x = left + weeks * (cell + gap) + 12

svg.append(
    f'''
<text
class="t"
x="{legend_x}"
y="{top+5}"
font-size="9"
fill="#80616d">
Less
</text>
'''
)

for i in range(6):

    svg.append(
        f'''
<rect
x="{legend_x + i * 14}"
y="{top+12}"
width="10"
height="10"
rx="3"
fill="{PALETTE[i]}"/>
'''
    )

svg.append(
    f'''
<text
class="t"
x="{legend_x+88}"
y="{top+21}"
font-size="9"
fill="#80616d">
More
</text>
'''
)

# statistics
sy = top + 53

svg.append(
    f'''
<text
class="t"
x="{legend_x}"
y="{sy}"
font-size="11"
fill="#c6a2ae">
{D["total"]} contributions
</text>

<text
class="t"
x="{legend_x}"
y="{sy+18}"
font-size="9"
fill="#80616d">
last year
</text>

<text
class="t"
x="{legend_x}"
y="{sy+40}"
font-size="9"
fill="#80616d">
current streak:
<tspan fill="#9a4b64">
{D["current_streak"]} days
</tspan>
</text>

<text
class="t"
x="{legend_x}"
y="{sy+58}"
font-size="9"
fill="#80616d">
longest streak:
<tspan fill="#9a4b64">
{D["longest_streak"]} days
</tspan>
</text>
'''
)

svg.append(
    f'''
<text
class="t"
x="18"
y="{H-12}"
font-size="9"
fill="#633044">
less noise · more code ♡
</text>

</svg>
'''
)

Path("contrib-heatmap.svg").write_text(
    "".join(svg),
    encoding="utf-8"
)

print("Rendered burgundy contribution heatmap.")