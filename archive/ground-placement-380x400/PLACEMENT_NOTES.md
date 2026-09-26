# First full ground assembly placement

2026-09-06. The middle electronics section retains the name **core**. This
placement combines it with the everyday vacuum bottom and cap. Propulsion,
flight sizing and the EDF stand remain deferred. The main robot stays outside
the 50 mm sofa gap; the separate reaching bottom remains in the ground roadmap.

Open the [offline placement viewer](../design/ground/output/ground_layout.html).
It contains vacuum, core, cap, side and service views. The
[coordinate report](../design/ground/output/ground_report.md) records each
reservation, its source and the geometric checks. For CAD inspection use the
[FreeCAD model](../design/ground/output/ground_placement.FCStd) or
[STEP model](../design/ground/output/ground_placement.step). These contain reference
solids and wire outlines for reserved spaces, not printable robot parts.

## Envelope and arrangement

All positions, mating planes and allowances are **design proposals**. Owner
measurements and manufacturer component envelopes constrain this first layout;
they do not validate the completed assembly.

| Proposed dimension | Value | Consequence |
|---|---:|---|
| Main body footprint | 380 × 400 mm | About 15 × 15.7 inches; leave room for the long head, drive mounts and rear drawer |
| Floor to bottom/core mate | 110 mm | Clears the 90 mm wheels and the upright blower reservation |
| Core height | 55 mm | Battery, power and Pi trays beside one another |
| Core/cap mate / cap top | 165 / 175 mm above floor | 10 mm cover envelope, not a solid 10 mm panel thickness |
| A1 reference top | 230 mm above floor | Scanner sits on core-fixed supports above the cap |
| Head reservation | 324 × 72 × 78 mm | Retains the 35 mm roof reference; extra height reserves powered drive and air-path development |
| Side-brush sweep placeholder | 70 mm diameter | Protrudes 9 mm left and 16 mm forward; moving outline becomes 389 × 416 mm |

The side brush's actual sweep is unmeasured. Its placeholder clears the roller
envelopes in this proposal; a larger brush will require repositioning or more
room. The 254 mm reported roller length is not a verified cleaning swath. The
short pair remains an alternative in the separate head study.

