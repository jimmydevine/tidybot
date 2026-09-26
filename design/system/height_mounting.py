"""I packaging overlay: maintain H wheel travel and account for real stem space.

G/H evidence remains reproducible. Changed-component mass deltas are explicit;
incomplete H frame stock is never substituted for an installed assembly.
"""
from copy import deepcopy
import hashlib
import itertools
import json
import math
from pathlib import Path

import build as base
import floor_support as support
import frame_joints as frame

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'design/system/output'
BOTTOMS = ('vacuum', 'mop', 'low')


def read():
    return json.loads((ROOT / 'config/height_mounting.json').read_text())


def configured(g, h, d):
    c, s = deepcopy(g), deepcopy(h)
    l, t = d['lidar'], d['top_port']
    for p in c['parts']:
        if p['id'] == 'lidar':
            p.update(min=l['min_mm'][:], size=l['size_mm'][:], label=l['model'])
        if p['id'] == 'top_port':
            p.update(min=t['min_mm'][:], size=t['size_mm'][:], notes=t['note'])
        if p['id'] == 'vac_bin_upper':
            top = base.hi(p)[2]
            p['min'][2] = d['layout']['vac_bin_upper_bottom_mm']
            p['size'][2] = top - p['min'][2]
        if p['id'] in ('blower_bay', 'blower_reference', 'exhaust'):
            p['min'][2] += d['layout']['blower_raise_mm']
        if p['id'] == 'mop_pump':
            p['min'][2] += d['layout']['mop_pump_raise_mm']
    c['parts'].append(dict(id='I_lidar_mount', module='core', label='Lidar support reservation',
        min=l['mount_bay_min_mm'][:], size=l['mount_bay_size_mm'][:], shape='box',
        hardware=[], group='structure', notes=l['note']))
    # Do not edit mass rows: comparison ledger below keeps provisional changes
    # distinct from G complete masses and H unfinished support replacement.
    s['caster']['reference_fitting_height_mm'] = d['caster']['added_height_mm']
    s['caster']['retainer_allowance_mm'] = d['caster']['stem_length_mm'] - s['caster']['plate_mm']
    return c, s


def caster_stack(h, d):
    s, c = h['caster'], d['caster']
    bottom = s['bare_height_mm'] + c['added_height_mm']
    plate_top = bottom + s['plate_mm']
    washer_top = plate_top + c['washer_thickness_reserve_mm']
    nut_top = washer_top + c['nut_height_reserve_mm']
    tip = bottom + c['stem_length_mm']
    hardware_top = max(tip, nut_top)
    return dict(plate_bottom_mm=bottom, plate_top_mm=plate_top,
        washer_top_mm=washer_top, nut_top_mm=nut_top, thread_tip_mm=tip,
        thread_projection_mm=tip-nut_top, hardware_top_mm=hardware_top,
        overhead_mm=c['overhead_z_mm'], overhead_gap_mm=c['overhead_z_mm']-hardware_top,
        bare_plus_stem_g=c['bare_mass_g'] + c['stem_mass_g'],
        stem_pairing_confirmed=False, caster_pullout_retention_verified=False)


def caster_beam(h,d):
    s=caster_stack(h,d);k=h['caster'];m=h['material']
    section=support.plate_section(k['saddle_width_mm'],k['plate_mm'])
    length=k['rear_attachment_y_mm']-k['centres_xy_mm']['vacuum'][1]
    # Ground force acts below the plate centroid, including the new fitting.
    moment=k['horizontal_load_n']*(s['plate_bottom_mm']+k['plate_mm']/2)
    force=k['factored_vertical_load_n'];inertia=section['inertia_mm4'];e=m['aluminum_e_mpa']
    stress=(force*length+moment)*section['c_mm']/inertia
    deflection=force*length**3/(3*e*inertia)+moment*length**2/(2*e*inertia)
    return dict(stress_mpa=stress,deflection_mm=deflection,
        passes=stress<=m['aluminum_bending_screen_mpa'] and deflection<=m['deflection_screen_mm'],
        scope='Gross 40 x 3 mm strip, rigid root, 100 N vertical plus 25 N fore/aft. Holes, bolted root and caster plug retention unqualified.')


