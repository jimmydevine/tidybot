# Vacuum head using owned consumables

**2026-09-13 status:** retain this as the owned-consumable and earlier-layout
reference. The [next vacuum-module pass](VACUUM_MODULE_NEXT_PASS.md) proposes a
front side brush feeding the main intake and moves the roller drive above one
end. The earlier rear gated inlet and CBM blower assignment below are not the
current selection. The [recommendation review](VACUUM_RECOMMENDATION_REVIEW.md)
now prioritizes TriCut investigation against hair-shedding alternatives, with
a washable-filter candidate and provisional BIQU blower. Owner dimensions below
do not specify those new parts.

2026-09-06. The owner has rollers, brushes and filters from
[Amazon ASIN B088W8HS1Y](https://www.amazon.com/dp/B088W8HS1Y).
Use these as the first everyday-vacuum consumable candidates. No complete powered
cleaning head, brush motors, transmission or mounting frame has been reported.

The owner now confirms s9/s9+ rollers/filters and reports **two roller styles in
each of two lengths: 10 inches and 7.25 inches**. Treat each length as a separate
complementary pair; do not mix a long roller with a short one. The original Amazon
page could not be retrieved, and it is not established that both length sets came
from that one listing or share the same end fittings. Use the reported physical
inventory for the design without assigning an unverified model number to either
length. Individual spare quantities and masses remain unknown.

## Working arrangement

| Part | Proposed installation | Hardware still to design/select |
|---|---|---|
| Rubber rollers | 7.25-inch complementary pair as the compact front cassette reference; 10-inch pair is an oversized-layout alternative; both styles have 28 mm fin diameter | Separate keyed drive couplings, end supports, transmission, motor and its power stage |
| Side brush | One behind the left wheel, feeding a separate gated inlet into the dirt well | Hub, motor/reduction, mount and its power stage; sweep envelope must clear wheels, bumper and docking features |
| Filter | One 136 × 76 × 14 mm element initially, with space for its pull tab | Holder, seal and clean-air plenum; tab location and removal access; confirm pressure loss with the chosen air path |

Installed quantities above are layout proposals, not a claim about current stock.
Replacement consumables stay at the station and do not add to carried mass.
The full everyday bottom still contains its own wheels, controls and air system;
its service cassette does not change the automatic whole-bottom swap architecture.
The separate low-clearance bottom retains its own head design.

For the s-series reference, iRobot describes two brushes turning in opposite
directions, with different functions. It also shows distinct square and star
drive pegs and removable end caps. Use the pair's intended handedness, with debris
fed into the pickup path. Actual coupler geometry must follow the owned parts.
[iRobot roller and maintenance reference](https://www.irobot.com/en_US/dual-multi-surface-rubber-brushes-for-roomba-s-series/4646490.html)

Propose a printed cassette with adjustable end-support locations and a removable
retaining door. Keep roller end caps accessible for hair removal. Reserve a dry
side bay for a single roller-drive motor and a transmission producing opposite
rotation; gear ratio, center spacing, contact depth and roller RPM remain open.
Do not assume the two rollers use identical drive sockets or require identical
surface speeds. The slow 18 RPM wheel motors are not assigned to this function.

Use compliant mounting and non-marking support surfaces to control contact on
wood/tile. Floor marking, pickup and hair wrap must be checked on the actual head.
Printed walls and bought fasteners are reasonable construction candidates; rotating
supports and couplers still need fit and wear checks before a fabrication release.

The side brush has its own drive. Both channels of the proposed wheel H-bridge
are already assigned to the wheels; the roller and side-brush power stages must
be included separately in the consolidated BOM. Local control must detect a jam
and stop the affected drive, with the sensing and current limits still to select.

## Air path and filter access

Use the path **roller intake → short duct → bin → sealed filter → CBM blower**.
Use the downward emptying door under the dirt well and an intentional make-up-air path;
isolate the onboard blower during station evacuation. The filter is removable
for servicing without detaching the core. No debris should bypass its perimeter
seal into the blower.

Compatibility with an s9 does not establish acceptable pressure loss with our
different blower and duct. Keep the filter holder replaceable and establish
pickup with both a clean filter and accumulated dog hair. Neither certified HEPA
performance nor washable construction is established for this aftermarket kit.
iRobot treats its original s-series filter as non-washable, separately from the
washable bin. [Original module reference](https://answers.irobot.com/knowledge/20962)

## Recorded dimensions and layout consequences

Owner measurements, 2026-09-06. Inch conversions use exactly 25.4 mm per inch;
their decimal precision does not imply a measurement tolerance.

| Item | Reported measurement | Working layout interpretation |
|---|---|---|
| Long roller pair | Two styles, 10 inches long; both styles 28 mm diameter | 254 × 28 mm overall-length/maximum-fin envelope for each roller |
| Short roller pair | Two styles, 7.25 inches long; both styles 28 mm diameter | 184.15 × 28 mm overall-length/maximum-fin envelope for each roller |
| Filter body | 136 × 76 × 14 mm | Outside frame envelope before its pull tab |
| Filter pull tab | 20 × 6.5 mm, raised roughly 5 mm; centered along the width axis on one side | Preserve the owner's location description; exact face, in-plane orientation and position along the other axis remain to establish |

The roller lengths were supplied in response to an overall-length question.
Treat them as end-to-end layout lengths for now. Rubber working length, bearing
seat spacing and drive engagement are separate dimensions, still unknown.

Use the **184.15 mm pair for the current 275 mm-wide everyday layout**. It reduces
the roller-length allowance by **69.85 mm** compared with the long pair. Its
254.15 mm-wide cassette targets a whole print; the long-pair cassette is 324 mm
wide under the same allowances and exceeds the body limit. Neither reported
roller length establishes the actual cleaning swath. The separate 50 mm-clearance
head still needs its own mechanism and complete height study.

Allow the drive bay and service access beyond the rollers themselves. The owner
now permits printed pieces up to 275 × 275 mm; this supersedes the earlier
preferred 250 mm span. The robot's main panels target 270 × 270 mm, with actual
print margins, flatness and structural design still to verify.

For the filter, **14 + 5 ≈ 19 mm** is the initial local depth allowance at the
tab, assuming the stated rise is normal to the broad face and additional to the
14 mm body. This is a derived envelope, not a measured total thickness or a
finished holder dimension. Leave tab relief movable until its exact placement is
known. Keep the grip reachable from the bin/filter service opening, with extra
finger access and extraction clearance; a 19 mm cavity alone does not provide
that access. Fit clearance, gasket compression and the sealing ledge are also
still to detail. Place the latch on the rigid frame rather than relying on the
pull tab as a retention feature.

**Diameter answer recorded:** Both styles are 28 mm in diameter. Apply that
reported value to both length sets. The initial envelope questions are resolved
in [owned_parts.json](../config/owned_parts.json); no new question is pending.

## First dimensioned clearance study

Open the [offline layout comparison](../design/ground/output/vacuum_head_layout.html)
to switch between the two roller lengths, or view the
[long-pair SVG](../design/ground/output/vacuum_head_long_10in.svg) and
[short-pair SVG](../design/ground/output/vacuum_head_short_7_25in.svg).
The drawings show measured roller/filter envelopes and proposed housing allowances;
they are not fabrication drawings. The filter is shown separately, not installed
inside the roller cassette.

| Initial proposal | Value | Basis |
|---|---:|---|
| Roller center spacing | 30 mm | Designer-selected clearance starting point; final contact and pickup setting open |
| Gap between maximum fin envelopes | 2 mm | 30 − 28; no deliberate fin compression modeled |
| Long-pair cassette study footprint | 324 × 72 mm | Reported rollers plus proposed supports, walls and drive bay |
| Short-pair cassette study footprint | 254.15 × 72 mm | Same allowances with the current compact pair |
| Roof reference above floor | 35 mm | 28 mm roller + 4 mm upper clearance + 3 mm roof; fin envelopes tangent to floor |

The width calculation reserves 2 mm axial clearance and a 10 mm support bay at
each end, a 40 mm drive bay on one side and 3 mm outer walls. Depth includes 4 mm
fin clearance and 3 mm walls at front and rear. These allowances are proposals,
not dimensions of selected hardware. The full powered head may grow once the
motor, transmission, intake plenum, duct and retention hardware are detailed.
The 35 mm roof reference does not establish a working head under a 50 mm sofa.

The short cassette targets a whole 254.15 mm-wide print. The long comparison
retains a midpoint split with 15 mm overlap and 177 mm panel spans, but its
assembled width remains too large for the compact robot. Joint hardware, rigidity
and support alignment remain to design.

Edit [vacuum_head_layout.json](../config/vacuum_head_layout.json) for allowance
changes, then run `python3 design/ground/generate.py`. Owner dimensions are read
from the inventory; the [calculation report](../design/ground/output/report.md)
records the formulas and limits. Changeable support plates should allow spacing
development without reprinting the whole bottom.

The [full ground placement](GROUND_PLACEMENT.md) now places this cassette,
bin/filter, upright blower and wheel assemblies with the core and cap. It reserves
a 62 mm side-drive height allowance while retaining the 35 mm cassette roof
reference. The wheel H-bridge occupies an independent bay above that roof. During detailed fitting, establish the working
lengths, drive ends, support caps, filter sealing ledge/tab position and side-brush
hub/sweep radius. No replacement consumables or dedicated test stand are proposed.

The compact arrangement moves the side brush behind the left wheel. A gated
inlet beneath the front dirt well receives its debris, because the rollers have
already passed during forward motion. Gate fit, suction sharing and edge pickup
remain unresolved. The vertical filter holder travels rearward with the low bin;
its upper portion and the upright blower occupy passive core openings but remain
attached to the vacuum bottom. See the full placement for coordinates and service
states before changing these parts independently.
