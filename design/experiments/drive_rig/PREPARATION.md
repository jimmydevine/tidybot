# Prepare the rolling rig before controller delivery

Updated 2026-09-12. **Two B-G431B-ESC1 boards are purchased; receipt has not been
reported.** The earlier delivery estimate was later in the week; actual price
and arrival date are unknown.
**Two HiLetgo AS5600 encoders are received.** The owner confirms 23 × 23 mm boards,
16 × 16 mm hole centers, 4 mm holes and centered sensor chips. The existing board carrier is preserved as a reference;
hold duplicate prints while rotor retention is redesigned. An included magnet
measures 4 mm diameter × 2 mm thick; polarization and received count are unconfirmed.
**The wheel spins freely with the holder removed.** The tape trial enters the
bore but wobbles and needs more reach; it is retired. The owner now proposes a
metal rod in the reported 3.4 mm bore. See [ENCODER_METAL_ROD.md](ENCODER_METAL_ROD.md)
for fit questions and material/retention review before selecting any new part.
Keep the current deck, motor brackets and encoder supports for this assessment.
The immediate milestone is an assembled, weighed chassis plus working USB and
encoder diagnostics. Powered driving follows motor characterization and firmware
commissioning. Lift testing stays deferred.

## Work to do now

1. **First complete motor/bracket fit confirmed.** The owner has mounted one
   motor in the 8.50 mm bracket and reports that it spins freely. The second
   bracket was last reported printing with Cura support disabled; its finished
   quality and fit remain unconfirmed. No repeat coupon print is needed.
2. **Finish the second [motor bracket](output/motor_bracket_8p50mm.stl) fit.**
   Inspect the completed print, particularly bridged areas and layer bonding.
   With the battery disconnected, start all four M2 × 6 screws loosely in the
   stationary motor face, then tighten gently by hand and turn the wheel through
   a full revolution. Nominal engagement is 2 mm. Verify clearance around the
   rotating body and wire exits.
3. **One [caster riser](output/caster_riser.stl) is printed and mounted**, per
   owner report on 2026-09-07. One is the full required quantity: the two drive
   wheels and one rear caster form three floor contacts. Check the caster's
   screws clear the ball/housing, then attach the riser to the deck with four
   M3 × 50 bolts. Check deck level and all three floor contacts after assembly.
   The existing encoder carrier uses four M3 screws and 3 mm spacers per board.
   Keep it while the [metal-rod approach](ENCODER_METAL_ROD.md) is assessed.
   No further tape carrier or replacement support print is requested.
