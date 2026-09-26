# Fixed drive mounts — N comparison

**Budget update:** the [owner's 4.5 kg transfer limit](MASS_BUDGETS.md) includes
the core, battery and loaded bottom, excluding lift. After cap removal, N still
exceeds it by 666 g vacuum / 204 g mop at maximum modeled contents. The mass
saving below is insufficient by itself; further redesign is required.

2026-09-14. A dimensioned alternative replaces K's separate suspension pods
with two fixed motor supports, one common crossmember and two rail cleats.
**Potential saving: 230 g per floor robot. This is not yet an adopted design.**
It preserves the motors, 72 mm wheels and rear caster reference; the cleaning
head must accommodate the additional body movement on thresholds.

[Interactive comparison](../design/system/output/fixed_drive.html) ·
[Calculated report](../design/system/output/fixed_drive.md) ·
[Itemized replacement mass](../design/system/output/fixed_drive_mass.csv)

| Complete assembly, with cap | M comparison | N comparison |
|---|---:|---:|
| Vacuum, including 150 g debris | 5.316 kg | 5.086 kg |
| Mop, including 350 g tank water and 50 g pad water | 4.954 kg | 4.724 kg |

Both cases retain the same 753 g cell-pack reference, cartridge/receiver,
electronics and all cleaning hardware. These are planning estimates, not
measured weights. The lift top is not included. The new scope totals **259 g**
against **489 g** for both K pods. It includes stock, two catalog motor
brackets, fastener sets, compression sleeves and a 20 g completion reserve.
The existing **225 g frame** and all M head/lift/riser allowances remain.
No savings from possible overlapping allowances are credited.

## Construction and load path

Coordinates remain X left-to-right, Y front-to-rear and Z above the nominal
floor, in millimetres. The motor axes remain Y=105, Z=36. Wheels remain inside
X=2–26 and 249–273. No motor, wheel or hub purchase changes follow from N.

| Part | Nominal geometry | Fabrication |
|---|---|---|
| Two motor support angles | 52 mm wide; 37.5 mm horizontal leg; 48.2625 mm vertical leg; 4.7625 mm wall | Cut from 2 × 2 × 3/16 inch 6061-T6 angle, trim legs and drill |
| Crossmember | 219 mm long; 12.7 mm square; 1.6002 mm wall | 1/2 inch square × .063 inch 6063-T52 tube; cut/drill |
| Two rail cleats | 22 mm long; 15 mm legs; 3.175 mm wall | Trim architectural angle; exact product/corner radius pending |
| Compression sleeves | Steel, 6 mm OD / 4.3 mm ID, nominal 9.4996 mm long | Cut to actual tube cavity; do not force a nominal-length spacer into tolerance stock |
| Motor brackets | Pololu 2676 | Retained catalog interface and flush motor screws |

The large angle's **6.35 mm inside radius is included**; it clears the motor
and its bracket in the nominal model. The shelf top stays Z=21.5. The tube
occupies X=28–247, Y=130–142.7, Z=52.3–65. It spans above the central dirty-air
duct and below the battery. Its 219 mm length is within the 275 mm footprint.
The new stock remains inside the existing body allocations and does not raise
the nominal sensor/cap stack. Tilted clearance over actual terrain remains
an operating-envelope check.

Load path: wheel → motor output support → catalog bracket → fixed angle →
crossmember → cleats/side rails → module structure. The old pivot, springs,
collars, bearing blocks and travel stops are absent. The inner H rail routes
terminate at the new crossmember rather than running through it; their joints
need detailing. Their old mass budget is retained.

The calculation keeps H/K's 150 N vertical and ±25 N fore-aft wheel cases.
It includes the moment from the wheel being outboard of the motor mount:
the foot-bolt columns see approximately +303/−153 N, not 75/75 N. This matters
for the bracket, bolt retention and plate thickness. The 3/16 inch angle and
small square tube pass the stated local section screens; no whole-assembly
strength approval follows from those checks.

Beam torsion assumes rotational restraint at the two ends. Actual cleat/rail
stiffness, screw heads/nuts, bearing and pull-out, fatigue and the motor shaft's
radial-load capability remain to verify. The CAD omits most fastener heads and
tool access, although the mass ledger includes their sets. Existing cassette,
caster retention and complete chassis joints remain unfinished too.

Stock cutting, drilling and deburring are needed. No lathe, mill or sheet-metal
brake is assumed. Supplier cutting is an option; confirm a practical trimming
and spacer-making method before fabrication. These files are comparison CAD,
not print-ready parts or an order list.

## What the terrain calculation changes

The fixed drivetrain forms a three-point support with the rear caster. That
allows chassis attitude to change without independently suspended wheels,
provided all supports retain positive load. It does not guarantee traction,
impact isolation or cleaning-head contact.

Across sampled 4/10 mm levels and eight caster headings:

- Required head pitch reaches **5.22°**, roll **2.32°**.
- Vacuum head translation spans **−8.4 to +10 mm**; mop **−6.0 to +10 mm**.
- These exceed M's −2 to +10 mm travel and ±1.5° tilt allocation.

The model recalculates gravity-direction support reactions and moves the head
mass to each requested pose. It assumes a constant target contact force; it
does not demonstrate that a passive spring/linkage supplies that force.
It uses sphere-radius wheel reach, a nominal caster contact point and a head
reference plane. A full head crossing a sharp edge, terrain between contact
points, descending transitions, tire compression, friction and dynamic impacts
still require analysis/testing. The sampled range is a design input, not a
guaranteed sufficient travel specification.

## Mop placement issue

With the present rear-heavy mop layout, raising the head to cross a 10 mm
sharp edge gives a caster-climb friction requirement of approximately **0.65**.
That exceeds all three wet-friction sensitivity values (0.20/0.35/0.50).
Actual tire grip is unmeasured. Lower robot mass alone does not fix a poor
front/rear load split: much of this requirement is a load-fraction ratio.

At the illustrative value 0.35, the loaded mop CG would need to move from
Y≈139.5 to **Y≤126.2 mm**, about **13.3 mm forward**, with the present axle and
caster. Investigate front-mounted water storage or a mop-specific drive-axle
location. These are placement alternatives, not completed tank/mount designs
or additional credited savings. Water capacity and dosing performance stay in
scope. Independently suspended wheels would not by themselves fix this static
caster-load problem either.

The 10 mm driven-wheel torque screen is below the existing transient motor/
gearbox limits, but above the continuous limit. A short crossing must therefore
remain a transient event; neither the motor calculation nor an unloaded wheel
spin proves wet-floor climbing.

## Decision

Keep N as a mass-reduction candidate and keep K/M as comparison fallbacks.
Do not buy or print new drivetrain parts from this pass. Next, lay out a
passive, positively retained vacuum head for the required motion and reposition
the mop's heavy components. Reconcile their complete mounts before adopting N
or updating the main system mass. A roughly 230 g saving is useful, but the
overall architecture still needs substantial weight reduction.

## Reproduce and inspect

```sh
python3 design/system/fixed_drive.py
python3 -m unittest discover -s design/system -p 'test_fixed_drive.py' -q
freecadcmd design/system/export_fixed_drive_freecad.py
```

The CAD run generated 23 valid local solids, with no nominal new-stock
intersections in the explicitly checked local pairs or retained vacuum/mop
allocations. It does not check every assembly pair or moving head pose.
Eight new calculation tests cover contact heights, uniform floor offsets,
left/right symmetry, beam/couple equilibrium, torsion boundaries and mass
conservation. The complete system suite passes 124 tests. All 208 viewer states
were exercised with a DOM shim and one SVG view was rendered and inspected;
this is not a full browser interaction test.

[Vacuum FreeCAD](../design/system/output/fixed_drive_vacuum.FCStd) ·
[Mop FreeCAD](../design/system/output/fixed_drive_mop.FCStd) ·
[Vacuum STEP](../design/system/output/fixed_drive_vacuum.step) ·
[CAD check scope](../design/system/output/fixed_drive_cad_checks.json)

Sources: [6061 angle dimensions](https://www.onlinemetals.com/en/buy/aluminum/2-x-2-x-0-1875-aluminum-angle-6061-t6-extruded-structural/pid/988),
[6063 square tube](https://www.onlinemetals.com/en/buy/aluminum/0-5-x-0-063-aluminum-square-tube-6063-t52-extruded/pid/20685),
[Hydro 6063 property limits](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6063.pdf),
[Pololu bracket](https://www.pololu.com/product/2676),
[Pololu gearbox/current guidance](https://www.pololu.com/file/0J1829/pololu-25d-metal-gearmotors.pdf).