def retainer(d, h, bottom):
    x, y = h['caster']['centres_xy_mm'][bottom]
    s = caster_stack(h,d); dia=d['caster']['tool_diameter_reserve_mm']
    return dict(id='I_caster_top_service_space', min=[x-dia/2,y-dia/2,s['plate_top_mm']],
                size=[dia,dia,s['overhead_mm']-s['plate_top_mm']], shape='box')


def body_parts(c, h, d, bottom):
    omitted=set(h['carrier']['removed_if_closed']) | {'pod_left','pod_right','caster','wheel_left','wheel_right'}
    parts=[p for p in base.reference_parts(c,bottom) if not p.get('parent')
           and p['shape']!='distributed' and p['id'] not in omitted]
    # Include a conservative full cap-height slab for HEIGHT checks only. Its
    # scanner opening is not a solid obstruction in the interference check.
    parts.append(dict(id='I_cap_height_bound', min=[2.5,2.5,d['cap_max_roof_z_mm']-2],size=[270,270,2]))
    return parts + support.stock(h,bottom) + [retainer(d,h,bottom)]


def height_at(parts, h, left, right, caster):
    n = support.support_plane(h,left,right,caster)
    best=(-math.inf,None)
    for p in parts:
        q=[base.hi(p)[i] if n[i]>=0 else p['min'][i] for i in range(3)]
        height=n[0]*(q[0]-caster[0])+n[1]*(q[1]-caster[1])+n[2]*q[2]
        if height>best[0]:best=(height,p['id'])
    return best, n


def height_screen(c, h, d, travel_step=2.5, heading_step=5):
    """Each bottom has its own geometry; finite sampling is not a proof."""
    w=h['wheel']; lo=-w['droop_candidate_mm']; hi=w['bump_mm']
    count=round((hi-lo)/travel_step)
    travel=[lo+(hi-lo)*i/count for i in range(count+1)]
    result={}
    for bottom in BOTTOMS:
        parts=body_parts(c,h,d,bottom);cx,cy=h['caster']['centres_xy_mm'][bottom]
        worst=dict(max_height_mm=-math.inf);poses=0
        for left,right,heading in itertools.product(travel,travel,range(0,360,heading_step)):
            a=math.radians(heading);trail=c['traction']['caster_trail_mm']
            caster=[cx+trail*math.cos(a),cy+trail*math.sin(a)]
            (height,id),n=height_at(parts,h,left,right,caster);poses+=1
            if height>worst['max_height_mm']:
                worst=dict(max_height_mm=height,part=id,left_travel_mm=left,right_travel_mm=right,
                           caster_heading_deg=heading,normal=n)
        worst.update(sampled_poses=poses,reserved_height_mm=worst['max_height_mm']+d['height_reserve_mm'],
            passes_reserved_screen=worst['max_height_mm']+d['height_reserve_mm']<=c['limits']['body_mm'][2])
        result[bottom]=worst
    return result


def changed_conflicts(c,h,d,bottom):
    parts=base.reference_parts(c,bottom)
    changed={'lidar','I_lidar_mount','top_port','vac_bin_upper','blower_bay','mop_pump','exhaust'}
    parts=[p for p in parts if not p.get('parent') and p['shape']!='distributed']
    errors=[]
    for a,b in itertools.combinations(parts,2):
        if (a['id'] in changed or b['id'] in changed) and base.overlap(a,b):
            errors.append(a['id']+' / '+b['id'])
    for p in parts:
        if p['id']!='caster' and base.overlap(retainer(d,h,bottom),p):
            errors.append('caster upper service space / '+p['id'])
    errors += support.stock_conflicts(c,h,bottom)
    return errors


def optics(c,d):
    l=d['lidar'];bottom=l['min_mm'][2]+l['optical_window_bottom_mm']
    # Full surrounding allocations, irrespective of azimuth: deliberately
    # stronger than checking only a ray through the nominal optical centre.
    surrounding=[p for p in c['parts'] if p['module'] in ('core','cap')
                 and not p.get('parent') and p['shape']!='distributed'
                 and p['id'] not in ('lidar','I_lidar_mount')]
    blocker=max(surrounding,key=lambda p:base.hi(p)[2])
    obstacle=max(base.hi(blocker)[2],d['cap_max_roof_z_mm'])
    gap=bottom-obstacle
    return dict(window_bottom_mm=bottom,beam_centre_mm=l['min_mm'][2]+l['beam_height_mm'],
        highest_surrounding_part=blocker['id'],surrounding_top_mm=obstacle,
        clear_gap_mm=gap,after_sensor_tolerance_mm=gap-l['drawing_tolerance_mm'],
        passes=gap-l['drawing_tolerance_mm']>=d['optical_clearance_min_mm'],
        scope='Ground cap and core vertical clearance only. Lift frame, connector cable loops, window covers and complete optical cone remain unqualified.')


