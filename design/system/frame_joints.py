"""G frame candidate: explicit metal load paths, joint screens and full masses."""
from copy import deepcopy
import csv
import hashlib
import html
import json
import math
from pathlib import Path

import build as base
import airborne_study as air
import core_partition as partition

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'


def read():
    return json.loads((ROOT/'config/frame_joints.json').read_text())


def flange_screen(force_n, width_mm, span_mm, thickness_mm, e_mpa):
    """Simply supported strip with central point load; no hole/notch analysis."""
    i=width_mm*thickness_mm**3/12
    return dict(stress_mpa=force_n*span_mm/4*(thickness_mm/2)/i,
        deflection_mm=force_n*span_mm**3/(48*e_mpa*i),second_moment_mm4=i)


def stock_parts(c,d):
    parts=[];k=d['corner'];r=d['rail'];a=d['clip'];rho=d['material']['density_g_mm3']
    def add(id,xyz,size,**extra):
        p=dict(id=id,module='core',label=id.replace('_',' '),min=xyz,size=size,shape='box',
            group='structure',hardware=[],notes='G reference; supplied radii, drilled holes, fasteners and tolerance stack remain to qualify.',**extra)
        p['stock_mass_g']=math.prod(size)*rho
        parts.append(p);return p
    for i,(x,y) in enumerate(c['interfaces']['lock_centres_xy_mm']):
        lo=[x-k['cut_length_x_mm']/2,y-k['outer_y_mm']/2,k['bottom_seat_z_mm']]
        w=k['cut_length_x_mm'];dep=k['outer_y_mm'];h=k['outer_z_mm'];t=k['wall_mm']
        add(f'G_corner_{i}_bottom',lo,[w,dep,t],drill_axis='z',drill_diameter=k['stud_entry_diameter_mm'],drill_center=[x,y])
        add(f'G_corner_{i}_top',[lo[0],lo[1],lo[2]+h-t],[w,dep,t],drill_axis='z',drill_diameter=k['stud_entry_diameter_mm'],drill_center=[x,y])
        add(f'G_corner_{i}_front',[lo[0],lo[1],lo[2]+t],[w,t,h-2*t])
        add(f'G_corner_{i}_rear',[lo[0],lo[1]+dep-t,lo[2]+t],[w,t,h-2*t])
        pad=k['bearing_pad_mm'];lift=pad[2]
        for end,z in [('bottom',lo[2]+t),('top',lo[2]+h-t-lift)]:
            p=add(f'G_lock_pad_{i}_{end}',[x-pad[0]/2,y-pad[1]/2,z],pad,
                drill_axis='z',drill_diameter=k['stud_entry_diameter_mm'],drill_center=[x,y])
            p['stock_mass_g']=0 # Seats and retainers are in the unchanged lock mechanism budget.
        # Twenty-millimeter blanks contain both openings and stay inside the
        # body during the full outward stroke; retain the mechanism mass budget.
        for end,z in [('bottom',lo[2]+t+lift+k['draw_gap_mm']),
                      ('top',lo[2]+h-t-lift-k['draw_gap_mm']-k['slider_size_mm'][2])]:
            direction=-1 if x<137.5 else 1
            p=add(f'G_lock_{i}_{end}',[x-direction*k['release_travel_mm']/2-k['slider_size_mm'][0]/2,y-k['slider_size_mm'][1]/2,z],k['slider_size_mm'],
                shape_override='slider',stud_center=[x,y],release_direction=direction)
            p['stock_mass_g']=0 # Entire mechanism remains in the existing core_locks budget.
            p['hardware']=[dict(id='core_locks',qty=1/8)]
    for name,xyz,size in [
        ('front',[10,4.475,r['z_mm']],[r['front_length_mm'],r['width_mm'],r['height_mm']]),
        ('rear',[10,270.525-r['width_mm'],r['z_mm']],[r['front_length_mm'],r['width_mm'],r['height_mm']]),
        ('left',[2.5,20,r['z_mm']],[r['width_mm'],r['side_length_mm'],r['height_mm']]),
        ('right',[272.5-r['width_mm'],20,r['z_mm']],[r['width_mm'],r['side_length_mm'],r['height_mm']])]:
        add('G_rail_'+name,xyz,size)
    # Four angle clips join side rails to the outer fore/aft faces of the tubes.
    for i,(x,y) in enumerate(c['interfaces']['lock_centres_xy_mm']):
        left=x<137.5;front=y<137.5;t=a['wall_mm'];leg=a['leg_mm'];z=r['z_mm'];h=a['length_z_mm']
        xx=2.5+r['width_mm'] if left else 272.5-r['width_mm']-leg
        yy=y+k['outer_y_mm']/2 if front else y-k['outer_y_mm']/2-leg
        add(f'G_clip_{i}_x',[xx if left else xx+leg-t,yy,z],[t,leg,h])
        add(f'G_clip_{i}_y',[xx+t if left else xx,yy if front else yy+leg-t,z],[leg-t,t,h])
    return parts


