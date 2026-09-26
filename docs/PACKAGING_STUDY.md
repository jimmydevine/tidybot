# TidyBot packaging and operating study

> **Scope update, 2026-09-13:** [Whole-system design](SYSTEM_DESIGN.md) now controls
> cross-module layout, carried mass, lift sizing and battery decisions. This
> earlier study remains supporting evidence; its lift deferral or battery-first
> recommendation, where present, is superseded.


**Historical packaging reference, superseded for current work on 2026-09-05.**
Follow [core and ground modules](GROUND_MODULE_DESIGN.md). All lift work is deferred
until the other modules' dimensions and carried masses are known. The body and
large flight-top station envelopes below are not current build requirements. The
new 50 mm sofa clearance is handled by a separate low head with the body outside;
see the current ground design for the dedicated bottom proposal.

2026-09-05 — preliminary design, based on the confirmed requirements in
[DESIGN_RESET.md](DESIGN_RESET.md). This defines the next mechanical study; it is
not fabrication CAD, a selected bill of materials or demonstrated flight performance.

**First model available:** the [dimensioned concept findings](CONCEPT_FINDINGS.md)
and [interactive viewer](../design/output/concept.html) now test these preliminary
ideas. That study reduces the trial body depth to 200 mm and compares sourced
propulsion references. Numbers below retain the earlier exploratory context.

## Recommended architecture

Use one electronics core, complete interchangeable wheeled cleaning bottoms, a
lightweight cap and one shared guarded lift top. Put module handling machinery and
bulk debris/water storage in two stationary service stations. The airborne assembly
always includes the core and its selected cleaning bottom.

During ordinary floor cleaning, the cap replaces the lift top. The aircraft hardware
travels with the robot between floors and is parked at the destination station during
floor cleaning. This gives the floor robot a smaller envelope without requiring a
folding rotor frame. Folding is an option only if station space or landing geometry
requires it; fixed arms avoid an additional deployed-position retention mechanism.

Every autonomous cleaning bottom includes its own wheels, encoder-equipped drive,
support contacts, floor-facing sensors and task hardware. The first is a vacuum with
a short, serviceable hair path and automatic bin-emptying connection. A later mop
bottom contains its liquid circuit. Keep the dirty-air and liquid circuits out of the
core's top/bottom structural interfaces.

## Three distinct operating envelopes

| Mode | What constrains it | Study to complete |
|---|---|---|
| Floor cleaning with cap | Furniture clearance, edges, hair pickup, bin access | Low core and task bottom with protected wheels and accessible roller ends |
| Transfer with lift top | Walls, rail projections at different heights, headroom, dogs, arrival/abort locations | Full guarded rotor envelope, body interference, thrust and perception coverage |
| Cleaning a tread with lift top | Contact support on an 11-inch tread, higher steps, rails and cleaning-head reach | Stable support polygon, stopped-rotor clearance and coverage of tread/edges |

The flight envelope cannot be reduced to propeller diameter. Include the core,
guards, frame members, tilt during control, deflection and the observed position
error distribution. A long, narrow rectangular rotor arrangement is worth comparing
with a square one; reducing width increases length and can worsen contact with
higher steps. Neither layout is selected yet.

For a first tread-support sketch, explore **240 mm fore-aft body depth** and
**200 mm fore-aft contact span**. Centered on a nominal 279.4 mm tread, these leave
19.7 mm body clearance and 39.7 mm contact-position margin at each end respectively.
These are ideal static margins before tire contact patches, nosing, positioning error,
tilt and deformation. A body may overhang a tread without tipping if its center of
mass stays within its supported contact polygon, but overhang can strike the riser.
Therefore do not turn these sketch dimensions into a released chassis specification.

The lift frame may reach over the next one or two higher steps even while the wheels
sit correctly. Check the frame and each rotor disk against a stepped 3D solid, through
approach, landing, stationary cleaning and takeoff. Raising the rotor plane enough to
clear a higher tread increases robot height and changes its structural moment loads.
This is a central design constraint, not a detail to fix with flight software.

The nominal stair pitch from the supplied dimensions is `atan(7.5/11) = 34.3°`.
If the reported 15 stairs means 15 risers, total rise is 112.5 inches (2.86 m). The
number of treads before the landing needs confirmation before setting horizontal
run. Model rail/lip geometry at its actual height; the owner has confirmed the
measurement references, but the combined 30.5-inch projection envelope in
DESIGN_RESET.md is not a scanned cross-section at one height.

