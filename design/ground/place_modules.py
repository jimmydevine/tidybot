#!/usr/bin/env python3
"""Ground assembly packaging; independent of the deferred flight model.

Boxes reserve space, not material. Child references are contained within their
parent reservations and are not additional installed assemblies or masses.
"""

import copy
import csv
import html
import itertools
import json
import math
from pathlib import Path

from generate import ROOT, OUTPUT, build_study, number


def upper(p):
    return [a + b for a, b in zip(p["min"], p["size"])]


def intersects(a, b):
    """Conservative AABB intersection; touching faces are allowed."""
    return all(min(aa, bb) - max(x, y) > 1e-7
               for x, y, aa, bb in zip(a["min"], b["min"], upper(a), upper(b)))


def contains(a, b):
    return all(x <= y + 1e-7 and bb <= aa + 1e-7
               for x, y, aa, bb in zip(a["min"], b["min"], upper(a), upper(b)))


def swept(p, delta):
    return {"min": [x + min(0, d) for x, d in zip(p["min"], delta)],
            "size": [x + abs(d) for x, d in zip(p["size"], delta)]}


def build_layout(config=None):
    c = copy.deepcopy(config or json.loads((ROOT / "config/ground_layout.json").read_text()))
    head = build_study()
    v = next(v for v in head["variants"] if v["id"] == c["head_roller_set"])
    inv = {p["id"]: p for p in json.loads((ROOT / "config/owned_parts.json").read_text())["owned_parts"]}
    parts = copy.deepcopy(c["reservations"])
    for p in parts:
        p["basis"] = "proposed reservation"
    sources = {
        "roller_filter": "../../../config/owned_parts.json",
        "motor": "https://www.pololu.com/product/4846/specs",
        "blower": "https://www.sameskydevices.com/product/resource/cbm-97b.pdf",
        "lidar": "https://www.slamtec.com/cn/lidar/a1spec",
        "pi": "https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-mechanical-drawing.pdf",
        "driver": "https://www.cytron.io/cytron/p-10amp-5v-30v-dc-motor-driver-2-channels",
        "battery": "https://www.amazon.com/dp/B0972RKJDS",
        "printer": "https://download.lulzbot.com/TAZ/6.0/documentation/manual/",
    }

    def add(pid, label, module, pos, size, basis="proposed reservation", **kwargs):
        p = dict(id=pid, label=label, module=module, min=pos, size=size, basis=basis, **kwargs)
        parts.append(p)
        return p

    hx, hy, hz = c["head_origin_mm"]
    add("head", "Short roller cassette reservation", "bottom", [hx, hy, hz],
        [v["cassette_study_width_mm"], v["cassette_study_depth_mm"], v["roof_reference_height_mm"]],
        bom=["head", "roller_drive", "vacuum_rollers"],
        note="35mm cassette roof reference. A separate side-drive extension reaches62mm; wheel driver sits independently above the roof. Not a completed powered head.")
    d = v["roller_diameter_mm"]
    for i, y in enumerate(v["roller_center_y_mm"]):
        add(f"roller_{i+1}", f"Owned roller style {'AB'[i]}", "bottom",
            [hx + v["roller_x_mm"], hy + y - d/2, hz], [v["roller_length_mm"], d, d],
            "owner dimensions", parent="head", shape="cylinder_x", source=sources["roller_filter"])
    a = head["proposed_allowances_mm"]
    add("roller_drive_space", "Roller drive side bay", "bottom",
        [hx + v["cassette_study_width_mm"] - a["outer_wall"] - a["drive_bay_width"], hy + 3, 3],
        [a["drive_bay_width"], v["cassette_study_depth_mm"] - 6, v["roof_reference_height_mm"]-6],
        parent="head", note="Motor, transmission and opposite rotation remain to detail.")
    wheel = inv[c["wheel_inventory_id"]]["known"]
    wd = wheel["diameter_mm"]
    ww = wheel.get("width_mm", c["wheel_width_allowance_mm"])
    wheel_basis = "owner dimensions" if "width_mm" in wheel else "owner diameter; proposed width allowance"
    wheel_note = (f"Owner reports {number(wd)} mm diameter x {number(ww)} mm width. "
                  if "width_mm" in wheel else
                  f"Owner reports {number(wd)} mm diameter; {number(ww)} mm width is an allowance. ")
    if "axle_hole_diameter_mm" in wheel:
        wheel_note += f"Owner reports {number(wheel['axle_hole_diameter_mm'])} mm center hole. "
    if wheel.get("hub_protrusion_beyond_reported_width_mm") == 0:
        wheel_note += "No wheel-hub protrusion reported. "
    wheel_note += "Selected motor adapter, fasteners and installed offset still need qualification."
    m = c["motor_reference_mm"]
    for side, center, face in zip(["left", "right"], c["wheel_centers_mm"], c["motor_face_x_mm"]):
        x, y, z = center
        add(f"wheel_{side}", f"Owned {side} wheel", "bottom", [x-ww/2, y-wd/2, z-wd/2],
            [ww, wd, wd], wheel_basis, shape="cylinder_x", bom=["wheels"],
            note=wheel_note)
        mx = face if side == "left" else face-m["body_length"]
        add(f"motor_{side}", f"25D {side} motor reference", "bottom",
            [mx, y-m["body_diameter"]/2, z-m["body_diameter"]/2],
            [m["body_length"], m["body_diameter"], m["body_diameter"]],
            "manufacturer reference; not purchased", parent=f"{side}_drive", shape="cylinder_x", source=sources["motor"])
        sx = face-m["shaft_extension"] if side == "left" else face
        add(f"shaft_{side}", f"{side.title()} output shaft", "bottom",
            [sx, y-m["shaft_diameter"]/2, z-m["shaft_diameter"]/2],
            [m["shaft_extension"], m["shaft_diameter"], m["shaft_diameter"]],
            "manufacturer reference; not purchased", parent=f"{side}_drive", shape="cylinder_x", source=sources["motor"])
    fw, fh, ft = head["filter"]["reported_body_envelope_mm"]
    ref = c["reference_placements"]
    fd = [fw,fh,head["filter_approximate_local_depth_mm"]]
    add("filter", "Owned filter including tab allowance", "bottom", ref["filter"],
        [fd[i] for i in c["filter_axis_order"]], "owner dimensions + derived tab depth",
        parent="filter_chamber", source=sources["roller_filter"],
        note="Broad face vertical, normal to x. Full-face19mm depth reserves unknown tab location. Filter chamber moves rear with bin, then opens for manual filter access.")
    cavity = c["proposed_bin_clear_cavity_mm"]
    add("bin_cavity", "Proposed clear debris cavity", "bottom", cavity["min"], cavity["size"],
        parent="bin_drawer", note="Rectangular geometric volume, not demonstrated usable capacity.")
    bd = inv["cbm_blower"]["known"]["reference_envelope_mm"]
    add("blower", "Owned CBM blower, upright", "bottom", ref["blower"], [bd[i] for i in c["blower_axis_order"]],
        "manufacturer envelope", parent="blower_bay", source=sources["blower"],
        note="Rotated 97 x 95 x 33 envelope. Drawing establishes axial inlet / tangential outlet; exact port adapters unmodeled.")
    add("driver_pcb", "MDD10A PCB footprint reference", "bottom", ref["driver_pcb"], [84.5,62,1],
        "manufacturer footprint; 1 mm display thickness", parent="wheel_driver_bay", source=sources["driver"],
        note="Footprint only; board components, terminals and cooling must fit the parent reservation.")
    add("battery", "Owned 3S pack listing reference", "core", ref["battery"], [43,132,25],
        "seller reference; not owner measured", parent="battery_tray", source=sources["battery"],
        note="Dimensions retained from the exact battery listing in EDF_BENCH_PLAN.md; cables and restraint use tray allowance.")
    add("pi_pcb", "Pi 4 PCB footprint reference", "core", ref["pi_pcb"], [85,56,1],
        "manufacturer footprint; 1 mm display thickness", parent="pi_tray", source=sources["pi"],
        note="Ports, cooler, storage and cables consume the parent tray; 1 mm sheet is only a drawing convention.")
    add("lidar", "Core-fixed RPLIDAR A1 reference", "core", ref["lidar"],
        inv["rplidar_a1"]["known"]["family_reference_envelope_mm"], "manufacturer family reference",
        bom=["lidar"], source=sources["lidar"], note="Owned revision and actual scan-plane offset unconfirmed; everything else is kept at/below the scanner base plane.")
    for interface, (z0, z1) in c["latch_z_ranges_mm"].items():
        for i, (x,y) in enumerate(c["latch_corners_by_interface"][interface]):
            jz0,jz1=c.get("latch_z_overrides",{}).get(f"{interface}_joint_{i+1}",[z0,z1])
            add(f"{interface}_joint_{i+1}", f"{interface.title()} joint zone {i+1}", "interface",
                [x,y,jz0], [*c["latch_xy_size_mm"],jz1-jz0], bom=["core_interfaces"],
                note="Compact combined mating zone for retention, seat and guides; fit and strength unverified. Initial bolts and later station latch share this zone; halves not modeled.")
    for p in parts:
        p.setdefault("shape", "box")
        p.setdefault("bom", [])
    data = dict(config=c, parts=parts, sources=sources, head_variant=v)
    data["derived"] = {
        "body_envelope_mm": [*c["body_mm"], max(upper(p)[2] for p in parts)],
        "moving_xy_min_mm": [min(0, min(p["min"][i] for p in parts)) for i in [0,1]],
        "gross_bin_cavity_l": math.prod(cavity["size"])/1e6,
        "panel_blank_span_mm": c["printing"]["main_piece_xy_mm"],
        "station_separation_mm": c["station"]["docked_tray_top_z_mm"]-c["station"]["lowered_tray_top_z_mm"],
    }
    data["derived"]["moving_xy_size_mm"] = [max(c["body_mm"][i], max(upper(p)[i] for p in parts))-data["derived"]["moving_xy_min_mm"][i] for i in [0,1]]
    data["checks"] = validate(data)
    return data


