"""S: core mass audit, explicit rectangular material geometry and load screens."""
import csv
import itertools
import json
import math
from pathlib import Path
import fixed_drive as N
import floating_heads as M
import build as B
import head_coupling as P
import mass_budgets as MB

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'


def read():return json.loads((ROOT/'config/core_support.json').read_text())


def box(x,y,z,a,b,c):return [x,y,z,a,b,c]


def inside(p,b):return all(b[i]<p[i]<b[i]+b[i+3] for i in range(3))


def volume_and_centre(add,cut):
    """Exact coordinate partition for unions/differences of axis-aligned boxes."""
    edges=[sorted({b[i]+offset for b in add+cut for offset in (0,b[i+3])}) for i in range(3)]
    spans=[[(a,b) for a,b in zip(e,e[1:]) if b>a] for e in edges]
    total=0;moments=[0,0,0]
    for cell in itertools.product(*spans):
        mid=[(a+b)/2 for a,b in cell]
        if not any(inside(mid,b) for b in add) or any(inside(mid,b) for b in cut):continue
        v=math.prod(b-a for a,b in cell);total+=v
        for i in range(3):moments[i]+=v*mid[i]
    if total<=0:raise ValueError('Material part is empty')
    return total,[v/total for v in moments]


def geometry(d=None):
    d=d or read();parts=[];beam=d['bridge'];rx=d['receiver']
    def add(id,material,boxes,cuts=(),role='fixed',basis='Dimensioned material; attachment holes and supplied radii not credited'):
        v,cg=volume_and_centre(boxes,list(cuts))
        parts.append(dict(id=id,material=material,add=boxes,cut=list(cuts),role=role,
            volume_mm3=v,mass_g=v*d['material_g_mm3'][material],centre_mm=cg,basis=basis))
    x=beam['x'];length=beam['length'];t=beam['thickness'];z=beam['z'];height=beam['height']
    for name,y in [('front',beam['front_y']),('rear',beam['rear_y'])]:
        add('equipment_bridge_'+name,'aluminum',[box(x,y,z,length,t,height)])
        yy=y-8 if name=='front' else y+t
        for side,xx in [('left',x),('right',x+length-8)]:
            a=xx if side=='left' else xx+7
            b=yy+7 if name=='front' else yy
            add(name+'_'+side+'_frame_clip','aluminum',[
                box(a,yy,z,1,8,6),box(xx,b,z,8,1,6)],basis='Gross angle-clip material; supplied bend radius and two-plane fasteners remain to detail')
    for side,x in [('left',rx['left_x']),('right',rx['right_x'])]:
        # Slots provide a path for the separate retracting latch tongue.
        add(side+'_receiver_end','aluminum',[box(x,rx['y'],rx['z'],1,rx['depth'],rx['height'])],
            [box(x-.1,94,73,1.2,53,43),box(x-.1,111.8,67.8,1.2,8.4,2.4),box(x-.1,129.5,65.9,1.2,23,2.9)],
            basis='1 mm receiver side web with central opening and latch slot; cartridge shoulder is in retained shell/restraint scope')
        xx=x+1 if side=='left' else x-6
        for name,y in [('front',85),('rear',beam['rear_y']-1)]:
            add(side+'_'+name+'_receiver_tab','aluminum',[box(xx,y,116,6,1,5.5)],
                basis='Receiver-to-bridge tab material; radiused bend/joint and fastener access remain unresolved')
        xx=x+1 if side=='left' else x-.5
        for i,y in enumerate((88,145)):
            add(side+'_guide_liner_'+str(i),'polymer',[box(xx,y,73,.5,6,43)],
                basis='Replaceable guide strip; nominal 0.2 mm clearance to retained cartridge outline, tolerance not qualified')
        xx=41.3 if side=='left' else 222.5
        add(side+'_battery_tongue','steel',[box(xx,112,68,4.2,8,2)],role='latch',
            basis='Closed-position tongue material; pawl, spring, guide and sensing retained in completion rows. Opens outward by 3 mm')
    # Pi tray is supported at the existing front rail and the new front bridge.
    add('pi_tray','polymer',[
        box(140,11,105.2,108,72.4125,1.5),
        box(140,11,106.7,1.5,72.4125,8),box(246.5,11,106.7,1.5,72.4125,8),
        box(140,11,106.7,108,1.5,8),
        box(140,80,114.7,1.5,3.4125,6.8),box(246.5,80,114.7,1.5,3.4125,6.8),
        box(135.5,80,113.5,6,3.4125,8),box(246.5,80,113.5,6,3.4125,8),
        box(140,6.0625,105.2,8,4.9375,8),box(240,6.0625,105.2,8,4.9375,8)],
        [box(144,15,105.1,100,64.4125,1.7),box(139.9,79.5,105.1,1.6,3,8.4)],basis='Open printed tray with outside ribs and raised rear attachment tabs; local relief clears floor shelf stiffener without changing that bottom part')
    add('supervisor_tray','polymer',[
        box(11,94,87,30.8,62,1.5),box(11,94,88.5,1,60,22),
        box(4.0875,94,109.5,6.9125,2,1),box(4.0875,151.5,109.5,6.9125,2,1)],
        basis='Printed shelf and outside wall tied to left G rail; board fasteners separate')
    add('power_board_shelf','aluminum',[box(226.2,84.5,87.5,44.3,71,1)],
        basis='Insulated shelf below protection bay; upright mounting and dielectric isolation retained in remaining mounts allowance')
    # Two logic-board trays are above the battery, with the electrical bays intact.
    for name,xyz,size in [('logic_buck_tray',[9,90,123.6],[35,49,1]),('dock_power_tray',[44.5,89,123.6],[36.5,62,1])]:
        xx,yy,zz=xyz;a,b,c=size
        add(name,'polymer',[box(xx,yy,zz,a,b,c)],[box(xx+3,yy+3,zz-.1,a-6,b-6,c+.2)],
            basis='Open logic tray; standoffs/rail attachments remain in equipment mounting allowance')
    # Mount reservation is inherited from I. This bridge plate does not change
    # lidar SKU or book the unaccepted A1-to-C1 mass reduction.
    add('lidar_tray','polymer',[box(102.4,97.15,131.5,64,64,1.5)],
        [box(110.4,105.15,131.4,48,48,1.7)],basis='Ring plate inside I mount reservation; legs and exact fasteners remain in mounting allowance')
    return parts


