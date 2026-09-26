# Retaining cradle v2 — central-ring correction

Status: **owner reports fan mounted to cradle with M3 nuts and bolts**.
Next: [attach the assembly to its moving mounting board](MOUNTING_BOARD.md).
V1 failed because the model omitted the raised ring around the fan housing.
V2 includes the owner's measured ring in the fan model and a local clearance
groove in the cradle. The owner has printed v2 and confirms a perfect fit, including
the ring, on the side opposite the three cables. Use that printed cradle with
**the cable exit facing upward**. The cradle does not clear the cable-exit side.

## Files

| File | Use |
|---|---|
| [retaining_cradle_v2.stl](output/retaining_cradle_v2.stl) | One printable cradle, 48 × 112 × 52.5 mm |
| [Cable-up orientation](output/mounting_orientation.svg) | End-view guide: one cradle underneath, cable exit above |
| [Cradle preview](output/retaining_cradle_v2_preview.svg) | Inspect the central groove, ear shelves and nut windows |
| [Cradle FreeCAD](output/retaining_cradle_v2.FCStd), [STEP](output/retaining_cradle_v2.step) | Editable solid |
| [Assembly preview](output/retaining_mount_assembly_v2_preview.svg) | Fan, ring, cradle, board and M3 hardware |
| [Assembly FreeCAD](output/retaining_mount_assembly_v2.FCStd), [STEP](output/retaining_mount_assembly_v2.step) | Reviewable assembly; do not print the existing fan or metal hardware |
| [Dimension sketch](output/mount_measurement.svg) | Ring and ear positions from the intake face |
| [Board drill template](output/mounting_board_template.svg) | Four holes on the 36 × 92 mm pattern |
| [V2 geometry report](output/mount_verification_v2.json) | Checks and their limits |

## Measured ring and groove

The owner reports **75.5 mm outside diameter, 1.5 mm width along the duct, and
ring center aligned with the mounting-ear hole centers**. The established hole
plane is 37 mm from the intake face, so no further axial measurement is needed.

| Feature | Dimension |
|---|---|
| Ring center from intake face | 37 mm |
| Ring edges from intake face | 36.25–37.75 mm |
| Groove diameter | 76.1 mm: 0.3 mm radial clearance around the ring |
| Groove width along airflow | 2.5 mm: 0.5 mm clearance at each ring edge |
| Groove edges from intake face | 35.75–38.25 mm |
| Plain saddle bore | 74.4 mm, matching the successful local gauge |
| Saddle length along airflow | 24 mm, spanning 25–49 mm from the intake face |

The groove is centered halfway along the saddle, at the ear slots. It is a
0.85 mm radial recess from the plain bore. These allowances are trial print
clearances. The mounting-hole plane, ear shelves, base bolt pattern and print
orientation remain the same as v1. The groove leaves 7.95 mm of material above
the top of the 8 mm-thick base at its deepest point; this is a geometric
measurement, not a strength rating.

## Cable orientation and fit result

The mount uses **one cradle below the fan**. It does not use a second printed
half over the top. Rotate the fan about its axis until the cable exit is at
the top and the ears are horizontal. This uses the side the owner reports fits.
See the [orientation diagram](output/mounting_orientation.svg).

The reported cable-exit area is **6 mm wide × 11 mm high**, between the ears
and on the motor side of the ring. These numbers are recorded as reported;
which dimension follows the duct and the radial protrusion are not established.
The CAD omits the cable geometry; the new diagram shows schematic routing only.

Route leads above the cradle and away from inlet/exhaust, with strain relief
on the moving assembly and a flexible loop where they cross to the fixed ESC.
The cable transition must not pull on the scale lever. Check that routing when
calibrating the complete stand.

The current bench uses cable-up orientation and the owner has progressed to
M3 installation. Cable-down relief is an alternative only if later requested.
If that alternative is needed,
confirm whether the 11 mm dimension runs along the duct or projects outward, and
establish the protrusion/position before releasing a relief cut. Do not infer
a slot depth from the 6 × 11 mm description alone.

## Print and hardware

The following settings are retained for reproducing the successful print. The
owner can reuse the existing v2 cradle. Print **one** cradle at 100% scale in millimetres, broad base flat on the bed.
Retain the prototype setup: PETG, 0.25 mm layers, 5 perimeters, at least 1.5 mm
solid top/bottom thickness and 50% infill, using the TAZ 6 profile for the installed
nozzle and filament. Check the slicer preview for the 9.5 mm nut-window bridges;
use removable local supports there if the existing print profile needs them.
Clear bridge debris from the groove, shelves, slots and windows before fitting.

