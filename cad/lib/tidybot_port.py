# =============================================================================
#  TidyBot -- TB-Port interface geometry  (SPEC VERSION 0.2.0)
# =============================================================================
#  THE authoritative definition of the module interface. Every module imports
#  this file. Nothing anywhere else may re-declare a port dimension.
#
#  Architecture: three identical tapered steel posts per face, retained by
#  cross pins in double shear, with all electricals in a sealed central
#  connector. Rationale: docs/decisions/0006-tri-post-coupling.md
#  Prose spec: docs/INTERFACE.md
#
#  Supersedes the 0.1.0 boss-and-bore geometry (git tag / commit 2c18923).
#
#  The PORT dict and derived() import under plain CPython -- no FreeCAD --
#  so firmware and test tooling read the same numbers:
#      python3 -c "from tidybot_port import PORT; print(PORT['POST_DIA'])"
#
#  COORDINATE CONVENTION -- both halves are built in their natural PRINT
#  orientation, features growing +Z off the bed:
#
#      module_port_parts()  plate z = -PLATE_THK..0, posts and cone grow +Z
#      base_port_parts()    face at z = 0, body grows -Z, sockets open upward
#
#  To mate, the base half is flipped and lifted by FLANGE_GAP.
# =============================================================================

import itertools
import math

SPEC_VERSION = "0.2.0"

# ----------------------------------------------------------------------------
#  PARAMETERS -- the interface. Changing anything here is a spec change:
#  bump SPEC_VERSION, update docs/INTERFACE.md, run `make -C cad check`.
# ----------------------------------------------------------------------------
PORT = dict(
    SPEC_VERSION      = SPEC_VERSION,

    # --- Overall footprint --------------------------------------------------
    PLATE_DIA         = 130.0,
    PLATE_THK         = 6.0,

    # --- Posts: 3, IDENTICAL, unequally spaced ------------------------------
    #  The 5 deg asymmetry at 235 is the keying feature. It makes a wrong
    #  orientation miss by ~4.4 mm against a 0.2 mm clearance -- mechanically
    #  impossible rather than merely discouraged. Keep the posts identical:
    #  one dowel size, one socket, one lip seal, one reamer, one spare.
    POST_ANGLES       = (0.0, 120.0, 235.0),
    POST_BC           = 100.0,   # bolt circle dia -> r = 50
    POST_DIA          = 10.0,
    POST_TIP_DIA      = 6.0,     # taper does the capture, on the post
    POST_TAPER_ANGLE  = 30.0,    # from the post axis; steeper = capture without length
    POST_LEN          = 18.0,    # protrusion from the module face
    SOCKET_CLEARANCE  = 0.20,    # diametral

    # --- Locking pins: double shear, driven by a cam plate INSIDE the base --
    PIN_DIA           = 5.0,
    PIN_HOLE_Z        = 9.0,     # cross-hole centre, above the module face
    PIN_CLEARANCE     = 0.15,

    # --- Central connector cone: engages FIRST, kills lateral error ---------
    #  It sits at r = 0, so yaw cannot displace it. That is the whole point:
    #  cone kills lateral, posts kill yaw. One feature, one job.
    CONE_BASE_DIA     = 40.0,
    CONE_TIP_DIA      = 30.0,
    CONE_LEN          = 22.0,    # > POST_LEN + 3 so it lands well before the posts
    CONE_CLEARANCE    = 0.30,
    CONTACT_COUNT     = 8,
    CONTACT_W         = 22.0,
    CONTACT_L         = 10.0,
    CONTACT_DEPTH     = 1.6,
    CONTACT_POGO_DEPTH= 6.0,

    # --- Sealing and drainage (ADR 0006, section on contamination) ----------
    GASKET_BC         = 118.0,   # groove on the BASE half; one gasket, not N
    GASKET_W          = 4.0,
    GASKET_H          = 2.0,
    DRAIN_DIA         = 4.0,     # from each socket floor, out the SIDE wall
    LIP_SEAL_W        = 1.5,

    FLANGE_GAP        = 1.0,     # designed air gap; steel carries the load
)

# Design loads -- ADR 0007. Not geometry, but every margin below refers to them.
LOAD = dict(
    AXIAL_TOP_N       = 192.0,   # 3-stack flight, top port
    AXIAL_BOTTOM_N    = 59.0,
    MOMENT_NM         = 4.0,
)


