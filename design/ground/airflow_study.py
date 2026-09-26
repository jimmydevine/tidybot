#!/usr/bin/env python3
"""Compare sourced blower curves with explicit, hypothetical system curves.

No third-party measurements, curve extrapolation or simulated pickup results.
Requires matplotlib for the standalone comparison plot.
"""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "design/ground/output"


def flow_lps(value, unit):
    return value / {"m3/h": 3.6, "L/min": 60}[unit]


def interpolate(points, x):
    if not points[0][0] <= x <= points[-1][0]:
        raise ValueError("Outside published curve; extrapolation is not permitted")
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return points[-1][1]


def system_pressure(scenario, q):
    return scenario["reference_pressure_kpa"] * (q / scenario["reference_flow_lps"]) ** 2


def intersection(points, scenario):
    lo, hi = points[0][0], points[-1][0]
    assert interpolate(points, lo) >= system_pressure(scenario, lo)
    assert interpolate(points, hi) <= system_pressure(scenario, hi)
    for _ in range(60):
        mid = (lo + hi) / 2
        if interpolate(points, mid) > system_pressure(scenario, mid):
            lo = mid
        else:
            hi = mid
    q = (lo + hi) / 2
    p = interpolate(points, q)
    assert abs(p - system_pressure(scenario, q)) < 1e-8
    return q, p


def main():
    config = json.loads((ROOT / "config/vacuum_selection.json").read_text())
    result = {
        "date": config["date"],
        "status": "APPROXIMATE_CURVE_COMPARISON_NOT_MEASURED_PERFORMANCE",
        "curve_note": config["curve_note"],
        "system_note": config["system_scenario_note"],
        "intersections": [],
        "duct_scenarios": [],
    }
    fig, ax = plt.subplots(figsize=(11.2, 7.4))
    colors = ["#2166ac", "#b35806", "#238443"]
    styles = ["-", "--", "-."]
    for curve, color, style in zip(config["curves"], colors, styles):
        points = [(flow_lps(q, curve["flow_unit"]), p) for q, p in curve["points"]]
        assert all(a[0] < b[0] and a[1] >= b[1] >= 0 for a, b in zip(points, points[1:]))
        ax.plot(*zip(*points), color=color, linestyle=style, linewidth=2, label=curve["label"])
        for scenario in config["system_scenarios"]:
            q, p = intersection(points, scenario)
            ax.plot(q, p, "o", color=color, markersize=6)
            result["intersections"].append({
                "curve_id": curve["id"], "scenario": scenario["id"],
                "flow_lps_approx": round(q, 1), "pressure_kpa_approx": round(p, 1),
            })

    for scenario, style in zip(config["system_scenarios"], [":", "--"]):
        qs = [i / 100 for i in range(601)]
        ax.plot(qs, [system_pressure(scenario, q) for q in qs], color="#555555",
                linestyle=style, linewidth=1.4, label=scenario["label"])
    # These are table claims, deliberately not forced onto the digitized graphs.
    ax.plot(13/3.6, 4, "D", color=colors[0], markerfacecolor="white", markersize=7)
    ax.plot(3, 2.5, "D", color=colors[2], markerfacecolor="white", markersize=7)
    ax.annotate("Micronel table differs\nfrom its 12 V graph", (3, 2.5), (3.7, .65),
                fontsize=9, arrowprops={"arrowstyle":"->", "color":colors[2]})
    ax.set(xlim=(0, 7.4), ylim=(0, 7), xlabel="Airflow (L/s)", ylabel="Static pressure (kPa)",
           title="Vacuum blower comparison — published curves and assumed system resistance")
    ax.grid(alpha=.2)
    ax.legend(loc="upper right", fontsize=9)
    fig.subplots_adjust(left=.08, right=.98, bottom=.22, top=.9)
    fig.text(.08, .125, "Dots: calculated intersections, not measured operating points. Diamonds: published table points.", fontsize=9)
    fig.text(.08, .092, "Clean assumption: 2 kPa at 4 L/s. Loaded assumption: 3 kPa at 3 L/s. Both use P ∝ Q².", fontsize=9)
    fig.text(.08, .059, "Manual curve readings are approximate. Conflicting manufacturer/kit curves remain separate.", fontsize=9)
    fig.text(.08, .026, "Sources, file hashes and input points: config/vacuum_selection.json · 2026-09-13", fontsize=9)

    duct = config["duct_proposal"]
    w, h = [v / 1000 for v in duct["clear_section_mm"]]
    area, hydraulic_diameter = w*h, 2*w*h/(w+h)
    k = duct["assumed_total_minor_loss_coefficient"]
    fl_d = duct["assumed_darcy_friction_factor"] * (duct["length_mm"]/1000) / hydraulic_diameter
    for flow in (3, 4, 5):
        speed = flow / 1000 / area
        dynamic_pressure = .5 * duct["assumed_air_density_kg_per_m3"] * speed**2
        result["duct_scenarios"].append({
            "flow_lps": flow, "mean_speed_mps": round(speed, 2),
            "estimated_duct_only_loss_pa": round((fl_d + k) * dynamic_pressure),
            "loss_basis": "Darcy-Weisbach plus assumed local loss coefficient; excludes head, bin, filter, blower ports and exhaust",
        })
    result["blower_outlet_scenarios"] = [{
        "flow_lps": q,
        "mean_speed_in_published_12mm_id_outlet_mps": round(q / 1000 / (math.pi*.012**2/4), 1),
    } for q in (3, 4, 5)]
    result["filter_outer_face_area_cm2"] = 136*76/100
    result["filter_note"] = "Outer frame area only, not active media area or evidence of pressure loss"
    result["blower_branch_budget"] = {
        "nominal_v":24, "design_continuous_output_w":80,
        "assumed_converter_efficiency":.9,
        "battery_current_a_at_nominal_3s":round(80/.9/11.1, 1),
        "battery_current_a_at_nominal_4s":round(80/.9/14.8, 1),
        "startup_current_requirement": "unresolved; driver's 6 A peak capability is not a measured blower startup draw",
        "note": "80 W is an engineering allocation, not typical consumption. Does not select a battery or converter."
    }
    OUTPUT.mkdir(exist_ok=True)
    fig.savefig(OUTPUT / "vacuum_airflow_comparison.svg")
    plt.close(fig)
    (OUTPUT / "vacuum_airflow_comparison.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
