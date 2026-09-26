# TidyBot whole-system design — revision C review

**T bottom-frame decision, 2026-09-15:** [reject the surrounding-frame integration](BOTTOM_CHASSIS.md)
that retains N's separate motor supports. The complete local estimate rises about
55 g and the head/service path has obstructions. This is not an adopted weight
increase. T also includes the 30 g caster-hardware correction omitted from the
older N/O ledger. The 681 g old support scope is smaller than the 775 g vacuum
deficit: a real chassis reduction must be accompanied by changes elsewhere.
Next compare direct motor support in a structural tray and lighter implementations
of the power stage and bin/air path while preserving their performance.

**S shared-core result, 2026-09-15:** [core supports and battery receiver](CORE_SUPPORT.md)
offer about 56 g conditional reduction with the existing battery capacity, complete
cartridge, sensing, protection and locks retained. New supports have vacuum/mop
clearance and exchange-path checks; several mounts and latch/contact details are
unfinished. Duster integration remains a mass projection. The current 5.275 kg
ordinary transfer estimate is unchanged; S alone would bring it to about 5.219 kg,
still about 719 g over the limit.

**R head-frame result, 2026-09-15:** [integrated cassette ends](INTEGRATED_HEAD.md)
combine pivot seats, skid ramps, stops and end walls within one local ledger.
The candidate is about 162 g against the existing 170 g frame/compliance scope,
only about 8 g conditional saving; powered lift and plumbing stay. The full
transfer estimate below is unchanged. The short air connection still needs
about 29.68 mm reach in a nominal 25 mm axial space when the head is raised.
P carrier supports have moved forward to clear the wheel envelopes during
withdrawal. These are reviewed geometry changes, not a fabrication release.

**Owner mass requirements, 2026-09-14:** [transfer assemblies have a 4.5 kg
maximum; hovering assemblies have a 3.5 kg design target](MASS_BUDGETS.md).
Include the complete core, installed battery/cartridge, attached working module
and maximum permitted contents; exclude the complete lift top and a cap that
is removed for flight. Actual aircraft mass adds the lift module back. These
requirements supersede any inference that an earlier heavier estimate was
accepted. [Current gaps](../design/system/output/mass_budgets.md).

**Sofa direction, 2026-09-14:** use [a dock-swapped extension resident on each floor](SOFA_ATTACHMENT.md)
as the candidate to develop. It replaces the normal powered head and shares the
vacuum drives, bin/filter/blower, core and battery. Restore the normal head and
park the extension before flight. The O interface allowance brings the ordinary
transfer candidate to 5.275 kg at maximum modeled debris, still 775 g over budget.
The former complete sofa bottom and its geometry below remain comparisons.

**P head interface:** [carrier, connections and exchange sequence](HEAD_COUPLING.md)
provides local CAD and a revised 120 mm withdrawal stroke. About 68 g of carrier
scope is allocated within existing mount/adapter budgets; only 35 g remains
for unresolved compliance. The complete transfer estimate stays unchanged.
Its 735 mm handling depth still needs integration with a supported dock layout.

**Q head-support comparison:** [independent slides and low pivots](PASSIVE_HEAD.md)
close the sampled kinematic constraints but require cassette end-frame rework.
A separate dock-only passive mechanism offers only 22–25 g conditional saving,
with friction and away-from-dock head release unresolved. Retain the powered-lift
allowance and integrate the guides with the existing frame; no reduction is booked.

**Weight correction:** [review and next work](MASS_OPTIMIZATION_REVIEW.md)
supersedes extending the K/M mechanisms. Their increasing mass requires a
simpler integrated chassis/head comparison and explicit reconciliation of old
allowances with new hardware. Preserve the following studies as evidence;
their estimates are not established minimum masses or accepted construction.

**N simplification comparison:** [fixed drivetrain mounts](FIXED_DRIVE_COMPARISON.md)
offer a conditional 230 g reduction against M, keeping all other mass allowances.
Nominal new-stock geometry clears the checked vacuum/mop allocations. Greater
head travel/tilt and the mop's wet-threshold load split remain unresolved;
5.086 / 4.724 kg are comparison estimates, not adopted system masses.

**M floating-head follow-up:** [motion, clearance and loads](FLOATING_HEAD_DESIGN.md)
finds conflicts in the original working-head space and proposes revised vacuum
and mop layouts. The ideal floor-following calculation includes head weight,
counterbalance/preload and moving water. Revised planning cases are 5.32 kg
vacuum and 4.95 kg mop after added mechanism allowances. The smaller component
envelopes, actual carriage/lift hardware and shared-core changes remain to
verify; the original C geometry below is not the current motion proposal.

**L spring and ride-height follow-up:** [spring selection](SUSPENSION_SPRING_SELECTION.md)
corrects spring loading for moving wheel/pod mass and solves the loaded chassis
attitude. A stock-spring candidate passes nominal checks with module-specific
settings, but tolerance and floating-head integration remain open. It supersedes
the K/J preload inference; K carried-mass estimates remain the planning scenario.

**K connected drivetrain follow-up:** [pod joints and travel stops](POD_JOINTS_AND_STOPS.md)
replaces the earlier pod allowances with a complete local hardware estimate.
Current ground mass planning becomes about 5.14 kg vacuum, 4.86 kg mop and
5.42 kg sofa vacuum. Other G frame/carrier allowances remain. The captive slot
provides both nominal travel limits; spring selection and complete structural
qualification remain open. Earlier mass figures below are comparison baselines.

**J wheel-pod follow-up:** [moving cradle, pivot and spring seats](WHEEL_POD_MECHANISM.md)
adds reviewable mechanism solids and checks the actual full-bump stop lever.
The 8 mm pivot passes the preliminary load screen. Complete joints and stops
remain unfinished, and the sofa module needs more preload range after revised
mass accounting. G remains the complete mass baseline.

**I height/mounting follow-up:** the [revised ground layout](HEIGHT_AND_CASTER_LAYOUT.md)
passes the sampled height screen at 179.35 mm including a 2 mm reserve, using
a C1 lidar, revised connector placement and the same H travel. Caster fitting
space is corrected; caster retention and complete suspension joints remain open.
G remains the complete mass baseline.

**H suspension/support follow-up:** [wheel pivots and caster saddle](FLOOR_SUPPORT_DESIGN.md)
provides revised mechanism candidates and exposes a suspension-height conflict.
G remains the complete mass baseline; nominal fit does not qualify full travel.
Use the corrected continuous motor/gearbox limits in section 5 below when
interpreting older generated traction screens.

**Revision G mechanical candidate:** [frame and module joints](FRAME_JOINT_DESIGN.md)
defines the proposed corner stock, slider motion, mounting rails and load screens.
It changes the top seat to 124.1 mm and updates complete configuration masses.
The C interface and frame figures below remain historical comparison inputs.

**Revision F candidate:** [core/floor-power partition](CORE_POWER_PARTITION.md)
provides the proposed revised converter locations, raw-pack bottom interface,
carrier geometry and complete before/after masses. The C power interface and
mass figures below remain its comparison baseline; do not combine their old
regulated-rail pin assignments with the F raw-pack interface.

