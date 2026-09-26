"""Draw the existing rotor layouts to explain their footprint; no flight claims."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
c = json.loads((ROOT / 'config/system_design.json').read_text())
r = json.loads((ROOT / 'design/system/output/system_design.json').read_text())['results']
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="820" viewBox="0 0 920 820">',
       '<rect width="920" height="820" fill="#f7f9fc"/>',
       '<g font-family="sans-serif" fill="#173047">',
       '<text x="30" y="35" font-size="23">Why the previous lift layout became long</text>',
       '<text x="30" y="61" font-size="14">Same scale. Existing comparison layouts; neither is a flight-approved design.</text>']
scale = 0.36
for index, key in enumerate(('octo10', 'quad10')):
    entry = r['flights']['vacuum_' + key]
    width, depth, _ = entry['screen']['envelope_mm']
    origin_x = 60 + index * 450
    origin_y = 153
    def point(x, y):
        return origin_x + (x + width / 2) * scale, origin_y + (y + depth / 2) * scale
    def text(x, y, value, size=14):
        out.append(f'<text x="{x:g}" y="{y:g}" font-size="{size}">{html.escape(value)}</text>')
    text(origin_x, 103, 'Eight independent rotors' if index == 0 else 'Four independent rotors', 19)
    text(origin_x, 129, f'{width:g} × {depth:g} mm · {entry["assembly"]["mass_g"][1]/1000:.2f} kg complete')
    out.append(f'<rect x="{origin_x}" y="{origin_y}" width="{width*scale:g}" height="{depth*scale:g}" fill="none" stroke="#9baab7" stroke-dasharray="5 5"/>')
    for i, (x, y) in enumerate(c['lift']['variants'][key]['rotors_xy_relative_mm']):
        px, py = point(x, y)
        out.append(f'<circle cx="{px:g}" cy="{py:g}" r="{c["lift"]["guard_diameter_mm"]*scale/2:g}" fill="#ffe8cf" stroke="#bc7525" stroke-width="2"/>')
        out.append(f'<circle cx="{px:g}" cy="{py:g}" r="{c["lift"]["prop_diameter_mm"]*scale/2:g}" fill="none" stroke="#bc7525" stroke-dasharray="3 3"/>')
        text(px-4, py+5, str(i+1))
    px, py = point(-137.5, -137.5)
    out.append(f'<rect x="{px:g}" y="{py:g}" width="{275*scale:g}" height="{275*scale:g}" rx="4" fill="#dce8f7" stroke="#466cbd" stroke-width="2"/>')
    text(px+12, py+45, '275 mm')
    text(px+20, py+64, 'body')
    text(origin_x, origin_y+depth*scale+28, f'Peak thrust/weight screen: {entry["screen"]["thrust_weight_nominal"]:.2f}:1')
    if index == 1:
        text(origin_x, 547, 'Same core and loaded vacuum bottom.')
        text(origin_x, 571, 'Four rotors miss the provisional 2:1 target;')
        text(origin_x, 593, 'eight were a margin choice, not a minimum.')
out += ['<text x="30" y="731" font-size="15">Width: 360 mm between columns + 284 mm guard = 644 mm.</text>',
        '<text x="30" y="757" font-size="15">Octo length: 1160 mm between outer row centres + 284 mm guard = 1444 mm.</text>',
        '<text x="30" y="791" font-size="13">Guards stay clear of the central body. Mass, guard losses and thrust margins are model assumptions.</text>',
        '</g></svg>']
(ROOT / 'design/system/output/lift_layout_review.svg').write_text('\n'.join(out) + '\n')
