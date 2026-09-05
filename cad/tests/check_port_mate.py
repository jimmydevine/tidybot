# =============================================================================
#  TidyBot -- TB-Port validation  (spec 0.2.0)
# =============================================================================
#  Run after ANY change to cad/lib/tidybot_port.py, before printing.
#      freecadcmd check_port_mate.py        (or: make -C cad check)
#
#  v0.1's checks compared plastic to plastic and passed while the coupling
#  could not physically work -- the balls never reached their dowels. These
#  checks model the STEEL: posts seated in sockets, pins through their
#  cross-holes. They assert that parts touch where they must and clear where
#  they must, and that a wrong orientation is physically blocked.
# =============================================================================

import math
import os
import sys

import Part
import FreeCAD as App
from FreeCAD import Vector

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "lib"))

from tidybot_port import (PORT, LOAD, derived, module_port,   # noqa: E402
                          base_port, steel_post)
from coupon import build_module_coupon, build_base_coupon            # noqa: E402

failures = []


def _say(msg):
    print(msg)
    sys.stdout.flush()


def check(label, ok, detail):
    _say("  [%s] %-36s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        failures.append(label)


def seat_base(shape):
    """Flip the base half and lift it by FLANGE_GAP -- the mated position."""
    s = shape.copy()
    s.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 180)
    s.translate(Vector(0, 0, PORT["FLANGE_GAP"]))
    return s


def polar(r, a):
    return r * math.cos(math.radians(a)), r * math.sin(math.radians(a))


