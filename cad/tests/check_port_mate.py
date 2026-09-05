# =============================================================================
#  TidyBot -- TB-Port mate validation
# =============================================================================
#  A regression test for the interface geometry. Run it after ANY change to
#  cad/lib/tidybot_port.py, before printing anything.
#
#      freecad.cmd check_port_mate.py       (or: make -C cad check)
#
#  It asserts the property the whole coupling depends on: when seated, the two
#  printed halves do NOT touch. All load goes through steel. If plastic
#  interferes, the coupling is over-constrained and repeatability is gone.
# =============================================================================

import os
import sys

import math

import Part
import FreeCAD as App
from FreeCAD import Vector

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "lib"))

from tidybot_port import PORT, derived, male_port, female_port  # noqa: E402
from coupon import build_male, build_female  # noqa: E402

CLASH_TOL_CM3 = 0.01

failures = []


def _say(msg):
    # FreeCAD discards buffered stdout on sys.exit(), so flush every line.
    print(msg)
    sys.stdout.flush()


def check(label, ok, detail):
    _say("  [%s] %-34s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        failures.append(label)


def main():
    _say("TB-Port %s -- mate validation\n" % PORT["SPEC_VERSION"])
    d = derived()
    m = male_port()
    f = female_port()

    _say("GEOMETRY")
    for name, s in (("male", m), ("female", f)):
        check("%s is a valid solid" % name,
              s.isValid() and len(s.Solids) == 1,
              "%d solid(s), %.1f cm3, ~%.0f g PETG @45%%"
              % (len(s.Solids), s.Volume / 1000.0, s.Volume / 1000.0 * 1.27 * 0.45))

    _say("\nMATE")
    # Seat the female: flip it, then lift it by the designed flange gap.
    fm = f.copy()
    fm.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 180)
    fm.translate(Vector(0, 0, PORT["FLANGE_GAP"]))

    clash = m.common(fm)
    vol = clash.Volume / 1000.0
    check("no plastic-on-plastic contact", vol < CLASH_TOL_CM3,
          "interference %.4f cm3 (tol %.2f)" % (vol, CLASH_TOL_CM3))

    check("boss does not bottom out", d["TIP_CLEARANCE"] >= 1.0,
          "%.2f mm of air below the seated boss tip" % d["TIP_CLEARANCE"])

    check("key engages before contacts",
          PORT["KEY_PROTRUSION"] > PORT["CONTACT_POGO_DEPTH"] - PORT["CONTACT_DEPTH"],
          "key %.1f mm vs contact travel %.1f mm"
          % (PORT["KEY_PROTRUSION"], PORT["CONTACT_POGO_DEPTH"] - PORT["CONTACT_DEPTH"]))

    check("parallel engagement sufficient", d["ENGAGEMENT"] >= 6.0,
          "%.2f mm after the funnel" % d["ENGAGEMENT"])

    # The coupon is what actually gets printed. Validating only the raw port
    # missed a bug where fusing the coupon plate back-filled every kinematic
    # ball socket -- geometry correct in male_port(), absent from the STL.
    # Check the artifact, not the ideal.
    _say("\nCOUPON AS PRINTED")
    cm, cf = build_male(), build_female()

    socket_depth = PORT["KC_BALL_DIA"] - PORT["KC_PROTRUSION"]
    for ang in PORT["KC_ANGLES"]:
        a = math.radians(ang)
        x = PORT["KC_BOLT_CIRCLE"] / 2.0 * math.cos(a)
        y = PORT["KC_BOLT_CIRCLE"] / 2.0 * math.sin(a)
        probe = Part.makeCylinder(PORT["KC_SOCKET_DIA"] / 2.0, socket_depth,
                                  Vector(x, y, -socket_depth), Vector(0, 0, 1))
        void = probe.Volume - cm.common(probe).Volume
        check("ball socket open @ %.0f deg" % ang, void > probe.Volume * 0.9,
              "%.0f of %.0f mm3 clear" % (void, probe.Volume))

    for ang in PORT["KC_ANGLES"]:
        a = math.radians(ang)
        x = PORT["KC_BOLT_CIRCLE"] / 2.0 * math.cos(a)
        y = PORT["KC_BOLT_CIRCLE"] / 2.0 * math.sin(a)
        probe = Part.makeCylinder(3.0, 2.0, Vector(x, y, -3.0), Vector(0, 0, 1))
        void = probe.Volume - cf.common(probe).Volume
        check("vee pocket open @ %.0f deg" % ang, void > probe.Volume * 0.9,
              "%.0f of %.0f mm3 clear" % (void, probe.Volume))

    for name, shape in (("male", cm), ("female", cf)):
        check("%s coupon is one solid" % name,
              shape.isValid() and len(shape.Solids) == 1,
              "%d solid(s), %.1f cm3" % (len(shape.Solids), shape.Volume / 1000.0))

    _say("\nPRINTABILITY (ADR 0005)")
    for name, shape in (("male coupon", cm), ("female coupon", cf)):
        bb = shape.BoundBox
        check("%s fits TAZ 6 volume" % name,
              max(bb.XLength, bb.YLength) <= 250.0 and bb.ZLength <= 230.0,
              "%.1f x %.1f x %.1f mm" % (bb.XLength, bb.YLength, bb.ZLength))

    _say("")
    if failures:
        _say("FAILED: %s" % ", ".join(failures))
        sys.exit(1)
    _say("All checks passed.")


main()