2026-09-13. This is the active preliminary engineering design for the **whole
robot**, superseding the instruction to defer lift sizing and the earlier
battery-first preference. No battery, additional hardware or fabrication is
authorized by this document. Existing orders remain recorded in the earlier
procurement documents.

**Revision E airborne supplement:** [AIRBORNE_DUSTING.md](AIRBORNE_DUSTING.md)
replaces the elevated-duster architecture below with a wheel-less, station-serviced
tool bottom. Its new mass, launch/landing handling, raised boom and mission model
are in the [airborne comparison](../design/system/output/airborne_dusting.html).
The wheeled duster, all-wheeled fleet counts and duster floor runtime below remain
historical comparison figures. Core, vacuum, mop, sofa and battery-interface
allocations remain the shared inputs to that supplement.

The [weight optimization review](MASS_OPTIMIZATION_REVIEW.md) identifies the
next architecture and detailed-design opportunities across all modules. The
current mass ledger has not established a minimum achievable weight or proven
performance; its allowances remain unchanged until replacement designs support
specific savings.

Revision B adds the owner-required automatic battery cartridges and charged
station spares. See [battery exchange](BATTERY_EXCHANGE.md) for the cartridge,
power handover, rack and charging-throughput design.

**Revision C review:** the owner considers the 644 × 1444 mm lift footprint
excessive. It remains comparison geometry while compact lift layouts are
investigated. The dusting target is now ceiling fans about 7 ft high, 1 ft below
the ceiling, with about 2 ft tool reach. The existing horizontal duster geometry
does not yet implement that target. See [lift layout review](LIFT_LAYOUT_REVIEW.md).

This revision C baseline accounts for one electronics core, one complete wheeled bottom,
one cap or lift top, a battery, carried dirt/water, and the machinery needed to
exchange and service the modules. It specifies the mechanisms and their reserved
spaces well enough to expose weight, power and space conflicts before parts
arrive. It is **not a completed production CAD or electrical release**: supplier
interfaces, custom power hardware and several mechanisms still need detailed
qualification. Those limitations are identified below rather than represented
as zero mass or proven performance.

- [Interactive layout and budget viewer](../design/system/output/system_design.html)
- [Generated mass, power and feasibility report](../design/system/output/system_budget.md)
- [Robot hardware by configuration](../design/system/output/system_hardware.csv)
- [Station hardware, per floor](../design/system/output/station_hardware.csv)
- [Mechanical stock schedule](../design/system/output/mechanical_stock.csv)
- [Editable design inputs](../config/system_design.json)
- [FreeCAD/STEP exports and reproduction instructions](../design/system/README.md)

The hardware CSV contains **alternative complete configurations**. Summing all
its rows would incorrectly add multiple robots together. The older
`ground_components.csv` and `ground_assemblies.csv` remain measurement records;
this study does not fill their blank measured weights with estimates.

## 1. Requirements and design boundary

| Requirement | Treatment in this revision |
|---|---|
| Core in the middle; wheels and cleaning machinery in interchangeable bottoms | Retained. Each complete bottom has two drive motors, one controller, suspension, support wheels and local sensing. |
| 275 × 275 mm rigid ground body, 180 mm total height | Everyday vacuum and mop allocations fit; scanner top is 178 mm. Main printed panels are 270 × 270 mm. |
| Extensions may exceed the footprint | Sofa retains approximately 1 m reach for 914 mm depth. Elevated duster now targets about 610 mm tool reach; the previous 1 m horizontal model is retained pending redesign. |
| Lift carries core and attached working bottom | Calculated with water/dirt still aboard. Cap is removed before lift attachment. |
| Three heavy-shedding dogs, wood/tile | Hair-cutting brush comparison, sealed collection, accessible bearings, compliant drive tires, wet-floor traction checks and pet-aware stopping. |
| 4–10 mm thresholds | 72 mm drive wheels, 10 mm upward suspension travel, 14 mm structural underside clearance; threshold speed target 0.05 m/s. Sharp wet thresholds remain a problem case. |
| Two floors, about 1000 ft² each | One station per floor; multiple charging/service visits allowed. |
| Fully automatic routine operation | Autonomous charging, module exchange, bin emptying, mop filling/washing and mission recovery are hardware requirements. Periodic bulk servicing remains manual. |
| 50 mm sofa gap, 914 mm depth, approach only from front | Separate low head, ≤40 mm working envelope, floor-supported telescope; main body remains outside. |
| Available fabrication tools | Printed PETG parts, purchased fasteners/bearings, cut/drilled aluminum strips and stock tubes. No lathe or mill assumed. |

The expanded lift footprint is **unresolved**. The owner considers 644 × 1444 mm
excessive; it is comparison evidence, not an accepted requirement. A compact
layout must be assessed with the same complete-payload requirement and the
existing 180 mm height limit. No automatic exception to that height is assumed.

The owner specifies ceiling fans approximately **2134 mm above the floor** and
**305 mm below the ceiling**, with about **610 mm desired duster reach**. These
supersede the earlier 2 m / 300 mm shelf assumption. The reach datum and blade
access need detail; the current horizontal boom is not a ceiling-fan solution.
The 914 mm under-sofa depth requirement remains unchanged.

## 2. Whole-robot results and their meaning

These nominal totals use the **753 g, 6S 5200 mAh comparison pack**, with no claim
that it is the final battery. Hardware, installation materials and contents are
included. The generated report is authoritative after input edits. Duster rows
retain the earlier horizontal mechanism; new fan-access articulation has not
yet been designed or added to those masses.

| Installed bottom + core + cap | Nominal loaded mass | Engineering low–high | Normal / high battery power | Illustrative floor-only runtime |
|---|---:|---:|---:|---:|
| Everyday vacuum | 4.68 kg | 3.56–6.29 kg | 116 / 195 W | 48 min |
| Oscillating mop | 4.58 kg | 3.66–5.93 kg | 58 / 123 W | 96 min |
| Under-sofa vacuum | 4.96 kg | 3.77–6.79 kg | 122 / 191 W | 45 min |
| Duster, moving on the floor | 4.88 kg | 3.69–6.71 kg | 90 / 191 W | 62 min |

Runtime uses 80% of nominal pack energy and the stated assumed loads. It excludes
flight reserves and service delays. For the extension cases the budget
conservatively retains the 20 W driving allowance even though the main wheels
must stop while a floor-supported head is deployed. Actual duty-cycle data will
replace that allowance later. Blower pressure, flow and power are coupled;
throttle percentage alone does not establish suction power.

At 180 mm useful vacuum swath, 0.22 m/s and 60% effective coverage, a 1000 ft²
floor takes about **65 minutes of modeled coverage**. The example battery thus
requires a battery-exchange visit even before flight is considered. Mopping at 230 mm,
0.14 m/s and 55% coverage takes about 87 minutes, before wash visits. These are
planning calculations, not room-cleaning trials.

The bounds are deliberately explicit engineering cases, **not statistical
confidence intervals**. Some rows use catalog weights; others use calculated
stock volume; custom wiring, seals and mechanisms have installed allowances.
Neither all-low nor all-high is a likely manufactured outcome. There is no
unlisted final “contingency” multiplier concealing missing assemblies.

