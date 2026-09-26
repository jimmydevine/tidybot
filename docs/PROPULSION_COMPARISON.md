# Propulsion screening from published data

> **Scope update, 2026-09-13:** [Whole-system design](SYSTEM_DESIGN.md) now controls
> cross-module layout, carried mass, lift sizing and battery decisions. This
> earlier study remains supporting evidence; its lift deferral or battery-first
> recommendation, where present, is superseded.


2026-09-05. **All propulsion work is deferred**, including this comparison,
fan selection, sizing and the $825 EDF stand. Current work is
[core and ground modules](GROUND_MODULE_DESIGN.md). Resume lift design after their
dimensions and carried masses are established. The data below and fitted cradle
are retained references; no fan or test-equipment purchase is proposed.

The current requirement remains lifting the complete robot, including the core
and cleaning attachment. Budget is flexible, but fixtures and measurements must
resolve a design decision worth their cost. No new spending limit is inferred.

## Candidates with useful published specifications

Prices below are per complete fan/motor assembly, excluding ESC, battery and
delivery/taxes where applicable. UK prices retain their advertised currency;
there is no assumed exchange rate. US prices are from Motion RC's
[current catalog](https://motionrc.com/collections/edf-power-systems), checked
2026-09-05. A listing does not guarantee stock. Exact motor revisions matter.
These are candidates, not a purchase order.

| Assembly | Supply / stated voltage | Thrust per fan | Current per fan | Fan/motor mass | Listed unit price |
|---|---|---:|---:|---:|---:|
| [PowerFun 70 mm, D2842-3400KV](https://www.4-max.co.uk/edf-pf-70mm-4S.html) | 4S / **14.79 V loaded** | 1.435 kgf | 52.5 A | 178 g | £47.50 |
| [Freewing E7215, 70 mm, 2550KV](https://www.freewingmodel.com/478.html) | 4S / 14.8 V nominal | 1.50 kgf | 55 A | 180 g | $45.99 |
| [PowerFun 70 mm, D2842-2300KV](https://www.4-max.co.uk/edf-pf-70mm-6S.html) | 6S / **22.26 V loaded** | 1.816 kgf | 51.8 A | 178 g | £53.49 |
| [Freewing E7216, 70 mm, 2150KV](https://www.freewingmodel.com/461.html) | 6S / 22.2 V nominal | 2.05–2.20 kgf | 55–58 A | 220 g | $43.99 |
| [Freewing E7219, 70 mm, 2100KV](https://www.freewingmodel.com/592.html) | 6S / 22.2 V nominal | 2.15 kgf | 54–57 A | 220 g | $78.49 |
| [Freewing E7218 Pro, 70 mm, 2210KV](https://www.freewingmodel.com/462.html) | 6S / 22.2 V nominal | **2.50–2.60 kgf** | 66–70 A | 240 g | **$81.79** |
| [Freewing E7238, 80 mm, 1680KV](https://www.freewingmodel.com/863.html) | 6S / 22.2 V nominal | 2.77 kgf | 78 A | 285 g | $78.49 |
| [Freewing E72314, 80 mm, 2150KV](https://www.freewingmodel.com/862.html) | 6S / 22.2 V nominal | 3.40–3.50 kgf | 103 A | 340 g | $110.99 |

The Freewing pages provide catalog thrust/current points or ranges. They do not
provide a continuous-hover rating, loaded-voltage history, or a full
part-throttle curve. Ranges are transcribed as ranges; their opposite endpoints
are not asserted to be simultaneous measurements. Several Freewing pages list
watts that differ from nominal volts times amps, so those numbers must not be
treated as a precise synchronized electrical measurement.

4-Max describes its own tests as free-air measurements with the manufacturer's
inlet ring fitted and warns that installation changes thrust. That makes it a
firsthand measurement source, although uncertainty and run duration are not
reported. [Test basis](https://4-max.co.uk/edf-units.html)

[edf_candidates.csv](../design/experiments/edf_candidates.csv) retains the original
figures, source type, nominal-versus-loaded voltage distinction and price source.
The separate 3S row is the PowerFun 4S assembly at a different supply voltage,
not another fan or another purchase.
The calculated mass substitutions and thrust ratios are retained in
[edf_screen.csv](../design/experiments/edf_screen.csv); blank hover-power fields
mean that a suitable partial-throttle curve was not available.

## Closest reference to the owner's existing fan

The PowerFun 70 mm/4S uses the same **D2842-3400KV** designation and 12-blade,
70 mm format reported for the owner's DD fan. Its two published operating points
are 887 gf at 11.13 V / 34.5 A / 384 W, and 1435 gf at 14.79 V / 52.5 A / 776 W.
It is a close comparison for initial sizing. **The matching motor designation
does not establish identical rotor, housing, winding revision or performance of
the owner's assembly.** No replacement fan is necessary just to use these data.
[Measured points](https://www.4-max.co.uk/edf-pf-70mm-4S.html)

All 70/80 mm labels describe nominal rotor diameter. Actual lip diameter, motor
length, mounting ears and cable exit must come from the chosen assembly drawing.
Do not assume a Freewing fan fits the owner's 74 mm-body cradle. A different
cradle would be a later mounting change, not a reason to build the proposed
measurement stand now.

## What the robot mass tells us already

The current concept is **4222.4 g** with four 9-inch motors/propellers. Its
provisional available-thrust target is **2:1**, requiring 2111.2 gf per rotor
before applying any installation-loss allowance. Hover alone needs 1055.6 gf per
rotor. The 2:1 value is a project screening assumption, not a universal flight rule.

At the unchanged reference mass, four PowerFun 4S fans offer only 1.36:1 from
their published point. Four Freewing E7215 fans offer 1.42:1. That is enough to
reject those particular four-fan arrangements against the current reserve target
without measuring another similar fan. It does not rule out a much lighter robot
or a different fan count.

Fan mass must also change. The original ledger contains four 89 g motors and
four **estimated** 15 g propellers, totaling 416 g. A first substitution screen
removes those and adds four complete EDF assemblies:

```text
screened_mass_g = 4222.4 - 416 + 4 * edf_assembly_mass_g
available_ratio = 4 * published_thrust_gf * installation_factor / screened_mass_g
```

This deliberately holds every other component fixed so the effect of fan mass is
visible. It is **not a completed EDF redesign or a lower bound on every possible
design**: guards/frames might become lighter, while ESCs, wiring and battery may
become heavier. Keep inlet/outlet access protection in an EDF design too.

| Four-fan substitution | Screened mass | Ratio at catalog thrust, no installation loss | Ratio with assumed 15% thrust loss |
|---|---:|---:|---:|
| PowerFun 70 mm/4S | 4.518 kg | 1.27:1 | 1.08:1 |
| Freewing E7215 70 mm/4S | 4.526 kg | 1.33:1 | 1.13:1 |
| PowerFun 70 mm/6S | 4.518 kg | 1.61:1 | 1.37:1 |
| Freewing E7216 70 mm/6S | 4.686 kg | 1.75–1.88:1 | 1.49–1.60:1 |
| Freewing E7219 70 mm/6S | 4.686 kg | 1.84:1 | 1.56:1 |
| Freewing E7218 Pro 70 mm/6S | 4.766 kg | 2.10–2.18:1 | **1.78–1.85:1** |
| Freewing E7238 80 mm/6S | 4.946 kg | 2.24:1 | 1.90:1 |
| Freewing E72314 80 mm/6S | 5.166 kg | 2.63–2.71:1 | **2.24–2.30:1** |

The 15% loss is the existing concept's **unmeasured sensitivity assumption**, not
a loss measured for any EDF. No additional voltage scaling has been applied to
these rows. Thrust at lower actual pack voltage remains unknown. Raw catalog
reserve alone is not flight feasibility.

For example, four E7218 fans at the lower 2500 gf catalog value and 0.85
installation factor support at most **4250 g** at 2:1. The simple mass substitution
is 4766.4 g, a **516.4 g reduction** away from that budget. At the upper catalog
value the budget is 4420 g. This is a useful design question to resolve on paper
before ordering four fans.

The stronger 80 mm E72314 clears this one static sensitivity screen but implies
up to **412 A total** if four units simultaneously reach the listed 103 A point.
That is not hover current, and it is not within the owner's 80 A ESC per-fan
rating. Its battery, ESCs, wiring, heat and partial-throttle efficiency must be
budgeted before treating it as a solution. The same caution applies to merely
adding more fans while keeping robot mass and power hardware fixed.

## Comparison with the existing 9-inch option

Hobbywing publishes a seven-point 24 V curve for the reference 3110 900KV motor
with **HQ9x4x3** propellers. It contains 1358 gf at 286 W, 1829 gf at 425 W, and
3318 gf at 1023 W. The table includes a **36-second full-throttle note**, which is
not a continuous-hover rating. [Manufacturer curve](https://www.hobbywing.com/en/uploads/file/20251117/7845436338d9dbe2f43a50c4bae18544.pdf)

Linear interpolation between the two surrounding Hobbywing points gives
**308.7 W at 1435 gf**, versus the measured **776 W** PowerFun 70 mm/4S point:
about **2.51 times as much electrical input for the EDF at that thrust**. This is
an inference across two published bench datasets and operating voltages, not a
controlled same-bench comparison or an installed efficiency guarantee. It is
nevertheless enough to keep the 9-inch configuration as the efficiency reference.
Do not estimate an EDF hover curve by dividing maximum power by maximum thrust;
power is not linear with thrust.

The 9-inch arrangement is much larger: the current guarded concept envelope is
approximately 749 × 549 × 315 mm. Its mass and low-voltage reserve were already
marginal in the [concept findings](CONCEPT_FINDINGS.md). It is not a completed
flight design. The comparison is a real packaging-versus-power trade, not a
claim that the largest available propeller must be used.

## Earlier recommendation — deferred

These were the preceding comparison's next steps. They are superseded by the
owner's instruction to complete ground-module design and mass evidence first;
none is active procurement or modeling work now.

1. **Spend nothing on the proposed EDF measurement stand now.** Use the PowerFun
   4S test as the closest published reference for the owner's fan class.
2. Keep **Freewing E7218 Pro** as the principal 70 mm candidate for a compact lift
   top study: its $81.79 assembly costs only $3.30 more than the weaker E7219
   listing. Four assemblies list at $327.16 before power hardware and shipping.
   This selects a modeling reference, not a purchase or a flight-ready design.
3. Compare it with the existing 9-inch reference and the 80 mm E72314 boundary
   case using complete fan/ESC/battery/frame/guard masses. Resolve the 70 mm
   option's mass deficit and the 80 mm option's current demand before detailed CAD.
4. Use eventual assembled-module checks to answer installation loss, heat,
   control response and retention questions after a design survives these screens.
   Published specs let us skip repeating basic fan characterization; they cannot
   establish the completed robot's performance around stairs or dogs.

No per-fan indoor-flight endurance or dynamic control curve was found in the
shortlisted EDF pages. Forward/reverse assembly availability is useful, but does
not establish adequate yaw authority for a quad-EDF robot. Catalog ducting and
stator effects on reaction torque need to be included in that later control study.
No radio, bench instrument or fan purchase is requested by this comparison.

## Other investigated options and source conflicts

- [PowerFun 90 mm/6S](https://www.4-max.co.uk/edf-pf-90mm-6S.html) lists 2924 gf,
  1561 W, 371 g and £95. It is a useful larger comparison, but that page also has
  an 8S battery recommendation conflicting with its 6S table and prohibition on
  7S+. Do not turn that conflicting page into a wiring recommendation.
- [JP Hobby 70 mm](https://www.jphobby.eu/en/jp-hobby/1025-edf-ducted-fan-jp-hobby-70mm-4-6s-2250kv-motor-ccw.html)
  lists 2350 gf at 22.2 V / 76.6 A, around 1700 W, at $199 through JP Hobby Europe.
  The page contains inconsistent higher-voltage labels. The
  [Motion RC metal-fan listing](https://motionrc.com/products/jp-hobby-70mm-12-blade-edf-4s-6s-power-system-w-2250kv-motor-jph6007-100)
  is $179.99 and lists different mass/geometry. Those versions and voltage points
  should not be merged. Neither is a compelling inexpensive baseline here.
- XFly's current [70 mm product family](https://www.xfly-model.com/productinfo/694364.html)
  includes multiple motor versions. An exact-version performance table and price
  were not verified in this pass; generic online thrust claims were not mixed
  into the numerical comparison.
