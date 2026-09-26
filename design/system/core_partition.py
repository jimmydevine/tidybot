"""Revision F candidate, preserving the C/E inputs for before/after comparisons."""
from copy import deepcopy
import csv
import hashlib
import html
import json
import math
from pathlib import Path

import build as base
import airborne_study as air

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'design/system/output'


def read():
    return json.loads((ROOT / 'config/core_partition.json').read_text())


def carrier_parts(d):
    parts = []
    for s in d['carrier_stock']:
        p = deepcopy(s)
        p['stock_mass_g'] = math.prod(p['size']) * d['aluminum_density_g_mm3']
        p['shape'] = 'box'
        parts.append(p)
    s = d['posts']; length = s['length_mm']; od = s['tube_od_mm']
    mass = math.pi / 4 * length * ((od**2-s['tube_id_mm']**2)*d['aluminum_density_g_mm3'] + s['rod_diameter_mm']**2*d['steel_density_g_mm3'])
    for i, (x, y) in enumerate(s['centres_xy_mm']):
        parts.append(dict(id='post_'+str(i), min=[x-od/2,y-od/2,s['z_mm']],
            size=[od,od,length], shape='cylinder_z', stock_mass_g=mass))
    return parts


def configured(c, d):
    c = deepcopy(c)
    old = {p['id']:deepcopy(p) for p in c['parts']}
    c['parts'] = [p for p in c['parts'] if p['id']!='core_power' and p.get('parent')!='core_power']

    def add(id, module, xyz, size, hardware=(), shape='box', **extra):
        p = dict(id=id, module=module, label=id.replace('_',' '), min=xyz, size=size,
            group='power', hardware=[dict(id=h,qty=1) for h in hardware], shape=shape,
            notes='F allocation; attachment details, tolerances and thermal duty remain unqualified.', **extra)
        c['parts'].append(p)
        return p

    def ledger(id, mass, basis):
        c['hardware'][id] = dict(name=id.replace('_',' '), mass_g=mass, mass_basis=basis,
            source='config/core_partition.json', notes='Unmeasured design estimate',
            procurement='design_candidate', measured_mass_g=None)

    bay = d['core_logic_bay']
    add('core_logic_power_F','core',bay['min'],bay['size'],['logic_buck'])
    for id in [p['id'] for p in old.values() if p.get('parent')=='core_power']:
        p = old[id]; p['min'] = d['locations_mm'].get(id,p['min'])
        if id=='logic_buck_reference':
            p['parent']='core_logic_power_F'
        else:
            p.pop('parent')
            p['module']='air_common' if id in ('cincon_reference','sink_reference','power_fan_reference') else 'drive'
        # Place each complete installed assembly's mass at a physical reference.
        ids = {'cincon_reference':'tool_converter', 'motor_buck_reference':'motor_buck',
               'clamp_resistor_reference':'regen_clamp'}
        p['hardware']=[dict(id=ids[id],qty=1)] if id in ids else []
        if id=='cincon_reference': p['mass_cg_mm']=[60.5,45,107]
        if id=='clamp_resistor_reference': p['mass_cg_mm']=[109,54,106]
        c['parts'].append(p)

    for p in carrier_parts(d):
        mass = [p['stock_mass_g']*f for f in d['stock_mass_factors']]
        id='floor_'+p['id']; ledger(id,mass,'Unperforated stock volume and density; tube plus full-diameter steel rod for each post')
        add(id,'drive',p['min'],p['size'],[id],p['shape'],stock_mass_g=p['stock_mass_g'])
    for id,module,key,xyz in (
        ('core_interface_F','core','core_interface_allowance_g',[13,185,72]),
        ('floor_interface_F','drive','floor_interface_allowance_g',[75,95,50]),
        ('floor_carrier_fasteners','drive','carrier_fasteners_allowance_g',[80,69,86])):
        ledger(id,d[key],'Additional allowance; existing harness, converter carrier and frame budgets retained')
        add(id,module,xyz,[1,1,1],[id],'distributed',mass_cg_mm=xyz)
    c['interfaces']['bottom_power']='F_RAW6S: switched raw 6S and protected 5 V logic; local 12/24 V conversion'
    c['interfaces']['floor_current_allocations_a']={'raw_pack_contact_requirement':20,'5v':1.5}
    c['interfaces']['partition_F']=deepcopy(d['interface'])
    return c


