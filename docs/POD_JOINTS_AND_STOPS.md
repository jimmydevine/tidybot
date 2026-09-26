# Connected wheel pods and travel stops — revision K

The [L spring/ride-height study](SUSPENSION_SPRING_SELECTION.md) supersedes the
preload inference below by accounting for moving pod weight and chassis attitude.
It retains K's carried-mass planning scenario and offers a catalog spring candidate
whose tolerance and cleaning-head integration checks remain open.

The pod now has a connected metal structure and a captive stop that limits both
upward and downward travel. Use the [interactive view](../design/system/output/pod_joints.html),
[FreeCAD assembly](../design/system/output/pod_joints.FCStd), or
[calculated report](../design/system/output/pod_joints.md).

This is the current **ground-drivetrain mass planning candidate**. G remains the
comparison model; J remains the earlier, partially detailed mechanism. The
current CAD and hand calculations do not release structural prints or prove
fatigue, impact life, motor bearing capacity or autonomous operation.

## Connected structure

The motor mounts to the existing Pololu bracket candidate. Four M3 screws join
that bracket to a **4 mm aluminum tray**. Two aluminum bearing blocks bolt to the
tray and hold the 8 mm pivot's polymer bushings. The pivot's fixed cheeks connect
through angle brackets to the cap and the inner/outer floor rails. The lower
spring fork remains printed; it is separately screwed to the tray.

This replaces J's printed structural cradle. A deliberately conservative 20 mm
wide strip calculation under a 150 N load at 30 mm overhang gives 150 MPa in a
3 mm tray, above the project's 120 MPa aluminum screen. The 4 mm candidate gives
84 MPa and about 0.18 mm deflection. This is a screening analogy, not a complete
plate/torsion analysis. A thinner tray with properly designed ribs remains a
possible weight reduction; this model takes no credit for unverified ribs.

The inner rail connection uses **two M4 screws** at Y=142/150.5 mm, Z=57.5 mm.
The local force model includes pivot and stop reactions plus either sign of an
85 N cap-branch load. Its maximum is about 862 N per bolt: M3 fails the declared
shear screen, while M4 passes. The inner angle's front edge moves to Y=137.25 mm,
and the cheek/rail end extends to Y=156 mm. The calculated edge stress includes
material removed by the countersink; it passes the project's 80 MPa shear screen.
The rear bin boundary remains Y=157 mm, leaving only 1 mm nominal clearance.

The outer cap/rail connection uses one through-bolt across the two angles and
cap. This avoids two opposing screws occupying the same space. Tapped joints,
bolt preload, locking, bearing-housing fits and the remaining frame joints still
need qualification; the M4 calculation does not certify every connection.

Material assumptions and project limits follow
[the G frame study](FRAME_JOINT_DESIGN.md) and its
[6061-T6 manufacturer reference](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf).

## One captive stop for both directions

A fixed steel sleeve, nominally **8 mm OD × 5.3 mm ID × 6 mm long**, passes through
a closed curved slot in the moving metal arm. The slot is 8.5 mm wide. Its two
ends stop the wheel at the proposed **−2.5 mm droop and +10 mm bump**. The spring
does not act as the hard stop.

The slot's centreline ends are shortened by about **0.641° each** to account for
the nominal 0.25 mm radial clearance. Without that compensation, the same drawn
endpoints would permit extra wheel travel. CAD confirms nominal contact at both
limits and interference if travel is extended another 0.1 mm. These are nominal
geometric stops: slot/sleeve tolerances, wear and elastic deflection still affect
the real limits. Adjustment requires a revised stop plate or a separately
qualified adjuster; this design does not claim an installed adjustable stop.

