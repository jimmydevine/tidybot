# Complete EDF bench purchasing list

**DEFERRED — NOT A CURRENT ORDER, 2026-09-05.** The owner rejected the approximately
$825 fixture cost and has since deferred all lift work. Current work is
[core and ground modules](../../../docs/GROUND_MODULE_DESIGN.md), establishing
their dimensions and measured masses. This package is retained for reference.

Prepared 2026-09-05 for the owner's **single DD 70 mm EDF, existing 3S battery,
80 A Classic ESC, wattmeter and AWS scale**. This is the consolidated purchase
package for the first limited-current thrust experiment. Buy the listed quantities
only if this deferred experiment is resumed, deducting items already in inventory. Pack quantities include assembly
spares; they are not all installed simultaneously.

**Scope:** begin at the proposed 20 A ceiling. A later 40 A operator stop is
conditional on initial electrical/thermal checks. The meter's adopted continuous
rating is 50 A. This package does not authorize full throttle or a full-current
4S test. A fuse is not an automatic current limiter.

The fan is already bolted into the fitting v2 cradle. The owner can cut wood and
has no shaft or bearings. No additional inventory answers are needed to use this
list. Connector uncertainty is covered by both mating genders and both likely
phase-bullet sizes. Check actual polarity and fit during assembly.

This is a **procurement specification**, not a completed or load-validated stand.
The selected interfaces below replace the earlier unspecified pivot hardware.
The detailed lever joints, stop setting and shield installation still require
assembly drawings and unpowered checks before a powered run. Standard stock and
fastener reserves are included for that work; there are no custom machined parts
to order. The existing cradle STL does not need another revision for cables-up use.

## Budget and order file

[hardware.csv](hardware.csv) contains every line below, ownership status,
quantities, source links and cost allowances. Prices are USD before shipping/tax.
goBILDA and TST-20 prices are published prices checked on 2026-09-05; other amounts
are **planning allowances, not quotations or stock guarantees**. Buy new parts
from a supplier able to identify the manufacturer and exact model, particularly
the high-current disconnect and fuse holder. Do not silently substitute a similar
looking switch based only on its continuous-current label.

The CSV now distinguishes `deferred`, `deferred_if_missing`, and `owned`. These
preserve the earlier inventory/cost distinction without an active buy status. Purchase
totals and major cost groups are in [purchase_totals.md](purchase_totals.md).

## Already owned — retain

| Quantity | Item | Use / condition to check |
|---:|---|---|
| 1 | DD 70 mm, 12-blade D2842-3400KV-4S EDF | Existing balanced assembly; no replacement rotor or motor required |
| 1 | Printed retaining_cradle_v2 | Installed underneath, cable exit up |
| 1 set | Installed M3 ear bolts and nuts | Nominal design uses 2 × M3 × 20, 4 × small 6 mm OD washers, 2 × locknuts; actual washer/nut details remain to inspect |
| 1 | RC Electric Parts 80 A Classic ESC | Published 2–6S, 5.5 V BEC, XT90 input, 4 mm phase connectors; verify actual revision/condition |
| 1 | Zeee 3S 5200 mAh XT60 LiPo | Initial test battery; inspect and check individual cells |
| 1 | Tenergy balance charger and existing supply | Exact model unconfirmed; use LiPo balance mode, 3S, initially 3.0 A as described in the test brief |
| 1 | KREATORDIRECT wattmeter | Use 50 A continuous planning limit; terminate its bare SOURCE/LOAD leads |
| 1 | AWS SC-2kg scale, 100 × 100 mm platform | Retain with the 2:1 lever; calibration and usable gross-load range still to establish |
| 1 set | TAZ 6, soldering/crimping tools, multimeter, drill/drill press, wood-cutting tools | No lathe, mill, shaft machining or bearing press assumed |

## Order: matched pivot components

All bores below are **8 mm round**, including the hubs. An 8 mm REX hub is a
different part. Keep the 200 mm shaft at its purchased length.