def withdrawal_errors(parts):
    """Full upward core withdrawal vs new fixed-bottom hardware, not station motion.

    Core boxes sweep upward indefinitely. Distributed shells and wiring are not
    certified; including rail references catches clearances hidden by their parent.
    """
    core=[p for p in parts if p['module']=='core' and p['shape']!='distributed']
    floor=[p for p in parts if (p['id'].startswith('floor_') and p['shape']!='distributed')
           or p['id'] in ('cincon_reference','sink_reference','power_fan_reference',
                         'motor_buck_reference','clamp_resistor_reference','brake_cap_reference','clamp_control_reference')]
    errors=[]
    for a in core:
        for b in floor:
            if all(min(base.hi(a)[i],base.hi(b)[i])>max(a['min'][i],b['min'][i])+1e-7 for i in (0,1)) and base.hi(b)[2]>a['min'][2]+1e-7:
                errors.append(a['id']+' / '+b['id'])
    return errors


def summarize(a):
    subtotal={}
    for row in a['rows']:
        subtotal[row['module']]=subtotal.get(row['module'],0)+row['mass_g'][1]
    return dict(mass_g=a['mass_g'],cg_mm=a['cg_mm'],subtotals_g=subtotal)


def study(c, d, ad):
    new=configured(c,d); before_air=air.study(c,ad); after_air=air.study(new,ad)
    ground={}; transfers={}
    for bottom in ('vacuum','mop','low'):
        old=base.assembly(c,bottom); a=base.assembly(new,bottom)
        ground[bottom]=dict(before=summarize(old),after=summarize(a),assembly=a,
            delta_g=a['mass_g'][1]-old['mass_g'][1],
            allocation=base.allocation_checks(new,a['parts'],bottom),
            withdrawal_errors=withdrawal_errors(a['parts']),
            support=base.support_metrics(new,a),power=base.power_metrics(new,bottom))
        old=base.assembly(c,bottom,'quad10'); a=base.assembly(new,bottom,'quad10')
        transfers[bottom]=dict(before=summarize(old),after=summarize(a),
            screen=base.lift_metrics(new,a,'quad10'),delta_g=a['mass_g'][1]-old['mass_g'][1])
    return dict(revision=d['revision'],config=d,ground=ground,transfers=transfers,
        airborne_before=before_air,airborne_after=after_air,
        carrier_stock_g=sum(p['stock_mass_g'] for p in carrier_parts(d)),
        carrier_installed_g=sum(p['stock_mass_g'] for p in carrier_parts(d))+d['carrier_fasteners_allowance_g'][1],
        raw_branch_current_a=d['interface']['raw_branch_allocation_w']/min(d['interface']['operating_pack_v']),
        input_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [ROOT/'config/system_design.json',ROOT/'config/airborne_dusting.json',ROOT/'config/core_partition.json']},
        qualified=False)