def audit():
    p=M.prepare('vacuum');rows=B.assembly(p['layout'],'vacuum',payload=False)['rows']
    grouped={}
    for row in rows:
        key=(row['module'],row['hardware_id'])
        if key not in grouped:grouped[key]=dict(module=key[0],id=key[1],name=row['name'],mass_g=0,basis=row['mass_basis'])
        grouped[key]['mass_g']+=row['mass_g'][1]
    core=sorted((v for v in grouped.values() if v['module']=='core'),key=lambda v:-v['mass_g'])
    metal=sum(v['mass_g'] for v in core if v['id'].startswith('G_'))
    return dict(core_rows=core,core_including_cartridge_g=sum(v['mass_g'] for v in core),
        metal_frame_and_fasteners_g=metal,rows=rows,
        basis='Latest M/N/O core ledger; G frame retained. These rows are NOT summed as the whole N/O robot: N replaces K pods and M/O add separate mechanisms.')


def study(d=None):
    d=d or read();parts=geometry(d);a=audit();oldrows=[v for v in a['core_rows'] if v['id'] in d['replace_hardware_ids']]
    before=sum(v['mass_g'] for v in oldrows);material=sum(v['mass_g'] for v in parts)
    unfinished=sum(v['mass_g'] for v in d['remaining_parts']);candidate=material+unfinished;saving=before-candidate
    cases=[]
    for row in MB.study()['cases']:
        if row['id'] not in ('O_vacuum','N_mop','G_E_air_dust'):continue
        cases.append(dict(id=row['id'],before_g=row['max_contents_mass_g'],candidate_g=row['max_contents_mass_g']-saving,
            budget_g=row['budget_g'],candidate_gap_g=row['max_contents_mass_g']-saving-row['budget_g'],
            layout_scope='vacuum and mop core fit checked' if row['id']!='G_E_air_dust' else 'mass projection only; common core placement has not been integrated with E duster',
            measured_compliance=False))
    b=d['bridge'];s=d['screen'];equipment=(a['core_including_cartridge_g']+d['retained']['battery_cells_g'])/1000
    force=equipment*B.G*s['equipment_acceleration_g']/s['sharing_beams'];I=b['thickness']*b['height']**3/12
    stress=force*b['length']/4*(b['height']/2)/I
    deflection=force*b['length']**3/(48*s['e_aluminum_mpa']*I)
    latch_force=s['cartridge_retention_n']/s['latches_sharing']
    return dict(config=d,parts=parts,audit={k:v for k,v in a.items() if k!='rows'},
        mass=dict(replaced_rows=oldrows,before_g=before,material_g=material,unfinished_g=unfinished,candidate_g=candidate,
            conditional_saving_g=saving,booked_saving_g=0,current_transfer_g=next(v['before_g'] for v in cases if v['id']=='O_vacuum'),
            core_candidate_including_cartridge_g=a['core_including_cartridge_g']-saving,
            same_capacity_wh=d['retained']['battery_capacity_ah']*d['retained']['battery_nominal_voltage_v']),cases=cases,
        beam_screen=dict(load_n=force,equipment_mass_g=equipment*1000,stress_mpa=stress,deflection_mm=deflection,
            passes=stress<=s['bending_limit_mpa'] and deflection<=s['deflection_limit_mm'],
            scope='Simply supported vertical bending, conservatively all baseline core plus cells at 3 g. End joints, weak-axis bending, torsion, holes and equipment fasteners unqualified. No 600 N module-interface load reassigned.'),
        latch_screen=dict(force_per_tongue_n=latch_force,nominal_engagement_mm=1.5,nominal_released_clearance_mm=1.5,
            average_shoulder_bearing_mpa=latch_force/(1.5*8),cantilever_stress_mpa=latch_force*2.1/(8*2**2/6),
            scope='Stress demand only, not allowable or qualification. Retained cartridge must have metal shoulders within its 65 g shell/restraint scope. All latches must lock; two-way sharing is not permission to operate with one unlocked.'),
        fabrication_release=False)


