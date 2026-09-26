# Drivetrain sourcing

2026-09-12. Supplier cross-reference for the proposed ground drivetrain. Prices
are USD listing snapshots before shipping, tax and any tariffs; stock statements
are not confirmed delivery dates. The [machine-readable source list](../config/drivetrain_sources.csv)
contains alternative suppliers and alternative components, **not a cumulative
shopping list**. Assembly hardware and power electronics are not yet complete.

## Recommendation

Keep the compact Pololu 25D encoder motors, RoboClaw controller and 72 mm Hogback
wheels as the preferred design candidate from the
[component recommendation](GROUND_COMPONENT_RECOMMENDATION.md). These can be
purchased through distributors, although availability has qualifications:

| Component / manufacturer part | Supplier and supplier SKU | Unit price | Listing status |
|---|---|---:|---|
| Pololu encoder gearmotor **4846**, two required | [DigiKey](https://www.digikey.com/en/products/detail/pololu/4846/10450248), **2183-4846-ND** | $56.95 | Marketplace; stock reported, shipped by Pololu |
| Same Pololu motor | [RobotShop](https://www.robotshop.com/products/pololu-12v-751-metal-gear-motor-hp-48-cpr-protected-encoder), **RB-Pol-840** | $56.95 | Re-stocking soon |
| Basicmicro RoboClaw 2x7A **IMC404**, one required | [RobotShop](https://www.robotshop.com/products/roboclaw-2x7a-6-34vdc-regenerative-motor-controller), **RB-Bat-22** | $79.95 | Re-stocking soon |
| Same RoboClaw controller | [Pololu](https://www.pololu.com/product/3682), **3682** | $79.95 | Backorder; owner also confirmed unavailable |
| Same RoboClaw controller | [ServoCity](https://www.servocity.com/roboclaw-2x7a-motor-controller/), **IMC404** | $79.99 | Listed without an out-of-stock label; dispatch unverified |
| Same RoboClaw controller | [Basicmicro](https://www.basicmicro.com/RoboClaw-2x7A-Motor-Controller_p_55.html), **IMC404** | $79.95 | Manufacturer-direct; explicitly reports in stock |
| Hogback wheel **3626-0014-0072**, two required | [RobotShop](https://www.robotshop.com/products/servocity-hogback-traction-wheel-72mm-diameter-50a-durometer), **RB-Sct-3644** | $8.99 | On demand; not normally stocked |
| Sonic 4 mm hub **1309-0016-0004**, two proposed | [RobotShop](https://www.robotshop.com/products/1309-series-sonic-hub-4mm-bore), **RB-Sct-1456** | $6.99 | On demand; not normally stocked |

The DigiKey motor listing offers distributor checkout, but does not establish a
second independent stock location: Pololu also identifies this relationship on
its [distributor page](https://www.pololu.com/product/4846/distributors).
[ServoCity](https://www.servocity.com/hogback-traction-wheels/) is another purchase
route for the same wheel, rather than a different interchangeable wheel design.
The nominal wheel-to-hub interface has now passed the supplier CAD check below.
Order the wheels and hubs together; physical wheels are not required to finish
the remaining bracket design.

**Controller availability follow-up:** the owner confirmed backorders at Pololu
and RobotShop. Basicmicro's product and category pages explicitly report stock;
ServoCity provides another US reseller listing, but no dispatch date was verified.
The direct manufacturer route does not satisfy distributor sourcing by itself.
Check ServoCity's fulfillment before ordering if distributor purchase is the
priority. These are purchase routes for IMC404, not a controller redesign; confirm
the supplied hardware revision before releasing its printed mount. The 2x15A
version was also backordered at Pololu and RobotShop when checked, so it does
not currently resolve those distributors' availability problem.
[Pololu 2x15A](https://www.pololu.com/product/3683) and
[RobotShop 2x15A](https://www.robotshop.com/products/roboclaw-2x15a-6-34vdc-regenerative-motor-controller).

## Alternatives with conventional DigiKey and Mouser listings

These are independent alternatives: either controller architecture could drive
either brushed motor candidate after appropriate configuration and sizing.

| Component | DigiKey | Mouser | Unit price at either listing |
|---|---|---|---:|
| DFRobot **FIT0185**, 12 V, 83 RPM encoder gearmotor | [1738-1105-ND](https://www.digikey.com/en/products/detail/dfrobot/FIT0185/6588527) | [426-FIT0185](https://www.mouser.com/en/ProductDetail/DFRobot/FIT0185?qs=lqAf%2FiVYw9g4vmxHGv4taQ%3D%3D) | $16.50 |
| DFRobot **DFR0601**, dual brushed-motor driver | [1738-DFR0601-ND](https://www.digikey.com/en/products/detail/dfrobot/DFR0601/10279757) | [426-DFR0601](https://www.mouser.com/ProductDetail/DFRobot/DFR0601?qs=PzGy0jfpSMt2BcSAELKXOA%3D%3D) | $29.38 |

All four listings reported distributor stock when reviewed. Check delivery and
price when ordering; this is not a stock reservation.

**FIT0185 motor:** the manufacturer documents a 37 mm body, 205 g mass and 6 mm
D shaft, versus 25 mm, 104 g and 4 mm for the Pololu. Two motors add about
202 g before changes to brackets and hubs. With 72 mm wheels, its nominal
83 RPM no-load speed corresponds to 0.31 m/s; loaded speed will be lower.
It requires a different mounting plate, 6 mm hub and encoder configuration.
It is not a drop-in replacement within the 275 mm chassis.
[DFRobot specifications](https://wiki.dfrobot.com/fit0185/) and
[Pololu specifications](https://www.pololu.com/product/4846/specs).

FIT0185 remains a conditional alternative: the current manufacturer table gives
stall torque, without an established continuous-duty torque rating. Do not use
the advertised 45 kgf·cm stall figure as a working load. Obtain the manufacturer's
continuous-load guidance before selecting it for the cleaning robot; the main
design does not depend on another characterization rig. The Pololu's documented
gearbox continuous-load guidance is one reason it remains preferred.
[FIT0185 product page](https://www.dfrobot.com/product-633.html) and
[Pololu load guidance](https://www.pololu.com/product/4846).

**DFR0601 controller:** this is a 6.5–37 V, two-channel H-bridge rated for
12 A continuous per channel, with 3–5 V control inputs and a
50 × 50 × 12.5 mm envelope. It is a power stage, whereas RoboClaw also processes
encoders and runs velocity loops. DFR0601 does not document programmable
motor-current limits or current telemetry.
[Manufacturer specifications](https://www.dfrobot.com/product-1861.html/).

A [Raspberry Pi Pico 2, SC1631](https://www.digikey.com/en/products/detail/raspberry-pi/SC1631/24627136)
is a distributor-stocked MCU candidate at $6.12. DFR0601 plus Pico 2 is $35.50
for those two boards only. Matching RoboClaw's intended role additionally needs
encoder interfacing, velocity-control firmware, current sensing/protection,
command timeout and a defined hardware disable state. Provide suitable logic
levels for the selected encoder and MCU. DFR0601's floating control inputs read
high; design explicit startup states. Board overtemperature protection is not
a motor-winding current limit.
[DFR0601 interface documentation](https://wiki.dfrobot.com/dfr0601/docs/18917).

Both architectures need a separate Pi supply and a braking-energy plan. A driver
accepting 4S battery voltage does not make a 12 V motor safe at unrestricted
4S drive. Complete those details during power integration.

## Wheels and interchangeability

### Wheel-to-hub check, 2026-09-12

FreeCAD inspection and assembly of the manufacturer's STEP files for
**3626-0014-0072** and **1309-0016-0004** confirm:

- Four shared mounting positions form a 16 × 16 mm square. The wheel has
  nominal 4 mm through holes; the hub has M4 threaded holes.
- The hub's 14 mm diameter, 2 mm long centering boss mates with the wheel's
  nominal 14 mm bore. The models have zero volumetric intersection when seated.
- The hub body is 8 mm long; the wheel mounting web is 4 mm thick. With the hub
  back at axial zero and the web seated at +8 mm, the tire spans -4 to +20 mm.
  Its inward overhang must be included in the printed bracket design.
- Pololu publishes a 12.5 mm long output shaft. Relative to the hub's 8 mm body,
  this leaves 4.5 mm for bracket/clearance consumption before full body engagement
  is lost. Placement and clamping on the actual D shaft remain assembly checks.

This establishes nominal mating of the purchased wheel and hub, not a finished
motor cartridge. Bracket shape, clamp access, fastener selection, shaft loading
and the complete 275 mm chassis envelope still need integration. Physical parts
will validate manufacturing tolerances during normal assembly; they are not a
prerequisite for these CAD checks. The practical wheel order is **two wheels plus
two hubs**. Wheels alone do not attach to the motor shafts.

[Hub CAD download](https://www.gobilda.com/content/step_files/1309-0016-0004.zip),
[wheel CAD download](https://www.gobilda.com/content/step_files/3626-0014-0072.zip),
and [motor shaft dimensions](https://www.pololu.com/product/4846/specs).

### Traction and other wheel options

The Hogback's specified silicone tread and 50A hardness make it a reproducible
candidate, but there is no published wet wood/tile traction coefficient. Its
performance on the intended cleaner film still needs a brief assembled-robot
check. Keep the wetted mop pad behind the normal wheel contacts and account for
crossing previously mopped areas.
[Wheel specification](https://www.gobilda.com/hogback-traction-wheel-72mm-diameter-50a-durometer/).

Two widely catalogued wheels do not replace it directly:

- [DFRobot FIT0199-R](https://www.dfrobot.com/product-653.html): the manufacturer
  allows tire material and tread pattern to vary. That is unsuitable as our
  reproducible traction reference.
- [DFRobot FIT0500](https://www.dfrobot.com/product-1535.html): an 80 × 17 mm
  silicone wheel, but its TT-motor mounting profile differs from both proposed
  D shafts. It would need a separately designed adapter.

For open-source acquisition, publish manufacturer part numbers, supplier SKUs,
drawings and interface requirements together. Keep exact-part supplier links
separate from substitute-part profiles. Proposed profiles should record motor
plate/hub geometry, wheel diameter, encoder counts per output revolution,
voltage/current limits and controller interface. A generic “25 mm gearmotor”
or an Amazon title is insufficient to establish interchangeability.

Next, package the preferred drive assembly and reserve a replaceable motor plate
and controller adapter. A 37 mm alternate remains conditional on continuous-load
documentation and fit. No new motor plates, controller firmware or replacement
fabrication files are released by this sourcing document.
