# Passive vacuum-head support — Q comparison

**Follow-up:** [R integrated cassette ends](INTEGRATED_HEAD.md) replaces the
intersecting head-end allocation with actual frame material and adds pitch-stop
slots, guide backings and a complete local mass comparison. It retains the powered
lift, finds only about 8 g conditional saving, and does not resolve Q's friction
concerns. Q remains the motion/force comparison rather than a fabrication design.

The useful result is a specific head-motion arrangement and a reason **not to
delete the lift actuator yet**. Two independent slides and low pivots can supply
the required translation, roll and pitch. A separate spring-balanced version
offers only 22 g of conditional saving and fails the conservative friction
screen. Gravity loading is simpler, but its worst modeled contact margin is
small and dock-only capture would restrict head release away from a station.

Continue toward an **integrated head frame with passive floor following**.
Keep the existing powered-lift allocation until threshold crossing, capture and
away-from-dock operation are resolved. The transfer estimate remains 5.275 kg,
including core, battery and maximum modeled debris, excluding the lift top:
775 g over the 4.5 kg requirement. This study does not accept that excess.

[Interactive motion](../design/system/output/passive_head.html) ·
[Calculation report](../design/system/output/passive_head.md) ·
[Inputs](../config/passive_head.json) ·
[Mass ledger](../design/system/output/passive_head_mass.csv) ·
[CAD check scope/results](../design/system/output/passive_head_cad_checks.json)

| Reference position | FreeCAD | STEP |
|---|---|---|
| Level cleaning | [Assembly](../design/system/output/passive_head_level.FCStd) | [Assembly](../design/system/output/passive_head_level.step) |
| Left-wheel threshold sample | [Assembly](../design/system/output/passive_head_left_step.FCStd) | [Assembly](../design/system/output/passive_head_left_step.step) |
| Station-raised head | [Assembly](../design/system/output/passive_head_captured.FCStd) | [Assembly](../design/system/output/passive_head_captured.step) |

## Motion that the support must provide

N's fixed wheels require about 5.22° pitch and 2.32° roll in the horizontal-level
threshold samples. The earlier M up/down allocation with ±1.5° tilt cannot do
this. Q uses one vertical carriage near each end of the head, with spherical
pivots allowing the head to tilt. The left pivot locates it laterally; the right
has axial float to accommodate the change in projected width during roll.
Rigidly clamping both pivots axially would bind the mechanism.

Nominal pivots are at [32,30,20] and [243,30,20] mm. Their carriages sit 20 mm
higher. A short drop link lets the guides fit above floor obstacles while
keeping floor-drag torque about the pitch axis lower. Raising the pivot itself
from 20 to 40 mm doubles the drag moment; the level-body calculation then
pushes the required floor reaction beyond the proposed rear support location.

The exact kinematic solution constrains both pivot centers to the same body Y,
holds the left X datum, and permits the right X datum to move. It differs from
M/P's unconstrained ideal rotation. Over 104 terrain samples, carriage centers
range from **27.11 to 50.00 mm**, with **0.173 mm** maximum geometric axial float.
The 1 mm float allocation leaves 0.327 mm after a separate 0.5 mm rail-spacing
tolerance. Rail end/placement tolerances and positive-stop room leave 1.61 mm
minimum calculated vertical travel margin. Those margins do not include every
manufacturing error or bearing clearance.

