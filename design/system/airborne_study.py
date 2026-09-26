"""Airborne-only dusting and compact propulsion trade, using the shared core model.

This supplement does not rewrite the earlier ground/CAD baseline. Undefined
duct performance stays undefined; geometry targets never become flight claims.
"""
from copy import deepcopy
import csv
import hashlib
import html
import json
import math
from pathlib import Path

import build as base

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'design/system/output'


def read():
    return json.loads((ROOT / 'config/airborne_dusting.json').read_text())


def boom_geometry(d):
    b = d['boom']; root = b['root_mm']; a = math.radians(b['angle_deg'])
    direction = b.get('direction_y', -1)
    elbow = [root[0], root[1]+direction*b['main_length_mm']*math.cos(a), root[2]+b['main_length_mm']*math.sin(a)]
    wrist = [elbow[0], elbow[1]+direction*b['wrist_length_mm'], elbow[2]]
    tip = [wrist[0], wrist[1], wrist[2]-b['brush_drop_mm']]
    def tube(od, inner, length):
        return math.pi/4*(od**2-inner**2)*length/1000*b['carbon_density_g_cm3']
    main_g = tube(b['main_od_mm'], b['main_id_mm'], b['main_length_mm'])
    sleeve_g = tube(b['wrist_od_mm'], b['wrist_id_mm'], b['internal_sleeve_length_mm'])
    wrist_g = tube(b['wrist_od_mm'], b['wrist_id_mm'], b['wrist_length_mm'])
    mid = [(x+y)/2 for x,y in zip(root, elbow)]
    wrist_mid = [(x+y)/2 for x,y in zip(elbow, wrist)]
    tube_cg = [((main_g+sleeve_g)*mid[i]+wrist_g*wrist_mid[i])/(main_g+sleeve_g+wrist_g) for i in range(3)]
    return dict(root=root, elbow=elbow, wrist=wrist, tip=tip, tubes_cg=tube_cg,
                stock_mass_g=main_g+sleeve_g+wrist_g, horizontal_reach_mm=abs(root[1]-tip[1]),
                contact_height_mm=tip[2], path_length_mm=b['main_length_mm']+b['wrist_length_mm']+b['brush_drop_mm'])


def configured(base_config, d):
    c = deepcopy(base_config); g = boom_geometry(d)
    c['bottoms']['air_dust'] = dict(label='Airborne duster / passive feet', groups=['air_dust'],
        payload_g=d['payload_g'][1], payload_high_g=d['payload_g'][2], payload_at=g['tip'],
        payload_note='Dust retained in microfiber; no water, suction bin or floor drive')
    parts = []
    def part(id, xyz, size, hardware=(), shape='box', **extra):
        p = dict(id=id, module='air_dust', label=id.replace('_',' '), min=xyz, size=size,
                 hardware=[dict(id=h, qty=1) for h in hardware], shape=shape,
                 group='tool', notes='Airborne study allocation; not fabrication geometry.', **extra)
        parts.append(p); return p
    for h in d['hardware']:
        c['hardware'][h['id']] = dict(name=h['name'], mass_g=h['mass_g'], mass_basis=h['basis'],
            source='', notes='Unmeasured design allowance', procurement='design_candidate', measured_mass_g=None)
        cg = h.get('cg_mm', g.get(h.get('location',''), g['tip']))
        if h.get('location') == 'tubes': cg = g['tubes_cg']
        part(h['id']+'_mass', [x-1 for x in cg], [2,2,2], [h['id']], 'distributed', mass_cg_mm=cg)
    for i,(x,y) in enumerate(d['landing_contacts_xy_mm']):
        part('air_foot_'+str(i), [x-10,y-10,0], [20,20,16])
    for i,(x,y) in enumerate(c['interfaces']['lock_centres_xy_mm']):
        part('air_post_'+str(i), [x-4,y-4,16], [8,8,70])
    for name,xyz,size in [('front',[2.5,2.5,16],[270,2,20]), ('rear',[2.5,270.5,16],[270,2,20]),
                          ('left',[2.5,4.5,16],[10,266,20]), ('right',[262.5,4.5,16],[10,266,20])]:
        p=part('air_rail_'+name, xyz, size)
        p['notes']='Edgewise 20 x 2 mm aluminum crossmember' if name in ('front','rear') else 'Printed rib allocation; material included in air_frame'
    socket_y = g['root'][1] - (30 if d['boom'].get('direction_y', -1) == 1 else 12)
    part('air_root_socket', [g['root'][0]-15,socket_y,24], [30,42,24])
    part('air_control_bay', [157,164,24], [36,60,22])
    for id,p0,p1,od in [('air_main_spar',g['root'],g['elbow'],d['boom']['main_od_mm']),
                       ('air_wrist_spar',g['elbow'],g['wrist'],d['boom']['wrist_od_mm'])]:
        part(id, [min(x,y)-od/2 for x,y in zip(p0,p1)],
             [abs(x-y)+od for x,y in zip(p0,p1)], shape='beam', endpoints_mm=[p0,p1], diameter_mm=od)
    tip=g['tip']; w,dep,h=d['boom']['head_size_mm']
    part('air_microfiber_head', [tip[0]-w/2,tip[1]-dep/2,tip[2]], [w,dep,h])
    part('air_head_hanger', [tip[0]-4,tip[1]-4,tip[2]+h], [8,8,g['wrist'][2]-tip[2]-h])
    c['parts'].extend(parts)
    return c


