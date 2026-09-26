# Airborne-only dusting — revision E supplement

**Owner hover-mass target, 2026-09-14:** [3.5 kg including the complete core,
battery and loaded dusting module, excluding the lift top](MASS_BUDGETS.md).
The G/E non-lift estimate with maximum modeled dust load is 2.611 kg nominal,
3.489 kg at the high estimate. Keep the remaining margin for uncertainty and
unfinished integration. The approximately 5 kg aircraft figures below include
their propulsion tops and use a different accounting boundary.

The [G frame/joint candidate](FRAME_JOINT_DESIGN.md) carries this same duster
and battery with the revised core frame: 5.017 kg nominal for the four-propeller
reference. G updates the top seat and upper core placement; E/F outputs retain
their previous comparison values.

**Revision F candidate:** [core/floor-power partition](CORE_POWER_PARTITION.md)
removes floor converters from the shared core and recalculates the complete
duster at 5.003 kg nominal with the four-propeller reference top. The E figures
and viewer below retain the earlier 5.249 kg comparison. Tool hardware, boom,
payload, battery and mission reserves are unchanged.

The preferred elevated-dusting bottom now has **no wheels, wheel motors, hubs,
wheel controller or caster**. It carries the cleaning head, a light boom, four
passive landing feet, the common module interface and local sensing. The core
and lift top remain separate modules. Vacuum, mop and under-sofa bottoms retain
their drivetrain. This replaces the assumption that every bottom must drive;
the wheeled suction-duster CAD is retained as comparison evidence.

Start with the [interactive comparison](../design/system/output/airborne_dusting.html),
[calculated report](../design/system/output/airborne_dusting.md),
[hardware worksheet](../design/system/output/airborne_dusting_hardware.csv), or
[FreeCAD](../design/system/output/airborne_dusting.FCStd) /
[STEP](../design/system/output/airborne_dusting.step) reference. Inputs are in
[airborne_dusting.json](../config/airborne_dusting.json). The supplement imports
the existing core, battery and propulsion model rather than copying their masses.
These are design allocations, not printable production parts.

## Weight and balance

| Bottom hardware | Nominal mass |
|---|---:|
| Earlier wheeled suction duster | 2.428 kg |
| Drive/support hardware removed from that design | 0.648 kg |
| New complete airborne bottom, including passive feet | **0.481 kg** |

The last row is a replacement assembly, not the first two rows subtracted.
Further savings come from removing the suction system and powered sofa telescope,
then budgeting the new frame, boom, head, retention, wiring and sensing. The frame allowance includes two edgewise 270 × 20 × 2 mm aluminum
crossmembers, printed ribs and metal load-path hardware. The new
hardware range is **0.323–0.752 kg**, plus 5–30 g retained dust. None is measured.

Keeping the same octo top and 6S pack changes total flying mass from **8.461 to
6.479 kg**. The quad remains **5.249 kg**. Revision E mounts the boom behind the
core and moves the rear stereo camera to a left outboard bracket, opposite the
right-side downward camera. This improves balance without ballast or added mass.
The keyed bottom connector stays in its original orientation; the rear boom
socket is a design change, not permission to rotate any module arbitrarily.

Both added cameras and the flight controller now have their mass assigned at
their physical allocations. With this consistent accounting, the front-boom
reference gives **1.86:1** balance-preserving peak thrust/weight; the revised
rear layout gives **1.97:1** (see the generated report for precision). Revision D's
1.81:1 used a centered distribution for these electronics. The improvement still
falls short of the provisional 2:1 target, and even perfect balance leaves only
about **89 g** aggregate mass-growth margin. Component uncertainty and contact
control require more margin. This quad also fails the loaded floor-bottom cases.

The fixed core retains all its current hardware, including idle floor regulators.
With one of each bottom per floor, the candidate fleet now has six rolling bottoms
and two airborne dusters: 12 drive motors/wheels and six dual wheel controllers,
instead of 16/16/eight. This is an inventory implication, not an order.

