"""O: compare a floor-resident extension sharing the ordinary vacuum bottom.

No baseline ledger or production CAD is modified. Space reservations and an
explicit incremental hardware scope accompany the mass accounting. Motion,
hair pickup, leak-tight seals, completed joints and traction remain unproven.
"""
from copy import deepcopy
import csv
import html
import json
import math
from pathlib import Path
import build as B
import fixed_drive as N

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'design/system/output'


def read():
    return json.loads((ROOT / 'config/sofa_attachment.json').read_text())


def hardware(d, baseline):
    rows = []
    def add(scope, item):
        rows.append(dict(scope=scope, id=item['id'], mass_g=item['mass_g'], basis=item['basis']))
    stock = d['body_receiver_stock']
    weight = stock['qty'] * math.prod(stock['plate_size_mm']) * stock['density_g_mm3']
    add('body_interface', dict(id='two_receiver_plates', mass_g=[weight]*3,
        basis='Two gross steel plate volumes; holes not deducted. Latches/fasteners separately counted'))
    for item in d['body_interface_allowances']:
        add('body_interface', item)
    add('normal_head_adapter', d['normal_head_adapter'])
    source = {r['instance']: r for r in B.assembly(baseline, 'low', payload=False)['rows']}
    for id in d['extension_source_instances']:
        row = source[id]
        add('extension', dict(id=id, mass_g=row['mass_g'], basis='Inherited dedicated-sofa function allowance; '+row['mass_basis']))
    for item in d['extension_additions']:
        add('extension', item)
    return rows


def space(d):
    g = d['geometry']
    stroke = (g['stage_count']-1)*(g['stage_length_mm']-g['overlap_mm'])
    head_y = g['head_min_stowed_mm'][1]
    depth = g['body_mm'][1]-head_y
    pivot_x, pivot_y = g['yaw_center_mm']
    # Entire stowed envelope, not just the head; bristles/operating margin excluded.
    points = [(x,y) for x in (0,g['body_mm'][0]) for y in (0,g['body_mm'][1])]
    points += [(x,y) for x in (g['head_min_stowed_mm'][0],g['head_min_stowed_mm'][0]+g['head_size_mm'][0])
               for y in (head_y,head_y+g['head_size_mm'][1])]
    points += [(x,y) for x in (g['tool_frame_min_mm'][0],g['tool_frame_min_mm'][0]+g['tool_frame_size_mm'][0])
               for y in (g['tool_frame_min_mm'][1],g['tool_frame_min_mm'][1]+g['tool_frame_size_mm'][1])]
    diameter = 2*max(math.hypot(x-pivot_x,y-pivot_y) for x,y in points)
    working_height = max(g['head_min_stowed_mm'][2]+g['head_size_mm'][2],g['outer_stage_min_mm'][2]+g['outer_mm'][1])
    return dict(stroke_mm=stroke, stowed_rigid_outline_mm=[g['body_mm'][0],depth,g['body_mm'][2]],
        extended_rigid_depth_mm=depth+stroke,
        head_standoff_mm=head_y-g['sofa_front_y_mm'],
        body_standoff_mm=-g['sofa_front_y_mm'],
        reach_from_sofa_front_mm=g['sofa_front_y_mm']-(head_y-stroke),
        required_sofa_depth_mm=g['sofa_depth_mm'],
        floor_in_front_mm=g['body_mm'][1]-g['sofa_front_y_mm'],
        stowed_yaw_swept_diameter_mm=diameter,
        under_sofa_working_height_mm=working_height,
        under_sofa_raised_height_mm=working_height+g['raised_travel_mm'],
        parked_tool_depth_mm=g['air_face_center_mm'][1]+g['air_face_size_mm'][1]/2-head_y,
        parking_nest_target_mm=g['parking_nest_target_mm'],
        scope='Flat-floor nominal envelope only; yaw rotation assumes cart follows body yaw. No leg-avoidance, threshold, joint-motion or autonomous route proof.')


