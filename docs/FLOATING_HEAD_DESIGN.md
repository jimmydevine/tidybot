# Floating vacuum and mop heads — revision M

**Weight-review update:** the owner challenged this candidate's increasing
mass. The [corrective design direction](MASS_OPTIMIZATION_REVIEW.md) now takes
priority over the detailed-carriage work proposed below. Preserve these motion
and load findings as comparison evidence while evaluating simpler construction.

The [N fixed-mount alternative](FIXED_DRIVE_COMPARISON.md) now quantifies that
tradeoff. Its sampled head requirements exceed M's travel and tilt limits;
do not reuse M's clearance results for a rigid drivetrain. The next passive
head comparison must include the larger motion before claiming a mass saving.

M establishes a **motion and load requirement for the mounts** and a revised
packaging proposal. The original static layout cannot accommodate floating
heads. The revised allocations pass the sampled clearance checks, but the
guide/lift hardware and tighter drive packages still need detailed CAD. These
files are review models; there are no new parts to print or order.

Start with the [interactive views](../design/system/output/floating_heads.html),
[calculation report](../design/system/output/floating_heads.md), or
[vacuum working CAD](../design/system/output/floating_heads_vacuum_working.FCStd)
and [mop working CAD](../design/system/output/floating_heads_mop_working.FCStd).
Each CAD scene also has a STEP export and a separate `_raised` pose.

## What must move

**Vacuum:** float the complete removable cassette, including its roller,
stationary cutter restraint, guard, drive motor, transmission and motor driver.
This keeps the motor/roller relationship fixed during head motion. The blower,
bin and main dirt duct remain attached to the bottom chassis. Retain a smooth,
short compliant connection at the rear outlet and a separate flexible service
harness. The flex-joint allocation is excluded from rigid collision checks;
its sealed deformation and force must still be established.

Keep the two service levels already agreed: the TriCut/plain roller comparison
within a compatible cassette, and complete cassette replacement for another
brush mechanism. The station exchanges the complete wheeled bottom. It does
not dismantle a brush cassette. Changing cassette mass requires a recorded
counterbalance setting as well as its brush speed/contact settings.

**Mop:** float the pad carrier, eccentric mechanism and motor together. Inside
that floating assembly, only the pad and its immediate oscillating plate make
the 3 mm peak-to-peak lateral cleaning stroke. The tank, pump and lift actuator
remain fixed. Keeping the drive with the pad avoids requiring an unmodeled
telescoping shaft or articulated drive across the vertical motion.

This is heavier than floating the textile alone, but that alternative needs a
complete moving drive interface before any mass saving can be credited.

## Proposed mount architecture

Use a chassis-mounted vertical carriage carrying a limited-angle head pivot.
The carriage provides vertical movement; a two-axis pivot lets the cleaning
surface follow small pitch/roll differences. Spring force acts on the carriage
through an adjustable equalizer. The head-to-carriage joint must carry yaw,
scrubbing and roller reaction loads while allowing the two specified tilt axes.
Its guides and pivot need guards against hair and mop splash.

| Requirement | Vacuum | Mop |
|---|---:|---:|
| Working vertical motion from current floor reference | −2 to +10 mm | −2 to +10 mm |
| Working pitch and roll allowance | ±1.5° each | ±1.5° each |
| Raised position, level relative to chassis | +16 mm | +16 mm |
| Moving dry hardware, including moving mount allowance | 512 g | 282 g |
| Extra moving contents | None modeled | 0–100 g pad water |
| Initial normal-force target | 3 N | 8 N with 50 g pad water |
| Effective total spring rate target | 0.12 N/mm | 0.16 N/mm |
| Signed preload at reference position | 2.02 N upward at +4 mm | 4.74 N downward at +1 mm |

These are **mechanism requirements, not selected spring specifications**. The
low effective rate and adjustable preload need a packaged spring/lever design.
The calculation treats vertical translation and floor alignment as ideal; it
does not prove that the proposed carriage and pivot fit, that they do not bind,
or that they balance the off-centre motor weight and cleaning moments. Locating
the actual pivot will also introduce lateral motion that must be added to the
clearance audit. Do not cut a slot and infer that the modeled freedom exists.

