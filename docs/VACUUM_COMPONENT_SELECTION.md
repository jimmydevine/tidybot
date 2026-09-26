# Everyday vacuum: consumables and blower selection

**Consumable recommendation superseded:** the
[requirements-based review](VACUUM_RECOMMENDATION_REVIEW.md) now prioritizes
TriCut investigation against hair-shedding alternatives, retaining an S7/S8-family
washable-filter candidate. The BIQU blower remains
provisional. The dual iRobot roller/s-series filter selection and associated
packaging and shopping figures below describe the earlier 2026-09-13 pass.
Its blower sources and curve calculations remain useful; they do not establish
the new filter's resistance. Drivetrain purchases are unchanged. Flight remains
deferred.

The [selection record](../config/vacuum_selection.json) separates SKU information,
owner measurements, proposed allowances, sourcing and unresolved items. It does
not relabel unidentified inventory as genuine iRobot parts.

### Basis for retaining the owned consumables

The owner asked whether inventory availability or suitability drove these
choices. Both influenced the study; neither owned component has been established
as the best fit. The short rollers have a packaging rationale independent of
ownership: their measured length leaves room for supports inside the 275 mm
width. That does not establish comparative pickup, hair handling, drive power or
durability. The filter choice relied more heavily on the available inventory
and its large frame; active media area, clean/loaded resistance, sealing quality
and complete installed volume remain unverified.

Treat the owned rollers and filters as candidates for reuse. The earlier
conversation's commitment to design around them was premature. The owner's
priority is suitability for the complete robot, with reuse when it meets that
priority. The OEM SKUs below are candidate replacement references, not confirmed
identifications of the owned parts or proof of interchangeability. No duplicate
consumable purchase follows from this record; keep the adapters provisional
until the integrated comparison supports the selection.

## Size-constraint audit

2026-09-13: **The selected parts remain plausible candidates for the everyday
275 × 275 × 180 mm robot, but complete assembled fit is not established.** The
new study is a top view; the older 178 mm ground assembly uses different wheels,
blower and controller. Its height and collision checks do not validate this
selection. Keep the owner's size limits fixed while integrating these parts.

| Item | Current evidence | Remaining fit work |
|---|---|---|
| Wheels, hubs and drive motors | Proposed tire span is 271 mm, leaving 2 mm per side. The motor bodies leave an 85 mm central gap. Supplier wheel/hub models mate. | Bracket thickness, shaft engagement, tire clearance, suspension sweep and guards must fit together. The 2 mm is nominal outline margin, not a sufficient guard or tolerance allowance. |
| Short roller cassette | Proposed 214.15 × 72 mm footprint, with the drive moved above one end. | Exact selected roller dimensions and the complete drive/support assembly remain unverified. |
| Bin and filter | Bin outer reservation is 192 × 80 × 60 mm; proposed filter holder is 144 × 84 × 24 mm. | Place the holder, plenum, seals and removal path separately; its 84 mm depth exceeds the bin's 80 mm reservation. Deduct the caster well and ducts from usable bin volume. |
| BIQU blower assembly | Bare blower is 71 × 70 × 37.5 mm; separate driver PCB is 50 × 40 mm and adapter is 38 × 38 mm. | Inlet/exhaust fittings, isolation mounts, board component heights, cooling and the unselected 24 V converter still need space. |
| RoboClaw IMC404 | Basicmicro publishes 48 × 42 × 17 mm for the controller. | Add standoffs, attached connectors and wire bends; confirm the delivered revision before making its mount. |

