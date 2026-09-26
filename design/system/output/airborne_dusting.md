# Airborne dusting and documented EDF comparison — revision E

The rear-mounted, wheel-less duster is the preferred lightweight bottom. None of the four-unit lift options below is selected for flight or procurement.

## Balance without ballast

Bottom hardware remains **481 g** nominal; complete quad aircraft **5.249 kg**. The boom root moves to x=165, y=283, z=36 mm. Its keyed socket is redesigned at the rear; the common electrical interface is unchanged. The station fits this rear boom, and flight approaches with the tool end leading.

The rear stereo camera moves to the left outboard bracket (allocation minimum −34.5, 278, 43 mm), opposite the right-side downward camera. The two cameras and flight controller now carry their mass at their physical allocations instead of a centered distribution. Counts and total mass are unchanged; mounting and cable routes remain to detail.

| Same mass and refined camera accounting | CG x / y | Balance-preserving peak thrust/weight |
|---|---:|---:|
| Front boom reference | 137.9 / 112.6 mm | 1.86:1 |
| Rear boom and left rear camera | 137.6 / 146.9 mm | 1.97:1 |

Body center is 137.5 / 137.5 mm. The largest static rotor share is now 25.86%. This still misses the provisional 2:1 target. Even perfect balance leaves only 89 g aggregate mass growth margin; high mass cases remain substantially worse. Revision D reported 1.81:1 using the older camera accounting; compare the two rows above to isolate this layout change.

Passive-foot nominal support margin with cap/core/pack is 109 mm. The tool still has 610 mm path, 439 mm horizontal root-to-contact reach and 345 mm contact height. The rear route clears the three retained lift/core allocation models. Full motion, optical coverage and structural joints are not validated.

## Propeller mission reference

| Lift top | Complete nominal / high mass | Hover estimate | Aggregate peak T/W | Local / longer-route cleaning |
|---|---:|---:|---:|---:|
| quad10 | 5.249 / 7.180 kg | 1734 W | 2.03:1 | 74 / 20 s |
| hex10 | 5.880 / 8.018 kg | 1723 W | 2.72:1 | 75 / 21 s |
| octo10 | 6.479 / 8.810 kg | 1804 W | 3.30:1 | 69 / 14 s |

Local dusting includes 20 s outbound, 20 s return and 30 s landing reserve; longer route has 45 s each way. Travel is 1.2× hover, contact flight 1.1× plus 2 W sensing. A 20% energy margin is applied to 92.352 Wh usable pack energy (80% of nominal 6S 5200 mAh). These are energy ceilings, not achieved endurance. Hex/octo still assume equal loads; the quad uses static trim. Do not rank tiny hover-power differences.

