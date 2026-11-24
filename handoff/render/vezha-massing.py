#!/usr/bin/env blender --background --python
"""
Vezha — enclosure massing model and renders.

Builds a block model of Enclosure A from the dimensions recorded in
docs/02-enclosure-a-upper.md and handoff/03-parts-and-dimensions.md, then
renders three views into handoff/img/.

This is a MASSING MODEL, not CAD. Every dimension is traceable to the docs,
but nothing here is a manufacturing geometry: no fillet radii, wall drafts,
boss positions, connector cutouts or tolerances are real. It exists to make
the proportions and the depth stack legible.

Run:
    blender --background --python handoff/render/vezha-massing.py
"""

import bpy
import os
import math

# ----------------------------------------------------------------------------
# Dimensions — all mm, all traceable to the docs
# ----------------------------------------------------------------------------

WALL = 2.0  # nominal wall, cap brief

# Enclosure A exterior
W = 110.0  # width        — cap brief initial envelope
BODY_H = 95.0  # body height   — board 75 on edge + foot
CAP_H = 60.0  # cap height    — cap brief initial envelope
SEAM = 1.2  # visible seam gap between body and cap
FOOT_H = 6.0  # stable foot

# Depth stack, front to rear (docs/02 · Thermal, handoff 0.3)
D_OLED = 6.0  # Adafruit 5297 breakout
D_OLED_GAP = 1.0  # mount clearance
D_M2 = 15.9  # front-face M.2 stack (GUESS — four stacked guesses)
D_PCB = 1.6  # Orange Pi PCB
D_HS = 12.6  # heatsink
D_GAP = 3.0  # fan-to-heatsink clearance ("small", unspecified)
D_FAN = 12.0  # NF-A4x10 5V installed with pads
D = WALL + D_OLED + D_OLED_GAP + D_M2 + D_PCB + D_HS + D_GAP + D_FAN + WALL

# Components
PCB_W, PCB_H = 100.0, 75.0  # Orange Pi 5 Plus
OLED_W, OLED_H = 40.5, 30.5  # 5297 breakout
OLED_ACTIVE = 20.076  # active area, square
HS_W, HS_H = 50.0, 46.0  # heatsink
FAN_SIZE = 40.0  # fan
ANT_L, ANT_W = 42.0, 7.0  # Taoglas FXP830 body

# Blender's light falloff and shader units assume METRES. The dimensions above
# are millimetres, so everything is scaled on the way into the scene; without
# this, a 110 mm object is treated as 110 m and no sane lighting rig works.
S = 0.001


def u(v):
    """mm -> Blender units (metres)."""
    return v * S


def uv(t3):
    return tuple(v * S for v in t3)


OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")
OUT = os.path.normpath(OUT)

