# 0006. Three tapered posts with cross pins

**Status:** Accepted
**Date:** 2026-09-04
**Supersedes:** the TB-Port v0.1 boss-and-bore geometry (spec 0.1.0)

## Context

The v0.1 port put all four of the port's jobs — capture, location, retention and
connection — into one small central boss. Three consequences followed, and only the
third was anticipated:

1. **It was deep.** At small radius, both tilt resistance and capture must be bought
   with axial length. Two ports consumed 62 mm of a 120 mm base height.
2. **It was congested.** The annulus between bore wall and flange edge was 19.8 mm
   wide, and three separate geometry bugs all landed in it.
3. **It failed in tension.** Once the 3-stack flies, both ports carry 192 N and 59 N
   respectively, and a ball detent is the textbook cam-out geometry.

Five architectures were compared at one scale in `docs/coupling-study.html`.

## Decision

**Three identical tapered steel posts per face, retained by cross pins in double shear.**

| Feature | Value | Reason |
|---|---|---|
| Post count | 3 | Exactly determinate: 6 constraints for 6 DOF. Four is over-constrained by two and will rock or jam in printed plastic. |
| Post angles | 0° / 120° / **235°** | The 5° asymmetry makes wrong orientations miss by 4.4 mm against a 0.2 mm clearance — mechanically impossible, not merely discouraged. |
| Post radius | 50 mm | Yaw offset scales with radius. Coming in from 80 mm halves it, for a moment load still 47× inside margin. |
| Posts | identical | One dowel size, one socket, one lip seal, one reamer, one spare. |
| Retention | Ø5 pin, double shear | 164× margin on the 192 N flight case, and shear is indifferent to load direction. |
| Actuation | cam plate inside the base | The mechanism never sees the room. |
| Electricals | central connector only | See below. |

## Consequences

**The mechanism is sealed.** Pins, cam plate and motor all live inside the base. What is
exposed is solid steel posts and drained holes, with nothing that can foul. This is the
property that matters most on a robot that vacuums and mops, and it is the one thing the
bayonet alternative structurally cannot offer — a ramped rotating collar on the outside
of a machine that manufactures abrasive dust.

**Capture is free.** The taper rides on the post, not in the base, so it costs zero
receptacle depth. Alone among the options considered.

**Alignment is staged, not toleranced.** Posts absorbing lateral *and* angular error at
once would need 14.2 mm of capture against a 2.5 mm taper. A central cone kills lateral
first — it sits at r = 0, where yaw cannot displace it — leaving the posts 0.74 mm to
swallow. Two of the five stages live in the docking station, which puts the dock on the
critical path.

**Posts carry load only.** A pin must bear on its post to transmit load, which makes
them one electrical node — three posts give three circuits, not the eight the spec needs.
And energised posts on a mopping robot are a bridged bus waiting for a puddle. All eight
contacts go in the sealed central connector instead, where CAN stays a proper twisted
pair.

**Materials are stainless, not mild steel.** The posts are exposed whenever a module is
off, on a machine that mops. Rust swells, and a rusted Ø10 post binds in a Ø10.2 socket.
Grade 303 for anything being machined by hand; a different alloy for the lock plate, since
austenitic stainless galls against itself under load. Margins are quoted at the
conservative 205 MPa austenitic yield and remain 61× and 123×.

**Costs accepted:**

- The central connector cone is the deepest feature (~25 mm) and dominates the volume
  consumed. Honest accounting: 3 post sockets are 4.4k mm³, the cone recess is ~25k, so
  the port takes ~29k mm³ against the bayonet's ~70k. That is a 59% reduction, not the
  88% quoted while counting posts alone.
- Sockets on the base's upper face point up and will collect dust. They need lip seals
  and a drain out the **side wall** — never into the electronics.
- One more actuator concept to design and validate: the cam plate.

## Alternatives considered

- **Bayonet with a rotating collar.** Shallowest option and strong in tension, but eight
  exposed moving parts with ramped slots, mounted outside, in the dirt. Rejected on
  contamination. Retained as the fallback if docking accuracy proves worse than hoped.
- **Cone with three balls and one central pin.** Elegant in compression; in tension the
  balls unload and it degenerates to a single-pin hinge. Disqualifying under a rotor.
- **Linear slide (cordless tool battery).** Mates with zero actuators and self-wiping
  contacts, both excellent. Rejected because a spring latch is all that stands between
  19.6 kg and a dropped robot, and it dictates a straight-line dock approach.
- **Different post diameters for keying.** Works, but the smallest post sets the joint's
  rating and you make, stock and replace three parts instead of one. Unequal *spacing*
  achieves the same for free.