def report(r):
    before=r['airborne_before']['cases']['quad10']; after=r['airborne_after']['cases']['quad10']
    core_before=summarize(before['assembly'])['subtotals_g']['core']
    core_after=summarize(after['assembly'])['subtotals_g']['core']
    tare=next(row['mass_g'][1] for row in after['assembly']['rows'] if row['hardware_id']=='battery_cartridge')
    rows=['# Revision F — core and floor-power partition', '',
        'Dimensioned candidate, not a fabrication release. C/E inputs remain the comparison baseline. All figures are estimates; no component has been weighed or tested in this revision.', '',
        '| Loaded configuration | Before | F candidate | Change |', '|---|---:|---:|---:|']
    for name,g in r['ground'].items():
        rows.append(f"| {name} + cap | {g['before']['mass_g'][1]:.0f} g | {g['after']['mass_g'][1]:.0f} g | {g['delta_g']:+.0f} g |")
    for name,g in r['transfers'].items():
        rows.append(f"| {name} + four-propeller lift | {g['before']['mass_g'][1]:.0f} g | {g['after']['mass_g'][1]:.0f} g | {g['delta_g']:+.0f} g |")
    rows += [f"| Airborne duster + four-propeller lift | {before['assembly']['mass_g'][1]:.0f} g | {after['assembly']['mass_g'][1]:.0f} g | {after['assembly']['mass_g'][1]-before['assembly']['mass_g'][1]:+.0f} g |",'',
        'Same battery cells, bin/water loads, cleaning hardware, sensors, guards and mission reserves in every comparison. The 140 g battery cartridge tare remains booked under core; cells are additional.', '',
        '## What moves and what is added', '',
        '- 190 g blower converter/cooling assembly moves to suction bottoms.',
        '- 24 g drive converter and 40 g braking assembly move to driven bottoms.',
        '- Core retains computing, all sensors, 5 V conversion, pack protection, battery receiver, frame and locks.',
        f"- Additional core interface allowance: {r['config']['core_interface_allowance_g'][1]} g. Fixed core falls from {core_before-tare:,.0f} to {core_after-tare:,.0f} g; including cartridge tare, {core_before:,.0f} to {core_after:,.0f} g.",
        f"- Each floor bottom adds {r['carrier_stock_g']:.1f} g of stock plus 10 g carrier fasteners and 16 g interface/wiring allowance: {r['carrier_installed_g']+16:.1f} g installed addition beyond relocated electronics.",
        '- Existing 190 g converter installation and original harness/frame allowances are retained. No credit is taken for their potentially redundant supports. Mop currently shares the carrier footprint; trimming its unused left shelf is a later opportunity.', '',
        '## Layout and exchange', '',
        'The bottom-owned power shelf occupies the old front-left converter space. Its main outline is 115 × 70 × 1 mm aluminum with a 34 × 17 mm front-right notch and a small left mounting tab. The shelf is at z = 86 mm. A 2 mm lower foot plate at z = 12 mm and three 72 mm tube/rod posts support it; 2 × 8 mm edge strips stiffen the shelf. The full dimension list is in core_partition.json and the CAD reference.', '',
        'Cut sheet/strip stock and drill holes; no machined block or bent-sheet tooling is assumed. This pass specifies stock envelopes and mass, not drilling templates: plate joints, anti-rotation, insulation, tolerances and attachment of the lower plate to the shared bottom frame still need design and load checks. The narrow post spacing requires lateral-stiffness validation. Hole removal is not credited in stock mass.', '',
        'Core 5 V board moves to [11, 93, 126] mm above the left MCU. Reserve a 34 × 47 × 14 mm bay and a local cap roof above z = 138 mm. Overall LiDAR height remains below 180 mm. Braking capacitor/control move behind y = 30 mm; the core camera occupies y ≤ 28 mm. The shelf notch preserves that upward removal path.', '',
        'Automatic checks cover static functional allocations and the upward core sweep against the new bottom power hardware. They do not validate complete station handling, connector float, cables, fastener heads, contoured shells or moving suspension/tool mechanisms.', '',
        '## Electrical interface', '',
        f"F_RAW6S supplies switched raw 18–25.2 V and protected 5 V logic to the bottom. At the 240 W raw-branch allocation, worst-case modeled current is {r['raw_branch_current_a']:.2f} A. Reserve contacts capable of 20 A continuously after thermal derating. This is a contact requirement, not a selected connector or fuse setting. The lift power trunk remains separate.", '',
        'The preceding keyed 12/24/5 V interface is incompatible. Give F_RAW6S a different physical key and ID; a software label alone does not prevent misconnection. Core protection/precharge remains upstream; local converters start disabled and run only after seating, all four bottom locks, identity, voltage, temperature and watchdog checks. Keep locks engaged during braking, disable converters, isolate and discharge the raw branch, then separate. Maintain core logic from dock power during exchange. The airborne duster uses the protected 5 V branch and keeps raw tool power disabled. The 18 V calculation boundary is not a recommended battery discharge cutoff.', '',
        'The 12 V regenerative clamp stays downstream of the drive buck; it does not rely on the buck returning braking energy to the battery. Converter enable polarity, capacitance/precharge, branch protection, CAN grounding, connector cycle life and fault responses remain implementation work.', '',
        'Moving converters gives no modeled efficiency benefit. Floor load/efficiency assumptions remain unchanged for comparison. Cincon specifies 87.5% full-load efficiency for CHB100W-24S24; the inherited model uses 90% for the 24 V rail, so actual duty efficiency and cooling still require verification. [Cincon datasheet](https://www.cincon.com/productdownload/Datasheet-CHB100W.pdf). The 12 V converter current capability depends on input voltage and cooling; headline current is not a guarantee across this 6S range. [Pololu D42V110F12](https://www.pololu.com/product/5677).', '',
        '## Flight consequence', '',
        '| Four-propeller airborne duster | Before | F candidate |','|---|---:|---:|',
        f"| Nominal mass | {before['assembly']['mass_g'][1]:.0f} g | {after['assembly']['mass_g'][1]:.0f} g |",
        f"| Modeled hover electrical power | {before['screen']['hover_w']:.0f} W | {after['screen']['hover_w']:.0f} W |",
        f"| Static thrust/weight, limiting rotor | {before['screen']['static_trim']['static_peak_thrust_weight']:.3f}:1 | {after['screen']['static_trim']['static_peak_thrust_weight']:.3f}:1 |"]
    for key,m in before['missions'].items():
        rows.append(f"| {key}: cleaning energy ceiling | {m['cleaning_seconds']:.0f} s | {after['missions'][key]['cleaning_seconds']:.0f} s |")
    rows += ['', 'Removing front power hardware moves the center of mass rearward; the flight calculation includes that unequal rotor loading. The nominal 2.002:1 result only just crosses the 2:1 arithmetic screen; the difference is far smaller than the design uncertainty and does not establish an adequate flight margin. These are energy/static screens using the same source thrust curve and guard assumptions, not achieved endurance or qualified flight. Upper mass bounds, contact dynamics and installed continuous thrust remain unresolved. Vacuum/sofa transfer loads retain their converters and increase with support hardware; the mop omits blower conversion and becomes lighter.', '',
        '## Next design work', '',
        'Resolve the shared bottom/core frame load paths and joints next. That will determine whether the extra shelf supports can be integrated into material already budgeted, and whether the common 305 g printed/metal core structure can be reduced. Preserve the current mass additions until actual replacement geometry supports a deduction. No new purchase or print is needed for this allocation review.', '',
        '[Design context](../../../docs/CORE_POWER_PARTITION.md) · [Interactive views](core_partition.html) · [FreeCAD](core_partition.FCStd) · [STEP](core_partition.step)']
    return '\n'.join(rows)+'\n'


