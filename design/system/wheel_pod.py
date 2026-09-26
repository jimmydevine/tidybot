"""J overlays H/I without silently changing the complete G mass ledger."""
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import floor_support as support
import height_mounting as height

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'


def read():
    return json.loads((ROOT/'config/wheel_pod.json').read_text())


def configured(h,d):
    h=deepcopy(h);p=d['pivot'];w=h['wheel']
    w.update(pivot_diameter_mm=p['diameter_mm'],bushing_length_mm=p['bushing_length_mm'],
             bushing_od_mm=p['bushing_od_mm'],bushing_centres_x_mm=p['bushing_centres_x_mm'],
             pivot_diameter_sensitivity_mm=[6,8])
    return h


def spring_pose(h,d,travel,shim):
    s=d['spring']
    if not s['shim_range_mm'][0]<=shim<=s['shim_range_mm'][1]:raise ValueError('shim outside design range')
    lower=support.rotate_yz(h,*s['lower_pivot_yz_mm'],travel)
    upper=[s['upper_pivot_yz_mm'][0],s['upper_pivot_yz_mm'][1]-shim]
    delta=[u-l for u,l in zip(upper,lower)];span=math.hypot(*delta)
    if span<=2*s['seat_offset_mm']:raise ValueError('spring seats cross')
    unit=[v/span for v in delta];length=span-2*s['seat_offset_mm']
    bottom=[v+s['seat_offset_mm']*a for v,a in zip(lower,unit)]
    top=[v-s['seat_offset_mm']*a for v,a in zip(upper,unit)]
    compression=s['free_length_mm']-length;force=max(0,compression)*s['rate_n_mm']
    # Downward force at the moving cup. Its moment about X balances wheel load.
    py,pz=h['wheel']['pivot_yz_mm'];ay=support.pose(h,travel)['axle_y_mm']
    moment_arm=(py-lower[0])*unit[1]+(lower[1]-pz)*unit[0]
    wheel_force=force*moment_arm/(py-ay)
    return dict(travel_mm=travel,shim_mm=shim,lower_pivot_yz_mm=lower,upper_pivot_yz_mm=upper,
                lower_contact_yz_mm=bottom,upper_contact_yz_mm=top,unit_yz=unit,
                length_mm=length,compression_mm=compression,force_n=force,
                equivalent_wheel_force_n=wheel_force,moment_arm_mm=moment_arm,
                guide_overlap_mm=2*s['guide_length_mm']-length,
                guide_end_gap_mm=length-s['guide_length_mm'],
                solid_gap_mm=length-s['solid_height_limit_mm'])


def spring_screen(h,d):
    s=d['spring'];w=h['wheel'];rows=[]
    for t in range(126):
        travel=-w['droop_candidate_mm']+(w['bump_mm']+w['droop_candidate_mm'])*t/125
        for k in range(13):rows.append(spring_pose(h,d,travel,k*.5))
    r=dict(samples=len(rows),min_length_mm=min(r['length_mm'] for r in rows),max_length_mm=max(r['length_mm'] for r in rows),
           max_force_n=max(r['force_n'] for r in rows),min_force_n=min(r['force_n'] for r in rows),
           min_guide_overlap_mm=min(r['guide_overlap_mm'] for r in rows),
           min_guide_end_gap_mm=min(r['guide_end_gap_mm'] for r in rows),min_solid_gap_mm=min(r['solid_gap_mm'] for r in rows),
           guide_radial_gap_mm=(s['upper_guide_id_mm']-s['lower_guide_od_mm'])/2,
           spring_to_guide_radial_gap_mm=(s['id_min_mm']-s['upper_guide_od_mm'])/2)
    r['passes']=all([r['min_force_n']>0,r['min_guide_overlap_mm']>=s['minimum_guide_overlap_mm'],
        r['min_guide_end_gap_mm']>=s['minimum_guide_end_gap_mm'],r['min_solid_gap_mm']>=s['solid_margin_mm'],
        r['guide_radial_gap_mm']>0,r['spring_to_guide_radial_gap_mm']>0])
    r['selected_spring']=False;r['fatigue_buckling_and_print_tolerances_verified']=False
    return r


