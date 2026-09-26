# Encoder mounting reference

Updated 2026-09-12. **The printed bore-plug magnet holder has failed retention.**
The wheel turns freely with the old holder removed. The tape version enters
but wobbles and lacks reach; it is also retired. Evaluate the owner's proposed
[metal rod and short magnet holder](ENCODER_METAL_ROD.md), reusing the existing
encoder position if fit permits. The nominal 3.4 mm motor bore is corroborated by the matching supplier listing;
rod fit and usable straight support length remain physical checks.

No replacement cap or rod cut length is released. The
[outside-wheel concept](ENCODER_RETENTION.md) remains a fallback.

## Existing stationary board carrier

The assembly photo shows one HiLetgo board on the printed deck. The owner
measures a 23 × 23 mm PCB, four 4 mm holes on 16 × 16 mm centers, and a centered
chip. The [existing carrier](output/encoder_carrier_hiletgo_16mm.stl) retains its
geometry as a reference. Its board mounting details may be reused in a new
support, but its current inboard position does not solve rotor retention.

## Hardware per encoder

| Item | Quantity | Notes |
|---|---:|---|
| M3 × 12 screws and M3 nuts | 4 each | Nylon preferred for this light sensor mount; verify full nut engagement with the actual stack |
| M3 insulating spacers, 3 mm long | 4 | About 6 mm outside diameter; equal lengths |
| M3 insulating washers | 8 | About 7 mm OD and 0.5 mm thick; must bridge the PCB's 4 mm holes without touching components |
| M3 × 20 screws, nuts and washers | 2 sets | Attach carrier foot through deck and motor bracket; already in rig BOM |

The carrier's PCB screw bores are **3.4 mm**, suitable for M3 fasteners. The
board's **4 mm** holes allow a little lateral adjustment; start all four screws
loosely and center the chip on the magnet axis before tightening. Do not fit M4
screws to these printed bores.

Existing stack: screw head → insulating washer → PCB → spacer → carrier →
washer → nut. Keep the board flat, clear solder joints, and tighten lightly and
evenly. Screw lengths and gap spacers must be checked again if the support changes.
Board headers and cables are not fully modeled.

## Superseded bore-plug experiments

- A 3.6 mm gauge fit, but the full 3.6 mm holder did not.
- The owner then used a 3.4 mm holder. A temporary deeper seating and 4 mm
  magnet-to-chip gap were reported on 2026-09-09.
- The neck was extended 2.5 mm, increasing overall length from 14.8 to 17.3 mm.
  Its 3.4 mm entry tip, 3.6 mm neck and 4.4 × 2.2 mm magnet pocket were retained.
  The expected 1.5 mm gap assumed unchanged seating; it was not a measured result.
- On 2026-09-12 the owner reported repeated retention failures and friction.
  This supersedes the temporary stable-fit report. Gap correction did not
  establish retention or free rotation.

The old rigid-fit `magnet_carrier*.stl` files and stem gauges are historical
geometry, not further print recommendations. The separate
`magnet_carrier_tape_trial_2p8mm.stl` also failed centering and is retired. The generic carrier aliases still
contain the longer 3.4 mm version; their filenames do not imply approval for use.

The assembly CAD uses a provisional PCB stack and an inferred holder translation
to illustrate the earlier gap calculation. Actual insertion depth is unknown.
Nominal collision checks cannot override the reported physical binding.

## Sensor checks after a retained mount is fitted

The magnet must remain centered on the rotation axis with no contact, wobble or
added wheel drag. Its air gap must be adjustable and checked on the assembly.
Use USB-only diagnostics and hand rotation before motor commissioning; verify
acceptable field status and smooth angle readings throughout a full revolution.
Magnet-detected status alone does not establish usable angle feedback.

For this flat-disc mounting, the magnet needs **diametric magnetization**
(north and south across its diameter). An ordinary disc with poles on its two
flat faces will not provide the rotating field this mount needs. The
[AS5600 guide](https://learn.adafruit.com/adafruit-as5600-magnetic-angle-sensor?view=all)
explains the required rotating field; it does not identify the supplied HiLetgo
magnet. Check acceptable field status **and** a smooth angle sweep through a
full hand-turned revolution; magnet-detected status alone is insufficient.
Board fit does not establish angle accuracy or operation near an energized motor.