## Lift sizing comparison

The following repeats the ideal hover calculation from DESIGN_RESET.md while varying
propeller diameter. It assumes four unobstructed, non-overlapping rotors in free air.

| Propeller diameter | Ideal hover power at 3 kg | At 4 kg | At 5 kg |
|---|---:|---:|---:|
| 10 inches | 227 W | 349 W | 487 W |
| 12 inches | 189 W | 291 W | 406 W |
| 15 inches | 151 W | 233 W | 325 W |

These are lower bounds calculated from momentum theory, not candidate motor ratings
or electrical consumption. Smaller rotors buy packaging room at a power cost. The
compact rows do not prove that purchasable motors can provide sufficient control
reserve at an acceptable temperature. Verify a complete motor/propeller/ESC combination
against manufacturer data and then measure it with the actual guard configuration.

Keep a mass ledger for core frame, battery, compute/sensors, wiring/protection,
bottom drivetrain, blower/roller/filter/bin, retained dirt, lift motors/ESCs/props,
arms, complete guards, flight sensing, connectors and retention. For the mop, replace
the vacuum allocation with all wet hardware and maximum allowed liquid contents.
Estimate from actual component candidates and weighed inventory; do not assign an
unmeasured total mass as a requirement that the parts must somehow fit afterward.

## Automatic stations

A candidate station combines a lower tool tray, side supports that engage dedicated
core hardpoints, and an overhead carriage for the cap/lift top. Use purchased linear
rails, lead-screw actuators and fasteners with printed guides and covers. This is a
mechanism family to package, not a claim that any particular rail or actuator fits.

### Space to reserve for the first prototype

Reserve the same initial envelope in the kitchen and master bedroom:

| Space | Provisional allowance | Purpose |
|---|---|---|
| Station cabinet and operating mechanism | 1,200 mm wide × 1,000 mm deep × 1,200 mm high (about 47 × 39 × 47 inches) | Module storage/exchange, frame, charging, removable service containers |
| Clear approach immediately in front | 1,200 mm wide × 1,000 mm deep (about 47 × 39 inches) | Straight docking and front service access |
| Combined rectangular floor reservation | 1,200 mm wide × 2,000 mm deep (about 4 × 6.6 feet) | Cabinet plus approach; approach can be ordinary clear floor |

These are layout allowances rather than measured component requirements. They assume
a guarded lift top no larger than approximately 700 mm wide × 900 mm long and a
compact roughly 300 mm-wide cap/bottom family. The aircraft dimensions are an input
for the study, not a flight-feasible design. A larger lift top or extra module
inventory increases station size. Door swings, tank withdrawal and actual turning
trajectories still need checking; the clear approach is not an in-place turning claim.

Park the lift top vertically above the docking bay. A separate small cap shuttle
operates below that parked frame. This avoids having to fit two large rotor-sized
bays side by side. Store complete bottoms on an indexed tray below the supported
core, with a lower service drawer for tanks and waste. Arrange vertical travel and
collision clearances in CAD before accepting the 1,200 mm height. The small cap
shuttle must not pass through the stored lift frame or its hanging wiring.

The robot approaches with rotors stopped and drives into the station. The approach
path from the staircase to the kitchen/bedroom must admit the full lift top through
doorways and around furniture. Available room area alone does not establish that
connection. The station does not require indoor takeoff underneath its overhead
storage mechanism.

### Tanks and periodic service

Use wall power and removable containers as the default. Explore 3–5 L clean-water
and dirty-water containers and a 3–5 L stationary debris container as initial
packaging candidates; these are not promised unattended capacities. Put them in a
front-access tray with leak collection, liquid-level sensing and a leak detector.
Keep mains equipment and charging contacts out of the wet compartment. Make a
future plumbing kit attach at the station's service side without changing the robot.