def collision_parts(parts):
    """Conservative small boxes along tubes, avoiding their huge diagonal AABB.

    Each box encloses an entire short tube segment plus a radius at both ends.
    This is a conservative static allocation check, not a continuous motion test.
    """
    result=[]
    for p in parts:
        if p['shape']!='beam':
            result.append(p);continue
        a,b=p['endpoints_mm'];n=math.ceil(math.dist(a,b)/5);rad=p['diameter_mm']/2
        for i in range(n):
            a0=[x+(y-x)*i/n for x,y in zip(a,b)]
            a1=[x+(y-x)*(i+1)/n for x,y in zip(a,b)]
            q=deepcopy(p);q.update(id=p['id']+'_segment_'+str(i),shape='box',
                min=[min(x,y)-rad for x,y in zip(a0,a1)],size=[abs(x-y)+2*rad for x,y in zip(a0,a1)])
            result.append(q)
    return result


def mission(hover_w, tool_w, available_wh, m, cleaning_s=0):
    if hover_w is None: return None
    overhead_s=(m['outbound_s']+m['return_s'])*m['transit_power_factor']+m['landing_reserve_s']
    contact_w=hover_w*m['cleaning_power_factor']+tool_w
    base_wh=hover_w*overhead_s/3600
    spendable_wh=available_wh/(1+m['energy_margin_fraction'])
    raw_seconds=(spendable_wh-base_wh)*3600/contact_w
    required=(base_wh+contact_w*cleaning_s/3600)*(1+m['energy_margin_fraction'])
    return dict(cleaning_seconds=max(0,raw_seconds), transfer_and_reserve_wh=base_wh,
                transit_reserve_feasible=spendable_wh>=base_wh, required_usable_wh=required,
                outbound_s=m['outbound_s'], return_s=m['return_s'], landing_reserve_s=m['landing_reserve_s'],
                contact_w=contact_w, scope='Energy ceiling; assumes the stated loads and travel times, no guarantee of thermal duty or achieved cleaning')


def compact_layouts(c,d):
    layouts=[]
    for spec in d['compact_layouts']:
        s=deepcopy(spec); rad=s['outer_mm']/2
        if 'centres_relative_mm' not in s:
            p=137.5+(rad+s['core_radial_clearance_mm'])/math.sqrt(2)
            s['centres_relative_mm']=[[-p,-p],[p,-p],[p,p],[-p,p]]
        xy=s['centres_relative_mm']; w=max(x for x,y in xy)-min(x for x,y in xy)+2*rad
        length=max(y for x,y in xy)-min(y for x,y in xy)+2*rad
        yaw=math.radians(c['lift']['yaw_uncertainty_deg'])
        occupied=w*math.cos(yaw)+length*math.sin(yaw)+2*c['lift']['lateral_margin_mm']
        clear=c['limits']['stair_clear_width_mm']-c['limits']['left_projection_mm']-c['limits']['right_projection_mm']
        gap=min(math.hypot(max(abs(x)-137.5,0),max(abs(y)-137.5,0))-rad for x,y in xy)
        s.update(envelope_xy_mm=[w,length], yaw_and_margin_width_mm=occupied,
                 corridor_margin_mm=clear-occupied, minimum_body_radial_clearance_mm=gap,
                 rotor_disk_area_m2=len(xy)*math.pi*(s['rotor_mm']/2000)**2,
                 flight_qualified=False, matched_hover_power_w=None, installed_top_mass_g=None)
        layouts.append(s)
    return layouts


def quad_balance(a,c):
    """Rectangle equilibrium with equal reaction-torque coefficients, zero yaw.

    Alternating spin directions assumed. This only checks static vertical loads;
    no dynamic allocator, contact forces or rotor failure are qualified.
    """
    x,y=[a['cg_mm'][i]-137.5 for i in (0,1)]
    positions=c['lift']['variants']['quad10']['rotors_xy_relative_mm']
    half_x=max(abs(p[0]) for p in positions);half_y=max(abs(p[1]) for p in positions)
    fractions=[(1+math.copysign(1,px)*x/half_x+math.copysign(1,py)*y/half_y)/4 for px,py in positions]
    return dict(fractions=fractions, cg_offset_xy_mm=[x,y], positive_hover_loads=min(fractions)>0)


def parked_boom(d):
    g=boom_geometry(d);root=g['root'];points=[]
    # Rotate main spar upright about its root. Head geometry is included.
    angle=math.radians((90-d['boom']['angle_deg'])*d['boom'].get('direction_y', -1))
    for name in ('root','elbow','wrist'):
        p=g[name];rad=d['boom']['main_od_mm']/2
        points.extend([[p[0]+sx*rad,p[1]+sy*rad,p[2]+sz*rad] for sx in (-1,1) for sy in (-1,1) for sz in (-1,1)])
    w,dep,h=d['boom']['head_size_mm'];tip=g['tip']
    points.extend([[tip[0]+sx*w/2,tip[1]+sy*dep/2,tip[2]+sz*h] for sx in (-1,1) for sy in (-1,1) for sz in (0,1)])
    rotated=[]
    for p in points:
        x,y,z=[p[i]-root[i] for i in range(3)]
        rotated.append([x,math.cos(angle)*y-math.sin(angle)*z,math.sin(angle)*y+math.cos(angle)*z])
    size=[max(p[i] for p in rotated)-min(p[i] for p in rotated) for i in range(3)]
    return dict(tool_extent_mm=size,rack_mm=d['station_boom_rack_mm'],
                clearance_mm=[a-b for a,b in zip(d['station_boom_rack_mm'],size)],
                scope='Detached spar/head only; receiver, handling motion and service access still need detail')