The vacuum head weighs about 5.02 N before touching the floor. Adding downward
springs would defeat a 3 N contact target. Upward counterbalance reduces its
mechanical contact force while letting it follow the floor. The plain roller
may need substantially less counterbalance; select its setting from installed
mass, not a presumed equal bare-roller weight.

The mop's wet reference moving weight is about 3.26 N. Its spring system adds
about 4.74 N at the reference position to reach 8 N. That is approximately
1.09 kPa over the 230 × 32 mm pad area. Neither this pressure nor the vacuum's
3 N target has been validated for cleaning performance.

At the existing 15 Hz design frequency, a 1.5 mm eccentric has about 13.3 m/s²
peak acceleration. If the existing 105 g pad allowance all oscillates, it
produces about 1.4 N peak inertial force dry and 2.7 N with 100 g retained water,
before any additional oscillating mount mass. A counterweight tuned dry cannot
cancel every wet-pad condition. Keep the vertical force adjustment independent
of the oscillator and check vibration isolation before committing the scanner
mounts. The M equilibrium calculation is static and excludes those forces.

## Lift and retention

The lift should operate through a lost-motion connection: slack during normal
floor following, taking up only when commanded to raise. It must level the
head before reaching the +16 mm stop. A mechanical capture supports it raised;
the actuator is not intended to remain stalled. Captive lower stops retain the
head when the entire robot is lifted. Position sensing must distinguish a head
resting on the floor from a mechanically captured head.

Stop the roller or mop oscillator before raising; stop water before lifting
the mop. Verify raised capture before module exchange or any future flight.
A caught head must cause a stop/recovery action rather than increased lift
force. The exact link ratio, lift load, release behavior and capture hardware
are still to design.