def study(g,h,d):
    c,s=configured(g,h,d);height=height_screen(c,s,d)
    prior=height_screen(g,h,d)
    # Independent fine local sweep around coarse maxima catches displaced peaks
    # without pretending that a sampled grid proves all possible attitudes.
    refined={}
    for bottom,row in height.items():
        parts=body_parts(c,s,d,bottom);cx,cy=s['caster']['centres_xy_mm'][bottom]
        best=row.copy();count=0
        def near(v,step,lo,hi):return sorted(set(max(lo,min(hi,v+i*step)) for i in range(-4,5)))
        for left,right,heading in itertools.product(
            near(row['left_travel_mm'],.25,-2.5,10),near(row['right_travel_mm'],.25,-2.5,10),
            near(row['caster_heading_deg'],1,-360,720)):
            a=math.radians(heading);trail=c['traction']['caster_trail_mm']
            (v,id),n=height_at(parts,s,left,right,[cx+trail*math.cos(a),cy+trail*math.sin(a)])
            count+=1
            if v>best['max_height_mm']:best.update(max_height_mm=v,part=id,left_travel_mm=left,
                    right_travel_mm=right,caster_heading_deg=heading%360,normal=n)
        best.update(local_poses=count,reserved_height_mm=best['max_height_mm']+d['height_reserve_mm'])
        best['passes_reserved_screen']=best['reserved_height_mm']<=c['limits']['body_mm'][2]
        refined[bottom]=best
    stack=caster_stack(s,d);bins=frame.bins(c,frame.read())
    port=next(p for p in c['parts'] if p['id']=='top_port')
    protection=next(p for p in c['parts'] if p['id']=='pack_protection')
    caster_est=stack['bare_plus_stem_g']+d['caster']['upper_fasteners_mass_reserve_g']+d['caster']['secondary_retention_mass_reserve_g']
    bare_delta=d['lidar']['bare_mass_g']-g['hardware']['lidar']['mass_g'][1]
    return dict(revision=d['revision'],config=d,configured_layout=c,configured_support=s,
        height_before=prior,height_after=refined,nominal_lidar_top_mm=base.hi(next(p for p in c['parts'] if p['id']=='lidar'))[2],
        optics=optics(c,d),caster_stack=stack,caster_beam=caster_beam(s,d),bins=bins,
        port_to_pack_protection_gap_mm=port['min'][2]-base.hi(protection)[2],
        conflicts={b:changed_conflicts(c,s,d,b) for b in BOTTOMS},
        mass_comparison=dict(bare_lidar_delta_g=bare_delta,new_mount_allowance_g=d['lidar']['mount_allowance_g'],
            caster_installation_reserve_g=caster_est,caster_delta_from_G_g=caster_est-g['hardware']['caster']['mass_g'][1],
            illustrative_net_delta_g=bare_delta+d['lidar']['mount_allowance_g'][1]+caster_est-g['hardware']['caster']['mass_g'][1],
            complete_G_masses_g={b:base.assembly(g,b)['mass_g'][1] for b in BOTTOMS},
            note='Not installed masses: all G supports retained; additional mount is conservative pending allocation within existing core structure. H joints and actual retainers remain incomplete.'),
        input_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [ROOT/'config'/n for n in ('system_design.json','core_partition.json','frame_joints.json','floor_support.json','height_mounting.json')]},
        continuous_envelope_proven=False,physical_validation=False,fabrication_release=False)