def diagram(r, axis='top'):
    a=r['ground']['vacuum']['assembly']; ix,iy=(0,1) if axis=='top' else (1,2)
    colors={'core':'#396bc1','drive':'#d07b17','air_common':'#d07b17'}
    lines=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 700">',
        '<rect width="700" height="700" fill="#fff"/>',
        f'<text x="30" y="32" font-family="sans-serif" font-size="20">F power partition — {axis} view (mm)</text>',
        '<text x="30" y="57" font-family="sans-serif" font-size="14">Blue: core · Orange: bottom · Gray: neighboring allocations</text>']
    for p in a['parts']:
        if p['shape']=='distributed':continue
        focus=(p['group']=='power' or p['id'].startswith('floor_'))
        x=45+2*p['min'][ix]
        y=95+2*p['min'][iy] if axis=='top' else 600-2*(p['min'][iy]+p['size'][iy])
        col=colors.get(p['module'],'#999') if focus else '#aaa'
        lines.append(f'<rect x="{x}" y="{y}" width="{2*p["size"][ix]}" height="{2*p["size"][iy]}" fill="{col if focus else "none"}" fill-opacity=".22" stroke="{col}" stroke-width="{1.4 if focus else .6}"><title>{html.escape(p["label"])}: {p["min"]}, size {p["size"]}</title></rect>')
    def label(x,y,text):
        return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="11" fill="#203044" stroke="white" stroke-width="3" paint-order="stroke" pointer-events="none">{text}</text>'
    if axis=='top':
        lines += [label(132,196,'24 V + cooling'),label(270,229,'12 V / braking'),
                  label(76,323,'Core 5 V'),label(279,128,'Front camera — removal space'),
                  label(450,83,'FRONT (y = 0)'),label(450,658,'REAR')]
    else:
        lines += [label(85,328,'Bottom power shelf'),label(197,547,'72 mm posts'),
                  label(232,310,'Core 5 V'),label(320,200,'Core lifts upward to detach'),
                  '<path d="M335 290 V220 M329 228 L335 220 L341 228" fill="none" stroke="#396bc1" stroke-width="2"/>',
                  label(320,220,'Separate x positions overlap in this projection.')]
        for z in (0,50,100,150,180):
            lines += [label(5,604-2*z,str(z)),f'<path d="M34 {600-2*z} H41" stroke="#444"/>']
        lines += [label(8,226,'z'),label(70,620,'FRONT'),label(515,620,'REAR')]
    for value in (0,50,100,150,200,250,275):
        lines += [label(40+2*value,674,str(value)),f'<path d="M{45+2*value} 659 V663" stroke="#444"/>']
    lines += ['<text x="30" y="696" font-family="sans-serif" font-size="11">Allocation reference; not print geometry. Hover over a part for dimensions.</text>','</svg>']
    return ''.join(lines)


