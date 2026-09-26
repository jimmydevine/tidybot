# Integrated cassette ends — R candidate

The head ends combine roller-end walls, spherical-bearing seats, skid ramps and pitch-stop supports. A thin removable hood connects the ends. The existing powered lift is retained; this is not Q’s dock-only capture mechanism.

**Review geometry only.** Purchased roller ends, pivot retention, guide mounting, wear surfaces, seals and powered-lift joints are unfinished. No printing or purchase release.

## Scope and mass

| Same complete local scope | Mass |
|---|---:|
| Prior frame + remaining compliance | 170.0 g |
| CAD material at solid material density | 86.92 g |
| Catalog guide/bearing references | 23.0 g |
| Remaining hardware, seals and reserve | 52.0 g |
| Candidate total | 161.92 g |
| Conditional reduction | 8.08 g |

P’s 70 g removable carrier, 62 g powered lift and 75 g plumbing remain. The roller, motor, transmission, driver, risers and body interface remain separate and unchanged. Do not add Q’s 72/75 g mechanism. Each item below belongs to the replacement 170 g scope once.

| Physical part or unfinished scope | Mass | Basis |
|---|---:|---|
| left_integrated_end | 7.09 g | CAD material: Solid-volume PETG estimate: end wall, bearing pocket, skid ramps and stop boss; hardware separate |
| left_drop_link | 3.57 g | CAD material: 2 mm aluminum profile with pivot/carriage holes and pitch-stop arc slot; keyed attachment unresolved |
| left_rail_backing | 11.31 g | CAD material: 1 mm steel L-shaped backing with rear-open P screw relief; rail attachment holes still unmodeled |
| left_carrier_spacer | 0.44 g | CAD material: Carrier offset pad; screws, load-spreading and keyed joints not modeled |
| right_integrated_end | 7.09 g | CAD material: Solid-volume PETG estimate: end wall, bearing pocket, skid ramps and stop boss; hardware separate |
| right_drop_link | 3.57 g | CAD material: 2 mm aluminum profile with pivot/carriage holes and pitch-stop arc slot; keyed attachment unresolved |
| right_rail_backing | 11.31 g | CAD material: 1 mm steel L-shaped backing with rear-open P screw relief; rail attachment holes still unmodeled |
| right_carrier_spacer | 0.44 g | CAD material: Carrier offset pad; screws, load-spreading and keyed joints not modeled |
| hood_and_outlet | 42.09 g | CAD material: 1.4 mm solid walls with rear outlet; end joints, motor mounts, seals and fasteners budgeted separately |
| guide_rails | 18.60 g | catalog reference: Q catalog reference: two 62 mm NS-01-17 rails |
| guide_carriages | 3.40 g | catalog reference: Q catalog reference: two standard NW-02-17 carriages |
| pivot_bearings | 1.00 g | catalog reference: Q historical KGLM-03 envelopes; current supplied variant remains to verify |
| pivot_retention_and_pitch_pin_hardware | 5.00 g | allowance: Allowance: two pivot joints plus two M2 pitch-stop screws/sleeves; exact axial stack unresolved |
| roller_end_inserts_and_guards | 10.00 g | allowance: Allowance: replaceable drive and stationary end inserts; exact purchased roller interfaces are not inferred |
| motor_transmission_frame_fastening | 7.00 g | allowance: Allowance: motor bosses, isolators, hood fasteners and captive inserts; motor/transmission masses remain separate |
| floor_lips_and_shell_seals | 8.00 g | allowance: Allowance: compliant lips, end seals and hood gasket; not the air-flex plumbing |
| skid_wear_surfaces | 2.00 g | allowance: Allowance: replaceable smooth polymer wear strips on modeled printed ramps |
| rail_and_carrier_fastening | 5.00 g | allowance: Allowance: backing/rail attachment and flush cheek attachment; exact fastener access remains unresolved |
| counterbalance_and_travel_stop_completion | 5.00 g | allowance: Allowance: springs/anchors and captive rail end stops; spring/friction performance remains unproven |
| completion_reserve | 10.00 g | allowance: Unassigned local completion reserve, not material and not a saving |

Current transfer estimate stays **5.275 kg**. Substituting this candidate alone would give **5.267 kg**, still **767 g over** the 4.5 kg limit. No savings are booked.

## Geometry checks

105 head poses and 121 forward-withdrawal samples checked. 0 motion intersections and 0 withdrawal intersections remain in the reported scope. See the CAD check JSON for exact pairs, exemptions and missing hardware.
Minimum sampled clearance to the protected roller envelope: 0.500 mm. Minimum sampled head/guide clearance: 2.999 mm.
The roller remains a protected 200.6 × 45.1 × 45.1 mm listing envelope. No end-cap dimensions or package-to-bare-mass correction is invented. Stock and printed solids can be volume checked without claiming those purchased interfaces are resolved.
The pitch-stop negative controls deliberately tilt to ±7° and find pin/slot interference on both sides; sampled working motion remains free. The nominal ±6° slot has 0.2 mm radial clearance, so it is not an exact ±6° hard limit. Pins, wear and joint capacity remain unqualified.
R also corrects P’s risers and end shoes: Y79 becomes Y72.5. Risers occupy Z60–66 and shoes Z59.5–64.5, clearing the wheel and both earlier P and current Q head-motion samples. The carrier stays within its existing 70 g allocation; no separate system saving is credited.

## Air connection is a separate constraint

The nominal 25 mm axial space requires centreline straight-line reach from **24.49 to 29.68 mm** across the sampled motion, including the 16 mm raised state. Corresponding bore-edge distances span **23.52–29.68 mm**; mating-axis angle reaches **5.22°**.
A taut 25 mm tube cannot supply this reach. A formed bellows or a longer routed flexible connector must be designed for the entire stroke, open bore and small restoring force. These distances are lower bounds, not a specification of bellows developed length. The existing 75 g plumbing allowance stays intact.

## Next decision

Close the pivot fastener stack, keyed carriage joint, rail attachment and powered-lift attachment against these actual end walls before releasing parts. Then solve the short air connection and revisit Q’s friction screen with the resulting moving mass and spring/connector forces. Thin printed walls and stop contact still need stiffness, wear and joint-load qualification. A few grams of frame saving cannot close the system’s remaining weight deficit.