def main():
    p, d = PORT, derived()
    _say("TB-Port %s -- validation\n" % p["SPEC_VERSION"])

    m = module_port()
    b = base_port()
    bm = seat_base(b)

    _say("GEOMETRY")
    for name, s in (("module half", m), ("base half", b)):
        check("%s is a valid solid" % name,
              s.isValid() and len(s.Solids) == 1,
              "%d solid(s), %.1f cm3, ~%.0f g PETG"
              % (len(s.Solids), s.Volume / 1000.0, s.Volume / 1000.0 * 1.27 * 0.45))

    _say("\nMATE -- plastic must NOT touch")
    clash = m.common(bm).Volume / 1000.0
    check("no plastic-on-plastic contact", clash < 0.01,
          "%.4f cm3 across a %.1f mm designed gap" % (clash, p["FLANGE_GAP"]))

    check("socket pattern mirrors the posts",
          tuple(sorted(d["SOCKET_ANGLES"])) == tuple(sorted((-a) % 360.0 for a in p["POST_ANGLES"])),
          "posts %s -> sockets %s"
          % ("/".join("%.0f" % a for a in p["POST_ANGLES"]),
             "/".join("%.0f" % a for a in d["SOCKET_ANGLES"])))

    _say("\nSTEEL -- modelled as hardware, not assumed")
    posts = [steel_post(p, a) for a in p["POST_ANGLES"]]

    # The posts must be steel, so there must be NOTHING printed where they go.
    printed_in_post_space = max(q.common(m).Volume for q in posts)
    press = math.pi * ((p["POST_DIA"] / 2.0) ** 2 - (p["POST_BORE_DIA"] / 2.0) ** 2) \
        * p["POST_EMBED"] * 3.0
    check("posts are steel, not printed", printed_in_post_space < press * 1.5,
          "%.0f mm3 overlap = the %.2f mm press fit only"
          % (printed_in_post_space, (p["POST_DIA"] - p["POST_BORE_DIA"]) / 2.0))

    worst_fit = max(q.common(bm).Volume for q in posts)
    check("posts seat without binding", worst_fit < 1.0,
          "%.2f mm3 interference, %.2f mm radial clearance"
          % (worst_fit, (d["SOCKET_DIA"] - p["POST_DIA"]) / 2.0))

    pin_z = p["PIN_HOLE_Z"]
    worst_pin = 0.0
    for ang, post in zip(p["POST_ANGLES"], posts):
        x, y = polar(p["POST_BC"] / 2.0, ang)
        ux, uy = polar(1.0, ang)
        pin = Part.makeCylinder(p["PIN_DIA"] / 2.0, 60.0,
                                Vector(x - ux * 30.0, y - uy * 30.0, pin_z),
                                Vector(ux, uy, 0))
        worst_pin = max(worst_pin, pin.common(post).Volume,
                        pin.common(m).Volume, pin.common(bm).Volume)
    check("pin clears the dowel cross-hole", worst_pin < 1.0,
          "%.2f mm3 obstruction through steel and plastic alike" % worst_pin)

    check("boss wall survives the press fit", d["BOSS_WALL"] >= 3.0,
          "%.1f mm of PETG around a Ø%.2f bore" % (d["BOSS_WALL"], p["POST_BORE_DIA"]))
    check("post grip is at least one diameter", p["POST_EMBED"] >= p["POST_DIA"],
          "%.0f mm embedded in a Ø%.0f post" % (p["POST_EMBED"], p["POST_DIA"]))

    check("pin bore has base material above it", d["PIN_BORE_COVER"] >= 3.0,
          "%.2f mm of cover" % d["PIN_BORE_COVER"])

    _say("\nSEQUENCE -- the cone must land before the posts")
    check("cone leads the posts", d["CONE_LEAD"] >= 3.0,
          "%.1f mm (cone %.0f, posts %.0f)" % (d["CONE_LEAD"], p["CONE_LEN"], p["POST_LEN"]))
    check("cone capture exceeds post capture", d["CONE_CAPTURE"] > d["POST_CAPTURE"],
          "cone %.1f mm kills lateral, posts %.1f mm kill yaw"
          % (d["CONE_CAPTURE"], d["POST_CAPTURE"]))

    _say("\nKEYING -- a wrong orientation must be impossible")
    # Rotate the ASSEMBLED module -- plate plus its steel posts. Rotating the
    # printed half alone proves nothing now that the posts are hardware.
    assembled = m
    for q in posts:
        assembled = assembled.fuse(q)
    for phi in (120.0, 240.0):
        wrong = assembled.copy()
        wrong.rotate(Vector(0, 0, 0), Vector(0, 0, 1), phi)
        blocked = wrong.common(bm).Volume
        check("blocked at %.0f deg" % phi, blocked > 100.0,
              "%.0f mm3 of collision -- cannot enter" % blocked)
    check("misfit far exceeds clearance",
          d["KEY_MISFIT_MM"] > 5.0 * p["SOCKET_CLEARANCE"],
          "%.2f mm misfit vs %.2f mm clearance"
          % (d["KEY_MISFIT_MM"], p["SOCKET_CLEARANCE"]))

    _say("\nCONTAMINATION -- every socket must drain")
    for ang in d["SOCKET_ANGLES"]:
        x, y = polar(p["POST_BC"] / 2.0, ang)
        ux, uy = polar(1.0, ang)
        rr = p["PLATE_DIA"] / 2.0 + 2.0
        probe = Part.makeSphere(1.5, Vector(ux * rr, uy * rr,
                                            -d["SOCKET_DEPTH"] + p["DRAIN_DIA"] / 2.0
                                            - (rr - p["POST_BC"] / 2.0) * 0.15))
        check("socket at %3.0f deg drains outward" % ang,
              probe.common(b).Volume < probe.Volume * 0.5,
              "drain exits the side wall")

    _say("\nCOUPON AS PRINTED")
    cm, cb = build_module_coupon(), build_base_coupon()
    for name, s in (("module", cm), ("base", cb)):
        bb = s.BoundBox
        check("%s coupon is one solid" % name,
              s.isValid() and len(s.Solids) == 1,
              "%d solid(s), %.1f cm3" % (len(s.Solids), s.Volume / 1000.0))
        check("%s coupon fits TAZ 6" % name,
              max(bb.XLength, bb.YLength) <= 250.0 and bb.ZLength <= 230.0,
              "%.1f x %.1f x %.1f mm" % (bb.XLength, bb.YLength, bb.ZLength))

    _say("\nMARGINS")
    check("pin double shear", d["PIN_MARGIN"] >= 10.0,
          "%.0fx on the %.0f N flight load" % (d["PIN_MARGIN"], LOAD["AXIAL_TOP_N"]))
    check("bearing on PETG", d["BEARING_MARGIN"] >= 3.0,
          "%.1f MPa, %.0fx margin" % (d["BEARING_MPA"], d["BEARING_MARGIN"]))

    _say("")
    if failures:
        _say("FAILED: %s" % ", ".join(failures))
        sys.exit(1)
    _say("All checks passed.")


main()
