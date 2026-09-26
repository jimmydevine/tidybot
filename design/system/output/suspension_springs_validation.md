# Revision L verification record

Checked 2026-09-14. Calculation/CAD evidence only; no physical testing or
fabrication release. Read the [design record](../../../docs/SUSPENSION_SPRING_SELECTION.md)
and [calculation report](suspension_springs.md) for assumptions and failed screens.

## Calculations

`python3 -m unittest discover -s design/system -p 'test_*.py' -q`:
**107 tests passed**, including eleven L tests covering force/moment conservation,
moving/fixed mass accounting, moving-pod gravity, free equilibrium, both stop
reaction signs, tool-contact load transfer, spring working-length and seating
failures, nominal/tolerance discrimination and the anti-tip mount requirement.

Generated study coverage:

- 576 nominal operational cases across contents, caster headings and imposed
  cleaning-head loads, with fixed calibrated settings per module.
- 6,144 operational sensitivity cases from independent spring rate/free-length
  corners and seat-position errors. Spring properties remain fixed within a run.
- Separate all-low/all-high hardware cases retain nominal settings. These are
  correlated mass bounds, not a proof over all component/CG combinations.
- 204 reapplications of the K impact screen cover the new springs/settings,
  including tolerance setups that fail spring-length checks. The cap-branch
  force bound increases from 85 to 110 N. The limited pin, stop-screw and inner
  M4/edge screens pass; this does not qualify the complete frame or spring cups.

Each module passes nominal installed spring screens. **Four of sixteen assumed
calibrated spring-tolerance setups fail for each module.** These failures remain
in the output; nominal fits are not treated as tolerance closure. Free-length,
rate, seat error and solid-height allowances are project sensitivities, not
manufacturer specifications.

The original front anti-tip roller positions intersect the floor in the proposed
resting poses. All resting calculations are conditional on the documented 10 mm
mount raise and appropriate floating-head movement. Raised anti-tip allocations
were compared with adjacent I functional allocations for all three bottoms; no
axis-aligned allocation overlap was found. Their brackets are not designed.
Minimum raised roller clearance remains positive in the nominal, spring-sensitivity
and separate mass-bound sweeps; the smallest reported mass-bound value is about
1.17 mm. That is a finite, ideal flat-floor result, not a tolerance/obstacle guarantee.

## CAD

FreeCAD 1.1.3 checked the enlarged 11.2 mm OD / 7 mm ID spring reservation at
**30 travel/setting combinations**, against physical K pod parts and the motor
reference. Representative resting, bump and droop assemblies also received a
local all-parts intersection audit, excluding intentional threaded joints.
No unexpected intersection was recorded.

The three exports contain **276 valid non-null input shapes** in total. All
FCStd archives passed CRC checks and contain Document.xml; all three STEP files
are present. [CAD check data](suspension_springs_cad_checks.json) records the
sampled settings and matching input fingerprints. The spring is an annular
clearance reservation, not a modeled helix or stress simulation. These exports
do not contain the proposed raised anti-tip brackets or completed floating heads.
Bolt lengths varying with spacer thickness are review envelopes, not an approved
standard-fastener purchase list.

J/K exporter entry points now also recognize the command-line file path because
FreeCAD invokes Python files under their basename. Importing those geometry
helpers into L does not regenerate the historical J/K artifacts.

## Interactive review

A Node DOM stub rendered **120 combinations** of module, contents, tool force and
caster heading without missing samples or invalid coordinates. The tolerance
failure count remained visible. A generated SVG was rendered with QtSvg and
visually reviewed. This is not full browser or accessibility testing.

No measured spring curve, fatigue life, wet traction, dynamic threshold crossing,
motor bearing capacity, tipping dynamics or automatic-cleaning performance is
established by these checks. K carried-mass estimates remain the planning baseline.