def configured(f,d):
    c=deepcopy(f);delta=d['corner']['bottom_seat_z_mm']+d['corner']['outer_z_mm']-c['interfaces']['core_top_seat_z_mm']
    c['parts']=[p for p in c['parts'] if not p['id'].startswith('core_rail_')]
    for p in c['parts']:
        p['hardware']=[h for h in p['hardware'] if h['id'] not in ('core_metal','core_locks')]
        if p['module']=='core' and p['min'][2]>=123:p['min'][2]+=delta
        if p['module']=='cap':p['min'][2]+=delta
        if p['id'] in ('pi_bay','pi_reference'):p['min'][0]+=d['layout']['pi_shift_x_mm']
        if p['id']=='pack_protection':p['min'][0]+=d['layout']['pack_protection_shift_x_mm']
        if p['id']=='floor_front_stiffener':
            p['min'][0]+=3;p['size'][0]-=3
            p['notes']+=' G trims 3 mm from the left end for slider clearance; the F stock mass is retained conservatively.'
        # Keep contiguous chamber edges and actual filter size. Reserve targets
        # are verified separately; these are not measured usable capacities.
        if p['id'] in ('vac_bin_left','mop_tank','extension_bin','filter_bay'):
            shift=d['layout']['rear_tool_inner_edge_x_mm']-p['min'][0]
            p['min'][0]+=shift;p['size'][0]-=shift
        if p['id']=='filter_reference':p['min'][0]+=d['layout']['filter_shift_x_mm']
        if p['id']=='extension_bin':p['size'][2]+=d['layout']['sofa_bin_extra_height_mm']
        if p['id']=='extension_drive':p['min'][1]+=d['layout']['sofa_feed_drive_shift_y_mm']
        if p['id']=='drive_control':
            p['size']=[58,53,30]
            p['hardware']=[h for h in p['hardware'] if h['id']!='bottom_mcu']
            p['label']='RoboClaw carrier / separate bottom supervisor'
        if p['id']=='bottom_mcu_reference':
            p['min']=[217,26,62];p['parent']='G_bottom_supervisor'
    c['parts'].append(dict(id='G_bottom_supervisor',module='drive',label='Separate bottom supervisor bay',
        min=[215,25,56],size=[32,57,30],shape='box',group='logic',hardware=[dict(id='bottom_mcu',qty=1)],
        notes='Existing full board size retained; split from the RoboClaw carrier to clear the replacement bridge route'))
    def hardware(id,mass,basis):
        c['hardware'][id]=dict(name=id.replace('_',' '),mass_g=mass,mass_basis=basis,
            source=d['corner']['stock_source'] if id.startswith('G_corner_') else 'config/frame_joints.json; rail/clip/fastener procurement open',procurement='design_candidate',measured_mass_g=None,
            notes='No purchase or fabrication release; mass is an unmeasured estimate')
    for p in stock_parts(c,d):
        if p['stock_mass_g']:
            hardware(p['id'],[p['stock_mass_g']*v for v in d['stock_mass_factors']],
                'Gross stock volume times density; drilled material is not credited')
            p['hardware']=[dict(id=p['id'],qty=1)]
        c['parts'].append(p)
    hardware('G_frame_fasteners',d['joint_fasteners_g'],'24 M3 screw/nut/washer sets: 8 rail-to-tube, 16 clip joints; 30 g nominal installation allowance')
    c['parts'].append(dict(id='G_frame_fasteners',module='core',label='G frame fasteners',
        min=[0,0,86],size=[275,275,38.1],shape='distributed',group='structure',
        hardware=[dict(id='G_frame_fasteners',qty=1)],notes='Actual fastener lengths and head/lock clearances remain to qualify'))
    c['interfaces']['core_top_seat_z_mm']+=delta
    c['limits']['top_mate_z_mm']+=delta
    c['interfaces']['G_mechanical_revision']='Top seat 124.1 mm; core-side sliders release outward in X. Prior top-seat fixtures are incompatible without adaptation.'
    return c