def air_losses(d, baseline):
    c=deepcopy(baseline); g=d['geometry']; a=d['air']
    e=c['extension']
    for key in ('stage_count','stage_length_mm','overlap_mm','outer_mm','wall_mm'):
        e[key]=g[key]
    e['step_mm']=g['stage_step_mm']
    results=[]
    w,h=[v/1000 for v in a['link_internal_mm']]
    dh=2*w*h/(w+h)
    for flow in a['flow_samples_l_s']:
        e['airflow_l_s']=flow
        r=B.extension_metrics(c)
        velocity=flow/1000/(w*h)
        dynamic=1.225*velocity**2/2
        straight=a['friction_factor']*(a['link_length_mm']/1000)/dh*dynamic
        link=straight+a['link_minor_k']*dynamic
        results.append(dict(flow_l_s=flow, telescope_loss_pa=r['total_added_loss_pa'],
            link_loss_pa=link,total_added_loss_pa=r['total_added_loss_pa']+link,
            link_k_sensitivity_total_pa=[r['total_added_loss_pa']+straight+k*dynamic for k in a['link_minor_k_range']],
            smallest_bore_mm=[g['outer_mm'][i]-(g['stage_count']-1)*g['stage_step_mm']-2*g['wall_mm'] for i in (0,1)]))
    return results


def geometry_checks(d,p):
    old=next(v for v in B.reference_parts(p['layout'],'low') if v['id']=='extension')
    conflicts=[v['id'] for v in p['parts'] if v.get('shape')!='distributed' and not v.get('parent') and B.overlap(old,v)]
    # Check only the defined receiver plate and air-face reservations. Do not
    # call a gross cart box a solid, or imply unspecified latch geometry fits.
    g=d['geometry'];plates=[dict(id='O_receiver_'+str(i),min=xyz,size=d['body_receiver_stock']['plate_size_mm']) for i,xyz in enumerate(g['receiver_plate_mins_mm'])]
    cx,cy,cz=g['air_face_center_mm'];w,t,h=g['air_face_size_mm']
    face=dict(id='O_air_face',min=[cx-w/2,cy-t/2,cz-h/2],size=[w,t,h])
    pairs=[]
    for candidate in plates+[face]:
        for v in p['parts']:
            # vac_flex is the intended common mating path, retained in mass.
            if v.get('shape')=='distributed' or v.get('parent') or v['id']=='vac_flex':continue
            if B.overlap(candidate,v):pairs.append([candidate['id'],v['id']])
    return dict(old_internal_telescope_conflicts=conflicts, receiver_reservation_intersections=pairs,
        receiver_reservations=plates+[face],
        scope='Checks these three axis-aligned reservations against nominal M vacuum placements retained by N. Excludes intended mating flex. Does not cover locks, head travel/withdrawal, hoses, fastener access or the rest of the unfinished cart.')