def report(r):
    s=r['caster_stack'];o=r['optics'];m=r['mass_comparison'];d=r['config']
    lines=['# I — height and caster mounting','',
        'A C1 lidar candidate and revised caster mounting space pass the sampled packaging screens while preserving H’s 10 mm bump and 2.5 mm candidate droop. This is an overlay; G remains the complete mass baseline. No print, order or flight release.','',
        '## Suspension height','',
        f"Lidar nominal top: **{r['nominal_lidar_top_mm']:.1f} mm**. The 2 mm project reserve is added after solving support attitude; it is not yet a tolerance stack. Each bottom uses its own geometry, including the raised components and a conservative cap-height bound.",'',
        '| Bottom | A1 sampled max | C1 sampled max | C1 + 2 mm reserve | 180 mm screen |',
        '|---|---:|---:|---:|---|']
    for b in BOTTOMS:
        a,z=r['height_before'][b],r['height_after'][b]
        lines.append(f"| {b} | {a['max_height_mm']:.3f} | {z['max_height_mm']:.3f} | {z['reserved_height_mm']:.3f} | {'Pass' if z['passes_reserved_screen'] else 'FAIL'} |")
    lines += ['', 'The three-support model uses spherical drive-wheel proxies and an ideal caster contact point. It samples independent wheel travel and swivel headings, then refines around each maximum. It does not establish a continuous extremum, spring equilibrium, threshold traversal, loaded tire shape or body clearances on irregular floors. Full travel remains a mechanical design candidate.','',
        '## Lidar and lift connector','',
        'C1 reference: 55.6 × 55.6 × 41.3 mm, 110 g, four M2.5 holes on a 43 mm square; screw insertion ≤4 mm. The manufacturer drawing gives ±0.2 mm dimensional tolerance. The mount reserves 64 × 64 × 9.4 mm above the core; screws and rail attachments are still to detail. Bare sensor is 60 g lighter than the 170 g A1 reference. These are reference specifications, not measurements of supplied hardware. [SLAMTEC drawing, rev1.1, pp15/18]('+d['sources']['c1_datasheet']+').','',
        'C1 is a candidate replacement, not an equivalent-specification claim: 5000 samples/s and a typical 10 Hz sweep, versus the A1 reference’s 8000 samples/s and 5.5 Hz. C1’s nominal 0.72° spacing is about 38 mm at 3 m; keep the near-obstacle sensors, camera and cliff sensing. Mapping and dog/furniture detection still need validation. [C1 manufacturer page]('+d['sources']['c1_current_page']+'), [A1 specification]('+d['sources']['a1']+').','',
        'The C1 electrical reference uses 5 V, 230 mA typical running and 800 mA typical startup; reserve startup headroom rather than sizing only to 1.15 W. Use its 3.3 V UART at 460800 baud with a supported driver. Keep existing power budgets until integrated measurements. [Manufacturer electrical tables, pp13–14]('+d['sources']['c1_datasheet']+').','',
        f"The existing lift-connector reservation rotates from 78 × 32 × 35 to 78 × 35 × 32 mm and moves to [193, 88, 122.5] mm. Its volume is preserved. This leaves {r['port_to_pack_protection_gap_mm']:.1f} mm above pack protection and {o['clear_gap_mm']:.1f} mm below the entire rotating optical enclosure ({o['after_sensor_tolerance_mm']:.1f} mm after the sensor drawing tolerance). The nominal beam is at z={o['beam_centre_mm']:.1f} mm. All four mechanical seats stay at z=124.1 mm; the connector carrier, cap opening, top-module mating route and harness must be revised to this location.",'',
        'The old A1 cannot simply move downward enough: battery top is 121 mm; lowering its 124.1 mm base by the needed several millimetres consumes the mounting clearance. C1 with the old tall port also fails the unobstructed-window screen. The new geometry therefore depends on both the lidar and connector layout changes. Do not cover the optical enclosure with an unqualified transparent shroud. This pass checks the ground cap; lift-frame visibility remains open.','',
        '## Caster stack','',
        'Use S70-8x15 / 8 (EAN 4031582322040, 0007193200) as the fitting candidate. TENTE specifies M8 × 15, 6 mm added height and 20 g. It replaces the unsupported 2.5 mm fitting assumption. Confirm the exact pairing with 5940UAP050L51-8 before ordering. [TENTE fitting datasheet]('+d['sources']['caster_stem']+').','',
        '| Feature | z above reference floor |','|---|---:|',
        f"| Bare caster | 50.5 mm |",
        f"| Fitting shoulder / plate underside | {s['plate_bottom_mm']:.1f} mm |",
        f"| 3 mm plate top | {s['plate_top_mm']:.1f} mm |",
        f"| Reserved washer / nut tops | {s['washer_top_mm']:.1f} / {s['nut_top_mm']:.1f} mm |",
        f"| Full uncut threaded stem tip | {s['thread_tip_mm']:.1f} mm |",
        f"| Equipment underside | {s['overhead_mm']:.1f} mm |",'',
        f"Reserve a 24 mm diameter service pocket above the plate. The uncut stem, not the nut, sets the top at {s['hardware_top_mm']:.1f} mm, leaving {s['overhead_gap_mm']:.1f} mm overhead. Washer ≤1.6 mm and locking nut ≤8 mm are fastener procurement limits; there is {s['thread_projection_mm']:.1f} mm nominal thread beyond that stack. Verify actual tolerances, locking engagement, tool access with equipment removed and fitting shoulder width before release.",'',
        'The upper nut only retains the fitting to our plate. It does not establish retention of the caster on the fitting’s plug end during lifting. Manufacturer confirmation of that joint or a positively captive replacement remains required. The rolling load rating is not a pull-out rating. No modification of the caster’s plastic body is proposed.','',
        f"Including the taller ground-to-plate moment arm, the gross 40 × 3 mm saddle screens at {r['caster_beam']['stress_mpa']:.1f} MPa and {r['caster_beam']['deflection_mm']:.3f} mm deflection under H's 100 N vertical / 25 N fore-aft case. These remain strip-beam estimates with a rigid root; the bolted angles and holes are not qualified.",'',
        '## Nearby equipment','',
        'Raise the vacuum bin bridge floor from 62 to 74 mm, keeping its top at 94 mm. A flat chamber floor avoids a new hair-catching pocket. Raise the entire blower/plenum and its exhaust by 10 mm in vacuum/sofa bottoms, and the mop pump by 8 mm. Their revised undersides are 74 mm. The mop tank, sofa bin, filter, cleaning head and wheel travel stay at their existing allocations. Duct transitions and pump hoses must follow these changes.','',
        '| Bottom | Internal volume after 15% reserve | Required target |','|---|---:|---:|']
    for b,v in r['bins'].items():lines.append(f"| {b} | {v['after_reserve_l']:.3f} L | {v['target_l']:.2f} L |")
    lines += ['', 'These are conservative separate inner-box screens with 3 mm walls; seals, baffles and evacuation still need detailed validation. No cleaning-capacity reduction below the existing targets is credited.','',
        '## Mass and outstanding work','',
        f"Bare lidar delta: {m['bare_lidar_delta_g']:+.0f} g. Add a provisional {m['new_mount_allowance_g'][1]} g mount reserve. Caster installation reserve rises to {m['caster_installation_reserve_g']:.0f} g including 20 g for unresolved secondary retention; this is {m['caster_delta_from_G_g']:+.0f} g relative to G. The illustrative combined delta is only **{m['illustrative_net_delta_g']:+.0f} g**, before completing the H support assembly. It is not a new complete robot mass or a flight-endurance improvement.",'',
        'Next detail the moving motor trays, spring cups, travel stops, wheel-drop switches and rail/seat joints. Resolve caster retention and exact connector mating before fabrication. Complete cable routes, mount tolerances and the actual cap shell before declaring the full envelope verified.','',
        'The interactive HTML and FreeCAD/STEP files are review artifacts. Bay outlines are allocations; mounting geometry is not fabrication-ready.','']
    return '\n'.join(lines)