Provide automatic onboard-bin evacuation, mop refill, dirty-water handling and pad
wash/dry as the relevant modules are developed. Measure actual usage to predict
service intervals: clean-water capacity divided by cleaning-plus-wash consumption,
dirty-water capacity divided by recovered volume, and debris capacity divided by
observed accumulation. Dog-hair packing, filter restriction and container hygiene
can require service earlier than volume alone indicates. Missing/full tanks inhibit
affected wet jobs while eligible dry jobs can continue. No fixed weekly/monthly
interval is claimed before household trials.

The core must be supported before its wheeled bottom is released. Keeping the main
handling actuators in the station reduces carried hardware, but each robot interface
still needs positive retention and a verified retained state. A mechanically operated
latch driven by a station tool is a candidate; it must stay locked after the tool
withdraws and upon power loss. Large entry guides plus a compliant module tray can
handle approach error before the final locating surfaces and connector engage.

The automatic connector needs guided mating, misconnection protection, strain relief,
and an appropriate continuous/transient current rating. Bench prototype plugs remain
useful for early measurements but are not the automatic interface. Module power stays
disabled during mating; core/station logic maintains control of the exchange.

An exchange sequence must distinguish weight supported, latch released, module moved,
new module seated, latch secured and connection validated. Motor current or a single
actuator endstop alone does not verify that the payload is retained. Interrupted
exchanges leave all parts captured by the station and keep flight/drive inhibited.

### Two-floor inventory and travel cycle

Each station has a cap storage position and a lift-top position large enough for the
guarded frame. A simple inventory uses one cap per floor and one shared lift top.
The station with a floor-cleaning robot stores the lift top and has its cap on the
robot. The other station stores its cap and leaves its lift-top bay empty for arrival.
This avoids requiring a duplicate lift top merely to complete a return trip.

```mermaid
flowchart LR
    A["Clean downstairs with cap"] --> B["Station fits lift top; checks energy and retention"]
    B --> C["Wait for clear transfer route and arrival space"]
    C --> D["Fly entire assembly upstairs"]
    D --> E["Land; stop rotors; drive into upstairs station"]
    E --> F["Station stores lift top and fits cap"]
    F --> G["Clean upstairs; recharge as needed"]
```

The destination approach must fit the lift top while driving from the landing point
into the station. The bookcase and robot turning envelope can constrain this even if
the flight corridor itself fits. Station space must include the carriage's swept
volume and approach lane, not just its closed cabinet dimensions. Arrival storage
availability and the intended cleaning bottom are part of mission planning.

Include a stationary vacuum source and larger debris container for automatic bin
emptying. Test evacuation with packed dog hair and a partially loaded filter. Its
power and mass stay off the aircraft. For mopping, develop automatic refill/drain and
pad wash/dry around the default removable tanks. The owner accepts periodic bulk
water/waste servicing and cleaning. The optional kitchen plumbing connection must
not become a requirement for operating the bedroom station or another user's system.

## Stair cleaning: landing versus blowing

The preferred first stair-cleaning experiment is **land, verify stable support,
stop rotors, vacuum, then lift to the next position**. The cleaner may traverse
sideways across a tread, but a differential drive cannot move sideways without
turning. Model a turn that keeps every required contact on the tread, or investigate
a dedicated stair bottom/head motion. A whole-assembly quarter-turn may be impossible
with a long rotor frame, even when its small wheeled bottom can turn.

Blowing debris downward is retained as an experiment. A directed nozzle may move
loose hair, but distributed propeller downwash is not a controlled stair-sweeping
tool. Measure debris delivered to the intended lower collection area, debris left
on treads, material deposited elsewhere and airborne particles. The blower still
needs to reach and aim at each tread; it does not eliminate the positioning problem.

The concern about fine dust is an engineering inference from the EPA's description
of how settled household dust is returned to the air during disturbance, and its
recommendations for damp dusting and filtered vacuuming. See
[EPA: sources of indoor particulate matter](https://www.epa.gov/indoor-air-quality-iaq/sources-indoor-particulate-matter-pm).
Prefer capturing debris near its source unless a controlled comparison shows the
blower method meets the cleaning and redistribution goals. A local air jet paired
with nearby suction is another candidate, with added power and duct complexity.

## What to resolve next

Proceed with [the ground module design](GROUND_MODULE_DESIGN.md): package the
electronics core and everyday vacuum bottom, and develop their joint
with the station support. Record actual masses as hardware is selected and built.
The flight path, rotor envelope and overhead lift-top storage study remain deferred.