def receiver_motion(d,p,n):
    """Sample terrain/raised clearance; exact straight AABB withdrawal at q=0.

    Each moving box conservatively encloses its rotated allocation. A box hit
    is a conflict reservation, not proof of solid interference for finished CAD.
    Positive clearance only applies to these modeled pieces and sampled poses.
    """
    heads=[v for v in p['parts'] if v['id'] in d['removed_normal_head_parts']]
    poses=N.terrain('vacuum',p,n,N.read())
    poses.append(dict(state='raised level',step_mm=0,heading_deg=0,
        q_mm=p['M']['raised_travel_mm'],normal=[0,0,1]))
    ref=p['M']['modules']['vacuum']['reference_mm']
    def gap(a,b):
        return math.sqrt(sum(max(0,b['min'][i]-a['min'][i]-a['size'][i],
            a['min'][i]-b['min'][i]-b['size'][i])**2 for i in range(3)))
    results={}
    for name,mins in [('previous',d['head_exchange']['legacy_receiver_plate_mins_mm']),
                      ('revised',d['geometry']['receiver_plate_mins_mm'])]:
        plates=[dict(id=f'{name}_receiver_{i}',min=xyz,size=d['body_receiver_stock']['plate_size_mm']) for i,xyz in enumerate(mins)]
        hits=[];minimum=math.inf
        for pose in poses:
            for head in heads:
                moved=N.M.envelope(head,ref,pose['q_mm'],pose['normal'])
                for plate in plates:
                    minimum=min(minimum,gap(moved,plate))
                    if B.overlap(moved,plate):hits.append(dict(state=pose['state'],step_mm=pose['step_mm'],
                        heading_deg=pose['heading_deg'],q_mm=pose['q_mm'],head=head['id'],receiver=plate['id']))
        results[name]=dict(intersection_count=len(hits),intersections=hits,minimum_sampled_box_gap_mm=minimum)
    withdrawal=d['head_exchange']['withdrawal_mm'];sweeps=[];hits=[]
    fixed=[v for v in p['parts'] if v['id'] not in d['removed_normal_head_parts'] and
        v['id']!='vac_flex' and v.get('shape')!='distributed' and not v.get('parent')]
    fixed+=geometry_checks(d,p)['receiver_reservations']
    for head in heads:
        swept=deepcopy(head);swept['min'][1]-=withdrawal;swept['size'][1]+=withdrawal
        sweeps.append(dict(id=head['id'],min=swept['min'],size=swept['size']))
        for v in fixed:
            if B.overlap(swept,v):hits.append([head['id'],v['id']])
    room=d['room_clearance'];s=space(d)
    return dict(pose_count=len(poses),**results,withdrawal_mm=withdrawal,
        withdrawal_sweeps=sweeps,withdrawal_intersections=hits,
        minimum_head_front_separation_after_withdrawal_mm=min(withdrawal-h['min'][1]-h['size'][1] for h in heads),
        extension_tail_front_separation_after_withdrawal_mm=withdrawal-d['geometry']['air_face_center_mm'][1]-d['geometry']['air_face_size_mm'][1]/2,
        exchange_combination_depth_mm=s['stowed_rigid_outline_mm'][1]+withdrawal,
        nominal_room_front_remainder_mm=room['front_space_mm']-s['floor_in_front_mm'],
        nominal_room_turning_diameter_remainder_mm=room['turning_space_diameter_mm']-s['stowed_yaw_swept_diameter_mm'],
        mass_delta_g=0,
        scope='Sampled N head poses plus level 16 mm lift; straight level withdrawal of existing head/motor boxes only. New receiver plates and air face included. Intended flexible air joint excluded; other unspecified adapters/locks/wiring and continuous motion/deflection are not validated. Room figures are approximate owner confirmation, not certified navigation margins.')


def study(d=None):
    d=d or read()
    if d['policy']['extension_flies']:
        raise ValueError('This study is explicitly for a floor-resident extension')
    p,n=N.nominal_mass('vacuum',N.read())
    original=B.assembly(p['layout'],'vacuum',payload=False)['rows']
    head=[r for r in original if r['part'] in d['removed_normal_head_parts']]
    if {r['part'] for r in head} != set(d['removed_normal_head_parts']):
        raise ValueError('Missing normal-head scope in baseline')
    h=hardware(d,p['layout'])
    def total(scope,index=1):return sum(r['mass_g'][index] for r in h if r['scope']==scope)
    interface=total('body_interface');adapter=total('normal_head_adapter');extension=total('extension')
    removed=sum(r['mass_g'][1] for r in head)
    contents=p['config']['contents']['vacuum']
    usual=sum(v[0] for v in contents[p['config']['calibration_contents_index']['vacuum']]['loads'])
    maximum=max(sum(v[0] for v in case['loads']) for case in contents)
    cap=sum(r['mass_g'][1] for r in original if r['module']=='cap')
    ground=n['mass_g']-usual+maximum
    flight=ground-cap+interface+adapter
    limit=json.loads((ROOT/'config/mass_budgets.json').read_text())['classes']['transfer']['budget_g']
    residents=d['policy']['floors']*d['policy']['extensions_per_floor']
    return dict(revision=d['revision'],config=d,hardware=h,removed_head_rows=head,
        mass=dict(baseline_N_ground_max_contents_g=ground,baseline_N_transfer_max_contents_g=ground-cap,
            common_body_interface_g=interface,normal_head_adapter_g=adapter,
            ordinary_head_removed_g=removed,parked_normal_head_with_adapter_g=removed+adapter,
            extension_g=extension,extension_estimate_interval_g=[total('extension',i) for i in range(3)],
            resident_extension_count=residents,all_resident_extensions_g=extension*residents,
            flight_interface_increment_g=interface+adapter,
            ordinary_ground_max_contents_g=ground+interface+adapter,
            sofa_ground_max_contents_g=ground+interface-removed+extension,
            transfer_usual_contents_g=flight-maximum+usual,transfer_max_contents_g=flight,
            transfer_budget_g=limit,transfer_reduction_needed_g=max(0,flight-limit),
            upper_complete_mass_g=None,usual_contents_g=usual,max_contents_g=maximum,removed_cap_g=cap,
            extension_mass_in_flight_g=0,measured_compliance=False),
        space=space(d),air=air_losses(d,p['layout']),checks=geometry_checks(d,p),
        receiver_motion=receiver_motion(d,p,n),
        context_parts=[v for v in p['parts'] if v['id'] in ('vac_head','vac_head_drive','vac_duct','vac_bin_left','vac_bin_front','vac_blower','battery_bay','front_camera','drive_control')])


