# Lift footprint review and ceiling-fan dusting target

2026-09-13, revision C review. The owner considers 644 × 1444 mm excessive.
This review explains the existing calculation; that footprint is not an accepted
requirement or a minimum-size result. The current CAD and mass results remain
comparison evidence while the lift and elevated-dusting layout are reconsidered.

**Revision E follow-up:** the [airborne dusting study](AIRBORNE_DUSTING.md) develops
a wheel-less bottom, a lightweight raised boom and automatic station handling.
Its [interactive comparison](../design/system/output/airborne_dusting.html) includes
smaller duct packaging targets, documented EDF comparisons, rear-boom balance and separate outbound,
cleaning, return and landing energy. This page retains the earlier size drivers.

## What produced 644 × 1444 mm

The eight-rotor comparison has two columns of four 10-inch propellers. Each
propeller is 254 mm across, inside a 284 mm guard. The columns are 360 mm apart,
and their frontmost/rearmost rotor centres are 1160 mm apart:

- **Width = 360 + 284 = 644 mm.**
- **Length = 1160 + 284 = 1444 mm.**

The rotor centres relative to the robot centre are x=−180/+180 and
y=−580/−280/+280/+580 mm. Four propellers are ahead of the core and four behind
it. This keeps a relatively narrow width for the stair corridor, but leaves a
long assembly. See the [layout drawing](../design/system/output/lift_layout_review.svg).

Those inner rotors cannot simply be slid beside the core at their existing
x positions: their disks would overlap the 275 mm square body. At x=180, the
distance beyond the core's side is only 42.5 mm. A 142 mm radius guard needs a
y offset of at least
`137.5 + sqrt(142² − 42.5²) = 273.0 mm` to clear the core corner, before margin.
The selected 280 mm offset is therefore reasonable **for this arrangement**.
The next row is another 300 mm forward/rearward, leaving 16 mm between guards.

This shows why reducing small assembly clearances cannot halve the length.
It does not establish that this two-column arrangement, rotor count, propeller
size or system mass is the best solution.

## Why the comparison grew to eight rotors

The model carries the complete core, battery cartridge and loaded vacuum bottom.
That ground assembly is about 4.676 kg. Removing its 70 g cap and adding the
3.651 kg lift top gives **8.257 kg** airborne.

| Eight-rotor top allowance | Nominal mass |
|---|---:|
| Eight motors | 1.000 kg |
| Eight propellers | 0.160 kg |
| ESC channels and local installation | 0.256 kg |
| Eight guards | 0.720 kg |
| Structure, wiring, locks, cameras and flight electronics | 1.515 kg |
| **Total lift top** | **3.651 kg** |

There is a feedback loop: more rotors and a larger frame add mass, which in turn
requires more lift. The mass estimates need scrutiny, particularly the shared
structure, guards, high-current distribution and repeated sensing hardware.
They are engineering allowances, not measured production parts.