The largest unresolved consequences are:

- Flight with the eight-rotor top is roughly **8.2–8.5 kg nominal**, depending on
  bottom, and about **2.4–2.6 kW in the hover model**. It is a much larger machine
  than a normal cleaning robot.
- The eight-rotor frame is **644 × 1444 mm**. The quad is smaller but fails the
  provisional 2:1 thrust/weight target even at nominal mass.
- The eight-rotor candidate clears the nominal thrust screen, but several
  high-mass cases do not. This remains a design candidate, not an approved lift.
- A 5200 mAh pack's energy capacity does not establish that its connector,
  wiring, cells or protection can support the approximately **115–123 A hover
  demand** and roughly **300 A short maneuver envelope**.
- A full automatic station is a substantial appliance: reserve **1200 × 1800 mm
  footprint, 1500 mm height, plus 1600 mm approach**, per floor. The approach may
  overlap ordinary open floor when the station is idle.

## 3. Coordinate system and core construction

Coordinates are millimetres: x right, y rearward, z above floor; front is y=0.
The fixed-body limit is [0,0,0] to [275,275,180]. Layout drawings show equipment
reservations and nested component references, not a solid stack of rectangular
plastic blocks.

The **core hardware subtotal is 1.579 kg nominal**, including one cartridge
carrier/monitor and fixed exchange hardware, but excluding the bare cell pack. Its construction uses two
open aluminum perimeter frames, metal spacers and through fasteners, with printed
trays/ribs. Four 270 mm and four 250 mm pieces of 10 × 2 mm strip make the two
frames. This replaces the need to machine large rings from plate. Frame strips
occupy z=86–88 and z=121–123; joints and bolt-hole detail remain to release.

| Core area | Placement and hardware |
|---|---|
| Front left | Cincon 24 V converter, heatsink/fan, separate 12 V and 5 V regulators; 113 × 70 × 46 mm allocation |
| Front right | Raspberry Pi 5 with active cooler and microSD; 104 × 70 × 34 mm bay |
| Front face | OAK-D S2 stereo camera, below the main logic trays; 104 × 26 × 31 mm reservation |
| Centre | 180 × 66 × 55 mm automatic battery cartridge/receiver at [44,86,66]; internal bare-cell pocket 158 × 62 × 53 mm; installed pack fit unqualified |
| Left middle | ESP32-DevKitC class core controller, CAN transceiver and independent watchdog |
| Right middle | Fixed switched discharge bus, precharge, shunt and protection stage; cell monitoring travels with cartridge |
| Above left battery edge | 35 × 60 × 20 mm auxiliary dock logic supply at [45,90,124]; reverse-blocking handover |
| Above centre | Core-fixed RPLIDAR A1 at [86,94,123]; upper envelope z=178 |
| Perimeter | Six outward range sensors; stop switch, audible/visible status, lock sensing and module identification |

The cap is contoured: power-bay roof at 135 mm, dock-power roof at 146 mm, a local lift-connector fairing
below 160 mm, and an opening around the fixed scanner. It does not force every
component under a flat 123 mm lid. The core stays fixed relative to its sensors
when bottoms are exchanged.

Front/rear converter airflow uses a clean, isolated cooling passage. Vacuum
exhaust and dirty air do not cool electronics. The battery is below the scanner,
close to the drive axle, with a positive cartridge latch and accessible service
disconnect. The station removes the bottom before extracting the cartridge
downward; the guide and recessed contact layout still require detailed design.

The battery tray dips below the 86 mm bottom seating plane. Corresponding reliefs
in every bottom permit straight vertical separation. This is intentional nesting
between modules; it is not permission for a tool to trap the core during exchange.

## 4. Common mechanical and electrical module interfaces

The four coupling centres are **[14,14], [261,14], [14,261], [261,261]** in x/y.
Bottom seats are at z=86 and top seats at z=123. A round locating pin and a
relieved second pin establish position without four overconstrained tight holes.
Four hard seats establish the plane. Replaceable wear inserts carry repeated
docking contact.

Each joint uses a through-bolted M4 mushroom shoulder, a captive **18 × 28 × 2 mm
steel sliding plate**, approximately 8 mm release travel, and 0.5 mm final draw.
The plate admits the head through a larger entry and captures its neck in the
locked position. A spring pawl positively retains the plate. Station cam bars
move the four locks together; release requires the station to support the load.
Switches detect seating and full lock travel separately. Thread friction or a
powered servo alone does not hold a flying module together.

An initial **600 N factored axial load-path requirement** covers the roughly
11 kg upper comparison assembly with additional dynamic allowance. Four anchors
nominally share 150 N each; unequal load and moments still require joint analysis.
Through bolts, metal seats and load spreaders transfer this force into the
aluminum frames. Printed threads or heat-set inserts are not the primary flight
retention path. The steel lock blanks can be drilled/filed with the available
tools or supplied by a flat-part cutting service; no precision mill is assumed.

The drawings establish the coupling locations and load path, but do not yet
release cam profiles, fatigue strength, wear tolerances or proof-load procedures.
The 130 g core-lock allowance includes all eight locks, springs, seats and
detection. Module-side studs are in their respective frame allowances.

Electrical reservations are common to all bottoms:

| Interface | Allocation / contract |
|---|---|
| Bottom mating carrier | [4,160,58], 18 × 50 × 27 mm; floating mount, lead-in guides and replaceable contacts |
| Floor power | Keyed 12 V up to 8 A allocated; 24 V up to 3.3 A; 5 V up to 1.5 A; dedicated power returns |
| Floor signals | CAN H/L, logic ground, presence loop, hardware-enable loop, identification/service |
| Top carrier | [193,88,123], 78 × 32 × 35 mm; separate raw-pack power and flight/control contacts |
| Flight power requirement | Target at least 150 A hover/service capability, about 320 A short maneuver capability; component selection still open |

These are **contact-system requirements**, not a claim that a hobby XT connector
is a qualified blind-mate connector. Prefer replaceable, independently guided
power and signal inserts over contacts molded into a structural printed latch.
Insertion force, wipe length, cycle life, insulation and the high-current
assembly still need supplier drawings and electrical design. Their installed
mass is already budgeted.

Exchange sequence is: outputs disabled, current verified near zero, station
support engaged, locks released, modules separated, new module guided onto
seats, locks and ID verified, then precharge and branch enable. No live tool
contacts are intentionally mated. A partial exchange remains mechanically
supported and electrically disabled.

## 5. Drive hardware shared by every complete bottom

