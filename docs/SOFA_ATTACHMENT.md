# Sofa attachment shared with the ordinary vacuum

**P interface follow-up:** [removable carrier and supported exchange](HEAD_COUPLING.md)
now provides local solids and an electrical/air mating contract. Its rearward
service connections require **120 mm withdrawal / 735 mm combined handling
depth**, superseding the provisional O 100/715 mm values below for P. The
O drawings remain the original comparison; use the
[P viewer](../design/system/output/head_coupling.html) for the new interface.
Mass totals are unchanged while the carrier, compliance and installation scopes
are reconciled. Full head suspension, service supports and station hardware
remain unfinished.

2026-09-14. **Develop a dock-swapped, floor-supported extension that replaces
the ordinary powered floor head.** The owner confirmed one duplicate extension
at each floor station, so neither extension needs to fly between floors.
The owner also confirmed approximately 650 mm of floor in front of both sofas
and 1 m of nearby turning space. This is the preferred architecture to develop
for sofa cleaning, subject to the interface/cleaning checks below. The previous
[dedicated wheeled sofa bottom](LOW_CLEARANCE_HEAD.md) remains a comparison.

[Interactive layout](../design/system/output/sofa_attachment.html) ·
[Calculated comparison](../design/system/output/sofa_attachment.md) ·
[Receiver placement drawing](../design/system/output/sofa_head_receiver.svg) ·
[Hardware ledger](../design/system/output/sofa_attachment_mass.csv) ·
[Parameterized inputs](../config/sofa_attachment.json)

## What is shared and what is exchanged

| Part | Ordinary cleaning | Sofa cleaning | Transfer flight |
|---|---|---|---|
| Core, battery, vacuum chassis and drivetrain | On robot | On robot | On robot |
| Vacuum bin, filter, blower and common duct | On robot | On robot | On robot |
| Body-side head receiver, locks, air/electrical interface | On robot | On robot | On robot |
| Powered normal head and its adapter | Installed | Parked at this floor's dock | Installed |
| Sofa head, telescope, external cart, feed/lift hardware | At this floor's dock | Installed | At this floor's dock |
| Cap / lift | Cap | Cap | Lift replaces cap |

The complete normal head includes the roller, guard/frame, roller motor,
transmission and power stage. Consumable roller replacement remains a separate
manual maintenance operation. The side brush and its motor stay with the vacuum;
disable them when they do not contribute to the sofa task.

Exchange one complete inlet for the other. A gasketed air face mates with the
existing common flex/duct, then leads to the same bin, filter and blower. This
avoids suction through an unused ordinary head opening. Dirty air stays within
the vacuum bottom and its attached tool; none enters the electronics core.
The vacuum bin retains its existing capacity and 300 g maximum modeled debris
load. The attachment uses the main battery, with a protected supply and keyed
tool connector; it has no separate battery, blower or wheel drivetrain.

| Architecture | Main advantage | Cost to resolve |
|---|---|---|
| Complete dedicated sofa bottom | Existing whole-bottom exchange boundary; internal layout can be tailored to telescope | Duplicates drives, blower, bin and filter; transporting it violates the current mass target |
| Extension added while normal head stays installed | Avoids an automatic powered-head removal operation | Requires inlet isolation/diversion and extra mounting space; unused normal head stays aboard during sofa work |
| Extension replaces complete normal head — candidate here | Shares the air system with one connected inlet; frees the head bay and parks unused head mass | Adds an automatic mechanical, air and electrical head-exchange joint |

Keeping the extension on each floor works with either attachment approach.
The head-replacement route is the initial layout candidate, not a demonstrated
minimum-mass solution. If the moving-head exchange joint proves too complex,
compare a separate extension port and positive inlet selector before committing
to its mechanism. Those additional parts are not hidden within this estimate.

## Layout that can be reviewed now

The old internal telescope intersects the ordinary vacuum's head, flex duct,
central duct and front bin. Instead place the telescope on a removable cart in
front, using two nonmarking swivel supports. A pitch/roll-compliant connection
to the vacuum constrains yaw, while a compliant air link crosses that joint.
The working head and intermediate skids support the deployed telescope.

The main body remains **275 × 275 × 180 mm**. With the extension stowed the
combination is **275 × 615 × 180 mm**; this uses the owner's exception for
extensions. Six 245 mm stages with 45 mm overlap provide 1000 mm travel.
The passive suction head is 200 × 60 × 38 mm. Guide height is at most 40 mm
while working, leaving a nominal 10 mm beneath a 50 mm sofa clearance.