def axial_stack(d):
    m=d['motor'];b=d['bracket'];u=d['hub'];p=d['pivot'];face=m['gear_face_x_mm']
    tip=face-m['shaft_length_mm'];back=u['back_x_mm'];front=back-u['body_length_mm']-u['pilot_length_mm']
    # Outward is decreasing X for the left wheel.
    return dict(gear_face_x_mm=face,motor_plate_x_mm=[face-b['thickness_mm'],face],shaft_tip_x_mm=tip,
                hub_x_mm=[front,back],shaft_hub_overlap_mm=max(0,min(face,back)-max(tip,front)),
                boss_to_hub_back_mm=face-m['boss_length_mm']-back,
                wheel_x_mm=[back-u['wheel_extent_from_back_mm'][1],back-u['wheel_extent_from_back_mm'][0]],
                motor_thread_insertion_mm=b['motor_screw_length_mm']-b['thickness_mm'],
                maximum_motor_thread_insertion_mm=m['maximum_thread_insertion_mm'],
                pivot_pin_mass_g=math.pi*p['diameter_mm']**2/4*p['pin_length_mm']*.00785,
                flush_heads_required=True,hub_clamp_and_motor_radial_rating_verified=False)


def stop_targets(h,d):
    w=h['wheel'];s=d['stop'];theta=math.radians(support.pose(h,w['bump_mm'])['angle_deg'])
    py,pz=w['pivot_yz_mm'];y=py-s['lever_mm']
    z=pz+(s['strike_z_mm']-pz-s['lever_mm']*math.sin(theta))/math.cos(theta)
    return dict(moving_contact_nominal_yz_mm=[y,z],bump_contact_yz_mm=support.rotate_yz(h,y,z,w['bump_mm']),
                nominal_gap_mm=s['strike_z_mm']-z,
                droop_contact_pose=support.pose(h,-w['droop_candidate_mm']),
                hardware_complete=False,scope='Point-contact targets, not a modeled hard stop or droop retainer')


def pivot_screen(h,d):
    """Resolve spring direction and actual bump-stop lever at full bump.

    The fore/aft force uses the H 36 mm moment-arm bound; at full bump the
    ideal floor contact is only 26 mm below the pivot, so this is conservative.
    A bigger spring force does NOT necessarily bound the bearing loads.
    """
    w=h['wheel'];a=support.pose(h,w['bump_mm']);stop=stop_targets(h,d)
    lever=w['pivot_yz_mm'][0]-stop['bump_contact_yz_mm'][0]
    cases=[]
    for i in range(13):
        s=spring_pose(h,d,w['bump_mm'],i*.5)
        for direction in (-1,1):
            fw=w['factored_vertical_wheel_load_n'];fh=direction*w['horizontal_wheel_load_n']
            fs=s['force_n'];fy=-fs*s['unit_yz'][0];fz=-fs*s['unit_yz'][1]
            force=(fw*(a['pivot_y_mm']-a['axle_y_mm'])+fh*w['axle_yz_mm'][1]-fs*s['moment_arm_mm'])/lever
            xs=[w['contact_x_mm'],d['spring']['x_mm'],d['stop']['x_mm']]
            az=support.simply_supported_loads(xs,[fw,fz,-force],w['bushing_centres_x_mm'])
            ay=support.simply_supported_loads(xs,[fh,fy,0],w['bushing_centres_x_mm'])
            pz=support.simply_supported_loads(w['bushing_centres_x_mm'],[-v for v in az['reactions_n']],w['fixed_support_centres_x_mm'])
            py=support.simply_supported_loads(w['bushing_centres_x_mm'],[-v for v in ay['reactions_n']],w['fixed_support_centres_x_mm'])
            moment=math.hypot(pz['max_moment_nmm'],py['max_moment_nmm'])
            reaction=max(math.hypot(y,z) for y,z in zip(ay['reactions_n'],az['reactions_n']))
            cases.append(dict(shim_mm=i*.5,fore_aft_force_n=fh,stop_force_n=force,spring_force_n=fs,
                moment_bound_nmm=moment,max_bearing_reaction_n=reaction))
    moment=max(c['moment_bound_nmm'] for c in cases);reaction=max(c['max_bearing_reaction_n'] for c in cases)
    screens=[]
    for dia in (6,8):
        bending=32*moment/(math.pi*dia**3);shear=4*reaction/(math.pi*dia**2)
        screens.append(dict(diameter_mm=dia,bending_mpa=bending,shear_mpa=shear,
            passes=bending<=w['steel_bending_screen_mpa'] and shear<=w['steel_shear_screen_mpa']))
    return dict(screens=screens,cases=cases,stop_lever_at_bump_mm=lever,
        max_hard_stop_force_n=max(c['stop_force_n'] for c in cases),pin_moment_bound_nmm=moment,
        max_projected_bushing_pressure_mpa=reaction/(w['pivot_diameter_mm']*w['bushing_length_mm']),
        motor_output_radial_load_rating_verified=False,bushing_rating_verified=False,
        scope='Full-bump static impact screen over preload settings and both fore/aft signs; separately bounded pin bending axes. Does not qualify the moving cradle or fixed joints.')


