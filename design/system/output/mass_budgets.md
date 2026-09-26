# Flight-carried mass budget check

Owner requirements: **4.5 kg maximum for transfer flights; 3.5 kg design target for sustained hovering work.** Both exclude the complete lift module and include the core, battery/cartridge, attached tool/drive module and carried contents.

The previous floor totals included a cap. This comparison removes that cap because the lift top replaces it; the nominal deduction is 70 g. Hardware that remains aboard is always counted.

## Latest applicable candidates

| Configuration | Budget | Usual contents | Maximum modeled contents | Reduction needed / headroom |
|---|---:|---:|---:|---:|
| O vacuum / resident sofa attachment | 4.50 kg | 5.125 kg | 5.275 kg | 775 g over |
| N mop | 4.50 kg | 4.654 kg | 4.704 kg | 204 g over |
| G/E airborne duster | 3.50 kg | 2.596 kg | 2.611 kg | 889 g headroom |

Both mass columns use nominal hardware. Contents assumptions: vacuum 150/300 g debris; mop 400/450 g including tank and wet/saturated pad; sofa 120/250 g debris; duster 15/30 g retained dust. The larger case is the maximum currently modeled, not a measured load-capacity rating.

O uses one resident extension per floor. The extension is parked and the ordinary head restored before flight, so vacuum and sofa missions share the same transfer configuration. O includes 108.84 g of added interface/head-adapter allowance. N remains conditional on head motion, joints and mop traction. K is retained below as the prior dedicated-sofa comparison; its mass has not been revised. The duster uses the wheel-less E tool with the F/G core.

## Hardware uncertainty and prior construction

| Candidate | Nominal hardware + maximum contents | High hardware + maximum contents | Budget |
|---|---:|---:|---:|
| N vacuum | 5.166 kg | Not defined for complete candidate | 4.50 kg |
| N mop | 4.704 kg | Not defined for complete candidate | 4.50 kg |
| M vacuum | 5.396 kg | 6.934 kg | 4.50 kg |
| M mop | 4.934 kg | 6.217 kg | 4.50 kg |
| O vacuum / resident sofa attachment | 5.275 kg | Not defined for complete candidate | 4.50 kg |
| K sofa vacuum | 5.481 kg | 7.177 kg | 4.50 kg |
| G/E airborne duster | 2.611 kg | 3.489 kg | 3.50 kg |

The airborne duster has nominal room under the target, but its modeled high estimate leaves only **11 g**. That is effectively no room for further growth at the high estimate. Preserve nominal headroom for uncertainty and unfinished details; it is not permission to add hardware up to 3.5 kg.

## Design gate

Every subsequent mass comparison must show its flight class, complete non-lift mass at maximum permitted contents, remaining headroom and uncertainty. A design above the applicable budget remains a redesign candidate. A nominal estimate below it is a mass-screen result, not measured compliance. Missing hardware or undefined uncertainty stays explicit.

**Actual takeoff mass = non-lift carried assembly + complete lift module.** At the ceiling this is 4.5 kg + lift for transfer or 3.5 kg + lift for hover. Propulsion sizing must still include its own structure, guards, controllers, wiring and any lift-owned energy storage, together with the full carried load. These budgets alone do not settle battery capacity, thrust or hover duration.

A module used for both transfer and sustained airborne cleaning must meet the hover target in its hovering configuration. Any removed mass must actually remain at a station. Preserve cleaning performance, capacities and automatic exchange while redesigning; moving a line item between accounting groups cannot create a physical saving.

[Owner mass requirements](../../../docs/MASS_BUDGETS.md) · [Machine-readable limits](../../../config/mass_budgets.json) · [Weight-reduction work](../../../docs/MASS_OPTIMIZATION_REVIEW.md)
