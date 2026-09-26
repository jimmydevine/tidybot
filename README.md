# TidyBot

A modular cleaning robot for hard floors, heavy dog hair and automatic operation
across two floors. The project is intended to become open source and adaptable to
different homes and component inventories.

| Section | Purpose |
|---|---|
| Middle electronics core | Shared battery, power distribution, central computing and structural frame |
| Bottom working unit | Wheeled vacuum/mop, or airborne duster with passive feet; resident sofa extension fits the vacuum |
| Top unit | Cap/display or a lift assembly carrying the core and attached bottom |

The completed system must clean, exchange tool modules and swap battery
cartridges automatically. Stations keep spare packs charged while the robot works.
Stations use removable bulk water and waste containers; periodic manual servicing
is accepted. Vacuuming comes first, then mopping and higher-area cleaning.

## Current work: whole-system design

**Bottom-frame comparison:** [T was rejected](docs/BOTTOM_CHASSIS.md).
Keeping the separate motor supports while integrating the surrounding frame adds
about **55 g** and obstructs head withdrawal. The [interactive review](design/system/output/bottom_chassis.html)
shows the material and conflicts. No new mass increase is adopted. The whole old
support/caster scope is only 681 g against a 775 g vacuum deficit, so chassis
changes alone cannot meet the limit. Next compare a chassis carrying the motor
brackets directly, plus lighter power-converter and bin/air-path construction.

**Core support comparison:** [S combines equipment supports and the fixed battery
receiver](docs/CORE_SUPPORT.md), with an [interactive cartridge-path view](design/system/output/core_support.html).
The replacement is about 154 g versus the former 210 g local allocation, a
conditional saving of about 56 g. Battery cells, the complete cartridge, sensors,
protection and module locks remain. This alone projects a 5.219 kg vacuum transfer
assembly, still about 719 g above the limit; no saving is booked yet. T above
evaluates the separately budgeted bottom frame and drive/power supports.

**Integrated head frame:** [R combines the end walls, pivot seats, skids and
pitch-stop supports](docs/INTEGRATED_HEAD.md), with [geometry views](design/system/output/integrated_head.svg)
and a [part-by-part mass comparison](design/system/output/integrated_head.md).
The candidate is about 162 g against the existing 170 g frame/compliance scope:
only about 8 g conditional saving. Powered lift remains. The withdrawal check
also corrects carrier-support interference with the wheel envelopes. Larger
shared assemblies still need redesign to close the weight deficit; no new saving
is booked and these are review models, not fabrication files.

**Owner mass budgets:** [4.5 kg maximum for transfer flights and 3.5 kg target
for sustained hovering](docs/MASS_BUDGETS.md), including core, battery and
loaded working module, excluding the lift top. The
[current budget check](design/system/output/mass_budgets.md) identifies the
remaining reductions; an estimate above its budget remains a redesign candidate.

**Sofa attachment direction:** keep [one dock-swapped extension on each floor](docs/SOFA_ATTACHMENT.md).
It replaces the ordinary powered head while sharing the vacuum drivetrain,
bin, filter and blower. Park the extension and reinstall the normal head before
flight. The [layout comparison](design/system/output/sofa_attachment.html)
reserves a 615 mm stowed depth; the owner confirmed approximate sofa approach
and turning space. Receiver placement now clears sampled head motion; complete
automatic head exchange remains to resolve. Including its proposed interface, the ordinary transfer assembly
is 5.275 kg at maximum modeled debris, still **775 g above the 4.5 kg budget**.

**Head coupling detail:** [P carrier and supported exchange](docs/HEAD_COUPLING.md)
adds local FreeCAD/STEP assemblies, a documented contact reference and an
[interactive withdrawal view](design/system/output/head_coupling.html).
The revised interface needs 120 mm withdrawal and 735 mm station handling
depth before margins. Carrier scope is about 68 g against an allocation of
70 g drawn from existing allowances; complete head compliance, latch guides
and service supports remain unfinished. The complete transfer estimate above
is unchanged. This candidate does not release print files or purchases.

**Weight correction:** the [mass audit and revised work direction](docs/MASS_OPTIMIZATION_REVIEW.md)
take priority over extending the K/M mechanisms. Their rising totals combine
heavy separate wheel supports with additional, partly overlapping allowances.
Next compare a simpler integrated chassis and vacuum-head support, reconcile
one mass entry per physical part, and retain cleaning/automation requirements.
The studies below remain comparison candidates; no weight savings are yet booked.

