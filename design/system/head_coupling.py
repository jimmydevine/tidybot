"""P head coupling: dimensioned interface, explicit budgets and mating checks.

The full ordinary-head suspension is not supplied here. Existing O/M assembly
masses stay unchanged until this local candidate and remaining scope close.
"""
import csv
import hashlib
import json
import math
from pathlib import Path
import sofa_attachment as O

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'


def read():return json.loads((ROOT/'config/head_coupling.json').read_text())


def source_fingerprint():
    """Include inherited layout inputs so CAD checks cannot silently go stale."""
    paths=sorted((ROOT/'config').glob('*.json'))+sorted((ROOT/'design/system').glob('*.py'))
    h=hashlib.sha256()
    for path in paths:
        h.update(str(path.relative_to(ROOT)).encode());h.update(b'\0');h.update(path.read_bytes())
    return h.hexdigest()


def study(d=None):
    d=d or read();s=d['material_g_mm3'];a=d['air'];e=d['electrical'];m=d['mass_ownership']
    rows=[]
    def add(owner,id,grams,basis):rows.append(dict(owner=owner,id=id,mass_g=grams,basis=basis))
    add('body','receiver_plates',2*math.prod(d['plates']['size'])*s['steel'],'Gross stock; no hole credit')
    ch=d['cheeks'];th=ch['size'][0];rad=ch['slot_radius'];end=ch['left_min'][1]+ch['size'][1]
    cuts=sum((end-(ch['closed_end_y']-relief))*2*rad+math.pi*rad**2/2 for relief in (0,ch['right_end_relief_mm']))
    cuts+=2*math.pi*d['locks']['hole_diameter']**2/4
    add('carrier','slotted_cheeks',(2*math.prod(ch['size'])-cuts*th)*s['steel'],'Analytic finished open slots and lock bores; checked against CAD volume')
    add('carrier','rear_risers',2*math.prod(d['rear_risers']['size'])*s['steel'],'Gross stock')
    length,width,height=d['crossmember']['size'];t=d['crossmember']['wall']
    add('carrier','crossmember',length*(width*height-(width-2*t)*(height-2*t))*s['aluminum'],'Hollow tube; no drilled-hole credit')
    area=math.prod(a['outer'])-math.prod(a['inner'])
    flange=area*a['flange_thickness']*s['polymer']
    add('body','air_flange_and_stub',flange+(a['body_stub_end_y']-a['body_flange_y']-a['flange_thickness'])*(38*28-math.prod(a['inner']))*s['polymer'],'Printed gross ring/stub walls; no mounting bosses counted here')
    add('body','seal_and_air_mount_completion',15-rows[-1]['mass_g'],'Remainder of existing O 15 g body air-face scope; no mass saving booked')
    add('carrier','air_flange',flange,'Tool-side printed ring; active flex remains in common plumbing budget pending physical partition')
    for id,v in d['allowances_g'].items():add('body' if id.startswith('body_') else 'carrier',id,v,'Installed allowance; unresolved hardware is explicit')
    subtotal={owner:sum(r['mass_g'] for r in rows if r['owner']==owner) for owner in ('body','carrier')}
    gap=m['carrier_target_g']-subtotal['carrier']
    add('carrier','unallocated_carrier_budget',max(0,gap),'Remaining allocation, not fabricated material or weight saving')
    # Force sensitivity; no gasket grade selected, so pressure is not a rating.
    gasket_area=math.prod(a['gasket_outer'])-math.prod(a['gasket_inner'])
    contact_force=8*e['contact_force_n_nominal']
    pressures=[dict(pressure_kpa=p,force_n=gasket_area*p/1000) for p in a['gasket_pressure_kpa_cases']]
    seal_load=contact_force+pressures[1]['force_n']
    max_preload=contact_force*1.3+pressures[-1]['force_n']
    retained=d['loads']['one_lock_fore_aft_n']+max_preload
    pin_area=math.pi*d['locks']['pin_diameter']**2/4
    cheek_t=d['cheeks']['size'][0]
    key=d['locks'];key_begin=key['left_pin_min_x'];key_end=key_begin+key['pin_length']
    cheek_begin=d['cheeks']['left_min'][0];cheek_end=cheek_begin+cheek_t
    receiver_begin=d['plates']['mins'][0][0];receiver_end=receiver_begin+d['plates']['size'][0]
    cheek_engagement=min(key_end,cheek_end)-max(key_begin,cheek_begin)
    body_engagement=min(key_end,receiver_end)-max(key_begin,receiver_begin)
    minimum_engagement=min(cheek_engagement,body_engagement)-key['axial_tolerance_mm']
    edge=d['cheeks']['left_min'][1]+d['cheeks']['size'][1]-d['locks']['y']-d['locks']['hole_diameter']/2
    # Simply supported full tube, center applied load; joint compliance omitted.
    iv=(width*height**3-(width-2*t)*(height-2*t)**3)/12
    ih=(height*width**3-(height-2*t)*(width-2*t)**3)/12
    def bend(force,i,depth):return dict(stress_mpa=force*length/4*depth/2/i,
        deflection_mm=force*length**3/(48*d['loads']['e_aluminum_mpa']*i))
    seal_bend=bend(seal_load,ih,width)
    high_seal_bend=bend(max_preload,ih,width)
    zdef=bend(d['loads']['vertical_n'],iv,height)
    stack=e['stack_tolerance_mm']+high_seal_bend['deflection_mm']
    seal_stack=a['compression_tolerance_mm']+high_seal_bend['deflection_mm']
    strokes=[e['nominal_compression_mm']-stack,e['nominal_compression_mm']+stack]
    compression=a['gasket_free_t']-a['gasket_compressed_t']
    Odata=O.study();o=Odata['mass']
    current=e['proposed_tool_current_limit_a'];r=e['contact_resistance_ohm_max']
    target_y=e['body_board_front_y']-e['free_height_mm']+e['nominal_compression_mm']
    rear=max(a['tool_flange_y']+a['flange_thickness'],target_y)
    return dict(config=d,rows=rows,mass=dict(detailed_body_scope_g=subtotal['body'],detailed_carrier_scope_g=subtotal['carrier'],
        carrier_budget_g=m['carrier_target_g'],carrier_remainder_g=gap,body_budget_g=m['existing_O_body_interface_g'],
        remaining_head_compliance_g=m['remaining_compliance_target_g'],head_lift_retained_g=m['existing_M_head_lift_g'],
        before_combined_budget_g=m['existing_O_body_interface_g']+m['existing_O_head_adapter_g']+m['existing_M_head_mount_g']+m['existing_M_head_lift_g'],
        after_combined_budget_g=m['existing_O_body_interface_g']+m['carrier_target_g']+m['remaining_compliance_target_g']+m['existing_M_head_lift_g'],
        prior_transfer_mass_g=o['transfer_max_contents_g'],prior_transfer_gap_g=o['transfer_reduction_needed_g'],booked_assembly_delta_g=0,
        complete_mechanism_mass_verified=False),
        electrical=dict(target_pad_face_y_mm=target_y,compression_with_tolerance_and_high_beam_deflection_mm=strokes,
            stays_within_catalog_stroke=0<min(strokes) and max(strokes)<e['max_stroke_mm'],
            power_contact_pair_drop_v=2*r*current,power_contact_pair_loss_w=2*r*current**2,
            contact_force_nominal_n=contact_force,all_enables_default_off=True),
        mechanical=dict(gasket_force_cases=pressures,nominal_mating_force_n=seal_load,high_mating_force_n=max_preload,
            one_lock_design_force_n=retained,lock_pin_single_shear_mpa=retained/pin_area,
            cheek_lock_bearing_mpa=retained/(cheek_engagement*d['locks']['pin_diameter']),
            fixed_receiver_bearing_mpa=retained/(body_engagement*d['locks']['pin_diameter']),
            minimum_key_engagement_with_axial_tolerance_mm=minimum_engagement,
            released_key_clearance_mm=cheek_begin-(key_end-key['withdrawal_mm']),
            rear_lock_ligament_mm=edge,cheek_rear_tearout_mpa=retained/(2*cheek_t*edge),
            crossmember_vertical=zdef,crossmember_seal=seal_bend,crossmember_high_seal=high_seal_bend,
            gasket_compression_fraction_range=[(compression-seal_stack)/a['gasket_free_t'],(compression+seal_stack)/a['gasket_free_t']],
            scope='Stress values are required capacities; material grade, notches, bolt pull-through, sleeve/rail bearing, latch housing, torsion/fatigue and full carrier joints remain unqualified. Foam pressure is a sensitivity input.'),
        exchange=dict(withdrawal_mm=d['withdrawal_mm'],last_tool_mating_face_y_mm=rear,
            separation_before_lateral_transfer_mm=d['withdrawal_mm']-rear,
            longitudinal_robot_and_extension_mm=Odata['space']['stowed_rigid_outline_mm'][1]+d['withdrawal_mm'],
            head_active_flex_length_mm=a['head_flex_active_y'][1]-a['head_flex_active_y'][0],
            proposed_guide_entry_before_power_contact_mm=d['cheeks']['left_min'][1]+d['cheeks']['size'][1]-max(d['guide_pins']['y'])-e['nominal_compression_mm']))


