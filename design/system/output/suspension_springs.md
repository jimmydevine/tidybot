# L — springs and loaded ride height

Engineering comparison; no spring or fabrication release

K remains the carried-mass planning scenario. L corrects spring loading for moving wheel/pod mass, solves chassis attitude and compares catalog springs. No physical tests or spring order are implied.

## Candidate comparison

The dimensional pass below uses module-specific calibration, all −2.5…+10 mm travel, a ±0.25 mm seat error, +0.5 mm solid-height uncertainty, 2 mm coil-bind gap and a 0.5 mm reserve above catalog L1. It does not establish fatigue life. The earlier spring has no catalog L1.

| Candidate | OD | Rate | Free length | Vacuum / mop / sofa installed screen |
|---|---:|---:|---:|---|
| J_target | 10.00 mm | 5.00 N/mm | 32.50 mm | fail / fail / fail |
| C0360-051-1250-M | 9.14 mm | 6.53 N/mm | 31.75 mm | fail / fail / fail |
| C0360-059-1120-M | 9.14 mm | 13.40 N/mm | 28.45 mm | fail / fail / fail |
| C0420-063-1000-M | 10.67 mm | 13.64 N/mm | 25.40 mm | pass / pass / pass |
| C0420-063-1250-M | 10.67 mm | 10.61 N/mm | 31.75 mm | fail / fail / fail |
| C0480-063-1000-M | 12.19 mm | 9.98 N/mm | 25.40 mm | fail / fail / fail |
| C0480-067-1000-M | 12.19 mm | 13.38 N/mm | 25.40 mm | fail / fail / fail |

**Preferred integration candidate: C0420-063-1000-M**, with an 11.2 mm OD clearance reservation in the existing 12 mm cups. This widens the earlier 10 mm spring reservation; it does not make the robot wider. Use the music-wire variant. Procurement and manufacturing tolerances are unconfirmed.

The reference resting points are +3 mm travel for vacuum/sofa and +1 mm for mop, leaving roughly 7 and 9 mm to the bump stop at calibration. The mop uses more preload than a +3 mm setup so its spring remains seated at full droop. This is not 10 mm of remaining bump and does not demonstrate crossing a 10 mm threshold. Empty/full containers do not trigger an automatic preload adjustment. Each bottom has its own calibrated left/right settings.

| Module | Left/right shim | Operational left travel | Right travel | Max body height + reserve |
|---|---:|---:|---:|---:|
| vacuum | 3.25 / 2.75 mm | 0.76…3.49 mm | 0.52…3.13 mm | 176.38 mm |
| mop | 3.25 / 2.5 mm | -0.82…1.40 mm | 0.43…2.25 mm | 176.96 mm |
| low | 3.75 / 2.5 mm | 2.44…3.28 mm | 2.47…3.55 mm | 175.41 mm |

Operation includes nominal hardware, separate empty/design/heavy contents and the declared tool contact forces over 24 caster headings. All settings remain fixed within each module. Sofa results cover stowed transit only.

| Module | Full-bump shortest spring incl. seat error | Remaining L1 margin after reserve | Failed calibrated tolerance setups |
|---|---:|---:|---:|
| vacuum | 18.25 mm | 0.60 mm | 4 / 16 |
| mop | 18.25 mm | 0.60 mm | 4 / 16 |
| low | 17.75 mm | 0.10 mm | 4 / 16 |

**Do not release this spring for purchase yet.** Some assumed rate/free-length tolerance corners lose either working-length margin at bump or positive seating force at droop at their calibrated settings. The sofa nominal margin is small. Obtain actual load-at-length/tolerance data, then accept a bounded spring/setpoint range or revise the seat/stop geometry. Passing nominal dimensions is insufficient.

## Moving mass, contents and tool contact

The moving wheel, hub, motor and pod subtotal is about 276 g per side. The wheels carry this mass directly as well as the chassis load. Its gravity moment is included in pod equilibrium and its position changes with travel. The K preload calculation treated the whole wheel reaction as spring-supported and therefore overstated preload. L retains the K total hardware mass, separating its moving and fixed portions without counting either twice. Wheel/hub centres move to the H/J axle location; mop water and wet-pad masses have separate positions.

