# Metal rod for the existing encoder position

2026-09-12. The tape-wrap holder enters the motor hole but wobbles and needs
more reach, per the owner. The shorter printed shaft did not suit this assembly.
The owner now reports a 3.4 mm rotating motor bore and proposes a steel rod cut
to length with the existing magnet at its end. Evaluate this before relocating
the encoder. No new part is released for printing or purchase yet.

**Nominal diameter established:** the owner provides the
[SpeedyFPV 2204 260KV listing](https://speedyfpv.com/products/2204-gimbal-motor),
which specifies a **3.4 mm shaft hole** and approximately **27.85 × 13.1 mm**
body. These agree with the owned motor's model/KV and reported 28 × 13 mm body.
Use **3.4 mm as the nominal rod candidate**. The listing supplies no bore fit
tolerance; exact rod fit is a physical check. This is corroborating supplier
data, not a new measurement of the owned motor or proof of electrical ratings.

**Latest observation:** the owner says the motor hole appears to go all the way
through and suspects the old holder rubbed the edge of the stationary mount.
This makes bracket contact plausible, but does not confirm the contact point
or a uniform 3.4 mm bore along the full passage. The wheel's previously reported
center hole is 3 mm, so a 3.4 mm rod must not be forced through the mounted wheel.

## Bracket clearance check

The modeled stationary bracket opening is **4.6 mm diameter**. The old printed
neck is 3.6 mm, leaving only **0.5 mm nominal radial clearance**. A centered
3.4 mm rod would have 0.6 mm nominal radial clearance. Printed hole quality,
alignment and shaft tilt still need physical checking. This bracket opening
provides clearance; it must not act as a rubbing bearing for the shaft.

With power disconnected and the encoder kept clear, check a smooth, known-size
rod/shank gently in the rotating motor bore. It should enter without force,
remain straight, and clear the stationary bracket throughout hand rotation.
Do not use tape to hide a loose fit. Inspect for contact at the bracket opening;
do not assume the through-hole establishes usable support depth or retention.
If a rod contacts the wheel's smaller center hole, stop before that restriction.

If bracket contact is confirmed, relieve the **plastic clearance opening only**,
with the motor removed and debris cleared before reassembly. The motor's bore
and bearing should not be enlarged. A relief size and any updated STL remain
to be selected from the actual rubbing location; no bracket reprint is requested
for the current diagnostic check.

## Mechanical concept

A straight, dimensionally controlled metal rod could replace the long printed
shaft. It must be located by a close fit along sufficient straight rotating
bore length, with no forced insertion or contact against stationary parts.
Stiffness alone cannot remove play between the rod and bore. Do not choose a
3.4 mm interference fit from the nominal hole specification: actual rod
diameter, bore tolerance and supported length remain unknown.

The rod needs retention against sliding out and turning independently of the
rotor. A close sliding fit establishes alignment, not retention. Select the
retention method after checking access and clearances; no adhesive application
inside the motor is specified now. Likewise, a magnet simply attracted to a
steel end is not an established centered, rotation-locked connection.

Use a short concentric magnet holder/cap if needed, with a socket that locates
on the metal rod and a pocket retaining the existing 4 × 2 mm magnet. The cap's
actual fit and centering must also be checked. Rod length follows the measured
insertion, bracket clearance, cap stack and sensor position. Do not copy the
14.8 or 17.3 mm printed part length as a rod cut length.

## Material and magnetic field

Prefer a nonmagnetic rod with controlled straightness and diameter. For a
magnetic steel rod, use a nonmagnetic cap/spacer between the rod and magnet
and validate the assembled sensor readings. The sensor manufacturer's guide
explains that nearby ferromagnetic material can divert or distort the field;
it illustrates a nonmagnetic spacer as a mitigation. Not all stainless steels
are nonmagnetic. Spacer thickness and the field at our 4 × 2 mm magnet remain
unqualified; there is no universal spacing selected here.
[ams magnet selection guide, section 2.7](https://ams-osram.com/documents/20143/80162/AnglePositionOnAxis_AN000271_2-00.pdf/bd13692b-b589-af7f-560c-4d62bf25d9dd)

After mechanical fit and retention checks, hand-turn through complete revolutions
using USB-only diagnostics. Check field status and repeatable angle readings,
not just magnet detection. Powered-motor field accuracy remains a later check.

## Questions saved

1. **Resolved for nominal design:** the owner reports 3.4 mm and supplies a
   matching listing specifying that dimension. No further measurement-method
   question is pending. A known-size rod fit has not been reported.
2. **Partially answered:** the motor hole appears to pass through. Uniform bore
   diameter and the length that closely supports the rod remain unverified;
   establish them during the gentle fit check. The wheel's 3 mm center hole is
   a separate restriction. The earlier 4 mm depth describes the stationary M2
   screw holes, not this rotating bore.

Once fit/support are known, measure the bore-mouth-to-sensor position to size
the rod and cap. Keep the deck, motor brackets and encoder supports for now.
The [outside-wheel bolted design](ENCODER_RETENTION.md) remains a fallback;
wheel bolt measurements can wait. The [tape trial](ENCODER_TAPE_TRIAL.md) is
retired after its centering failure.
