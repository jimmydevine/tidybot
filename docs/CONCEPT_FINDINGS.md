# First dimensioned concept: findings and next decision

**Historical concept — ground packaging superseded 2026-09-05.** Current work is
[core and ground modules](GROUND_MODULE_DESIGN.md). Propulsion selection and testing
are deferred until the other modules' dimensions and masses are established.
Numbers below are estimates for the earlier model; its floor envelope does not
fit the newly reported 50 mm sofa clearance.

2026-09-05. Open the [interactive concept](../design/output/concept.html),
[CAD exports](../design/README.md) and [generated checks](../design/output/report.md).
The model and ledger implement the first feasibility study promised in the roadmap
discussion. This is not a release of build-ready robot parts.

## What changed when we modeled the hardware

The trial core/bottom footprint is now **200 mm fore-aft × 280 mm wide**, with a
90 mm bottom, a 90 mm core and a 10 mm cap. The earlier 240 mm fore-aft sketch fails
the assumed tread landing error budget. The smaller body fits the modeled component
boxes, but packaging remains tight and has not yet included routed ducts and cables.

The strongest configuration in this first comparison uses four **9-inch propellers**
on a rectangular layout with motor centers at x=±245 mm and y=±145 mm. A rotor plane
300 mm above the contact surface produces an overall guard envelope of approximately
**749 × 549 × 315 mm**. It passes the currently implemented geometric screens. A low
200 mm rotor plane collides with the uphill step/arm envelope under the sampled errors.

The tested 12- and 15-inch layouts fail several screens. The particular 12-inch motor
reference also lacks enough thrust for the assembled mass. This rejects those tested
combinations, not every motor or layout using those propeller diameters.

## The mass and power result is marginal

The reference mass is **4.22 kg loaded**: core 1.66 kg, vacuum bottom including a
150 g debris allowance 1.33 kg, and lift top 1.24 kg. Estimated masses use ±30% and
manufacturer masses ±5% as sensitivity bounds, giving **3.34–5.10 kg**. These are
deliberate uncertainty scenarios, not statistical confidence intervals.

The small-prop reference is Hobbywing's XRotor/RTF 3110 900KV with HQ9x4x3 propellers.
Its manufacturer table is measured at **24 V** and includes a **36-second full-throttle
note for that propeller**. That duration is not a hover endurance rating. The study
interpolates its thrust/power data without extrapolation and applies an unmeasured
15% thrust-loss allowance for the guarded installation. See the
[manufacturer specification](https://www.hobbywing.com/en/uploads/file/20251117/7845436338d9dbe2f43a50c4bae18544.pdf).

Using an additional unvalidated square-voltage sensitivity at 21 V gives approximately
**2.05:1 available thrust/weight** against a provisional 2:1 target. Only **96 g** of
nominal mass headroom remains. At the upper mass sensitivity, the ratio falls to
**1.69:1**. The mass and propulsion budget therefore remains open despite the nominal
screen passing. Greater guard losses also remove the margin.

The bench-equivalent hover estimate is approximately **1.06 kW**, including shared
electronics. If that power held at 21 V, the battery branch would carry roughly
**51 A** in hover; transient demand can be much higher. This is not a validated
low-voltage power curve, wire rating or connector selection.

A reference 6S 5 Ah pack stores 111 Wh nominal. An assumed 60 seconds of flight costs
about 17.7 Wh in this calculation. With 80% usable battery energy and a 123 W ground
load allowance, approximately **35 minutes of ground cleaning** remain after that
flight allowance. This does not establish a safe reserve or coverage per charge;
recharge during jobs is already acceptable in the brief. Automatic per-cell charge
management and the charge connector remain design work.

## Components to compare with existing inventory

The [CSV ledger](../config/components.csv) includes sources, dimensions, masses,
power allowances and price basis. These are candidates to compare, not a purchase order.

| Component | Reference | Why it is useful now |
|---|---|---|
| Battery | Grepow 6S 5 Ah reference, 755 g | Establishes real package size and substantial carried battery mass |
| Wheel motors | Pololu 5727, 99:1 HP 24 V with encoders, 102 g each | A lighter alternative to 37 mm gearmotors; current listing indicated backorder |
| Blower | Wonsmart WS7040-24-V200, external controller | Small clean-air blower for a filtered intake bench experiment |
| Core compute | Raspberry Pi 5 with cooling/storage allowance | Candidate for floor navigation; flight perception compute load still needs profiling |
| Flight controller | Pixhawk 6C Mini, current Model A | Dedicated flight controller with an explicit regulated supply requirement |

The wheel motor's **continuous gearbox torque limit**, not extrapolated stall torque,
must guide drive loading. Its manufacturer lists a 4 kg·cm continuous limit for this
gearbox family. Confirm brush drag, traction, motor heating and wheel support load in
the floor rig. [Pololu family specifications](https://www.pololu.com/category/384/24v-high-power-hp-25d-mm-gearmotors)

The blower is a clean-air reference, placed **after the bin and filter**. The
manufacturer drawing specifies a working point above 12 m³/h at 3 kPa and below 2.5 A
at 24 V; this says nothing by itself about pickup through our roller, ducts and dirty
filter. Regulated operation over the battery range and an appropriate external motor
controller remain to select. [Wonsmart drawing](https://www.wonsmartmotor.com/uploads/WS7040-24-V2004.pdf)

## Station result

The provisional **1,200 × 1,000 × 1,200 mm** station contains the default static
working volumes: overhead lift-top parking, a cap shelf/shuttle, an elevated core,
three bottom positions and removable tank/waste envelopes. Front/rear entry bounds,
parked height, cap storage width and tool-to-core vertical separation are checked.

The displayed mechanism is a set of envelopes. It still needs an actual elevator,
indexer, retained core supports, actuated coupling and guided connectors. Stored
bottoms are conceptual copies, not designed mop/duster modules. External doorways,
arrival paths, complete swap trajectories and fault recovery remain unverified.

## What should happen next

Follow the [ground module design](GROUND_MODULE_DESIGN.md): package the core and
ordinary vacuum bottom with station-accessible joints, then build a
rolling vacuum and measure its components and complete modules. Develop the cap,
dedicated low-clearance bottom, mop, duster and automatic service interfaces
against that evidence. Sofa access is resolved as a low head with the body outside.

The [propulsion comparison](PROPULSION_COMPARISON.md) and
[EDF experiment](EDF_BENCH_PLAN.md) are both deferred. The owner rejected the
approximately $825 fixture proposal and subsequently deferred all lift work.
Revisit propulsion after the carried ground hardware and operating loads are known,
adding the eventual lift assembly and any power-system changes to that payload.
This earlier model does not establish flight feasibility around stairs or dogs.