## Cleaning mechanism

Use a removable microfiber sleeve on a **60 × 50 mm** head as the first candidate.
It aims to retain dust for removal in an enclosed stationary comb/vacuum pocket.
Aircraft translation supplies the cleaning motion. Dust capture, shedding in
rotor airflow and finish compatibility require tests. If necessary, compare a
small suction-assisted option with explicit added mass and power. This choice
does not change the primary floor dog-hair vacuum.

The tool uses a fixed 45° spar with a short horizontal wrist:

- Two 240 mm lengths of purchased 12/10 mm carbon tube make a 480 mm spar,
  joined with a 60 mm internal sleeve and mechanically retained splice.
- A 100 mm, 10/8 mm tube wrist reaches over a blade edge; a 30 mm drop places
  the cleaning face below it. The total tool path is 610 mm.
- Horizontal root-to-contact reach is **439 mm**, and contact height is **345 mm
  above the robot landing plane**. This explicitly interprets the approximate
  two-foot requirement as tool path, not two feet beyond the rotor guards.
- A keyed metal root and captive station-actuated lock sit at the rear,
  offset 27.5 mm right of centre to clear the hex reference's central beam.
  Its root datum is x=165, y=283, z=36 mm; the rear camera sits to its left.
  The station removes the boom for storage, avoiding carried deployment motors.
- Passive compliance, captive breakaway, tip force/range sensing and local
  interlocks remain. Normal contact at 0.2 N and retreat at 0.5 N are targets.

The root load screen calls for about **3.8 N·m factored moment**, using upper
component masses, retreat force and a factor of three. This is a required design
load, not a proven joint rating. Tube grade, splice fit, stiffness and root
retention remain to detail; printed material is not the long structural spar.

For a surface 2134 mm above the floor, the robot landing plane is near 1788 mm
and the lift-top upper envelope near 1968 mm. The wrist approaches over a blade
edge while the aircraft remains below it. This is not a validated path around
a real fan's hub, lights or brackets. Check approach/withdrawal, blade-stop
interlocking, airflow, contact behavior and camera occlusion. The boom is an
extension exception; the body/lift height limit remains. The sofa telescope is
separate and retains its approximately one-metre reach.

## Automatic handling

The station supports the core, seats/locks the airborne bottom, installs the rear boom
and lift top, then carries the whole robot onto an open launch platform. On
return, load sensing and rotor-stop checks precede shuttle movement into the
exchanger. The station removes/services the boom, stores it upright, and exchanges
the bottom or battery using the supported-core sequence. No airborne coupling
is required. The existing cabinet picker alone does not implement this shuttle.

Allocate **3.1 kg per station** for the shuttle, boom handling/rotation and service
pocket, excluded from flight mass. The detached boom/head fits a **90 × 160 ×
700 mm** rack allocation after rotating the main spar upright. Rack placement,
gripper clearance and full transfer paths still need integration with the compact
station; its old CAD does not implement this sequence. The bottom base uses the
normal tray. The landing platform must accommodate the selected deployed lift.

Passive feet have a nominal 109 mm static support margin with the cap/core/pack
and deployed tool. This is not a landing qualification. They permit an off-station
landing but cannot retrieve a robot that cannot fly again. Automatic routine
operation therefore requires a demonstrated launch/return/exchange cycle and
an appropriate return-energy policy; fault recovery can still require assistance.

## Compact lift and mission result

| Four-position arrangement | Projected footprint | Evidence |
|---|---:|---|
| Guarded 254 mm propellers | 644 × 844 mm | Existing motor/propeller curve and installed allowances |
| 150 mm rotors in 180 mm hover ducts | 596 × 596 mm | Packaging target; no matched hardware/performance yet |
| 90 mm EDFs in 120 mm installation envelopes | 494 × 494 mm | Packaging target; fan/inlet/guard dimensions must be verified |

