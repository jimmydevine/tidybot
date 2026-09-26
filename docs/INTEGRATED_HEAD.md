# Integrated vacuum-head frame — R study

The cassette ends now share structure between the roller-end walls, spherical
pivot seats, front/rear skid ramps and pitch-stop supports. A 1.4 mm hood joins
the ends and supplies the rear air outlet. This replaces the old solid head
allocation with material geometry so the frame and its suspension can be counted
together.

[Dimensioned geometry views](../design/system/output/integrated_head.svg) ·
[Mass and air-motion report](../design/system/output/integrated_head.md) ·
[Part ledger](../design/system/output/integrated_head_mass.csv) ·
[Editable inputs](../config/integrated_head.json) ·
[CAD checks](../design/system/output/integrated_head_cad_checks.json)

| Review position | FreeCAD | STEP |
|---|---|---|
| Level | [Assembly](../design/system/output/integrated_head_level.FCStd) | [Assembly](../design/system/output/integrated_head_level.step) |
| Left wheel on threshold sample | [Assembly](../design/system/output/integrated_head_left_step.FCStd) | [Assembly](../design/system/output/integrated_head_left_step.step) |
| Head raised 16 mm | [Assembly](../design/system/output/integrated_head_raised.FCStd) | [Assembly](../design/system/output/integrated_head_raised.step) |

These are review models, not fabrication files. They preserve the purchased
roller's entire listing envelope rather than guessing its cutter or end-cap
interfaces. The exact roller ends still determine the replaceable inserts.

## What changed

- Each end wall is 1.5 mm thick, with an integral bearing pocket and skid ramps.
  The ramps rise 13.5 mm over 14 mm at each end; smooth wear strips and compliant
  floor lips remain separately budgeted. Floor contact and scratch resistance
  remain physical checks.
- Each moving link is 2 mm aluminum. A curved slot receives a head-mounted
  pitch-stop screw/sleeve. The slot provides the working pitch range while the
  spherical pivots permit roll and the right pivot permits axial float. Pins and
  retainers still need a complete fit and accessible fastening stack.
- Guide supports now have actual steel backing profiles and carrier spacers.
  Their rear-open reliefs let the existing carrier screws and washers pass during
  forward withdrawal. Round clearance holes would have trapped the head.
- The left side-brush reservation moves another 1 mm outward from Q, to X0–18,
  to accommodate the backing. It stays inside the 275 mm rigid-width limit,
  with only 0.5 mm nominal backing clearance. Real brush hardware and fastener
  tolerance must fit this space.
- All modeled printed pieces fit within the requested 275 mm print footprint.
  They are thin-wall material estimates, not slicer estimates; print direction,
  fasteners, creep and stiffness still need a fabrication pass.

The guide and carriage remain the catalog **envelopes** inherited from
[Q](PASSIVE_HEAD.md), not supplier CAD. The guide envelope touches the link at
the intended carriage mounting plane. This is not evidence of running clearance
for an actual guide. The report's head/guide gap refers to the printed frame and
hood, excluding that mounting plane. Steel backing stiffness, carriage
antirotation, rail screw access and captive travel stops remain unresolved.

## Mass ownership and decision

Compare the complete new local scope against **135 g head frame + 35 g remaining
compliance = 170 g**. The CAD material, guide/bearing references and unfinished
hardware rows all enter that replacement once. Keep the existing **70 g removable
carrier, 62 g powered head lift and 75 g plumbing**. Keep the roller, motor,
transmission, driver, risers and body interface separately. Do not also add Q's
72/75 g dock-only mechanism.

The generated report records the resulting small conditional saving. Integrating
the ends avoids duplicate structural parts, but the guide backings and joints
consume much of the apparent benefit. This is **not a substantial solution to
the vacuum's 775 g weight deficit**, and no saving is booked. The current transfer
estimate remains 5.275 kg, including core, battery and maximum modeled debris,
excluding cap and lift top.

Even eliminating this entire 170 g scope would not close that deficit; it would
also remove required functions. Further weight work must address larger shared
assemblies rather than relying on additional shaving of the cassette walls.

## Air connection and unfinished work

The nominal 25 mm head-to-carrier gap needs up to **29.68 mm straight-line reach**
when raised. Its end orientation also changes during floor following. A taut
25 mm tube cannot provide the motion. A purpose-shaped bellows or longer routed
connector must preserve the bore without pulling the head off the floor.
Endpoint distance is only a lower bound: it does not establish hose bend radius,
wall strain, fatigue, pressure drop or restoring force.

The powered-lift budget stays because the robot needs to raise/release its head
away from a dock. The modeled raised pose does not prove an actuator can reach
it. Q's adverse friction results remain open; R does not reuse Q's old moving
mass to claim a new contact-force result. The actual completed mass, guide drag,
spring forces and flexible connector must be evaluated together.

Before this mechanism can be released: close pivot retention and roller inserts,
keyed carriage attachment, rail fasteners/stops, motor mounts, powered lift and
the air-flex design; verify printed stiffness, stop loads and wear. The new model
checks fit and motion of its stated solids, not complete strength or assembly.

The next system-level weight pass should rank the current core, battery-cartridge
and shared structural parts by installed mass and required function. Preserve
capacity and automation; compare concrete replacements before changing budgets.