def svg(r,travel=1,side=False):
    """Static, dimensioned review drawing; the HTML viewer also varies travel."""
    g=r['config']['geometry'];stroke=r['space']['stroke_mm']*travel
    xmin=-1400;xmax=325;zbase=250
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{xmin} -55 {xmax-xmin} 380" role="img" aria-label="Sofa attachment {"side" if side else "top"} layout">',
         '<style>text{font:18px sans-serif;fill:#172d3b} .small{font-size:14px}</style>']
    def rect(x,y,w,h,fill,stroke='#334e60',opacity=1):
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{fill}" stroke="{stroke}" opacity="{opacity}"/>')
    def label(x,y,t,cls=''):out.append(f'<text x="{x}" y="{y}" class="{cls}">{html.escape(t)}</text>')
    sy=g['sofa_front_y_mm'];back=sy-g['sofa_depth_mm']
    if side:
        rect(back,zbase-180,g['sofa_depth_mm'],180-g['sofa_clearance_mm'],'#dfd8c8',opacity=.8)
        out.append(f'<path d="M{xmin},{zbase} H{xmax}" stroke="#536471"/>')
        rect(0,zbase-180,275,180,'#b9ced9',opacity=.7)
        rect(-280,zbase-40,245,36,'#179eaa')
        for i in range(1,g['stage_count']):
            width,height=[v-i*g['stage_step_mm'] for v in g['outer_mm']]
            rect(-280-i*stroke/(g['stage_count']-1),zbase-(22+height/2),245,height,'#5fc3c7')
        rect(-340-stroke,zbase-38,60,38,'#e99a35')
        rect(-122,zbase-77,80,35,'#8264ad')
        rect(-35,zbase-41,117,22,'#179eaa')
        for y in (-220,105,232):
            radius=17 if y<0 else (36 if y==105 else 16)
            out.append(f'<circle cx="{y}" cy="{zbase-radius}" r="{radius}" fill="#455560"/>')
        label(back+20,5,'Sofa underside: 50 mm')
        label(-300,300,'Head 38 mm / guide 40 mm working; raise only outside sofa','small')
    else:
        rect(back,-20,g['sofa_depth_mm'],315,'#ebe7dc',opacity=.7)
        rect(0,0,275,275,'#c9dbe3')
        for part in r['context_parts']:
            if part['id'] in r['config']['removed_normal_head_parts']:continue
            x,y,z=part['min'];w,l,h=part['size'];rect(y,x,l,w,'#8fabbb',opacity=.5)
        for x in (2,249):rect(69,x,72,24,'#455560')
        rect(-280,22.5,245,230,'#d5e9e5',opacity=.65)
        for i in range(g['stage_count']):
            width=g['outer_mm'][0]-i*g['stage_step_mm']
            rect(-280-i*stroke/(g['stage_count']-1),137.5-width/2,245,width,'#42b4bf')
        rect(-340-stroke,37.5,60,200,'#e99a35')
        rect(-122,28.5,80,75,'#8264ad')
        rect(-35,121.5,117,32,'#179eaa')
        for x,y in g['supports_xy_mm']:rect(y-18,x-12,36,24,'#455560')
        label(back+20,-32,'914 mm sofa depth; front-only access')
        label(5,-15,'Shared vacuum')
        label(-315,315,'External support cart / feed drive','small')
    out.append(f'<path d="M{sy},-20 V280" stroke="#a46522" stroke-dasharray="6 4"/>')
    label(-1380,315,'Floor-supported extension; ordinary roller head parked at dock','small')
    out.append('</svg>')
    return ''.join(out)