At a 20 mm stowed-head setback from the sofa, useful forward reach is **980 mm**,
against 914.4 mm sofa depth. The body itself is then 360 mm from the sofa.
Do not conflate head setback with body setback. The drive cartridge stays
outside the sofa; stage/head lifting is only for travel outside the gap.
The 12 mm raised position makes the guide 52 mm high and cannot enter that gap.

Reach is measured to the head's leading edge; the actual suction-mouth position
remains to define. Full 1000 mm stroke would carry that edge 66 mm beyond the
nominal sofa back. It is available travel, not the commanded cleaning stroke:
stop sooner for a rear wall or other obstruction and retain position/contact
feedback. The layout does not assert clearance behind the sofa.

Nominal approach space is 635 mm in front of the sofa. A yaw-constrained cart
makes the ideal retracted turning sweep about 912 mm diameter, before margins.
The confirmed approximate 650/1000 mm spaces contain these nominal envelopes;
the 15 mm front difference and 88 mm diameter difference are not surveyed
navigation margins. Legs, underside obstacles and actual navigation tolerances
still need checking. While extended, hold the body stationary; retract before
turning or shifting sideways to another cleaning strip.

The receiver review moved the same **1.5 × 40 × 20 mm plates** higher and outward:
their minimum corners are now **[24.5,40,68] and [249,40,68] mm** in the robot
coordinate system (X across, Y front-to-rear, Z up from floor). Each contacts
the outer face of an existing side rail. Their former Z50 location cleared
the stationary head but overlapped its upward movement; it is superseded.
The revised plate reservations clear **105 sampled terrain/raised poses**,
including the existing 16 mm level head lift. Minimum sampled box separation
is 2.86 mm. Plate stock and carried-mass accounting are unchanged.

The plate and air-face reservations are not finished locks or load-rated parts.
Keep the ordinary head's compliance **between its removable fixed adapter and
the moving cleaning head**. The dock supports and locates this assembly before
unlocking; a rigid latch on the roller body would prevent floor following.
The extension's fixed adapter instead connects to its own articulated cart.
Release access, locators, fasteners, electrical contacts and compliant air-joint
separation still need detailed geometry. Existing manually fastened M3
cassettes do not already provide automatic exchange.

## Mass consequences

The complete new attachment is **about 1.25 kg nominal**, with a 0.86–1.91 kg
planning range. It includes inherited telescope/head/feed/lift functions plus
an external frame, support wheels, hitch, connectors, local controls, sensing,
wiring and completion allowances. It is ground equipment. Two resident copies
increase inventory, not the amount carried during a flight.

The ordinary vacuum carries about **109 g of proposed quick-change hardware**:
94 g on the body and 15 g on the normal head. Starting from N, transfer mass is
therefore **5.275 kg**, including core, battery and 300 g debris, excluding the
cap and lift. It remains **775 g over the 4.5 kg limit**. This is an explicit
additional scope in a comparison, not an accepted increase to the target.

With cap and extension fitted, sofa-cleaning ground mass is about **6.10 kg**.
The known 482 g ordinary head plus its new 15 g adapter are parked. Existing
M head mount/lift/riser allowances remain conservatively aboard until a detailed
scope replacement establishes what physically leaves with each head. N still
has unresolved joints/head motion and no complete upper mass estimate. These
figures are estimates, not minimum weights or a validated drivetrain result.

Sharing hardware mainly reduces duplicated equipment and allows the bulky
extension to stay on its floor. It does not by itself lighten the ordinary
vacuum. Optimize that vacuum/core and integrate its quick-change mount within
the **same 4.5 kg budget**. Keep the prior dedicated-sofa estimate in the audit
for comparison, rather than silently subtracting its drivetrain from another
configuration that already has only one drivetrain.

## Automatic exchange concept

Each station needs **one extension nest and one empty normal-head nest**.
One ordinary powered head travels with the vacuum; no second normal head per
floor is required by this sequence. Reserve roughly 270 × 450 × 140 mm for
each extension nest. Normal-head nest and travel space need separate allocation.

Use an external supported exchange apron. The body can approach the apron
backwards, leaving the attached nose tool facing the aisle and accessible to
the station shuttle. Guide/capture the vacuum before operating its locks.
This requires compatible rear approach sensing and station guides. The apron,
tool shuttle and reach are new station design work; the earlier cabinet model
does not demonstrate accommodation of a 615 mm combination.