def air_assembly(c,d,top='cap'):
    a=base.assembly(c,'air_dust',top)
    if top != 'cap' and d.get('flight_layout'):
        locate_flight_hardware(a,c,d['flight_layout'])
    next(r for r in a['rows'] if r['instance']=='payload')['mass_g']=d['payload_g'][:]
    a.update(base.mass_and_cg(a['rows']))
    return a


def locate_flight_hardware(a,c,layout):
    """Move modeled camera/FC mass onto their physical allocation proxies.

    Replaces their distributed rows, never adds another set of electronics.
    Shared structure, harness and smaller flight electronics remain allowances.
    """
    for p in a['parts']:
        if p['module'] != 'lift': continue
        if p['id'] in ('depth_camera', 'flight_controller'): p['hardware']=[]
        if p['id'] in layout: p['min']=layout[p['id']][:]
        if p['id'] in ('flight_camera_rear', 'flight_camera_down'):
            p['hardware']=[dict(id='depth_camera',qty=1)]
        if p['id']=='flight_fc_proxy':p['hardware']=[dict(id='flight_controller',qty=1)]
    extra=deepcopy([r for r in a['rows'] if r['instance'] in ('battery','payload')])
    a['rows']=base.hardware_rows(c,a['parts'])+extra
    a.update(base.mass_and_cg(a['rows']))


