"""T: reconcile a complete bottom support scope before claiming integration savings."""
import csv
import json
from pathlib import Path
import core_support as S
import fixed_drive as N
import floating_heads as M
import height_mounting as I
import build as B
import mass_budgets as MB

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'
F_IDS={'floor_shelf_left','floor_shelf_right','floor_shelf_tab','floor_foot_plate',
       'floor_foot_tab','floor_rear_stiffener','floor_front_stiffener',
       'floor_post_0','floor_post_1','floor_post_2','floor_carrier_fasteners'}


def read():return json.loads((ROOT/'config/bottom_chassis.json').read_text())


def geometry(bottom='vacuum',d=None):
    d=d or read();parts=[];t=d['side_wall_mm'];seat=d['seat_wall_mm']
    def add(id,boxes,cuts=(),basis='Material route; fasteners, holes and stock radii not credited'):
        v,c=S.volume_and_centre(boxes,list(cuts))
        parts.append(dict(id=id,add=boxes,cut=list(cuts),volume_mm3=v,centre_mm=c,
                          mass_g=v*d['material_g_mm3']['aluminum'],basis=basis))
    # Existing receiver/cleat attachment faces X28 and X247 are preserved.
    add('left_side_rail',[[28-t,26.7,65,t,221.6,21]])
    add('right_front_rail',[[247,26.7,65,t,126.3,21]])
    add('right_offset_link',[[247,153,65,18,2,21]])
    add('right_rear_rail',[[263,155,65,t,93.3,21]])
    # The rear bridge goes below the rear cliff-sensor windows, behind the bin.
    for side,x in [('left',28-t),('right',263)]:
        if side=='right':
            add('right_rear_drop',[[x,248.3,62,t,26.7,3],[x,262.3,52.3,t,12.7,9.7]])
            continue
        add(side+'_rear_drop',[[x,248.3,52.3,t,26.7,33.7]],
            [[x-.1,248.2,52.2,t+.2,14.1,12.8],
             [x-.1,248.2,65,t+.2,25.5,21.1]] +
            ([[x-.1,258.3,69,t+.2,17,10]] if side=='right' else []))
    add('front_head_bridge',[[28,83.5,66.5,219,1.5,20]])
    wall=d['rear_tube_wall_mm']
    add('rear_crossmember',[[28,262.3,52.3,235,12.7,12.7]],
        [[27.9,262.3+wall,52.3+wall,235.2,12.7-2*wall,12.7-2*wall]],
        'Closed tube behind the bin and below cliff windows; joints/sleeves in frame_joints')
    for side,x in [('left',5),('right',247)]:
        for end,y in [('front',1.3),('rear',248.3)]:
            # L-shaped seat profiles, continuous with their local vertical leg.
            legx=28-seat if side=='left' else (247 if end=='front' else 263)
            add(side+'_'+end+'_seat',[[x,y,86-seat,23,25.4,seat],
                [legx,y,65,seat,25.4,21-seat]],
                [[legx-.1,258.3,64.9,seat+.2,16,14.1]] if side=='right' and end=='rear' else [],
                'Angle/profile blank, 86 mm seat retained; 4 mm stud bore and supplied corner radius remain to detail')
    # Plate counted here only; the 142 g I caster hardware excludes this plate.
    add('caster_saddle',[[117.5,222,56.5,40,40.3,3],
                         [117.5,259.3,59.5,40,3,5.5]],
        basis='L profile from stock angle or outsourced cut part; no assumption of a home bending brake')
    # Keep exact F shelf locations, replace the tall rods/feet with side webs.
    pp={v['id']:v for v in M.prepare(bottom)['parts']}
    for id in ('floor_shelf_left','floor_shelf_right','floor_rear_stiffener','floor_front_stiffener'):
        v=pp[id];add(id,[v['min']+v['size']],basis='Retained F shelf/stiffener geometry, counted once in this scope')
    top=104 if bottom=='vacuum' else 86
    for name,x in [('left',26),('inner',105)]:
        low=86 if name=='left' else 65
        if top>low:
            add('power_web_'+name,[[x,26.7,low,2,56.3,top-low]],
                [[x-.1,32.7,low+5,2.2,44.3,max(.1,top-low-10)]],
                'Windowed upright shares chassis support with power shelf; web and attachment dimensions unqualified')
    # Two strips and a rear web support three front control-board bays.
    deck=72.5 if bottom=='vacuum' else 54.5
    add('control_board_shelf',[[108,29,deck,139,54,1.5]],
        [[112,33,deck-.1,131,46,1.7]],'Open aluminum carrier under blower/drive/supervisor bays; insulation and standoffs separate')
    add('control_front_bridge',[[107,28,deck-7,140,1,7],
                                [108,29,deck-1.5,139,4,1.5]])
    shelf_face=deck if bottom=='vacuum' else deck+1.5
    add('control_rear_web',[[108,82.5,min(shelf_face,66.5),139,1,abs(shelf_face-66.5)]],
        basis='Rear shelf connection to head bridge; end clips and joint hardware remain in frame_joints')
    return parts


