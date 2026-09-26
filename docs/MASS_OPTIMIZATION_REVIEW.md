# Weight optimization review

**T integration result:** [this frame arrangement is rejected](BOTTOM_CHASSIS.md).
Its complete support scope is about 736 g versus 681 g for the old vacuum scope,
including a previously omitted 30 g caster-hardware correction. It also obstructs
head withdrawal. Keeping N's separate motor angles/crossmember while sharing
surrounding supports is insufficient. Do not treat T as an adopted mass increase
or spend more effort completing its joints.

Even removing the whole old 681 g scope would leave the vacuum at 4.594 kg;
chassis-only changes cannot close the 775 g deficit. Compare a structural tray
that directly carries the motor brackets, then the 190 g converter/cooling
assembly and bin/air-path construction. Preserve outputs, capacity and automation.

**S common-core follow-up:** [equipment supports and fixed cartridge receiver](CORE_SUPPORT.md)
now have a 154 g candidate replacing a 210 g scope, approximately **56 g conditional
saving**. The battery/cartridge, G frame, electronics and eight locks are retained.
The vacuum would still be roughly 719 g over its limit if this alone were adopted.
Do not stack R or reduce existing system totals before completion. T above
evaluates the 225 g general bottom frame together with the separate drive
supports and floor-power carrier.

## Owner targets, 2026-09-14

[Mass budgets](MASS_BUDGETS.md) now set **4.5 kg maximum for transfer-flight
assemblies** and a **3.5 kg target for hovering assemblies**, both including
the core, installed battery and loaded tool, excluding the lift top. The cap
is removed for this comparison. At nominal hardware and maximum modeled
contents, the O ordinary vacuum with its resident-extension interface needs
another **775 g** reduction; N mop needs **204 g**. The earlier N vacuum without
that interface needs 666 g, and the former K dedicated sofa bottom needs 981 g.
P's [head coupling detail](HEAD_COUPLING.md) allocates existing adapter/mount
scope without booking a weight saving; complete compliance and service supports
remain unresolved. The wheel-less G/E duster is 2.611 kg
nominal but 3.489 kg at its modeled high estimate. Preserve headroom for
unfinished hardware; these numbers do not establish flight performance.

Regenerate `design/system/mass_budgets.py` for the
[current requirement comparison](../design/system/output/mass_budgets.md).
This requirement takes priority over continuing any over-budget construction.

## First simplification comparison: fixed drive mounts

The [R integrated-frame pass](INTEGRATED_HEAD.md) now counts end walls, pivot
seats, skids, hood, slotted links and guide backings from material geometry.
Including references and unfinished hardware, it is about **162 g against a
170 g frame/compliance scope**, only **8 g conditional reduction**. The powered
lift, carrier and plumbing remain. Integrating parts prevents double counting,
but this local mechanism cannot deliver the remaining system reduction.
Prioritize a concrete comparison of larger shared core, cartridge and structural
assemblies before spending more effort on small cassette-wall savings.

The [Q head-support comparison](PASSIVE_HEAD.md) is a follow-up: a separate
passive mount and dock capture offers only 22–25 g conditional reduction, with
friction and away-from-dock lift/release unresolved. Retain the lift budget and
integrate guide supports with the existing 135 g cassette frame. Do not add a
second complete frame or book the tentative reduction as achieved.

The [N comparison](FIXED_DRIVE_COMPARISON.md) develops a fixed motor-support
and crossmember alternative with **259 g installed planning mass**, replacing
the two K pod scopes totaling 489 g. Potential reduction is **230 g**, giving
5.086 kg vacuum / 4.724 kg mop with every other M allowance retained. This is
conditional, not a new accepted system mass. Nominal stock CAD fits the checked
allocations, but the head needs more travel/tilt, complete joints remain open,
and the mop's rear-heavy placement fails the wet-threshold sensitivity screen.

Independent suspension is a design choice; the requirement is reliable 4–10 mm
crossing with cleaning contact. Before adopting either support architecture,
develop the simpler retained head and correct the mop load distribution.
The [interactive comparison](../design/system/output/fixed_drive.html) exposes
the terrain tradeoffs rather than treating the mass reduction as free.

## 2026-09-14 correction: prioritize simplification before more mechanisms