def study(c,d):
    new=configured(c,d); g=boom_geometry(d)
    bare=air_assembly(new,d); feet=d['landing_contacts_xy_mm']
    margin=base.signed_margin(bare['cg_mm'][:2],feet)
    old=base.assembly(c,'dust','octo10',pose='extended')
    old_bottom=[r for r in old['rows'] if r['module'] not in ('core','cap','battery','payload','lift')]
    removed_drive={'drive_motor','drive_wheel','wheel_hub','pod','caster','roboclaw','anti_tip'}
    drive_g=sum(r['mass_g'][1] for r in old_bottom if r['hardware_id'] in removed_drive)
    pack=c['batteries']['design_6s']; usable=pack['nominal_v']*pack['capacity_ah']*c['power']['usable_energy_fraction']
    cases={}
    for variant in c['lift']['variants']:
        a=air_assembly(new,d,variant)
        collision_a=deepcopy(a);collision_a['parts']=collision_parts(a['parts'])
        f=base.lift_metrics(new,collision_a,variant)
        core_parts=[p for p in collision_a['parts'] if p['module']=='core' and p['shape']!='distributed' and not p.get('parent')]
        tool_parts=[p for p in collision_a['parts'] if p['module']=='air_dust' and p['shape']!='distributed']
        f['geometry_errors'] += ['Core/tool allocation overlap: '+p['id']+' / '+q['id']
                                 for p in core_parts for q in tool_parts if base.overlap(p,q)]
        if variant=='quad10':
            trim=quad_balance(a,new)
            per=[base.interpolate(new['lift']['curve_thrust_g_power_w'],a['mass_g'][1]*fraction/new['lift']['guard_factor']) for fraction in trim['fractions']]
            electronic_w=sum(x['normal_w']/new['power']['rail_efficiency'][x['rail']] for x in new['power']['core_loads'])+16
            f['hover_w']=None if None in per else sum(per)*new['lift']['power_overhead_factor']+electronic_w
            f['hover_current_a']=None if f['hover_w'] is None else f['hover_w']/new['lift']['minimum_voltage_screen_v']
            trim['static_peak_thrust_weight']=f['thrust_weight_nominal']/(4*max(trim['fractions']))
            trim['meets_2_to_1_static_screen']=trim['static_peak_thrust_weight']>=2
            f['static_trim']=trim
            # Base-model aggregate maneuver/departure fields are not used in
            # this supplement: retain no stale mission values after trim.
            for key in list(f):
                if key.startswith(('maneuver_','transfer_','landing_','departure_','energy_remaining_','airborne_tool_')):del f[key]
        b=d['boom']; root=g['root']
        # Conservative scalar moment sum: gravity plus horizontal tip contact;
        # this is not a motor allocation or force-control stability analysis.
        boom_ids={'air_tubes','air_joints','air_head','air_flexure','air_tip_sense'}
        gravity=sum(r['mass_g'][1]/1000*base.G*abs(r['cg_mm'][1]-root[1])/1000
                    for r in a['rows'] if r['hardware_id'] in boom_ids or r['instance']=='payload')
        gravity_high=sum(r['mass_g'][2]/1000*base.G*abs(r['cg_mm'][1]-root[1])/1000
                         for r in a['rows'] if r['hardware_id'] in boom_ids or r['instance']=='payload')
        contact=b['tip_force_normal_n']*math.dist(root,g['tip'])/1000
        contact_retreat=b['tip_force_retreat_n']*math.dist(root,g['tip'])/1000
        cases[variant]=dict(assembly=a, screen=f,
            missions={key:mission(f['hover_w'],d['tool_electrical_w'][0],usable,m) for key,m in d['missions'].items()},
            nominal_2_to_1_margin_g=f['max_mass_at_target_g']-a['mass_g'][1],
            boom_gravity_moment_nm=gravity, boom_contact_moment_nm=contact,
            root_factored_moment_nm=(gravity_high+contact_retreat)*b['root_load_factor'],
            sensor_note='Rear boom and outboard rear stereo allocation avoid static contact. Perception coverage, structural mounting and optical occlusion remain open.')
    layouts=compact_layouts(c,d)
    layouts[0]['matched_hover_power_w']=cases['quad10']['screen']['hover_w']
    layouts[0]['installed_top_mass_g']=sum(r['mass_g'][1] for r in cases['quad10']['assembly']['rows'] if r['module']=='lift')
    # Common-mass requirements, not assumed EDF/hover-duct performance.
    comparison_mass=cases['quad10']['assembly']['mass_g'][1]
    mission_targets=[]
    for seconds in (60,180,300):
        m=d['missions']['local_dusting']; equivalent=(m['outbound_s']+m['return_s'])*m['transit_power_factor']+m['landing_reserve_s']+seconds*m['cleaning_power_factor']
        max_hover=(usable/(1+m['energy_margin_fraction'])*3600-seconds*d['tool_electrical_w'][0])/equivalent
        mission_targets.append(dict(cleaning_s=seconds, maximum_hover_w=max_hover,
            required_wh_at_current_quad=mission(cases['quad10']['screen']['hover_w'],d['tool_electrical_w'][0],usable,m,seconds)['required_usable_wh']))
    result = dict(revision=d['revision'], config=d, boom=g, supported_assembly=bare, cases=cases,
        old_bottom_nominal_g=sum(r['mass_g'][1] for r in old_bottom), new_bottom_mass_g=[sum(h['mass_g'][i] for h in d['hardware']) for i in range(3)],
        removed_drive_hardware_g=drive_g, old_octo_mass_g=old['mass_g'][1],
        same_octo_mass_saving_g=old['mass_g'][1]-cases['octo10']['assembly']['mass_g'][1],
        passive_foot_nominal_support_margin_mm=margin,
        parked_boom=parked_boom(d),
        limits=dict(flight_qualified=False, station_motion_validated=False, blade_access_validated=False),
        usable_pack_wh=usable, layouts=layouts, common_mass_g=comparison_mass,
        four_unit_hover_thrust_each_g=comparison_mass/4, four_unit_peak_target_each_g=comparison_mass/2,
        mission_targets=mission_targets, source_curve=c['lift']['curve_thrust_g_power_w'],
        source=c['sources']['flight_motor'],
        core_flight_electronics_w=sum(x['normal_w']/c['power']['rail_efficiency'][x['rail']] for x in c['power']['core_loads'])+16,
        guard_factor=c['lift']['guard_factor'], power_overhead_factor=c['lift']['power_overhead_factor'],
        input_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                      [ROOT/'config/system_design.json',ROOT/'config/airborne_dusting.json']})
    if d.get('front_reference'):
        front=deepcopy(d);ref=front.pop('front_reference')
        front['boom'].update(root_mm=ref['root_mm'],direction_y=-1)
        front['flight_layout']['flight_camera_rear']=ref['flight_camera_rear']
        for h in front['hardware']:
            if h['id'] in ref['hardware_cg_mm']:h['cg_mm']=ref['hardware_cg_mm'][h['id']]
        fa=air_assembly(configured(c,front),front,'quad10');trim=quad_balance(fa,c)
        result['front_reference']=dict(mass_g=fa['mass_g'],cg_mm=fa['cg_mm'],
            static_peak_thrust_weight=cases['quad10']['screen']['thrust_weight_nominal']/(4*max(trim['fractions'])),
            accounting='Both configurations assign the two added cameras and FC to their actual proxies; D used a centered distributed mass for these items.')
    result['ducted_comparison']=ducted_comparison(c,d,result)
    result['ground_quad_reference']={}
    for bottom in ('vacuum','mop','low'):
        a=base.assembly(c,bottom,'quad10')
        result['ground_quad_reference'][bottom]=dict(mass_g=a['mass_g'],screen=base.lift_metrics(c,a,'quad10'))
    return result