# ----------------------------------------------------------------------------
# Scene helpers
# ----------------------------------------------------------------------------


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def mat(name, rgb, rough=0.5, metal=0.0, alpha=1.0, emit=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.blend_method = "BLEND"
    if emit > 0.0:
        b.inputs["Emission Color"].default_value = (*rgb, 1.0)
        b.inputs["Emission Strength"].default_value = emit
    return m


def box(name, size, loc, material=None, bevel=0.0):
    """size = (x, y, z) in mm; loc = centre in mm."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=uv(loc))
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = uv(size)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel > 0.0:
        bm = ob.modifiers.new("Bevel", "BEVEL")
        bm.width = u(bevel)
        bm.segments = 6
        bm.limit_method = "ANGLE"
    if material:
        ob.data.materials.append(material)
    return ob


def cyl(name, r, depth, loc, rot=(0, 0, 0), material=None):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=u(r), depth=u(depth), location=uv(loc), rotation=rot, vertices=48
    )
    ob = bpy.context.active_object
    ob.name = name
    if material:
        ob.data.materials.append(material)
    return ob


def boolean_cut(target, cutter):
    m = target.modifiers.new("Cut", "BOOLEAN")
    m.operation = "DIFFERENCE"
    m.object = cutter
    m.solver = "EXACT"  # Blender 5.x: FLOAT | EXACT | MANIFOLD
    cutter.hide_render = True
    cutter.hide_viewport = True
    return m


# ----------------------------------------------------------------------------
# Materials
# ----------------------------------------------------------------------------


def build_materials():
    return {
        "shell": mat("Shell", (0.185, 0.197, 0.215), rough=0.55),
        "shell_ghost": mat("ShellGhost", (0.70, 0.78, 0.88), rough=0.15, alpha=0.040),
        "cap": mat("Cap", (0.118, 0.128, 0.145), rough=0.68),
        "pcb": mat("PCB", (0.055, 0.260, 0.145), rough=0.52),
        "oled_body": mat("OledBody", (0.085, 0.088, 0.098), rough=0.44),
        "oled_glass": mat("OledGlass", (0.48, 0.80, 1.00), rough=0.12, emit=18.0),
        "heatsink": mat("Heatsink", (0.74, 0.76, 0.79), rough=0.28, metal=0.92),
        "fan": mat("Fan", (0.60, 0.20, 0.16), rough=0.48),
        "fan_hub": mat("FanHub", (0.19, 0.18, 0.18), rough=0.42),
        "m2": mat("M2", (0.13, 0.16, 0.38), rough=0.45),
        "ant": mat("Antenna", (0.93, 0.64, 0.20), rough=0.36, metal=0.40),
        "accent": mat("Accent", (0.95, 0.46, 0.13), rough=0.35),
    }


# ----------------------------------------------------------------------------
# Geometry
# ----------------------------------------------------------------------------

# Z datum: 0 at the bottom of the foot.
BODY_Z0 = 0.0
BODY_Z1 = BODY_H
CAP_Z0 = BODY_H + SEAM
CAP_Z1 = CAP_Z0 + CAP_H

# Board sits on edge, header at the bottom.
PCB_Z = FOOT_H + 4.0 + PCB_H / 2.0
OLED_Z = BODY_Z1 - 26.0  # OLED sits high on the front face

# Depth datum: y = -D/2 is the FRONT face.
Y_FRONT = -D / 2.0


def y_at(offset, thickness):
    """Centre of a layer whose front face is `offset` from the front wall."""
    return Y_FRONT + offset + thickness / 2.0


OFF_OLED = WALL
OFF_M2 = OFF_OLED + D_OLED + D_OLED_GAP
OFF_PCB = OFF_M2 + D_M2
OFF_HS = OFF_PCB + D_PCB
OFF_FAN = OFF_HS + D_HS + D_GAP


def build_shell(M, ghost=False):
    """Body + cap + foot. Returns the list of shell objects."""
    shell_mat = M["shell_ghost"] if ghost else M["shell"]
    cap_mat = M["shell_ghost"] if ghost else M["cap"]
    objs = []

    body = box(
        "Body",
        (W, D, BODY_H - FOOT_H),
        (0, 0, FOOT_H + (BODY_H - FOOT_H) / 2.0),
        shell_mat,
        bevel=3.2,
    )
    objs.append(body)

    foot = box("Foot", (W, D, FOOT_H), (0, 0, FOOT_H / 2.0), shell_mat, bevel=2.0)
    objs.append(foot)

    cap = box(
        "AntennaCap",
        (W, D, CAP_H),
        (0, 0, CAP_Z0 + CAP_H / 2.0),
        cap_mat,
        bevel=3.2,
    )
    objs.append(cap)

    # Strap slots — a through-slot in each lower side wall
    for sx in (-1, 1):
        cutter = box(
            f"StrapCut{sx}",
            (14.0, 24.0, 5.0),
            (sx * (W / 2.0 - 2.0), 0.0, FOOT_H + 12.0),
        )
        boolean_cut(body, cutter)

    # Surface texture — fine horizontal grooves cut into the lower body, the
    # styling reference's signature line work. Cut in, so the silhouette is
    # unbroken.
    for i in range(0 if ghost else 10):
        groove = box(
            f"Groove{i}",
            (W - 7.0, D + 6.0, 0.9),
            (0, 0, FOOT_H + 14.0 + i * 3.0),
        )
        boolean_cut(body, groove)
        groove2 = box(
            f"GrooveSide{i}",
            (W + 6.0, D - 7.0, 0.9),
            (0, 0, FOOT_H + 14.0 + i * 3.0),
        )
        boolean_cut(body, groove2)

    # OLED window — recessed bezel cut into the front face
    win = box(
        "OledWindowCut",
        (OLED_ACTIVE + 2.4, 6.0, OLED_ACTIVE + 2.4),
        (0, Y_FRONT + 1.2, OLED_Z),
    )
    boolean_cut(body, win)
    if not ghost:
        scr = box(
            "ScreenFace",
            (OLED_ACTIVE, 0.6, OLED_ACTIVE),
            (0, Y_FRONT + WALL + 0.4, OLED_Z),
            M["oled_glass"],
        )
        objs.append(scr)

    # Fan intake — a grille of slots on the rear face
    for i in range(7):
        z = PCB_Z + 4.0 - 18.0 + i * 6.0
        slot = box(
            f"VentCut{i}",
            (FAN_SIZE - 4.0, 8.0, 2.6),
            (0, D / 2.0 - 1.0, z),
        )
        boolean_cut(body, slot)

    # Two cap retaining screws, rear face just below the seam
    for sx in (-1, 1):
        s = cyl(
            f"CapScrew{sx}",
            1.7,
            4.0,
            (sx * (W / 2.0 - 16.0), D / 2.0 - 1.2, BODY_Z1 - 7.0),
            rot=(math.radians(90), 0, 0),
            material=M["accent"],
        )
        objs.append(s)

    return objs


def build_internals(M, explode=0.0, antennas=True):
    """Internal stack. `explode` spreads layers along +/-Y."""
    objs = []

    def ey(center, rank):
        return center + explode * rank

    # OLED breakout + emissive active area
    ob = box(
        "OLED",
        (OLED_W, D_OLED, OLED_H),
        (0, ey(y_at(OFF_OLED, D_OLED), -3), OLED_Z),
        M["oled_body"],
    )
    objs.append(ob)
    g = box(
        "OLEDActive",
        (OLED_ACTIVE, 0.8, OLED_ACTIVE),
        (
            0,
            ey(y_at(OFF_OLED, D_OLED), -3) - D_OLED / 2.0 - 0.4,
            OLED_Z,
        ),
        M["oled_glass"],
    )
    objs.append(g)

    # Front-face M.2 stack — card + adapter, 22 x 30 footprint
    m2 = box(
        "M2Stack",
        (30.0, D_M2, 22.0),
        (-18.0, ey(y_at(OFF_M2, D_M2), -2), PCB_Z - 18.0),
        M["m2"],
    )
    objs.append(m2)

    # Orange Pi, on edge
    pcb = box(
        "OrangePi",
        (PCB_W, D_PCB, PCB_H),
        (0, ey(y_at(OFF_PCB, D_PCB), 0), PCB_Z),
        M["pcb"],
    )
    objs.append(pcb)

    # 40-pin header along the bottom edge, internal only
    hdr = box(
        "Header40",
        (65.0, 2.6, 5.0),
        (0, ey(y_at(OFF_PCB, D_PCB), 0) - 2.4, PCB_Z - PCB_H / 2.0 + 4.0),
        M["oled_body"],
    )
    objs.append(hdr)

    # Heatsink: base + fins
    hs_y = ey(y_at(OFF_HS, D_HS), 2)
    base = box(
        "HeatsinkBase",
        (HS_W, 3.0, HS_H),
        (0, hs_y - D_HS / 2.0 + 1.5, PCB_Z + 2.0),
        M["heatsink"],
    )
    objs.append(base)
    n_fins = 13
    for i in range(n_fins):
        x = -HS_W / 2.0 + 2.5 + i * ((HS_W - 5.0) / (n_fins - 1))
        f = box(
            f"Fin{i}",
            (1.4, D_HS - 3.0, HS_H),
            (x, hs_y + 1.5, PCB_Z + 2.0),
            M["heatsink"],
        )
        objs.append(f)

    # Fan: frame + hub + blades
    fan_y = ey(y_at(OFF_FAN, D_FAN), 3)
    frame = box(
        "FanFrame",
        (FAN_SIZE, D_FAN, FAN_SIZE),
        (0, fan_y, PCB_Z + 2.0),
        M["fan"],
    )
    cut = cyl(
        "FanBoreCut",
        FAN_SIZE / 2.0 - 2.0,
        D_FAN + 4.0,
        (0, fan_y, PCB_Z + 2.0),
        rot=(math.radians(90), 0, 0),
    )
    boolean_cut(frame, cut)
    objs.append(frame)

    hub = cyl(
        "FanHub",
        7.0,
        D_FAN - 3.0,
        (0, fan_y, PCB_Z + 2.0),
        rot=(math.radians(90), 0, 0),
        material=M["fan_hub"],
    )
    objs.append(hub)
    for i in range(7):
        a = i * (2 * math.pi / 7)
        bl = box(
            f"Blade{i}",
            (15.0, 2.0, 5.0),
            (
                math.cos(a) * 12.0,
                fan_y,
                PCB_Z + 2.0 + math.sin(a) * 12.0,
            ),
            M["fan_hub"],
        )
        bl.rotation_euler = (0, math.radians(22), a)
        objs.append(bl)

    # Four antennas on the inside faces of the cap
    for i, (sx, sy) in enumerate([] if not antennas else [(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        a = box(
            f"Antenna{i}",
            (ANT_L, 0.6, ANT_W),
            (
                sx * 26.0,
                sy * (D / 2.0 - WALL - 1.0),
                CAP_Z0 + 18.0 + (i % 2) * 22.0,
            ),
            M["ant"],
        )
        objs.append(a)

    return objs


# ----------------------------------------------------------------------------
# Lighting, camera, render
# ----------------------------------------------------------------------------


def studio(bg=0.012):
    world = bpy.data.worlds.new("W")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (bg, bg, bg * 1.15, 1)

    def area(name, loc, rot, size, energy, color=(1, 1, 1)):
        d = bpy.data.lights.new(name, "AREA")
        d.energy = energy
        d.size = u(size)
        d.color = color
        o = bpy.data.objects.new(name, d)
        o.location = uv(loc)
        o.rotation_euler = rot
        bpy.context.collection.objects.link(o)
        return o

    # Watts at metre scale; positions given in mm and converted.
    area("Key", (-230, -300, 320), (math.radians(44), 0, math.radians(-37)), 260, 22)
    area("Fill", (300, -210, 130), (math.radians(76), 0, math.radians(57)), 340, 7,
         color=(0.78, 0.85, 1.0))
    area("Rim", (90, 330, 250), (math.radians(-55), 0, math.radians(168)), 240, 13,
         color=(1.0, 0.78, 0.55))
    area("Top", (0, -40, 420), (0, 0, 0), 400, 6)

    bpy.ops.mesh.primitive_plane_add(size=u(2600), location=(0, 0, u(-0.25)))
    g = bpy.context.active_object
    g.name = "Ground"
    g.data.materials.append(mat("Ground", (0.040, 0.043, 0.050), rough=0.70))


def camera(loc, look_at, lens=72.0, ortho=None):
    cd = bpy.data.cameras.new("Cam")
    cd.lens = lens
    if ortho:
        cd.type = "ORTHO"
        cd.ortho_scale = u(ortho)
    cam = bpy.data.objects.new("Cam", cd)
    cam.location = uv(loc)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam

    tgt = bpy.data.objects.new("Target", None)
    tgt.location = uv(look_at)
    bpy.context.collection.objects.link(tgt)
    c = cam.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    return cam


def label(text, loc, size=7.0, material=None):
    """A billboarded text label, positioned in mm."""
    bpy.ops.object.text_add(location=uv(loc))
    ob = bpy.context.active_object
    ob.data.body = text
    ob.data.size = u(size)
    ob.data.align_x = "CENTER"
    ob.data.align_y = "CENTER"
    ob.data.extrude = u(0.12)
    if material:
        ob.data.materials.append(material)
    cam = bpy.context.scene.camera
    if cam:
        c = ob.constraints.new("TRACK_TO")
        c.target = cam
        c.track_axis = "TRACK_Z"
        c.up_axis = "UP_Y"
    return ob


def render(path, samples=180, res=(1600, 1400)):
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.cycles.samples = samples
    s.cycles.use_denoising = True
    s.render.resolution_x, s.render.resolution_y = res
    s.render.resolution_percentage = 100
    s.render.film_transparent = False
    s.view_settings.view_transform = "AgX"
    s.view_settings.look = "AgX - Base Contrast"

    # Prefer Metal on Apple silicon; fall back to CPU without complaining.
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "METAL"
        prefs.get_devices()
        for d in prefs.devices:
            d.use = True
        s.cycles.device = "GPU"
    except Exception:
        s.cycles.device = "CPU"

    s.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f"  wrote {path}")


# ----------------------------------------------------------------------------
# The three views
# ----------------------------------------------------------------------------

CENTRE = (0, 0, CAP_Z1 * 0.46)


def view_exterior():
    reset()
    M = build_materials()
    build_shell(M, ghost=False)
    studio()
    camera((-250, -400, 215), CENTRE, lens=85)
    render(os.path.join(OUT, "vezha-exterior.png"))


def view_rear():
    reset()
    M = build_materials()
    build_shell(M, ghost=False)
    studio()
    camera((235, 395, 225), CENTRE, lens=85)
    render(os.path.join(OUT, "vezha-rear.png"))


def view_ghost():
    reset()
    M = build_materials()
    build_shell(M, ghost=True)
    build_internals(M)
    studio(bg=0.009)
    camera((-420, -330, 240), CENTRE, lens=80)
    render(os.path.join(OUT, "vezha-ghost.png"))


def view_exploded():
    """Side-on, so the front-to-back stack reads left to right."""
    reset()
    M = build_materials()
    EX = 26.0
    build_internals(M, explode=EX, antennas=False)
    studio(bg=0.009)
    camera((640, -150, 205), (0, 0, PCB_Z + 4), lens=58)

    ink = mat("Ink", (0.92, 0.93, 0.96), rough=0.6, emit=1.4)
    accent = mat("InkAccent", (1.0, 0.58, 0.22), rough=0.6, emit=2.2)

    def ey(center, rank):
        return center + EX * rank

    top = PCB_Z + PCB_H / 2.0 + 10.0
    rows = [
        ("OLED  6.0", ey(y_at(OFF_OLED, D_OLED), -3), top + 20, ink),
        ("M.2 stack  15.9", ey(y_at(OFF_M2, D_M2), -2), top + 2, accent),
        ("Orange Pi  1.6", ey(y_at(OFF_PCB, D_PCB), 0), top + 20, ink),
        ("heatsink  12.6", ey(y_at(OFF_HS, D_HS), 2), top + 2, ink),
        ("fan  12.0", ey(y_at(OFF_FAN, D_FAN), 3), top + 20, ink),
    ]
    for text, y, z, m in rows:
        label(text, (0, y, z), size=8.0, material=m)

    label(
        "FRONT   <<<   depth stack   >>>   REAR",
        (0, -EX * 1.2, PCB_Z - PCB_H / 2.0 - 16.0),
        size=8.5,
        material=ink,
    )
    label(
        "~56 mm of stack  ·  the brief allowed 30",
        (0, -EX * 1.2, PCB_Z - PCB_H / 2.0 - 30.0),
        size=7.0,
        material=accent,
    )
    render(os.path.join(OUT, "vezha-exploded.png"), res=(2000, 1150))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"Vezha massing — W {W} x H {BODY_H}+{CAP_H} x D {D:.1f} mm")
    view_exterior()
    view_rear()
    view_ghost()
    view_exploded()
    print("done")