def before_rows(bottom):
    p=M.prepare(bottom)
    rows=[dict(id=v['hardware_id'],mass_g=v['mass_g'][1],basis=v['name'])
          for v in B.assembly(p['layout'],bottom,payload=False)['rows']
          if v['hardware_id'] in F_IDS|{'bottom_frame','caster'}]
    rows.extend(dict(id='N_'+v['id'],mass_g=v['mass_g'],basis=v['basis']) for v in N.stock_rows(N.read()))
    rows.append(dict(id='M_risers',mass_g=p['M']['modules'][bottom]['riser_addition_g'][1],
                     basis='M raised power carrier or tank supports, covered by T webs/tool mounts'))
    return rows


def screen(d):
    s=d['screens'];E=s['e_mpa'];k=s['section_factor'];t=d['side_wall_mm']
    # Gross vertical web; wheel force is transmitted into it by the N cleat.
    span=261-14;at=141-14;inertia=t*21**3/12*k
    side=N.beam_bending(span,[at],[s['wheel_force_n']],E*inertia)
    stress=side['max_moment_nmm']*10.5/inertia
    seat=d['seat_wall_mm'];seat_stress=s['corner_force_n']*12/(25.4*seat**2/6*k)
    # Rear box tube must carry caster force and the pitch torque from its arm.
    b=12.7;w=d['rear_tube_wall_mm'];Iy=(b**4-(b-2*w)**4)/12*k
    rear=N.beam_bending(235,[109.5],[s['caster_force_n']],E*Iy)
    J=(b-w)**3*w*k
    torque=s['caster_force_n']*(268.65-232)+s['caster_horizontal_n']*58
    torsion=N.beam_torsion(235,[109.5],[torque],26000*J)
    shear=torsion['max_torque_nmm']/(2*(b-w)**2*w*k)
    bending=rear['max_moment_nmm']*(b/2)/Iy
    # Open strips have low torsional stiffness: do not report a side-web pass
    # as a complete frame pass, nor a fixed-end beam as a qualified bolted joint.
    return dict(side_web=dict(stress_mpa=stress,deflection_mm=side['max_deflection_mm'],
                passes=stress<s['bending_limit_mpa'] and side['max_deflection_mm']<s['deflection_limit_mm']),
        corner_seat=dict(stress_mpa=seat_stress,passes=seat_stress<s['bending_limit_mpa']),
        rear_tube=dict(combined_stress_mpa=(bending*bending+3*shear*shear)**.5,
            twist_deg=torsion['max_twist_deg'],deflection_mm=rear['max_deflection_mm']),
        unchanged_drive=N.structural_screen(N.read()),whole_frame_qualified=False,
        scope='150 N per wheel, 300 N unequal corner case, 100 N caster plus 25 N fore/aft. Side-web strong-axis and corner-strip screens only; eccentric cleat loading, open-section torsion, rear notches, holes, buckling, joints and fatigue are unresolved. Rear-tube torsion assumes both ends restrained. Do not infer 600 N module retention from these local screens.')


