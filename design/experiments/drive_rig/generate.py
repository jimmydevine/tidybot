"""Generate offline drawings, course calculator and BOM summary from rig inputs."""
import csv
import html
import json
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'output'
OUT.mkdir(exist_ok=True)
C = json.loads((HERE / 'config.json').read_text())
motor_pitch = C['motor']['stationary_hole_pattern_mm']
motor_pitch_label = ' × '.join(f'{p:.2f}' for p in motor_pitch) + ' mm'
bracket_file = 'motor_bracket_' + f'{motor_pitch[0]:.2f}'.replace('.', 'p') + 'mm.stl'
bracket_fit_count = C['motor']['mount_fit']['bracket_physical_fit_count']
with (HERE / 'hardware.csv').open(newline='') as f:
    BOM = list(csv.DictReader(f))
total = sum(Decimal(r['unit_usd'])*int(r['quantity']) for r in BOM)
quoted = sum(Decimal(r['unit_usd'])*int(r['quantity']) for r in BOM if 'manufacturer' in r['price_basis'])
remaining = sum(Decimal(r['unit_usd'])*int(r['quantity']) for r in BOM
                if r['status'] not in ('purchased awaiting delivery', 'received'))
table = '\n'.join(f"| {r['quantity']} | {r['item']} | ${Decimal(r['unit_usd'])*int(r['quantity']):.2f} | {r['status']} | {r['price_basis']} |" for r in BOM if Decimal(r['unit_usd']))
(HERE / 'HARDWARE.md').write_text(f'''# Rolling rig hardware and purchase status

**Received: two HiLetgo AS5600 boards**, per owner report on 2026-09-07.
An included 4 × 2 mm magnet is also received; total magnet count is unconfirmed.
Two B-G431B-ESC1 boards remain ordered with receipt unreported.
The earlier ST estimate was later in the week; actual paid prices are unknown.
**Remaining planning allowance: ${remaining:.2f} before shipping/tax**, before
deducting any additional supplies already owned or ordered. Received encoders, bundled magnets and purchased controllers
are excluded from this remaining allowance.

The current complete-path planning reference total is **${total:.2f} before shipping/tax**.
It includes all listed
purchase allowances and consumable/media allowances, assuming reuse of the
owned motors, wheels, caster, Pi, battery, wattmeter, scale and tools. It is
not a purchase receipt. Only **${quoted:.2f}** uses observed manufacturer prices;
the remaining **${total-quoted:.2f}** uses explicitly labeled allowances. Regional
availability, taxes, minimum packs and shipping can change the total. A full
filament spool, if needed, costs more than the filament consumption allowance.
There is no dedicated force stand or precision scale purchase.

| Qty | Item | Reference/allowance USD | Status | Price basis |
|---:|---|---:|---|---|
{table}

The [CSV](hardware.csv) includes source links, quantities, owned items, wiring
notes and every allowance. Controller selection is the purchased ST path,
not interchangeable with the owned aircraft ESC or a brushed H-bridge.

Selected controllers and proposed supporting electronics:

- [ST B-G431B-ESC1](https://estore.st.com/en/products/evaluation-tools/product-evaluation-tools/mcu-mpu-eval-tools/stm32-mcu-mpu-eval-tools/stm32-discovery-kits/b-g431b-esc1.html):
  two purchased; $38.98 each is the earlier observed reference, not the receipt.
  Includes MCU, driver, current sensing and
  ST-LINK programmer, so no separate ESP32, PWM board, current-sense shield or
  servo tester is required. Small-pad soldering and custom firmware are required.
- [HiLetgo AS5600 module](https://www.amazon.com/dp/B09KGWC1PT): two received;
  owner reports 23 × 23 mm, 16 × 16 mm hole centers, 4 mm holes and centered chip.
  Hold further encoder support prints pending the retention redesign. The $5.95 each retained in the planning
  table is the historical Adafruit reference, not the HiLetgo purchase price.
- **Included HiLetgo magnet, 4 × 2 mm**, owner-measured: no separate magnet
  purchase allowance. The rig needs two; total received count is unconfirmed.
  Both the rigid-fit holder and tape trial are retired; the tape version enters
  but wobbles and lacks reach. Evaluate the owner's [metal-rod proposal](ENCODER_METAL_ROD.md)
  before moving the encoder. No rod diameter tolerance, cut length, retention
  method or cap geometry is released. Existing magnets/boards are candidates
  for reuse; magnetic field and mechanical alignment must be verified.
- [Pololu D24V50F5](https://www.pololu.com/product/2851): one; $35 allowance,
  not an observed price. It supplies the Pi; the motor controllers use the fused
  3S bus. Check regulator temperature and Pi rail voltage under actual USB load.

Fastener quantities for the modeled assembly (buy an assortment with spares):

| Location | Fasteners/spacers |
|---|---|
| Stationary motor faces | 8 × M2 × 6 pan head; nominal 2 mm engagement through 4 mm plate |
| Wheels | Existing M2 fasteners if suitable; otherwise select from assortment after measuring actual hub stack and clearance |
| Motor feet | 8 × M3 × 25, washers and nuts |
| Encoder carrier feet | 4 × M3 × 20, washers and nuts |
| Sensor boards | 8 × M3 × 12 screws/nuts (nylon preferred), 8 × 3 mm M3 insulating spacers, 16 insulating M3 washers; verify component clearance/full nut engagement; adjust spacers for actual sensor gap |
| Caster to riser | 2 × M3 × 14, washers and nuts; inspect ball/housing clearance |
| Caster riser to deck | 4 × M3 × 50 through bolts, washers and nuts |
| Ballast shelf | 4 × M3 × 60 through bolts, washers and nuts; 4 printed 42 mm columns |
| Pi | 4 × 10 mm M2.5 female spacers; 4 × 8 mm and 4 × 6 mm screws; verify spacer threads before tightening |
| Two controller carriers | 8 × 10 mm M3 female spacers; 16 × M3 × 8 screws with washers; board retention by edge pads/light ties |

No threaded inserts, machined hubs, new shafts or separate wheel bearings are
required. The small contact thermometer is a $20 allowance, not a selected SKU.
Regulator/switch/connector physical fit and actual stock still need checking
when choosing vendors. AS5600s and an included magnet are received; ST controllers are ordered.

See [ENCODER_MOUNT.md](ENCODER_MOUNT.md) for the first HiLetgo carrier fit and
per-board hardware. M3 replaces the earlier M2.5 sensor mounting hardware.

See [preparation before arrival](PREPARATION.md) for the remaining order checklist,
fit prints and measurement blanks. See the [assembly and test instructions](README.md) for wire routing, initial
fuse choices, low-current commissioning and the remaining firmware work.
''')