def bins(c,d):
    p={p['id']:p for p in c['parts']};wall=d['layout']['minimum_bin_wall_mm'];reserve=d['layout']['bin_internal_reserve_fraction']
    result={}
    for name,ids in dict(vacuum=['vac_bin_left','vac_bin_front','vac_bin_upper'],mop=['mop_tank'],low=['extension_bin']).items():
        inner=sum(math.prod(max(0,v-2*wall) for v in p[id]['size']) for id in ids)/1e6
        target=d['layout']['bin_target_l'][name]
        result[name]=dict(inner_box_l=inner,after_reserve_l=inner*(1-reserve),target_l=target,
            target_screen_pass=inner*(1-reserve)>=target,usable_capacity_qualified=False)
    return result


def bridge_conflicts(c,d,bottom):
    bridge=d['floor_bridge_candidate']
    return [p['id'] for p in base.reference_parts(c,bottom) if not p.get('parent') and p['shape']!='distributed'
            and not p['id'].startswith('floor_') and base.overlap(bridge,p)]


def slider_sweep_errors(parts,d):
    errors=[]
    for slider in [p for p in parts if p.get('shape_override')=='slider']:
        sweep=deepcopy(slider);travel=d['corner']['release_travel_mm']
        if slider['release_direction']<0:sweep['min'][0]-=travel
        sweep['size'][0]+=travel
        for p in parts:
            if p['id']==slider['id'] or p['shape']=='distributed' or p.get('parent'):continue
            if base.overlap(sweep,p):errors.append(slider['id']+' / '+p['id'])
    return errors


def corner_radius_screen(d):
    k=d['corner'];inner=k['outer_y_mm']-2*k['wall_mm'];r=k['inside_radius_screen_mm']
    side=(inner-k['slider_size_mm'][1])/2;z=k['bearing_pad_mm'][2]
    # Loaded position: draw gap is closed, but the metal bearing pad remains.
    radial_margin=r-math.hypot(max(0,r-side),max(0,r-z))
    flat_margin=(inner-2*r-k['bearing_pad_mm'][1])/2
    return dict(assumed_inside_radius_mm=r,loaded_slider_radius_margin_mm=radial_margin,
        pad_to_fillet_flat_margin_mm=flat_margin,passes=radial_margin>=0 and flat_margin>=0,
        delivered_profile_qualified=False)