def ducted_comparison(c,d,r):
    spec=d.get('ducted_comparison')
    if not spec:return None
    n=spec['rotor_count'];v=spec['supply_screen_v'];f=spec['retained_thrust']
    replaced={'lift_motor','lift_prop','lift_esc','lift_guard'}
    shared=[row for row in r['cases']['quad10']['assembly']['rows'] if row['module']=='lift' and row['hardware_id'] not in replaced]
    common=[sum(row['mass_g'][i] for row in shared) for i in range(3)]
    bottoms={'air_dust':r['cases']['quad10']['assembly']}
    for bottom in ('vacuum','mop','low'):
        bottoms[bottom]=base.assembly(c,bottom,'quad10')
    results=[]
    for fan in spec['candidates']:
        ledger=[dict(item='Retained common quad frame, wiring and flight electronics',qty=1,mass_g=common,basis='Existing installed allowances; no compact-frame mass credit'),
                dict(item='Fan, motor and test intake ring',qty=n,mass_g=[n*(fan['fan_motor_g']+fan['inlet_g'])]*3,basis=fan['source']),
                dict(item='ESC assemblies',qty=n,mass_g=[n*x for x in spec['esc_each_g']],basis='Unselected installed allowance'),
                dict(item='Inlet/outlet protection and fan mounts',qty=n,mass_g=[n*x for x in spec['guard_mount_each_g']],basis='Unmeasured allowance; protection loss independent'),
                dict(item='Yaw control, actuation and connections',qty=1,mass_g=spec['yaw_control_g'],basis='Unselected allowance; no qualified control allocation')]
        top=[sum(row['mass_g'][i] for row in ledger) for i in range(3)]
        curve=fan['points_v_a_w_g']
        peak=base.interpolate([[p[0],p[3]] for p in curve],v)
        peak_w=base.interpolate([[p[0],p[2]] for p in curve],v)
        cases={}
        for bottom,a in bottoms.items():
            carried=[sum(row['mass_g'][i] for row in a['rows'] if row['module']!='lift') for i in range(3)]
            masses=[x+y for x,y in zip(carried,top)]
            # Equal sharing is explicitly optimistic: EDF yaw/trim not solved.
            required=masses[1]/n/f
            power=base.interpolate([[p[3],p[2]] for p in curve],required)
            within_peak=peak is not None and required<=peak
            hover=None if power is None or not within_peak else n*power*spec['power_overhead_factor']+r['core_flight_electronics_w']
            travel=dict(outbound_s=c['lift']['transfer_s'],return_s=0,landing_reserve_s=c['lift']['landing_reserve_s'],
                        transit_power_factor=c['lift']['maneuver_power_factor'],cleaning_power_factor=1,energy_margin_fraction=c['lift']['energy_margin_fraction'])
            energy=mission(hover,0,r['usable_pack_wh'],travel)
            cases[bottom]=dict(mass_g=masses,source_equivalent_hover_each_g=required,hover_w=hover,
                hover_current_a=None if hover is None else hover/v,
                aggregate_peak_tw=None if peak is None else n*peak*f/masses[1],
                aggregate_peak_tw_high_mass=None if peak is None else n*peak*f/masses[2],
                peak_tw_retention_sensitivity=[None if peak is None else n*peak*ret/masses[1] for ret in spec['retained_thrust_sensitivity']],
                ideal_nominal_voltage_peak_tw=n*curve[-1][3]/masses[1],
                transfer=energy,
                local_dusting=mission(hover,d['tool_electrical_w'][0],r['usable_pack_wh'],d['missions']['local_dusting']) if bottom=='air_dust' else None,
                hover_status=('Insufficient installed thrust to hover at supply screen' if not within_peak else
                              'Equivalent voltage-sweep interpolation, equal loads; unqualified' if hover is not None else
                              'Unknown: required hover thrust outside published samples; no extrapolation'),
                flight_qualified=False,trim_and_yaw_qualified=False)
        results.append(dict(id=fan['id'],label=fan['label'],source=fan['source'],ledger=ledger,top_mass_g=top,
            peak_each_source_g=peak,
            peak_input_current_screen_a=None if peak_w is None else (n*peak_w*spec['power_overhead_factor']+r['core_flight_electronics_w'])/v,
            cases=cases))
    return dict(spec=spec,candidates=results,
        scope='Four-unit screening only. EDF yaw/trim, height, cooling, thrust response and protection are unresolved. No CAD or fixed-voltage continuous qualification. 150 mm hover duct remains a separate unselected candidate.')


def diagram(r):
    g=r['boom']; d=r['config']; b=d['boom']
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="940" viewBox="0 0 1080 940">',
         '<rect width="1080" height="940" fill="#f8fafc"/><g font-family="sans-serif" fill="#173047">']
    def text(x,y,s,size=15): out.append(f'<text x="{x}" y="{y}" font-size="{size}">{html.escape(s)}</text>')
    text(28,36,'Airborne duster: passive feet, light spar and dust-catching head',23)
    text(28,62,'Reference allocations. Blade-edge access and flight control require validation; no fabrication release.')
    scale=.67
    def pt(p):
        y=275-p[1] if b.get('direction_y',-1)==1 else p[1]
        return 390-y*scale,360-p[2]*scale
    bodyx,bodyy=pt([0,0 if b.get('direction_y',-1)==1 else 275,180])
    out.append(f'<rect x="{bodyx}" y="{bodyy}" width="{275*scale}" height="{180*scale}" fill="#dce8f7" stroke="#466cbd"/>')
    text(bodyx+10,bodyy+45,'Core + battery',17);text(bodyx+10,bodyy+68,'Passive feet below',13)
    for start,end in [(g['root'],g['elbow']),(g['elbow'],g['wrist']),(g['wrist'],g['tip'])]:
        x1,y1=pt(start);x2,y2=pt(end)
        out.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#a96028" stroke-width="7" fill="none"/>')
    x,y=pt(g['tip']);out.append(f'<rect x="{x-18}" y="{y-13}" width="36" height="13" fill="#258c79"/>')
    # Blade extends forward from an edge between elbow and brush, leaving spar outside.
    edge_y=g['elbow'][1]+b.get('direction_y',-1)*40; ex,ey=pt([0,edge_y,g['tip'][2]])
    out.append(f'<rect x="{ex}" y="{ey}" width="{1040-ex}" height="5" fill="#909aa3"/>')
    text(765,ey-14,'Stopped blade / surface',15)
    text(415,385,f'Horizontal root-to-contact reach: {g["horizontal_reach_mm"]:.0f} mm')
    text(415,407,f'Contact height above landing plane: {g["contact_height_mm"]:.0f} mm')
    text(415,429,f'Rear tool, 610 mm path; fixed {b["angle_deg"]}° root; station detaches for storage')
    text(28,473,'Four-position lift footprints, drawn to the same scale',21)
    text(28,497,'Duct footprints are targets; documented EDF mass and performance screens appear in the report.')
    sc=.32
    for index,s in enumerate(r['layouts']):
        ox=185+index*350; oy=699
        text(25+index*350,535,s['label'],17)
        for x,y in s['centres_relative_mm']:
            out.append(f'<circle cx="{ox+x*sc}" cy="{oy+y*sc}" r="{s["outer_mm"]*sc/2}" fill="#ffe6cb" stroke="#ba782e"/>')
            out.append(f'<circle cx="{ox+x*sc}" cy="{oy+y*sc}" r="{s["rotor_mm"]*sc/2}" fill="none" stroke="#ba782e" stroke-dasharray="3 3"/>')
        out.append(f'<rect x="{ox-137.5*sc}" y="{oy-137.5*sc}" width="{275*sc}" height="{275*sc}" fill="#dce8f7" stroke="#466cbd"/>')
        w,l=s['envelope_xy_mm'];text(25+index*350,864,f'{w:.0f} × {l:.0f} mm projected footprint',16)
        text(25+index*350,889,f'{s["corridor_margin_mm"]:.0f} mm stair-width margin in the 2° yaw screen',12)
    text(28,925,'Compact footprints alone do not establish lift capability. Inlet/outlet clearance and the complete flight route remain open.',13)
    out.append('</g></svg>');return '\n'.join(out)


