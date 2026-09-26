"""Run with freecadcmd design/ground/export_placement.py after place_modules.py.

Exports named reference solids and wire reservation boxes, not printable parts.
"""
import json
import os
from pathlib import Path

import FreeCAD as App
import Part

ROOT = Path(os.environ.get("TIDYBOT_PROJECT_ROOT", Path.cwd())).resolve()
OUT = ROOT / "design/ground/output"
data = json.loads((OUT / "ground_layout.json").read_text())
if data["checks"]["errors"]:
    raise ValueError("Regenerate and resolve placement errors before exporting")
doc = App.newDocument("GroundPlacement")
features = []


def feature(name, shape, basis, space=False):
    if shape.isNull() or not shape.isValid():
        raise ValueError(f"Invalid export shape: {name}")
    obj = doc.addObject("PartDesign::Feature", f"Placement{len(features):03d}")
    obj.Label = name
    obj.Shape = Part.makeCompound(shape.Edges) if space else shape
    obj.addProperty("App::PropertyString", "StudyScope").StudyScope = "Placement only; NOT fabrication geometry"
    obj.addProperty("App::PropertyString", "DimensionBasis").DimensionBasis = basis
    if obj.ViewObject:
        obj.ViewObject.ShapeColor = (0.65,0.83,0.78) if basis.startswith("owner") else (0.65,0.77,0.9)
        obj.ViewObject.LineColor = (0.4,0.45,0.5)
    features.append(obj)


for p in data["parts"]:
    x,y,z=p["min"]; w,d,h=p["size"]
    if p["shape"]=="cylinder_x":
        shape=Part.makeCylinder(d/2,w,App.Vector(x,y+d/2,z+h/2),App.Vector(1,0,0))
    elif p["shape"]=="cylinder_z":
        shape=Part.makeCylinder(w/2,h,App.Vector(x+w/2,y+d/2,z),App.Vector(0,0,1))
    else:
        shape=Part.makeBox(w,d,h,App.Vector(x,y,z))
    is_space = p["basis"]=="proposed reservation"
    feature(("SPACE: " if is_space else "REF: ")+p["label"],shape,p["basis"],is_space)

c=data["config"]; w,d=c["body_mm"]
for name,z0,z1 in [("Bottom boundary",0,c["bottom_mate_z_mm"]),("Core boundary",c["bottom_mate_z_mm"],c["top_mate_z_mm"])]:
    feature(name,Part.makeBox(w,d,z1-z0,App.Vector(0,0,z0)),"Proposed section boundary",True)
# Cap is an outline with a through-opening. Do not imply a solid ten-mm cover.
cx,cy,cw,cd=c["cap_outline_mm"]
cap=Part.makeBox(cw,cd,c["cap_top_z_mm"]-c["top_mate_z_mm"],App.Vector(cx,cy,c["top_mate_z_mm"]))
ax,ay,aw,ah=c["cap_aperture_mm"]
opening=Part.makeBox(aw,ah,100,App.Vector(ax,ay,c["top_mate_z_mm"]-10))
feature("Cap boundary / scanner opening",cap.cut(opening),"Proposed cover envelope, not material thickness",True)
for pocket in c["core_clearance_pockets"]:
    feature("CORE OPENING: "+pocket["id"],Part.makeBox(*pocket["size"],App.Vector(*pocket["min"])),
            "Passive opening for bottom-owned vacuum tower; must remain free of core structure",True)
doc.recompute()
doc.saveAs(str(OUT/"ground_placement.FCStd"))
Part.export(features,str(OUT/"ground_placement.step"))
print(f"EXPORTED ground placement: {len(features)} valid reference / wire-envelope features")
App.closeDocument(doc.Name)