def study(f,d,ad):
    c=configured(f,d);k=d['corner'];m=d['material'];load=d['loads'];stock=stock_parts(c,d)
    current=base.assembly(f,'vacuum');own_mass=sum(row['mass_g'][1] for row in current['rows'] if row['module'] in ('core','battery'))
    flange=[]
    for sharing in load['load_sharing_cases']:
        for t in k['wall_sensitivity_mm']:
            row=flange_screen(load['factored_axial_n']/sharing,k['effective_flange_width_mm'],k['outer_y_mm']-2*t,t,m['elastic_modulus_mpa'])
            row.update(anchors_sharing=sharing,thickness_mm=t,force_n=load['factored_axial_n']/sharing,
                       passes_stress_screen=row['stress_mpa']<=m['screen_bending_allowable_mpa'])
            flange.append(row)
    rail_load=own_mass/1000*base.G*load['core_equipment_acceleration_g']/load['core_equipment_supporting_rails']
    rr=d['rail'];rail=flange_screen(rail_load,rr['width_mm'],load['rail_effective_span_mm'],rr['height_mm'],m['elastic_modulus_mpa'])
    rail.update(force_n=rail_load,passes=rail['stress_mpa']<=m['screen_bending_allowable_mpa'] and rail['deflection_mm']<=load['rail_deflection_screen_mm'])
    cases={}
    for bottom in ('vacuum','mop','low'):
        before=base.assembly(f,bottom);after=base.assembly(c,bottom)
        cases[bottom]=dict(before=partition.summarize(before),after=partition.summarize(after),assembly=after,
            checks=base.allocation_checks(c,after['parts'],bottom),withdrawal_errors=partition.withdrawal_errors(after['parts']),
            slider_sweep_errors=slider_sweep_errors(after['parts'],d),
            bridge_conflicts_before=bridge_conflicts(f,d,bottom),bridge_conflicts=bridge_conflicts(c,d,bottom))
    return dict(revision=d['revision'],config=d,model_config=c,ground=cases,
        airborne_before=air.study(f,ad),airborne_after=air.study(c,ad),bins=bins(c,d),
        stock_mass_g=sum(p['stock_mass_g'] for p in stock),
        installed_frame_mass_g=sum(p['stock_mass_g'] for p in stock)+d['joint_fasteners_g'][1],
        old_frame_mass_g=f['hardware']['core_metal']['mass_g'][1],
        flange_screens=flange,rail_screen=rail,corner_radius_screen=corner_radius_screen(d),new_top_seat_mm=c['interfaces']['core_top_seat_z_mm'],
        flange_average_ligament_shear_mpa=load['factored_axial_n']/min(load['load_sharing_cases'])/((k['cut_length_x_mm']-k['stud_entry_diameter_mm'])*k['wall_mm']),
        ground_height_mm=max(base.hi(p)[2] for p in cases['vacuum']['assembly']['parts'] if p['module']!='lift'),
        unlocked_slider_x_envelope_mm=[min(p['min'][0]+min(0,p['release_direction']*k['release_travel_mm']) for p in stock if p.get('shape_override')=='slider'),
                                      max(base.hi(p)[0]+max(0,p['release_direction']*k['release_travel_mm']) for p in stock if p.get('shape_override')=='slider')],
        battery_exchange_errors=base.battery_exchange_metrics(c)['geometry_errors'],
        input_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [ROOT/'config/system_design.json',ROOT/'config/airborne_dusting.json',ROOT/'config/core_partition.json',ROOT/'config/frame_joints.json']},
        fabrication_release=False,flight_qualified=False)


