# Owner mass budgets

Confirmed 2026-09-14. These budgets control subsequent module design and mass
reviews; previous estimates above them remain candidates requiring redesign.

| Flight duty | Budget for the assembly excluding lift | Applies to |
|---|---:|---|
| Short transfer flights | **4.5 kg maximum** | Loaded vacuum/drive or mop/drive, including retained tool interfaces |
| Sustained hovering work | **3.5 kg design target** | Airborne duster and future tools used while hovering |

Both use the same boundary: **complete core + installed battery/cartridge +
attached working module + carried contents**. Include sensors, electronics,
structure, drives, locks, mounts, wiring, connectors, water, wet cleaning media,
debris and retained dust. Include installation/completion allowances until
documented finished hardware replaces them. The budget applies at the maximum
permitted operating load, rather than just with empty containers.

Exclude the complete physically separate lift module. Exclude the ground cap
only when it is actually removed and replaced by that lift module. Spare packs
and equipment left at a station are not carried. The electronics core and
installed battery remain included during both kinds of flight.

**Sofa policy, 2026-09-14:** the owner confirmed one duplicate dock-swapped
extension on each floor. Each stays at its station during a transfer flight.
The [shared attachment candidate](SOFA_ATTACHMENT.md) flies the ordinary vacuum
with its normal powered head restored, including all retained quick-change
hardware. The extension's ground mass is not a separate flight-budget case.

**Takeoff mass = budgeted non-lift assembly + complete lift-module mass.**
The lift module still needs its own optimized, complete installed mass ledger.
Its motors, propellers/fans, guards, structure, controls, wiring, connectors and
any additional energy storage must be included in propulsion/energy sizing.
These new budgets do not establish sufficient thrust or hover duration by
themselves, and do not finalize the battery selection.

For a module with both roles, use the 3.5 kg target for its sustained-hover
configuration. The owner stated 4.5 kg as a maximum and 3.5 kg as the current
hover design target; preserve that distinction in reports.

## Current gap

[Reproducible budget audit](../design/system/output/mass_budgets.md) ·
[Input requirements](../config/mass_budgets.json) ·
[Comparison data](../design/system/output/mass_budgets.csv)

These figures use nominal hardware and the **largest current modeled contents
load**. Each excludes the lift top and the removed 70 g nominal cap.

| Latest applicable candidate | Non-lift mass | Budget | Remaining reduction |
|---|---:|---:|---:|
| O vacuum with head-exchange interface; extension parked | 5.275 kg | 4.500 kg | **775 g** |
| N mop | 4.704 kg | 4.500 kg | **204 g** |
| G/E airborne duster | 2.611 kg | 3.500 kg target | 889 g nominal headroom |

Contents are 300 g vacuum debris, 350 g mop tank water plus 100 g in a saturated
pad, and 30 g retained dust. These are planning loads, not measured capacities.
O adds 108.84 g of interface and normal-head adapter allowance to N's 5.166 kg
transfer estimate. At usual contents, O vacuum/N mop are 5.125/4.654 kg after
removing the cap. O's automatic head interface is a candidate, not completed
hardware; it has not increased the permitted budget.

The earlier K dedicated sofa bottom remains a historical comparison at 5.481 kg
with 250 g debris. Its 981 g excess is preserved in the generated audit, but it
is no longer the transfer configuration for the floor-resident attachment plan.
Neither both resident extensions nor one attached extension are included in O
flight mass. Sofa work on the floor is about 6.102 kg including one extension
and cap; that load needs its own ground-support and traction assessment.

N's 230 g saving remains conditional on a compatible head and completed joints;
O inherits that condition while using the ordinary vacuum. The saving has not
been applied to the separate K sofa bottom. The duster has no wheel drivetrain.
Its high hardware/content estimate is **3.489 kg**, leaving only 11 g under
the target. Nominal headroom needs to absorb unfinished detail and uncertainty.
N has no defined upper mass estimate for its new replacement scope; this is
reported as unknown rather than assumed equal to nominal.

## How to use the budgets

Every further design pass must state its flight duty, included hardware,
maximum allowed contents, predicted carried mass and remaining headroom.
Keep measured values separate from catalog values and unfinished allowances.
Replace each physical scope once; moving a core/tool item into a different
accounting category does not reduce actual mass.

An over-budget candidate requires redesign. A nominal estimate below budget
still needs completion, uncertainty review and eventual weighing. Preserve
cleaning performance, capacities and automated module/battery exchange while
reducing weight. Extra station visits, smaller packs, reduced water/debris
allowances or removed functions are explicit performance trades rather than
unqualified savings. No extra numerical reserve percentage is imposed here.

The immediate priorities remain the vacuum head/chassis and automatic head
interface, the mop's component placement and pump/support mass, and the shared
core. The resident sofa extension needs ground-performance and dock integration,
rather than flight-weight optimization. Protect the lighter duster's headroom
while these common parts are completed.

Run `python3 design/system/mass_budgets.py` to refresh the comparison. The
requirements live separately from historical geometry configurations so adding
a limit does not rewrite an estimate or invalidate unchanged CAD. The report
checks planning budgets; it is not flight-control firmware or a flight release.