def receiver_svg(r):
    """Front projection of reservations; Y placement given as text separately."""
    g=r['config']['geometry'];stock=r['config']['body_receiver_stock']['plate_size_mm']
    items=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-15 -36 305 188" role="img" aria-label="Receiver plate height and supported head withdrawal review">',
        '<rect x="-15" y="-36" width="305" height="188" fill="white"/>',
        '<g font-family="DejaVu Sans" font-size="5" fill="#183446">',
        '<text font-size="7" x="0" y="-24">Head receiver — front projection, dimensions in mm</text>',
        '<text x="0" y="-14">Green: revised plates   Red: former plates   Dashed: level head raised 16 mm</text>']
    def rect(x,z,w,h,color,dashed=False):
        dash=' stroke-dasharray="2 1"' if dashed else ''
        items.append(f'<rect x="{x}" y="{100-z-h}" width="{w}" height="{h}" fill="{color}" stroke="#274d60" stroke-width="0.45"{dash}/>')
    for x in (26,247):rect(x,65,2,20,'#718996')
    for v in r['context_parts']:
        if v['id'] not in r['config']['removed_normal_head_parts']:continue
        x,y,z=v['min'];w,l,h=v['size']
        rect(x,z,w,h,'#f5c37c' if v['id']=='vac_head' else '#b9afd1')
        rect(x,z+16,w,h,'none',True)
    for x,y,z in r['config']['head_exchange']['legacy_receiver_plate_mins_mm']:
        rect(x,z,stock[0],stock[2],'#cb695c')
    for x,y,z in g['receiver_plate_mins_mm']:
        rect(x,z,stock[0],stock[2],'#219b83')
    items += ['<path d="M0,100 H275" stroke="#274d60" stroke-width="0.5"/>',
        '<text x="0" y="109">Floor Z0; head shown level at its working position. Receiver plates span Y40–80.</text>',
        '<text x="0" y="119">Revised plate minima: [24.5,40,68] and [249,40,68]; stock: 1.5 × 40 × 20 each.</text>',
        '<text x="0" y="129">Dock withdrawal: support the head level, then move it 100 mm forward (out of this view).</text>',
        '<text font-size="4.4" x="0" y="141">Projection of allocation boxes only. Complete locks, adapters, fasteners and head supports remain unfinished.</text>',
        '</g></svg>']
    return ''.join(items)