def report(r):
    delta=r['installed_frame_mass_g']-r['old_frame_mass_g'];d=r['config'];k=d['corner']
    a=r['airborne_after']['cases']['quad10'];old=r['airborne_before']['cases']['quad10']
    s=['# Revision G — core frame and joint candidate','',
        '**This pass establishes a more explicit load path, not a claimed weight saving.** The nominal metal frame changes from a 145 g allowance to '+f"{r['installed_frame_mass_g']:.1f} g including mounting hardware ({delta:+.1f} g). The 160 g printed trays/ribs, 130 g locks and all floor-frame/carrier allowances remain. These are estimates, not fabricated or proof-tested parts.",'',
        '## Construction and load path','',
        'Use four 18 mm slices of 1 × 1.5 × 0.125 inch rectangular 6061-T6 tube at the existing [14/261, 14/261] mm coupling centers. Each slice has two horizontal faces joined by two continuous metal walls. Opposed module studs load steel sliding locks against the inside faces; the walls connect the upper and lower interfaces. Printed guides locate sliders and equipment; they are not the primary axial connection between modules.','',
        'Use a 20 × 18 × 2 mm steel slider with 8 mm travel through the open tube ends. Front and rear locks on the left release toward −X; right locks release toward +X. The shorter blank contains a 5 mm capture opening connected to a 9.5 mm entry opening and remains inside the 275 mm body during release. Tube internal depth is 19.05 mm, leaving 0.525 mm nominal clearance per side. An 18 × 12 × 2 mm metal bearing pad holds each slider clear of the tube corner radii even when the 0.5 mm draw gap closes.','',
        f"With an assumed 3.175 mm inside radius, the loaded slider corner has {r['corner_radius_screen']['loaded_slider_radius_margin_mm']:.3f} mm radial clearance and the pad has {r['corner_radius_screen']['pad_to_fillet_flat_margin_mm']:.3f} mm clearance to the curved region. This is a radius/tolerance screen, not verified stock. The reference CAD uses sharp tube walls; actual profile radii must be checked. The existing 130 g lock allowance already includes seats: each mechanism retains 16.25 g, including its roughly 5.7 g steel blank and 1.2 g gross aluminum pad. No weight credit is taken for the shorter slider blank. Pad keepers, printed end retainers/actuation guides, wear liners, pawls, springs, fastening and sensed travel must fit the remaining allowance or increase the ledger. The slot geometry is not a completed latch.",'',
        f"Ground envelope remains 275 × 275 × {r['ground_height_mm']:.1f} mm, including the full modeled slider stroke. The 38.1 mm tube height moves the top seat from 123 to {r['new_top_seat_mm']:.1f} mm; LiDAR and upper core allocations rise 1.1 mm. Preserve the 180 mm overall limit. Sliders release only at a supported station, with motion/power inhibited. Manufacturing tolerance and station actuator access still need validation.",'',
        'Four 12.7 × 1.5875 mm aluminum strips stand on edge between the corner blocks: two 255 mm and two 235 mm lengths. Four 12.7 mm angle clips connect the side strips to the tube blocks. The front/rear strips lap the inside faces of the tube walls. Reserve 24 M3 screw/nut/washer sets: two per direct rail end, four per angle clip. Flat joint faces and through fasteners avoid a precision-machined central frame. Confirm head clearance, hole layout, tool access and stock radii before release.','',
        'Stock can be cut by the supplier, or with a suitable metal-cutting saw and vise. The tube only needs crosscuts and drilled entry/mounting holes; no longitudinal milling, welding or sheet-metal brake is assumed. A countersink is needed where outward screw heads would use the side clearance. Tool ownership and exact cutting/drilling method should be settled at fabrication release, not by ordering a test harness now.','',
        '[Tube stock reference](https://www.onlinemetals.com/en/buy/aluminum/1-x-1-5-x-0-125-aluminum-rectangle-tube-6061-t6-extruded/pid/14469). This is a catalog dimensional reference, not verified delivered stock. [Hydro alloy data](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf) lists 240 MPa minimum yield for its 6061-T6 extrusions. The model uses project screening limits of 120 MPa bending, 80 MPa shear and an approximate 69 GPa elastic modulus; these are not certification allowables or proof that other tempers are equivalent.','',
        '## Mechanical screens','',
        'Keep the inherited 600 N factored axial requirement. Check 150 N per corner with four-way sharing and 300 N with two-way sharing. The latter screens unequal load; it does not permit a robot to lift with missing/unlocked joints. Do not multiply the already factored 600 N by the separate equipment acceleration again.','',
        'For flange bending, treat a 10 mm effective strip as simply supported between the tube walls with a central load: I = b t³ / 12, σ = F L t / (8 I), δ = F L³ / (48 E I). This excludes drilled-hole stress concentrations, corner radii, load introduction, prying, wear and fatigue. It compares candidate sections; it does not qualify the joint.','',
        '| Tube wall | 300 N flange stress | Bending screen |','|---|---:|---|']
    for row in r['flange_screens']:
        if row['anchors_sharing']==2:s.append(f"| {row['thickness_mm']:.3f} mm | {row['stress_mpa']:.1f} MPa | {'Pass' if row['passes_stress_screen'] else 'Fail'} |")
    s += ['',f"The independent rail check applies the core/cartridge/cells at 3 g, shared across two rails, over a 247 mm support span: {r['rail_screen']['stress_mpa']:.1f} MPa and {r['rail_screen']['deflection_mm']:.2f} mm. This screens the equipment support only; the 600 N module load travels through the corner blocks. Torsion and joint stiffness still require analysis/test.",'',
        f"The average shear screen over the aluminum remaining beside the 9.5 mm entry hole is {r['flange_average_ligament_shear_mpa']:.1f} MPa at 300 N, below the 80 MPa project screen. This does not calculate notch stress, pull-through, prying or fatigue. The steel slider/pawl and supplied mushroom head must be checked separately.",'',
        '## Packaging changes and preserved functions','',
        'The Pi bay and board shift 2 mm left to clear the right front slider. The fixed pack-protection bay shifts 3 mm inward to clear the side rail. The F carrier front stiffener is trimmed 3 mm at its left end, retaining its previous mass allowance. Rear left bin/tank and filter-bay edges move to x = 29 mm to clear the rear sliders. Their opposite edges stay fixed; the filter element shifts 2 mm and retains its full 141 × 76 × 20 mm allocation. The sofa bin becomes 1 mm taller. No sensor, converter, wheel, roller, water/debris load or energy reserve is removed.','',
        'Capacity screen: inset each chamber box by 3 mm walls, then reserve 15% for non-storage features. This is a declared packaging assumption; later baffles, seals, ports and evacuation geometry must still fit without reducing the targets.','',
        '| Module | After wall/reserve screen | Required usable target |','|---|---:|---:|']
    for name,b in r['bins'].items():s.append(f"| {name} | {b['after_reserve_l']*1000:.0f} mL | {b['target_l']*1000:.0f} mL |")
    s += ['', '## Power-carrier integration result','',
        'A straight shared upper front bridge at [27, 83.5, 65] mm, 221 × 1.5 × 20 mm, initially intersects the controller bay and sofa feed-drive bay. G clears the route: separate the RoboClaw and full-size supervisor board allocations, moving the supervisor 1 mm right/4 mm forward, and move the full sofa feed-drive bay 5 mm forward. No PCB or actuator allocation is shrunk. The F carrier stock is excluded from the bridge collision test because it would be replaced.','',
        '| Bottom | F obstruction | G obstruction, excluding replaced carrier |','|---|---|---|']
    for name,g in r['ground'].items():s.append('| '+name+' | '+', '.join(g['bridge_conflicts_before'])+' | '+(', '.join(g['bridge_conflicts']) or 'None')+' |')
    s += ['', 'The bridge route is now available, but its attachments to the fixed suspension pivots and the caster-support structure are not yet designed. Keep the 225 g bottom frame and complete F carrier in the carried mass. Do not build both overlapping carrier systems or credit support removal until the replacement load path, insulation and fasteners are complete. The bridge is a checked replacement envelope, not an installed zero-mass part.','',
        '## Complete carried estimates','', '| Loaded configuration | F | G candidate |','|---|---:|---:|']
    for name,g in r['ground'].items():s.append(f"| {name} + cap | {g['before']['mass_g'][1]:.0f} g | {g['after']['mass_g'][1]:.0f} g |")
    s += [f"| Airborne duster + quad | {old['assembly']['mass_g'][1]:.0f} g | {a['assembly']['mass_g'][1]:.0f} g |",'',
        f"Duster static limiting-rotor thrust/weight becomes {a['screen']['static_trim']['static_peak_thrust_weight']:.3f}:1. This remains effectively at the 2:1 threshold within modeling uncertainty; the frame study does not qualify flight or select a battery.",'',
        'Model and CAD checks cover the new stock allocations, slider positions, core withdrawal past the F power hardware and downward battery extraction. The full station motion, latch retention, optical coverage, production shell, cables, fastener protrusion, wet-floor behavior and installed thrust remain unverified. Keep F as the comparison record; G is a candidate mechanical revision with a changed top seat.','',
        '[Design note](../../../docs/FRAME_JOINT_DESIGN.md) · [Frame drawing](frame_joints.svg) · [FreeCAD](frame_joints.FCStd) · [STEP](frame_joints.step)']
    return '\n'.join(s)+'\n'