[Top-view dimensions and assumptions](../design/ground/output/next_vacuum_study.json),
[wheel/hub stack check](DRIVETRAIN_SOURCING.md),
[Basicmicro mechanical specifications](https://www.basicmicro.com/RoboClaw-2x7A-Motor-Controller_p_55.html).
Blower and consumable sources and dimensional limitations are detailed below.

Height is the unresolved constraint: retaining the older study's 55 mm-tall A1
reference above a clear cap leaves at most **125 mm from the floor to the LiDAR
mounting surface**, before any additional top protection. For comparison, simply
stacking the 60 mm bin reservation, 24 mm filter holder and 37.5 mm blower consumes
121.5 mm; adding the LiDAR would consume 176.5 mm before floor clearance, plenums,
mounts or core structure. This is an illustration of an unsuitable simple stack,
not the proposed assembly height. Arrange the blower beside the filter where
possible and use passive pockets through the core for taller bottom components,
while preserving module separation and the scan view.

The next 3D placement must include the battery and its leads, Pi and cooling,
both motor-control systems, power conversion, roller and side-brush drives,
caster/head motion, bumpers, latches, wiring and service/removal paths. Revise
placement or component choices if those do not fit. This audit covers the
everyday vacuum bottom, core and cap/LiDAR; it does not establish the size of the
deferred flight or deployed long-reach attachments.

## Consumable choice

| Function | Design baseline | Installed quantity | Published purchase price, USD |
|---|---|---:|---:|
| Main rollers | [iRobot 4639309](https://www.irobot.com/en_US/dual-multi-surface-rubber-brushes-for-roomba-combo-and-roomba-e,-i,-and-j-series-and-roomba-combo-10-max/4639309.html), complementary e/i/j rubber pair | 1 pair | $39.99/pair; approximately two weeks to ship shown |
| Fine filter | [iRobot 4643682](https://www.irobot.com/en_US/high-efficiency-filter,-3-pack-for-roomba-s-series/4643682.html), s-series high-efficiency element | 1 element | $39.99/three-pack; in stock shown |

Use the short roller family to preserve end-support and drive space inside the
275 mm body. The pair uses different drive-end shapes; the manufacturer identifies
square and hex pegs and provides removable-end maintenance instructions. Keep both
ends accessible. Rubber rollers still accumulate hair at their ends; automatic
bin emptying does not eliminate this service task.
[Manufacturer brush-care instructions](https://support.irobot.co.uk/articles/en_GB/Knowledge/2451).

The owner's **184.15 mm overall length and 28 mm diameter** remain useful study
envelopes, but are not verified dimensions of genuine 4639309. Working rubber
length, support seats, drive engagement and required pair spacing must come from
the exact selected parts before couplers are printed. Do not describe 184 mm as
the cleaning swath. The existing 214 mm cassette proposal remains provisional;
allow the end plates to move if the selected pair differs.

The filter can be from a different family because we are designing its housing.
Reserve a generous filter area and accessible drawer instead of minimizing the
filter first. The owner's s9-compatible frame measures **136 × 76 × 14 mm**, with
the recorded pull tab. Its outer face is 103.4 cm²; that is not active media area.
A genuine 4643682 still needs its sealing land and tab checked. Proposed initial
holder allowance: **144 × 84 × 24 mm**, excluding plenum and finger access. This
is above/rear of the bin and is wider in depth than the 80 mm bin reservation;
it cannot simply be inserted into that bin envelope. The next 3D pass must reserve
its own space and removal path through the core's passive equipment pockets.

Use a replaceable filter adapter, a continuous compressible perimeter gasket,
and a latch bearing on the rigid frame. Protect the pleats from direct hair
impact with a smooth baffle and a removable, generously open hair guard. Its
open area and clogging behavior remain to detail; adding a fine screen would
introduce another loading surface. Keep pressure taps on both sides of the filter.

No clean/loaded pressure-loss curve was found for the selected filter. Neither
frame size nor the OEM's allergen claim establishes our assembled system's
filtration efficiency. Treat it as a dry filter; iRobot instructs users not to
wash it. The bin can be designed for washing separately, then dried before use.
[Filter care](https://support.irobot.co.uk/articles/en_US/Knowledge/20986).

### Alternatives considered

| Option | Decision |
|---|---|
| Long s9 roller pair | Leave out of the compact baseline. The owned 254 mm pair already exceeds 275 mm once both supports and walls are included under our current allowances. |
| Complete [iRobot cleaning head 4706166](https://www.irobot.com/en_US/roomba-cleaning-head-module-for-roomba-i3-and-j7-series/4706166.html) | $89.99 including brushes; potentially reduces custom drive work. The reviewed listing does not give the mounting envelope, electrical interface or drive ratings needed here. Its dated compatibility restrictions also make it a less reproducible module than replaceable consumables. Retain as an alternative, not a verified drop-in. |
| Compact [e/i/j filter 4639161](https://www.irobot.com/en_US/high-efficiency-filter%2C-3-pack-for-roomba-combo-and-roomba-i%2C-e%2C-and-j-series/4639161.html) | $36.99/three-pack. A packaging alternative if the larger filter cannot fit. No pressure-loss curve found for this one either; do not assume one small element or two parallel elements is equivalent to the s filter. |

Sourcing is broad at the **consumable-family** level, not uniformly immediate for
every OEM SKU. [Home Depot lists replenishment kit 4639168 for $64.99](https://www.homedepot.com/p/307337506),
containing a roller pair, side brushes and compact filters; check exact contents
and delivery before using a kit as a substitute. The
[Lowe's 4639309 page](https://www.lowes.com/pd/iRobot-Roomba-174-e-and-i-Series-Replacement-Dual-Multi-Surface-Rubber-Brushes/5000738263)
says no longer sold. [Lowe's lists 4643682](https://www.lowes.com/pd/iRobot-Roomba-s-Series-3-Pack-HEPA-Vacuum-Filter-for-Upright-Vacuums/1001069220)
with location-dependent availability. Publish dimensioned replaceable adapters;
do not promise that every aftermarket listing fits or filters identically.

## Blower choice

Prefer **BIQU Universal Turbo Kit V1.0, 1060000677**, containing a Wonsmart
WS7040-24-V200 and matched WS2403DY01V04 driver plus control adapter. It offers a
documented pressure/flow curve, separate electronics and public reference models.
Use it downstream of the fine filter, with a sealed inlet connection. The kit's
printer intake filter is not a substitute for our dust filter.

| Source | Useful information |
|---|---|
| [BIQU motor specification](https://global.bttwiki.com/img/Turbo_Kit/Turbo_Kit_Motor1.webp) | At 24 V: 13 m³/h at 4 kPa and 1.9 A. Calculated: 3.61 L/s and 45.6 W. Free flow: 25.5 m³/h, 2.7 A; static: 6.5 kPa. These are separate operating points. |
| [Dimensioned blower drawing](https://www.wonsmartmotor.com/uploads/WS7040-24-V200.pdf) | 71 × 70 × 37.5 mm; inlet ID 20.8 mm, outlet ID 12 mm. Add fittings, wiring and mounting space. |
| [BIQU driver specification](https://global.bttwiki.com/img/Turbo_Kit/Turbo_Kit_Driver1.webp) | Driver rated 3 A continuous, 6 A peak; 9–29 V electronics range does not make the 24 V blower a fully rated 3S load. EN grounded stops; floating runs. |
| [Kit manual](https://github.com/bigtreetech/Universal-Turbo-Kit/blob/master/Manual/Universal%20Turbo%20Kit%20User%20Manual.pdf) | Driver PCB 50 × 40 mm; adapter 38 × 38 mm. 24 V motor power is distinct from the adapter's fan-control input. |

Provide a hardware default-off enable/power path and local fault handling. Do not
depend on a Pi process or assume an unplugged command wire stops this driver.
Determine input polarity and safe signal levels in the wiring pass. Keep the
driver cooled and account for starting delay; its peak rating is not a measurement
of blower startup current. Installed mass and enclosure noise remain unknown.

### Curve comparison and its limits

The [comparison plot](../design/ground/output/vacuum_airflow_comparison.svg) and
[calculated results](../design/ground/output/vacuum_airflow_comparison.json) use
manually read curves, without extrapolation. Run
`MPLCONFIGDIR=/tmp/tidybot-matplotlib python3 design/ground/airflow_study.py`
to regenerate them; matplotlib is required.

For sizing, use **4 L/s against 2 kPa** as a proposed clean-system target and
**3 L/s against 3 kPa** as a proposed loaded-system target. These are engineering
assumptions for total head/duct/bin/filter/exhaust resistance, not proven pickup
requirements or measured filter characteristics. The script models each case as
`P = P_reference × (Q/Q_reference)²`. Actual filter behavior may differ.

| Published curve, at stated supply | Intersection with assumed clean system | Intersection with assumed loaded system |
|---|---:|---:|
| BIQU kit, 24 V | About 4.8 L/s | About 3.6 L/s |
| Wonsmart separate drawing, same motor number, 24 V | About 4.2 L/s | About 3.2 L/s |
| Micronel U51DL-012KK-4, 12 V graph | About 3.6 L/s | About 2.6 L/s |

These intersections are calculated predictions for hypothetical resistance curves.
The two Wonsmart/BIQU curves are **different published data**, not manufacturing
tolerance bounds. Their nominal curves support the 3–4 L/s study, but with
different margins. Tie procurement to the exact kit/driver; establish which curve
applies before treating the higher flow as a requirement met by delivered parts.
[BIQU curve](https://global.bttwiki.com/img/Turbo_Kit/Turbo_Kit_Motor2.webp),
[Wonsmart drawing and lower-flow curve](https://www.wonsmartmotor.com/uploads/WS7040-24-V200.pdf).

Micronel's datasheet has another discrepancy: its 12 V graph and table disagree
on working point and endpoints. The graph gives roughly 2 kPa at 180 L/min,
while the table gives 2.5 kPa there. The tabulated static speed exceeds its
continuous speed limit. It remains a premium alternative requiring clarification;
the [DigiKey Marketplace listing](https://www.digikey.com/en/products/detail/micronel-usa/U51DL-012KK-4/14545084)
shows $398 plus $23 shipping from Micronel USA.
[Micronel datasheet, pages 1, 2 and 5](https://www.micronel.com/wp-content/uploads/2025/04/U51DL-012KK-4.pdf).

The earlier 8 L/s sensitivity case is outside both WS7040 curves' free-flow limits;
drop it as a design expectation for this selection. Generic cooling blowers and
unidentified replacement vacuum fans are not additional baseline candidates.

## Integration consequences

- **Dirt passage:** start with a smooth 32 × 22 mm clear duct through the 85 mm
  motor-body gap, with a short compliant section at the floating head. At 4 L/s
  mean duct speed is 5.7 m/s. An illustrative 180 mm duct with Darcy factor 0.03
  and total minor-loss coefficient 3 loses about 62 Pa; this excludes all other
  parts and is not a system resistance prediction. Avoid internal fasteners and
  sharp hair-catching joints. The small printer hose is unsuitable as our main
  debris passage.
- **Exhaust:** the blower's 12 mm outlet gives about 35 m/s at 4 L/s. Use a short
  transition into a larger exhaust chamber, with a broad outlet directed away
  from the floor. Include its losses and acoustic treatment in the final model.
  Port speed is calculated, not a noise prediction.
- **Power:** allocate an **80 W continuous 24 V supply budget** with headroom;
  keep actual driver load within its rating. A 3S or 4S battery would need a boost
  converter for that branch. At assumed 90% conversion efficiency, 80 W means
  about 8 A from nominal 3S or 6 A from nominal 4S, for this branch alone. Startup
  and depleted-pack limits remain to size. This does not select a final battery,
  converter, or require changing the drivetrain's voltage.
- **Hair and automation:** provide removable bearing/end-shield plates, a broad
  bin evacuation opening, a sealed make-up-air route and onboard-blower isolation
  during station emptying. Monitor roller current and motion, stop on a jam,
  and limit automatic clearing attempts. A persistent jam should stop cleaning
  and request service. Filter differential pressure needs interpretation alongside
  blower command/airflow; pressure alone does not reliably identify a full bin.

## Purchase grouping and next fabrication dependency

Current prices before tax/shipping: [BIQU $53.99](https://biqu.equipment/products/universal-turbo-kit),
[Fabreeko $74.99 with hose](https://www.fabreeko.com/products/biqu-universal-turbo-kit-cpap-fan-for-3d-printer),
or [3DJake $67.62](https://www.3djake.com/biqu/universal-turbo-kit).
BIQU shows an order button; dispatch is not confirmed. Fabreeko exposes conflicting
stock text in the retrieved page. 3DJake shows six units but international shipping
is additional. Specify the full kit, not the hose-only variant or a different
"Eco"/"Panda" product.

The roller pair + three-pack of filters + BIQU blower kit would be **$133.97** at
the listed direct prices, or **$154.97** using Fabreeko's blower listing. These
totals exclude the remaining vacuum assembly and are not a complete shopping list.
Only one filter is installed; the other two stay at the station.

Before producing the grouped vacuum-assembly order, finish these together:

1. Exact roller-end/working-length geometry, pair spacing, motor/transmission,
   supports and dedicated tool driver. Use an adjustable printed cassette; do
   not assign an arbitrary roller RPM or reuse the slow wheel motors by default.
2. Bin/filter/blower 3D placement, clean-air seals, cassette float, service access,
   10 mm transitions and passive core pockets within 275 × 275 × 180 mm.
3. Edge-brush motor and consumable, 24 V source, local controls, sensors, harness,
   mounts, gaskets, fasteners and station-air interfaces.

After that integration, check real pickup, hair wrap and filter loading on the
assembled cleaning module. A separate blower characterization rig is not required
by this selection. No new owner question is needed for this selection pass.