def study(d=None):
    d=d or read();cases=[];ic=I.read()['caster']
    caster=[dict(id='caster_'+id,mass_g=ic[key],basis=basis) for id,key,basis in [
        ('bare','bare_mass_g','I catalog bare caster reference'),('stem','stem_mass_g','I selected fitting reference'),
        ('upper_hardware','upper_fasteners_mass_reserve_g','I upper nut/washer allowance'),
        ('secondary_retention','secondary_retention_mass_reserve_g','I caster-to-plug captive retention allowance; still unresolved')]]
    baselines={v['id']:v for v in MB.study()['cases']}
    for bottom,id in [('vacuum','O_vacuum'),('mop','N_mop')]:
        parts=geometry(bottom,d);before=before_rows(bottom)
        kept=[dict(id='N_'+v['id'],mass_g=v['mass_g'],basis=v['basis']) for v in N.stock_rows(N.read())]
        rows=parts+kept+caster+d['remaining_parts'];old=sum(v['mass_g'] for v in before);new=sum(v['mass_g'] for v in rows)
        base=baselines[id];saving=old-new
        cases.append(dict(bottom=bottom,parts=parts,prior_rows=before,rows=rows,prior_scope_g=old,
            material_g=sum(v['mass_g'] for v in parts),candidate_scope_g=new,conditional_saving_g=saving,
            current_transfer_g=base['max_contents_mass_g'],candidate_transfer_g=base['max_contents_mass_g']-saving,
            budget_g=base['budget_g'],candidate_over_budget_g=base['max_contents_mass_g']-saving-base['budget_g'],
            impossible_zero_scope_transfer_g=base['max_contents_mass_g']-old,
            booked_saving_g=0,measured_compliance=False))
    return dict(config=d,cases=cases,screens=screen(d),fabrication_release=False,
        caster_correction_g=sum(v['mass_g'] for v in caster)-112,
        retained_functions=['motor/wheel/hub geometry','500 mL vacuum bin','350 mL mop tank','all power electronics and cooling','automatic module/head/battery interfaces','head lift and compliance','bumper/sensor hardware'],
        source_fingerprint=S.P.source_fingerprint())