**Q passive-head comparison:** [independent slides with low head pivots](docs/PASSIVE_HEAD.md)
provide the required sampled travel/tilt, but require redesigned cassette end
frames. The [interactive model](design/system/output/passive_head.html) shows
the motion. A separate dock-only mechanism offers only 22–25 g conditional
saving and has unresolved friction/release behavior. Keep the lift allowance;
integrate the guides into the existing head frame before adding hardware.

**N simplification comparison:** [fixed motor supports and a common crossmember](docs/FIXED_DRIVE_COMPARISON.md)
offer a conditional **230 g reduction**, with all other M allowances retained.
The [interactive review](design/system/output/fixed_drive.html) shows the cost:
greater head travel/tilt and an unresolved wet-threshold load split in the mop.
Complete those checks before adopting the candidate or changing the main mass
ledger. Nominal geometry and a complete local mass scope are available for review.

**M floating-head integration:** the [motion and load study](docs/FLOATING_HEAD_DESIGN.md)
adds separate moving-head mass and proposes clearance for working/raised heads.
The [interactive views](design/system/output/floating_heads.html) show the revised
vacuum power shelf, mop tank and shared electronics positions. Sampled height
stays below 180 mm; added mount/lift allowances bring the vacuum/mop planning
cases to **5.32 / 4.95 kg**. Tightened roller/drive envelopes and actual guide/lift
hardware still need detailed fit checks. No new print or purchase is released.

**L spring and ride-height study:** the [updated suspension calculation](docs/SUSPENSION_SPRING_SELECTION.md)
separates moving pod weight from spring-supported load and checks empty/full
containers, tool pressure and caster direction. The
[interactive results](design/system/output/suspension_springs.html) show fixed
settings for each module and a 10.7 mm stock spring candidate. Nominal spring
checks pass, while some tolerance cases fail. Complete spring selection and
floating-head integration before fabrication; K carried-mass estimates remain.

**K connected drivetrain candidate:** the [pod joints and captured stops](docs/POD_JOINTS_AND_STOPS.md)
add a metal tray, bearing blocks and bolted frame connections. The
[interactive review](design/system/output/pod_joints.html) shows the closed stop
slot. Including the detailed pod hardware raises current ground mass planning
to about **5.14 kg vacuum, 4.86 kg mop and 5.42 kg sofa vacuum**. Spring selection,
remaining joint qualification and fabrication details remain open. L supersedes
K's preload-range inference; G/J are preserved for comparison.

**J wheel-pod mechanism candidate:** the [moving cradle and spring design](docs/WHEEL_POD_MECHANISM.md)
adds a catalog motor bracket, an 8 mm pivot with internal retainers, and rocking
spring seats. Review the [interactive mechanism](design/system/output/wheel_pod.html).
The detailed pin load screen passes, but complete joints, stops and spring
selection remain open. The sofa module is already at the preload limit; the
installed mass must be reconciled before selecting springs or claiming savings.

**I height/mounting candidate:** the [revised layout](docs/HEIGHT_AND_CASTER_LAYOUT.md)
uses a C1 lidar and rotated lift-connector reservation to retain the proposed
wheel travel at a sampled 177.35 mm height, or 179.35 mm with a 2 mm reserve.
A documented caster fitting now has space for its full threaded stem; nearby
equipment moves upward while meeting the existing bin/tank volume targets.
Start with the [interactive comparison](design/system/output/height_mounting.html).
Caster retention and detailed suspension joints remain open; G is still the
complete mass baseline.

**H suspension/support study:** [wheel pivots and caster support](docs/FLOOR_SUPPORT_DESIGN.md)
adds mechanism CAD, impact/spring calculations and an
[interactive travel view](design/system/output/floor_support.html). The proposed
downward wheel travel exposes a height conflict: the nominal 179.1 mm pose can
reach about 181.9 mm in the support model. Frame joints and caster fitting remain
open; G's complete mass estimates remain unchanged.

**Revision G frame candidate:** the [dimensioned corner/frame design](docs/FRAME_JOINT_DESIGN.md)
adds a metal load path through the module joints and checks it against the existing
600 N factored requirement. It adds about 14 g to the F estimate and brings
modeled ground height to 179.1 mm. The floor bridge route is cleared, while its
unfinished replacement supports remain fully counted. Start with the
[core frame CAD](design/system/output/frame_joints_core.FCStd) or
[joint drawing](design/system/output/frame_joints.svg).

**Revision F power-partition candidate:** the [new layout and mass comparison](docs/CORE_POWER_PARTITION.md)
moves floor-specific converters out of the shared core. It saves an estimated
246 g on the airborne duster and 103 g on the mop; vacuum/sofa assemblies gain
87 g with the added support/interface allowances. See the
[F viewer](design/system/output/core_partition.html) for the proposed layout.
The C/E viewers below retain the earlier layout and mass for comparison.