# ----------------------------------------------------------------------------
#  DERIVED GEOMETRY + GUARDS
#  Everything here is solved from the parameters, so a parameter change
#  re-solves instead of silently invalidating a hand-entered number. The
#  guards refuse specs that cannot work -- v0.1 shipped three bugs that a
#  guard would have caught.
# ----------------------------------------------------------------------------
def derived(p=None):
    p = p or PORT
    d = {}

    # --- Post taper: the capture feature, riding on the post ---------------
    dr = (p["POST_DIA"] - p["POST_TIP_DIA"]) / 2.0
    if dr <= 0:
        raise ValueError("POST_TIP_DIA must be smaller than POST_DIA")
    d["POST_CAPTURE"]   = dr
    d["POST_TAPER_LEN"] = dr / math.tan(math.radians(p["POST_TAPER_ANGLE"]))

    d["SOCKET_DIA"]   = p["POST_DIA"] + p["SOCKET_CLEARANCE"]
    d["SOCKET_DEPTH"] = p["POST_LEN"] + 2.0

    # --- Cone: engages before the posts ------------------------------------
    d["CONE_CAPTURE"]      = (p["CONE_BASE_DIA"] - p["CONE_TIP_DIA"]) / 2.0
    d["CONE_RECESS_DEPTH"] = p["CONE_LEN"] + 3.0
    d["CONE_LEAD"]         = p["CONE_LEN"] - p["POST_LEN"]
    if d["CONE_LEAD"] < 3.0:
        raise ValueError(
            "Cone leads the posts by only %.1f mm. It must land first and settle "
            "the lateral error before any post enters, or the posts inherit a job "
            "they cannot do (see ADR 0006)." % d["CONE_LEAD"])

    # --- Receptacle depth and volume consumed ------------------------------
    d["RECEPTACLE_DEPTH"] = max(d["SOCKET_DEPTH"], d["CONE_RECESS_DEPTH"])
    v_sockets = 3 * math.pi * (d["SOCKET_DIA"] / 2.0) ** 2 * d["SOCKET_DEPTH"]
    r1, r2 = p["CONE_BASE_DIA"] / 2.0, p["CONE_TIP_DIA"] / 2.0
    v_cone = math.pi / 3.0 * d["CONE_RECESS_DEPTH"] * (r1*r1 + r1*r2 + r2*r2)
    d["VOL_SOCKETS"] = v_sockets
    d["VOL_CONE"]    = v_cone
    d["VOL_TOTAL"]   = v_sockets + v_cone

    # --- Mirror handedness -------------------------------------------------
    #  The two faces meet each other, so they are mirror images. A module post
    #  at angle a must find a base socket at -a. With the old symmetric
    #  0/120/240 layout this was invisible (the set mirrors onto itself); the
    #  asymmetric keying layout makes it real, and getting it wrong means
    #  nothing mates at all.
    d["SOCKET_ANGLES"] = tuple((-a) % 360.0 for a in p["POST_ANGLES"])

    # --- Keying: a wrong orientation must be physically impossible ---------
    r = p["POST_BC"] / 2.0
    A = [a % 360.0 for a in p["POST_ANGLES"]]
    worst = 1e9
    for phi in (120.0, 240.0):
        rot = [(a + phi) % 360.0 for a in A]
        best = 1e9
        for perm in itertools.permutations(rot):
            err = max(min(abs(x - a), 360.0 - abs(x - a)) for x, a in zip(perm, A))
            best = min(best, err)
        worst = min(worst, best)
    d["KEY_MISFIT_DEG"] = worst
    d["KEY_MISFIT_MM"]  = r * math.radians(worst)
    if d["KEY_MISFIT_MM"] < 5.0 * p["SOCKET_CLEARANCE"]:
        raise ValueError(
            "POST_ANGLES %s let the module mate in more than one orientation: a "
            "wrong orientation misses by only %.2f mm against %.2f mm of clearance. "
            "Break the symmetry (see ADR 0006)."
            % (p["POST_ANGLES"], d["KEY_MISFIT_MM"], p["SOCKET_CLEARANCE"]))

    # --- Load-centroid offset, the cost of that asymmetry ------------------
    cx = sum(math.cos(math.radians(a)) for a in A) / 3.0 * r
    cy = sum(math.sin(math.radians(a)) for a in A) / 3.0 * r
    d["CENTROID_OFFSET"] = math.hypot(cx, cy)
    d["LOAD_IMBALANCE_NM"] = LOAD["AXIAL_TOP_N"] * d["CENTROID_OFFSET"] / 1000.0

    # --- Margins -----------------------------------------------------------
    A_shear = 2.0 * math.pi * (p["PIN_DIA"] / 2.0) ** 2   # double shear
    d["PIN_CAPACITY_N"]  = A_shear * 200.0                # mild steel, conservative
    d["PIN_LOAD_N"]      = LOAD["AXIAL_TOP_N"] / 3.0
    d["PIN_MARGIN"]      = d["PIN_CAPACITY_N"] / d["PIN_LOAD_N"]
    wall = (d["SOCKET_DIA"] - p["PIN_DIA"]) / 2.0 + p["PIN_DIA"]
    d["BEARING_MPA"]     = d["PIN_LOAD_N"] / (p["PIN_DIA"] * p["PIN_DIA"])
    d["BEARING_MARGIN"]  = 50.0 / d["BEARING_MPA"]        # PETG compressive
    if d["BEARING_MARGIN"] < 3.0:
        raise ValueError("Pin bearing margin only %.1fx on printed plastic."
                         % d["BEARING_MARGIN"])

    # --- Enough base material above the pin bore ---------------------------
    #  The pin bore is a hole in the base near the mating face. Too close and
    #  it breaks out into the face under load.
    d["PIN_BORE_COVER"] = (p["PIN_HOLE_Z"] - p["FLANGE_GAP"]
                           - (p["PIN_DIA"] + p["PIN_CLEARANCE"]) / 2.0)
    if d["PIN_BORE_COVER"] < 3.0:
        raise ValueError(
            "Only %.1f mm of base material between the pin bore and the mating "
            "face. It will break out. Raise PIN_HOLE_Z or lengthen the post."
            % d["PIN_BORE_COVER"])

    # --- Pin must actually pass through the post ---------------------------
    if p["PIN_HOLE_Z"] + p["PIN_DIA"] / 2.0 > p["POST_LEN"] - d["POST_TAPER_LEN"]:
        raise ValueError(
            "The cross-hole at z=%.1f runs into the taper, which starts at %.1f. "
            "The pin would bear on a conical surface instead of a cylindrical one."
            % (p["PIN_HOLE_Z"], p["POST_LEN"] - d["POST_TAPER_LEN"]))
    return d


