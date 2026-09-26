# Suspension springs and loaded ride height — revision L

The [interactive study](../design/system/output/suspension_springs.html) and
[calculation report](../design/system/output/suspension_springs.md) compare stock
springs using the detailed K drivetrain mass. The preferred integration candidate
is **ASRaymond C0420-063-1000-M**, a music-wire compression spring. Its catalog
dimensions are approximately 10.67 mm outside diameter, 25.4 mm free length and
13.64 N/mm rate. The [manufacturer catalog](https://www.asraymond.com/globalassets/catalogs/spec-springs-and-washers-catalog-u.pdf)
supplies the comparison data. Exact supply, tolerances and fatigue duty remain
unconfirmed; this is not an order recommendation.

## What changed

The earlier preload calculation assigned the whole wheel reaction to the spring.
About 276 g per side moves with the wheel, motor and pod. Its weight also creates
a moment about the pivot. The new calculation includes that moment and changes
the moving mass position with travel, while preserving the K total hardware mass.
Consequently, the earlier statement that the sofa module necessarily needs more
than 6 mm of preload adjustment is superseded by this more complete analysis.

The model also solves chassis pitch/roll, rather than assuming a level chassis
for every contents load. It distinguishes mop tank water from pad water and
samples caster direction and imposed cleaning-head pressure. Each module keeps
one pair of fixed settings throughout its contents/contact sweep.

## Candidate configuration

Retain the K metal tray, pivot, captured stops and 12 mm spring cups. Enlarge the
spring clearance reservation from 10 to **11.2 mm diameter** to accommodate the
catalog spring. The 6.5 mm guide remains inside its nominal 7.47 mm bore. The new
spring envelope does not increase the robot's outer dimensions.

The front anti-tip roller mounts must also move **10 mm upward**, changing their
allocation from Z=2–26 to Z=12–36 mm. At the new resting attitude the original
rollers would contact the floor and add supports, invalidating this calculation.
The proposed raised positions clear the nominal running poses by at least about
5.9 mm. Their brackets and behavior during tipping and threshold crossing remain
to design. The pod CAD below does not include those future brackets.

The starting left/right spacer settings are:

| Bottom | Left | Right | Reference resting travel |
|---|---:|---:|---:|
| Vacuum | 3.25 mm | 2.75 mm | +3 mm |
| Mop | 3.25 mm | 2.50 mm | +1 mm |
| Sofa vacuum, stowed | 3.75 mm | 2.50 mm | +3 mm |

These settings are rounded calculation results for the design load, with the tool
raised. They require calibration on assembled hardware. Positive travel is bump;
the vacuum/sofa setup therefore has approximately 7 mm remaining to its +10 mm
stop, while the mop has approximately 9 mm. The mop's different setting preserves
spring seating at full droop. This does not demonstrate 10 mm threshold crossing.

The [nominal pod](../design/system/output/suspension_springs.FCStd),
[bump](../design/system/output/suspension_springs_bump.FCStd) and
[droop](../design/system/output/suspension_springs_droop.FCStd) exports show the
larger spring reservation and representative settings. They are review assemblies,
not new print files. K geometry and its earlier exports remain available.

## What the results support

With the raised anti-tip mounts and the required floating-head movement, nominal
hardware stays clear of both suspension stops across the sampled contents,
caster headings and tool loads. The sampled I body-height envelope, including its
2 mm reserve, remains below 180 mm. The vacuum head needs roughly 1.4–4.8 mm of
upward movement relative to its chassis reference to follow a flat floor with this
resting setup; its floating mount must actually provide that movement. This study
does not establish traction on wet floors, damping, dynamic threshold climbing or
extended sofa-tool behavior.

The catalog spring passes the nominal installed-length and guide checks, but the
sofa full-bump working-length margin is only about **0.10 mm after the declared
reserves**. Four of sixteen assumed calibrated spring-tolerance combinations fail
an installed spring screen for each module. Nominal success therefore does not
close the selection. Actual spring properties, guide/cup retention and head
compliance must be reconciled before fabrication.

K's robot mass estimates remain approximately 5.14 kg vacuum, 4.86 kg mop and
5.42 kg sofa vacuum. L separates moving/fixed centres of mass and fluid locations;
it does not claim a weighed assembly or savings from changed spacers/springs.
The larger uncertainty ranges and preliminary impact-load recheck are in the
calculation report.

## Next design work

Complete the floating vacuum-head and mop mounts with their intended contact force
and stroke, and detail the raised anti-tip mounts. Then choose spring acceptance limits and spacer settings that retain
working-deflection margin for those loads, or revise the spring seats/stop geometry.
Keep the 4–10 mm threshold requirement open until wheel, head and body contact are
evaluated together. Supplier load-at-length, tolerance and life data are still
needed before spring procurement.

Reproduce with:

```sh
python3 design/system/suspension_springs.py
freecadcmd design/system/export_suspension_springs_freecad.py
python3 -m unittest discover -s design/system -p 'test_*.py' -q
```

[Inputs](../config/suspension_springs.json),
[CAD check data](../design/system/output/suspension_springs_cad_checks.json) and
[verification record](../design/system/output/suspension_springs_validation.md)
record the scope and evidence.