Retain the existing **PQ12-100-6-R envelope as a reference**. Its manufacturer
lists 20 mm stroke, 19 g mass and 10 mm/s no-load speed. A 16 mm head lift does
not yet imply 16 mm actuator movement or a demonstrated lift time. The 62 g
installed allowance includes the actuator, links, supply and switches. The
manufacturer currently lists it on backorder; this study adds no purchase.
[Actuonix product data](https://www.actuonix.com/pq12-100-6-r).

## Necessary packaging changes

Coordinates remain X left-to-right, Y front-to-back and Z upward in the nominal
chassis frame. These changes are an M overlay; the previous files are preserved.

| Allocation | M proposal | Reason |
|---|---|---|
| Vacuum cassette | 230 × 60 × **48 mm**, same floor reference | +16 mm raised head must clear side rails starting at Z=65 mm |
| Vacuum drive | **71 × 60 × 29 mm**, minimum [32,6,50] | Clears side rail, raised power shelf and neighbouring electronics while tilting |
| Vacuum power shelf and its equipment | Raise **18 mm** | Creates room for the motor to move with the cassette |
| Vacuum drive controller, blower driver and bottom supervisor | Raise **18 mm** | Clears the moving cassette |
| Shared Pi bay | Raise **20 mm**, new Z=107…141 mm | Makes room over the revised front electronics |
| Shared front camera | Raise **16 mm**, new Z=70…101 mm | Clears the lifted head while staying below the front frame rail |
| Front-right near sensor | Move X from 235 to 250 mm | Clears the raised Pi bay |
| Mop motor/crank allocation | **32 × 27 × 83 mm**, minimum [105,162,24] | Clears battery, lidar mount and rear pump through motion |
| Mop tank | Raise **18 mm**, new Z=41…121 mm | Clears lifted/tilted pad while retaining tank volume |
| Mop lift allocation | Raise **15 mm**, new Z=42…71 mm | Clears the raised pad |
| Cap roof reservation | Raise **6 mm** to 153.1 mm | Covers the raised vacuum power/fan bay; lidar still sets overall height |

The smaller envelopes need actual hardware fit checks. In particular, a listed
45.1 mm brush dimension inside a 48 mm head leaves only 2.9 mm gross difference;
this is **not a verified guard/cutter/brush-to-floor stack**. A 25 mm motor in a
29 mm drive height leaves only 4 mm for surrounding structure/clearance. The
mop's narrow drive bay similarly needs a real motor, eccentric, wiring and
support arrangement. If these stacks fail, revise the nearby packaging instead
of reducing required guards or brush clearance.

The Pi/camera changes affect the shared core, including other bottoms. M checks
vacuum and mop integration only; sofa/duster interfaces, camera view and
removal paths must be rechecked before adopting those shared changes. Existing
camera/LiDAR performance and occlusion assumptions are not revalidated here.

The power shelf now needs taller structural supports and a renewed thermal and
harness check. Raising the tank needs positive retention and a revised leak
tray. The clearance model does not contain these new brackets.

## Loads, clearances and mass accounting

The model separates fixed chassis mass, each moving wheel pod and the complete
moving head. Tank water stays with the tank; pad water moves with the mop.
It solves head position/contact force and wheel spring equilibrium together.
Contents and caster direction change during use; wheel shim settings remain
fixed after module calibration.

| Result | Vacuum | Mop |
|---|---:|---:|
| Nominal loaded planning mass | **5.316 kg** | **4.954 kg** |
| Added mount/lift/riser allowance | 174 g | 98 g |
| Wheel shim proposal, left/right | 3.50 / 3.00 mm | 3.50 / 2.75 mm |
| Working head translation | +2.42…+3.69 mm | −0.23…+0.14 mm |
| Net floor support at head | 1.92…3.89 N | 6.29…9.36 N |
| Total normal load on drive wheels | 40.45…45.45 N | 29.53…33.10 N |
| Minimum raised-head floor clearance | 10.47 mm | 14.52 mm |
| Maximum height including 2 mm reserve | 176.01 mm | 177.55 mm |

The mass totals retain K's complete hardware allowances. M adds guide/pivot
and riser allowances plus one vacuum lift; the existing mop lift stays counted
once. Some old head allowances already included suspension, so there may be
overlap to remove when the hardware is resolved. **No weight saving is claimed.**
I's alternative scanner masses are still not substituted into K's totals.
Some aggregate power/structure CG rows lack component-level positions; their
placement remains an allowance. These are not measured assemblies or final
flight inputs.

The operational sweep has 1,512 working cases and 168 raised cases. It varies
contents, 24 caster directions, ±20% effective head-spring rate and ±1 N net
parasitic force. These are project sensitivity bounds, not supplier tolerances
or measured guide/duct forces. All modeled wheel supports stay positive and
clear their stops; all required working poses remain within the selected travel.

A separate **0–5 N suction-force sensitivity** raises gross vacuum floor
contact to as much as 8.89 N. Pressure pushing the head down and the resulting
floor contact act in opposite directions on the whole robot. With coincident
resultants, they increase local contact/drag without unloading the chassis by
that same 5 N. The calculation keeps net head support separate from gross
contact. It does not establish the pressure footprint, its moment, skid/brush
friction, or available wet-floor traction.

There are 28 geometric poses per module: 27 combinations of translation and
tilt, plus the level raised stop. The mop pad also receives ±1.5 mm oscillation
offsets. The proposed transformed bounding boxes have no overlaps with the
checked fixed allocations and remain within 275 mm in X/Y. This is a finite,
conservative envelope check, not a complete assembly collision certification.
K's detailed moving pod, new guide/lift/retention hardware, cable motion and
the deforming air joint still need inclusion.

The 10.47 mm vacuum raised clearance has little margin over a 10 mm threshold,
and is measured above a **flat floor** in the static model. It does not prove
step crossing, which changes support points and chassis attitude. Retain the
L requirement to raise the anti-tip mounts 10 mm; they remain clear in this
sweep, but their new brackets are not designed. L's wheel-spring tolerance
failures also remain open despite nominal M shim checks passing.

## Next deliverable

Detail the **vacuum cassette and its carriage first**: real roller/drive-end
and guard stack inside the 48 mm head, motor/transmission inside the narrowed
drive bay, then guide/pivot, counterbalance, captive stops and lift latch.
Include their actual motion, side loads, duct stiffness and mass in the model.
If the component stack needs more room, revise the overhead layout before
releasing a full head print. Apply the proven carriage approach to the mop only
after its oscillating stage and wet-pad load range are accounted for.

Inputs: [floating_heads.json](../config/floating_heads.json).
Checks and remaining limits: [validation record](../design/system/output/floating_heads_validation.md).
Regenerate calculations with `python3 design/system/floating_heads.py` and CAD
with `freecadcmd design/system/export_floating_heads_freecad.py`.
Run the system test suite with
`python3 -m unittest discover -s design/system -p 'test_*.py' -q`.