# ----------------------------------------------------------------------------
#  FREECAD GEOMETRY  (imported lazily; module stays CPython-importable)
# ----------------------------------------------------------------------------
def _fc():
    import Part
    import FreeCAD as App
    return Part, App


def _polar(radius, angle_deg):
    a = math.radians(angle_deg)
    return radius * math.cos(a), radius * math.sin(a)


def _rotated(shape, angle_deg):
    _, App = _fc()
    s = shape.copy()
    s.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), angle_deg)
    return s


def module_port_parts(p=None):
    """Male half, on every module: (additive_solid, [cut_tools]).

    Plate at z = -PLATE_THK..0; three tapered posts and the connector cone
    grow +Z. Prints as generated, features up, no supports.

    Use attach() -- never host.fuse(module_port()) -- when putting this on a
    module body. Fusing over a finished port back-fills its recesses.
    """
    Part, App = _fc()
    p = p or PORT
    d = derived(p)
    Z = App.Vector(0, 0, 1)
    cuts = []

    body = Part.makeCylinder(p["PLATE_DIA"] / 2.0, p["PLATE_THK"],
                             App.Vector(0, 0, -p["PLATE_THK"]), Z)

    # --- three identical tapered posts -------------------------------------
    straight = p["POST_LEN"] - d["POST_TAPER_LEN"]
    for ang in p["POST_ANGLES"]:
        x, y = _polar(p["POST_BC"] / 2.0, ang)
        body = body.fuse(Part.makeCylinder(
            p["POST_DIA"] / 2.0, straight, App.Vector(x, y, 0.0), Z))
        body = body.fuse(Part.makeCone(
            p["POST_DIA"] / 2.0, p["POST_TIP_DIA"] / 2.0, d["POST_TAPER_LEN"],
            App.Vector(x, y, straight), Z))
        # cross-hole for the locking pin, in the cylindrical section.
        # RADIAL, matching the cam plate that drives the pins -- not along X,
        # or only the post at 0 deg would line up.
        ux, uy = _polar(1.0, ang)
        cuts.append(Part.makeCylinder(
            (p["PIN_DIA"] + p["PIN_CLEARANCE"]) / 2.0, p["POST_DIA"] * 3.0,
            App.Vector(x - ux * p["POST_DIA"] * 1.5, y - uy * p["POST_DIA"] * 1.5,
                       p["PIN_HOLE_Z"]),
            App.Vector(ux, uy, 0.0)))

    # --- central connector cone: lands first, kills lateral error ----------
    body = body.fuse(Part.makeCone(
        p["CONE_BASE_DIA"] / 2.0, p["CONE_TIP_DIA"] / 2.0, p["CONE_LEN"],
        App.Vector(0, 0, 0), Z))
    # contact pad PCB recess in the cone tip
    cuts.append(Part.makeBox(
        p["CONTACT_W"], p["CONTACT_L"], p["CONTACT_DEPTH"] + 0.1,
        App.Vector(-p["CONTACT_W"] / 2.0, -p["CONTACT_L"] / 2.0,
                   p["CONE_LEN"] - p["CONTACT_DEPTH"])))
    # harness bore up the cone axis
    cuts.append(Part.makeCylinder(
        8.0, p["CONE_LEN"] + p["PLATE_THK"] + 2.0,
        App.Vector(0, 0, -p["PLATE_THK"] - 1.0), Z))
    return body, cuts


