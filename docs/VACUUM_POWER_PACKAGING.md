# Converter and caster packaging decision

> **Scope update, 2026-09-13:** [Whole-system design](SYSTEM_DESIGN.md) now controls
> cross-module layout, carried mass, lift sizing and battery decisions. This
> earlier study remains supporting evidence; its lift deferral or battery-first
> recommendation, where present, is superseded.


2026-09-13. Working design update; no new purchase or print release.
**Battery architecture under review:** the owner asked whether a different battery
would replace the need for this converter. The Cincon placement is a 3S-based
comparison case, not a committed purchase. The owner has supplied specific 6S and
8S LiPo candidates; compare the pack and all regulation/charging hardware before
finalizing this bay. **6S is the current design preference**, pending that review.
No replacement battery or direct-battery blower connection has been approved.

The [integration model](../design/ground/output/vacuum_integration.html) includes
the converter cooling stack and a complete caster swivel envelope. Select a part
and **Isolate selected assembly** to inspect that bay.

## 24 V working baseline

### Battery alternative to evaluate first

| Battery option | Nominal / full voltage | Effect on this robot |
|---|---|---|
| Owned 3S LiPo | 11.1 / 12.6 V | Keeps the present traction branch; needs the 24 V blower converter. |
| 4S LiPo | 14.8 / 16.8 V | Still needs a blower boost stage; also requires reconsidering the 12 V motor limits. |
| 6S conventional Li-ion/LiPo | 21.6–22.2 / 25.2 V | Candidate for a higher-voltage main bus; battery voltage falls below 24 V during discharge. Direct blower operation remains unqualified. |
| 8S conventional LiPo | 29.6 / 33.6 V | Can supply a 24 V buck regulator with a suitable discharge cutoff; exceeds the blower driver's input rating and approaches the RoboClaw's 34 V maximum. |