def report(r):
    q=r['cases']['quad10'];before=r['front_reference'];trim=q['screen']['static_trim']
    lines=['# Airborne dusting and documented EDF comparison — revision E', '',
        'The rear-mounted, wheel-less duster is the preferred lightweight bottom. None of the four-unit lift options below is selected for flight or procurement.', '',
        '## Balance without ballast', '',
        f'Bottom hardware remains **{r["new_bottom_mass_g"][1]:.0f} g** nominal; complete quad aircraft **{r["common_mass_g"]/1000:.3f} kg**. The boom root moves to x=165, y=283, z=36 mm. Its keyed socket is redesigned at the rear; the common electrical interface is unchanged. The station fits this rear boom, and flight approaches with the tool end leading.', '',
        'The rear stereo camera moves to the left outboard bracket (allocation minimum −34.5, 278, 43 mm), opposite the right-side downward camera. The two cameras and flight controller now carry their mass at their physical allocations instead of a centered distribution. Counts and total mass are unchanged; mounting and cable routes remain to detail.', '',
        '| Same mass and refined camera accounting | CG x / y | Balance-preserving peak thrust/weight |',
        '|---|---:|---:|',
        f'| Front boom reference | {before["cg_mm"][0]:.1f} / {before["cg_mm"][1]:.1f} mm | {before["static_peak_thrust_weight"]:.2f}:1 |',
        f'| Rear boom and left rear camera | {q["assembly"]["cg_mm"][0]:.1f} / {q["assembly"]["cg_mm"][1]:.1f} mm | {trim["static_peak_thrust_weight"]:.2f}:1 |', '',
        f'Body center is 137.5 / 137.5 mm. The largest static rotor share is now {100*max(trim["fractions"]):.2f}%. This still misses the provisional 2:1 target. Even perfect balance leaves only {q["nominal_2_to_1_margin_g"]:.0f} g aggregate mass growth margin; high mass cases remain substantially worse. Revision D reported 1.81:1 using the older camera accounting; compare the two rows above to isolate this layout change.', '',
        f'Passive-foot nominal support margin with cap/core/pack is {r["passive_foot_nominal_support_margin_mm"]:.0f} mm. The tool still has 610 mm path, {r["boom"]["horizontal_reach_mm"]:.0f} mm horizontal root-to-contact reach and {r["boom"]["contact_height_mm"]:.0f} mm contact height. The rear route clears the three retained lift/core allocation models. Full motion, optical coverage and structural joints are not validated.', '',
        '## Propeller mission reference', '',
        '| Lift top | Complete nominal / high mass | Hover estimate | Aggregate peak T/W | Local / longer-route cleaning |',
        '|---|---:|---:|---:|---:|']
    for key,v in r['cases'].items():
        a=v['assembly'];f=v['screen'];m=v['missions']
        lines.append(f'| {key} | {a["mass_g"][1]/1000:.3f} / {a["mass_g"][2]/1000:.3f} kg | {f["hover_w"]:.0f} W | {f["thrust_weight_nominal"]:.2f}:1 | {m["local_dusting"]["cleaning_seconds"]:.0f} / {m["longer_dusting"]["cleaning_seconds"]:.0f} s |')
    lines += ['', 'Local dusting includes 20 s outbound, 20 s return and 30 s landing reserve; longer route has 45 s each way. Travel is 1.2× hover, contact flight 1.1× plus 2 W sensing. A 20% energy margin is applied to 92.352 Wh usable pack energy (80% of nominal 6S 5200 mAh). These are energy ceilings, not achieved endurance. Hex/octo still assume equal loads; the quad uses static trim. Do not rank tiny hover-power differences.', '',
        f'[Matched propeller source]({r["source"]}). The model assumes 75% thrust retention, a 21 V peak-thrust screen and 10% power overhead. The highest source point is limited to 29 seconds. Neither guards nor continuous installed duty are qualified.', '',
        '| Ground bottom carried intact by the same quad | Complete nominal mass | Aggregate peak T/W, before trim |',
        '|---|---:|---:|']
    labels={'air_dust':'Airborne duster','vacuum':'Vacuum + contents','mop':'Mop + water','low':'Under-sofa vacuum, stowed'}
    for key,v in r['ground_quad_reference'].items():
        lines.append(f'| {labels[key]} | {v["mass_g"][1]/1000:.3f} kg | {v["screen"]["thrust_weight_nominal"]:.2f}:1 |')
    lines += ['', 'A lighter dusting bottom does not make this quad a universal top for stair transfers.', '',
        '## Documented 89 mm EDF assemblies', '',
        'Use the matched WeMoTec fan/motor assemblies as comparison evidence. Each listed source includes a stabilized-voltage sweep; it is not a fixed-6S partial-throttle test. Only interpolate within the published points. The supplied intake ring is included in mass. A 120 mm installed diameter is still a packaging target; motor protrusion, inlet/outlet guards, yaw hardware and installed height have not been resolved.', '',
        '| Assembly | Fan + motor + inlet mass per unit | Source sample voltage / thrust / input |', '|---|---:|---|']
    comp=r['ducted_comparison'];spec=comp['spec']
    for fan in spec['candidates']:
        samples='; '.join(f'{p[0]:.1f} V / {p[3]/1000:.2f} kgf / {p[2]:.0f} W' for p in fan['points_v_a_w_g'])
        lines.append(f'| [{fan["label"]}]({fan["source"]}) | {fan["fan_motor_g"]+fan["inlet_g"]} g | {samples} |')
    lines += ['', 'Complete installed-top accounting retains the existing common frame, harness and flight electronics. Each EDF gets a 100 g ESC allowance and 50 g protection/mount allowance; another 120 g is reserved for unresolved yaw-control hardware. These are engineering allowances, not selected products. No compact-frame weight saving is credited.', '',
        '| Four-unit top | Installed low / nominal / high mass | Peak input-current screen at 21 V |', '|---|---:|---:|']
    for fan in comp['candidates']:
        masses=' / '.join(f'{x/1000:.3f}' for x in fan['top_mass_g'])
        lines.append(f'| {fan["label"]} | {masses} kg | {fan["peak_input_current_screen_a"]:.0f} A |')
    lines += ['', 'These peak-current estimates include 10% power overhead and core/flight electronics. They exceed the existing 150 A continuous / 320 A short-duration power-path allocations, which themselves remain unqualified. Controller amps are not battery capacity or guaranteed pack capability.', '',
        '| EDF option / carried bottom | Complete nominal / high mass | Aggregate peak T/W at 21 V | Equal-load hover estimate |', '|---|---:|---:|---:|']
    for fan in comp['candidates']:
        for key,v in fan['cases'].items():
            power='Unknown — below source samples' if v['hover_w'] is None else f'{v["hover_w"]:.0f} W'
            lines.append(f'| {fan["id"].replace("wemotec_", "HET ")} / {labels[key]} | {v["mass_g"][1]/1000:.3f} / {v["mass_g"][2]/1000:.3f} kg | {v["aggregate_peak_tw"]:.2f}:1 | {power} |')
    weak=comp['candidates'][0]['cases'];air=weak['air_dust'];vac=weak['vacuum']
    lines += ['', 'EDF results assume 85% delivered thrust after installation and 10% power overhead. The viewer also shows 70–100% retention sensitivity. Their different loss assumption does not imply EDF guards outperform propeller guards. Equal loads and unresolved yaw make the aggregate thrust an optimistic bound, not controlled lift capability. More than four units, other motors and other voltages have not been ruled out by this study.', '',
        f'The 1970 option needs an estimated **{air["local_dusting"]["required_usable_wh"]:.1f} Wh usable** for the local dusting trip and landing reserve before any cleaning, exceeding {r["usable_pack_wh"]:.1f} Wh available. A 45 s one-way stair transfer plus 30 s landing reserve needs about **{vac["transfer"]["required_usable_wh"]:.1f} Wh** carrying the vacuum, with energy margin. The stronger 2000 variant has no published hover-range samples for these loads, so its hover/endurance remains unknown; its thrust-margin failure is independently calculable.', '',
        f'**Yaw is a separate gate.** The cited EDF pages do not establish matched reverse-rotation units or net reaction torque. Do not reverse motor wiring and assume the fan retains its performance, or reuse the propeller quad mixer. A [stator-equipped ducted-aircraft study]({spec["yaw_source"]}) uses deflecting vanes for control. That supports investigating a dedicated control solution here, not transferring its performance or proving this EDF configuration.', '',
        '## Design decision and next work', '',
        '- Retain the rear, wheel-less duster with a station-removable microfiber tool. No ballast or extra battery has been added.',
        '- Keep both small EDF variants as rejected four-unit candidates under the current mass, voltage and mission assumptions; do not purchase them for this robot.',
        '- Continue the 150 mm hover-duct option as an open requirements target. Seek complete rotor/motor/duct/guard data, continuous hover duty, throttle response and a yaw solution; do not substitute RC-jet peak thrust for these data.',
        '- Reduce common core and lift overhead next, because those masses are carried with every bottom. Preserve explicit allowances for protection, exchange locks and sensors.',
        '- Size the universal transfer top against the loaded vacuum/mop/sofa bottoms separately from dusting duration. Multiple compatible top variants remain an option; none is selected.', '',
        'At fixed pack energy, three minutes of local dusting still needs roughly 1 kW hover or less. A larger battery changes mass and must be recalculated. The station still needs its powered launch shuttle, supported exchanges, rear-boom handler and 90 × 160 × 700 mm vertical rack; no station motion is released for fabrication.', '',
        '[Design explanation](../../../docs/AIRBORNE_DUSTING.md) · [Interactive comparison](airborne_dusting.html) · [Layout drawing](airborne_dusting.svg) · [EDF mass worksheet](airborne_edf_hardware.csv)', '']
    return '\n'.join(lines)