| ID | Order quantity | Part / manufacturer link | Unit USD | Purpose |
|---|---:|---|---:|---|
| P01 | 1 | [goBILDA 2100-0008-0200](https://www.gobilda.com/8mm-shaft-stainless-steel-200mm-length/), stainless round shaft, 8 × 200 mm | 4.99 | Pivot shaft; select the 200 mm variant |
| P02 | 2 | [1602-0032-0008 pillow block](https://www.gobilda.com/8mm-bore-1-side-2-post-pillow-block-24mm-height/) | 7.99 | Bought bearing assemblies; 24 mm axis height, two M4 mounting threads on 32 mm centers |
| P03 | 2 | [1310-0016-0008 Hyper Hub](https://www.gobilda.com/1310-series-hyper-hub-8mm-bore/) | 7.99 | Clamp two moving lever cheeks to the shaft; pinch hardware included |
| P04 | 2 | [2910-0921-0008 clamping collar](https://www.gobilda.com/2910-series-aluminum-clamping-collar-8mm-id-x-21mm-od-9mm-length/) | 4.99 | Axial retention at the outside of the two bearings |
| P05 | 1 pack of 12 | [2807-0811-0500 shims](https://www.gobilda.com/2807-series-stainless-steel-shim-8mm-id-x-11mm-od-0-50mm-thickness-12-pack/), 8 ID × 11 OD × 0.5 mm | 2.69 | Clearance at rotating bearing inner races |
| P06 | 1 pack of 4 | [1522-0010-0040 spacers](https://www.gobilda.com/1522-series-8mm-id-spacer-10mm-od-4mm-length-4-pack/), 8 ID × 10 OD × 4 mm | 2.99 | Additional shaft spacing as needed |

Pivot order subtotal: **$52.61**. Do not clamp a collar against a stationary
bearing housing or preload the two bearings together. Fit only enough shims and
spacers to clear the stationary parts while retaining small axial freedom.
Small-angle friction must be checked with known loads; these bearings are not a
guarantee of scale accuracy.

## Order: wood, structural hardware and barriers

Generic items can come from a local hardware/plastics supplier. Sizes are buying
specifications. The blank allocation is not an instruction to cut every piece
before the assembly drawing is complete.

| ID | Order quantity | Specification | Allocation |
|---|---:|---|---|
| S01 | 1 panel | Sound flat plywood, nominal 18–19 mm, at least 610 × 1220 mm (2 × 4 ft) | Base 600 × 320; moving board 120 × 140; two lever-cheek blanks 300 × 140; bearing supports/caps, crosspieces and gussets from remainder |
| S02 | 10 m total | Straight timber battens, approximately 25 × 38 mm | Bracing, joint cleats, base feet and separate barrier frame; includes cutting allowance |
| S03 | 1 kit | M4 socket screws: **25 each of 20, 25 and 35 mm**; **50 M4 locknuts; 100 M4 washers** (about 9 mm OD) | Hubs, bearing feet, cradle-to-board, stops/frame fittings; choose length against actual material/thread depth |
| S04 | 1 kit | M6 bolts: **25 × 40 mm, 50 × 50 mm, 25 × 70 mm**; **100 M6 locknuts; 200 M6 large washers** (about 18 mm OD) | Through-bolted timber cleats, paired cheeks, support feet, gussets and stop bridge; reserve included |
| S05 | 1 kit | **1 M6 × 200 mm threaded rod, 2 M6 coupling nuts, 2 M6 acorn nuts, 2 fully threaded M6 × 60 bolts, 12 plain M6 nuts** | Adjustable scale contact and two travel stops; plain nuts permit jam-locking |
| S06 | 1 box of 100 | Approximately 4 × 40 mm wood screws, plus wood glue | Barrier frame and supplementary cleats; critical moving joints use through-bolts |
| S07 | 4 | Bench/F clamps, at least 150 mm jaw opening | Secure fixed base and independent barrier frame; never clamp the moving lever |
| S08 | 3 panels | **Polycarbonate**, 6 mm thick, 600 × 600 mm; supplier-cut | Stock for two side barriers and an overhead panel; separate frame, inlet/outlet kept clear |
| S09 | 1 kit | **32 M4 × 50 bolts, 32 M4 locknuts, 64 wide M4 washers (about 12–16 mm OD), 64 nylon washers** | Barrier panels through the approximately 25 mm batten thickness; spread load, allow thermal clearance and avoid overtightening |
| S10 | 1 | Feeler-gauge set covering about 0.05–1 mm | Set/check free travel and stop gaps during unpowered calibration |

No additional metal angle brackets are assumed: the fixture uses timber cleats,
plywood gussets and through-bolts. M6 × 50 accommodates nominal two-layer 18–19 mm
plywood joints; M6 × 70 accommodates a 38 mm batten plus one plywood layer. Exact
bolt projection and washer stack must be checked before tightening.

The polycarbonate is an **access/debris barrier material allowance**, not a
certified rotor-burst enclosure. Panel thickness alone does not establish
containment; frame, gaps, separation and the actual rotor energy matter. Its final
installation must keep the operator outside the rotor plane and keep people/dogs
out of the open inlet/exhaust paths. Do not install a fine mesh immediately at
the fan and then call that an unobstructed thrust measurement.

## Order: throttle, power interruption and harness

| ID | Order quantity | Specification / link | Use |
|---|---:|---|---|
| E01 | 1 | [ProtoSupplies TST-20](https://protosupplies.com/product/servo-tester/) manual servo tester | $2.95 published; manual mode, powered from the ESC's 5.5 V BEC |
| E02 | 1 | **Albright ED125-1 emergency DC disconnect**, complete knob, terminal and mounting hardware; [manufacturer](https://www.albrightinternational.com/products/ed125/) | Budget $150. Direct main-power interruption, reachable from the operator position |
| E03 | 1 | **Littelfuse 04980921GXM5** inline MIDI fuse holder with cover and M5 terminal hardware; [datasheet](https://www.littelfuse.com/assetdocs/midi-498-il-datasheet?assetguid=%7B2a144dfe-6adb-4d21-9e0f-305f0a0de6ed%7D) | In battery-positive lead near the pack |
| E04 | 2 of each | **30 A and 50 A MIDI bolt-down fuses**, Littelfuse 0498030 / 0498050 families, 32 V DC; [datasheet](https://www.littelfuse.com/assetdocs/midi-32v-bolt-down-series-data-sheet?assetguid=b55e8034-180d-40f6-a0a7-bebc2d4a94f5) | Initial 30 A fuse for the 20 A stage; one spare each. 50 A only for a subsequently qualified 40 A stage |
| E05 | 2 m each color | **10 AWG flexible copper silicone wire**, red and black | Stock for fixed DC harness; installed leads kept short, not a four-metre battery extension |
| E06 | 1 m each color | **12 AWG flexible copper silicone wire**, red and black | Three short phase-adapter leads, flexible loops near pivot and short XT60 pigtails |
| E07 | 3 mating pairs | Genuine **XT60**, both contact genders, housings included | Battery/meter/harness connections and spare |
| E08 | 2 mating pairs | Genuine **XT90**, both contact genders, housings included | Match listed ESC input without cutting the battery lead; spare included |
| E09 | 6 pairs of each size | **3.5 mm and 4.0 mm bullet connectors**, male and female, insulating sleeves/heat-shrink | Three phase adapters; both sizes cover the EDF/ESC listing discrepancy and a setup motor |
| E10 | 6 of each | Crimp ring terminals for **10–12 AWG copper**, **M5 and M8 stud holes** | Fuse holder and ED125 main terminals; use a die suitable for these lugs |
| E11 | 1 set | Red/black adhesive heat-shrink assortment, insulating terminal boots, split sleeve | Cover every lug, bullet and soldered joint; no exposed unused live contacts |
| E12 | 1 | Insulating enclosure, approximately **200 × 150 × 100 mm**, removable lid, with cable glands and mounting screws | Enclose fuse/disconnect terminal backs; external knob stays accessible. Cut/drill after receiving switch |
| E13 | 1 | **1 m, three-wire 22 AWG servo extension**, JR-compatible keyed housing | Move throttle control to operator side; verify S / + / −, never feed pack voltage into tester |
| E14 | 2 | **3S four-pin JST-XH balance extensions**, about 300 mm | One for cell monitor, one available for charging; verify pin sequence |
| E15 | 1 pack | At least **20 screw-mounted cable clips/P-clips, 50 cable ties, 2 battery straps** | Fixed harness strain relief; free phase loops must not bias the lever |
| E16 | 1 | **300 mm three-wire servo patch lead with socket contacts at both ends**, 22 AWG | Connect tester output pins to BG-8S pulse-test input pins during setup; vendor gender names vary |

The [ED125 data](https://www.albrightinternational.com/products/ed125/) distinguish
its continuous rating from DC breaking capability. It is intended for emergency
interruption/no-load isolation, not routine switching under load. Normal shutdown
is minimum throttle, wait for the rotor to stop, then isolate. Its M8 main-terminal
and M5 mounting hardware are shown in the [manufacturer's parts sheet](https://www.albrightinternational.com/wpcms/wp-content/uploads/2019/05/ED125-Spares.pdf).
Order the complete assembly, not a bare replacement knob. A normal low-current
mushroom button cannot substitute directly in this main-power circuit.

Electrical order, positive side:

```text
3S battery XT60 -> MIDI fuse -> ED125 -> wattmeter SOURCE
wattmeter LOAD -> ESC XT90 -> three phase adapters -> EDF
```

Negative follows battery -> wattmeter SOURCE -> wattmeter LOAD -> ESC. The ED125
switches the positive path. Use recessed live battery-side contacts and verify
polarity end to end with the multimeter before plugging in the pack. Keep the
unverified wattmeter auxiliary lead insulated and unused. The fuse is backup
fault protection: its time/current curve does not enforce a 20 A or 40 A ceiling,
and it is not proof that every component survives every fault.

Use short 12 AWG pigtails where the XT60 solder cups require them; do not force
10 AWG wire into undersized cups or remove strands to make it fit. The existing
meter also has 12 AWG leads. These short sections remain subject to the same
initial current and temperature checks as the rest of the path.

Keep the battery, meter, ESC and disconnect on the **fixed** structure. Place
the operator controls beside the inlet end and outside the rotor plane, with
the barrier between operator and fan. Use short DC wiring and extend the servo
lead. Give the motor wires loose flexible loops close to the pivot, without
contacting the fan or stops; calibrate with the final wire routing installed.

## Order: measurement and calibration

| ID | Order quantity | Specification / link | Use |
|---|---:|---|---|
| I01 | 1 | **ISDT BG-8S** individual-cell checker with configurable per-cell low-voltage alarm; [manufacturer manual](https://www.isdt.co/down/pdf/BG-8S_en.pdf) | Connect through 3S balance extension; budget $45. Direct-shop listing was sold out at checking, so source the same model through an RC dealer |
| I02 | 1 | **SkyRC Thermologger Duo SK-500043**, including its **two K-type probes and CR2450**; [manufacturer](https://www.skyrc.com/thermologgerduo?from=banner) | Budget $40; fixed ESC-case and battery-surface temperatures. Requires a compatible phone/Bluetooth app |
| I03 | 2 | **500 g calibration masses**, M1 class or better | Known scale and lever loads; budget $15 each |
| I04 | 1 | **0–5 kg spring pull gauge**, graduations no coarser than 0.05 kg, continuous reading | Horizontal pull through the fan thrust line; check against known masses before use; budget $20 |
| I05 | 1 kit | **2 m low-stretch cord, 2 small shackles, 2 M6 eye bolts with 4 nuts/4 washers, small hanging cup/hook** | Apply known loads to the lever calibration point and connect pull gauge; include carrier mass in load |

The BG-8S also reads RC pulse width during unpowered setup, so no oscilloscope is
required just to check tester endpoints. During the fan test, use it as the cell
monitor; it is not the throttle controller or an ESC cutoff. Do not start its
balancing or USB power-bank functions during measurements. Its manual documents
alarm settings on page 7 and pulse measurement on page 8; it can use the balance
connection for this 3S pack. Cross-check voltages against the existing multimeter.

Attach temperature probes only to electrically insulated, stationary surfaces.
The purple outer motor bell rotates: do not attach a probe or tape to it. The
optional-to-buy IR thermometer below is for checks after stopping, not viewing
through a polycarbonate screen. Surface temperature is not winding temperature.

## Buy in the same order if missing from the shop

These are part of the complete preparation list, not presumed existing inventory.

| ID | Quantity | Item |
|---|---:|---|
| C01 | 1 | Main charge lead: **4 mm banana plugs to the battery's mating XT60**, at least 16 AWG; no unused exposed branches. Reuse an existing correct lead |
| C02 | 1 | Small ordinary **3S brushless motor, about 1000–1500 KV**, with mounting cross and screws, **no propeller**; e.g. a basic 2212-class motor |
| C03 | 1 | IR thermometer, roughly −20 to 150 °C or wider, with batteries; motor/connector surface checks after shutdown |
| C04 | 1 | Phone clamp/tripod, plus an existing phone capable of filming the scale and meter; a second phone can display the logger if available |
| C05 | 1 set | Eye protection and hearing protection |
| C06 | 1 | LiPo charging bag/container suitable for the pack, and a noncombustible tray/surface; neither makes unattended charging acceptable |
| C07 | 1 kit | 200 g PETG reserve, solder/flux, polyimide tape, small adhesive rubber feet, spare instrument batteries |
| C08 | 1 kit | Drill bits **3.5, 4.5, 6.5 and 10 mm**, small step bit for enclosure/cable glands, metric hex keys/spanners, countersink/deburring tool |
| C09 | 1 kit | **4 × M3 × 20, 4 × M3 × 12, 8 M3 locknuts, 16 small M3 washers (3.2 ID × 6 OD × 0.5 mm)** |
| C10 | 1 kit | Modest-load meter check: **10 Ω, 50 W, 1% aluminium-housed resistor**, approximately **100 × 100 × 3 mm aluminium plate**, heat-transfer compound |

C02 lets the [Classic ESC's throttle calibration](https://www.rcelectricparts.com/classic-esc-user-guide.html)
use motor tones with an unloaded, secured motor while preserving the EDF's
balanced rotor. Borrowing any suitable existing unloaded brushless motor avoids
this purchase. Its mounting screws are part of the motor purchase; the M3 stock
also supplies small fixture joints. Do not run this bare motor loose on the bench.

C10 checks the wattmeter at a modest known load, not propulsion current: mount
the resistor to the plate with M3 hardware, use the existing multimeter to measure
its cold resistance and load voltage, then compare approximately I = V/R with
the wattmeter. At 12.6 V a nominal 10 Ω load draws 1.26 A and dissipates 15.9 W.
Use brief checks, stop on heating and let it cool; the nominal 50 W part rating
does not establish that this small plate can dissipate 50 W continuously. This
is a gross-error check, not a traceable calibration at 40 A. Keep the resistor
and plate away from the battery and wood. Do not put EDF current through the
ordinary multimeter's current input.

The charger itself and supply are retained, subject to identifying/checking them
before use. Do not order a blind replacement supply with an assumed connector or
polarity. A missing, unsuitable or failed charger/supply would be a fault-driven
replacement outside this fixture list.

## How the selected hardware fits the stand

The design keeps the existing **120 mm thrust arm / 240 mm scale arm**. Nominal
heights are measured above the fixed base, not the floor:

| Interface | Procurement / assembly constraint |
|---|---|
| Shaft | 8 × 200 mm bought stock, replacing the earlier 180 mm allowance; no shaft cutting |
| Bearing centers | Start at y = ±65 mm; final axial stack must leave collars and lever cheeks clear |
| Bearing feet | 24 mm below shaft center. With pivot at 180 mm, mounting shelves are **156 mm above base top** |
| Fixed supports | Two braced plywood uprights with horizontal bearing caps; for 18 mm caps, upright height is 138 mm. Recalculate against actual plywood thickness before cutting |
| Moving lever | Two plywood cheeks bolted to the two clamping hubs, connected by through-bolted crosspieces/cleats and gussets; no screw-only end-grain torque joint |
| Fan board | Top **246 mm above base top**, keeping fan axis at 300 mm. Nominal 18 mm board underside is 228 mm, or 48 mm above pivot |
| Fan-to-board joint | Existing 36 × 92 mm cradle hole pattern; 4 × M4 × 35 with 8 washers/4 locknuts for 18 mm plywood |
| Hub/foot screws | Start with M4 × 25 through nominal 18–19 mm plywood; use 20 mm or washers if needed to avoid bottoming. Confirm thread engagement and hole pattern from delivered parts |
| Scale contact | M6 adjustable rod with rounded cap and a smooth load-spreading pad centered on the scale platform |
| Stops | Two M6 adjustment screws on fixed bridge/cleats, one for each travel direction. Neither touches the moving lever in the measurement range |
| Cable transfer | Flexible phase loops near shaft; all heavy electronics fixed |

The 1800 g **gross** scale working stop is a proposed measurement limit; tare does
not restore capacity. Set travel stops using actual scale deflection and known
loads. If the scale cannot provide clearance between useful travel and overload,
the stop arrangement/force sensor must change. No fixed guessed gap is specified.

The blank stock above covers a base, two lever cheeks, bearing caps/supports,
crosspieces, gussets and stop bridge. Keep offcuts until assembly is complete.
Metric 18 mm and US 3/4-inch plywood are not assumed equal; measure thickness
once on receipt and use it in the cut/drill drawing. That adjustment needs no
new specialty hardware order.

## Deliberately separate: later 4S or higher-current experiment

The existing 3S stage can measure thrust versus electrical power over its allowed
range. It cannot establish the fan's maximum advertised 4S thrust. A subsequent
full-current stage would need a **4S pack**, a **documented ≥100 A continuous
measurement path above 16.8 V**, and an appropriately rated battery connector,
harness and fuse selection. The existing XT60 pack and 50 A-continuous meter
must not be carried into that stage merely because their burst labels are high.
ESC cooling/current limits and the stand/guard also need review against results.
Those are a different experiment, not small parts omitted from this order.

An RC radio, receiver, flight controller, flight battery array and robot module
hardware are not required for this static test. Automatic logging/current cutoff
can be a later instrumentation upgrade; this initial test is attended and
manually commanded.

## Next deliverable

The current deliverable is the core and ground-module design, linked above.
Stand assembly/cut/drill drawings, a powered protocol and propulsion comparison
are deferred. No purchase from this list is needed for the ground phase.
