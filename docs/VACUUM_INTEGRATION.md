# Selected-component vacuum integration

> **Scope update, 2026-09-13:** [Whole-system design](SYSTEM_DESIGN.md) now controls
> cross-module layout, carried mass, lift sizing and battery decisions. This
> earlier study remains supporting evidence; its lift deferral or battery-first
> recommendation, where present, is superseded.


2026-09-13. **The new component reservations fit inside the requested envelope;
this is an inspectable placement proposal, not finished or printable hardware.**
It supersedes the inventory-based whole-robot placement for the everyday vacuum.

Open the [rotatable offline viewer](../design/ground/output/vacuum_integration.html),
[FreeCAD model](../design/ground/output/vacuum_integration.FCStd), or
[STEP model](../design/ground/output/vacuum_integration.step).
The [coordinate/check report](../design/ground/output/vacuum_integration_report.md)
is generated from [one placement input](../config/vacuum_integration.json).

| Constraint / result | Current proposal | Qualification |
|---|---|---|
| Rigid envelope | 275 × 275 × 180 mm limit | Frame, bumpers, guards and fasteners still must fit inside it. |
| Wheel outside width | 271 mm | Only 2 mm margin per side; no extra outboard suspension hardware. |
| Scanner top | 178 mm | Family reference dimensions; mounting stack must retain the remaining 2 mm margin. |
| Main printable panels | 270 × 270 mm maximum | This reserves an outline; no full solid panel is implied across the vacuum towers. Bed adhesion margins still matter. |
| Core/bottom mating plane | 86 mm above floor | Most trays occupy z88–120 mm; the converter bay extends down to z70 mm. |
| Bin envelope | 149 × 107 × 64 mm | 1.020 L gross; 0.838 L after simple 3 mm walls alone. |
| Usable bin target | 0.5–0.6 L | Baffles, fill clearance, seals and evacuation gate are not yet subtracted. |
| Head cassette envelope | 230 × 60 × 50 mm, drive above its left end | 10 mm upward compliance allocation; actual brush end/cutter interfaces unknown. |
| Wheel compliance | 10 mm upward, approximately 1.271 mm rearward | Independent trailing-pod concept; not evidence of crossing a 10 mm threshold. |

## Arrangement and ownership

The roller occupies the front. Two geared wheel pods sit behind it with a central
dirt duct between their motors. The bin is at the rear left; the filter and clean-air
plenum sit above it. The blower sits at the rear right, above an offset caster.
This avoids subtracting a caster well from the bin.

The bin, filter, duct, blower, wheels, head and local bottom electronics all leave
with the vacuum bottom during a station swap. The battery, Pi, power conversion,
core supervisor and LiDAR stay on the core. The cap has a scanner opening.
The rear filter and blower towers extend above the bottom mating plane through
**openings in the core structure**. A continuous core floor or rear panel there
would invalidate the arrangement. Neither core structure nor a cap shell has been
modeled as finished material.

The model gives the ordered TriCut listing a 200.6 × 45.1 × 45.1 mm reference,
leaving 14.7 mm per end inside the proposed 230 mm cassette width. This is an
allocation for adapters, guards and retention, not verified clearance around the
rotating mechanism. The matching plain Dreame brush is the comparison sample;
only one brush is carried. The purchased filter gets a **141 × 76 × 20 mm maximum
body allocation**, not an invented measured dimension. Its actual seal and removal
tab must fit within the larger chamber. Component evidence is retained in the
[selection review](VACUUM_RECOMMENDATION_REVIEW.md).

The battery reference now uses the owner's **135 × 43 × 22 mm measurement**,
with its cable end pointing toward the center/right of the robot. This differs
from the earlier seller-size record. Its tray slides left for manual service.
The Pi slides forward, while the joined bin/filter cassette slides rearward after
releasing the clean-air seal. The complete head slides forward after the bottom
is supported, powered down and its fasteners, plug and flexible duct are released.
Automatic *whole-bottom* exchange and manual consumable/head comparison service
remain separate mechanisms.

## Wheel-pod and mounting concept

Use the selected Pololu 4846 motors, 72 × 24 mm Hogback tires and 4 mm Sonic hubs.
The [drivetrain sourcing record](DRIVETRAIN_SOURCING.md) contains supplier references
and the previously checked wheel/hub mating pattern.

Each motor and wheel move together on a short pod, hinged behind its axle. In the
side projection, the nominal axle is at y108/z36 mm and the proposed hinge at
y148/z36 mm. With a 40 mm arm, 10 mm upward wheel travel produces
`40 − sqrt(40² − 10²) = 1.270 mm` rearward travel (1.271 mm rounded upward).
The tire reservation rounds that to 1.3 mm. The motor/pivot reservation extends
rearward to y152 mm. This simple arc avoids assuming a wheel can translate
vertically on a hinge without any horizontal movement.

