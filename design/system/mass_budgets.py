"""Apply owner budgets to complete non-lift assemblies without changing masses.

Separate from historical geometry configs so adding a requirement does not
invalidate unchanged CAD or imply that a mass-over-budget design was repaired.
"""
import csv
import json
from pathlib import Path
import airborne_study as E
import build as B
import fixed_drive as N
import floating_heads as M
import floor_support as H
import sofa_attachment as O

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'


def read():return json.loads((ROOT/'config/mass_budgets.json').read_text())


def included_mass(rows,index=1,cap_removed=True):
    excluded={'lift'} | ({'cap'} if cap_removed else set())
    return sum(row['mass_g'][index] for row in rows if row['module'] not in excluded)


def comparison(id,label,bottom,usual_g,loaded_g,upper_g,usual_contents_g,max_contents_g,cap_g,basis,d):
    role=d['module_classes'][bottom];limit=d['classes'][role]['budget_g']
    return dict(id=id,label=label,bottom=bottom,flight_class=role,budget_kind=d['classes'][role]['kind'],budget_g=limit,
        usual_contents_g=usual_contents_g,max_modeled_contents_g=max_contents_g,
        usual_mass_g=usual_g,max_contents_mass_g=loaded_g,
        upper_hardware_and_max_contents_g=upper_g,removed_cap_nominal_g=cap_g,
        usual_reduction_needed_g=max(0,usual_g-limit),
        reduction_needed_g=max(0,loaded_g-limit),headroom_g=limit-loaded_g,
        nominal_hardware_with_max_contents_within_budget=loaded_g<=limit,
        upper_estimate_within_budget=None if upper_g is None else upper_g<=limit,
        measured_compliance=False,flight_qualified=False,basis=basis)


def floor_case(bottom,revision,d):
    p=M.prepare(bottom);rows=B.assembly(p['layout'],bottom,payload=False)['rows']
    cap=sum(row['mass_g'][1] for row in rows if row['module']=='cap')
    cases=p['config']['contents'][bottom]
    usual=sum(v[0] for v in cases[p['config']['calibration_contents_index'][bottom]]['loads'])
    maximum=max(sum(v[0] for v in case['loads']) for case in cases)
    dry=p['dry_mass_g']-cap
    if revision=='N':
        _,a=N.nominal_mass(bottom,N.read())
        usual_mass=a['mass_g']-cap;loaded=usual_mass-usual+maximum
        # N supplies one nominal replacement mass. Do not silently reuse the
        # nominal value as its high hardware bound or import K's removed bound.
        upper=None
        basis='N fixed-mount candidate, all remaining M allowances retained; N replacement has no defined upper mass interval. Head-motion and joint changes remain unresolved.'
    elif revision=='M':
        usual_mass=dry+usual;loaded=dry+maximum
        high=M.prepare(bottom,index=2)
        high_rows=B.assembly(high['layout'],bottom,payload=False)['rows']
        upper=high['dry_mass_g']-sum(row['mass_g'][2] for row in high_rows if row['module']=='cap')+maximum
        basis='M independent-suspension and floating-head comparison, with its additional mount/lift/riser allowances.'
    else:raise ValueError(revision)
    return comparison(revision+'_'+bottom,revision+' '+bottom,bottom,usual_mass,loaded,upper,usual,maximum,cap,basis,d)


def study():
    d=read();cases=[floor_case(b,rev,d) for rev in ('N','M') for b in ('vacuum','mop')]
    # Both floors retain an extension. Only the ordinary vacuum and completed
    # quick-change interface are carried between floors; no duplicate tool mass.
    om=O.study()['mass']
    cases.append(comparison('O_vacuum','O vacuum / resident sofa attachment','vacuum',
        om['transfer_usual_contents_g'],om['transfer_max_contents_g'],None,
        om['usual_contents_g'],om['max_contents_g'],om['removed_cap_g'],
        'N vacuum with O automatic-head interface allowance and normal head installed. One extension remains at each floor station; no extension flies. N mechanics and O quick-change joints remain unresolved; whole-hardware upper bound undefined.',d))
    # Sofa has K accounting, not a validated application of N's fixed mounts.
    c=M.prepare('vacuum')['layout'];a=B.assembly(c,'low',payload=False)
    usual=c['bottoms']['low']['payload_g'];maximum=c['bottoms']['low']['payload_high_g']
    cap=sum(v['mass_g'][1] for v in a['rows'] if v['module']=='cap')
    cases.append(comparison('K_low','K sofa vacuum','low',included_mass(a['rows'])+usual,
        included_mass(a['rows'])+maximum,included_mass(a['rows'],2)+maximum,usual,maximum,cap,
        'Latest K sofa mass model; N fixed mounts and M head additions have not been integrated with this bottom.',d))
    ad=E.read();ac=E.configured(H.baseline(),ad);a=E.air_assembly(ac,ad)
    usual=ad['payload_g'][1];maximum=ad['payload_g'][2]
    cap=sum(v['mass_g'][1] for v in a['rows'] if v['module']=='cap')
    cases.append(comparison('G_E_air_dust','G/E airborne duster','air_dust',included_mass(a['rows']),
        included_mass(a['rows'])-usual+maximum,included_mass(a['rows'],2),usual,maximum,cap,
        'Wheel-less E duster on the F/G core and frame. Latest M core placement changes are not mechanically integrated; no mass-saving credit from them. Upper figure is the sum of modeled high estimates, not a measured tolerance bound.',d))
    return dict(requirements=d,cases=cases,primary_case_ids=['O_vacuum','N_mop','G_E_air_dust'],
        scope='Budget audit. O adds a candidate interface scope to N and leaves one sofa extension on each floor. Historical candidate masses are preserved. Maximum modeled contents are planning loads; permitted operational limits and measured weights remain to establish.')