def write_viewer(r):
    d=r['config'];c=r['configured_layout'];s=r['configured_support']
    data=dict(before=r['height_before'],after=r['height_after'],stack=r['caster_stack'],optics=r['optics'],
        parts={b:[p for p in base.reference_parts(c,b) if not p.get('parent') and p['shape']!='distributed']+
               support.stock(s,b)+[retainer(d,s,b)] for b in BOTTOMS})
    template=(ROOT/'design/system/height_mounting_viewer.html').read_text()
    return template.replace('__DATA__',json.dumps(data).replace('</','<\\/'))


def main():
    r=study(support.baseline(),support.read(),read());OUT.mkdir(exist_ok=True)
    (OUT/'height_mounting.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'height_mounting.md').write_text(report(r))
    (OUT/'height_mounting.html').write_text(write_viewer(r))
    print(json.dumps({k:r[k] for k in ('height_after','caster_stack','optics','conflicts','bins','mass_comparison')},indent=2))
    if (any(r['conflicts'].values()) or not r['optics']['passes'] or not r['caster_beam']['passes']
            or any(not x['target_screen_pass'] for x in r['bins'].values())
            or any(not x['passes_reserved_screen'] for x in r['height_after'].values())):
        raise SystemExit('I candidate has unresolved packaging screen failures')


if __name__=='__main__':main()
