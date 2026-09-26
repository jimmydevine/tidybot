# Retaining cradle v1 — print and assembly

Status: **FAILED PHYSICAL FIT — retained for reference, do not reprint v1**.
The owner printed one cradle and reports interference with the raised ring around
the middle of the housing. The straight bore and nominal fan model omitted that
feature. See the [v2 correction and print instructions](CRADLE_V2.md).
The original dimensions and assembly notes below describe the failed prototype.

## Files

| File | Use |
|---|---|
| [retaining_cradle_v1.stl](output/retaining_cradle_v1.stl) | Failed-fit part retained for comparison; not the next print |
| [Cradle preview](output/retaining_cradle_v1_preview.svg) | See the cradle, ear shelves and nut windows |
| [Cradle FreeCAD](output/retaining_cradle_v1.FCStd), [STEP](output/retaining_cradle_v1.step) | Editable/reviewable solid |
| [Assembly preview](output/retaining_mount_assembly_v1_preview.svg) | Fan interfaces, cradle, M3 hardware and board |
| [Assembly FreeCAD](output/retaining_mount_assembly_v1.FCStd), [STEP](output/retaining_mount_assembly_v1.step) | Inspect fit and hardware; **not an STL to print** |
| [Board drill template](output/mounting_board_template.svg) | Four base holes, nominal 36 x 92 mm center pattern |
| [Historical geometry check results](output/mount_verification_v1.json) | Earlier nominal checks that missed the ring |

The assembly model uses a nominal 74 mm cylindrical housing and simplified existing
ears. Motor, wiring, real housing taper and ear root fillets are omitted. The four
board bolts are listed below but not included in the assembly model. The motor
and fan internals should stay assembled.

## Geometry and retention

- Print envelope: **48 x 112 x 52.5 mm**.
- Open saddle bore: **74.4 mm**, from the successful gauge trial.
- Saddle length along the fan: **24 mm**, centered on the ear holes, spanning
  **25-49 mm from the intake face**. This longer region still needs a physical fit
  check; the 6 mm-wide gauge did not establish the entire body's profile.
- Existing ears: nominal **20 x 8 x 3 mm**, with **4 mm holes**, centers about
  **82.5 mm apart** and **37 mm from the intake face**.
- Ear shelves: **8 mm thick**. Each has a **3.6 x 4.6 mm capsule slot** across the
  fan, with 1 mm between the slot's end-circle centers. The slots accommodate
  modest uncertainty in the reported spacing; verify actual screw alignment.
- Two open nut windows: **9.5 mm wide x 14 mm high**, accessible from either
  axial end of the cradle. Nuts are held with a small tool, not captive in plastic.
- Four base holes: **4.5 mm diameter**, on a **36 x 92 mm** center pattern.

The ears sit on the shelves and the screws retain the fan. Do not pull the ears
down with the screws to force a tight housing into the saddle. The rounded bore
locates/supports the body; it is not a friction-only clamp. Actual ear strength,
printed-part strength and vibration resistance remain to test.

## Original print settings (v1 failed fit)

Use the TAZ 6 profile for the installed nozzle and chosen filament. Starting
settings for the stock 0.5 mm nozzle are **0.25 mm layers, 5 perimeters, at least
1.5 mm solid top/bottom thickness, and 50% infill**. These are prototype choices,
not a validated structural recipe. Keep the broad base flat on the bed at 100%
scale. Do not scale the part to correct an isolated fit issue.