Select spring preload from the assembled wheel loads; include a captured spring,
travel stops and a cable loop on each pod. The head has its own compliance, so its
floor pressure does not depend entirely on wheel spring compression. No spring
rate, pivot bolt size or bearing arrangement has been released. Gearbox radial
load capacity and wheel overhang also need resolution before a final bracket.

The proposed axial stack is:

| Feature | Dimension / consequence |
|---|---|
| Motor shaft extension | 12.5 mm reference |
| Motor face to hub back | 4 mm proposed |
| Hub body | 8 mm reference |
| Shaft entering hub | 8.5 mm calculated; 0.5 mm beyond hub body into the mating region |
| Faceplate | 2 mm proposed, leaving 2 mm to the hub back |
| Wheel width around hub | Tire reaches 4 mm inboard of hub back; bracket must clear the actual recessed wheel shape |

This is why the wheel/hub mating check alone does not release the bracket: the
plate, tire/spokes, hub clamp screw, motor fasteners and shaft end need one complete
solid-geometry check. A 2 mm printed faceplate is not accepted as strong enough
merely because it has space. A ribbed printed bracket or a small drilled metal
plate may be needed; no machining-dependent construction has been selected.

## Air path and maintenance

Use a flexible connection behind the compliant head, then a central rectangular
duct, bin, sealed filter, short clean-air bridge and blower. The central duct
allocation is 38 × 28 mm outside, giving a nominal 32 × 22 mm passage with 3 mm
walls. Its velocity would be 5.7 m/s at an assumed 4 L/s. That calculation does
not predict hair bridging, filter loss or actual suction.

The blower body is flat above the caster. Its 55 mm high bay includes only about
16.5 mm above the 37.5 mm body for an inlet adapter/plenum, plus a rear exhaust
region. Those fittings still need geometry. A detachable clean-air bridge must
release before bin withdrawal. Design a rear evacuation opening with a closing
gate, accessible hair traps, removable end shields and a gasketed filter frame;
none is represented by the box model's nominal free volume.

## Checks and remaining limits

The generator checks 28 independent reservations and 18 nested references for
body limits, containment and interference. It also checks the wheel references
through their allocated arc bounds, the coupled head/drive upward travel, and
four conditional straight service paths. The checks currently find no conflicts.
Touching box faces are allowed; that is appropriate for shared boundaries but
**does not add real wall thickness, connector clearance or manufacturing tolerance**.

The station sketch raises the core and supported bottom together on a tray whose
surface starts 70 mm above the dock floor, captures the core, then lowers the
bottom by 60 mm. The rear towers project 34 mm above the mating plane and the
core power bay projects 16 mm below it, leaving 10 mm conservative vertical
separation after lowering. This is a vertical-clearance calculation;
ramps, loading, locks, release actuation, connectors and horizontal transfer remain
to design. A 70 mm platform is not a floor threshold the robot can simply drive onto.

The highest-priority open packaging items are:

1. **24 V supply integration:** Cincon CHB100W-24S24 is the working baseline in a
   70 × 70 × 50 mm bay with carrier, heat sink and fan references. Battery and Pi
   trays moved to clear it. Routing, airflow, default-off behavior and startup
   remain open; see the [power packaging decision](VACUUM_POWER_PACKAGING.md).
2. **Rear inboard joint:** only 14 mm width is reserved between bin and blower.
   This is not an approved automatic lock. Reshape the plenum, relocate the joint,
   or revise the frame if the retention mechanism needs more room.
3. **Caster:** the bay is now 80 × 80 × 60 mm, checked against a documented
   78 mm swivel sweep. That TENTE reference has a riveted axle and no thread
   guards; it is not a final purchase selection. It stays offset right; empty/full
   center of mass must remain
   inside the actual contact triangle, including caster trail. No stability claim
   is made without those masses and contact coordinates.
4. **Brush drives:** the main drive allocation is 74 × 60 × 24 mm above the head.
   The side-brush drive allocation is especially narrow, 18 × 35 mm in plan.
   Select actuators and power stages before accepting either allocation.
5. **Remaining structure and sensors:** pivots, springs, stops, bumper/cliff
   coverage, connectors, cooling, seals and frame material are not accounted for
   by a clean reservation report alone.

Next, detail converter integration and close the caster/retention choices and reconcile the delivered
roller and filter interfaces. Then release small unpowered fit pieces for the
wheel bracket stack, brush ends and filter seal. The full deck and head prints
follow those interfaces; the older BDUAV deck is not the new robot chassis.

```sh
python3 design/ground/integrate_vacuum.py
python3 -m unittest discover -s design/ground -p 'test_*.py' -v
freecadcmd design/ground/export_integration.py
```