def report(r):
    m=r['mass'];a=r['audit'];b=r['beam_screen'];l=r['latch_screen']
    lines=['# S — shared core equipment supports and battery receiver','',
        'A pair of equipment bridges uses the existing G frame to support the battery receiver and lightweight equipment trays. The main frame, module locks, battery cartridge, protection and all electronics remain. This pass replaces only the former 160 g core-print allowance and 50 g fixed receiver allowance.','',
        '**Review candidate, not a fabrication release.** The contact/latch completion, several equipment mounts, fasteners and cooling guides remain explicit allowances.','',
        '## Core audit','',f"The current core, including its removable cartridge tare but excluding battery cells, is **{a['core_including_cartridge_g']:.1f} g**. The existing metal frame and frame fasteners account for **{a['metal_frame_and_fasteners_g']:.1f} g** and remain untouched.",'',
        '| Core item | Current mass |','|---|---:|']
    lines += [f"| {v['name']} | {v['mass_g']:.1f} g |" for v in a['core_rows'] if not v['id'].startswith('G_')]
    lines += ['', 'The 140 g removable cartridge contains 65 g shell/restraint, 35 g monitor/ID and 40 g fuse/contacts/wiring. All 140 g stays. Cells remain 753 g, 6S/5.2 Ah, 115.44 Wh nominal. No voltage, capacity, discharge capability, sensor or automation change is credited. The 170 g lidar row remains even though I has a smaller C1 placement candidate; this study does not accept that earlier performance trade.','',
        '## Installed replacement scope','', '| Item | Mass |','|---|---:|',
        f"| Previous core prints + fixed receiver | {m['before_g']:.2f} g |",
        f"| Modeled material | {m['material_g']:.2f} g |",
        f"| Remaining hardware and completion allowance | {m['unfinished_g']:.2f} g |",
        f"| Complete local candidate | {m['candidate_g']:.2f} g |",
        f"| Conditional saving | {m['conditional_saving_g']:.2f} g |",'',
        '| Part | Mass | Basis |','|---|---:|---|']
    lines += [f"| {v['id']} | {v['mass_g']:.2f} g | {v['basis']} |" for v in r['parts']+r['config']['remaining_parts']]
    lines += ['', 'The sum includes unions only once and subtracts modeled openings at solid material density. This is not a slicer/weighed result. The cartridge hardware, G frame/fasteners, eight locks, 125 g harness, 80 g main power stage, logic converters and all other masses stay in their original rows. R’s tentative head saving is not stacked onto this candidate.','',
        '## Complete non-lift mass at maximum modeled contents','',
        '| Configuration | Current | With S only | Budget | Candidate over / under |','|---|---:|---:|---:|---:|']
    for c in r['cases']:lines.append(f"| {c['id']} | {c['before_g']/1000:.3f} kg | {c['candidate_g']/1000:.3f} kg | {c['budget_g']/1000:.3f} kg | {c['candidate_gap_g']:+.0f} g |")
    lines += ['', 'Duster numbers are a mass projection only: the shared core layout still needs integration with its older E tool layout. Vacuum and mop packaging checks do not establish duster compatibility. Whole-assembly upper uncertainty remains undefined for N/O, and no saving is booked.','',
        '## Mechanical demand screens','',
        f"Two {r['config']['bridge']['length']:.3f} mm spans carry a conservative **{b['equipment_mass_g']:.1f} g** baseline core-plus-cells load at 3 g. Each takes **{b['load_n']:.2f} N**, producing **{b['stress_mpa']:.2f} MPa** bending stress and **{b['deflection_mm']:.3f} mm** deflection in the simply supported strip model. Screen result: **{'pass' if b['passes'] else 'fail'}** against project limits of 120 MPa / 1 mm.",
        'The bridge uses the existing 12.7 × 1.5875 mm strip reference on edge. Grade/temper and actual stock still need confirmation. Elastic modulus 69 GPa and density 2.7 g/cm³ are engineering assumptions. Hydro’s 6061 sheet supports the reference alloy context, not the joint design or other stock tempers. [Hydro alloy reference](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf).',
        f"A separate 100 N cartridge retention case shared by two tongues asks for **{l['force_per_tongue_n']:.0f} N each**, **{l['average_shoulder_bearing_mpa']:.2f} MPa** average shoulder bearing and **{l['cantilever_stress_mpa']:.2f} MPa** nominal tongue bending stress. These are capacity demands, not proof of a supplied latch, shell or fastener. Both latches must be sensed locked. Spring closure alone is not positive retention; completing the pawls remains required.",
        'The G corner frame retains the full 600 N inter-module requirement. The cartridge and component bridges do not carry that load instead. Weak-axis and torsional stiffness, fastening, sheet bend radii, local stress and durability remain open.','',
        '## Exchange and limits','',
        'The station supports the core and removes the bottom before cartridge extraction. It supports the cartridge, verifies zero power-contact current, then retracts both tongues 3 mm. The cartridge goes down 100 mm. The printed guide strips remain on the core, while the cartridge metal shoulders travel with the retained shell. The 0.2 mm nominal side-guide gap is not a tolerance-qualified fit.',
        'The 158 × 62 × 53 mm cell pocket and 16 × 62 × 53 mm electrical interface-end reservation remain protected. Neither validates an installed 150 A contact/fuse/BMS stack or soft-pack swelling clearance. The main battery interface is still unfinished; weight cannot be removed from its 140 g allowance on that basis.','',
        'See core_support_cad_checks.json for scoped intersections, upward core removal and downward cartridge clearance. Nominal non-overlap is not tolerance or deflection approval, and wire sweeps are not yet modeled.','',
        'The remaining system deficit requires additional concrete work on the bottom chassis and power-carrier supports, followed by bin/air-path construction. Further shaving of small common-core pieces alone will not close it.','']
    return '\n'.join(lines)


def main():
    r=study();(OUT/'core_support.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'core_support.md').write_text(report(r))
    with (OUT/'core_support_mass.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['id','mass_g','basis'],extrasaction='ignore');w.writeheader();w.writerows(r['parts']+r['config']['remaining_parts'])
    print(json.dumps(r['mass'],indent=2));print(json.dumps(r['beam_screen'],indent=2))


if __name__=='__main__':main()