def balance_diagram(r):
    front=deepcopy(r['config']);front['boom'].update(root_mm=front['front_reference']['root_mm'],direction_y=-1)
    cases=[('Front boom reference',boom_geometry(front),r['front_reference']['cg_mm'],r['front_reference']['static_peak_thrust_weight']),
           ('Rear boom, left rear camera',r['boom'],r['cases']['quad10']['assembly']['cg_mm'],r['cases']['quad10']['screen']['static_trim']['static_peak_thrust_weight'])]
    s=.45;out=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="750" viewBox="0 0 1080 750">',
        '<rect width="1080" height="750" fill="#f8fafc"/><g font-family="sans-serif" fill="#173047">',
        '<text x="28" y="34" font-size="24">Duster balance: relocate hardware, keep the same mass</text>',
        '<text x="28" y="60" font-size="15">Plan views: body center cross; red CG point magnified in the readout. Boom is above the guards.</text>']
    for i,(label,g,cg,tw) in enumerate(cases):
        ox=275+i*530;oy=393
        def xy(p):return ox+(p[0]-137.5)*s,oy+(p[1]-137.5)*s
        out.append(f'<text x="{ox-225}" y="98" font-size="21">{label}</text>')
        for x,y in r['layouts'][0]['centres_relative_mm']:
            out.append(f'<circle cx="{ox+x*s}" cy="{oy+y*s}" r="{142*s}" fill="#ffe6cb" stroke="#ba782e"/>')
        out.append(f'<rect x="{ox-137.5*s}" y="{oy-137.5*s}" width="{275*s}" height="{275*s}" fill="#dce8f7" stroke="#466cbd"/>')
        for a,b in [('root','elbow'),('elbow','wrist')]:
            x1,y1=xy(g[a]);x2,y2=xy(g[b]);out.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#a96028" stroke-width="5"/>')
        x,y=xy(g['tip']);out.append(f'<rect x="{x-13.5}" y="{y-11.25}" width="27" height="22.5" fill="#258c79"/>')
        x,y=xy(cg);out.append(f'<path d="M{ox-9},{oy} H{ox+9} M{ox},{oy-9} V{oy+9}" stroke="#173047"/><circle cx="{x}" cy="{y}" r="4" fill="#c83d37"/>')
        for pos in ([85.5,278,43],[285,112,50]) if i==0 else (r['config']['flight_layout']['flight_camera_rear'],[285,112,50]):
            x,y=xy(pos);out.append(f'<rect x="{x}" y="{y}" width="{104*s}" height="{27*s}" fill="#bda4d3"/>')
        out.append(f'<text x="{ox-225}" y="686" font-size="17">CG {cg[0]:.1f} / {cg[1]:.1f} mm; static peak T/W {tw:.2f}:1</text>')
    out.append('<text x="28" y="728" font-size="14">Both use 5.249 kg nominal aircraft mass and the same camera/FC accounting. Neither meets the 2:1 target.</text></g></svg>')
    return '\n'.join(out)