def main():
    c=base.read();d=read();r=study(c,d,air.read())
    for name,g in r['ground'].items():
        if g['allocation']['errors'] or g['withdrawal_errors']:
            raise ValueError((name,g['allocation']['errors'],g['withdrawal_errors']))
    for name,v in r['airborne_after']['cases'].items():
        if v['screen']['geometry_errors']:raise ValueError((name,v['screen']['geometry_errors']))
    OUT.mkdir(exist_ok=True)
    (OUT/'core_partition.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'core_partition.md').write_text(report(r))
    for axis in ('top','side'):(OUT/f'core_partition_{axis}.svg').write_text(diagram(r,axis))
    with (OUT/'core_partition_hardware.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['configuration','instance','hardware_id','module','low_g','nominal_g','high_g','mass_basis'])
        assemblies={k:g['assembly'] for k,g in r['ground'].items()}
        assemblies['air_dust_quad']=r['airborne_after']['cases']['quad10']['assembly']
        for key,a in assemblies.items():
            for row in a['rows']:w.writerow([key,row['instance'],row['hardware_id'],row['module'],*row['mass_g'],row['mass_basis']])
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TidyBot F power partition</title><style>body{font:16px system-ui;max-width:1000px;margin:30px auto;padding:0 20px;color:#203044}button{padding:10px;margin:5px}svg{width:100%;max-height:75vh}a{color:#2463a5}table{border-collapse:collapse;width:100%}th,td{padding:10px;text-align:left;border-bottom:1px solid #ddd}th{background:#eef3f7}</style><h1>Core / bottom power partition</h1><p>F candidate. Blue power hardware stays with the core; orange stays with the bottom. Hover over parts for dimensions. Geometry checks cover component envelopes; joints and physical performance remain unverified.</p><button id="top">Top view</button><button id="side">Side view</button><div id="view"></div><p><a href="core_partition.md">Mass, power and limitations</a> · <a href="core_partition.FCStd">FreeCAD</a> · <a href="core_partition.step">STEP</a> · <a href="core_partition_hardware.csv">Hardware ledger</a></p>SUMMARY<p>Estimated complete loaded masses. Battery, contents, cleaning hardware, guards and mission reserves are unchanged. This candidate is not ready to fabricate or fly.</p><script>const views=VIEWS;const view=document.getElementById('view');for(const key of ['top','side'])document.getElementById(key).onclick=()=>view.innerHTML=views[key];view.innerHTML=views.top;</script></html>'''
    summary=['<table><tr><th>Loaded configuration</th><th>Before</th><th>F candidate</th><th>Change</th></tr>']
    for line in report(r).split('## What moves')[0].splitlines():
        if line.startswith('| ') and not line.startswith('| Loaded'):
            summary.append('<tr>'+''.join('<td>'+html.escape(cell.strip())+'</td>' for cell in line.split('|')[1:-1])+'</tr>')
    summary.append('</table>')
    page=page.replace('SUMMARY',''.join(summary)).replace('VIEWS',json.dumps({a:diagram(r,a) for a in ('top','side')}))
    (OUT/'core_partition.html').write_text(page)
    print(report(r).split('## What moves')[0])


if __name__=='__main__':main()