def diagram(r):
    # Two dimensioned corner sections communicate the load path better than a
    # full cluttered robot view. Generated from the same tube/slider inputs.
    k=r['config']['corner'];t=k['wall_mm'];h=k['outer_z_mm'];w=k['outer_y_mm']
    s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 650">','<rect width="1000" height="650" fill="white"/>',
       '<style>text{font-family:sans-serif;fill:#24374b} .label{font-size:16px} .dim{font-size:14px}</style>',
       '<text x="30" y="40" font-size="25">G core corner — cut rectangular tube, retained steel sliders</text>',
       '<text x="30" y="70" class="label">Reference section; latch details and local stresses remain unqualified.</text>']
    scale=8;x=100;y=150
    s += [f'<rect x="{x}" y="{y}" width="{w*scale}" height="{h*scale}" fill="#9cabb8"/>',
          f'<rect x="{x+t*scale}" y="{y+t*scale}" width="{(w-2*t)*scale}" height="{(h-2*t)*scale}" fill="white"/>']
    for offset in (t,t+k['bearing_pad_mm'][2]+k['draw_gap_mm'],h-t-k['bearing_pad_mm'][2]-k['draw_gap_mm']-2,h-t-k['bearing_pad_mm'][2]):
        is_pad=offset in (t,h-t-k['bearing_pad_mm'][2]);ww=k['bearing_pad_mm'][1] if is_pad else 18
        s.append(f'<rect x="{x+(w-ww)/2*scale}" y="{y+offset*scale}" width="{ww*scale}" height="16" fill="{"#ba862a" if is_pad else "#315d89"}"/>')
    s += [f'<path d="M{x+w*scale+22} {y} h10 V{y+h*scale} h-10" fill="none" stroke="#24374b"/>',
          f'<text x="{x+w*scale+40}" y="{y+h*scale/2}" class="dim">38.1 mm</text>',
          '<text x="105" y="490" class="label">25.4 mm external depth</text>',
          '<text x="85" y="525" class="label">3.175 mm walls · 18 mm cut length</text>',
          '<text x="480" y="170" class="label">Upper module stud → steel lock → tube face</text>',
          '<text x="480" y="215" class="label">Two continuous walls carry load between faces</text>',
          '<text x="480" y="260" class="label">Tube face → steel lock → lower module stud</text>',
          '<text x="480" y="325" class="label">Sliders move through the open tube ends</text>',
          '<text x="480" y="353" class="label">8 mm outward release at the station</text>',
          '<text x="480" y="410" class="label">600 N factored overall load</text>',
          '<text x="480" y="438" class="label">300 N / corner in unequal-sharing screen</text>',
          f'<text x="30" y="590" class="label">Complete core metal estimate: {r["installed_frame_mass_g"]:.1f} g; previous allowance: 145 g.</text>',
          '<text x="30" y="622" class="dim">The drawing shows material and load direction, not a finished cam, pawl or slider guide.</text>','</svg>']
    return ''.join(s)