The **150 mm hover duct remains a requirements target**, with no selected
rotor/motor/duct assembly or performance curve. Revision E adds two documented
89 mm EDF assemblies to the separate [calculated comparison](../design/system/output/airborne_dusting.md#documented-89-mm-edf-assemblies)
and [installed-top mass worksheet](../design/system/output/airborne_edf_hardware.csv):

| Four-unit EDF installation | Airborne duster mass | Loaded vacuum mass | Aggregate peak T/W: duster / vacuum |
|---|---:|---:|---:|
| WeMoTec / HET 650-58-1970 | 6.369 kg | 8.147 kg | 1.58 / 1.24 |
| WeMoTec / HET 650-68-2000 | 6.585 kg | 8.363 kg | 1.75 / 1.38 |

These are our calculations with complete top allowances, 21 V supply and 85%
retained thrust. The [1970 manufacturer data](https://shop.wemotec.com/Midi-Fan-evo-Impeller-HET-650-58-1970-komplett-montiert-feingewuchtet-und-harmonisch-abgestimmt)
and [2000 manufacturer data](https://shop.wemotec.com/Midi-Fan-evo-ducted-fan-unit-HET-650-68-2000-completely-assembled-precision-balanced-and-harmonically-tuned)
provide matched fan/motor masses and voltage-sweep samples. Fan plus intake mass
is 367 g or 421 g per unit, before ESCs, guards, mounts and control hardware.
Neither is a purchase recommendation. Four units of either fail our thrust target;
that conclusion does not rule out every other duct, rotor count or voltage.

For the 1970 variant, equivalent-point interpolation estimates **3.90 kW hover**
with the light duster and **5.62 kW** carrying the vacuum. The 2000 dataset starts
above the thrust needed at hover, so its hover power and endurance stay **unknown**.
No partial-throttle or below-range performance is invented. The smaller 494 mm
square footprint is still a packaging target; installed height, guards, cooling,
control hardware and all approach paths are unresolved.

The lighter EDF case needs about **101 Wh usable** for a 20-second outbound and
20-second return trip plus landing reserve, before cleaning, versus **92.4 Wh**
available in the comparison pack. With the vacuum attached, a 45-second one-way
stair transfer plus landing reserve needs about **157 Wh**, including energy
margin. Peak input-current screens of approximately 378 / 439 A also exceed the
present power-path allocations. A larger battery would add weight and require
another calculation; it does not cure the thrust-margin failure automatically.

EDF yaw cannot inherit the propeller quad mixer without evidence. The product
data does not establish matched opposite-rotation assemblies or net reaction
torque. A [ducted-aircraft study](https://www.mdpi.com/2076-3417/5/4/666) demonstrates
stator compensation and vane control on its own prototype; this motivates a
control-design gate here, not a transferred performance claim. A 120 g yaw-system
allowance is included, with no selected implementation. The comparison uses
optimistic equal load sharing, not a solved EDF flight controller.

The propeller references still estimate **1.7–1.8 kW hover**. The 6S 5200 mAh
comparison pack leaves about **69–75 seconds of cleaning** after a local
20-second outbound and 20-second return trip, with the stated contact-power,
landing and energy margins. A 45-second trip each way leaves about 14–21 seconds.
These are modeled energy ceilings, not qualified duty or achieved cleaning.

Three minutes of local cleaning would require roughly **1.0 kW or less hover
power at this pack energy**, or about **160 Wh usable energy at the current quad
mass/power**. Added battery energy also adds mass; this isolates the shortfall
and does not select a larger pack. Swaps help between sorties, not within one.

Next reduce shared core/lift overhead and seek a documented hover-oriented duct
assembly with complete installed mass, continuous hover data and a yaw solution.
Keep stair-transfer sizing against the loaded floor bottoms separate from dusting
endurance. One universal top has not been demonstrated; compatible top variants
remain an option. Battery selection, fabrication and flight qualification remain
open. No additional owner measurements or purchases are needed for this pass.