**Hardware change: use 6 mm outside-diameter M3 washers.** The earlier 7 mm
washers can touch the ring when a screw is shifted inward. M3 DIN 433 metal washers
are available with 3.2 mm ID, 6 mm OD and 0.5 mm thickness.
[Supplier dimensions](https://www.accu.co.uk/metric-flat-washers/404911-HRDW-M3-A4).

| Quantity | Item |
|---:|---|
| 2 | M3 × 20 mm socket-head metal screws, nominal 5.5 mm head diameter |
| 4 | M3 DIN 433 flat metal washers, 3.2 mm ID × 6 mm OD × 0.5 mm |
| 2 | M3 locknuts, nominal 5.5 mm across flats and 4 mm high |
| 1 | Flat 120 × 140 × 18 mm mounting board, or larger suitable scrap |
| 4 | M4 × 35 mm screws for that 18 mm board |
| 8 | M4 washers, nominal 9 mm OD × 0.8 mm thick |
| 4 | M4 locknuts, nominal 5 mm high |

The M3 stack remains 16 mm under the screw head, leaving about 4 mm of a 20 mm
screw beyond the nominal locknut. Verify actual hardware and thread engagement.
The slots remain 3.6 × 4.6 mm; they provide assembly adjustment, not a guarantee
that every screw/washer position clears the real housing.

## First assembly, power disconnected

1. Put the cable exit at the top, opposite the cradle, and lower the fan into
   the saddle with the ears horizontal. Align the raised
   ring with the central groove and the ear holes with the slots. Both ears
   should rest on their shelves without pushing or squeezing the housing.
2. Check the central ring, other housing ribs, ear roots and wires for contact.
   Do this before adding screws; screws must not pull a poor fit into place.
3. Fit each M3 screw as **head → washer → fan ear → shelf → washer → locknut**.
   Center the screw and upper washer in the existing ear hole, keeping a visible
   gap between washer and ring. Avoid sliding the hardware inward against the
   housing. The nominal centered upper-washer gap is about 0.53 mm; at the
   sampled inward limit it falls to about 0.03 mm, which is too small to rely
   on with real tolerances or washer movement.
4. Hold each nut through its window and snug only enough to remove movement.
   Stop if an ear or shelf bends. Check that the screws align, nuts are
   accessible and the fan does not rock or slide under gentle handling.
5. If the fit passes, attach the cradle to the board with the M4 hardware.
   The drill template's calibration bar must measure 50 mm at actual print size.

The owner has now mounted the fan with M3 nuts and bolts. Recheck washer/cable
clearance during handling, then follow the [mounting-board step](MOUNTING_BOARD.md).
The complete stand and its load validation remain to finish.

## Verification and records

[config.json](config.json) preserves the successful local gauge result and the
failed v1 cradle trial, and records the v2 cable-free-side fit separately from
the interference on the cable side. Installation with M3 nuts and bolts is now
reported; this does not establish a load rating. The actual
ring reproduces the collision against the preserved v1 solid as well as the
regenerated plain saddle. The corrected CAD is checked for ring/fan clearance,
sampled vertical placement, M3 hardware placement, board-hole alignment, valid
CAD/STEP files and a closed STL. Those checks use nominal dimensions; the remaining
housing taper, root fillets and wiring are not measured.

The independent [regression test](test_center_ring.py) uses synthetic dimensions
to catch an omitted or misplaced groove. It is separate from verification with
the owner's measurements. The [v1 report](output/mount_verification_v1.json) and
[v1 print record](CRADLE_V1.md) remain historical; their earlier nominal checks
missed the raised ring.

```sh
python3 design/experiments/edf_bench/generate.py
freecadcmd design/experiments/edf_bench/export_freecad.py
freecadcmd design/experiments/edf_bench/verify_mount.py
freecadcmd design/experiments/edf_bench/test_center_ring.py
```

After a successful physical fit, detail the board-to-lever connection, pivot and
overload stops, then verify retention and calibration without power. The
[bench plan](../../../docs/EDF_BENCH_PLAN.md) tracks the remaining fixture work.