def base_port_parts(p=None):
    """Female half, on the base: (additive_solid, [cut_tools]).

    Face at z = 0, body grows -Z, sockets open upward. Prints as generated.
    Every socket drains out the SIDE wall -- never into the electronics.
    """
    Part, App = _fc()
    p = p or PORT
    d = derived(p)
    Z = App.Vector(0, 0, 1)
    cuts = []

    depth = d["RECEPTACLE_DEPTH"] + p["PLATE_THK"]
    body = Part.makeCylinder(p["PLATE_DIA"] / 2.0, depth,
                             App.Vector(0, 0, -depth), Z)

    for ang in d["SOCKET_ANGLES"]:
        x, y = _polar(p["POST_BC"] / 2.0, ang)
        # socket
        cuts.append(Part.makeCylinder(
            d["SOCKET_DIA"] / 2.0, d["SOCKET_DEPTH"] + 0.1,
            App.Vector(x, y, -d["SOCKET_DEPTH"]), Z))
        # lead-in chamfer at the socket mouth, so the taper meets a taper
        cuts.append(Part.makeCone(
            d["SOCKET_DIA"] / 2.0 + 1.2, d["SOCKET_DIA"] / 2.0, 1.2,
            App.Vector(x, y, -1.2), Z))
        # radial bore for the locking pin, driven from inside the base
        z_pin = -(p["PIN_HOLE_Z"] - p["FLANGE_GAP"])
        ux, uy = _polar(1.0, ang)
        cuts.append(Part.makeCylinder(
            (p["PIN_DIA"] + p["PIN_CLEARANCE"]) / 2.0, p["PLATE_DIA"] / 2.0,
            App.Vector(x - ux * 40.0, y - uy * 40.0, z_pin),
            App.Vector(ux, uy, 0.0)))
        # drain: socket floor -> out through the side wall
        cuts.append(Part.makeCylinder(
            p["DRAIN_DIA"] / 2.0, p["PLATE_DIA"],
            App.Vector(x, y, -d["SOCKET_DEPTH"] + p["DRAIN_DIA"] / 2.0),
            App.Vector(ux, uy, -0.15)))

    # --- connector cone recess --------------------------------------------
    cc = p["CONE_CLEARANCE"]
    cuts.append(Part.makeCone(
        (p["CONE_BASE_DIA"] + cc) / 2.0, (p["CONE_TIP_DIA"] + cc) / 2.0,
        p["CONE_LEN"], App.Vector(0, 0, 0), App.Vector(0, 0, -1)))
    cuts.append(Part.makeCylinder(
        (p["CONE_TIP_DIA"] + cc) / 2.0, d["CONE_RECESS_DEPTH"] - p["CONE_LEN"] + 0.1,
        App.Vector(0, 0, -d["CONE_RECESS_DEPTH"]), Z))
    # pogo block pocket at the cone floor
    cuts.append(Part.makeBox(
        p["CONTACT_W"] + 1.0, p["CONTACT_L"] + 1.0, p["CONTACT_POGO_DEPTH"],
        App.Vector(-(p["CONTACT_W"] + 1.0) / 2.0, -(p["CONTACT_L"] + 1.0) / 2.0,
                   -d["CONE_RECESS_DEPTH"] - p["CONTACT_POGO_DEPTH"] + 0.1)))
    # harness bore
    cuts.append(Part.makeCylinder(
        8.0, depth + 2.0, App.Vector(0, 0, -depth - 1.0), Z))

    # --- perimeter gasket groove: one gasket on the base, not N on modules -
    go = Part.makeCylinder((p["GASKET_BC"] + p["GASKET_W"]) / 2.0,
                           p["GASKET_H"] + 0.1, App.Vector(0, 0, -p["GASKET_H"]), Z)
    gi = Part.makeCylinder((p["GASKET_BC"] - p["GASKET_W"]) / 2.0,
                           p["GASKET_H"] + 0.3, App.Vector(0, 0, -p["GASKET_H"] - 0.1), Z)
    cuts.append(go.cut(gi))
    return body, cuts