def main():
    r=study();(OUT/'bottom_chassis.json').write_text(json.dumps(r,indent=2)+'\n')
    with (OUT/'bottom_chassis_mass.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['bottom','scope','id','mass_g','basis'],extrasaction='ignore');w.writeheader()
        for c in r['cases']:
            for scope,key in [('before','prior_rows'),('candidate','rows')]:
                w.writerows(dict(v,bottom=c['bottom'],scope=scope) for v in c[key])
    lines=['# T — integrated bottom chassis comparison','','The side rails carry the fixed drive crossmember, head receiver, power shelves and rear caster beam. The four module-seat locations remain at Z86. This comparison replaces complete scopes; it does not remove H route boxes as fictitious mass savings.','',
        '**Review geometry only.** Detailed attachment holes, several mount profiles and torsional/joint qualification remain unfinished. The full N drive assembly is retained once. R and S savings are not stacked.','',
        '| Bottom | Previous local scope | T local scope | Conditional saving | Loaded transfer with T only | Over 4.5 kg |','|---|---:|---:|---:|---:|---:|']
    for c in r['cases']:lines.append(f"| {c['bottom']} | {c['prior_scope_g']:.1f} g | {c['candidate_scope_g']:.1f} g | {c['conditional_saving_g']:+.1f} g | {c['candidate_transfer_g']/1000:.3f} kg | {c['candidate_over_budget_g']:+.0f} g |")
    lines+=['','The old local scope includes 225 g general frame, complete N supports, complete F mechanical carrier, M risers and 112 g installed caster. The T scope includes all new material, retained N supports, caster hardware and explicit completion rows. The 16 g floor electrical interface, harness, converters, controllers, tool structure and automatic coupling budgets stay outside this replacement.','',
        'The I caster hardware totals 142 g: 90 g caster, 20 g stem, 12 g upper fastening and 20 g unresolved captive retention. That is 30 g more than the old 112 g allocation, before this study’s separately counted saddle. The newer I hardware had not been carried into N/O totals. This is an accounting correction within the T comparison, not a measured weight.','',
        f"Even the impossible removal of the entire {r['cases'][0]['prior_scope_g']:.1f} g old support/caster scope would leave the vacuum at {r['cases'][0]['impossible_zero_scope_transfer_g']/1000:.3f} kg. Chassis changes alone cannot close the original 774.8 g vacuum deficit. A real replacement must weigh more than zero, so further reduction must also come from other assemblies.",'',
        'The frame does not yet carry a complete 600 N retention qualification. N’s wheel support stress screen remains unchanged. New side webs and corner seats have local bending calculations below; open-section torsion, offset cleat moments, rear reliefs, bolt patterns, local buckling and motor-bearing limits remain open. Nominal fit is not a structural release.','',
        '## Material and completion rows','']
    for c in r['cases']:
        lines += [f"### {c['bottom']}",'','| Item | Mass | Basis |','|---|---:|---|']
        lines += [f"| {v['id']} | {v['mass_g']:.2f} g | {v['basis']} |" for v in c['rows']]
    checks_path=OUT/'bottom_chassis_cad_checks.json'
    if checks_path.exists():
        cad=json.loads(checks_path.read_text())
        if cad['source_fingerprint']!=r['source_fingerprint']:raise RuntimeError('Regenerate T CAD before publishing report')
        lines+=['','## Geometry checks','',
            'The CAD is a rejected route candidate. Counts below are sampled intersections, not counts of unique defects. No print files are released.','',
            '| Check | Intersections |','|---|---:|']
        lines += [f"| {key} | {len(cad[key])} |" for key in ('internal_intersections','equipment_intersections','head_intersections','withdrawal_intersections','core_upward_intersections')]
        lines += ['', 'Known obstructions include the inner power web against the head crossmember/motor envelope, front module seats across the carrier withdrawal path and the control-board support in the departing crossmember path. These remain visible failures. Removing material to clear them would require new seat/web load checks, so this heavier arrangement is not developed further.',
            'The core-removal check retracts the four lower G lock sliders before upward travel; checking engaged locks would create a false obstruction against the power shelf. New S parts are checked for geometric compatibility only, without taking their weight reduction. Mop motion uses conservative M bounding boxes, not a completed physical guide.','']
    lines+=['','## Load screens','', '```json',json.dumps(r['screens'],indent=2),'```','',
        'The aluminum density and elastic constants are design assumptions. The 120 MPa project screen is not a certified allowable. [Hydro 6061 material reference](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf). Angle-shaped seats/saddles require purchased angle or outsourced profiling; this study does not assume a bending brake or treat bent T6 sheet as qualified.','',
        '## Decision','',
        'Reject this arrangement for development: it is heavier before completing its joints, and its head/service paths have obstructions. Historical N/O totals stay unchanged; T is not a new accepted assembly. Next compare a structural tray carrying the existing motor brackets directly, evaluated under the same wheel loads and interfaces. Also review the 190 g 24 V converter/cooling assembly and the bin/air-path construction: the arithmetic rules out chassis-only closure. Preserve blower output, bin capacity, protection and autonomy when comparing alternatives.','']
    (OUT/'bottom_chassis.md').write_text('\n'.join(lines))
    print(json.dumps([{k:v for k,v in c.items() if k not in ('parts','prior_rows','rows')} for c in r['cases']],indent=2))


if __name__=='__main__':main()
