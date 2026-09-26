# Whole-system engineering budget

Revision C-review, 2026-09-13. Preliminary design, not measured performance.

All masses include the stated battery and contents. Low/high are engineering bounds, not statistical intervals. A complete bottom includes its own wheels and controls.

Revision C baseline: lift layouts and the wheeled horizontal duster below remain comparison evidence. The preferred wheel-less duster, raised boom, compact duct targets and round-trip mission budget are in the [revision D airborne supplement](airborne_dusting.md) and [interactive comparison](airborne_dusting.html). See [LIFT_LAYOUT_REVIEW.md](../../../docs/LIFT_LAYOUT_REVIEW.md) for earlier size drivers.

## Loaded floor configurations

| Bottom + core + cap | Low / nominal / high kg | Normal / high battery W | 6S example runtime min | Level-floor nominal support margin mm |
|---|---:|---:|---:|---:|
| Everyday vacuum / drive | 3.56 / 4.68 / 6.29 | 115.9 / 195.2 | 48 | 10.4 |
| Oscillating mop / drive | 3.66 / 4.58 / 5.93 | 58.0 / 122.7 | 96 | 29.0 |
| Under-sofa vacuum / drive | 3.77 / 4.96 / 6.79 | 122.0 / 190.8 | 45 | 14.2 |
| Extended duster / drive | 3.69 / 4.88 / 6.71 | 90.0 / 190.8 | 62 | 13.1 |

Runtime uses 80% nominal energy and assumed average loads, including conversion losses. A battery with adequate energy may still fail flight-current or packaging requirements.

## Module hardware masses without bare cells or contents

| Module | Low / nominal / high kg |
|---|---:|
| core | 1.143 / 1.579 / 2.226 |
| cap | 0.045 / 0.070 / 0.100 |
| vacuum | 1.525 / 2.124 / 2.844 |
| mop | 1.367 / 1.778 / 2.332 |
| low | 1.762 / 2.433 / 3.390 |
| dust | 1.747 / 2.428 / 3.410 |
| quad10 | 1.782 / 2.421 / 3.352 |
| hex10 | 2.271 / 3.052 / 4.190 |
| octo10 | 2.737 / 3.651 / 4.982 |

## Lift comparisons at 21 V and assumed 75% retained thrust

| Bottom | Top | Complete nominal / high kg | Nominal / high-mass thrust:weight | Estimated hover W / A | Departure reserve Wh |
|---|---|---:|---:|---:|
| vacuum | quad10 | 7.03 / 9.54 | 1.52 / 1.12 | 2593.1 / 123.5 | 72.6 |
| vacuum | hex10 | 7.66 / 10.38 | 2.09 / 1.54 | 2486.6 / 118.4 | 69.6 |
| vacuum | octo10 | 8.26 / 11.17 | 2.59 / 1.91 | 2450.5 / 116.7 | 68.6 |
| mop | quad10 | 6.93 / 9.18 | 1.54 / 1.16 | 2545.5 / 121.2 | 71.3 |
| mop | hex10 | 7.56 / 10.02 | 2.12 / 1.60 | 2444.8 / 116.4 | 68.5 |
| mop | octo10 | 8.16 / 10.81 | 2.62 / 1.98 | 2408.7 / 114.7 | 67.4 |
| low | quad10 | 7.31 / 10.04 | 1.46 / 1.06 | 2731.4 / 130.1 | 76.5 |
| low | hex10 | 7.94 / 10.88 | 2.02 / 1.47 | 2608.3 / 124.2 | 73.0 |
| low | octo10 | 8.54 / 11.67 | 2.50 / 1.83 | 2572.2 / 122.5 | 72.0 |
| dust | quad10 | 7.23 / 9.96 | 1.48 / 1.07 | 2694.2 / 128.3 | 75.4 |
| dust | hex10 | 7.86 / 10.80 | 2.04 / 1.48 | 2575.6 / 122.6 | 72.1 |
| dust | octo10 | 8.46 / 11.59 | 2.52 / 1.84 | 2539.5 / 120.9 | 71.1 |

The 2:1 sizing target is provisional. Guard loss and voltage scaling are unverified. Hover power comes from interpolation at required equivalent open-rotor thrust, plus 10% installation/electrical power overhead and flight electronics. These are coupled assumptions, not a measured flight curve.

Departure reserve includes 45 s transfer at 1.2 times estimated hover power, 30 s landing reserve, then 20% energy margin. It is an illustrative mission allocation, not an approved flight policy. Tool motors are off during transfer. Airborne dusting adds tool power and uses the extended configuration.

## Packaging and compatibility

- vacuum: 51 root allocations, 0 numerical conflicts.
- mop: 44 root allocations, 0 numerical conflicts.
- low: 51 root allocations, 0 numerical conflicts.
- dust: 51 root allocations, 0 numerical conflicts.
- design_6s: bare pack can fit the cartridge cell pocket in some orientation: True; reference-axis clearance [2.5, 13.5, 3] mm. Installed cartridge fit is unqualified.
- design_8s: bare pack can fit the cartridge cell pocket in some orientation: True; reference-axis clearance [2, 15, -8] mm. Installed cartridge fit is unqualified.
- quad10: [644, 844, 180] mm; width with 2° yaw and 25 mm lateral allowance each side 723.1 mm versus conservative 774.7 mm stair corridor. Remaining width 51.6 mm.
- hex10: [644, 1424, 180] mm; width with 2° yaw and 25 mm lateral allowance each side 743.3 mm versus conservative 774.7 mm stair corridor. Remaining width 31.4 mm.
- octo10: [644, 1444, 180] mm; width with 2° yaw and 25 mm lateral allowance each side 744.0 mm versus conservative 774.7 mm stair corridor. Remaining width 30.7 mm.
- Lift/base static allocation checks include cameras, controller and beam routes. Guard/box checks use disk distance, not only rectangular bounds; dynamic swept volumes and clamp details remain excluded.