The owner challenged the M estimates of **5.32 kg vacuum / 4.95 kg mop**.
The direction is inconsistent with the earlier weight-reduction objective.
Local clearance and conservative strength studies progressed while the design
accumulated separate supports and unreconciled installation allowances.

The [G–M audit](../design/system/output/mass_growth_audit.md) reconciles the
increases: **365 g per robot** from replacing the earlier wheel-pod allowances,
then **174 g vacuum / 98 g mop** from M mounts, lifts and risers. The battery
and nominal carried contents are unchanged. These masses include a cap, not a
lift top; flight hardware would add to the carried assembly after cap removal.

The latest estimates remain useful warnings, but **K/M are not the preferred
construction to keep extending**. Retain their geometry/load calculations as
comparison evidence. This instruction supersedes M's next step of detailing
its added carriage and lift without first reviewing the architecture.

The next design work is:

1. **Integrate wheel suspension into the bottom chassis.** Compare a simpler
   swing-arm and bushing arrangement with pivot seats and captured travel stops
   supported directly by chassis ribs/rails. The current separate pods total
   489 g without motors, wheels or hubs, alongside a retained 225 g frame
   allowance. Revisit the load path and conservative strip analogies using real
   geometry; retain the required load cases and verify manufacturing feasibility.
2. **Simplify the vacuum head's floor following.** Compare a passive compliant
   cassette with mechanical retention against M's powered lift and multi-axis
   carriage. Determine whether skids/travel and station-actuated capture can
   satisfy thresholds, docking and whole-assembly lifting. Fully automatic
   operation remains required. A powered vacuum lift is a design choice,
   not an independently stated user requirement. Neither alternative is yet
   validated for 10 mm thresholds or hair pickup.
3. **Give each physical part one mass entry.** The vacuum's 135 g head frame
   already mentions suspension; the mop's 105 g pad/carrier already mentions
   floating supports. M adds 90/80 g mounts beside those entries. Similar
   ownership issues exist among the frame and power shelves. Replace complete
   scopes explicitly; keep a separately identified completion contingency.
   Do not delete an entire allowance merely because part of its description
   overlaps with new CAD.
4. **Review the mop pump and supports after the common chassis.** The 200 g
   dosing-pump reference and separate tank/drive/lift supports are worthwhile
   candidates. Preserve dosing, leakage control, pad performance and capacity;
   select replacements from documented requirements and complete installed mass.

The deliverable is a side-by-side installed mass comparison for a simpler
chassis and head architecture, with the same functions and loads. A lower
headline estimate requires an actual replacement design; no savings are booked
by this audit, and no new orders or prints are needed. Battery capacity, water
capacity, cleaning performance, automatic exchange and full-assembly lifting
remain in scope.

Regenerate the audit and row ledger with
`python3 design/system/mass_growth_audit.py`. The earlier review below retains
its historical figures.

---

The [G frame/joint candidate](FRAME_JOINT_DESIGN.md) now develops the core metal
structure and load path. Including stock and mounting hardware adds about 14 g
over F; the original 145 g frame allowance was not evidence of a lighter,
qualified mechanism. The printed trays and complete floor carrier remain counted.

Follow-up: [revision F core/floor-power partition](CORE_POWER_PARTITION.md)
now supplies a dimensioned candidate, added installation mass and recalculated
carried loads for the first architecture change below. This original review
retains its before-change figures and remaining optimization priorities.

2026-09-13. Owner question: is the current design the lightest achievable across
all modules without sacrificing performance?

**No. The current mass ledger is a preliminary feasibility budget, not an
optimized design or a demonstrated lower bound.** It combines catalog references,
calculated material allowances and unfinished mechanisms. Some choices reserve
space and mass for a function without establishing the best implementation.
Cleaning and flight performance have not yet been demonstrated, so equivalent
performance remains a design and verification requirement.

This review uses `config/system_design.json` and `config/airborne_dusting.json`.
It changes no masses in either model and makes no new procurement selection.
The opportunities below are masses to investigate, not promised savings.

## Present hardware and priorities

