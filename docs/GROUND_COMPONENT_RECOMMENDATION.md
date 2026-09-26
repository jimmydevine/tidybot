# Ground robot component recommendation

2026-09-12. Recommendation for the robot, with component choices driven by the
cleaning requirements. The owner has asked us to assume that owned components
requiring basic performance characterization will not be suitable. The BDUAV
drive rig is now an optional experiment, not a prerequisite for robot design.
The owner subsequently reported two selected motors and the dual controller on
the way. Wheel/hub purchases have not been reported. Fabrication remains pending
the placement and integration work in the [next vacuum-module pass](VACUUM_MODULE_NEXT_PASS.md).

The three-section architecture, automatic exchange/charging, vacuum-first
priority, 275 × 275 mm rigid footprint and 180 mm total height remain the design
requirements. Whole-assembly flight stays deferred until ground-module masses
are established. The separate long-reach head remains the solution for the
50 mm sofa clearance.

## Recommended drivetrain

Use two geared brushed motors with integrated encoders, a dual controller with
closed-loop speed control, and compliant purchased tires. This removes the
custom rotor magnet, shaft and commutation development from the main robot.
The drive assemblies should be removable cartridges in each wheeled bottom.

Prices below were checked on 2026-09-12 in USD, before shipping and tax. They are
component prices, not a complete robot or complete assembly order.

