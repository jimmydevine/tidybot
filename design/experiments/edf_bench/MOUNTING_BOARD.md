# Next build step: cradle to moving mounting board

**Deferred:** the complete bench proposal is on hold because of its cost. The
[core and ground-module design](../../../docs/GROUND_MODULE_DESIGN.md)
is the current work. All propulsion work is deferred until the carried modules'
dimensions and masses are established. These assembly instructions are historical.

The owner has installed the fan in the v2 cradle with M3 nuts and bolts.
**Next, attach that assembly to the small mounting board.** This board will carry
the fan on the moving lever of the thrust stand. It is separate from the large,
fixed bench base. This step is an unpowered mechanical assembly.

## Board and fasteners

The existing CAD uses a flat **120 × 140 × 18 mm board**, with the 120 mm dimension
along the fan axis. Use sound plywood or hardwood stock; a pre-cut piece avoids
needing a saw. A different thickness needs a revised bolt length and an update to
the stand's board support height. Confirm the stock before cutting substitute parts.

| Quantity | Part for the nominal 18 mm board |
|---:|---|
| 1 | Flat 120 × 140 × 18 mm board |
| 4 | M4 × 35 mm bolts |
| 8 | M4 flat washers, nominal 9 mm OD and 0.8 mm thick |
| 4 | M4 locknuts, nominal 5 mm high |

The nominal stack is 8 mm printed base + 18 mm board + two 0.8 mm washers +
5 mm nut = **32.6 mm** under the bolt head. A 35 mm bolt leaves about 2.4 mm beyond
the nominal nut. Check that actual bolts engage through the locking insert.

## Mark and assemble

1. Center the cradle on the board, with the fan axis along the 120 mm direction.
   Keep the fan supported while marking; the cradle base has four mounting holes.
2. Transfer those four hole centers, or use the
   [actual-size drill template](output/mounting_board_template.svg). If printing
   the template, verify its 50 mm calibration bar before marking.
3. Set the fan/cradle assembly aside, clamp the board over a backing piece and
   drill four **4.5 mm through holes**. Remove splinters so the cradle sits flat.
4. Assemble each joint as **bolt head → washer → printed base → board → washer
   → locknut**. Tighten evenly until seated, without crushing the plastic or wood.
5. Check that the board sits flat, the fan/cradle cannot rock under gentle
   handling, and the cables and washers have clearance. This is not a proof-load test.

The hole centers form a **36 × 92 mm rectangle**. For a 120 × 140 mm board, measured
from one corner with x along 120 mm and y along 140 mm:

| Hole | x (mm) | y (mm) |
|---|---:|---:|
| 1 | 42 | 24 |
| 2 | 78 | 24 |
| 3 | 42 | 116 |
| 4 | 78 | 116 |

## What follows

The owner can cut wood and has no shaft or bearings. The
[complete hardware list](HARDWARE_LIST.md) now selects the shaft, bearings, hubs,
structural stock, fasteners and electrical/instrument parts together. Use that
list for ordering; this page covers just the moving mounting board.

The next design work is the full assembly/cut/drill drawing using those parts.
The [stand layout](output/layout.svg) keeps the fan axis 120 mm above the pivot and
the scale contact 240 mm from it. The selected shaft is 8 × 200 mm bought stock;
there is no shaft cutting. Structural joints, travel stops and barrier mounting
still need detail drawings. This page is not an instruction to run the EDF.

After the complete stand is assembled, verify its retention and calibrate the
lever without power before progressing to the electrical test in the
[bench plan](../../../docs/EDF_BENCH_PLAN.md).