The [weight optimization review](docs/MASS_OPTIMIZATION_REVIEW.md) identifies
unfinished mass allowances and redesign priorities across every module. Current
weights are feasibility estimates; they are not the minimum achievable design.

**Revision E airborne supplement:** the preferred elevated duster omits its
drivetrain, suction system and sofa telescope. See the
[interactive airborne comparison](design/system/output/airborne_dusting.html) and
[dusting design](docs/AIRBORNE_DUSTING.md) for its 481 g nominal tool bottom,
rear-boom balance, documented EDF mass/power comparisons, automatic station
handling and complete flight-energy budgets.
The earlier wheeled duster below remains comparison evidence. Vacuum, mop and
under-sofa modules retain their drive.

**2026-09-13, revision C review: design every module before selecting battery cells.** The active
[whole-system design](docs/SYSTEM_DESIGN.md) covers the electronics/sensor core,
vacuum/drive, mop/drive, under-sofa vacuum, duster, whole-assembly lift and automatic
stations. It supersedes the earlier instruction to defer lift sizing and the
battery-first preference. Existing motor/controller, brush/filter and blower
orders remain recorded; this study adds no purchases.

Start with the [interactive layout and budget viewer](design/system/output/system_design.html).
It compares complete assemblies, batteries, payload and assumed guard loss, with
stowed/extended views and individual component inspection. The
[generated report](design/system/output/system_budget.md),
[robot hardware CSV](design/system/output/system_hardware.csv),
[station hardware CSV](design/system/output/station_hardware.csv) and
[FreeCAD/STEP layouts](design/system/README.md) make the design reviewable.
Inputs are in [system_design.json](config/system_design.json).

[Automatic battery exchange](docs/BATTERY_EXCHANGE.md) now uses a cartridge,
station logic power during handling, and two spare packs in four bays per floor.
Five packs serve the two-floor system, with one carried. Capacity and current
capability remain open; extra packs do not establish unlimited cleaning or flight.