| Module | Contents mass | Head retraction needed at reference point |
|---|---:|---:|
| vacuum | 0…300 g | 1.39…4.75 mm |
| mop | 0…450 g | 0.02…0.86 mm |
| low | 0…250 g | Stowed head: 4.43 mm minimum floor clearance |

The head values are required motion relative to the chassis, not evidence that the current head mechanism supplies it. Tool pressure and floating-head travel must be designed together before the resting point is adopted. Mop fluid sensitivity covers a centred wet pad and water at the allocated tank centre; slosh is unmodeled. Sofa head/hose support while extended needs a separate contact model.

## Necessary anti-tip mount change

The original front anti-tip rollers extend down to Z=2 mm. They intersect the floor in these resting poses, so the three-support calculation would not describe the unchanged robot. L is explicitly conditional on raising their mounts 10 mm (new allocation Z=12…36 mm). Their mass is retained and raised in the CG model. The raised allocation clears the sampled normal-running poses; actual brackets and tipping/threshold behavior remain unqualified.

| Module | Original minimum clearance | Raised minimum clearance |
|---|---:|---:|
| vacuum | -3.94 mm | 6.05 mm |
| mop | -1.24 mm | 8.76 mm |
| low | -4.13 mm | 5.87 mm |

## Uncertainty and scope

The 16 calibrated tolerance setups combine independent ±10% spring rates and ±0.5 mm free lengths; operational sweeps then add ±0.25 mm seat errors. These are project sensitivities, not supplier specifications. Low/high hardware sweeps use the existing component mass intervals with nominal shim settings, preserving contents as separate loads. They are correlated all-low/all-high cases, not every mixed component/CG corner. No design-wide tolerance closure is claimed.

| Module | Low-hardware travel L/R | High-hardware travel L/R | High-mass stop cases |
|---|---|---|---:|
| vacuum | -1.48…1.41 / -1.53…1.22 | 3.48…6.05 / 2.98…5.46 | 0 |
| mop | -2.15…0.01 / -0.94…0.83 | 1.08…3.35 / 2.33…4.20 | 0 |
| low | 0.25…1.08 / 0.73…1.75 | 5.44…6.26 / 5.01…6.10 | 0 |

The calculation assumes quasistatic motion, parallel ground-normal forces, spherical tire reach and an ideal caster. Drive torque, friction, damping, acceleration, tire deformation and obstacle-climbing dynamics are absent. Extra rigid ground contacts invalidate the three-support solution; the raised anti-tip clearance is checked separately. Stop reaction signs are checked for equilibrium at the limits. The installed spring calculations use all travel; operational height is a finite sample.

Reapplying the K impact cases with the new spring gives at most 107.4 N spring force and uses a ±110 N fixed-cap branch bound. Screened pivot/stop-screw bending: 98.8/113.2 MPa; inner M4 bolt shear: 99.9 MPa; angle-edge shear: 70.8 MPa. These limited static screens pass; cup/trunnion strength, retention, fatigue, thread and motor-shaft checks remain open.

Spring mass, revised shims and any new hardware remain within an unclosed mass allowance; K totals are not presented as measured or finalized L hardware.

## Sources and artifacts

- [ASRaymond manufacturer catalog](https://www.asraymond.com/globalassets/catalogs/spec-springs-and-washers-catalog-u.pdf): spring dimensions, rates and load lengths; catalog music-wire values used.
- [ASRaymond C0360-051-1250-M](https://www.asraymond.com/mechanical-wire-springs/compression/spec-standard-compression-springs-132415/c0360-051-1250-m-c03600511250m/) and [C0480-067-1000-M](https://www.asraymond.com/mechanical-wire-springs/compression/spec-standard-compression-springs-132415/c0480-067-1000-m-c04800671000m/): product identity/rate references; rounded solid heights differ from the catalog, so the larger catalog dimensions are retained.
- [Interactive results](suspension_springs.html), [inputs](../../../config/suspension_springs.json), [calculation data](suspension_springs.json), [design record](../../../docs/SUSPENSION_SPRING_SELECTION.md).
