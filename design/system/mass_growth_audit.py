"""Reconcile G -> K -> M growth without crediting speculative weight savings."""
import csv
import json
from collections import defaultdict
from pathlib import Path
import build as B
import floor_support as H
import floating_heads as M
import suspension_springs as L

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'


def audit():
    results={};ledger=[]
    for bottom in ('vacuum','mop'):
        p=M.prepare(bottom);md=p['M']['modules'][bottom]
        contents=p['config']['contents'][bottom][p['config']['calibration_contents_index'][bottom]]['loads']
        payload=sum(v[0] for v in contents)
        ga=B.assembly(H.baseline(),bottom,payload=False)
        ka=B.assembly(p['layout'],bottom,payload=False)
        stages={'G':ga['mass_g'][1]+payload,'K':ka['mass_g'][1]+payload,'M':p['dry_mass_g']+payload}
        rows=[]
        for row in ka['rows']:
            rows.append(dict(configuration=bottom,instance=row['instance'],module=row['module'],
                hardware_id=row['hardware_id'],mass_g=row['mass_g'][1],basis=row['mass_basis']))
        for key in ('mount_allowance_g','lift_addition_g','riser_addition_g'):
            rows.append(dict(configuration=bottom,instance='M:'+key,module='M additions',hardware_id=key,
                mass_g=md[key][1],basis='Additional planning allowance; prior head/frame/support budgets retained'))
        rows.append(dict(configuration=bottom,instance='contents',module='contents',hardware_id='contents',
            mass_g=payload,basis='Same nominal debris or tank/pad-water load in G, K and M'))
        subtotals=defaultdict(float);hardware=defaultdict(float)
        for row in rows:
            subtotals[row['module']]+=row['mass_g'];hardware[row['hardware_id']]+=row['mass_g']
        assert abs(sum(row['mass_g'] for row in rows)-stages['M'])<1e-8
        assert abs(stages['K']-stages['G']-(hardware['pod']-124))<1e-8
        assert abs(stages['M']-stages['K']-subtotals['M additions'])<1e-8
        results[bottom]=dict(stages_g=stages,subtotals_g=dict(subtotals),hardware_g=dict(hardware),
            growth_since_G_g=stages['M']-stages['G'],growth_percent=100*(stages['M']/stages['G']-1))
        ledger.extend(rows)
    return results,ledger


def main():
    r,rows=audit()
    with (OUT/'mass_growth_ledger.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (OUT/'mass_growth_audit.json').write_text(json.dumps(r,indent=2)+'\n')
    lines=['# Mass growth audit — G through M','',
        '2026-09-14. The owner challenged the increasing weight. This audit changes no hardware masses and credits no savings. K/M are comparison candidates pending a simpler integrated design.','',
        'All rows below include the same 753 g cell-pack reference, 70 g cap and nominal contents: 150 g debris for vacuum; 350 g tank water plus 50 g pad water for mop. Battery cartridge hardware is already inside the core subtotal. A lift top is not included.','',
        '| Stage | Vacuum | Mop | Change |','|---|---:|---:|---|']
    for stage,desc in [('G','Frame candidate; 62 g allowance per wheel pod'),('K','Detailed local pod assemblies replace the two 62 g entries'),('M','Additional floating-head mount/lift/riser allowances')]:
        lines.append(f"| {stage} | {r['vacuum']['stages_g'][stage]/1000:.3f} kg | {r['mop']['stages_g'][stage]/1000:.3f} kg | {desc} |")
    lines+=['','| Increase | Vacuum | Mop |','|---|---:|---:|']
    for before,after in [('G','K'),('K','M'),('G','M')]:
        v=[r[b]['stages_g'][after]-r[b]['stages_g'][before] for b in ('vacuum','mop')]
        lines.append(f'| {before} → {after} | {v[0]:.1f} g | {v[1]:.1f} g |')
    lines+=['','## M total, reconciled','', '| Included group | Vacuum | Mop |','|---|---:|---:|']
    for group in ('core','drive','vacuum','air_common','mop','cap','battery','contents','M additions'):
        values=[r[b]['subtotals_g'].get(group,0) for b in ('vacuum','mop')]
        lines.append(f'| {group} | {values[0]:.1f} g | {values[1]:.1f} g |')
    lines+=['',
        'The shared core subtotal includes the 140 g cartridge tare and 50 g fixed receiver. The drive group includes frame, suspension, wheel/motor/hub hardware, support caster, electronics, wiring and power-carrier stock. Vacuum cleaning hardware spans vacuum and air_common; group names are accounting categories, not physically separate extra modules.',
        '', '## Priority mass entries','', '| Item | Nominal mass | Accounting/design issue |','|---|---:|---|',
        '| Two K suspension pods | 489.0 g | Excludes drive motors, wheels and hubs; includes local fixed supports. Review the load path and integrate it with the chassis. |',
        '| Bottom frame | 225 g | Older complete frame allowance remains beside detailed local pod/support hardware; ownership needs reconciliation. |',
        '| Vacuum head frame | 135 g | Description already includes suspension, springs and captive hardware; M adds a separate 90 g mount allowance. The overlap is unquantified. |',
        '| Mop pad/carrier | 105 g | Includes floating carrier and leaf springs; M adds 80 g for a mount. The overlap is unquantified. |',
        '| M vacuum lift / risers | 62 / 22 g | New mechanism and packaging consequences; determine whether powered vacuum-head lift is necessary. |',
        '| M mop risers | 18 g | Added after the lift/head layout conflicted with the tank. Integrate tank retention with the chassis. |',
        '| Mop dosing pump | 200 g | Documented reference, but not established as the lightest pump that meets dosing/leak requirements. |',
        '| Shared core printed supports / harness | 160 / 125 g | Effective-volume and routing allowances; unfinished geometry and cable ownership. |',
        '', '## Interpretation','',
        'The increases combine real growth in the chosen mechanism with unresolved allowance ownership. Neither the full increase nor the entire older allowance can be called double-counted. The CAD mass of the current pods also does not establish that this architecture is necessary or near the minimum weight.',
        '', 'M has no detailed guide/lift geometry despite adding its mass allowances. Passing its allocation checks is not evidence of a finished, mass-efficient mechanism. The next task is to compare simpler integrated construction and establish one installed mass per physical item before extending the candidate.',
        '', 'The existing load, retention, floor-following and cleaning requirements remain. A lighter design must achieve them through a better load path and fewer separate parts. A smaller battery, less water, weaker guards or poorer cleaning are not credited as equivalent-performance savings.',
        '', '[Corrective design direction](../../../docs/MASS_OPTIMIZATION_REVIEW.md) · [Complete row ledger](mass_growth_ledger.csv)']
    (OUT/'mass_growth_audit.md').write_text('\n'.join(lines)+'\n')
    for b,v in r.items():print(b, {k:round(x,1) for k,x in v['stages_g'].items()},'growth',round(v['growth_since_G_g'],1),'g')


if __name__=='__main__':main()