def esc(s): return html.escape(str(s))

svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 700" role="img" aria-label="Dimensioned top view of rolling drive rig">',
       '<style>text{font:16px sans-serif;fill:#223447}.small{font-size:13px}.dim{stroke:#607787;stroke-width:1;fill:none}</style>',
       '<rect width="960" height="700" fill="#f6f8fb"/>',
       '<text x="28" y="32" style="font-size:24px">Rolling rig · top view</text>',
       '<text x="28" y="57">Front at top. Dimensions in mm. Dashed orange = battery beneath tray.</text>']
# Draw physical coordinates at 2 px/mm, translated to page center.
svg.append('<g transform="translate(380 95) scale(2)">')
svg.append('<rect x="-110" width="220" height="240" fill="#d8e1e6" stroke="#667d8e"/>')
svg.append('<path d="M -118 65 L 118 65 L 0 210 Z" fill="#339d9620" stroke="#41958d" stroke-dasharray="4 3"/>')
for sign in (-1,1):
    x=114 if sign>0 else -122
    svg.append(f'<rect x="{x}" y="35" width="8" height="60" rx="3" fill="#303d46"/>')
    x=101 if sign>0 else -114
    svg.append(f'<rect x="{x}" y="51" width="13" height="28" fill="#399593"/>')