[Matched propeller source](https://www.hobbywing.com/en/uploads/file/20251117/2a4a3f326d2bdede135f3e582b73eef3.pdf). The model assumes 75% thrust retention, a 21 V peak-thrust screen and 10% power overhead. The highest source point is limited to 29 seconds. Neither guards nor continuous installed duty are qualified.

| Ground bottom carried intact by the same quad | Complete nominal mass | Aggregate peak T/W, before trim |
|---|---:|---:|
| Vacuum + contents | 7.027 kg | 1.52:1 |
| Mop + water | 6.931 kg | 1.54:1 |
| Under-sofa vacuum, stowed | 7.306 kg | 1.46:1 |

A lighter dusting bottom does not make this quad a universal top for stair transfers.

## Documented 89 mm EDF assemblies

Use the matched WeMoTec fan/motor assemblies as comparison evidence. Each listed source includes a stabilized-voltage sweep; it is not a fixed-6S partial-throttle test. Only interpolate within the published points. The supplied intake ring is included in mass. A 120 mm installed diameter is still a packaging target; motor protrusion, inlet/outlet guards, yaw hardware and installed height have not been resolved.

| Assembly | Fan + motor + inlet mass per unit | Source sample voltage / thrust / input |
|---|---:|---|
| [Midi Fan evo / HET 650-58-1970](https://shop.wemotec.com/Midi-Fan-evo-Impeller-HET-650-58-1970-komplett-montiert-feingewuchtet-und-harmonisch-abgestimmt) | 367 g | 14.8 V / 1.66 kgf / 718 W; 18.5 V / 2.48 kgf / 1332 W; 22.2 V / 3.20 kgf / 2020 W |
| [Midi Fan evo / HET 650-68-2000](https://shop.wemotec.com/Midi-Fan-evo-ducted-fan-unit-HET-650-68-2000-completely-assembled-precision-balanced-and-harmonically-tuned) | 421 g | 18.5 V / 2.81 kgf / 1443 W; 22.2 V / 3.68 kgf / 2398 W |

Complete installed-top accounting retains the existing common frame, harness and flight electronics. Each EDF gets a 100 g ESC allowance and 50 g protection/mount allowance; another 120 g is reserved for unresolved yaw-control hardware. These are engineering allowances, not selected products. No compact-frame weight saving is credited.

| Four-unit top | Installed low / nominal / high mass | Peak input-current screen at 21 V |
|---|---:|---:|
| Midi Fan evo / HET 650-58-1970 | 2.846 / 3.541 / 4.604 kg | 378 A |
| Midi Fan evo / HET 650-68-2000 | 3.062 / 3.757 / 4.820 kg | 439 A |

These peak-current estimates include 10% power overhead and core/flight electronics. They exceed the existing 150 A continuous / 320 A short-duration power-path allocations, which themselves remain unqualified. Controller amps are not battery capacity or guaranteed pack capability.

| EDF option / carried bottom | Complete nominal / high mass | Aggregate peak T/W at 21 V | Equal-load hover estimate |
|---|---:|---:|---:|
| HET 1970 / Airborne duster | 6.369 / 8.432 kg | 1.58:1 | 3902 W |
| HET 1970 / Vacuum + contents | 8.147 / 10.794 kg | 1.24:1 | 5625 W |
| HET 1970 / Mop + water | 8.051 / 10.432 kg | 1.25:1 | 5531 W |
| HET 1970 / Under-sofa vacuum, stowed | 8.426 / 11.290 kg | 1.20:1 | 5895 W |
| HET 2000 / Airborne duster | 6.585 / 8.648 kg | 1.75:1 | Unknown — below source samples |
| HET 2000 / Vacuum + contents | 8.363 / 11.010 kg | 1.38:1 | Unknown — below source samples |
| HET 2000 / Mop + water | 8.267 / 10.648 kg | 1.40:1 | Unknown — below source samples |
| HET 2000 / Under-sofa vacuum, stowed | 8.642 / 11.506 kg | 1.34:1 | Unknown — below source samples |

EDF results assume 85% delivered thrust after installation and 10% power overhead. The viewer also shows 70–100% retention sensitivity. Their different loss assumption does not imply EDF guards outperform propeller guards. Equal loads and unresolved yaw make the aggregate thrust an optimistic bound, not controlled lift capability. More than four units, other motors and other voltages have not been ruled out by this study.

The 1970 option needs an estimated **101.4 Wh usable** for the local dusting trip and landing reserve before any cleaning, exceeding 92.4 Wh available. A 45 s one-way stair transfer plus 30 s landing reserve needs about **157.5 Wh** carrying the vacuum, with energy margin. The stronger 2000 variant has no published hover-range samples for these loads, so its hover/endurance remains unknown; its thrust-margin failure is independently calculable.

**Yaw is a separate gate.** The cited EDF pages do not establish matched reverse-rotation units or net reaction torque. Do not reverse motor wiring and assume the fan retains its performance, or reuse the propeller quad mixer. A [stator-equipped ducted-aircraft study](https://www.mdpi.com/2076-3417/5/4/666) uses deflecting vanes for control. That supports investigating a dedicated control solution here, not transferring its performance or proving this EDF configuration.

## Design decision and next work

- Retain the rear, wheel-less duster with a station-removable microfiber tool. No ballast or extra battery has been added.
- Keep both small EDF variants as rejected four-unit candidates under the current mass, voltage and mission assumptions; do not purchase them for this robot.
- Continue the 150 mm hover-duct option as an open requirements target. Seek complete rotor/motor/duct/guard data, continuous hover duty, throttle response and a yaw solution; do not substitute RC-jet peak thrust for these data.
- Reduce common core and lift overhead next, because those masses are carried with every bottom. Preserve explicit allowances for protection, exchange locks and sensors.
- Size the universal transfer top against the loaded vacuum/mop/sofa bottoms separately from dusting duration. Multiple compatible top variants remain an option; none is selected.

At fixed pack energy, three minutes of local dusting still needs roughly 1 kW hover or less. A larger battery changes mass and must be recalculated. The station still needs its powered launch shuttle, supported exchanges, rear-boom handler and 90 × 160 × 700 mm vertical rack; no station motion is released for fabrication.

[Design explanation](../../../docs/AIRBORNE_DUSTING.md) · [Interactive comparison](airborne_dusting.html) · [Layout drawing](airborne_dusting.svg) · [EDF mass worksheet](airborne_edf_hardware.csv)
