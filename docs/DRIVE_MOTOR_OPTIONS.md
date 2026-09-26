# Ground-drive motor alternatives

**2026-09-12 update:** use the
[ground component recommendation](GROUND_COMPONENT_RECOMMENDATION.md) for the
current proposal: Pololu #4846 with wider 72 mm wheels. The BDUAV experiment is
optional. The older comparisons and sale references below are historical, not
the current purchase list.

2026-09-05. Recommendation for discussion; no replacement motors selected or
ordered. The owner wants a faster long-term drivetrain. The two owned 12 V,
18 RPM GA25-371 encoder motors remain available for a slow prototype or reserve.
Their particular output speed is the limitation; the GA25 family name alone
does not establish speed, torque, mounting compatibility or encoder details.

## Recommendation and speed target

The compact [ground placement](GROUND_PLACEMENT.md) now uses the owned 60 mm
wheels as its reference, so **two Pololu 25D HP 12 V 75:1 (#4846)** encoder motors
are the current candidate. **99:1 (#4847)** remains the candidate for the larger
90 mm wheels. Both fit the same published body envelope. Keep interchangeable motor plates.

The proposed cleaning speed remains **0.15–0.25 m/s**, subject to pickup and
obstacle-stopping performance; it is not a confirmed owner requirement. Encoder
feedback sets cruising speed below the motor's unloaded maximum. From
`wheel RPM = speed_m_s * 60 / (pi * diameter_m)`:

| Wheel | RPM needed at 0.15 m/s | RPM needed at 0.25 m/s | Speed at the owned motor's listed 18 RPM |
|---|---:|---:|---:|
| 90 mm | 31.8 | 53.1 | 0.0848 m/s |
| 60 mm | 47.7 | 79.6 | 0.0565 m/s |

The alternatives below provide speed headroom. Final torque adequacy depends on
loaded assembly mass, wheel loading, turning friction and cleaning-head drag;
none is established yet. Do not infer a supported robot mass from stall torque.

## Documented alternatives

USD list prices checked 2026-09-05, before discounts, tax, delivery and accessories.
All new options include encoders. Wheel speeds are calculated at the listed
**12 V no-load RPM**, not measured travel speeds or intended cleaning commands.

| Candidate | No-load RPM | Speed with 90 / 60 mm wheels | Each / pair | Reference mass each | Role |
|---|---:|---:|---:|---:|---|
| [Pololu #4847: 25D HP, 99:1](https://www.pololu.com/product/4847) | 100 | 0.471 / 0.314 m/s | $56.95 / $113.90 | 104 g | Leading compact candidate for 90 mm wheels |
| [Pololu #4846: 25D HP, 75:1](https://www.pololu.com/product/4846) | 130 | 0.613 / 0.408 m/s | $56.95 / $113.90 | 104 g | Same size; more speed margin with 60 mm wheels |
| [Pololu #4755: 37D, 100:1, helical first stage](https://www.pololu.com/product/4755) | 100 | 0.471 / 0.314 m/s | $60.95 / $121.90 | 210 g | Larger gearbox alternative if load/drag warrants it |
| [DFRobot FIT0277](https://www.dfrobot.com/product-777.html) | 143 ±10% | 0.674 / 0.449 m/s | $39.00 / $78.00 | 270 g | Lower list price, but larger and documentation conflicts remain |

Pololu currently advertises 20% off these motor categories with `LD26C51` (limit
four of each item), making a 25D pair approximately **$91.12** or the 37D pair
**$97.52** before other costs. This is a temporary offer, not the design budget.
The product pages allow backorders; an immediate ship date was not established.
[Manufacturer sale terms](https://www.pololu.com/laborday2026)

## Torque and mechanical fit

The Pololu 25D family has a recommended continuous gearbox-load ceiling of
**4 kgf·cm (0.392 N·m)**. The 37D ceiling is **10 kgf·cm (0.981 N·m)**. These are
mechanical limits, not guarantees that the motor can thermally sustain that
load in our enclosed bottom. Both families also recommend generally staying at
or below 25% of stall current for sustained brushed-motor operation. Published
stall torque must not be used as the working rating.
[25D load guidance](https://www.pololu.com/product/4847),
[37D load guidance](https://www.pololu.com/product/4755)

| Candidate | Body envelope, excluding output shaft | Output shaft | Published current at 12 V: no-load / stall extrapolation |
|---|---|---|---|
| #4847 and #4846 | 25 mm diameter × 69 mm long | 4 mm D, 12.5 mm extension | 0.30 / 5.0 A each |
| #4755 | 37 mm diameter × 72.5 mm long | 6 mm D, 16 mm extension | 0.20 / 5.5 A each |

Allow additional room for hubs, cables and service access. Reference dimensions
and masses: [#4847 specs](https://www.pololu.com/product/4847/specs),
[#4846 specs](https://www.pololu.com/product/4846/specs),
[#4755 specs](https://www.pololu.com/product/4755/specs).
The 25D no-load RPM is typical with a stated ±20% tolerance; speed control and
loaded checks are still needed. These are not confirmed drop-in replacements for
the owned GA25 motors.

The DFRobot store lists 123 × 36 × 36 mm, 3.6 A stall current and 5.5 kgf·cm rated
torque. Its [wiki](https://wiki.dfrobot.com/fit0277) instead lists 146 RPM,
51:1 gearing and 10 kgf·cm, while the store lists 143 RPM and 56:1. The store's
13 PPR/663 output PPR also does not match 56:1 gearing. Resolve the actual revision,
shaft drawing, torque duty and encoder specification with DFRobot before selecting
it. The speed table uses the current store figure only. It is not the preferred
purchase despite the lower list price.

For a 25D pair, the straightforward bought mounting parts are one
[#2676 bracket pair](https://www.pololu.com/product/2676) ($10.95) and one
[#1997 4 mm hub pair with M3 holes](https://www.pololu.com/product/1997) ($10.95).
With motors, that is **$135.80 at list prices for this mechanical subset**.
Bracket-to-chassis and wheel-to-hub screws still need appropriate lengths.
Confirm the owned 90 mm wheel variant accepts these hubs; its standard 3 mm
center bore does not fit directly onto a 4 mm motor shaft. The unidentified
60 × 8 mm wheels now have an owner-confirmed 3 mm center hole and no hub
protrusion. They also require a qualified bolt-on hub/adapter for the 4 mm shaft;
the reported BDUAV face-hole match does not establish compatibility with the
Pololu hub. Keep the shaft end clear of the smaller wheel bore and account for
adapter offset, screw engagement and runout. Printed replaceable chassis plates
and axle hair shields should avoid machining for this installation.

## Owned BDUAV 2204-260KV as a wheel-drive alternative

2026-09-06. **Direct M2 wheel attachment confirmed; drive performance unqualified.**
The owner confirms that the matching motor face rotates relative to the opposite
side and that the 60 × 8 mm wheels bolt directly to it using M2 fasteners. A
separate wheel hub is therefore unnecessary for this BDUAV option. The current
25D gearmotor option still needs its own 4 mm-shaft hub/adapter.

The owner also confirms **BDUAV 2204-260KV is printed on the motor itself**. The
attached specification image came from the purchase page, but is headed
**ML2206B Motor** and lists **160 RPM/V**. This is a confirmed source conflict;
the image is retained as disputed evidence and is not applied to the owned unit.
A shared appearance or matching mounting holes does not resolve electrical ratings.

### Attached purchase-page image: transcription, not adopted specifications

| Image field | As supplied |
|---|---|
| Model heading | ML2206B Motor |
| Motor KV | 160 RPM/V |
| Motor resistance (Rm) | 5.6 ohms |
| No-load current | 0.06 A at 7.4 V |
| Maximum continuous current | 1.3 A |
| Maximum power | 15 W |
| Motor diameter / body length | 28 mm / 15 mm |
| Approximate weight | 23 g |
| Bolt-hole spacing | 12 mm |
| Bolt thread notation | M2X4 |
| Stator arms / pole count | 12N / 14P |

Source: owner-attached image, with purchase-page provenance confirmed by the owner;
page URL and original publisher were not supplied. This full transcription is
also stored under `unverified_attached_specification` in the inventory. None of
these values is promoted to the owned motor's mass, electrical limits or geometry.
The original 260KV report now has confirmation from the physical label.

Even if corrected evidence later establishes some matching values, the image
does not specify phase versus line-to-line resistance, phase versus bus current,
RMS/peak conventions, cooling conditions or a torque-speed curve. The 7.4 V entry
is a no-load test condition, not a supply range. The 15 W entry does not identify
input versus shaft power or establish continuous power at 48–80 RPM; dividing it
by wheel angular speed would not establish low-speed torque. Current and KV
conventions also matter when converting electrical constants to torque.
[FOC parameter conventions](https://docs.simplefoc.com/voltage_torque_control)

The sheet's 23 g figure cannot support a claimed weight saving for the actual
BDUAV pair. Its measured mass remains unknown, and an installed comparison must
include drivers, feedback, mounting and wiring. M2X4 is transcribed notation, not
a selection of 4 mm-long bolts through an 8 mm-wide wheel. Actual material stack,
engagement and clearance determine screw length; the owner has confirmed M2 thread
compatibility independently of this image.

### Speed and torque are separate requirements

At 60 mm wheel diameter, the proposed 0.15–0.25 m/s cleaning range requires
**47.7–79.6 wheel RPM**. The confirmed 260KV marking is a speed constant in RPM/V, not an
operating-speed command or a continuous torque rating. A gimbal-type motor can
be controlled at low speed; smooth motion does not establish enough traction.
[Motor-class reference](https://docs.simplefoc.com/bldc_motors),
[KV parameter units](https://docs.simplefoc.com/bldcmotor)

Use `wheel torque = tangential force × 0.030 m` for these wheels. For an
illustrative **5 N total straight-line tractive demand**, equally shared by two
wheels, each motor needs `5 / 2 × 0.030 = 0.075 N·m` at the wheel. This is a
sensitivity example, **not measured robot drag or a claimed BDUAV rating**.
Actual requirements include rolling resistance, brush/skid drag, turning,
acceleration and climbing the docking ramp. Robot mass and sustained available
motor torque remain unknown. Gearing can trade speed for torque, but adds
transmission size, losses and another mechanism to qualify.

### Control and mechanical cost of reuse

For a traction implementation, propose a matched three-phase driver per motor,
rotor position feedback, local speed control and current/temperature limits.
Use the [wheel-controller shopping criteria](DRIVE_CONTROLLER_REQUIREMENTS.md)
when comparing ESCs, integrated controllers and separate driver/MCU combinations.
SimpleFOC is one possible open-source implementation: its closed-loop speed
control uses a position sensor to react to changing load.
[Control modes](https://docs.simplefoc.com/motion_control)

The owned PCA9685/Waveshare servo boards do not provide the motor power stage.
The proposed Cytron brushed driver is not a substitute for a three-phase drive.
The aircraft ESC has not been qualified for this bidirectional low-speed task;
its 80 A label says nothing about the gimbal motor's safe winding current.
The owner subsequently requested a [printed rolling drive rig](../design/experiments/drive_rig/README.md)
for the BDUAV motors. That experiment is now the next drive-validation step;
mechanical fit files and a full hardware proposal exist, with powered commissioning
and firmware still pending.

The rotating attachment face and M2 fit are now confirmed. Final mounting still
needs centering, screw engagement and internal clearance checked, along with a
bearing load assessment. A camera motor's bearings are not automatically qualified
for cantilevered wheels carrying the cleaning robot. Direct mounting makes this
option mechanically simpler than previously established; load and thermal evidence
still determine whether it is a useful traction drive.

**Current decision:** retain the 75:1 encoder gearmotor as the full-robot layout
reference, subject to its own load and hub qualification. Use the BDUAV pair in
the requested rolling experiment to establish drive performance, control needs,
bearing behavior and heating under measured load before final selection.
This is an evidence-based selection preference, not a claim that a gimbal motor
cannot drive wheels. Mass and cost comparisons must include the complete drive;
ownership alone does not make it the lighter or cheaper installed option.

The rotating-face and specification-source questions are resolved in the inventory.
During the rolling-rig design the owner also measured the motor at 28 × 13 mm,
with stationary M2 holes on an 8 mm square, approximately 4 mm depth to an internal
obstruction, and a rotating 4 mm central bore. These are independent measurements,
not adoption of the conflicting purchase-page sheet. Correct variant-specific
ratings or controlled measurements are still needed for operating limits.

## Power, control and next design step

The 12 V Pololu options are candidates for the owned 3S battery through a brushed
H-bridge. Speed/current figures above are at 12 V; the pack varies from 12.6 V
fully charged downward. Allow for voltage sag, driver losses and reduced speed
under load, with appropriate duty limits, battery protection and braking-energy
handling. Do not promise the table's top speed throughout a discharge.
Keep 3S as the current ground-development candidate; these motor alternatives
do not require a 4S purchase. The [ground power comparison](GROUND_MODULE_DESIGN.md#power-and-data)
records the implications of a later 4S supply and regulated 12 V loads.

The previously proposed Cytron MDD10A plus ESP32 remains a controller/driver
candidate, with motor-current protection still to design. Its driver current
capacity is not a motor or gearbox protection setting. These Pololu encoders
require **3.5–20 V** power and produce outputs up to their supply voltage:
use a regulated 5 V encoder supply with **four channels of 5 V-to-3.3 V signal
translation** for an ESP32. Do not power these encoders at 3.3 V or connect their
5 V outputs directly to the MCU. [25D encoder interface](https://www.pololu.com/product/4846)

The consolidated drivetrain BOM still needs hubs, brackets, fasteners, dual
H-bridge, local MCU, encoder translation, power/protection and wiring. Count one
motor pair per installed bottom, not every alternative. Keep the owned pair in
the prototype ledger until a replacement is chosen; none of the masses here is
an owned-part measurement.

Next, check the small motor-mount coupon for the requested rolling rig and record
the actual motors' unpowered lead-pair resistance. Complete the rig's feedback
control commissioning before loaded starts, turns and thermal trials. Cleaning
head drag and docking loads will still require later full-bottom testing.
Lift sizing remains deferred.