def main():
    f=partition.configured(base.read(),partition.read());d=read();r=study(f,d,air.read())
    errors=[]
    for name,g in r['ground'].items():errors.extend(name+': '+e for e in g['checks']['errors']+g['withdrawal_errors']+g['slider_sweep_errors'])
    for name,v in r['airborne_after']['cases'].items():errors.extend(name+': '+e for e in v['screen']['geometry_errors'])
    errors.extend(r['battery_exchange_errors'])
    if not r['corner_radius_screen']['passes']:errors.append('Corner-radius / bearing-pad clearance screen fails')
    for name,b in r['bins'].items():
        if not b['target_screen_pass']:errors.append(name+': capacity screen fails')
    for name,g in r['ground'].items():
        errors.extend(name+': proposed replacement bridge / '+e for e in g['bridge_conflicts'])
    if errors:raise ValueError(errors)
    OUT.mkdir(exist_ok=True)
    (OUT/'frame_joints.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'frame_joints.md').write_text(report(r))
    (OUT/'frame_joints.svg').write_text(diagram(r))
    with (OUT/'frame_joints_hardware.csv').open('w',newline='') as file:
        writer=csv.writer(file);writer.writerow(['instance','hardware','low_g','nominal_g','high_g','basis'])
        for row in r['ground']['vacuum']['assembly']['rows']:
            if row['module']=='core':writer.writerow([row['instance'],row['hardware_id'],*row['mass_g'],row['mass_basis']])
    print(f"G core metal {r['installed_frame_mass_g']:.3f} g; ground height {r['ground_height_mm']:.1f} mm")
    print('Flange screens:',[(x['thickness_mm'],round(x['stress_mpa'],1),x['passes_stress_screen']) for x in r['flange_screens'] if x['anchors_sharing']==2])


if __name__=='__main__':main()