def _resolve(parts):
    body, cuts = parts
    for c in cuts:
        body = body.cut(c)
    return body


def module_port(p=None):
    """Male half as a standalone finished solid. Do NOT fuse a host onto it."""
    return _resolve(module_port_parts(p))


def base_port(p=None):
    """Female half as a standalone finished solid. Do NOT fuse a host onto it."""
    return _resolve(base_port_parts(p))


def attach(host, parts):
    """Fuse a port onto a host body with the correct cut ordering.

    ALWAYS use this instead of host.fuse(module_port()). Fusing a host over a
    finished port back-fills its recesses -- silently, with no error. This
    exact bug shipped in v0.1 and removed all three ball sockets.
    """
    body, cuts = parts
    out = host.fuse(body)
    for c in cuts:
        out = out.cut(c)
    return out


def report(p=None):
    """Derived geometry, margins and BOM. Runs under plain python3."""
    p = p or PORT
    d = derived(p)
    print("TB-Port spec %s  --  three tapered posts, cross pins" % p["SPEC_VERSION"])
    print("\nGEOMETRY")
    print("  post                  3 x Ø%.1f, identical, at %s deg"
          % (p["POST_DIA"], "/".join("%.0f" % a for a in p["POST_ANGLES"])))
    print("  post bolt circle      Ø%.0f  (r = %.0f)" % (p["POST_BC"], p["POST_BC"] / 2))
    print("  base sockets at       %s deg  (mirror of the posts -- the faces meet)"
          % "/".join("%.0f" % a for a in d["SOCKET_ANGLES"]))
    print("  taper                 %.2f mm long -> %.2f mm capture, on the post"
          % (d["POST_TAPER_LEN"], d["POST_CAPTURE"]))
    print("  socket                Ø%.2f x %.1f deep" % (d["SOCKET_DIA"], d["SOCKET_DEPTH"]))
    print("  cone                  Ø%.0f->Ø%.0f x %.0f, leads the posts by %.0f mm"
          % (p["CONE_BASE_DIA"], p["CONE_TIP_DIA"], p["CONE_LEN"], d["CONE_LEAD"]))
    print("  receptacle depth      %.1f mm  (the cone is the deepest feature)"
          % d["RECEPTACLE_DEPTH"])
    print("  pin bore cover        %.2f mm of base material above the bore"
          % d["PIN_BORE_COVER"])
    print("\nVOLUME CONSUMED IN THE BASE")
    print("  3 post sockets        %6.0f mm3" % d["VOL_SOCKETS"])
    print("  connector cone        %6.0f mm3" % d["VOL_CONE"])
    print("  total                 %6.0f mm3   (bayonet alternative: ~69,979)"
          % d["VOL_TOTAL"])
    print("\nKEYING")
    print("  wrong orientation misses by %.1f deg = %.2f mm at r=%.0f"
          % (d["KEY_MISFIT_DEG"], d["KEY_MISFIT_MM"], p["POST_BC"] / 2))
    print("  socket clearance %.2f mm -> a wall, not a tight fit" % p["SOCKET_CLEARANCE"])
    print("  cost: centroid %.2f mm off axis = %.2f N*m imbalance"
          % (d["CENTROID_OFFSET"], d["LOAD_IMBALANCE_NM"]))
    print("\nMARGINS (top port, %.0f N flight load)" % LOAD["AXIAL_TOP_N"])
    print("  pin double shear      %.0f N per pin, need %.0f -> %.0fx"
          % (d["PIN_CAPACITY_N"], d["PIN_LOAD_N"], d["PIN_MARGIN"]))
    print("  bearing on PETG       %.2f MPa -> %.0fx" % (d["BEARING_MPA"], d["BEARING_MARGIN"]))
    print("\nBILL OF MATERIALS per mated pair")
    print("  3 x Ø%.0f x %.0f steel dowel, one end tapered %.0f deg  (posts)"
          % (p["POST_DIA"], p["POST_LEN"] + 8, p["POST_TAPER_ANGLE"]))
    print("  3 x Ø%.0f steel dowel                                 (locking pins)" % p["PIN_DIA"])
    print("  3 x lip seal, %.1f mm            (socket mouths)" % p["LIP_SEAL_W"])
    print("  1 x TPU O-ring, Ø%.0f x %.0f       (perimeter gasket, on the base)"
          % (p["GASKET_BC"], p["GASKET_H"]))
    print("  1 x %d-way pogo block + mating pad PCB  (central connector)" % p["CONTACT_COUNT"])


if __name__ == "__main__":
    report()