def report(r):
    m=r['mass'];q=r['mechanical'];e=r['electrical'];x=r['exchange']
    lines=['# Removable head coupling — P candidate','','The carrier slides forward out of four captured guide studs. Two spring-engaged cap-head keys prevent withdrawal; a supported dock tool retracts both. Each key bridges the removable cheek and a fixed steel receiver bore, so retention does not depend on bending a small threaded shank. Normal-head floor following is downstream of this fixed carrier. The extension connects the same carrier to its own supported hitch.','',
        '**Candidate status:** interface geometry and electrical contract; not a fabrication release or completed head suspension. O/M complete mass estimates remain unchanged.','',
        '## Mass ownership','','| Scope | Detailed nominal / reserved | Existing allocation |','|---|---:|---:|',
        f"| Body interface, including still-allowed latch/contact details | {m['detailed_body_scope_g']:.2f} g | {m['body_budget_g']:.2f} g |",
        f"| Removable fixed carrier and mating half | {m['detailed_carrier_scope_g']:.2f} g | {m['carrier_budget_g']:.0f} g |",
        f"| Unfinished normal-head compliance | {m['remaining_head_compliance_g']:.0f} g reserved | Within prior M mount |",
        f"| Existing normal-head lift | {m['head_lift_retained_g']:.0f} g retained | Prior M lift |",'',
        f"The 70 g carrier allocation combines O's 15 g adapter and 55 g of M's 90 g mount. That leaves **35 g for unresolved normal-head compliance**. The combined carried allowance remains {m['after_combined_budget_g']:.2f} g, exactly the previous {m['before_combined_budget_g']:.2f} g. This is a scope assignment, not a demonstrated weight reduction. If the remaining mechanism exceeds its allocation, redesign the shared head/frame before claiming budget closure.",'',
        f"Transfer remains **{m['prior_transfer_mass_g']/1000:.3f} kg / 4.5 kg**, requiring {m['prior_transfer_gap_g']:.0f} g reduction. No extra saving from parking the lift/compliance or consolidating the extension adapter is booked until their installed geometry is complete.",'',
        '## Mating and release','','- Keep the 275 mm body width. Cheeks sit outside the side rails; a rear tube joins them below the power hardware. The candidate raises H_front_bridge 1.5 mm to clear that tube. Its attachment holes and full bridge joints require integration.',
        '- Rear-open slots capture four 4 mm sleeves. Left closed slot end sets insertion depth; the right end has 0.5 mm relief to avoid two competing axial stops. The right side still requires a lateral float/shim strategy to accommodate rail spacing tolerances.',
        '- Two nominal 3.8 mm diameter, 2 mm long M2 socket-head keys engage at Y76/Z70. At the left joint the head spans X23.2–25.2: 1.0 mm engagement in the removable cheek and 0.7 mm in the fixed receiver, across a 0.3 mm gap. A 3 mm outward stroke clears the cheek. The thin engagement, screw chamfers/tolerances, preload spring, captive pull nuts and guide need validation. The fixed receiver bore must carry the transverse load; the threaded shank only actuates the key.',
        '- Dock support must carry the head and locate its floating portion level before release. The locks retain the carrier, not the free-moving brush body. Tool power must be isolated before the dock pulls the pins.',
        f"- Withdraw **{x['withdrawal_mm']} mm** along negative Y before moving toward a storage nest. The rearmost mating face clears the body front by {x['separation_before_lateral_transfer_mm']:.1f} mm. Robot plus withdrawing extension occupies **{x['longitudinal_robot_and_extension_mm']:.0f} mm** before margins, separate from confirmed sofa space.",'',
        '## Air joint','','Move the fixed air flange rearward to Y96–99 and start the retained fixed duct at Y104, keeping its rear end unchanged. The removable flange ends at Y94; a 3 mm replaceable foam gasket compresses into the 2 mm gap. The clear bore stays 32 × 22 mm, and the gasket opening is 34 × 24 mm so its edges start outside the air passage. The actual gasket must resist inward deformation and release cleanly.','',
        f"The working-head flex retains {x['head_active_flex_length_mm']:.0f} mm nominal axial length (Y66–91). Its working/raised bend, compression, fatigue and hair passage remain unresolved. The seal is on the fixed carrier interface; floor-following motion belongs in the upstream flex. Avoid a sliding dirty-air O-ring through the hair stream.",'',
        f"At assumed gasket compression pressures of 10/25/50 kPa, seal forces are {[round(v['force_n'],1) for v in q['gasket_force_cases']]} N. Eight contacts add {e['contact_force_nominal_n']:.1f} N nominal. Combined nominal mating force is {q['nominal_mating_force_n']:.1f} N; the high screen including +30% contact-force sensitivity is {q['high_mating_force_n']:.1f} N. These foam values are design sensitivities, not a selected gasket specification.",'',
        '## Electrical interface','','Use eight protected spring contacts against replaceable hard-gold target pads. Contacts mate along Y, separately from the dirty-air seal, at X178/186/194/202 and Z54/60. Set the body-board front at Y107 and pad face at Y98.186. Locator engagement precedes contact. All pins have equal length: do not claim ground-first sequencing. Keep both supplies off while mating. After seating and both locks are confirmed, enable limited logic power for ID/communication checks, then enable tool driver power.','',
        '| Front-view row | Pin 1 | Pin 2 | Pin 3 | Pin 4 |','|---|---|---|---|---|',
        '| Z54, left to right | 12 V tool | Power return | 5 V logic | Logic return |',
        '| Z60, left to right | CAN H | CAN L | Hardware enable | ID/presence |','',
        'Use a fused/current-limited 12 V branch (4 A candidate) and 5 V logic (0.25 A candidate). Identify the tool on limited logic power before enabling its driver supply. The normal roller reference has a 5 A stall extrapolation, so motor current limiting and pickup/starting torque still need validation; a 4 A branch is not permission to stall it. Local CAN controller/driver-enable gating, encoder acquisition and an ID resistor are part of the carrier electronics allowance. No Pi timing dependency or direct motor phases cross this connector.','',
        'Provide unpowered high-impedance CAN behavior, local pull-down of enable, a heartbeat timeout and current/voltage monitoring. Terminate the short bottom-to-tool CAN segment at its two ends; do not add a third terminator to the core bus. Use a dedicated bus segment or controller interface that actually supports this topology. No firmware/PCB is released here.','',
        f"The reference contact is Mill-Max **0860-0-15-20-82-14-11-0**. Its November 2022 manufacturer sheet gives 9.957 mm free height, 2.286 mm maximum stroke, 20 mΩ maximum contact resistance and 7.2 A derated current. At the proposed 4 A tool limit the two power contacts contribute up to {e['power_contact_pair_drop_v']:.2f} V drop and {e['power_contact_pair_loss_w']:.2f} W total. Individual-contact catalog limits do not qualify the assembled bank. [Manufacturer datasheet](https://www.mouser.com/catalog/specsheets/Mill-Max_0860-0-15-20-82-14-11-0.pdf).",'',
        f"Proposed compression is 1.143 mm. Including ±0.3 mm stack tolerance and high-load calculated beam deflection gives {e['compression_with_tolerance_and_high_beam_deflection_mm'][0]:.2f}–{e['compression_with_tolerance_and_high_beam_deflection_mm'][1]:.2f} mm, within the listed stroke. Confirm spring force, plated-pad wear, dust protection, PCB mounting and thermal behavior. The earlier April 2022 copy contains inconsistent stroke/derating entries and is not used.",'',
        '[Roller motor reference](https://www.pololu.com/product/4842/specs) · [Feed motor reference](https://www.pololu.com/product/4845/specs) · [Existing motor driver reference](https://www.pololu.com/product/2997/specs)','',
        '## Local load screen','',
        f"With {q['one_lock_design_force_n']:.1f} N assigned to a single lock (40 N fore-aft plus high mating preload), required key shear is {q['lock_pin_single_shear_mpa']:.1f} MPa, cheek bearing {q['cheek_lock_bearing_mpa']:.1f} MPa, fixed receiver bearing {q['fixed_receiver_bearing_mpa']:.1f} MPa and simple rear-edge tear-out stress {q['cheek_rear_tearout_mpa']:.1f} MPa. Minimum engagement after ±0.2 mm axial variation is only {q['minimum_key_engagement_with_axial_tolerance_mm']:.1f} mm. Check actual cap chamfers/hardness and bearing length before using this key concept. These numbers do not qualify the purchased screw, engagement tolerances, support housing or the thin rail joint.",'',
        f"The ideal tube calculation gives {q['crossmember_vertical']['deflection_mm']:.2f} mm at a 50 N central vertical load and {q['crossmember_seal']['deflection_mm']:.2f} mm under nominal mating force. Connections and torsion are excluded; no head/robot lifting certification follows. Gasket compression including the high-load beam movement and stack allowance spans {100*q['gasket_compression_fraction_range'][0]:.0f}–{100*q['gasket_compression_fraction_range'][1]:.0f}% and needs a compatible material/force curve.",'',
        'The CAD checks solids and sampled head positions, not the unfinished active flex, all fastener heads or continuous threshold motion. See the generated CAD check JSON for every remaining overlap rather than assuming the study passed.','',
        '[Design record](../../../docs/HEAD_COUPLING.md) · [Interactive coupling](head_coupling.html) · [Drawing](head_coupling.svg) · [Mass rows](head_coupling_mass.csv) · [CAD checks](head_coupling_cad_checks.json)']
    return '\n'.join(lines)+'\n'


def main():
    r=study();OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'head_coupling.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'head_coupling.md').write_text(report(r))
    with (OUT/'head_coupling_mass.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['owner','id','mass_g','basis']);w.writeheader();w.writerows(r['rows'])
    print(json.dumps(dict(mass=r['mass'],electrical=r['electrical'],mechanical=r['mechanical'],exchange=r['exchange']),indent=2))


if __name__=='__main__':main()