[Lift footprint review](docs/LIFT_LAYOUT_REVIEW.md) explains why the earlier
rotor layout became long. The owner considers its 644 × 1444 mm size excessive;
compact lift and duster geometry are now under review. The updated dusting target
is ceiling fans about 7 ft high, 1 ft below the ceiling, with about 2 ft tool reach.
Baseline duster CAD retains the previous horizontal mechanism; the airborne
supplement provides the rear angled-boom reference for fan-edge access. The longer under-sofa telescope remains required.
The review now includes [weight priorities and ducted-fan comparisons](docs/LIFT_LAYOUT_REVIEW.md#weight-reduction-and-ducted-fan-comparison):
compare complete guarded-propeller, hover-duct and compact EDF installations
before selecting a smaller lift layout or revising the mass allowances.

The everyday floor configurations use a **275 × 275 × 180 mm** nominal allocation
and 270 mm main print panels. The [suspension travel envelope](docs/FLOOR_SUPPORT_DESIGN.md)
still needs qualification. G's earlier estimated loaded floor mass is **4.49–5.06 kg**;
the K drivetrain scenario above increases it to about **4.86–5.42 kg**. Earlier
modeled normal power is **58–122 W**. These are engineering estimates, not
measurements. The eight-rotor lift candidate is much larger: approximately
644 × 1444 mm, about 8.2–8.5 kg complete nominal mass and over 2 kW estimated hover
power. Several upper mass cases fail the thrust-margin screen. Battery current
delivery, flight qualification, custom locks/power hardware, telescope mechanics
and detailed fabrication remain open.

The owner updates and unresolved design gates are retained in the
[design document](docs/SYSTEM_DESIGN.md#13-fabrication-verification-and-remaining-work).
Earlier studies below remain evidence and implementation history; the whole-system
record controls current layout, carried mass and battery decisions.

## Earlier component and ground studies

| Earlier record | Contents |
|---|---|
| [Selected-component integration viewer](design/ground/output/vacuum_integration.html) | Rotatable current placement, layer controls, dimensions and service views; not printable geometry |
| [Integration decisions](docs/VACUUM_INTEGRATION.md) | Trailing wheel pods, interchangeable head, rear bin/filter/blower arrangement and unresolved fit |
| [Converter and caster packaging](docs/VACUUM_POWER_PACKAGING.md) | Distributor converter baseline, cooling stack, corrected swivel allowance and docking clearance |
| [Power and remaining hardware](docs/VACUUM_POWER_AND_HARDWARE.md) | Functional diagram, load allocations and consolidated procurement worksheet with open selections |
| [Ground component recommendation](docs/GROUND_COMPONENT_RECOMMENDATION.md) | Proposed geared drive, 72 mm compliant wheels, wet-floor layout and cleaning-component selection; prices and remaining integration work |
| [Drivetrain sourcing](docs/DRIVETRAIN_SOURCING.md) | Exact distributor part numbers and prices; stock versus Marketplace/on-demand fulfillment; conditional motor and controller alternatives |
| [Current vacuum build plan](docs/VACUUM_MODULE_NEXT_PASS.md) | Orders, work during delivery, arrival checks, first assembly and cleaning milestones; retained earlier layout study |
| [Vacuum recommendation review](docs/VACUUM_RECOMMENDATION_REVIEW.md) | Hair-priority brush investigation, cutting versus shedding, washable-filter candidate, sourcing and evidence limits |
| [Cassette and brush comparison plan](docs/VACUUM_CASSETTE_PLAN.md) | Two levels of replacement, first comparison samples, receiver/air/electrical interface, build order and pickup trials |
| [Earlier vacuum component selection](docs/VACUUM_COMPONENT_SELECTION.md) | Superseded consumable choice; retained blower sources, curve discrepancies, airflow and power calculations |
| [Ground module design](docs/GROUND_MODULE_DESIGN.md) | Core, vacuum, cap, automatic joints and next physical milestones |
| [Low-clearance bottom](docs/LOW_CLEARANCE_HEAD.md) | Separate interchangeable bottom; 50 mm clearance, 36-inch depth and front-only access |
| [Owned-parts reuse](docs/OWNED_PARTS_REUSE.md) | Pi 4, A1 LiDAR, 60 mm wheel reference, two 18 RPM encoder motors and CBM blower; missing electronics |
| [Drive motor alternatives](docs/DRIVE_MOTOR_OPTIONS.md) | Faster encoder gearmotors for 90/60 mm wheels; prices, torque limits, mounts and control requirements |
| [Rolling drive rig](design/experiments/drive_rig/README.md) | Optional BDUAV experiment, paused as the robot's development path; fit history and recording tools retained |
| [Rig preparation before controller delivery](design/experiments/drive_rig/PREPARATION.md) | Two ST boards purchased; remaining supplies, fit checks, measurement worksheet and USB-only diagnostics |
| [Vacuum head and consumables](docs/VACUUM_HEAD.md) | Owned roller/brush/filter kit, proposed cassette and remaining fit measurements |
| [Dimensioned head layout](design/ground/output/vacuum_head_layout.html) | Compare both roller lengths; measured envelopes and proposed cassette clearances |
| [Earlier inventory-based placement](design/ground/output/ground_layout.html) | Core, complete vacuum bottom and cap; dimensioned views and service paths |
| [Earlier placement decisions](docs/GROUND_PLACEMENT.md) | Proposed 275 × 275 × 178 mm body, side-access core trays, rear bin, joint zones and station separation |
| [Inventory record](config/owned_parts.json) | Owned variants, quantities where known, missing items and resolved questions |
| [Ground component ledger](config/ground_components.csv) | Per-assembly requirements, candidates and measured mass fields; not an order |
| [Assembly mass record](config/ground_assemblies.csv) | Complete sections with empty/loaded states kept separate |
| [Design proposal](docs/DESIGN_RESET.md) | Confirmed requirements and overall architecture |
| [Autonomy proposal](docs/AUTONOMY.md) | Scanning, local control, optional MCP/LLM planning and portable profiles |
| [Example home profile](config/examples/straight_stair_home.json) | Owner measurements and explicit unknowns; design data only |
| [Design files](design/README.md) | Current records and retained earlier modeling tools |

Use TAZ 6-printed parts and purchased hardware, with machining kept within the
owner's available tools. A consolidated compatible parts list with costs will
accompany the component layout before proposing purchases. Robot parts and
automatic interfaces are not yet released for fabrication; control/MCP software
has not been implemented.

## Deferred studies

The [earlier packaging study](docs/PACKAGING_STUDY.md),
[interactive concept](design/output/concept.html),
[concept findings](docs/CONCEPT_FINDINGS.md) and
[propulsion comparison](docs/PROPULSION_COMPARISON.md) are retained references.
Their dimensions, flight-driven battery choice and mass estimates do not constrain
the new ground layout. The [EDF experiment](docs/EDF_BENCH_PLAN.md),
[shopping proposal](design/experiments/edf_bench/HARDWARE_LIST.md) and
[cradle files](design/experiments/edf_bench/README.md) are also deferred. The owned
fan remains mounted in the fitting v2 cradle; no thrust measurements were taken.

## Archive

Earlier CAD experiments and superseded architecture are preserved in
[archive/](archive/README.md). They do not govern the current design.
