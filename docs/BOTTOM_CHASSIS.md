# Bottom chassis integration — T comparison

**Decision: reject this arrangement.** Combining the surrounding frame while
retaining N’s separate motor-support angles and crossmember does not reduce the
complete installed estimate. The new frame also obstructs parts of the head
motion and withdrawal path. These are reported failures, not an adopted design.

Review the [interactive frame and obstructions](../design/system/output/bottom_chassis.html),
[complete mass calculation](../design/system/output/bottom_chassis.md),
[itemized ledger](../design/system/output/bottom_chassis_mass.csv), and
[vacuum CAD](../design/system/output/bottom_chassis_vacuum.FCStd).
The [mop CAD](../design/system/output/bottom_chassis_mop.FCStd) uses the same frame
routes with its lower control/power shelves. Both have matching STEP exports.

| Complete local support scope | Previous estimate | T comparison | Increase |
|---|---:|---:|---:|
| Vacuum | 680.9 g | 735.7 g | 54.8 g |
| Mop | 676.9 g | 732.7 g | 55.7 g |

This scope includes the general bottom frame, complete N wheel supports,
complete F mechanical power carrier, M risers and caster installation. It
excludes the motors, wheels, hubs, cleaning hardware and electrical components,
which remain fully counted elsewhere. The old H route geometry had no separate
booked mass, so deleting it cannot produce a saving.

T replaces the old scopes with dimensioned material and explicit remaining
hardware. The caster plate has one owner. The newer I caster/stem/retention
allocation totals **142 g**, versus the old **112 g** installed-caster row;
this corrects 30 g of the increase before counting the new saddle. The fitting
and positive airborne retention remain unqualified. No measured weight is claimed.

T alone would give **5.330 kg vacuum / 4.760 kg mop**, at maximum modeled contents,
including core and battery and excluding the lift and removed cap. R and S
reductions are not stacked. Historical O/N comparison totals remain unchanged;
their old caster allowance is incomplete and those figures are not final masses.

There is a useful limit to the chassis work: the vacuum needs **774.8 g** removed,
while this entire old support/caster scope is only **680.9 g**. Even a physically
impossible zero-mass replacement would leave **4.594 kg**. Other assemblies must
also change to meet the 4.5 kg requirement.

The proposed side rails connect to N’s existing cleats and support the head
receiver and power shelves. A rear box beam routes below the rear cliff windows,
behind the bin, and carries the caster saddle. Four corner seats retain the
86 mm core mating datum. Component locations, purchased drivetrain parts,
cleaning capacities, head lift and automatic interfaces are preserved.

The CAD check found no internal material overlap. It does find obstructions
between the inner power web and head hardware, and between the front seats or
controller support and the departing carrier. Core removal is checked after
retracting the four lower core sliders; the S supports are included as a fit
comparison without taking their mass saving. Local bending screens do not
qualify frame torsion, joints, notches, buckling, shaft loads or flight retention.

Stop detailing this arrangement. The next comparisons are:

1. A structural tray carrying the existing motor brackets directly, replacing
   N’s separate support angles and crossmember as part of the chassis. Keep the
   wheel locations and 150 N wheel / 600 N module-interface load requirements.
2. A lighter implementation of the **190 g 24 V converter/cooling assembly**,
   retaining its required electrical output, thermal performance and protection.
3. Integrated bin/air-path construction, retaining 500 mL usable capacity,
   filtration, hair clearance and automatic emptying.

These are comparisons to develop, not permission to remove hardware allowances
or reduce performance. No printing or purchasing is needed for this rejected frame.

Reproduce from the repository root:

```sh
freecadcmd design/system/export_bottom_chassis_freecad.py
python3 design/system/bottom_chassis.py
python3 design/system/bottom_chassis_viewer.py
python3 -m unittest discover -s design/system -p 'test_*.py' -q
```

After changing model source, also regenerate P/Q/R/S CAD fingerprints before
running the full suite. Tests verify the accounting and that failed geometry
remains explicitly rejected; passing tests do not mean this frame is fit to build.