| Module | Nominal hardware mass | First items to optimize | Requirements to preserve |
|---|---:|---|---|
| Fixed core | 1,439 g | 305 g printed/metal structure, 130 g coupling locks, 125 g harness; partition tool-specific power hardware | Module interchange, load transfer, computing, sensing, cooling and protected battery exchange |
| Battery cartridge tare | 140 g, additional to cells | Shell/restraint, contact supports, monitoring and receiver interface as one design | Cell restraint, monitoring, current delivery, guided automatic exchange and serviceability |
| Vacuum/drive bottom | 2,124 g | Frame 225 g, bin 195 g, head cassette 135 g and duct/plenum allowance 75 g | Dog-hair pickup, roller service, sealed filtration, bin capacity, head following and floor traction |
| Mop/drive bottom | 1,778 g | 200 g dosing pump; 225 g frame; tank, pad carrier and oscillation/lift mechanism | Dose accuracy, pressure/flow, leakage control, pad force/motion, usable water capacity and wet-floor behavior |
| Under-sofa bottom | 2,433 g | 270 g telescope tubes, 185 g feed drive, 125 g guides/seals; 135 g head | Approximately 1 m extension, 50 mm furniture gap, reliable retrieval, sealing and stiffness |
| Airborne duster bottom | 481 g | 180 g frame, 50 g root socket, 28 g joints and 40 g landing feet | Positive retention, contact compliance, dust capture, tip sensing, landing support and station handling |
| Four-propeller lift top | 2,421 g | 378 g structure, 360 g guards, 430 g harness and 120 g joinery | Installed thrust, continuous duty, control authority, protection, stiffness and power delivery |

Bottom figures exclude the core, battery, carried contents and top. The fixed
core figure excludes the 140 g cartridge tare, which the current assembly ledger
books under `core`. The earlier 1,579 g subtotal includes both. Reclassification
changes no total carried mass. The comparison cells add 753 g. Other lift rotor
counts retain their own complete mass budgets.

### Architecture changes

- Put floor-specific power conversion and braking-energy management in the
  bottoms that use them. The existing 190 g 24 V blower converter and 64 g
  12 V/braking assemblies represent 254 g potentially absent from an airborne
  duster configuration. Revised connectors, raw-pack branch protection, cooling
  and layout must be included before crediting that saving. These components
  remain carried during flight with a floor bottom that needs them.
- Review the core and lift's three stereo camera allocations as one coverage
  design. Sharing a useful viewpoint between modes may simplify hardware, but
  sensor count alone does not establish redundancy. Occlusion, viewing direction,
  latency and loss of coverage must be resolved before deleting a camera.
- Design the load-bearing frame, component mounts and coupling reinforcement
  together within each module. Give each member a load case; avoid budgeting
  separate plastic and metal structures without defining why both are needed.
  Keep the independently removable modules and their positive retention.
- Size each pump, actuator and converter against its required operating range
  and thermal duty. A documented part is a reference, not automatically the
  lightest suitable implementation. The mop pump is a specific sourcing-review
  candidate, not an assertion that a smaller pump already meets the requirements.

### Detailed-design changes

Calculate printed material from actual walls, ribs and mounting geometry. Size
stock members from loads, stiffness, joints and manufacturing constraints. Route
wires to establish length, conductor size, voltage drop and connector mass.
Retain seals, strain relief, cooling and fasteners in the installed totals.

Check uncertain supplied-part weights. In particular, the TriCut 200 g reference
does not yet resolve bare versus packaged mass; the installed blower/filter
figures also remain allowances. Correcting these may move the budget either way.

Lightening a bin by reducing capacity, carrying less water, reducing battery
reserve, deleting guards, sacrificing traction, or reducing sofa reach is a
performance/requirement trade. Extra station visits affect mission duration even
when pickup quality is unchanged. Record those changes separately; do not call
them savings without a performance cost.

## Next deliverable and acceptance

Start with the common core and floor-power partition, then the shared drive/frame
construction. Develop the vacuum, mop and sofa mechanisms from those interfaces;
update the lightweight duster and lift sizing with the resulting complete loads.

For each proposed change, provide:

1. The component or mechanism being replaced and its required function.
2. Dimensioned replacement geometry or a documented candidate assembly.
3. Before/after installed mass and electrical/thermal consequences.
4. Effects on every carried configuration, including water, dirt and battery.
5. The analysis or later physical check needed to preserve performance.

Only then update the nominal mass ledger. No blanket percentage reduction or
all-low mass case is evidence of an optimized robot. Final limits still depend
on the complete flight load and dusting mission, rather than the weight of the
tool alone.

[Whole-system design](SYSTEM_DESIGN.md) · [Current airborne model](AIRBORNE_DUSTING.md)