Retain two **Pololu 4846, 75:1, 12 V encoder gearmotors**, two 72 × 24 mm goBILDA
Hogback silicone wheels, two 4 mm Sonic hubs and one **RoboClaw IMC404** per
bottom. These choices remove the uncertain gimbal-motor commutation and custom
encoder-magnet interface from the main robot. The motor is published at 130 RPM
no-load, 104 g and 5 A stall; stall torque is not a continuous operating rating.
[Motor specification](https://www.pololu.com/product/4846/specs),
[controller specification](https://www.basicmicro.com/RoboClaw-2x7A-Motor-Controller_p_55.html).

The wheel-to-hub mating geometry was checked against supplier CAD in
[drivetrain sourcing](DRIVETRAIN_SOURCING.md#wheel-to-hub-check-2026-09-12).
Maintain clearance from the motor face; verify the clamp grips the D shaft and
wheel screws do not bottom out. The 12.5 mm shaft, 8 mm hub body and 4 mm wheel
web are accounted for as a nested assembly; the hub is not an extra 8 mm outside
the 24 mm tire width. Actual bracket holes, clamp-tool access and shaft bending
loads still need the cartridge detail release.

The C/G reference wheel contacts are at x=14/261, y=108, with the axle 36 mm above floor.
The [H candidate](FLOOR_SUPPORT_DESIGN.md) moves them to y=105 and specifies a
rear-mounted 6 mm pivot; the earlier M4 pin fails its impact screen. Each motor
rides in a 40 mm leading arm, with bushings, metal motor plate,
replaceable spring and positive stops. Approximately 10 mm upward wheel travel
is reserved; the arc moves the axle rearward about 1.3 mm. Target 0.8 N/mm at the
wheel: H's 0.4 motion ratio requires about 5 N/mm at the spring. Set each module's
preload from its assembled wheel loads.
Do not use spring travel as extra space for motor wires.

The rear support candidate is the **TENTE 5940UAP050L51-8**: twin 50 mm
polyurethane wheels, 50.5 mm overall height, 40.5 mm swivel radius, thread guards
and a catalog mass of 90 g. Installed allocation is 112 g. It sits centrally in
the vacuum/mop and moves to the rear right for the telescope bottoms. Its 92A
tread is substantially harder than the driven tires. It is chosen for documented
height/sweep and debris protection, not because it is proven ideal on wet wood.
[Manufacturer dimensions](https://www.tente.com/en-ca/swivel-castor-50-mm/5940uap050l51-8-load-9011).

Two front backup rollers use 624-2RS bearings, printed hubs, silicone O-rings and
M4 shoulder hardware. Their 20 mm treads normally sit 2 mm above floor, catching
forward pitch after about 1.2°. They are not normal swivelling support wheels.
They are necessary because several independent mass/position-bound cases put the
CG ahead of the nominal three-contact support triangle. The expanded contact hull
has positive static margin in this model, but does **not** prove that a pitched
head keeps proper floor contact or that the robot can turn on the backup rollers.
Finished weight distribution must preserve normal caster loading; otherwise
reposition hardware rather than declaring the backup rollers a cure.

The earlier model sets wheel current to 2 A per motor, giving about 0.78 N·m
in its DC approximation, versus roughly 0.07–0.11 N·m for assumed level cleaning
loads. **Correction from the H review:** the manufacturer's 4 kgf·cm continuous
gearbox guidance gives 0.392 N·m, which supersedes the older 0.54 N·m
fraction-of-stall screen. Its 8 kgf·cm intermittent guidance is 0.785 N·m.
The general 25%-of-stall-current guidance corresponds to 1.25 A. Treat 2 A as a
bounded transient setting, with duty and temperature limits; the old generated
traction outputs do not establish continuous permission at that setting.
[Manufacturer load guidance](https://www.pololu.com/product/4846).

**The difficult transition is pushing the rear caster over a sharp edge.** With
the loaded mop, the 10 mm edge calculation needs roughly μ=0.56 floor traction,
above the model's 0.2–0.5 wet-floor sensitivity range. Wheel motor torque alone
does not resolve this. Raise the pad, stop dosing, cross before wetting that area,
and retain an approach on dry floor. If crossings must occur while everything is
wet, a passive transition ramp or a revised driven/support arrangement is needed.
The current design does not claim guaranteed wet 10 mm step climbing.

Six downward/outward cliff sensor allocations avoid using the low front camera
as a cliff detector. Two wheel-drop switches and segmented bumpers feed the
bottom controller directly. Their oblique optical paths must clear the rotating
caster and cleaning head; bounding-box clearance does not validate a ToF cone.

## 6. Everyday vacuum / drive

The front head is a **230 × 60 × 50 mm removable cassette**. The initial insert
accepts the ordered Dreame TriCut reference and a matching plain roller for
comparison. Two spring-guided vertical links give the head compliance independent
of wheel movement. A smooth replaceable lower lip, guarded roller ends and an
accessible hair-removal path support the dog-hair priority.

A **Pololu 4842 9.7:1 encoder motor**, 1:1 timing belt, supported drive stub and
TB9051FTG carrier are allocated above the left end. The motor is a published
1000 RPM no-load, 95 g reference. An initial adjustable 650–900 RPM control range
is a development allocation, **not an approved TriCut speed**. The stationary
cutter restraint and safe cutter loading must match the actual purchased brush.
Do not simply spin a cutter cartridge whose stationary portion is unsecured.
[Motor data](https://www.pololu.com/product/4842/specs),
[TriCut product reference](https://www.dreametech.com/products/anti-tangle-roller-brush).

An independent **Pololu 5216** micro gearmotor drives the flexible edge brush.
The sensor/controller stops and optionally reverses the roller on a sustained
current/encoder mismatch; it stops the side brush separately on a jam. Bearing
caps and end inserts remove without dismantling the electronics core.

The air path is:

```text
front roller / floor lips
  -> compliant throat -> central smooth duct
  -> U-shaped drop-out bin -> filter -> clean plenum
  -> BIQU/Wonsmart blower -> diffused upward/rearward exhaust
```

The bin wraps around the centre caster and under the raised filter tray. Three
connected volumes reserve approximately one litre gross; **0.50 L usable fill**
is the conservative target after baffles, wall thickness and the caster relief.
Budget 150 g dirt nominal, 300 g upper case, regardless of whether a bin-full
optical detector sees fluffy hair reliably. A station weighing check provides a
second way to prevent excessive flight payload. A large rear evacuation gate
opens only after the station is sealed to the port.

The filter adapter reserves a **141 × 76 × 20 mm maximum element** within a
156 × 96 × 35 mm bay. That is not a measured S7/S8 filter. The ordered element
needs a replaceable perimeter seal and a tool-free pull tab. Emptying the bin is
automatic; periodic filter washing/replacement remains a manual bulk-service task.
Filter removal is a rearward drawer operation after the station has separated
the core from the bottom, so it need not pass through a frame rail.

The **WS7040-24-V200 / WS2403DY01V04** reference from the ordered BIQU kit sits
rear right in a 77 × 86 × 68 mm bay. It remains a provisional blower choice.
The BIQU motor sheet gives a 24 V point of 13 m³/h at 4 kPa and 1.9 A; its
free-flow and maximum-pressure points are different conditions. The driver
sheet's 9–29 V range does not establish that the motor may be run at any such
voltage. Use a regulated 24 V rail and a hardware default-off interface because
the supplied driver's EN behavior must not cause a startup on a floating wire.
[BIQU documentation](https://global.bttwiki.com/Universal%20Turbo%20Kit.html),
[motor sheet](https://global.bttwiki.com/img/Turbo_Kit/Turbo_Kit_Motor1.webp),
[driver sheet](https://global.bttwiki.com/img/Turbo_Kit/Turbo_Kit_Driver1.webp).

Reserve two differential-pressure channels (0–10 kPa class), protected pressure
taps before/after the filter, a bin-fill sensor and motor-temperature sensing.
The channels distinguish a dirty filter from a nozzle restriction. Exact sensor
board selection and any 5 V analog-to-3.3 V ADC interface are unresolved within
the installed 38 g allowance. Initial air-path targets at 3.6 L/s are below
2.5 kPa clean and 3.8 kPa at the service limit, including the head and filter;
these are design targets requiring pressure-loss evidence, not measured values.

## 7. Mop / drive

Use a **230 × 32 mm oscillating microfiber pad** immediately behind the drive
wheels and ahead of the rear caster. Two large spinning disks would compete with
the tank, rear support and drive pods in this body. The shallow pad retains a
full cleaning width and leaves the rear volume available for water hardware.

A vertically placed Pololu 4842, 1.5 mm eccentric radius, counterweight, links
and two flexure guides create a **3 mm peak-to-peak stroke at about 15 Hz**.
Initial normal force is 8 N, approximately 1.1 kPa over the pad area. Both force
and frequency remain adjustable. Dynamic reaction isolation belongs in the pad
carriage, keeping vibration away from the scanner and electronics.

An **Actuonix PQ12-100-6-R**, separate 6 V supply, four-bar linkage and end
switches lift the pad 12 mm using part of its 20 mm stroke. The manufacturer
lists 19 g, 6 V, 50 N maximum load and 10 mm/s no-load for this exact version;
the installed 62 g allowance also includes links, regulator and mounting. A hard
stop supports the raised carriage. The servo need not remain stalled to hold it.
[Exact actuator reference](https://www.actuonix.com/pq12-100-6-r).

The left tank is **350 mL clean water**, baffled, with a retained cap, dock-fill
seal, level detection and leak tray. Budget another 50 g water retained by the
pad, 100 g in the upper case. A **12 V Adafruit 1150 peristaltic pump** feeds a
drip manifold, with a shutoff/check arrangement that prevents siphoning when
lifted. Its published 200 g mass is included; it is not modeled as a tiny 20 g
micropump. A lighter pump can substitute only with known flow, suction and
leak behavior. [Pump dimensions and data](https://www.adafruit.com/product/1150).

Start with dosing recipes of 3 mL/m² on wood and 6 mL/m² on tile. At the chosen
speed and width this is approximately 6 and 12 mL/min while actively laying a
strip, within the pump's stated capacity. Stop water immediately on stopped
motion, lifted pad or a leak. These starting recipes must be adjusted for the
wood finish and actual pad wetness.

The station washes the pad every 10 m² initially, using about 120 mL per wash,
scrubs it against a driven station roller, drains through a removable hair
strainer and dries it with unheated air. Dirty water stays at the station; this
bottom is not a carried extraction mop. No claim of sanitation or complete
drying at a fixed time is made. The rear caster may mark a fresh wet strip;
crossings and wash paths should place that contact near a previous/drying lane.

## 8. Sofa extension and dusting bottoms

**Historical layout:** the [O resident extension](SOFA_ATTACHMENT.md) moves the
sofa mechanism outside the ordinary vacuum; the [E airborne duster](AIRBORNE_DUSTING.md)
omits a wheel drivetrain. Those directions supersede the complete wheeled
bottoms in this section. The old internal telescope cannot fit unchanged inside
the normal vacuum, and its stowed outline/standoff do not apply to O.

These are complete wheeled bottoms sharing the compact vacuum air system but
replacing the roller cassette with a powered telescope. Their raised bin targets
**0.30 L usable**. The caster moves to the rear right to leave a continuous
central duct corridor. Neither attachment requires dragging the 180 mm body
under the sofa.

The proposed telescope uses six **245 mm long rectangular stages**. Outer size
starts at 48 × 36 mm and decreases by 3 mm in both dimensions per stage, ending
at 33 × 21 mm. Nominal wall thickness is 1 mm. With at least 45 mm overlap,
five moving stages provide **1000 mm travel** and a 1245 mm extended guide.
Printed collars prevent pull-apart; replaceable low-friction strips and wipers
provide guidance and sealing. All individual printed stages fit the printer.

This is a proposed mechanism, not a catalog telescope. The nominal 0.5 mm
sliding clearance per side must accommodate printed tolerances, wear strips and
seals. A guided 6 × 0.3 mm spring-steel feed strip drives the end stage; its guide
must remain continuous through the overlaps, with unsupported gaps no longer
than 20 mm. The strip stores on a coil in the front-left feed bay. A Pololu 4845,
compact right-angle transmission, paired pinch rollers, slip clutch and feed
encoder provide an initial 12 N force limit at 50 mm/s. The coil and transmission
are installed allowances; their detailed guides and gear arrangement remain a
mechanical design gate. This route avoids assuming that a flexible vacuum hose
will push itself a metre beneath a sofa.

The whole telescope, rear air turn and head lift 12 mm for transit using a
PQ12 linkage. The rear flex seal reserves 20 mm height in working position and
8 mm when raised. Driving is inhibited until independent stow and raised
switches agree. During a floor cleaning stroke, the body stops; the head and
intermediate wear skids support the tube on the floor. Slip, excess motor
current or lack of feed-encoder motion causes a stop and controlled retraction.
The local controller must not continue pushing after the endpoint stops moving.

For the sofa bottom, the passive nozzle is **200 × 60 × 38 mm**, with a soft
leading lip, smooth skids and replaceable comb/bristle strips. Its working tube
envelope is 40 mm high, leaving nominal 10 mm clearance beneath the sofa. The
head stows in front of the body, extending the transit depth to 335 mm. With an
80 mm body stand-off, the outer edge reaches about **980 mm under the sofa**,
exceeding the 914 mm target. A stroke takes 20 seconds each way. Cover the sofa
width in overlapping lanes, mapping legs before advancing the head.

The telescope's smallest nominal air area is 589 mm². A Darcy/minor-loss
screen at 3.6 L/s estimates about **155 Pa added loss** for the extended stages.
This calculation excludes head/filter resistance, seal leakage, feed-channel
intrusion and local manufacturing defects. It does not establish the blower's
installed operating point or cleaning effectiveness at the far end.

The dusting version uses a **120 × 50 × 32 mm compliant brush/suction head**,
with a tip-range sensor and contact-force sensing. Passive retention keeps a
released tip attached. Initial contact target is 0.2 N, retreat threshold 0.5 N;
these are control design limits to be qualified, not certified safe forces.
Vacuum capture is preferred to blowing hair and fine dust into occupied rooms.
The alternative blower-sweeping mode discussed earlier is therefore not the
baseline hardware configuration.

The prior horizontal shelf-access calculation put the fully extended head about
1.05 m ahead of the body, or 466 mm beyond the current octo's front guards.
It remains a reference calculation. For the new ceiling-fan task, the owner
requests about 610 mm tool reach and the head must access blades around 2134 mm
high. A 610 mm reach measured from the body front would extend only 25 mm beyond
that octo's guards, before clearance or upward articulation. This is another
reason to reconsider lift and duster geometry together. The old shared telescope
and tip-sensor allowance do not include a new upward articulation mechanism.
See [the footprint and reach review](LIFT_LAYOUT_REVIEW.md).

**Floor support cannot be assumed while dusting in the air.** Tube deflection,
joint play, the force-sensor flexure, rotor airflow on the shelf and controller
reaction to tip contact all remain open. A simple weakest-section PETG beam
screen suggests millimetres to centimetres of sag at full reach, so the shelf
position controller must not treat the head as rigidly fixed to the core.
There is no indoor contact-flight approval in this revision.

## 9. Lift top and stair route

**Footprint under review:** the following is the previous mass/thrust comparison,
not a selected production layout. [Why it became this large](LIFT_LAYOUT_REVIEW.md)
shows the rotor spacing, added mass and provisional margin assumptions.

The comparison uses a documented **Hobbywing RTF-3115 900KV motor with HQProp
10×4.5×3 propeller**, with 125 g catalog motor mass and a 4–6S voltage range.
The source provides a 24 V thrust/input-power curve. Its largest point,
4648 g at 1477 W, has a **29-second limit**; it is not continuous thrust.
[Manufacturer motor/propeller data](https://www.hobbywing.com/en/uploads/file/20251117/2a4a3f326d2bdede135f3e582b73eef3.pdf).

The model compares four, six and eight non-coaxial rotors. It places all disks
outside the body so they do not have to blow through electronics or water tanks.
Per rotor it includes the motor, purchased propeller, matched 65 A-class ESC
channel, local mounting/capacitance and an installed 90 g guard allowance.
Matched channels can be grouped into two four-channel boards for the octo;
the power and thermal routing must follow the selected manufacturer's board.
Grouping is not permission to add another unbudgeted ESC set.

The 644 mm width is 360 mm column spacing plus a 284 mm guard. The 1444 mm
length is 1160 mm outer-row spacing plus the same guard. Eight was a thrust-margin
choice: six already passes the nominal 2:1 screen. Neither rotor count nor this
long arrangement has been established as necessary.

For the eight-rotor geometry, x positions relative to body centre are ±180 mm;
y positions are ±280 and ±580 mm. Alternate CW/CCW directions symmetrically.
Two 1200 mm carbon tubes, 20 mm OD/18 mm ID, carry the longitudinal loads.
340 mm crossbeams at y=-15 and y=290 clear the core and end at the inner faces
of the longitudinal tubes, joined by metal clamps. Beam centre height is
89 mm; metal motor plates place the motor body above the beam and the propeller
plane near z=149. Short risers link the top seats to the beams. Purchased split
clamps, drilled metal plates and diagonal braces carry primary loads.

A first beam screen at roughly 20 N thrust per rotor gives about 11 N·m at a
front support, around 41 MPa nominal tube bending stress and a few millimetres
of outer-rotor displacement using an assumed 70 GPa longitudinal modulus.
That is not a carbon-laminate allowable or a clamp fatigue calculation. Supplier
tube properties, clamp crush resistance, joint slip, torsion and vibration must
be checked before releasing this structure.

Guards are 284 mm outside diameter, with upper and lower planes at z=180 and
z=118. Four printed quadrants form each ring; **a 284 mm ring is not a single
275 mm print**. Spaced mesh/ribs cover both sides. The retained-thrust assumption
is 75%, varied from 65–85% in the viewer. Mesh loss, blade deflection and guarded
thrust have not been measured. Guards reduce access but do not prove containment
or that the machine is safe around a dog.

The flight controller candidate is a **Holybro Pixhawk 6C Mini** with its own
regulated supply, independent IMU, current/voltage feedback and logging. The core
front stereo camera is supplemented by rearward and downward stereo viewpoints,
plus independent downward and sector range sensing. The underside camera is
outboard of the body and below the carbon beam. Self-obstructed measurements
must be rejected. In particular, the guards overlap the RPLIDAR scan height;
flight cannot rely on an unobstructed 360° scan from that sensor.

This elongated layout requires a **geometry-specific thrust/control allocator**.
A stock quad or octo-X motor map does not represent its lever arms. The source
coordinates are available in `system_design.json`; forward in a flight frame
is minus this document's y. Motor directions, axes, actuator bounds, CG offsets
and controller sign conventions require independent verification. Eight motors
do not automatically imply a validated motor-out capability.

The sizing screen applies a 21/24 voltage ratio squared to peak thrust, a 75%
guard factor and a 2:1 thrust/weight target. Estimated hover input comes from
interpolating the source curve at the equivalent unguarded thrust, then adding
10% installation/electrical overhead and flight electronics. Same-thrust power
at lower voltage is an approximation; loss and thermal changes are unresolved.

For the nominal loaded vacuum, the quad gives approximately 1.52:1, the hex
about 2.09:1 and the octo about 2.59:1. The octo's high-mass vacuum case falls
below 2:1, and extension cases have less margin. A 2:1 design mass
ceiling under these assumptions is **10.68 kg**. This is a screening ceiling,
not a certified maximum takeoff mass.

The illustrative energy allocation is 45 s transfer at 1.2 times estimated hover
power, plus 30 s landing reserve, then 20% energy margin. The nominal octo/vacuum
case requires about **69 Wh held available at departure**. The example 6S pack
contains only 92 Wh at the assumed usable-energy fraction, leaving about 24 Wh
above this reservation. A prolonged airborne dusting task adds tool consumption
and approximately 2.6 kW total continuous load. Efficient floor cleaning and
flight have very different energy requirements.

The stair corridor is not simply the 914 mm tread width. Subtracting both reported
overhangs gives a conservative **774.7 mm** band. The 644 × 1444 mm octo frame,
at 2° yaw and with 25 mm lateral allowance per side, occupies approximately
744 mm, leaving only 31 mm additional width. At larger yaw the margin vanishes.

There is also a vertical constraint: a level frame straddles several treads.
For the reported 190.5/279.4 mm stair slope, the simple 100 mm clearance screen
puts the body origin about **474 mm above the local stair plane** and the
highest trailing part about **1.15 m above the lowest underlying tread**.
These figures exclude pitch/roll error and discrete stair/railing geometry.
Full 3D swept-volume planning is required; a top-view width fit is insufficient.

Do not land the complete body on individual 279.4 mm treads: a 275 mm body has
only 4.4 mm total nominal depth margin, before pose error or overhanging rotors.
The current flight objective is **floor-to-floor transfer between clear
landings**. Cleaning stair treads while hovering would use the compliant tool,
but contact, suction downwash and collision control remain unqualified; this
revision does not promise automated cleaning of each tread.

## 10. Electrical distribution and battery decision

```text
Removable cartridge: cells, monitor/ID, temperature and fuse
  ├─ service disconnect + fault protection + current measurement
  ├─ protected floor branch (240 W allocation)
  │    ├─ 5 V / 40 W -> Pi, core sensing and control
  │    ├─ 12 V / 96 W -> wheel controller + low-voltage tool motors
  │    │     └─ reverse-energy management / brake resistor
  │    └─ 24 V / 80 W -> vacuum blower
  ├─ separately protected raw-pack lift branch
  │    ├─ fore/aft motor distribution -> ESC channels
  │    └─ independent flight-controller supply
  └─ separate charge interface <-> independently supervised station rack bay

Station auxiliary 24 V -> protected converter / source OR -> core 5 V logic
  (keeps logic live during exchange; cannot energize tools or empty pack socket)
```

The 5 V reference is **Pololu D42V110F5, #5671**; #5672 is the 5.3 V version and
is not interchangeable just because its package matches. The 12 V reference is
**D42V110F12, #5677**. Their achievable current depends on input voltage,
temperature and cooling; family headline ratings at 42 V are not a guarantee at
the robot's supply. Design allocations remain 40 W and 96 W respectively.
[Regulator family table](https://www.pololu.com/category/370/d42v110fx-step-down-voltage-regulators).

Use a short, low-resistance Pi power path. A nominal 5 V regulator is not by
itself a complete USB-C 5 A power-delivery solution. Cable drop, power entry,
backfeed protection and available USB peripheral power must be included in the
electrical detail design before connecting the cameras.

The 24 V reference is **Cincon CHB100W-24S24**, 9–36 V input, with matched
HBT127/PH01 thermal hardware and a fan. This establishes space for regulated
24 V throughout a 6S discharge, not just when the pack is near full. A direct
pack connection is not equivalent. With a future 8S system, a step-down design
could replace this converter, but its weight, heat and dropout must be updated
in the whole model. [Converter data](https://www.cincon.com/productdownload/Datasheet-CHB100W.pdf).

The RoboClaw can regenerate. A normal buck regulator is not assumed to absorb
that energy. Reserve reverse blocking, rail voltage sensing, a hardware braking
clamp and bulk capacitance. An initial **15 V clamp, 10 Ω/25 W resistor and
2200 µF/25 V** capacitor allocation illustrates the required hardware; comparator,
FET, tolerances, pulse energy and thermal mounting are not a released circuit.
At 15 V the resistor dissipates 22.5 W. Stops, pushing and descending transitions
must not charge the regulated bus beyond component ratings.
[RoboClaw operating requirements](https://resources.basicmicro.com/manual/roboclaw/operational-requirements/).

The raw flight branch bypasses the floor regulators. Its high-current contacts,
conductors, fuse, shunt, disconnect and protection power stage must be designed
together for the flight current envelope. The BQ76952 reference is a **cell
monitor/protection controller**, not a purchasable 320 A BMS. Likewise BQ25756 is
a **charger controller IC**, not a finished automatic charger. Their current
external-FET, thermal and PCB assumptions are open and may increase the mass
budget. These are among the strongest reasons not to choose a battery now.
[Cell monitor](https://www.ti.com/product/BQ76952),
[charger controller](https://www.ti.com/product/BQ25756).

The model keeps both owner-proposed packs:

| Comparison pack | Nominal / full voltage | Nominal energy | Listed mass | Bare-body fit |
|---|---:|---:|---:|---|
| Zeee 6S, 5200 mAh | 22.2 / 25.2 V | 115.4 Wh | 753 g | 155.5 × 48.5 × 50 mm fits the cell pocket numerically; installed fit unverified |
| Ovonic 8S, 5200 mAh | 29.6 / 33.6 V | 153.9 Wh | about 921 g | Rotate 156 × 47 × 61 mm to 156 × 61 × 47 mm; only 1 mm total pocket width allowance |

The input-axis 8S height fails the cell pocket, but rotating it changes that answer;
the code explicitly checks permutations. Restraints, leads, tolerances and
delivered dimensions still matter. **8S exceeds the 4–6S lift motor reference**,
so the model refuses to extrapolate flight performance to that voltage.
Changing the pack means choosing a matching propulsion system and revisiting
every voltage-limited branch. More series cells alone do not solve flight mass
or energy.

The owned charger label supports up to six lithium cells, but its exact model,
input supply and charging power remain unidentified. It is not assigned as the
automatic dock charger. The current 3S battery remains useful for appropriately
regulated ground development; it does not define the production power system.

## 11. Automatic station hardware and exchange paths

The existing station comparison reserves a **1200 × 1800 × 1500 mm cabinet**,
plus 1600 mm approach. Its intact-top storage drives much of that size; revise
this reservation with the compact lift study rather than freezing it as a
household footprint requirement.
The [station plan](../design/system/output/station_top.svg) and
[station CAD](../design/system/output/station.FCStd) show machinery reservations.
The off-robot CSV includes frame stock, rails, actuators, controls, charging,
washing, evacuation, battery rack/exchange hardware, containers, harnesses and
fasteners. Its 58.9 kg empty machinery
estimate is separate from spare bottoms, battery contents and carried mass.

Use cut aluminum extrusion, purchased linear rails, **TR8×2 screws for gravity
axes**, NEMA17-class motors with a ≥0.45 N·m target and approximately 2:1
reduction on lifts. A 20 kg vertical design load needs about 0.21 N·m screw
torque at an assumed 30% screw efficiency. This is a sizing calculation; actual
motor torque at operating speed must be verified. Spring-engaged mechanical
catches and retained forks support the core/top on power loss. Lead-screw
friction alone is not the retention mechanism.

The station has five bottom positions: four local working-bottom slots plus a
receiving vacancy for an arriving robot. This avoids assuming that a robot can
bring a vacuum to another floor whose only vacuum slot is already occupied.
The scheduler tracks module identity, ownership and free slots before transfer.
Duplicated tool inventory is station stock, not weight carried by the robot.

A full two-floor inventory would therefore be **one core, two caps, one travelling
lift top and two copies of each of the four bottoms**. One bottom is on the robot;
the others occupy station slots. This implies 16 drive motors/wheels/hubs and
eight wheel controllers across the system, not on one robot. There are six
stationed/carried vacuum-air assemblies across the vacuum, sofa and duster
bottoms, two mop tanks/pumps, and two complete service stations. Development can
build one instance of each design first; these deployment quantities are not a
new shopping list.

The core is captured at reinforced side pickup features and lifted **300 mm**.
Stored bottoms rest at z=80 and reach z=212; a picker uses a transfer base at
z=220 and remains below z=352. The raised core's lowest battery bay is z=376,
leaving 24 mm nominal separation. The core-lift tower is a permanent obstacle:
the picker routes around it through a rear waypoint before approaching the
central exchange position. A straight line through the lift tower is not a
valid storage-to-dock path. Final gantry crossmembers and cable chains must be
checked against this route.

The top handler raises a detached top by about **480 mm**, then moves it
rearward to an intact parking envelope of [278,308,600] to [922,1752,780].
The core remains down while the top is removed; it is raised only after the
overhead path clears. The cap occupies a separate shelf. Normal cleaning leaves
the lift parked, avoiding its mass, span and rotor hazards during floor work.

Battery handling uses the same XYZ picker after it parks the old bottom. A
100 mm downward withdrawal clears the supported core; the rack occupies
[880,250,375] to [1160,890,535]. Four bays hold two resident spare cartridges,
a receiving vacancy and recovery space. The complete fleet has five packs,
including the one carried. See [battery exchange](BATTERY_EXCHANGE.md) for
mechanics, auxiliary power, per-pack charge isolation and readiness policy.

The automatic operating sequence is:

1. Confirm station vacancy and health; approach using map, local ranging and a
   visual docking target. Park on a protected, calibrated weighing platform.
2. Reserve a compatible READY battery and receiving vacancy if exchanging packs.
   Establish and verify auxiliary logic power. Disable wheels/tools, isolate
   the main bus, confirm near-zero pack current, capture the core and engage
   mechanical support. Drain/contain any fluid operation before release.
3. If necessary, remove the cap/lift top and park it using the overhead handler.
4. Release the bottom locks; raise the core; pick up and store the old bottom.
5. If exchanging batteries, capture and withdraw the old cartridge, store it,
   insert/latch/identify the reserved replacement, then precharge and verify
   protected pack power. The station powers logic throughout.
6. Bring the required bottom through the clear transfer route, seat the core,
   lock and verify alignment, identity, electrical isolation and all latch states.
7. Empty the vacuum bin or fill/wash the mop as appropriate. Verify level, leak
   and pressure states. Returned cartridges cool and charge independently in
   the rack under their own validated profiles.
8. Attach the requested top. For flight, weigh the complete assembly, check
   energy/current/temperature margins and clear the full launch envelope.
9. Verify battery-to-logic power handover and remove auxiliary station power.
   Remove handling fixtures only after the robot is supported and ready.
   Any failed step remains supported, stops energy transfer and reports a fault.

Bulk containers are 5 L clean water, 5 L dirty water and 5 L debris. Ten 120 mL
pad washes per 1000 ft² pass add 1.2 L to the water requirement. Including dosing,
the starting recipe consumes approximately **1.48 L for wood or 1.76 L for tile**
per floor. That is about three floor passes per 5 L clean tank, not a promise of
weeks without servicing. Hair load will determine the waste-bin interval.

The station power allocation is 280 W DC, with up to 180 W reserved for charging.
This is 180 W total shared among four charge channels, not per bay. Up to 60 W
of auxiliary robot logic supply is separately allocated during exchange.
Motion, drying and charging are sequenced so the supply is not oversubscribed.
An enclosed off-the-shelf vacuum appliance gets a separate
800 W mains allowance; retain its original electrical enclosure and protection.
The bulk wash circuit uses a screened drain, level switches, backflow break and
leak detection. No household plumbing connection is required.

## 12. Sensors, autonomy and recovery

The Pi performs mapping, perception, coverage and mission planning. A core MCU
owns power state, module identity and interlocks. Each bottom MCU owns local
wheel/tool commands, watchdogs, bumps, cliffs, wheel drop, current and fluid
interlocks. The flight controller owns attitude and thrust allocation. Local
hardware must be able to stop floor tools without waiting for a Linux process,
wireless link or cloud request.

Floor navigation combines encoder odometry, IMU, LiDAR and stereo, with local
cliff/bump sensing independent of the room map. Pets, cables, toys, wet areas
and suspected waste become local no-go regions or waiting conditions. A dog
does not have to learn a predictable route for the robot to stop. A failed or
blocked cleaning lane is recorded and retried later, rather than repeatedly
driving into the obstruction.

Optional MCP/LLM integration can submit structured jobs such as “vacuum kitchen”
or propose room priorities. A deterministic validator checks map regions,
tool capability, battery reserve, dock availability and safety constraints.
It cannot issue raw motor commands, override flight interlocks, accept arbitrary
sensor text as control instructions or bypass cliff/pet exclusions. Routine
cleaning must remain possible without internet access.

Autonomous flight is the largest unresolved control requirement. Before takeoff,
both the transit corridor and a recovery landing must be available. A pet entering
the path requires a validated wait/retreat/landing response; “cut all motors”
is not an appropriate generic response while airborne. No hardware list alone
establishes that this works with freely moving dogs. The design retains that
requirement and does not treat the dogs as guaranteed excluded from the stairs.

## 13. Fabrication, verification and remaining work

This revision supplies component envelopes, module mechanisms, shared interface
dimensions, an editable mass/power ledger, four floor layouts, three lift
comparisons, two extended layouts and a station layout. Generated FreeCAD/STEP
files distinguish solid component/stock references from wireframe reservations.
There are deliberately **no new fabrication STLs** for an unqualified latch,
flight structure or telescope.

TAZ 6 parts should be ribbed shells and small replaceable carriers, not solid
275 mm slabs. Main panels are 270 mm square to reserve bed margin. Tube stages
are 245 mm long; guards split into quadrants. Aluminum strips, carbon tubes,
standard screws/bearings and stock springs supply the parts that benefit from
material properties beyond printed plastic. The stock CSV gives starting cut
lengths and quantities; holes, tolerances and print orientation remain part of
the detail release. Carbon cutting requires appropriate stock-handling practice;
pre-cut tubing is an alternative to machining it in the home workshop.

Automated model checks cover assembly accounting, non-overlap of functional
ground allocations and core rails, nested reference containment, mass/CG bounds,
power conversion accounting, extension travel, voltage compatibility and
non-extrapolating propulsion interpolation. They also retain adverse results:
negative worst-case normal support margin, difficult wet caster crossings and
unqualified flight. CAD shape validity is separate from mechanical strength.

The next design work is now specific and can be prioritized without purchasing
more experimental motors:

| Gate | Evidence needed to close it |
|---|---|
| Tool interfaces | Exact TriCut stationary/drive-end drawing, matched plain-roller ends, safe operating speed and the delivered filter/seal dimensions |
| Frame and locks | Detailed plates, seats, fastening access, cam/pawl tolerances, load-sharing/creep/fatigue checks and service paths |
| Ground mechanics | Final wheel-pod mounting stack, actual CG/wheel loading, caster retaining stem, head following and wet transition behavior |
| Telescope | Detailed feed spool/right-angle drive, continuous strip guides, collars/seals, retrieval force and cantilever stiffness |
| Power | Schematics and thermal layout for cartridge contacts/protection, pack cell monitoring, regenerative clamp, Pi/dock power handover and independent rack charging |
| Lift | Installed guarded thrust, low-voltage temperature limits, structural dynamics, current delivery and 3D route/control qualification |
| Stations | Detailed gantry routes/cable chains, lock actuation, weighing calibration, connector-cycle behavior and fluid fault recovery |

**Owner update retained, 2026-09-13:**

- The 644 × 1444 mm lift is considered excessive; its footprint has not been
  accepted. Review compact rotor arrangements and mass before fixing lift and
  station structure.
- Highest dusting targets are ceiling fans about 7 ft above floor and 1 ft below
  ceiling. Desired duster reach is about 2 ft. These supersede the previous shelf
  assumption; the sofa still needs its longer reach.

The next lift/duster deliverable is a compact comparison including usable tip
reach, vertical access, total mass, power, stair/fan clearance and storage.
Ground-interface detail can proceed independently. Confirm a physical reach datum
and fan blade geometry when a concrete approach is available for review.