def preload(h,d,g):
    rows={}
    for b in ('vacuum','mop','low'):
        load=support.static_wheel_loads(g,h,b)['support_force_ranges_n'][:2]
        # At nominal pose cups are vertical, 16/40 moment ratio is exact.
        f0=spring_pose(h,d,0,0)['equivalent_wheel_force_n']
        slope=spring_pose(h,d,0,1)['equivalent_wheel_force_n']-f0
        required=[[(v-f0)/slope for v in pair] for pair in load]
        rows[b]=dict(wheel_load_ranges_n=load,required_shim_ranges_mm=required,
                     within_adjuster_range=all(d['spring']['shim_range_mm'][0]<=x<=d['spring']['shim_range_mm'][1] for pair in required for x in pair))
    return rows


def study(h,d,g):
    j=configured(h,d);spring=spring_screen(j,d);pivot=pivot_screen(j,d)
    return dict(revision=d['revision'],config=d,configured_support=j,axial=axial_stack(d),
                spring=spring,pivot=pivot,
                stops=stop_targets(j,d),preload=preload(j,d,g),
                poses=[spring_pose(j,d,t,k) for t in (-2.5,0,10) for k in (0,6)],
                fabrication_release=False,complete_mass_baseline='G retained; J subtotal does not replace complete masses',
                continuous_clearance_proven=False,
                input_hashes={name:hashlib.sha256((ROOT/'config'/name).read_bytes()).hexdigest() for name in
                    ('system_design.json','core_partition.json','frame_joints.json','floor_support.json','height_mounting.json','wheel_pod.json')})