def report(r):
    lines=['# Flight-carried mass budget check','','Owner requirements: **4.5 kg maximum for transfer flights; 3.5 kg design target for sustained hovering work.** Both exclude the complete lift module and include the core, battery/cartridge, attached tool/drive module and carried contents.','',
        'The previous floor totals included a cap. This comparison removes that cap because the lift top replaces it; the nominal deduction is 70 g. Hardware that remains aboard is always counted.','',
        '## Latest applicable candidates','','| Configuration | Budget | Usual contents | Maximum modeled contents | Reduction needed / headroom |','|---|---:|---:|---:|---:|']
    for id in r['primary_case_ids']:
        c=next(v for v in r['cases'] if v['id']==id)
        change=f"{c['reduction_needed_g']:.0f} g over" if c['reduction_needed_g'] else f"{c['headroom_g']:.0f} g headroom"
        lines.append(f"| {c['label']} | {c['budget_g']/1000:.2f} kg | {c['usual_mass_g']/1000:.3f} kg | {c['max_contents_mass_g']/1000:.3f} kg | {change} |")
    lines+=['','Both mass columns use nominal hardware. Contents assumptions: vacuum 150/300 g debris; mop 400/450 g including tank and wet/saturated pad; sofa 120/250 g debris; duster 15/30 g retained dust. The larger case is the maximum currently modeled, not a measured load-capacity rating.','',
        'O uses one resident extension per floor. The extension is parked and the ordinary head restored before flight, so vacuum and sofa missions share the same transfer configuration. O includes 108.84 g of added interface/head-adapter allowance. N remains conditional on head motion, joints and mop traction. K is retained below as the prior dedicated-sofa comparison; its mass has not been revised. The duster uses the wheel-less E tool with the F/G core.','',
        '## Hardware uncertainty and prior construction','','| Candidate | Nominal hardware + maximum contents | High hardware + maximum contents | Budget |','|---|---:|---:|---:|']
    for c in r['cases']:
        hi='Not defined for complete candidate' if c['upper_hardware_and_max_contents_g'] is None else f"{c['upper_hardware_and_max_contents_g']/1000:.3f} kg"
        lines.append(f"| {c['label']} | {c['max_contents_mass_g']/1000:.3f} kg | {hi} | {c['budget_g']/1000:.2f} kg |")
    dust=next(v for v in r['cases'] if v['bottom']=='air_dust');gap=dust['budget_g']-dust['upper_hardware_and_max_contents_g']
    lines+=['',f"The airborne duster has nominal room under the target, but its modeled high estimate leaves only **{gap:.0f} g**. That is effectively no room for further growth at the high estimate. Preserve nominal headroom for uncertainty and unfinished details; it is not permission to add hardware up to 3.5 kg.",'',
        '## Design gate','','Every subsequent mass comparison must show its flight class, complete non-lift mass at maximum permitted contents, remaining headroom and uncertainty. A design above the applicable budget remains a redesign candidate. A nominal estimate below it is a mass-screen result, not measured compliance. Missing hardware or undefined uncertainty stays explicit.','',
        '**Actual takeoff mass = non-lift carried assembly + complete lift module.** At the ceiling this is 4.5 kg + lift for transfer or 3.5 kg + lift for hover. Propulsion sizing must still include its own structure, guards, controllers, wiring and any lift-owned energy storage, together with the full carried load. These budgets alone do not settle battery capacity, thrust or hover duration.','',
        'A module used for both transfer and sustained airborne cleaning must meet the hover target in its hovering configuration. Any removed mass must actually remain at a station. Preserve cleaning performance, capacities and automatic exchange while redesigning; moving a line item between accounting groups cannot create a physical saving.','',
        '[Owner mass requirements](../../../docs/MASS_BUDGETS.md) · [Machine-readable limits](../../../config/mass_budgets.json) · [Weight-reduction work](../../../docs/MASS_OPTIMIZATION_REVIEW.md)']
    return '\n'.join(lines)+'\n'


def main():
    r=study();OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'mass_budgets.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'mass_budgets.md').write_text(report(r))
    with (OUT/'mass_budgets.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(r['cases'][0]));w.writeheader();w.writerows(r['cases'])
    for c in r['cases']:print(c['label'],round(c['max_contents_mass_g'],1),'g /',c['budget_g'],'g budget; headroom',round(c['headroom_g'],1),'g')


if __name__=='__main__':main()