Use **100 mm straight forward withdrawal** as the initial shuttle stroke, with
the body captured and head supported level at its nominal working height.
The swept boxes of the existing normal head and motor clear the checked fixed
allocations, revised receiver plates and air face. Their rear edges finish
34 mm ahead of the body front. This does not yet check a complete removable
adapter or air-flex disconnection, and is not permission to pull an unsupported
head free.

The extension's reserved air-face tail would finish 16.5 mm ahead of the body
after the same stroke. Robot plus withdrawing extension then occupy **715 mm
longitudinally before clearance margins**. Allocate that path separately from
its storage nest and the operator/recovery aisle. The user's sofa-space answer
does not confirm station-apron dimensions. Complete adapter/hitch withdrawal
and shuttle routing to both nests remain the next station geometry work.

1. Reserve the resident extension and a vacant normal-head nest. Verify battery
   energy for the task and return, plus station availability for recovery.
2. Capture/support the vacuum and normal head. Stop wheel/brush/blower drives,
   isolate tool power and verify the supported state before releasing retention.
3. The station cam releases normally engaged positive head locks. A guided
   shuttle withdraws the whole normal head into its nest, supporting it before
   the last locator disengages. How the floating carrier disconnects is a
   required detail of the head-interface design.
4. Present the fully retracted extension on its supports, engage locators and
   air/electrical faces, and allow the locks to engage. Confirm tool identity,
   seating and positive retention separately. Power its controller only after
   mating; verify position/obstruction signals and an air-seal check before work.
5. Release station support only after the robot can support/control the new
   configuration. Navigate using its larger footprint; lower the head outside
   the sofa and execute measured extension/retraction strips.
6. Return retracted and raised. Capture both body and extension at the apron,
   isolate power, park the extension, then reinstall the normal head. Verify
   retention and inlet sealing again before leaving or changing the top.
7. Enable a transfer mission only when the extension is confirmed absent and
   the normal head is installed/retained, along with the other module, battery,
   mass and flight checks. The resident attachment is not carried to the next
   floor, even if the next task there is sofa cleaning.

This is an automation specification, not implemented controller behavior.
If seating, retention, identification or seal checks fail, keep the parts
supported and stop the exchange. Recovery must allow a bounded reseat attempt
and restoration of the normal head. Loss of power must not release a tool.
Keep enough space for accessible manual fault recovery without making manual
handling part of the normal cleaning cycle.

Head exchange can precede the supported core/bottom/battery workflow. No
assumption is made that the ordinary battery bay can receive the extended
robot. Where mechanism access requires separation, use the station's supported
bottom handling; never depend on a detached tool to support the core.

## Cleaning and drive gates

At an assumed 3.6 L/s, the telescope and extra coupling link add approximately
191 Pa in the smooth-duct model. Actual operating flow still depends on the
blower curve, head, filter loading, leakage and common air path. The smallest
stage's **31 × 19 mm passage** is a particular dog-hair-clump risk; the model
does not demonstrate that clumps pass. Keep seals/fasteners flush, design a
cleanable path, and enlarge or replace the telescope air path if pickup and
clogging comparisons demand it. A passive suction head is a first candidate,
not a demonstrated substitute for the ordinary cutting roller's performance.

Ground support, wheel loads and traction must be solved for the cart retracted
and fully extended. Check the 4–10 mm floor thresholds, wet tire behavior,
turning drag, hinge travel, head lifting and sensor visibility. The existing
N vacuum results do not qualify the heavier attached combination. Added
feed/lift power and travel energy need an updated duty cycle after these loads
are resolved; no new battery or runtime claim follows from this study.

## Confirmed answer and next design step

**Question:** For each sofa, is there roughly 650 mm (26 inches) of clear floor
directly in front, with about 1 m (40 inches) of turning space nearby?
**Owner answer, 2026-09-14: yes.** Recorded in `config/sofa_attachment.json` so
it survives conversation summaries. No room-clearance question is pending.

The next receiver detail is the removable fixed adapter and its positive locks,
with ordinary-head compliance, air disconnect and electrical mating arranged
around the checked forward withdrawal. Couple that drawing to the supported
station shuttle path. Replace the existing O/M allowances with a complete
physical scope when available; this placement review adds no mass or claimed
saving. Vacuum transfer still needs 775 g reduction against its 4.5 kg ceiling.

Reproduce with `python3 design/system/sofa_attachment.py`, then
`python3 design/system/mass_budgets.py`. The viewer and SVGs are allocation
drawings; no fabrication CAD or new order is implied.