**PETG is the preferred prototype material.** Prusa identifies it as suitable for
holders and other mechanical parts; that does not establish this mount's load or
temperature rating. Use the filament maker's temperature guidance and your TAZ
profile, rather than transferring another printer's temperatures unchanged.
[Material reference](https://help.prusa3d.com/article/petg_2059).

The nut-window roofs bridge 9.5 mm. Inspect the slicer preview for bridging across
that short direction. Use local supports inside the windows if needed, then
remove them fully before assembly. Inspect the shelves, slots and bore for
drooping plastic. Bridging depends on material, cooling and speed;
[Prusa's bridging guide](https://help.prusa3d.com/article/poor-bridging_1802)
explains those dependencies. No new gauge print is needed.

## Hardware to gather

Reuse matching inventory where available. Sizes below define the intended stack;
check the actual washers and nuts before assembly. They are not purchases already
made or confirmations of what is in inventory.

| Quantity | Item | Purpose |
|---:|---|---|
| 2 | **M3 x 20 mm metal screws**, socket cap or comparable head fitting the ear | Through the existing 4 mm ear holes and cradle slots |
| 4 | **M3 flat metal washers**, 3.2 mm ID, 7 mm OD, 0.5 mm thick | One above each ear and one below each shelf |
| 2 | **M3 nylon-insert locknuts**, about 5.5 mm across flats and 4 mm tall | Retain ear screws through the accessible windows |
| 1 | Flat **120 x 140 x 18 mm mounting board**, or suitable larger scrap/pre-cut stock for the unpowered trial | Support the cradle; eventual connection to the lever remains to detail |
| 4 | **M4 x 35 mm screws** for an 18 mm board | Through the cradle base and board |
| 8 | **M4 washers**, nominal 9 mm OD, 0.8 mm thick | Above the printed base and below the board |
| 4 | **M4 locknuts**, nominal 5 mm tall | Retain board screws |

M3 locknut dimension reference: [Westfield Fasteners DIN 985 data](https://www.westfieldfasteners.co.uk/Datasheets/Nut_HexNy_M.pdf).
Match washer diameters because the housing and nut windows leave limited space.
Do not enlarge the fan's existing holes to fit a larger screw.

The modeled M3 stack is 3 mm ear + 8 mm shelf + two 0.5 mm washers + 4 mm nut =
**16 mm**. A 20 mm screw therefore projects about **4 mm beyond the nut**. Confirm
that the actual thread passes through the locking insert and that its tip clears
the window. For a different board thickness, select the M4 length to suit the
complete stack and locking insert; 35 mm assumes the listed 18 mm board.

## First assembly, power disconnected

1. Remove support/bridge debris from the cradle. Check that screws pass through
   its slots and that washers and nuts can be reached through the windows.
2. Lower the fan into the open saddle, with the two ears horizontal. Align each
   existing hole with a slot. The ears should sit on both shelves without forcing
   the housing down. Check housing ribs, ear roots and wire routing throughout
   the 24 mm saddle region.
3. Fit each M3 screw in this order: **head -> washer -> fan ear -> printed shelf
   -> washer -> locknut**. Hold the nut through its window. Snug evenly only enough
   to remove movement; stop if an ear or shelf visibly bends. A torque value has
   not been established for this fan's molded ears.
4. For board mounting, use the cradle itself as a transfer template, or print the
   SVG at actual size and first verify its 50 mm calibration bar. Make four 4.5 mm
   holes, then attach the cradle with the listed M4 hardware. Keep the assembly
   supported while working; do not handle it by the fan's wires or rotor.
5. Check that the fan cannot slide axially or rock in the mount under gentle
   handling, the nuts remain accessible, and both inlet and outlet stay clear.
   This is a fit/assembly check, not a proof-load test.

The useful feedback from this prototype is whether the fan seats on both shelves,
the screws line up, the nuts are accessible and any rib/wire root interferes.
The trial failed at the central housing ring. Its dimensions have since been
supplied and incorporated into v2; see the corrected instructions, including
the change from 7 mm to 6 mm OD M3 washers.

## Verification and remaining work

The historical v1 geometry check covered a valid single solid, a closed printable STL,
nominal fan clearance during sampled vertical placement, M3 hardware at nominal
and slot-end positions, board-hole alignment and base washer/head clearance. It
also reopened all four CAD/STEP exports. The physical trial has shown why those
checks were insufficient: the raised center ring was absent from both models.

The next bench work after a successful assembly is to detail the board-to-lever
connection, pivot and overload stops, then check stiffness, retention and force
calibration without power. Shielding, independent power interruption and the
electrical/thermal run limits in the [bench plan](../../../docs/EDF_BENCH_PLAN.md)
remain to complete before running the EDF. Neither the cradle nor the fan duct
is a rotor-containment enclosure.

The source now targets v2 with the measured central ring. The following commands
regenerate that corrected version:

```sh
python3 design/experiments/edf_bench/generate.py
freecadcmd design/experiments/edf_bench/export_freecad.py
freecadcmd design/experiments/edf_bench/verify_mount.py
```

The preview renderer uses NumPy in the FreeCAD Python environment (available in
the FreeCAD 1.1.3 installation used here). CAD comes from
[retaining_mount.py](retaining_mount.py); parameters are in [config.json](config.json).