The source motor/propeller curve is for the Hobbywing RTF-3115 900KV and HQProp
10×4.5×3 at 24 V. Its largest thrust point is time-limited to 29 seconds.
[Manufacturer curve](https://www.hobbywing.com/en/uploads/file/20251117/2a4a3f326d2bdede135f3e582b73eef3.pdf).

The design imposed a provisional **2:1 peak thrust-to-weight target**, assumed
75% retained thrust with guards, and scaled maximum thrust for a 21 V bus.
These assumptions led to the following screens with the loaded vacuum:

| Previous layout | Footprint | Complete mass | Screened peak thrust/weight |
|---|---:|---:|---:|
| Four independent rotors | 644 × 844 mm | 7.027 kg | 1.52:1 |
| Six independent rotors | 644 × 1424 mm | 7.658 kg | 2.09:1 |
| Eight independent rotors | 644 × 1444 mm | 8.257 kg | 2.59:1 |

Six already clears that target at nominal mass. Eight was a margin preference;
it was not a demonstrated minimum. Neither clears all upper-mass cases, and
none is a flight qualification. A four-rotor result below 2:1 does not mean it
cannot produce hover thrust; it means it misses this particular reserve target.
Lowering the target alone would not establish appropriate indoor control margin.

## Direction for the next layout pass

First compare a lighter guarded-propeller system with ducts designed for hover
and documented compact EDF assemblies. Within the propeller branch, compare
four independent rotors, four coaxial pairs and a better-packed independent
six/eight-rotor layout. Keep the full
carried bottom requirement, guarded rotors and explicit mass/current accounting.
Choose a documented motor/propeller operating point for each viable arrangement.
The aim is to determine a credible compact envelope, not to select another motor
before doing the layout.

Four coaxial pairs at the previous quad's centre positions would project into
approximately **644 × 844 mm** with the same guard diameter. That is only a
plan-view example: two rotors at each position need vertical clearance, different
guard/frame details and a new aerodynamic/power model. It cannot inherit the
eight independent rotors' thrust or power calculation. Rotor interference and
spacing affect performance; NASA's multirotor design work explicitly treats
those interactions.
[NASA conceptual multirotor design study](https://rotorcraft.arc.nasa.gov/Publications/files/Young_1079_TN20401_16055_Conceptual_Design_Aspects.pdf).

A folding frame can reduce station storage, but leaves its deployed flight
footprint unchanged. More square layouts must be evaluated against the narrow
stair corridor including yaw; an attractive plan-view rectangle alone is not a
route check. The existing 180 mm height constraint remains in effect unless the
owner changes it. No new compact size is promised by this review.

The existing large station follows the intact lift-top parking assumption.
Reconsider its cabinet and handling arrangement after choosing the lift's flight
and storage geometry. Do not freeze the current 1200 × 1800 mm station footprint
as a household requirement.

## Weight reduction and ducted-fan comparison

The owner's next priority is reducing carried mass and reconsidering ducted
fans. Both belong in the next design pass. No propulsion type is selected by
this review, and the existing numerical allowances remain until replacement
geometry or documented hardware supports a change.

The current nominal lift top is 3.651 kg of the 8.257 kg flying vacuum assembly.
The following are useful pools to investigate, **not promised savings**:

| Existing allocation | Nominal mass | Design work |
|---|---:|---|
| Lift guards, structure and high-current harness/distribution | 1.690 kg | Repack the rotors; shorten load paths and cable runs while retaining structural strength, protection and electrical capacity |
| Core printed parts/metal frames, vacuum frame, bin, head frame and wheel pods | 0.984 kg | Replace bounding-box allowances with thin walls, ribs, stock members and actual joints; check duplicated supports |
| A1 LiDAR and three OAK camera allocations | 0.488 kg | Evaluate shared sensing against required ground and flight coverage before removing devices |

For context, the Pi/cooler/storage allowance is only 82 g. Changing that board
alone cannot resolve a kilograms-scale lift problem. Emptying debris or draining
unneeded mop water at the station can reduce transfer payload while still
carrying the complete bottom, but retain loaded cases for tasks that need those
consumables. Do not trade away dog-hair pickup, wet-floor traction, module locks
or necessary obstacle coverage to meet an arbitrary mass target.

Distinguish three concepts:

- **Guarded propeller:** a protective enclosure; no aerodynamic duct benefit is
  established by the current 75% retained-thrust assumption.
- **Duct designed for hover:** rotor, inlet, tip clearance and outlet developed
  together. A suitable duct can improve hover performance at a given rotor
  diameter. A printed ring around a chosen propeller does not establish that
  result. NASA's 10-inch ducted-rotor experiments explicitly varied inlet shape
  and tip clearance and measured their effect on hover performance.
  [NASA ducted-rotor experiments](https://ntrs.nasa.gov/api/citations/20050009943/downloads/20050009943.pdf).
- **Compact jet-style EDF:** a smaller rotor area and fast exhaust can provide
  a useful packaging trade, at a hover-power cost that must be assessed from
  the specific assembly's data. A duct is not by itself evidence of low noise,
  lower installed mass or inaccessible blades; include inlet/outlet protection.

A source-based example illustrates why small EDFs need careful comparison.
At **1.435 kgf of static thrust per unit**:

| Reference | Electrical input | Evidence |
|---|---:|---|
| PowerFun 70 mm / D2842-3400KV EDF | 776 W | 4-Max's reported test at 14.79 V under load |
| Hobbywing RTF-3115 900KV / HQ10×4.5×3, unguarded | About 291 W | Linear interpolation of manufacturer data at 24 V |
| Same 10-inch system, assuming 75% retained thrust with guards | About 435 W | Interpolation at 1.435 / 0.75 = 1.913 kgf of unguarded thrust; guard effect is unmeasured |

[4-Max EDF test data](https://www.4-max.co.uk/edf-pf-70mm-4S.html),
[Hobbywing motor/propeller data](https://www.hobbywing.com/en/uploads/file/20251117/2a4a3f326d2bdede135f3e582b73eef3.pdf).

These are separate test datasets at different voltages, not a controlled
comparison or a prediction for the installed robot. The EDF's added protective
screens and installation losses are not included; neither source establishes
the required continuous operating duty. The Hobbywing maximum point has a
29-second full-throttle limit. The owned DD fan is not verified to match the
PowerFun assembly despite the similar motor designation. This one comparison
does not establish the performance of every ducted fan.

Evaluate each complete candidate using its own installed mass, hover power,
continuous thrust, transient reserve, battery current, inlet/outlet clearance,
control response, usable duster reach and stair envelope. Smaller thrusters may
shorten structure and wiring but also require a heavier power system; iterate
the complete mass rather than comparing bare motor thrust-to-weight ratios.
The short stair-transfer mission and sustained dusting mission need separate
energy checks. Swappable packs do not remove instantaneous current or cooling
requirements. Prefer published curves for this pass; the owned EDF test stand
remains deferred and this review adds no purchases.

## Updated duster requirement

The owner reports:

- Ceiling-fan blades about **7 ft / 2134 mm above the floor**.
- About **1 ft / 305 mm between the fan and ceiling**, implying an approximately
  8 ft / 2438 mm ceiling at that location.
- About **2 ft / 610 mm duster reach** should cover the intended tasks.

This replaces the earlier assumed 2 m high, 300 mm deep shelf. The reach datum
has not been specified; retain 610 mm as the reported tool reach without silently
adding rotor clearance to it or treating it as the fan's radius.

The old octo guards extend **584.5 mm forward of the body's front edge**.
If a 609.6 mm reach is measured from that body edge, only **25.1 mm** extends
beyond the guards, before any clearance to the object. At the old quad's front
guard, the same arithmetic leaves 325.1 mm. Useful reach must therefore be checked
from the actual rotor clearance envelope, with any upward tool angle included.
The fan dimensions do not by themselves select a two-foot straight horizontal boom.

For the next pass, investigate an articulated duster that can reach the top of
a stopped blade while the aircraft remains below and clear of the fan assembly.
Do not assume the robot can operate inside the one-foot fan-to-ceiling gap.
The previous horizontal-only head and its mass allowance do not yet implement
that access; articulation, tool orientation, compliance, restart prevention and
blade clearance must be added and budgeted. Robot rotors and ceiling-fan blades
must remain distinct swept volumes throughout approach and withdrawal.

The sofa requirement remains **914 mm deep, approached only from the front**.
Its approximately 1 m telescope is independent of the shorter desired duster
reach. Do not shorten the sofa mechanism when updating the elevated duster.

The next concrete deliverable is a compact lift/duster comparison with total
mass, projected and vertical dimensions, usable tip reach, stair/fan clearance,
power/current and station storage shown together. Ground-interface detail can
continue, but lift-dependent structure and station dimensions should stay open.