| Component | Qty | Recommendation and reason | Unit price |
|---|---:|---|---:|
| Drive motor | 2 | [Pololu #4846, 25D HP 12 V, 75:1, encoder](https://www.pololu.com/product/4846): compact documented gearmotor; 130 RPM nominal no-load speed | $56.95 |
| Wheel | 2 | [goBILDA Hogback 3626-0014-0072](https://www.gobilda.com/hogback-traction-wheel-72mm-diameter-50a-durometer/): 72 mm diameter, 50A silicone tread | $8.99 |
| Wheel hub | 2 | [goBILDA Sonic Hub 1309-0016-0004](https://www.gobilda.com/1309-series-sonic-hub-4mm-bore/): 4 mm clamping bore; nominal mating with the Hogback wheel verified in supplier CAD | $7.99 |
| Dual motor controller | 1 | [RoboClaw 2x7A, current V6B/V6F listing](https://www.pololu.com/product/3682): encoder feedback and velocity control, USB/serial commands | $79.95 |
| **Subtotal** | | Motors, wheels, hubs and controller only | **$227.81** |

Allow approximately $50–100 more for motor plates, caster, suspension hardware,
fasteners and guards at this stage; that allowance is an estimate. Battery,
regulators, protection, wiring, sensors, printed chassis and cleaning hardware
are additional. Stock varies; the Pololu listings allow backorders, so check
delivery before an order. RoboClaw is also listed by
[Basicmicro](https://www.basicmicro.com/motor-controller2).

The [drivetrain sourcing record](DRIVETRAIN_SOURCING.md) adds exact DigiKey,
Mouser and RobotShop cross-references, fulfillment qualifications and conditional
alternatives. It distinguishes manufacturer-shipped Marketplace listings from
distributor inventory; the preferred component choices below remain unchanged.
The wheel-to-hub CAD check now passes: order the two wheels with their two hubs.
Printed bracket integration and final fastening hardware remain unfinished.

The motor's published body is 25 × 69 mm, with a 4 mm D shaft extending 12.5 mm;
reference mass is 104 g. Its gearbox continuous-load recommendation is
4 kgf·cm, approximately 0.392 N·m. This, plus motor heating, governs sizing;
the advertised extrapolated stall torque is not usable continuous torque.
[Motor specifications](https://www.pololu.com/product/4846/specs) and
[load guidance](https://www.pololu.com/product/4846).

For a 72 mm wheel, our proposed 0.15–0.25 m/s cleaning speed needs approximately
40–66 wheel RPM. The nominal unloaded maximum is about 0.49 m/s; commanded
cleaning speed would be limited below that. These are calculated speeds, not
measured cleaning performance.

Use 3–5 kg only as an initial *sizing scenario*, not as the robot's established
mass. For illustration, at 5 kg, assuming rolling resistance coefficient 0.03,
4 N tool drag, 0.2 m/s² acceleration and a 5° station ramp, each 36 mm-radius
wheel needs about 0.19 N·m; a 1.5 multiplier gives about 0.29 N·m. Formula:
`torque = (m*g*Crr + tool_drag + m*a + m*g*sin(ramp)) * radius / 2`.
Actual mop drag, caster swivel resistance and thresholds may dominate this
estimate. Revisit sizing if the load exceeds this scenario; preserve alternate
motor plates. Brushed motors and gearboxes are service parts; this selection
does not establish unattended appliance lifetime.

RoboClaw handles both encoders and motor speed loops. Set motor-specific current
limits, acceleration limits and communication timeout behavior during integration.
Its 7.5 A/channel capability is not an operating-current target for these motors.
Use a separate appropriately rated Pi supply. Account for regenerative braking
in the power design: an ordinary buck converter must not be assumed to absorb
returned energy. The controller is a purchased firmware component; the robot's
CAD, application code and interfaces can still be published openly.
[Controller documentation](https://www.pololu.com/product/3682).

The two purchased B-G431B-ESC1 boards remain with the brushless experiment. They
are not the proposed controller for these two-wire brushed gearmotors.

## Tires, support and wet floors

The wheel manufacturer provides tread material, hardness, mass and CAD, but no
wet wood/tile traction coefficient. I recommend this wheel as a well-defined
candidate, not as a guaranteed wet-floor solution. Its nominal mass is 55 g.
The [manufacturer's STEP model](https://www.gobilda.com/content/step_files/3626-0014-0072.zip)
was inspected in FreeCAD; axial width is approximately 24 mm. The new tires are
therefore substantially wider than the owned 8 mm wheels. Width alone does not
prove better grip on a water/detergent film.

Design each drive cartridge with limited vertical compliance and sufficient
wheel loading. Keep the battery low and make the load distribution work with
both empty and full bins/tanks. Use an accessible, nonmarking soft-tread swivel
caster instead of making the owned metal ball caster the household baseline.
Select its exact part after support height, swept clearance and load are known.
Guard rotating hubs and make hair removal possible without dismantling the core.

For the mop bottom, put the wetted pad behind all normal ground-contact wheels.
Meter water into the pad and lift the pad for repositioning. Prefer forward
passes with dry-route turns; stop water delivery when stopped or reversing.
Lifting the pad does not dry an already wetted route, so plan wet-area crossings
explicitly and use restrained acceleration there. The center of mass and pad
force must still leave useful traction load on the drive wheels.

A brief final-system test on the actual floors remains necessary: dry and freshly
mopped straight travel, starts/stops and turns, with empty/full service loads.
Record slip, stopping distance, scuffing and hair accumulation using the intended
cleaner concentration. This checks application suitability; it does not require
rediscovering undocumented motor torque or constructing an expensive test stand.

## Vacuum and mop hardware

**2026-09-13 reassessment:** the [vacuum review](VACUUM_RECOMMENDATION_REVIEW.md)
prioritizes TriCut investigation and comparison with hair-shedding mechanisms;
the plain Roborock roller is a fallback. Keep the S7/S8 washable-filter candidate
and provisional BIQU WS7040 blower/driver kit. Micronel
below remains a premium comparison; its graph/table discrepancy is documented
in the [earlier selection record](VACUUM_COMPONENT_SELECTION.md).

Use a compact removable head that prevents hair accumulation, accessible end
supports, a sealed collection bin and a replaceable filter with a reproducible
supplier/model. Hair pickup and detangling requirements outrank simpler mechanics.
Design the edge brush to feed the main pickup path. Neither the large owned
filter nor the existing roller-end geometry should force the whole packaging
layout. Approximately 180–200 mm cleaning width is a proposed starting point;
confirm overall cassette width including transmission and bearing supports.

Use a centrifugal suction blower with a published pressure/flow curve and
integrated or explicitly matched electronics. A documented example worth
comparing is the
[Micronel U51DL-012KK-4](https://www.micronel.com/productfinder/radial-blower-u51dl-012kk-4/).
Its [datasheet](https://www.micronel.com/wp-content/uploads/2025/04/U51DL-012KK-4.pdf)
lists a nominal operating point of 180 L/min at 2.5 kPa and 30 W, integrated
control electronics, and 120 g mass. The 4.2 kPa shutoff and 440 L/min free-flow
figures are different endpoints, not simultaneous performance. This is a
filtered-air candidate downstream of the bin/filter, not a debris-handling fan.

This is **a blower shortlist entry, not an instruction to buy**: the
[Micronel USA DigiKey marketplace listing](https://www.digikey.com/en/products/detail/micronel-usa/U51DL-012KK-4/14545084)
was $398 plus separate shipping. Compare that cost with other documented
blower/controller assemblies after estimating the head/filter pressure losses.
The linked sheet also lists static speed above its continuous speed limit;
resolve that operating restriction before release. Do not size from shutoff
pressure, assume blocked operation is acceptable, or substitute the externally
commutated `-5` model as if it were the same electrical assembly.

For the later dedicated mop bottom, start with a replaceable microfiber pad,
metering pump, shutoff provision and pad lift. Preserve automatic station
servicing. Pad washing/drying, water delivery and drag need an integrated layout;
individual pump or actuator SKUs are not yet selected.

## Core and power

The Pi 4 and RPLIDAR A1 remain reasonable starting components because their
interfaces and geometry are documented. Retaining them does not require proving
the unknown BDUAV motor specifications. Keep a local microcontroller for physical
bump/cliff inputs, module latches and tool interlocks; reserve near-floor obstacle
sensing in addition to the planar LiDAR. LLM/MCP planning must not run the wheel
commutation or immediate stop loop.

Do not freeze a new battery around either the owned 3S pack or the deferred
flight module. Select a protected rechargeable pack, matching dock charger,
temperature monitoring and power distribution together after the operating
loads are budgeted. A 4S architecture remains possible, but a fully charged 4S
pack is 16.8 V: neither a nominally 12 V motor nor the shortlisted blower should
be assumed to accept that as an unrestricted supply. The blower's stated range
is 9–15 V. Specify motor voltage/current management and a regeneration path as
part of the power design, before choosing a battery SKU.

## Placement work that follows

The current ground CAD, JSON and component CSV still describe the earlier
inventory-based placement. They do **not** establish fit for this recommendation.
Keep them as a reference while preparing the next revision:

1. Repack the wider wheel cartridges, caster, compact head and air path inside
   275 × 275 × 180 mm, including suspension motion and caster sweep.
2. Carry forward the verified wheel-to-hub mating geometry, and finish D-shaft
   clamping engagement, screw lengths, bearing loads, encoder clearance and tool
   access. Include the tire's inward overhang in the bracket design.
3. Reserve bin/tank and dock interfaces; calculate empty/full wheel loading and
   mass allowances for all three sections.
4. Complete power/control wiring and produce one compatible, costed assembly
   list before further fit prints or purchases.

No additional owner measurements are needed to begin that placement pass.