def validate(data):
    c, parts = data["config"], data["parts"]
    by_id = {p["id"]: p for p in parts}
    errors = []
    if len(by_id) != len(parts):
        errors.append("Duplicate component IDs")
    for p in parts:
        if any(not math.isfinite(x) for x in p["min"]+p["size"]) or min(p["size"]) <= 0:
            errors.append(f"Invalid dimensions: {p['id']}")
        if "parent" in p and not contains(by_id[p["parent"]], p):
            errors.append(f"Reference exceeds parent reservation: {p['id']}")
        if not p.get("outside_body") and not contains({"min":[0,0,0],"size":data["derived"]["body_envelope_mm"]}, p):
            errors.append(f"Outside body envelope: {p['id']}")
        if p["module"] == "bottom" and upper(p)[2] > c["bottom_mate_z_mm"]:
            over = dict(p, min=[*p["min"][:2],c["bottom_mate_z_mm"]],
                        size=[*p["size"][:2],upper(p)[2]-c["bottom_mate_z_mm"]])
            if not any(contains(pocket,over) for pocket in c["core_clearance_pockets"]):
                errors.append(f"Bottom projection lacks core clearance pocket: {p['id']}")
    rigid = [p for p in parts if not p.get("outside_body")]
    limit=c["constraints"]["max_rigid_xyz_mm"]
    if any(s>maximum for s,maximum in zip(data["derived"]["body_envelope_mm"],limit)):
        errors.append("Assembly exceeds owner rigid size limit")
    for p in rigid:
        if not contains({"min":[0,0,0],"size":limit},p):
            errors.append(f"Rigid component exceeds owner limit: {p['id']}")
    if not c["constraints"]["flexible_bristles_may_extend"] and any(p.get("outside_body") for p in parts):
        errors.append("Bristle protrusion has not been allowed")
    for pocket in c["core_clearance_pockets"]:
        for p in parts:
            if p["module"] in ("core","interface") and intersects(pocket,p):
                errors.append(f"Core pocket obstructed: {pocket['id']} / {p['id']}")
    roots = [p for p in parts if "parent" not in p]
    checked = 0
    for a,b in itertools.combinations(roots,2):
        checked += 1
        if intersects(a,b):
            errors.append(f"Reservation collision: {a['id']} / {b['id']}")
    # Parent boxes include internal space; siblings still must not collide.
    for a,b in itertools.combinations([p for p in parts if "parent" in p],2):
        if a["parent"] == b["parent"] and intersects(a,b):
            errors.append(f"Internal reference collision: {a['id']} / {b['id']}")
    services = []
    seal = by_id["clean_plenum"]
    released_seal = dict(seal, size=seal.get("service_size", seal["size"]))
    released_seal["min"] = seal.get("service_min", seal["min"])
    seal_gap = released_seal["min"][0] - upper(by_id["filter_chamber"])[0]
    if seal_gap < 3:
        errors.append("Bin seal release must provide at least 3 mm clearance before extraction")
    for pid, delta in c["service_translations_mm"].items():
        if sum(d != 0 for d in delta) != 1:
            errors.append(f"Only single-axis service sweeps supported: {pid}")
        p, blockers = by_id[pid], []
        member_ids=[pid,*c.get("service_members",{}).get(pid,[])]
        members=[by_id[member] for member in member_ids]
        regions=[swept(member,delta) for member in members]
        for obstacle in roots:
            if obstacle["id"] in member_ids:
                continue
            check = obstacle
            if pid == "bin_drawer" and "service_size" in obstacle:
                check = dict(obstacle, min=obstacle.get("service_min",obstacle["min"]),size=obstacle["service_size"])
            if any(intersects(region,check) for region in regions):
                blockers.append(obstacle["id"])
        if blockers:
            errors.append(f"Service sweep blocked: {pid} by {', '.join(blockers)}")
        final_min = [x+d for x,d in zip(p["min"],delta)]
        axis = next(i for i,d in enumerate(delta) if d)
        if not (final_min[axis] >= c["body_mm"][axis] or final_min[axis]+p["size"][axis] <= 0):
            errors.append(f"Service stroke does not extract entire tray: {pid}")
        low=[min(region["min"][i] for region in regions) for i in range(3)]
        high=[max(upper(region)[i] for region in regions) for i in range(3)]
        services.append(dict(id=pid, member_ids=member_ids, translation_mm=delta,
                             sweep={"min":low,"size":[h-l for l,h in zip(low,high)]},
                             occupied_sweeps=regions, blockers=blockers))
    aperture = c["cap_aperture_mm"]
    lidar = by_id["lidar"]
    if not contains({"min":[*aperture[:2],0],"size":[*aperture[2:],10000]},lidar):
        errors.append("Cap aperture cannot pass over scanner")
    cap_clearance = c["top_mate_z_mm"]+c["station"]["cap_lift_mm"]-upper(lidar)[2]
    if cap_clearance < 5:
        errors.append("Cap lift must clear scanner top by at least 5 mm")
    actual_projection=max(upper(p)[2] for p in parts if p["module"]=="bottom")-c["bottom_mate_z_mm"]
    projection=max(actual_projection,c["station"]["bottom_projection_above_mate_mm"])
    gap = c["station"]["docked_tray_top_z_mm"]-c["station"]["lowered_tray_top_z_mm"]-projection
    if c["station"]["lowered_tray_top_z_mm"] < 0:
        errors.append("Lowered station tray passes below floor")
    if gap < c["station"]["required_separated_gap_mm"]:
        errors.append("Bottom separation cannot clear proposed mating projection")
    tx,ty,tw,td = c["station"]["tray_xy_mm"]
    for p in parts:
        if p["module"]=="bottom" and not contains({"min":[tx,ty,0],"size":[tw,td,10000]},p):
            errors.append(f"Station tray misses bottom outline: {p['id']}")
    if min(p["min"][1]+c["station"]["bottom_rear_transfer_mm"] for p in parts if p["module"]=="bottom") < c["body_mm"][1]:
        errors.append("Bottom transfer stroke does not clear core footprint")
    if any(s>maximum for s,maximum in zip(data["derived"]["panel_blank_span_mm"],c["printing"]["max_piece_xy_mm"])):
        errors.append("Whole main panel exceeds print size limit")
    if any(s>maximum for s,maximum in zip(data["derived"]["panel_blank_span_mm"],c["printing"]["bed_reference_xyz_mm"])):
        errors.append("Whole main panel exceeds nominal printer bed")
    if max(c["usable_bin_target_l"]) > data["derived"]["gross_bin_cavity_l"]:
        errors.append("Usable bin target exceeds proposed clear cavity")
    # Preserve the connected routing corridor when a measured head grows/moves.
    for a,b in [(by_id["head"],by_id["dirty_duct"]),(by_id["dirty_duct"],by_id["bin_drawer"])]:
        if abs(upper(a)[1]-b["min"][1]) > 1e-7 or any(min(upper(a)[i],upper(b)[i]) <= max(a["min"][i],b["min"][i]) for i in [0,2]):
            errors.append(f"Dirty-air routing faces do not meet: {a['id']} / {b['id']}")
    duct,bin_body=by_id["dirty_duct"],by_id["bin_drawer"]
    if any(duct["min"][i]<bin_body["min"][i] or upper(duct)[i]>upper(bin_body)[i] for i in [0,2]):
        errors.append("Full dirty-duct outlet must enter the dirty bin face")
    with (ROOT/"config/ground_components.csv").open() as stream:
        ledger = {r["id"] for r in csv.DictReader(stream)}
    for p in parts:
        if set(p["bom"])-ledger:
            errors.append(f"Unknown BOM reference: {p['id']}")
    return dict(errors=errors, root_pairs_checked=checked, service_sweeps=services,
                separated_mate_clearance_mm=gap, cap_lift_clearance_mm=cap_clearance,
                bin_released_seal_gap_mm=seal_gap,
                actual_bottom_projection_mm=actual_projection,
                limits="AABB reservation checks only; touching routing faces and parent containment intentional. Unmodeled structure, cables, fasteners, tolerances, loads, scan optics, full station hardware and fluid performance are not validated.")