4. **Battery/meter body fit checked; the [220 × 240 mm deck](output/deck.stl)
   is printed and visible in the assembly photo.** Reported 2026-09-09. The HiLetgo revision preserves the
   existing deck, motor brackets and carrier attachment holes. This is a prototype print
   decision; later physical fit checks may still identify adjustments.
   The reported **135 × 43 × 22 mm** battery fits the existing
   **140 × 50 × 30 mm** reservation. Put its long dimension across the deck and
   cable end toward the right (+X). Guide both corner leads past the tray columns
   without pinching them. There is 20 mm from the unpadded battery top to the tray
   underside; padding and straps use some of that space.
   The **86 × 43 × 25 mm** wattmeter fits across the shelf's **162 × 64 mm clear
   interior** (168 × 70 mm outside, with a 3 mm rim on each side). Centering it
   leaves 38 mm at each cable end and 10.5 mm on each long side. Guide its two
   cables at each end gently over the rim; use insulating padding if a low
   cable exit would press against it. Body fit does not establish actual cable
   bend radii. Check leads, plugs and straps during unpowered assembly.
   Print the deck, one ballast tray, four tray
   columns and two electronics carriers, then follow the
   [full assembly order](README.md#assembly). Roll the chassis by hand to check
   that both wheels and the caster share the floor, the deck sits level, and
   nothing rubs or tips before adding ballast.
5. Label the two motors **L** and **R**, then measure their disconnected lead
   pairs as described below. These measurements help configure later motor
   characterization; they do not establish a continuous-current rating.
6. Weigh available parts into [masses.csv](masses.csv). Each value is the **total
   for that row's quantity**. Use the 2 kg scale for parts/subassemblies and sum
   them; taring does not increase its physical capacity. Leave missing parts
   blank rather than estimating them as measured. Keep ballast separate. If a
   bracket, motor and wheel are weighed together, record that grouping and avoid
   counting the same parts again in individual rows.
7. Prepare the Pi 4 with its existing working OS, Python 3, SD card and cooling.
   Use a suitable USB supply for desk work. If its card is blank, use
   [Raspberry Pi Imager](https://www.raspberrypi.com/software/) with Raspberry Pi
   OS Lite (64-bit); retain any existing useful card rather than overwriting it.
   Copy the rig folder to the Pi and run `python3 record_run.py --help` from that
   folder. It logs entered measurements and never commands motors.
8. Tape a 2 m course with clear stopping space, and choose a phone position that
   sees both marks. Practice timing a marker moved by hand; keep practice data
   separate from actual powered-drive results.

The remaining [print quantities and assembly order](README.md) are already
documented. Use PETG for the chassis; PLA is fine for the initial coupon. No
shafts, bearing blocks, machining or dedicated force stand are needed for this
rolling experiment.

## Remaining hardware to check or order together

The [complete BOM](HARDWARE.md) contains every quantity, reference price and
fastener length. Its current remaining allowance is **$171.00 before tax and
shipping**, before removing supplies already owned/ordered. Most of this is
allowances for supporting hardware and consumables, not a verified shopping cart.
Purchased ST boards, received AS5600s and bundled magnets are excluded from that remaining figure.

| Group | Still needed unless already owned/ordered |
|---|---|
| Wheel feedback | HiLetgo AS5600s and included 4 × 2 mm magnet received; total magnet count unconfirmed (two required). Fit revised board/magnet carriers; check 2 × four-wire leads. Magnetization and field/gap remain unverified |
| Pi power and communication | 1 × regulated 5 V supply for the 3S pack (BOM candidate Pololu D24V50F5); suitable USB-C power lead; 2 × USB-A to Micro-B **data** cables |
| Power harness | 3 × XT60 mating pairs; 3 fuse holders with main 5 A and initial 1 A branch fuses plus spares; latching motor-power switch; 3S-compatible cell alarm; power/signal wire and heat shrink |
| Assembly | Listed M2/M2.5/M3 screws, nuts, washers and spacers; four straps, small cable ties, nonconductive padding and localized adhesive for the magnets |
| Measurements/supplies | Contact thermometer, PETG, floor tape, weighed ballast, Pi SD/cooling if missing |

The two ST boards each contain the MCU and programmer. A separate ESP32,
Arduino, servo tester, PWM board or CAN adapter is not needed for this USB-based
rig. Sensor boards with other dimensions or magnets of other sizes require a
carrier revision; do not assume an AS5600 listing has the same mechanical fit.
Initial fuse choices protect wiring; they are not winding-current limits.

## Unpowered motor worksheet

Disconnect every motor lead from controllers, battery and other circuits. Hold
the wheel still. Name the three leads A/B/C consistently for each motor. Set the
multimeter to its lowest useful resistance range, short its probes together and
record that reading. Measure A–B, B–C and C–A with firm contacts; repeat if unstable.
Record raw readings before subtracting lead resistance. If the meter cannot
resolve the value, record that limitation.

| Measurement | Left motor | Right motor |
|---|---|---|
| Meter model/range/resolution | pending | pending |
| Shorted probes, Ω | pending | pending |
| A–B raw, Ω | pending | pending |
| B–C raw, Ω | pending | pending |
| C–A raw, Ω | pending | pending |
| Each lead to bare metal case (A/B/C) | pending | pending |
| Motor case temperature/ambient | pending | pending |
| Wheel turns freely with mount tightened | pending | pending |
| Motor + wheel mass, g (note if entered as an assembly) | pending | pending |

One mounted motor has been reported to spin freely; its L/R designation has not
been reported, so the individual columns above remain unassigned.

The three corrected pair readings should be broadly similar. A mismatch prompts
a contact/lead check, not an automatic current setting. Do not convert line-pair
resistance to phase resistance until winding topology is established. A DMM
showing no case continuity is only a basic screen. Pole count, current-sense
calibration and usable continuous torque are still unknown; the conflicting
ML2206B sheet does not supply them.

| Fit measurement | Value |
|---|---|
| Battery body L × W × H, mm | 135 × 43 × 22, owner-reported 2026-09-06 |
| Battery lead exits | Both corners of one end; connector/bend fit to check on assembly |
| Wattmeter body L × W × H, mm | 86 × 43 × 25, owner-reported 2026-09-06 |
| Wattmeter lead exits | Two power cables at each end; bend/rim clearance to check on assembly |
| Pi cooler height above PCB, mm | pending |

## When the boards arrive

Keep the ST-LINK daughterboards attached. Start with **one controller connected
by USB only, with battery and all motor leads disconnected**. Follow the
[diagnostic firmware guide](firmware/README.md). First establish USB reporting
without an encoder, then fit and check one encoder, then repeat for the other
side. Record board IDs, measured masses and actual board revisions.

The diagnostic has been compile-checked; it has not been tried on these boards.
It provides no motor-driving commands. Before floor runs we still need sensored
motor control, calibrated current sensing, startup limits and verified stopping
on faults or lost commands. Buying controllers does not establish motor torque
or release the rig for powered tests.

## Questions awaiting the owner's answers

These are saved here so they remain visible after the conversation is summarized:

1. **Nominal bore size resolved:** 3.4 mm is corroborated by the owner's
   [SpeedyFPV listing](https://speedyfpv.com/products/2204-gimbal-motor). Use a
   3.4 mm nominal rod candidate; actual fit remains an assembly check.
2. How much straight bore length can support the rod before an obstruction?
   The earlier 4 mm depth describes the M2 screw holes, not this bore.
3. Which remaining BOM supplies are already available? This inventory check can wait.

**Answered:** the wheel turns freely without the holder; the tape version fits
but wobbles and needs more reach. **Deferred:** wheel bolt/center-hole details
for the outside-wheel alternative.

Answered dimensions and fit history are saved in [inventory](../../../config/owned_parts.json).
The received HiLetgo PCB is 23 × 23 mm with 16 × 16 mm hole centers, 4 mm holes
and a centered chip; its included magnet is 4 × 2 mm. The 3.6 mm stem gauge fit,
but the full holder did not. A 3.4 mm holder had temporary deeper seating and
4 mm gap on 2026-09-09; its neck was lengthened 2.5 mm for an expected 1.5 mm gap.
**On 2026-09-12 repeated retention failures and friction superseded that temporary
stable-fit report.** The old bare-stem mount is retired. The owner subsequently
confirmed free rotation with it removed and proposed a compliant tape wrap. See
the [trial record](ENCODER_TAPE_TRIAL.md). Its subsequent reported fit included
wobble and insufficient reach. It is retired; evaluate the owner's metal-rod
proposal before changing the encoder position. Exact contact point and usable
magnetic field remain unconfirmed.

## Motor bracket print observations

**Resolved:** the owner identified the clip-like feature as Cura-generated
support. One motor is mounted to the first completed bracket and spins freely.
Support is disabled for the second bracket print, which is still in progress.
This does not yet confirm a successful support-free print. Select support per
part and orientation; the caster riser and small carriers have their own bridge
requirements. See the [model-only bracket preview](output/motor_bracket_8p50mm_preview.svg).

**Unconfirmed cause:** an earlier USB print from Cura on the computer made tiny
movements separated by roughly one-second waits, then resumed normal printing.
The owner stopped that print, power-cycled the printer and restarted. Identifying
support resolves the extra geometry, not the earlier pauses.

The generated `motor_bracket_8p50mm.stl` was checked again: 136,084 bytes,
2,720 triangles, one connected component, no boundary/nonmanifold edges and no
zero-area triangles. These checks give no evidence of a broken mesh; they do
not validate the slicer's toolpath or diagnose the printer. No actual sliced
G-code has been supplied or found in the rig folder or Downloads. No CAD geometry
or printer firmware was changed in response to this observation.

If pauses recur, save the sliced G-code, affected layer, Cura version/profile and
any temperature/display changes. Comparing the same G-code over USB and from SD
can help investigate command delivery. Marlin documents slowdown as its movement
buffer empties; this is one possible cause, not a diagnosis of this print.
[Marlin buffering configuration](https://marlinfw.org/docs/configuration/configuration.html)

Cura's Minimum Layer Time can deliberately slow small layers, and Lift Head can
add a wait after a layer. These are alternatives to check against the actual
profile and pause locations, not established causes. Do not change cooling or
mesh-resolution settings blindly on this fitting part.
[Cura setting definitions](https://github.com/Ultimaker/Cura/blob/main/resources/definitions/fdmprinter.def.json)

With the G-code available, inspect the affected region for short move/retraction
sequences, commanded speeds, explicit G4 dwell commands and M109 temperature
waits. Record the affected height/layer and inspect the finished print for blobs,
gaps, shifted layers or poor bonding before proceeding with the bracket fit.
[Marlin G4](https://marlinfw.org/docs/gcode/G004.html),
[Marlin M109](https://marlinfw.org/docs/gcode/M109.html)

The **8.50 mm coupon fit and one complete motor/bracket fit are confirmed**.
One caster/riser is mounted and the deck is printed. Free rotation with the old
holder removed is confirmed. The tape trial failed centering; metal-rod fit is
the next assessment.
The second motor/bracket fit is still unreported.

Motor resistance readings, remaining fit results and available part masses can
be supplied together as the preparation work progresses.
