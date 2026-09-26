# Airborne design verification — revision E

2026-09-13. Numerical and reference-geometry checks only; no hardware measurements or flight tests.

- 42 Python model tests passed (28 baseline and 14 airborne). Checks cover complete carried mass, retained core/cartridge/top accounting, physical camera/FC mass placement, static rotor force/moment/yaw balance, both dusting travel legs and landing reserve, single-leg stair transfer, rear-boom interference regression, unknown EDF hover data and complete replacement-top accounting.
- The rear duster clears the three retained propeller-top and core allocation models. Angled tubes use conservative enclosing segment boxes. This does not validate full motion, camera visibility, contact control or structural joints.
- Updated airborne_dusting.FCStd and airborne_dusting.step contain 68 valid reference/outline shapes. EDF assemblies remain mass/performance studies without qualified installed geometry; no misleading EDF fabrication CAD was generated.
- Generated viewer JavaScript passed Node syntax checking. A minimal DOM exercised 83 combinations: 27 propeller/mass/travel cases and 56 EDF/payload/retention cases. Checks include unavailable source data, a failed energy budget and insufficient maximum thrust. Actual browser layout was not tested.
- Both layout and before/after balance SVGs were rendered through QtSvg and visually inspected. 92 local links across the active README, airborne design, model README, report and viewer resolved.
- Baseline ground geometry and hardware budgets are unchanged. Existing full-system and station CAD remain earlier reference allocations. The new rear-boom station sequence, camera brackets and compact EDF/yaw installation are not fabrication designs.

Manufacturer evidence is linked in the report and config. WeMoTec samples are stabilized-voltage sweeps, not fixed-6S partial-throttle hover tests. EDF results use complete fan/motor/intake masses, explicit installed allowances, 85% retained thrust and 10% power overhead. Equal-load screening is optimistic: yaw/trim are unresolved. Source points are never extrapolated; power/endurance outside the samples remain unknown. Peak input current and battery delivery are not qualified ratings.

Not established: actual carried mass, continuous propulsion duty, installed protection loss, control response, structural/connector/lock ratings, boom compliance, blade access, optical coverage, dust capture/retention, battery current/thermal behavior, launch/landing/exchange trajectories or automatic recovery.

## Reproduction

`python3 design/system/airborne_study.py`

`python3 -m unittest discover -s design/system -p "test_*.py" -q`

`freecadcmd design/system/export_airborne_freecad.py`

## Source fingerprints

- `config/system_design.json`: `0fcabe616ea34c53c47c1d3dbd72489484af97ee88e86682df02577d6bf473a2`
- `config/airborne_dusting.json`: `2d29d994be70cac1a17eeee5de7479258853e2691b9bdcb737e87652e834dbaa`
- `design/system/build.py`: `1e43e07452c4e1661be2c1c632b6586f66da0df1959b8fabf707575fd73a9f68`
- `design/system/airborne_study.py`: `9c85aa3c4733cd84b3ba1b1c240e3ed32ec1dc2c1ac74e096f337e4be61d980d`
- `design/system/airborne_viewer.html`: `f8425f4ad69f219fb5436b89c6049ec1fa9f48e787353a7ca085679260b186d4`
- `design/system/export_airborne_freecad.py`: `c64860802b573f9ec322b900e647e08bc0ce856d93d02bd3bfcf99714854b4f2`
- `design/system/test_system.py`: `befe771b4df07a0f54cfe23d3f316ebb15eba35c715e063f962391d91be0d5eb`
- `design/system/test_airborne.py`: `c3a459a612312486111e45f10dec5d290c4faa172c6f97b92e3309bf00dc6ca0`