COLORS = {"bottom":"#e9eff4", "core":"#e3ebf8", "interface":"#ffe3b2"}


class SVG:
    def __init__(self, title, width=900, height=670):
        self.e = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">',
                  f'<title>{html.escape(title)}</title>',
                  '<style>text{font-family:Arial,sans-serif;fill:#20344b} .dim{stroke:#5c7186;stroke-width:1;marker-start:url(#a);marker-end:url(#a)}</style>',
                  '<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5c7186"/></marker></defs>',
                  f'<rect width="{width}" height="{height}" fill="white"/>']
        self.text(30,30,title,23)

    def text(self,x,y,s,size=13,anchor="start"):
        self.e.append(f'<text x="{x:g}" y="{y:g}" font-size="{size}" text-anchor="{anchor}">{html.escape(s)}</text>')

    def rect(self,x,y,w,h,fill="none",extra=""):
        self.e.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}" stroke="#64798d" {extra}/>')

    def line(self,x1,y1,x2,y2,extra='stroke="#6e8093"'):
        self.e.append(f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" {extra}/>')

    def dim(self,x1,y1,x2,y2,label):
        self.line(x1,y1,x2,y2,'class="dim"')
        self.text((x1+x2)/2,(y1+y2)/2-8,label,13,"middle")

    def part(self,p,scale,ox,oy,axes=(0,1),floor=None):
        a,b = axes
        x = ox+p["min"][a]*scale
        y = oy+p["min"][b]*scale if floor is None else floor-upper(p)[b]*scale
        w,h = p["size"][a]*scale,p["size"][b]*scale
        fill = COLORS[p["module"]]
        if p["basis"].startswith("owner"):
            fill="#a7dac8"
        elif p["basis"].startswith("manufacturer"):
            fill="#afd2ef"
        elif p["basis"].startswith("seller"):
            fill="#ddc2e8"
        self.e.append(f'<g><title>{html.escape(p["label"]+" | "+p["basis"]+" | "+" x ".join(map(number,p["size"]))+" mm")}</title>')
        circular = (p["shape"]=="cylinder_z" and axes==(0,1)) or (p["shape"]=="cylinder_x" and axes==(1,2))
        if circular:
            self.e.append(f'<ellipse cx="{x+w/2:g}" cy="{y+h/2:g}" rx="{w/2:g}" ry="{h/2:g}" fill="{fill}" stroke="#5f7288"/>')
        else:
            self.rect(x,y,w,h,fill,'stroke-dasharray="4 3"' if p["basis"]=="proposed reservation" else "")
        self.e.append('</g>')

    def done(self):
        return "\n".join(self.e+["</svg>"])


def plan(data,layer):
    c, parts = data["config"], data["parts"]
    s=SVG({"bottom":"Everyday vacuum bottom · top view", "core":"Electronics core · top view", "cap":"Cap and shared joints · top view"}[layer])
    s.text(30,54,"PLACEMENT STUDY · mm · front at top · component sources and allowances in report",12)
    scale,ox,oy=1.6,110,110
    w,d=c["body_mm"]
    s.rect(ox,oy,w*scale,d*scale,"#fafbfc")
    s.dim(ox,83,ox+w*scale,83,f'{number(w)} mm body width')
    s.line(30,oy,30,oy+d*scale,'class="dim"')
    s.text(48,oy+d*scale/2,number(d),12,"middle")
    if layer=="cap":
        ax,ay,aw,ah=c["cap_aperture_mm"]
        cx,cy,cw,cd=c["cap_outline_mm"]
        s.rect(ox+cx*scale,oy+cy*scale,cw*scale,cd*scale,"#e9eff4")
        s.rect(ox+ax*scale,oy+ay*scale,aw*scale,ah*scale,"white")
        for p in parts:
            if p["id"]=="lidar" or p["id"].startswith("top_joint") or p["id"]=="top_connector":
                s.part(p,scale,ox,oy)
        notes=["Core-fixed A1 in cap opening", f'Opening: {number(aw)} × {number(ah)} mm', "Cap lifts 70 mm over scanner", "Optional display remains open", "Four compact joint zones", "Round + slotted registration", "Different top/bottom keys", f'Whole cover: {number(cw)} × {number(cd)} mm']
    else:
        chosen=[p for p in parts if p["module"]==layer or (p["module"]=="interface" and (layer=="core" or p["id"].startswith("bottom")))]
        if layer=="core":
            for pocket in c["core_clearance_pockets"]:
                s.rect(ox+pocket["min"][0]*scale,oy+pocket["min"][1]*scale,pocket["size"][0]*scale,pocket["size"][1]*scale,"#f9e5d8",'stroke-dasharray="5 3"')
        # References drawn after enclosing reservations; height is shown in side view.
        for p in sorted(chosen,key=lambda p: "parent" in p):
            if layer=="core" and p["id"] in ("lidar", "scanner_pedestal"):
                s.rect(ox+p["min"][0]*scale,oy+p["min"][1]*scale,p["size"][0]*scale,p["size"][1]*scale,
                       "none",'stroke-dasharray="7 3"')
            else:
                s.part(p,scale,ox,oy)
        if layer=="bottom":
            labels={"head":"H", "bin_drawer":"B", "blower_bay":"V", "filter":"F", "wheel_driver_bay":"W", "bottom_mcu_bay":"M", "tool_power_bay":"P", "dirty_duct":"D"}
            notes=["H  Short pair / side drive", "D  Dirty-air corridor", "B  Bin slides rear with filter", "F  Vertical filter at bin right", "V  Upright blower in core well", "W  Wheel driver above head", "M  Bottom MCU above motor", "P  Separate tool power stages", "Side brush feeds gated inlet", "60 x 8 mm wheels; hubs open"]
        else:
            labels={"battery_tray":"B", "power_tray":"P", "pi_tray":"C", "core_mcu_bay":"M", "navigation_bay":"N", "front_sensor_bay":"S", "lidar":"L"}
            notes=["B  3S battery exits left", "C  Pi 4 tray exits right", "P  Protection + regulators", "M  Independent core supervisor", "N  Navigation / cable allowance", "S  Outward sensor bay", "L  A1 stays on the core", "Peach: open tool clearances", "Mate z=68; frame top z=113", "Vacuum towers stay on bottom"]
        by_id={p["id"]:p for p in chosen}
        for pid,label in labels.items():
            p=by_id[pid]
            x=ox+(p["min"][0]+p["size"][0]/2)*scale
            y=oy+(p["min"][1]+p["size"][1]/2)*scale
            if pid=="lidar":
                y=oy+(p["min"][1]-10)*scale
            s.rect(x-10,y-12,20,20,"white")
            s.text(x,y+3,label,14,"middle")
        if layer=="bottom":
            # Flow arrows are schematic centerlines, not manufactured ducts.
            for x1,y1,x2,y2 in [(137,73,137,132),(125,185,171,185),(193,185,223,185),(240,267,240,279),(5,186,37,167)]:
                s.line(ox+x1*scale,oy+y1*scale,ox+x2*scale,oy+y2*scale,
                       'stroke="#247d89" stroke-width="2" marker-end="url(#a)"')
    for i,note in enumerate(notes):
        s.text(573,139+i*29,note,13)
    for i,note in enumerate(["Green: owner dimensions", "Blue: manufacturer reference", "Purple: seller pack reference", "Grey: proposed space", "Amber: mating reservations"]):
        s.text(573,476+i*21,note,12)
    s.text(30,624,"Positions, clearances and empty bays are design proposals. Full coordinates and limits are in the report.",12)
    s.text(30,647,"Structure, wiring, port adapters and purchased mounts still need detailed fitting. Not fabrication geometry.",12)
    return s.done()


def side(data):
    c=data["config"]; by_id={p["id"]:p for p in data["parts"]}
    s=SVG("Complete stack · side projection",900,480)
    s.text(30,55,"Front at left. Left/center/right components share this projection; see top views for lateral separation.",12)
    scale,ox,floor=1.55,100,360
    d=c["body_mm"][1]
    for z0,z1,fill in [(0,c["bottom_mate_z_mm"],"#f5f8fa"),(c["bottom_mate_z_mm"],c["top_mate_z_mm"],"#edf2fc"),(c["top_mate_z_mm"],c["cap_top_z_mm"],"#d7e0ea")]:
        s.rect(ox,floor-z1*scale,d*scale,(z1-z0)*scale,fill)
    for pid in ["head","bin_drawer","filter_chamber","dirty_duct","wheel_driver_bay","blower","exhaust","battery_tray","battery","left_pickup","lidar","wheel_left","roller_1","roller_2"]:
        s.part(by_id[pid],scale,ox,0,axes=(1,2),floor=floor)
    s.line(ox-30,floor,ox+d*scale+30,floor,'stroke="#20344b" stroke-width="2"')
    s.dim(ox,floor+30,ox+d*scale,floor+30,f'{number(d)} mm body depth')
    h=data["derived"]["body_envelope_mm"][2]
    s.line(60,floor,60,floor-h*scale,'class="dim"')
    s.text(40,220,number(h),13,"middle")
    for i,line in enumerate([f'{number(h)} mm total; maximum 180', f'{number(c["cap_top_z_mm"])} mm cap top',f'{number(c["top_mate_z_mm"]-c["bottom_mate_z_mm"])} mm core frame height',f'{number(c["bottom_mate_z_mm"])} mm bottom mating plane', "60 mm wheel diameter", "Tool towers reach 105 mm", "Core has passive tool openings", "Mass / CG still unmeasured"]):
        s.text(600,105+i*30,line,13)
    s.text(30,435,"The main body stays outside 50 mm sofa gaps. The separate reaching bottom remains a later ground module.",12)
    s.text(30,458,"No lift system, flight mass estimate or fabrication parts are included.",12)
    return s.done()


def service(data):
    c=data["config"]; by_id={p["id"]:p for p in data["parts"]}
    s=SVG("Service and station access · top view",900,890)
    s.text(30,56,"Dashed boxes show full straight-line tray sweeps; paths are at different heights.",12)
    scale,ox,oy=1.4,200,90
    w,d=c["body_mm"]
    s.rect(ox,oy,w*scale,d*scale,"#f7f9fc")
    for item in data["checks"]["service_sweeps"]:
        p=item["sweep"]
        s.rect(ox+p["min"][0]*scale,oy+p["min"][1]*scale,p["size"][0]*scale,p["size"][1]*scale,"#ecf6f1",'stroke-dasharray="6 4"')
        for pid in item["member_ids"]:
            s.part(by_id[pid],scale,ox,oy)
        source=by_id[item["id"]]; delta=item["translation_mm"]
        cx,cy=[source["min"][i]+source["size"][i]/2 for i in [0,1]]
        s.line(ox+cx*scale,oy+cy*scale,ox+(cx+delta[0])*scale,oy+(cy+delta[1])*scale,'stroke="#24674e" stroke-width="2" marker-end="url(#a)"')
    for pid in ["left_pickup","right_pickup"]:
        s.part(by_id[pid],scale,ox,oy)
    s.text(35,150,"Battery: 100 mm stroke",13)
    s.text(640,150,"Pi: 140 mm stroke",13)
    s.text(640,171,"Rail above tray",12)
    s.text(ox+96,oy+390*scale,"Bin + filter: 160 mm rear stroke",13,"middle")
    s.text(ox+96,oy+411*scale,"Retract seal 3 mm right first",12,"middle")
    s.text(30,824,"Station reserves 80 mm side access per side, a 50 mm bottom drop and 310 mm rear transfer stroke.",12)
    s.text(30,848,"Dock tray top: 60 mm above floor; lower to 10 mm with core captured. Towers clear the core by 13 mm.",12)
    s.text(30,872,"Battery/Pi servicing occurs off the station or with its fingers withdrawn. Servicing and exchanging are separate states.",12)
    return s.done()


def report(data):
    c, d, checks=data["config"],data["derived"],data["checks"]
    lines=["# Full ground assembly placement", "", "Generated by `python3 design/ground/place_modules.py`. Placement only; not fabrication geometry.", "",
           f"Body: **{' × '.join(map(number,d['body_envelope_mm']))} mm**, including A1 height. Proposed side-brush sweep expands horizontal travel outline to **{' × '.join(map(number,d['moving_xy_size_mm']))} mm**; actual side brush is unmeasured.", "",
           f"Bottom/core mate z={c['bottom_mate_z_mm']} mm; core/cap mate z={c['top_mate_z_mm']} mm; cap top z={c['cap_top_z_mm']} mm. Main robot stays outside the 50 mm furniture gap.", "",
           f"Proposed clear debris cavity: {' × '.join(map(number,c['proposed_bin_clear_cavity_mm']['size']))} mm = **{d['gross_bin_cavity_l']:.3f} L gross**. The 0.5–0.6 L usable target allows for freeboard and collection details; it is not established by a bounding box.", "",
           "## Geometry checks", "", f"- {checks['root_pairs_checked']} independent reservation pairs checked in 3D; no positive-volume overlaps." if not checks["errors"] else "- FAILED; see errors below.",
           "- Reference parts fit their parent reservations; sibling references do not intersect. Parent/child volumes intentionally nest.",
           "- Battery, computer and bin translation sweeps clear modeled stationary reservations. Bin seal must retract first.",
           f"- Station bottom separation: {number(d['station_separation_mm'])} mm minus {number(c['station']['bottom_projection_above_mate_mm'])} mm mating projection = **{number(checks['separated_mate_clearance_mm'])} mm clearance**.",
           f"- Cap opening passes the scanner's entire reference footprint; {c['station']['cap_lift_mm']} mm lift leaves **{number(checks['cap_lift_clearance_mm'])} mm** above scanner top.",
           f"- Whole main panels: **{' × '.join(map(number,d['panel_blank_span_mm']))} mm**; actual brim, toolpath, flatness and strength unverified.",
           "- Rigid body and wheels fit275x275mm; every rigid part stays below180mm. Flexible bristles are explicitly exempt. Tool projections above the68mm mating plane fit reserved core openings.",
           "- Head/duct/bin routing reservations meet at faces. This is not a flow, sealing or pressure-loss calculation.","",checks["limits"],"",
           "## Coordinates and provenance", "", c["coordinates"], "", "Rows marked as children sit inside a reservation and are not additive assemblies. All placements are proposed regardless of the source of part dimensions.","",
           "| ID | Section / parent | Minimum x, y, z (mm) | Size x, y, z (mm) | Basis |", "|---|---|---|---|---|"]
    for p in data["parts"]:
        lines.append(f"| `{p['id']}` | {p['module']}"+(f" / {p['parent']}" if p.get("parent") else "")+f" | {', '.join(map(number,p['min']))} | {' × '.join(map(number,p['size']))} | {p['basis']} |")
    lines += ["", "## Sources and unmodeled detail", ""]
    for k,url in data["sources"].items():
        lines.append(f"- [{k.replace('_',' ')}]({url})")
    lines += ["", *[f"- {note}" for note in c["notes"]], "", "## Individual reservation notes", ""]
    lines += [f"- **{p['label']}:** {p['note']}" for p in data["parts"] if p.get("note")]
    return "\n".join(lines)+"\n"


def page(data):
    views=[("bottom","Vacuum bottom"),("core","Electronics core"),("cap","Cap / joints"),("side","Complete stack"),("service","Service paths")]
    options="".join(f'<option value="{v}">{label}</option>' for v,label in views)
    figures="".join(f'<figure data-view="{v}"{ " hidden" if v!="bottom" else ""}><img src="ground_{v}.svg" alt="{label}: dimensioned placement study"><figcaption><a href="ground_{v}.svg">Open standalone drawing</a></figcaption></figure>' for v,label in views)
    d=data["derived"]
    return f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TidyBot · Ground assembly placement</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;color:#20344b;background:#f2f5f8;margin:0}}main{{max-width:1040px;margin:30px auto;padding:24px;background:white;border-radius:12px}}h1{{font-size:30px;margin:0 0 8px}}.eyebrow{{color:#6a522b;font-weight:650;letter-spacing:.06em;font-size:12px}}select{{font:inherit;padding:8px;min-width:240px}}figure{{margin:20px 0}}img{{width:100%;height:auto}}figure[hidden]{{display:none}}a{{color:#245d8e}}.facts{{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0}}.facts span{{background:#edf2f8;padding:10px 14px;border-radius:6px}}p{{max-width:930px}}@media(max-width:600px){{main{{margin:0;padding:14px}}}}@media print{{select,label,figcaption{{display:none}}figure[hidden]{{display:block}}figure{{break-inside:avoid}}}}</style>
<main><div class="eyebrow">PLACEMENT STUDY · 6 SEPTEMBER 2026 · DIMENSIONS ADJUSTABLE</div>
<h1>Core, vacuum bottom and cap</h1>
<p>The short roller pair leads into a rear-service bin. Its upright filter and blower rise into passive
openings in the electronics frame, staying attached to the bottom. Battery and Pi trays slide out opposite sides.</p>
<div class="facts"><span><b>{' × '.join(map(number,d['body_envelope_mm']))} mm</b> rigid body, including LiDAR</span><span><b>0.5–0.6 L</b> usable bin target</span><span><b>270 × 270 mm</b> whole main panels</span></div>
<label for="view">View: </label><select id="view">{options}</select>
{figures}
<p><b>Owner limits: 275 × 275 mm rigid footprint and 180 mm total height.</b> Flexible bristles may extend.
The owner reports 60 × 8 mm drive wheels with a 3 mm center hole and no hub protrusion; the proposed 4 mm-shaft gearmotor needs a qualified bolt-on adapter. Part references nest inside proposed spaces. The side brush size, powered roller drive,
mounts, seals, cooling, wiring and automatic latch hardware remain to detail. The 70 mm brush placeholder
expands the moving outline to {' × '.join(map(number,d['moving_xy_size_mm']))} mm. No mass or flight capability is implied.</p>
<p>Checked: owner size limits, reference containment, 3D interference, core pockets, three service sweeps,
cap removal, station separation and whole panel spans. These checks cover the modeled envelopes; structural and
cleaning performance remain unverified.</p>
<p><a href="ground_report.md">Coordinates and check report</a> · <a href="ground_layout.json">Machine-readable placement</a> ·
<a href="ground_placement.FCStd">FreeCAD model</a> · <a href="ground_placement.step">STEP model</a> ·
<a href="../../../docs/GROUND_PLACEMENT.md">Design decisions and next build work</a> ·
<a href="vacuum_head_layout.html">Roller-length comparison</a></p>
</main><script>
const selector = document.getElementById('view');
const figures = [...document.querySelectorAll('figure[data-view]')];
function selectView() {{ for (const f of figures) f.hidden = f.dataset.view !== selector.value; }}
selector.addEventListener('change', selectView);
selectView();
</script></html>'''


def main():
    data=build_layout()
    if data["checks"]["errors"]:
        raise ValueError("\n".join(data["checks"]["errors"]))
    OUTPUT.mkdir(parents=True,exist_ok=True)
    for layer in ["bottom","core","cap"]:
        (OUTPUT/f"ground_{layer}.svg").write_text(plan(data,layer))
    (OUTPUT/"ground_side.svg").write_text(side(data))
    (OUTPUT/"ground_service.svg").write_text(service(data))
    (OUTPUT/"ground_layout.json").write_text(json.dumps(data,indent=2)+"\n")
    (OUTPUT/"ground_report.md").write_text(report(data))
    (OUTPUT/"ground_layout.html").write_text(page(data))
    print(f"Generated ground placement: {len(data['parts'])} reservations/references; {data['checks']['root_pairs_checked']} root-pair checks; 3 service sweeps clear.")


if __name__=="__main__":
    main()