## Traction and transitions

| Bottom | Level-floor torque per wheel N·m | 10 mm step wheel torque N·m | Caster-climb assumed minimum floor friction | Mass/position-bound support margin mm |
|---|---:|---:|---:|---:|
| vacuum | 0.073 | 0.516 | 0.17 | -16.4 |
| mop | 0.117 | 0.410 | 0.53 | 5.9 |
| low | 0.076 | 0.526 | 0.23 | -13.6 |
| dust | 0.075 | 0.524 | 0.22 | -15.7 |

The transition model excludes tire deformation and impact. Wet coefficients are assumptions; a nominal torque pass is not a traction qualification. Inspect the uncertainty result, not only nominal CG.

## Extension

- 1000 mm travel; 1245 mm guide length; 980.0 mm useful depth after 80 mm stand-off.
- One-way stroke 20 s at 50 mm/s. Nominal moving height 40 mm; transit lifts the assembly 12 mm.
- Estimated added duct loss 155 Pa at 3.6 L/s: 18 Pa straight + 137 Pa fittings/contractions. Leakage, nozzle and filter excluded.

## Automatic station allowance

- Per floor: 4.08 m² including approach; five bottom positions plus intact lift-top parking.
- Machinery allowance: 58.9 kg empty, excluding spare robot modules and bulk contents.
- Water recipe per 1000 ft²: 1.48 L for wood or 1.76 L for tile, including ten pad washes.
- 280 W DC supply allocation; charge and motion interlocked. 800 W mains evacuation is a separate appliance load.

## Automatic battery exchange

- 2 spare packs and 4 bays per floor; 5 packs across two floors including the one carried. Extra bays receive the returning pack and preserve recovery space.
- Cartridge tare: 140 g nominal, already included once in the core hardware subtotal. Loaded 6S example cartridge: 893 g. Stored spares add 1.79 kg per station, outside robot mass.
- Fixed receiver and dock logic-power hardware are also included in the carried core. Battery chemistry, capacity and current capability remain open.
- The 180 W total charge-input allowance gives 129.6 W average to cells at assumed 90% conversion and 80% charge-enabled time. This is an energy ceiling; charge acceptance can reduce it.
- Two resident spares give each depleted pack two robot runs to recover. Recovery includes cooling, power sharing, charge taper and balancing; the following counts assume that recovery time is actually achieved.

| Floor task | Run min | Charge-energy margin W | Total local packs for 60 / 90 / 120 min recovery |
|---|---:|---:|---:|
| vacuum | 48 | 13.7 | 3 / 3 / 4 |
| mop | 96 | 71.6 | 2 / 2 / 3 |
| low | 45 | 7.6 | 3 / 3 / 4 |
| dust | 62 | 39.6 | 2 / 3 / 3 |

Positive average energy margin is necessary, not proof of uninterrupted service. Flight scheduling must budget transfer/dusting energy separately; spare packs do not extend a single airborne sortie.

- Battery rack/core-withdrawal allocation conflicts: 0. This check excludes detailed contacts, gripper geometry and the complete moving gantry.
- See [BATTERY_EXCHANGE.md](../../../docs/BATTERY_EXCHANGE.md) for the mechanism, power handover, reserve policy and failure recovery.

## Open engineering gates

- Automatic battery exchange is required. Cartridge contacts/retention, cell monitoring, no-break dock logic power and independently supervised rack charging need electrical/mechanical detail; extra packs are not a no-wait guarantee.
- Both battery packs remain comparisons. The 8S bare body fits only after rotating it onto its 47 mm side; installed restraint/lead clearance is unverified. It exceeds the selected lift motor voltage; do not substitute it in that propulsion curve.
- TriCut stationary restraint, drive end, safe speed and cutter loading are not public dimensions. The cassette and drive are sized, but the interface insert needs the supplied brush or a supplier drawing.
- Actual filter body/seal and clean/loaded pressure drop are unavailable. The maximum element allocation is not a measured filter.
- Guard losses, hot/low-voltage motor performance, airflow near stairs and dynamic pet avoidance are unqualified. Current sizing results are screening cases.
- Cell protection, regenerative clamp and automatic mating power contacts need schematic/PCB/thermal validation; IC/connector families are not finished subsystems.
- The guided push strip, printed sliding air seals and telescope retrieval force need mechanical qualification; the reach calculation does not prove jam-free deployment.
- Distributed frame/fastener/wiring mass is included, but production frame geometry and complete stress/creep checks are not finished.
- Owner considers 644 x 1444 mm excessive: reopen lift packing and mass. Ceiling-fan target is now 2134 mm high, 305 mm below ceiling, with about 610 mm tool reach; current horizontal dust geometry does not implement fan access.
- Autonomous station motions, floor navigation and flight estimators are specified as hardware/control contracts; no claim of implemented autonomy.

See [SYSTEM_DESIGN.md](../../../docs/SYSTEM_DESIGN.md) for interfaces, mechanisms, source limits, electrical branches and the complete station sequence.
