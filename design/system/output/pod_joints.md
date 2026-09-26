# K connected suspension candidate

Candidate design; strength screens and nominal CAD, not fabrication release

One closed curved slot and a fixed steel sleeve provide both travel stops. The slot endpoints are shortened to account for nominal sleeve/slot clearance. No spring or printed part serves as the hard stop.

Nominal travel: −2.5 to +10 mm. Slot width 8.5 mm around an 8 mm sleeve; each endpoint is trimmed by 0.641°.

Maximum screened stop force 257.4 N; 8 mm pivot bending 99.3 MPa; stop-screw root bending 121.1 MPa.

The local inner-rail group reaches 862.3 N per bolt in the declared load cases. M3 shear screen: False; M4: True. The front angle edge includes the countersink's reduction in ligament.

| Tray strip | Bending | Deflection | Screen |
|---|---:|---:|---|
| 3 mm | 150.0 MPa | 0.435 mm | False |
| 4 mm | 84.4 MPa | 0.183 mm | True |

The 4 mm aluminum tray is selected for this conservative strip analogy. It does not prove the complete two-dimensional plate, motor bracket, local threads or fatigue.

Complete pod estimate: 244.5 g nominal per side, including fixed local supports. Earlier J's 106.2 g excluded the fixed cap/cheeks/frame joints.

Only G pod entries are replaced; motors kept once and separated for CG. All other G hardware, including bottom-frame and unfinished carrier allowances, remains. I changes are not silently combined.

| Assembly | G nominal | K nominal | Change |
|---|---:|---:|---:|
| vacuum | 4.777 kg | 5.142 kg | +365.0 g |
| mop | 4.491 kg | 4.856 kg | +365.0 g |
| low | 5.056 kg | 5.421 kg | +365.0 g |

| Bottom | Required left shim | Required right shim | Existing 0–6 mm range |
|---|---:|---:|---|
| vacuum | 5.29–5.78 mm | 3.64–4.13 mm | True |
| mop | 2.21–3.35 mm | 0.92–2.06 mm | True |
| low | 6.43–6.89 mm | 2.83–3.73 mm | False |

Do not extend the shim range without rechecking spring coil bind and guide bottoming. The spring remains a sourcing target. The mass update does not establish flight endurance or change battery selection.

See [design record](../../../docs/POD_JOINTS_AND_STOPS.md) and [CAD checks](pod_joints_cad_checks.json) for modeled fasteners, clearance limits and unfinished work.