def report(r):
    a=r['axial'];s=r['spring'];p=r['pivot'];st=r['stops']
    lines=['# J wheel-pod mechanism study','',r['config']['status'],'',
       'Complete G mass remains unchanged. These are calculated nominal dimensions and candidate parts; no physical load test is claimed.','',
       '## Shaft, motor and wheel stack','',
       f"Left tire X={a['wheel_x_mm'][0]:g}…{a['wheel_x_mm'][1]:g} mm; mirrored right tire ends at 273 mm. Motor plate X=24…26 mm sits inside the wheel recess.",
       f"Shaft/hub nominal axial overlap {a['shaft_hub_overlap_mm']:.2f} mm; motor boss to hub back {a['boss_to_hub_back_mm']:.2f} mm. Proposed flush M3×6 screws enter the gearbox {a['motor_thread_insertion_mm']:g} mm, below its {a['maximum_motor_thread_insertion_mm']:g} mm maximum. Stock bracket holes are not countersunk.",'',
       '## Pivot and spring','',
       '| Pin | Calculated bending | Preliminary screen |','|---|---:|---|']
    for v in p['screens']:lines.append(f"| {v['diameter_mm']} mm | {v['bending_mpa']:.1f} MPa | {'Pass' if v['passes'] else 'Fail'} |")
    lines+=['',f"Bearings at X=44/88 mm leave room for two internal collars. The 8×80 mm steel pin weighs {a['pivot_pin_mass_g']:.2f} g per side before tolerances. Collar clearance diameter is 22.4 mm, including the clamp screw.",'',
        f"At full bump the stop lever is {p['stop_lever_at_bump_mm']:.2f} mm, rather than its nominal 32 mm. Re-solving equilibrium across preload settings gives a maximum stop force of {p['max_hard_stop_force_n']:.1f} N. The weakest-preload case matters; the largest spring force alone does not bound pivot load.",'',
        f"Spring sourcing target: 5 N/mm, free length 32.5 mm, OD≤10 mm, ID≥7 mm, solid height≤13.5 mm. Across {s['samples']} sampled travel/preload combinations, installed length is {s['min_length_mm']:.2f}–{s['max_length_mm']:.2f} mm and force reaches {s['max_force_n']:.1f} N.",
        f"Minimum telescope overlap {s['min_guide_overlap_mm']:.2f} mm; guide end gap {s['min_guide_end_gap_mm']:.2f} mm; spring solid-height clearance {s['min_solid_gap_mm']:.2f} mm. Dimensional screen: {'pass' if s['passes'] else 'FAIL'}. This does not verify a spring SKU, fatigue, friction or print fit.",'',
        'Shims lower the upper rocker fork by 0–6 mm. At nominal travel, this supports 13–25 N per wheel. Shims are a setup adjustment for each bottom module; automatic attachment exchange does not adjust them.','',
        '| Bottom | Left shim range | Right shim range | In range |','|---|---:|---:|---|']
    for b,v in r['preload'].items():
        ranges=['–'.join(f'{x:.2f}' for x in pair)+' mm' for pair in v['required_shim_ranges_mm']]
        lines.append(f"| {b} | {ranges[0]} | {ranges[1]} | {v['within_adjuster_range']} |")
    lines+=['','Those ranges use G nominal mass/CG and caster headings, not revised pod mass or payload uncertainty. Recalculate after the installed mass ledger closes.','',
        '## Stop targets and remaining work','',
        f"Moving bump-contact point at nominal Y/Z={st['moving_contact_nominal_yz_mm'][0]:.2f}/{st['moving_contact_nominal_yz_mm'][1]:.2f} mm reaches the fixed Z=62 mm plane at +10 mm wheel travel. A positive droop retainer must stop at −2.5 mm. These point targets are not connected hardware.",'',
        'Finish the metal/printed load path, cap-to-frame fastening, spring SKU and cups, hard-stop strike surfaces, droop capture, wheel-drop switch, cable loop and bushing housing process. Raw printed bores are not precision bearing housings. Motor output-shaft radial capacity and hub clamp strength remain unverified. Caster retention from I also remains open.','',
        '## Sources','']
    for name,url in r['config']['sources'].items():lines.append(f'- [{name.replace("_"," ")}]({url})')
    return '\n'.join(lines)+'\n'


def main():
    h=support.read();d=read();g=support.baseline();r=study(h,d,g)
    OUT.mkdir(exist_ok=True)
    (OUT/'wheel_pod.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'wheel_pod.md').write_text(report(r))
    template=(ROOT/'design/system/wheel_pod_viewer.html').read_text()
    (OUT/'wheel_pod.html').write_text(template.replace('__MODEL__',json.dumps(r)))
    print(json.dumps(dict(spring=r['spring'],preload=r['preload'],pivot=r['pivot']),indent=2))


if __name__=='__main__':main()