bl,bw,bh=C['payload']['battery_body_mm']
ml,mw,mh=C['payload']['wattmeter_body_mm']
svg += [f'<rect x="{-bl/2}" y="{C["payload"]["battery_center_y"]-bw/2}" width="{bl}" height="{bw}" fill="#efb661" fill-opacity=".4" stroke="#bc821f" stroke-dasharray="3 2"/>',
        '<rect x="-84" y="65" width="168" height="70" fill="#bd785340" stroke="#af7050"/>',
        f'<rect x="{-ml/2}" y="{C["payload"]["wattmeter_center_y"]-mw/2}" width="{ml}" height="{mw}" fill="#45566a" fill-opacity=".6" stroke="#334455"/>',
        '<rect x="-100" y="160" width="85" height="56" fill="#74a581" stroke="#315c48"/>',
        '<rect x="20" y="155.5" width="30" height="41" fill="#74a581" stroke="#315c48"/>',
        '<rect x="68" y="155.5" width="30" height="41" fill="#74a581" stroke="#315c48"/>',
        '<rect x="-22.5" y="196" width="45" height="28" fill="#f7f6ef" stroke="#607787"/>',
        '<circle cx="0" cy="210" r="4" fill="#65727a"/>',
        '<path class="dim" d="M -122 -9 L 122 -9 M -122 -13 L -122 -5 M 122 -13 L 122 -5 M -135 0 L -135 240 M -139 0 L -131 0 M -139 240 L -131 240"/>',
        '</g>',
        '<text x="300" y="72">244 across wheels</text>',
        '<text x="63" y="350" transform="rotate(-90 63 350)">240 deck length</text>',
        '<text x="347" y="298" class="small" style="fill:white">Wattmeter</text>',
        '<text x="284" y="381" class="small">Battery below shelf</text>',
        '<text x="215" y="478">Pi 4</text>',
        '<text x="412" y="503" class="small">Controllers</text>',
        '<text x="339" y="559" class="small">Caster</text>',
        '<text x="650" y="175">Deck: 220 × 240</text>',
        '<text x="650" y="210">Wheel track: 236</text>',
        '<text x="650" y="245">Axle to caster: 145</text>',
        '<text x="650" y="280">Wheel axle Z: 30</text>',
        '<text x="650" y="315">Deck underside Z: 50</text>',
        '<text x="650" y="350">Tray floor Z: 100</text>',
        '<text x="650" y="385">Tray rim Z: 110</text>',
        '<text x="650" y="430" class="small">Teal triangle: floor contacts.</text>',
        '<text x="650" y="450" class="small">Keep load centered between them.</text>',
        f'<text x="650" y="490" class="small">Battery body: {bl} × {bw} × {bh}</text>',
        f'<text x="650" y="510" class="small">Meter body: {ml} × {mw} × {mh}</text>',
        '<text x="650" y="530" class="small">Tray inside: 162 × 64</text>',
        f'<text x="28" y="633">Fit prototype · motor bracket pitch {motor_pitch_label} · caster hole pitch 34 mm</text>',
        '<text x="28" y="663" class="small">Wiring, detailed component profiles and screw clearances still require physical inspection.</text>',
        '</svg>']
(OUT/'plan.svg').write_text('\n'.join(svg))