The sleeve is clamped to the fixed cheek with an **M5 × 14 countersunk screw**, a
0.8 mm washer and an M5 thin nut. The 16 mm screw envelope collided with the upper
spring fork; 14 mm leaves nominal clearance and thread projection beyond the nut.
The [DIN 7991 screw reference](https://www.accu.co.uk/countersunk-socket-head-screws/495106-SSK-M5-16-10-9-Z)
documents the 16 mm variant, so the 14 mm length remains a procurement requirement.
The [thin-nut table](https://uk.c.misumi-ec.com/book/EPE1_ENG_09_10_24/pdf/8002.pdf)
documents the 2.7 mm M5 height. A thin nut is **not inherently self-locking**;
the final locking method remains open. Sleeve dimensions are a sourcing target,
not a selected part.

The revised load calculation gives approximately **257 N at the stop**,
**99 MPa pivot bending** and **121 MPa at the stop screw's conservative root
section**, inside the project's respective static screens. No reinforcement
credit is taken for the sleeve surrounding the screw. Impact absorption, slot
wear, fatigue and screw clamping are separate qualification work.

## Weight and spring consequences

The complete suspension pod estimate is about **245 g per side**, including the
fixed local supports, modeled fasteners and a completion reserve. It excludes
the motor, wheel and hub, which remain counted separately. J's 106.2 g subtotal
excluded fixed cap/cheeks and frame joints, so these figures have different
boundaries.

For the K planning scenario, replace G's two 62 g pod entries with the K pod
intervals. Keep all other G hardware, including the 225 g bottom-frame and
unfinished carrier allowances. This avoids claiming savings from unfinished
supports. The motor and pod centres of mass are now separate.

The resulting loaded floor configurations are approximately **5.14 kg vacuum**,
**4.86 kg mop** and **5.42 kg sofa vacuum**. Exact intervals, centres of mass and
replacement arithmetic are in the generated report. The illustrative I lidar/
caster mass change is not silently combined with these totals. Duster hardware
is unchanged, while lifting a ground module will need to use its revised mass.
No battery or flight-endurance conclusion is updated by this pass.

The existing spring target and 0–6 mm shim range still cover the nominal loaded
vacuum and mop calculations. The sofa module needs approximately **6.4–6.9 mm on
the left**, beyond the range. Increasing shim thickness alone risks losing guide
end clearance or reaching coil bind. The next spring pass must include the new
mass/CG, empty/full contents and tolerances, then select an actual spring and
check ride height throughout travel. The current spring is not an orderable BOM
selection.

## Fabrication and remaining work

The proposal uses flat aluminum parts, small angle sections, drilled bearing
blocks and printed spring components. The curved slot, trimmed angles,
countersinks, tapped holes and precision bushing bores require a fabrication
plan. A drill press helps with several operations; the slot/profile can be
outsourced, and bearing bores may need reaming. Tool availability and the costs
of those operations should be settled before releasing fabrication files.

Next complete spring selection and ride-height checks, wheel-drop switch mounting,
spring-pin retention, cable routing, nut locking and the remaining joint/load-path
checks. The caster retention and upper connector work from I remain open.

Review artifacts:

- [Inputs](../config/pod_joints.json) and [pod hardware/mass CSV](../design/system/output/pod_joints_hardware.csv).
- [Nominal FreeCAD](../design/system/output/pod_joints.FCStd),
  [bump](../design/system/output/pod_joints_bump.FCStd),
  [droop](../design/system/output/pod_joints_droop.FCStd), with same-named STEP files.
- [CAD check data](../design/system/output/pod_joints_cad_checks.json) and
  [verification record](../design/system/output/pod_joints_validation.md).

Reproduce from the repository root:

```sh
python3 design/system/pod_joints.py
freecadcmd design/system/export_pod_joints_freecad.py
python3 design/system/pod_joints.py
python3 -m unittest discover -s design/system -p 'test_*.py' -q
```

The first calculation supplies the mechanism inputs; the second imports the CAD
mass ledger. The K exporter reuses J's motor/spring geometry functions without
regenerating or overwriting the J artifacts.
