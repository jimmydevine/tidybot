# Mass growth audit — G through M

2026-09-14. The owner challenged the increasing weight. This audit changes no hardware masses and credits no savings. K/M are comparison candidates pending a simpler integrated design.

All rows below include the same 753 g cell-pack reference, 70 g cap and nominal contents: 150 g debris for vacuum; 350 g tank water plus 50 g pad water for mop. Battery cartridge hardware is already inside the core subtotal. A lift top is not included.

| Stage | Vacuum | Mop | Change |
|---|---:|---:|---|
| G | 4.777 kg | 4.491 kg | Frame candidate; 62 g allowance per wheel pod |
| K | 5.142 kg | 4.856 kg | Detailed local pod assemblies replace the two 62 g entries |
| M | 5.316 kg | 4.954 kg | Additional floating-head mount/lift/riser allowances |

| Increase | Vacuum | Mop |
|---|---:|---:|
| G → K | 365.0 g | 365.0 g |
| K → M | 174.0 g | 98.0 g |
| G → M | 539.0 g | 463.0 g |

## M total, reconciled

| Included group | Vacuum | Mop |
|---|---:|---:|
| core | 1347.1 g | 1347.1 g |
| drive | 1564.9 g | 1564.9 g |
| vacuum | 795.0 g | 0.0 g |
| air_common | 462.0 g | 0.0 g |
| mop | 0.0 g | 721.0 g |
| cap | 70.0 g | 70.0 g |
| battery | 753.0 g | 753.0 g |
| contents | 150.0 g | 400.0 g |
| M additions | 174.0 g | 98.0 g |

The shared core subtotal includes the 140 g cartridge tare and 50 g fixed receiver. The drive group includes frame, suspension, wheel/motor/hub hardware, support caster, electronics, wiring and power-carrier stock. Vacuum cleaning hardware spans vacuum and air_common; group names are accounting categories, not physically separate extra modules.

## Priority mass entries

| Item | Nominal mass | Accounting/design issue |
|---|---:|---|
| Two K suspension pods | 489.0 g | Excludes drive motors, wheels and hubs; includes local fixed supports. Review the load path and integrate it with the chassis. |
| Bottom frame | 225 g | Older complete frame allowance remains beside detailed local pod/support hardware; ownership needs reconciliation. |
| Vacuum head frame | 135 g | Description already includes suspension, springs and captive hardware; M adds a separate 90 g mount allowance. The overlap is unquantified. |
| Mop pad/carrier | 105 g | Includes floating carrier and leaf springs; M adds 80 g for a mount. The overlap is unquantified. |
| M vacuum lift / risers | 62 / 22 g | New mechanism and packaging consequences; determine whether powered vacuum-head lift is necessary. |
| M mop risers | 18 g | Added after the lift/head layout conflicted with the tank. Integrate tank retention with the chassis. |
| Mop dosing pump | 200 g | Documented reference, but not established as the lightest pump that meets dosing/leak requirements. |
| Shared core printed supports / harness | 160 / 125 g | Effective-volume and routing allowances; unfinished geometry and cable ownership. |

## Interpretation

The increases combine real growth in the chosen mechanism with unresolved allowance ownership. Neither the full increase nor the entire older allowance can be called double-counted. The CAD mass of the current pods also does not establish that this architecture is necessary or near the minimum weight.

M has no detailed guide/lift geometry despite adding its mass allowances. Passing its allocation checks is not evidence of a finished, mass-efficient mechanism. The next task is to compare simpler integrated construction and establish one installed mass per physical item before extending the candidate.

The existing load, retention, floor-following and cleaning requirements remain. A lighter design must achieve them through a better load path and fewer separate parts. A smaller battery, less water, weaker guards or poorer cleaning are not credited as equivalent-performance savings.

[Corrective design direction](../../../docs/MASS_OPTIMIZATION_REVIEW.md) · [Complete row ledger](mass_growth_ledger.csv)