page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TidyBot rolling drive rig</title><style>
body{font:17px/1.55 system-ui,sans-serif;margin:0;background:#f4f6f8;color:#243342}main{max-width:1080px;margin:auto;padding:30px}
h1{font-size:36px;line-height:1.2}h2{font-size:24px}p{max-width:850px}a{color:#086b76}.tag{color:#915b1e;font-weight:650}
section{background:white;padding:24px;border:1px solid #d9e1e6;border-radius:12px;margin:24px 0}img{width:100%;max-width:100%;height:auto}table{border-collapse:collapse;width:100%}th,td{padding:10px;text-align:left;border-bottom:1px solid #dce3e8}
.fields{display:flex;flex-wrap:wrap;gap:18px}label{display:block}input,select{display:block;padding:8px;font:inherit;border:1px solid #9cabb6;border-radius:5px;max-width:190px}output{display:block;font-size:22px;font-weight:600;margin-top:16px}.small{font-size:14px;color:#586b79}button{font:inherit;padding:8px 15px;background:#e0f0ed;border:1px solid #5b9289;border-radius:6px;cursor:pointer}
</style><main><p class="tag">GROUND DRIVE EXPERIMENT · FIT PROTOTYPE</p><h1>Test the drive at a known weight.</h1>
<p>Two owned BDUAV motors, 60 mm wheels, one caster, Pi 4 and the existing 3S battery. Add secured ballast, run a measured course, and record what actually happens.</p>
<p><a href="../README.md">Assembly and test instructions</a> · <a href="../HARDWARE.md">Complete hardware proposal</a> · <a href="drive_rig_assembly.step">Assembly STEP</a> · <a href="__BRACKET_FILE__">Updated motor bracket</a> · <a href="../ENCODER_METAL_ROD.md">Metal-rod encoder proposal</a> · <a href="../ENCODER_MOUNT.md">Encoder mounting guide</a></p>
<section><h2>The test chassis</h2><img src="assembly.svg" alt="Isometric CAD view of deck, wheels, motors, caster, battery, ballast tray, Pi and controller boards"><img src="plan.svg" alt="Top view with dimensions and component placement"><p>The deck prints as one 220 × 240 mm piece; wheels bring the width to 244 mm. The assembly now uses the received HiLetgo board outline, 16 mm square hole pattern and revised carrier. PCB thickness and sensor package dimensions are allowances; actual connector clearance and magnetic gap remain to check. No powered trials or load rating have been established.</p></section>
<section><h2>Observe speed over a fixed course</h2><p>Enter your measurements. Mass records the load condition; it does not predict speed. Time a visible chassis marker over the course using video timestamps.</p>
<div class="fields"><label>Total carried mass (g)<input id="mass" type="number" min="1" placeholder="Measured total"></label><label>Course distance (m)<input id="distance" type="number" min="0.01" step="0.01" value="2"></label><label>Observed elapsed time (s)<input id="elapsed" type="number" min="0.01" step="0.01" placeholder="Measured seconds"></label></div>
<output id="answer">Enter mass and elapsed time.</output><p class="small">Equivalent wheel RPM is calculated from ground speed and nominal 60 mm diameter; it is not an encoder reading. Standing-start times include acceleration.</p>
<p><a href="../record_run.py">CSV recorder for Pi/computer</a> · <a href="../runs.csv">Results file</a> · <a href="../masses.csv">Component mass worksheet</a></p>
<table><thead><tr><th>Target speed</th><th>60 mm wheel RPM</th><th>Ideal 2 m time at steady speed</th></tr></thead><tbody><tr><td>0.15 m/s</td><td>47.7</td><td>13.33 s</td></tr><tr><td>0.20 m/s</td><td>63.7</td><td>10.00 s</td></tr><tr><td>0.25 m/s</td><td>79.6</td><td>8.00 s</td></tr></tbody></table><p class="small">These are geometric targets, not simulated or measured motor performance. Use the CSV recorder to save observations; this calculator does not save entries.</p></section>
<section><h2>Hardware and readiness</h2><p><strong>Two HiLetgo AS5600s and an included 4 × 2 mm magnet received. ST controller receipt remains unreported.</strong> Remaining allowance: <strong>__REMAINING__ before shipping/tax</strong>, before deducting other supplies in inventory. Actual paid prices are unknown. The complete BOM separates observed reference prices from allowances.</p><p>Confirmed full bracket fits with free motor rotation: <strong>__BRACKET_FIT_COUNT__ of 2</strong>. The brackets use __MOTOR_PITCH__ adjacent-hole spacing. The second bracket fit remains unreported. One caster riser is printed and mounted; only one is required. The owner identified the extra clip-like feature as Cura support. A USB-only encoder diagnostic is available; motor-driving firmware and commissioning remain to be completed.</p><p><strong>Battery and wattmeter body dimensions fit the existing layout.</strong> The battery is 135 × 43 × 22 mm; the meter is 86 × 43 × 25 mm and fits the tray's 162 × 64 mm clear interior. Leads and straps require an unpowered assembly check. The photo shows the printed deck with one wheel/motor/encoder assembly. Its geometry and motor brackets are unchanged; the revised encoder carrier preserves the existing mounting interface.</p><p><strong>Next:</strong> the tape holder enters the bore but wobbles and lacks reach. Review the owner's <a href="../ENCODER_METAL_ROD.md">metal-rod proposal</a> before relocating the encoder. The owner-supplied SpeedyFPV listing corroborates the nominal 3.4 mm motor bore. Use a 3.4 mm nominal rod candidate; check close shaft fit and straight support length before selecting cut length, retention or magnet cap. No new print is released. The assembly preview is historical and does not validate a replacement. Independent weighing, wiring preparation and USB-only diagnostics can continue.</p></section></main>
<script>
const ids=['mass','distance','elapsed'];
function calculate(){const [m,d,t]=ids.map(id=>Number(document.getElementById(id).value));const out=document.getElementById('answer');
 if(![m,d,t].every(x=>Number.isFinite(x)&&x>0)){out.textContent='Enter positive measured values.';return;}
 out.textContent=`${m.toFixed(1)} g · ${(d/t).toFixed(3)} m/s average · ${(d/t*60/(Math.PI*.06)).toFixed(1)} equivalent wheel RPM`;}
ids.forEach(id=>document.getElementById(id).addEventListener('input',calculate));
</script></html>'''
(OUT/'drive_rig.html').write_text(page.replace('__REMAINING__',f'${remaining:.2f}')
    .replace('__BRACKET_FILE__',esc(bracket_file)).replace('__MOTOR_PITCH__',esc(motor_pitch_label))
    .replace('__BRACKET_FIT_COUNT__',str(bracket_fit_count)))
print(f'BOM planning total ${total:.2f}; observed prices ${quoted:.2f}; allowances ${total-quoted:.2f}')
print(f'Remaining planning allowance ${remaining:.2f}; actual paid total unknown')
print('Generated HARDWARE.md, plan.svg and drive_rig.html; results/masses left unchanged')