The reference uses compact drylin N guides, with documented dimensions and mass,
and spherical bearings as pivot references. Their assembled interfaces remain
to be designed. The guide manufacturer calls for proper mounting surfaces and
fixed/floating arrangements; a flexible printed mounting face is not assumed to
meet those requirements. [Manufacturer guide catalog](https://www.igus.com/us/pdf/drylinn.pdf).

The historical KGLM-03 bearing has specified shaft and housing fits. Printing a
nominal hole does not establish those fits, and the current LC successor cannot
be substituted without checking its drawing. A mechanically captured housing,
smooth pin and accessible retainers are required. [Bearing catalog](https://www.igus.com/us/pdf/igubal.pdf).

## What the CAD checks establish

Q adds guide envelopes, nominal drop-link stock, carriage and bearing references
to the P coupling context and the actual N drivetrain support solids. The
protected roller envelope and moving motor clear those new guides at the
sampled positions. The moving head allocations also clear the checked P/N
context. See the generated JSON for the individual results and source fingerprint.

The left guide fits between the side-brush reservation and chassis rail only
after moving the side-brush reservation 1 mm outward, from X2 to X1. It remains
inside the rigid body footprint. Nominal lateral clearance is only 0.5 mm;
actual hardware, fastener heads and mounting tolerances still need checking.
This change is local to Q; earlier exports remain unchanged.

**The new guides occupy part of the old head-frame allocation.** The CAD check
reports those intersections explicitly. They require redesigned end-frame
pockets, not a claim that the present cassette already fits. The solid roller
reference starts farther inboard, but exact roller end/cutter interfaces remain
unverified. This is why the guide support must be designed with the existing
135 g head-frame scope instead of bolted onto another complete frame.

Guide/carriage and bearing shapes are envelopes, not reconstructed supplier
solids. Pivot pins, bearing cages, keyed carriage mounting, carrier tabs, spring
anchors, end/pitch stops, raised capture, air-flex motion and wiring are incomplete.
The rail's cantilevered installation needs a load-path review. The P positive
exchange locks still need their own completion. No STL files are released.

## Contact force and drag

The modeled moving head is approximately 498 g and has its center of mass
left of center because of the roller motor. A nominal 3.5 N floor load therefore
needs unequal upward spring forces: about 1.17 N left and 0.22 N right. The
chosen spring rates are design sensitivities, not selected catalog springs.
The small right force falls to zero as the head rises; the model permits slack
and does not invent a downward force from an extension spring.

With just spring/preload variation and the earlier ±1 N service-force allowance,
all sampled cases maintain positive contact. That result is insufficient.
Including guide drag and its moments changes the conclusion: the conservative
friction model contains cases with no sustained floor contact. The model
accounts for the drop-link moment, an offset load acting on the slide, and the
feedback of friction through that offset. It uses assumed friction, effective
contact spacing and breakaway force; these are not measured bearing properties.

Gravity loading removes the balancing springs. Nominal contact becomes about
4.89 N, and the modeled mechanism falls from 75 to 72 g. Its high-friction case
leaves only about **0.25 N** contact margin before additional unknown loads.
That is a reason to investigate friction and simplify the support, not evidence
of reliable cleaning. Dust, hair, misalignment, flex stiffness and different
head masses could consume the margin. Pitch stops are still needed when a
transient load moves the resultant beyond the front/rear support interval.

Two end skids are proposed with front and rear ramps rising 13.5 mm over 14 mm.
They are intended to encounter a 10 mm edge before the hard head housing.
The wedge calculation shows the extra push needed at several assumed friction
values. It does not establish a continuous path across a threshold: finite
contact transitions, tire traction, head pitching and guide resistance must
be solved together. The current N traction calculation assumes a raised head
and cannot validate this passive crossing by itself.

## Lift, exchange and flight retention

Passive floor following does not automatically replace all powered-lift functions.
The dock-only alternative would have the station raise the head by 16 mm, engage
two positive catches and a pitch locator, and independently verify capture.
The receiving floor's station would support and release it before cleaning.
Travel stops provide captivity; they do not by themselves provide raised,
level flight restraint. A 50 N local retention design load remains a requirement,
not a proven capability of the catalog carriage or an unfinished catch.

This sequence can support station-to-station transfer in principle. It does not
provide arbitrary head raising or release away from a station, and must not
silently rule out the owner's stair-cleaning intent. Failure recovery and landing
with a captured head remain to develop. **Keep the lift allowance while these
functions are unresolved.** No new user restriction on stair cleaning is assumed.

## Mass comparison and implementation decision

| Alternative | Complete local comparison scope | Consequence |
|---|---:|---|
| Existing P/M allocation | 35 g remaining compliance + 62 g lift = **97 g** | Unfinished baseline |
| Separate spring-balanced guides + dock capture | **75 g** | 22 g conditional saving; friction screen fails |
| Gravity-loaded guides + dock capture | **72 g** | 25 g conditional saving; small contact margin and dock-only release |

Only 23 g of the spring-balanced version is based on catalog reference masses;
52 g remains itemized installation/capture/completion allowances. Its 75 g is
not a weighed assembly or a full CAD-volume total. All versions retain the
70 g P carrier, 135 g head frame, 75 g plumbing and other module budgets.
The carrier's unfinished mating-face supports are not newly counted here.

The 22–25 g opportunity is small compared with the 775 g system shortfall.
Even achieving the lighter dock-only mechanism would leave approximately
**750 g still to remove**. The saving is not booked, and a separate finished
guide assembly should not be added to the current frame.

The next useful mechanical change is to make the cassette end plates serve as
the pivot housings, skid supports and positive stops, and connect the guide tops
directly to the removable carrier. Build one explicit mass ledger for the shell,
guard, guides, retention and lift functions. Retain the powered option during
that comparison; remove it only if another mechanism preserves the required
automatic operation. Resolve the short air flex's motion and force in that same
layout, because its resistance is part of whether the head follows the floor.

## Reproduction

All 154 system-model tests passed after the final exports. The offline viewer
passed pose/capture/reset checks and was visually reviewed. The CAD checks
reported no guide/context, moving-reference or head/P/N intersections in their
stated scope, while retaining 210 old head-frame overlap entries requiring
redesign. Passing software checks does not validate the physical mechanism.

```sh
python3 design/system/passive_head.py
python3 design/system/passive_head_viewer.py
freecadcmd design/system/export_passive_head_freecad.py
freecadcmd design/system/export_head_coupling_freecad.py
python3 -m unittest discover -s design/system -p 'test_*.py' -q
```

Both CAD JSON files fingerprint the model inputs and Python sources. Refresh
them after source changes. Tests check kinematic closure, force/mass accounting,
insufficient travel, spring slack, tipping, friction failure and explicit frame
rework. They do not validate the unbuilt mechanism or arbitrary stair trajectories.