Coordinates use x left to right, y front to rear, z above the floor. Wheel centers
are at **(17, 181, 45)** and **(363, 181, 45) mm**. The head begins at
**(28, 55, 0) mm**, ahead of both wheel envelopes. The 25D motor bodies extend
inward from the wheels; purchased hubs and replaceable mounting plates occupy
the surrounding drive bays. Their shaft and wheel interfaces still need fitting.
The motor envelope is the leading Pololu #4847 candidate, not a purchase decision.
[Manufacturer dimensions](https://www.pololu.com/product/4847/specs)

These floor-relative heights describe the vacuum configuration. Other complete
bottoms may declare different heights and outlines while using the same core
mate. The station must accommodate their pickup heights and separation travel;
the vacuum's 110 mm datum does not freeze every future bottom's height.

A front support and two rear support reservations include caster swivel space.
They need compliant mounts and controlled preload so five contacts do not unload
the drive wheels on uneven floors. A contact outline alone does not establish
traction or stability. Loaded center of gravity cannot be calculated until the
assemblies and debris allowance are weighed.

## Vacuum bottom and service access

The proposed path is **front rollers → central duct → rear bin → left-side
filter → clean plenum → upright blower → rear diffuser**. The wheel H-bridge
sits above the dirty-air corridor on a separating deck. The bottom MCU and
dedicated roller, side-brush and blower power stages sit to the bin's right.
They travel with this complete bottom during station swaps.

The bin/filter drawer occupies **190 × 156 × 93 mm**, including the side filter
holder and rear evacuation-port allowance. A proposed **140 × 110 × 65 mm** clear
debris region is **1.001 L geometrically**. Retain the **0.5–0.75 L usable target**
to allow for freeboard, inlet features and hair collection behavior. Actual
capacity, pickup and emptying performance remain untested.

The filter's 136 × 76 mm broad face stands vertically along the drawer's left
wall. Reserve 19 mm across that face for the body and unknown exact tab location,
with a separate holder and seal allowance. The blower is beside the drawer so
it does not obstruct rear removal. Its **33 × 97 × 95 mm rotated envelope** fits
upright, with its axial intake toward the filter and tangential outlet toward
the rear. The 35 mm plenum reservation gives room to transition between the
filter and blower intake. Exact adapters and diffuser area are still to design.
[CBM mechanical drawing, page 5](https://www.sameskydevices.com/product/resource/cbm-97b.pdf)

For manual bin/filter maintenance, first retract the clean-plenum sealing face
**3 mm left**, then slide the complete drawer **200 mm rearward**. The inlet
uses an intended face seal that separates in this direction. Once the drawer is
out, its filter holder opens upward and exposes the tab. This avoids trying to
pull the filter through the fixed blower. The sealing-face cam and drawer lock
are reserved functions, not finished mechanisms.

The rear emptying-port allowance stays on the drawer. Normal automatic emptying
uses this port with the onboard blower off, an intentional makeup-air path via
the head, and an isolation feature between the filter/plenum and blower.
Sliding the drawer out is a maintenance action, not a required cleaning-cycle
step. Hair bridging, valves and leak-tight seals need development together.
The CBM requires protected DC supply and must not use power/ground PWM.
[Manufacturer operating instructions, page 6](https://www.sameskydevices.com/product/resource/cbm-97b.pdf)

## Core and cap

| Reservation | Position and maintenance |
|---|---|
| Battery tray | Left, near the wheel line; 90 × 170 × 38 mm space including restraint and leads; 150 mm leftward extraction |
| Power tray | Center, beside battery; protection, regulators, distribution and current sensing |
| Pi tray | Right; 110 × 115 × 38 mm for Pi 4, cooling and connector bends; 150 mm rightward extraction |
| Core supervisor | Behind power tray; separate from the bottom MCU |
| Additional navigation | Front interior bay plus outward camera/near-field bay; sensor choice and field of view open |
| Station pickup rails | Core sides, y=80–320 and z=157–165 mm; above both sliding trays |

Keep the owned **3S pack**. Its modeled 132 × 43 × 25 mm pack envelope is a
seller reference retained in the battery record, not an owner measurement. The
tray must be checked against the actual pack, leads and connector before printing.
The Pi's 85 × 56 mm PCB footprint is only part of its tray requirement; the cooler,
ports and wire bends must fit too. One-millimeter PCB sheets in the model are
drawing conventions, not completed board-height claims.
[Pi mechanical drawing](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-mechanical-drawing.pdf)

The A1 stays on a pedestal fixed to the core. The cap has a proposed
**107 × 81 mm through-opening**, clearing the **96.8 × 70.3 × 55 mm A1 family
reference** during a straight upward removal. With its base at the cap top,
the other proposed structure is below the scanner body; the actual optical
scan plane and owned revision still need confirmation. A **70 mm cap lift**
puts its underside 5 mm above the scanner top before lateral transfer. An
optional display remains unselected and must stay below the scan plane.
[SLAMTEC family dimensions](https://www.slamtec.com/cn/lidar/a1spec)

## Mates and automatic exchange

Reserve four **20 × 20 mm corner joint zones** at minimum corners
**(8,8), (352,8), (8,372), (352,372) mm** on both mating faces. A proposed round
locator near (18,18) and slotted locator near (362,382) share diagonally opposite
zones; they are not drilled-hole specifications. Distinct top/bottom keys,
compression seats and station-operated retention remain to detail. Guides and
locks must carry loads through the core frame rather than through connectors.

The bottom connector pocket is front-center, away from rear dirt servicing.
The low-power cap connector pocket is front-right. Both show combined mating
space, without a selected connector, pinout or live-mating permission. Separate
seated, locked and identity detection remain required. Frame members and access
openings must respect the shown service paths.

The initial station motion allowance avoids lowering a bottom through the room
floor. Dock onto a tray whose top is **40 mm above the floor**, capture the core
from its sides, disable/isolate the bottom actuator supply, and release the
bottom locks only after both sections are supported. Lower the tray to **10 mm**:
the resulting **30 mm separation** clears the proposed **13 mm mating projection**
by **17 mm**. Then translate the supported bottom rearward **440 mm**. Reverse
the sequence to install and verify the next bottom before enabling its actuators.

The tray footprint reservation is **410 × 440 mm**, with **80 mm access on each
side of the body** for station support/release mechanisms. These are movement
allowances, not a cabinet footprint: ramp, actuators, grippers, chargers and
storage for all modules remain to place. The station must also support the core
when a bottom is absent. Battery/Pi manual servicing takes place off the station
or with its fingers withdrawn; those are different operating states.

## Build work following placement

The [component ledger](../config/ground_components.csv) remains the consolidated
assembly requirements list. Positions link back to its rows; spare rollers, all
owned Pis and alternate motors are not silently added to carried hardware.
Measured component and complete-section masses remain blank.

Next detail the **core-to-bottom joint sample and everyday head drive** against
this placement. Group the remaining fit information into one measurement sheet:
roller working length and both drive/support ends, side-brush sweep/hub, actual
battery with leads, wheel hub variant and blower mounting/access. Then select
the associated bought mounts, couplers, drives, connectors and protection as a
compatible set and complete the fastener/wiring quantities and costs before an
order. No additional measurement question is being asked in this placement turn.

Four-way panel segmentation allows nominal **205 × 215 mm** blanks including
15 mm join allowance, within the preferred 250 mm print span. This is a panel
packaging check, not a joint-strength calculation or a claim that every future
part already fits the printer. Through-bolts, stock metal spacers and printed
carriers remain the construction direction; no new machining process is assumed.

Regenerate with `python3 design/ground/place_modules.py`, then run
`python3 -m unittest discover -s design/ground -p 'test_*.py' -v`.
Export CAD using `freecadcmd design/ground/export_placement.py`. None of these
commands imports the deferred flight model.