def main():
    c=base.read();d=read();r=study(c,d);OUT.mkdir(exist_ok=True)
    (OUT/'airborne_dusting.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'airborne_dusting.svg').write_text(diagram(r)+'\n')
    (OUT/'airborne_balance.svg').write_text(balance_diagram(r)+'\n')
    (OUT/'airborne_dusting.md').write_text(report(r))
    template=(ROOT/'design/system/airborne_viewer.html').read_text()
    (OUT/'airborne_dusting.html').write_text(template.replace('__AIRBORNE_DATA__',json.dumps(r).replace('</','<\\/')))
    with (OUT/'airborne_dusting_hardware.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['id','item','low_g','nominal_g','high_g','mass_basis'])
        for h in d['hardware']:w.writerow([h['id'],h['name'],*h['mass_g'],h['basis']])
    with (OUT/'airborne_edf_hardware.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['candidate','item','qty','total_low_g','total_nominal_g','total_high_g','basis'])
        for fan in r['ducted_comparison']['candidates']:
            for row in fan['ledger']:w.writerow([fan['id'],row['item'],row['qty'],*row['mass_g'],row['basis']])
    errors={key:v['screen']['geometry_errors'] for key,v in r['cases'].items() if v['screen']['geometry_errors']}
    print(json.dumps({'bottom_mass_g':r['new_bottom_mass_g'],'quad_mass_g':r['common_mass_g'],
                      'local_cleaning_s':r['cases']['quad10']['missions']['local_dusting']['cleaning_seconds'],
                      'lift_allocation_errors':errors},indent=2))
    if errors:raise SystemExit('Resolve lift/duster allocation clashes')


if __name__=='__main__':main()
