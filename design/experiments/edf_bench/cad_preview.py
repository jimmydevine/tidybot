"""Generate standalone SVG previews from CAD triangulations, without a GUI."""
import html
import math
import base64
import struct
import zlib

import numpy as np


def preview_svg(scene, title, subtitle):
    # View the intake-facing axial face and one side from above.
    camera = (-1, -.45, .7)
    norm = math.sqrt(sum(v * v for v in camera))
    camera = tuple(v / norm for v in camera)
    horizontal = math.hypot(camera[0], camera[1])
    right = (-camera[1] / horizontal, camera[0] / horizontal, 0)
    up = (camera[1] * right[2] - camera[2] * right[1],
          camera[2] * right[0] - camera[0] * right[2],
          camera[0] * right[1] - camera[1] * right[0])

    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    triangles = []
    for shape, color in scene:
        if not shape.Faces:
            continue
        vertices, facets = shape.tessellate(.2)
        for indices in facets:
            p = [tuple(vertices[i]) for i in indices]
            a = tuple(p[1][i] - p[0][i] for i in range(3))
            b = tuple(p[2][i] - p[0][i] for i in range(3))
            normal = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
            n = math.sqrt(dot(normal, normal))
            if n < 1e-10:
                continue
            normal = tuple(v / n for v in normal)
            if dot(normal, camera) <= 0:
                continue
            light = .48 + .52 * max(0, dot(normal, camera))
            fill = tuple(round(v * light) for v in color)
            projected = [(dot(v, right), -dot(v, up), dot(v, camera)) for v in p]
            triangles.append((projected, fill))
    assert triangles
    coords = [p for tri, _ in triangles for p in tri]
    xmin, xmax = min(p[0] for p in coords), max(p[0] for p in coords)
    ymin, ymax = min(p[1] for p in coords), max(p[1] for p in coords)
    scale = min(850 / (xmax - xmin), 460 / (ymax - ymin))
    tx, ty = 500 - scale * (xmin + xmax) / 2, 360 - scale * (ymin + ymax) / 2
    # A depth buffer handles the concave nut windows and overlapping parts;
    # sorting large triangles by average depth gives misleading visible seams.
    rgb = np.full((700, 1000, 3), (246, 248, 251), dtype=np.uint8)
    depth = np.full((700, 1000), -np.inf, dtype=np.float32)
    for tri, fill in triangles:
        p = [(tx + scale * x, ty + scale * y, z) for x, y, z in tri]
        x0, y0, z0 = p[0]; x1, y1, z1 = p[1]; x2, y2, z2 = p[2]
        left, right_edge = max(0, math.floor(min(v[0] for v in p))), min(999, math.ceil(max(v[0] for v in p)))
        top, bottom = max(0, math.floor(min(v[1] for v in p))), min(699, math.ceil(max(v[1] for v in p)))
        denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(denom) < 1e-10:
            continue
        xx, yy = np.meshgrid(np.arange(left, right_edge + 1) + .5, np.arange(top, bottom + 1) + .5)
        w0 = ((y1 - y2) * (xx - x2) + (x2 - x1) * (yy - y2)) / denom
        w1 = ((y2 - y0) * (xx - x2) + (x0 - x2) * (yy - y2)) / denom
        w2 = 1 - w0 - w1
        zz = w0 * z0 + w1 * z1 + w2 * z2
        previous = depth[top:bottom + 1, left:right_edge + 1]
        visible = (w0 >= -1e-8) & (w1 >= -1e-8) & (w2 >= -1e-8) & (zz > previous)
        previous[visible] = zz[visible]
        rgb[top:bottom + 1, left:right_edge + 1][visible] = fill

    def chunk(kind, payload):
        return struct.pack('!I', len(payload)) + kind + payload + struct.pack('!I', zlib.crc32(kind + payload) & 0xffffffff)

    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', 1000, 700, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(b''.join(b'\x00' + row.tobytes() for row in rgb))) + chunk(b'IEND', b'')
    encoded = base64.b64encode(png).decode('ascii')
    rows = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="700" viewBox="0 0 1000 700">',
            f'<image width="1000" height="700" href="data:image/png;base64,{encoded}"/>',
            '<style>text{font-family:Arial,sans-serif;fill:#15243a}</style>',
            f'<text x="35" y="38" font-size="22">{html.escape(title)}</text>',
            f'<text x="35" y="66" font-size="15">{html.escape(subtitle)}</text>']
    rows.append('<text x="35" y="649" font-size="16">Unpowered assembly prototype. Use the separate cradle STL for printing.</text>')
    rows.append('<text x="35" y="677" font-size="14">CAD checks establish nominal geometry; actual fit, print quality and load capacity remain to verify.</text>')
    rows.append('</svg>')
    return '\n'.join(rows)