def report(r):
    m=r['mass'];s=r['space']
    lines=['# Floor-resident sofa attachment comparison','',
        '**Preferred architecture to develop:** exchange the complete ordinary powered head for an external, floor-supported sofa extension. Share the vacuum drivetrain, bin, filter, blower, core and battery. Keep one extension on each floor. The extension is never part of the transfer-flight load.','',
        'This is a feasibility candidate. N remains conditional, and the automatic head interface is new work; the existing manual M3 cassette mount cannot perform this exchange. No new printable parts or purchase list are released.','',
        '## Complete carried mass at maximum modeled contents','','| Configuration | Nominal mass | Meaning |','|---|---:|---|',
        f"| N vacuum before head-exchange hardware | {m['baseline_N_transfer_max_contents_g']/1000:.3f} kg | Transfer assembly, no cap/lift |",
        f"| O vacuum ready for transfer | {m['transfer_max_contents_g']/1000:.3f} kg | Core, battery, normal head and permanent exchange hardware; no extension/cap/lift |",
        f"| O ordinary floor vacuum | {m['ordinary_ground_max_contents_g']/1000:.3f} kg | Same configuration with cap |",
        f"| O sofa cleaning on floor | {m['sofa_ground_max_contents_g']/1000:.3f} kg | With cap and one extension; normal head parked |",
        f"| One detached extension | {m['extension_g']/1000:.3f} kg | Own cart, telescope, head, feed/lift hardware and interfaces |",'',
        f"All vacuum rows use {m['max_contents_g']:.0f} g debris in the existing shared bin. Transfer is **{m['transfer_reduction_needed_g']:.0f} g above the 4.5 kg limit**. This architecture does not fix the underlying vacuum/core mass deficit. At usual {m['usual_contents_g']:.0f} g debris, O transfer is {m['transfer_usual_contents_g']/1000:.3f} kg.",'',
        f"The flight increment is {m['common_body_interface_g']:.2f} g of body interface plus {m['normal_head_adapter_g']:.0f} g on the normal head, totaling **{m['flight_interface_increment_g']:.2f} g**. The {m['ordinary_head_removed_g']:.0f} g known head hardware and its new adapter stay in the nest during sofa work. Full existing M mount/lift/riser and N support allowances remain counted; overlapping scopes are not credited before a detailed replacement exists.",'',
        f"Extension estimate interval: {m['extension_estimate_interval_g'][0]/1000:.3f} / {m['extension_g']/1000:.3f} / {m['extension_estimate_interval_g'][2]/1000:.3f} kg (low/nominal/high planning values, not statistical bounds). Whole-robot upper mass remains undefined because N has no upper replacement estimate. {m['resident_extension_count']} resident extensions total {m['all_resident_extensions_g']/1000:.3f} kg of inventory; only one attaches at a time, and zero fly. Station racks/shuttles are additional stationary hardware, outside these carried masses.",'',
        '## Space and reach','','| Quantity | Nominal reservation |','|---|---:|',
        f"| Ordinary rigid body and wheels | 275 × 275 × 180 mm |",
        f"| With extension retracted | 275 × {s['stowed_rigid_outline_mm'][1]:.0f} × 180 mm |",
        f"| Telescope travel | {s['stroke_mm']:.0f} mm |",
        f"| Maximum leading-edge reach beyond sofa front | {s['reach_from_sofa_front_mm']:.0f} mm versus {s['required_sofa_depth_mm']:.1f} mm depth |",
        f"| Under-sofa working head / guide height | 38 / {s['under_sofa_working_height_mm']:.0f} mm |",
        f"| Straight floor space in front of sofa | {s['floor_in_front_mm']:.0f} mm before clearance margin |",
        f"| Ideal stowed turning sweep | {s['stowed_yaw_swept_diameter_mm']:.0f} mm diameter before clearance margin |",
        f"| One extension parking nest target | 270 × 450 × 140 mm |",'',
        'The ordinary body remains inside the owner limit. The removable extension uses the explicit exception for extensions. Six 245 mm stages with 45 mm overlap give 1000 mm travel. Here the main body is 360 mm from the sofa front; the stowed head is only 20 mm away. These are different distances. Do not reuse the old internal-telescope model’s 80 mm body standoff or 335 mm stowed outline.','',
        'Working head/guide must lower before entering the 50 mm gap. Raising 12 mm gives a 52 mm guide envelope, too tall for that gap. The feed drive stays outside the sofa. Reach is axial and measured to the leading edge; the suction-mouth position is unfinished. Full stroke extends 66 mm past the nominal sofa back, so limit the commanded stroke for rear walls/obstructions. Sofa legs and underside obstructions may leave areas inaccessible; mapping and coverage checks remain necessary.','',
        'The telescope cannot simply occupy its old position within the ordinary vacuum. Nominal conflicts: '+', '.join(r['checks']['old_internal_telescope_conflicts'])+'. Move it outside the body, on its own supports. Receiver plate/air-face reservation intersections: '+str(r['checks']['receiver_reservation_intersections'])+'. That limited screen does not validate the moving receiver, latch, wiring, withdrawal path or finished joints.','',
        '## Airflow screen','','| Assumed flow | Telescope + added coupler/link loss | Coupler K sensitivity |','|---|---:|---:|']
    for a in r['air']:
        lo,hi=a['link_k_sensitivity_total_pa']
        lines.append(f"| {a['flow_l_s']:g} L/s | {a['total_added_loss_pa']:.0f} Pa | {lo:.0f}–{hi:.0f} Pa |")
    lines += ['',
        'Smooth-duct Darcy/minor-loss calculation inherited from the system model, with 150 mm extra 32 × 22 mm link. It excludes the head, common duct/bin/filter, joint leakage and hair blockage; it is not a blower operating point or a pickup prediction. The smallest telescope bore is only 31 × 19 mm (589 mm²). Flush seals and a cleanable path matter, and representative dog-hair clumps may force a larger bore or a different guide/hose arrangement.','',
        'Use one common air connection at a time. Park the roller cassette and insert the extension outlet, so the blower does not draw through an unused floor opening. Do not add an uncounted tee/diverter. Retain the common flex/duct and add the tool-side compliant link across the articulated hitch.','',
        '## What remains to resolve','',
        '- Complete the receiver, positive locks, tool-support/load path, electrical contacts and air seals together. Preserve the ordinary head’s floor following; a rigid latch cannot replace its compliance.',
        f"- Specify an articulated, yaw-constrained cart connection and floor support. Check retracted/extended balance, wet-floor traction, turning and all 4–10 mm thresholds. Existing wheel-drive results are not validation for the roughly {m['sofa_ground_max_contents_g']/1000:.1f} kg sofa configuration.",
        '- Complete telescope guides, seal clearances, feed-strip routing, lift, wiring, obstruction detection and retrieval. Existing function masses are retained estimates, not finished mechanisms.',
        '- Allocate a supported external tool-exchange apron at each station. The 615 mm combination cannot be assumed to fit the old 275 mm robot bay. Parking-nest dimensions alone do not specify the entire station footprint.',
        '- Establish blower operating flow with the actual filter, head, link and staged duct. Preserve hair pickup before claiming battery endurance. Shared battery powers the attachment; feed/lift and added drag remain to validate. No additional carried battery is assumed.',
        '- Reduce the ordinary vacuum/core mass to the 4.5 kg transfer budget including its completed quick-change interface.', '',
        '## Confirmed room space and receiver follow-up','',
        'The owner answered **yes** to approximately 650 mm of clear floor in front of each sofa and 1 m of nearby turning space. The nominal envelope leaves only 15 mm of front-space difference and about 88 mm across the turning diameter; these rough figures are not measured operating margins. Sofa legs, navigation tolerances and station-apron space still need their own layout checks.','',
        f"The original receiver-plate reservations intersected head envelopes in {r['receiver_motion']['previous']['intersection_count']} sampled head/plate pairs. The same plates now sit at minimum corners [24.5,40,68] and [249,40,68] mm, against the outer faces of the existing side rails. They have no envelope intersections across {r['receiver_motion']['pose_count']} sampled terrain/raised poses, with a minimum sampled box gap of {r['receiver_motion']['revised']['minimum_sampled_box_gap_mm']:.2f} mm. Plate stock and complete carried-mass accounting are unchanged.",'',
        f"A level, supported {r['receiver_motion']['withdrawal_mm']:.0f} mm forward withdrawal of the normal head/motor boxes has {len(r['receiver_motion']['withdrawal_intersections'])} intersections against the checked fixed allocations and receiver/air-face reservations. Their rear edges end {r['receiver_motion']['minimum_head_front_separation_after_withdrawal_mm']:.0f} mm ahead of the body front. This establishes a candidate straight shuttle direction, not a finished automatic head exchange. Dock-located support, removable adapter/compliance, positive locks, connector engagement and air-flex disconnection remain to detail.",'',
        f"For the extension, the same proposed withdrawal clears its reserved air-face tail by {r['receiver_motion']['extension_tail_front_separation_after_withdrawal_mm']:.1f} mm ahead of the body, while robot plus tool occupy {r['receiver_motion']['exchange_combination_depth_mm']:.0f} mm longitudinally before margins. This is a station handling envelope, separate from the confirmed sofa approach space. The extension adapter/hitch withdrawal geometry remains incomplete.",'',
        '[Architecture and automatic sequence](../../../docs/SOFA_ATTACHMENT.md) · [Receiver drawing](sofa_head_receiver.svg) · [Interactive layout](sofa_attachment.html) · [Incremental hardware ledger](sofa_attachment_mass.csv) · [Inputs](../../../config/sofa_attachment.json)']
    return '\n'.join(lines)+'\n'


def main():
    r=study();OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'sofa_attachment.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'sofa_attachment.md').write_text(report(r))
    with (OUT/'sofa_attachment_mass.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['scope','id','low_g','nominal_g','high_g','basis'])
        for row in r['hardware']:w.writerow([row['scope'],row['id'],*row['mass_g'],row['basis']])
    for side in (False,True):
        (OUT/f'sofa_attachment_{"side" if side else "top"}.svg').write_text(svg(r,side=side))
    (OUT/'sofa_head_receiver.svg').write_text(receiver_svg(r))
    template=(Path(__file__).parent/'sofa_attachment_viewer.html').read_text()
    (OUT/'sofa_attachment.html').write_text(template.replace('__DATA__',json.dumps(r).replace('</','<\\/')))
    print(json.dumps(dict(mass=r['mass'],space=r['space'],checks=r['checks']),indent=2))


if __name__=='__main__':main()