The kit driver is specified for 9–29 V, but its motor data gives performance at
24 V only. The driver's input range does not establish the blower's permitted
maximum voltage or its low-pack pickup capability. Constant 24 V from 6S would
still require a regulator that can both step up and step down.
[BIQU motor and driver specifications](https://global.bttwiki.com/Universal%20Turbo%20Kit.html).

The ordered Pololu 4846 motors are rated 12 V; the IMC404 controller supports up
to 34 V. A higher battery voltage therefore requires either a properly designed
12 V traction supply or verified controller voltage/current limits appropriate
to these motors and operating modes. Controller input compatibility alone does
not establish motor compatibility. A supply before the RoboClaw must account for
returned braking energy; an ordinary buck converter is not assumed to absorb it.
[Motor rating](https://www.pololu.com/product/4846/specs),
[controller specifications](https://www.basicmicro.com/RoboClaw-2x7A-Motor-Controller_p_55.html),
[regeneration requirements](https://resources.basicmicro.com/manual/roboclaw/operational-requirements/).

Compare complete installed mass, dimensions, cost and losses: pack with balancing,
protection and temperature monitoring; remaining converters; motor protection;
and compatible dock charging. A BMS does not replace a charger. Capacity comparison
must use Wh: 22.2 V × 2.6 Ah and 11.1 V × 5.2 Ah are both approximately 57.7 Wh.
Higher voltage alone does not add energy. Pack current capability must cover the
combined load and startup; no replacement capacity or pack SKU is selected yet.

### Exact 6S and 8S candidates supplied by the owner

Listing specifications retrieved 2026-09-13; these are reference values, not
measurements of delivered batteries. Neither pack has been recorded as purchased.

| Property | [Zeee, ASIN B0BNDHPBBX](https://www.amazon.com/dp/B0BNDHPBBX) | [Ovonic Roam, ASIN B0D3HSY7PM](https://www.amazon.com/dp/B0D3HSY7PM) |
|---|---:|---:|
| Configuration / capacity | 6S1P / 5200 mAh | 8S1P / 5200 mAh |
| Nominal / fully charged voltage | 22.2 / 25.2 V | 29.6 / 33.6 V |
| Calculated nominal energy | 115.44 Wh | 153.92 Wh |
| Listed body, L × W × H | 155.5 × 48.5 × 50 mm | Approximately 156 × 47 × 61 mm |
| Listed battery mass | Approximately 753 g | Approximately 921 g |
| Power connector | EC5 | XT90-S anti-spark |
| Advertised discharge rating | 100C | 150C |

The Ovonic dimensions convert its listed 6.14 × 1.85 × 2.4 inches; its mass
converts the listed 2.03 lb. Its description contains a stray 22.2 V claim, which
conflicts with its 8S title and 29.6 V specification. Treat the table as the 8S
candidate and confirm the delivered label. Neither advertised C rating establishes
usable sustained flight current, voltage sag or thermal performance.

At equal 5.2 Ah capacity, 8S gives **33.3% more nominal energy** and draws 25% less
battery current at the same electrical power and corresponding cell voltage.
These particular listings suggest about **168 g more battery mass** and 11 mm more
body height. At an illustrative 100 W average battery draw and 80% usable-energy
allowance, runtime is about **55 minutes for 6S or 74 minutes for 8S**. Additional
mass and changed conversion losses can change the actual load; these are not
measured cleaning runtimes.

**Recommendation: use the Zeee 6S pack as the preferred candidate for the next
power and packaging review.** It has lower listed mass and height and stays well
below the existing RoboClaw's 34 V input ceiling. This is not a direct-battery
connection or a confirmed packaging release. In particular:

- **Blower:** 6S needs buck-boost regulation for constant 24 V throughout its
  intended discharge range. 8S permits a buck-only approach if the minimum loaded
  battery voltage remains above 24 V plus converter dropout. Raw 8S exceeds the
  kit driver's 29 V maximum, even at nominal voltage.
- **Traction:** both candidates require addressing the 12 V motor rating and
  braking-energy path. A fully charged 8S pack is only 0.4 V below the RoboClaw's
  34 V maximum, leaving inadequate design margin for a proposed raw 8S connection.
  A regulated traction branch with managed regeneration, or different hardware,
  would be needed. An ordinary buck alone does not resolve returned braking energy.
- **Charging:** the owner's Tenergy front panel lists support for 1–6 lithium
  cells, so 8S needs another development charger. The exact charger model and
  power limit remain unknown; 6S capability on the label does not establish its
  available charge rate. Both packs still need a designed automatic dock-charging
  system with cell balancing, monitoring and appropriate protection.

Electrical limits: [BIQU driver specification](https://global.bttwiki.com/img/Turbo_Kit/Turbo_Kit_Driver1.webp),
[RoboClaw IMC404 specifications](https://www.basicmicro.com/RoboClaw-2x7A-Motor-Controller_p_55.html).
Charger capability is from the owner's photograph, not an assumed model number.

8S remains an option if the eventual lift design justifies its voltage and mass.
Neither voltage is yet qualified for whole-robot flight. Choosing 6S for floor
development does not freeze the future lift battery interface or propulsion system.

### 6S 5200 mAh candidate across attachments

The owner proposed this capacity as a possibility for vacuum, mop, dusting and
whole-assembly lift. The Zeee candidate is now identified above, but its installed
fit and flight capability remain unconfirmed. Its nominal voltage gives 115.44 Wh,
twice the nominal energy of the owned 11.1 V / 5.2 Ah pack. Using 80% as a floor
planning allowance gives 92.35 Wh. This percentage is an assumption, not a tested
usable capacity or a flight reserve policy.

| Assumed average total battery-side draw | Calculated floor runtime from 92.35 Wh |
|---|---:|
| 60 W | 92 minutes |
| 100 W | 55 minutes |
| 150 W | 37 minutes |

Include electronics, traction, active tools and conversion losses in that draw.
These are sensitivity cases, not measured attachment loads or coverage estimates.
Because bottoms are exchanged, do not sum vacuum, mop and duster as simultaneous
loads. A powered mop may use less energy than the blower but scrubbing drag and
pad motors are unselected. Dry dusting and blower-assisted dusting are different
load cases. Airborne dusting adds the cleaning load to the lift load.

For scale only, a hypothetical **1.5 kW total flight draw** would take about 71 A
at 21 V under load and 25 Wh for one minute. Neither power nor transfer duration
has been established for this robot. Capacity alone cannot qualify lift: assess
pack discharge curves, sag, temperature, connectors and protection behavior
against the complete flight assembly and heaviest permitted loaded bottom. Include
water and wet pads for the mop. Stop routine cleaning before the energy needed
for the planned transfer and landing reserve is consumed; recharging at each floor
allows that reserve to be restored. The 80% floor allowance is not permission to
launch at its end. Voltage sag and capacity both matter to flight monitoring.
[ArduPilot voltage/current guidance](https://ardupilot.org/copter/docs/current-limiting-and-voltage-scaling.html),
[battery failsafe documentation](https://ardupilot.org/copter/docs/failsafe-battery.html).

Retain the battery in a replaceable core tray. The CAD still uses the owned
135 × 43 × 22 mm battery in a 164 × 59 × 32 mm reservation. Both supplied packs
exceed that reservation's height in every orientation. Their similar footprint
does not establish a fit: allow for restraint, protection, leads, connector bends
and service removal as well as the taller body. The current 178 mm assembled-height
result applies to the 3S layout only. Repack within the owner's 275 × 275 × 180 mm
limit before releasing a new tray. Candidate masses are not added to the existing
assembly ledger or substituted into the CAD as though either pack were installed.

The floor tool branch and eventual lift branch require separate current ratings.
Lift power must not pass through a wheel-voltage regulator or inherit the floor
connector/fuse ratings. The 6S bus also requires resolving the existing 12 V wheel
motors and 24 V blower as described above, plus pack-specific automatic charging.
No existing pack-protection board is assumed suitable for flight merely because
it supports six cells. Lift design remains deferred pending mass and propulsion
requirements.

**Owner's pack-link question resolved:** Zeee B0BNDHPBBX and Ovonic B0D3HSY7PM are
recorded above. Next design work is to compare the complete regulated power branches
and charging provisions, then revise the core battery placement. No additional
owner measurement is needed to perform that draft review.

### Retained 3S converter comparison

Use **Cincon CHB100W-24S24** as the electrical and packaging baseline: 9–36 V
input, 24 V / 4.17 A output, nominal 100 W rating. Its case is 61 × 57.9 × 12.7 mm
and its reference mass is 95 g, excluding the carrier and cooling. The robot
retains an **80 W supply allocation**; the Wonsmart driver's lower continuous
rating still governs the blower load. This converter accommodates the voltage
range of both 3S and 4S, without approving a 4S change for the other branches.
[Cincon datasheet, model-specific row](https://www.cincon.com/productdownload/Datasheet-CHB100W.pdf).

This is more expensive than the $45 DFRobot FIT0172 screened previously. It earns
its place through documented low-input operation, thermal data and distributor
sourcing, with a smaller and lighter bare module. It still requires integration.

| Part | Procurement route / observed price | Status |
|---|---|---|
| CHB100W-24S24 | [DigiKey 2034-3000-ND](https://www.digikey.com/en/products/detail/cincon-electronics-co-ltd/CHB100W-24S24/9684253), $104.30 | Working baseline, not ordered. Cached listing shows stock; delivery must be checked at checkout. |
| Cincon HBT127, also called M-C091 | [DigiKey 2034-3489-ND](https://www.digikey.com/en/products/detail/cincon-electronics-co-ltd/M-C091-HEAT-SINK/9684742), $4.82 | Matched heat-sink candidate. Product/category stock results disagree; availability unresolved. |
| PH01 thermal pad and heat-sink screws | Cincon thermal accessories | Pad required by this stack. Confirm actual kit contents and screw engagement; no duplicate kit and separate-parts purchase. |
| Noctua NF-A4x10 **5V**, three-wire version | [Manufacturer's retailer/Amazon links](https://www.noctua.at/en/products/nf-a4x10-5v/buy) | Cooling candidate; price not recorded. Fan rating does not establish cooling in this enclosure. |
| Carrier, input/output components, fuse, inhibit circuit, temperature sensing, fan guard and duct | To be specified together | Required additions; converter alone is not a wiring kit. |

The two priced items total **$109.12 before the remaining parts, tax and shipping**.
This is not a complete assembly quote. Distributor data accessed 2026-09-13 can
be cached; neither stock nor cost is a delivery promise.

## Physical stack

The previous 61 × 60 × 32 mm allowance omitted necessary installation space.
The new bay is **70 × 70 × 50 mm**, at x176–246, y92–162, z70–120 mm.
The battery tray shifts 15 mm left and the Pi tray 4 mm forward. There is 6 mm
between this bay and the top of the allocated moving motor pod, and 3 mm between
its side and the right-wheel reservation. These are space checks; frame thickness,
wire bends and tolerances must be fitted within them.

| Layer | Floor-relative z range, mm | Basis |
|---|---:|---|
| Lower support/insulation space | 70–74.2 | Proposed; maximum pin lengths and solder joints need checking |
| Carrier PCB | 74.2–75.8 | Proposed 66 × 64 × 1.6 mm outline, not a routed board |
| Case-to-PCB gap | 75.8–78 | Proposed 2.2 mm; 4.6 mm minimum pins project 0.8 mm through the board |
| Converter case | 78–90.7 | Manufacturer reference |
| Thermal pad | 90.7–90.95 | PH01 reference |
| Heat sink | 90.95–103.65 | HBT127 reference envelope; fin details omitted |
| Fan-to-fin space | 103.65–105.65 | Proposed 2 mm; airflow not proven |
| Fan with pads | 105.65–117.65 | Allocate 12 mm from extended specifications |
| Upper allowance | 117.65–120 | 2.35 mm for clearance/guard; requires a vented cap above |

The fan's nominal name says 10 mm, while its current extended specifications say
11 mm without pads and 12 mm with pads. Use the latter for packaging. It draws
up to 0.25 W at 5 V and has a 15 g reference mass. Include it within the 25 W
logic-branch allocation and provide a local tachometer interface.
[Noctua mechanical/electrical specifications](https://www.noctua.at/en/products/nf-a4x10-5v/specifications).

Cincon identifies HBT127 with M-C091; its envelope is 61 × 58 × 12.7 mm and its
reference mass is 50.4 g. PH01 is 60 × 56.9 × 0.25 mm, 1.9 g. The current thermal
document mixes K310W kit naming with an M3×8 drawing callout: verify hardware
against the actual mounting stack before specifying screw length.
[Cincon thermal accessories, pp. 2, 14 and 16](https://www.cincon.com/_i/assets/upload/files/Datasheet-HS-LBQBHBFB.pdf).

Converter, sink, pad and fan contribute **162.3 g of reference mass**. Carrier,
fasteners, wiring, guard and duct are additional and unweighed. The mass ledger
keeps these separate from the remaining generic core-power assembly.

## Cooling and startup still to close

At an **assumed 82% efficiency**, an 80 W output means `80/0.82 − 80 = 17.6 W`
of heat. This is a sizing scenario, not a measured 3S efficiency. The published
87.5% nominal-input figure must not be assigned unchanged to a 3S battery.

Using the heat-sink document's typical case-to-air resistances gives this screen:

| Cooling condition in supplier test | Typical resistance | Estimated case at 35°C local air and 17.6 W loss |
|---|---:|---:|
| Natural convection | 4.7°C/W | 118°C |
| 100 LFM through fins | 2.89°C/W | 86°C |
| 200 LFM through fins | 2.30°C/W | 75°C |

Thus a sealed, passively cooled printed pocket is unsuitable at this allocation.
These figures do **not** predict our top-mounted fan's fin velocity or thermal
resistance. Develop an outside-air inlet through the cap, a shroud and transverse
outlets that prevent recirculation into the inlet or heating the adjacent battery.
Keep this air separate from vacuum dirty air and blower exhaust. The drawing has
not yet reserved a complete inlet/outlet duct. An 85°C converter-case ceiling at
35°C local inlet air is a proposed engineering target; plastic, battery and nearby
components require their own lower temperature limits and separation.

Close these items before buying the complete power assembly:

- Carrier schematic/layout: input filtering and fuse, output decoupling and local
  sense connections, intentional ground-bond/isolation choice, and wire routing.
- Hardware-default-off converter and blower control through startup, MCU reset,
  an unplugged module and stop commands. The positive-enable converter runs
  with its input open; a direct 3.3 V high is below the specified high threshold.
- Total driver/input capacitance and controlled startup. Use the model datasheet's
  1800 µF load-capacitance limit pending clarification; the family application note
  lists 2200 µF. Do not silently choose the larger number.
- Thermal/airflow design, case-temperature sensing and fan-loss response. Validate
  the installed assembly at the selected pack cutoff and actual blower load,
  including startup, before unrestricted operation.

The converter's own undervoltage shutdown is too low to serve as this pack's
discharge policy. Pack/cell monitoring remains separate. Manufacturer application
guidance covers low-line current, filtering, sensing and thermal derating; its
family maximum input current is not the robot's fuse selection.
[Cincon application note](https://www.cincon.com/productdownload/CHB100W-series-application-note.pdf).

## Caster space corrected; purchase choice remains open

The **TENTE 1530PJO040P41** illustrates the missing swivel clearance: 40 mm wheel,
51 mm overall height, 19 mm offset, and **78 mm complete swivel diameter**. Its
plate is 37 × 37 mm. This cannot fit the old 76 × 65 mm allowance.
[Manufacturer geometry](https://www.tente.com/en-ca/swivel-castor-40-mm/1530pjo040p41).

The revised rear-right bay is **80 × 80 × 60 mm**, with pivot x232/y232. The
reference has 1 mm radial margin and 9 mm above it for mounting, not an extra
9 mm of wheel travel. The 1 mm is a minimum geometric screen, not a finished
hair-clearance or deflection allowance. It remains outside the bin volume.

Do not order that TENTE reference as the final caster: its riveted axle and absent
thread guards conflict with the desired hair access, and a US distributor route
has not been established. Seek a removable axle, protected bearing gaps,
nonmarking compliant tread and published complete swivel dimensions. If that
requires a larger bay, repack it before printing. Load capacity alone does not
prove that a small passive wheel will cross a 10 mm threshold.
[Manufacturer axle/tread details](https://www.tente.com/en-us/swivel-castor-1.57-in/1530pjo040p41).

The caster stays offset because centering it would intrude into or raise the bin.
Empty/full mass distribution and the contact triangle, including caster trail,
remain a required design check. No stability result is inferred from this placement.

## Effect on module exchange

The core power bay projects 16 mm below the z86 mating plane; the vacuum towers
project 34 mm above it. A conservative horizontal-transfer screen therefore needs
both projections cleared: **60 − 16 − 34 = 10 mm** separation. The station's
proposed tray starts at 70 mm and lowers to 10 mm after capturing the core.
Loading/lifting and the rear module lock still need mechanisms. The platform
height is not a step the robot is expected to climb.
