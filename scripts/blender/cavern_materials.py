"""Reusable two-metre stone surface, authored offline, packed in the GLB.

Periodic fields make seamless tiles. Broad mineral patches and broken sediment
veins carry the style; small relief supplies grazing-angle detail, not noisy dirt.
UV density is set by cavern_structure.py rather than the size of the chamber.
"""
import bpy
import numpy as np


def stone_material(vertex_layer='RockColor'):
    size = 1024
    rng = np.random.default_rng(505)
    yy, xx = np.mgrid[:size, :size].astype(np.float32) / size

    def field(scale):
        # Smooth periodic lattice interpolation, independent of Blender versions.
        lattice = rng.uniform(-1, 1, (scale, scale)).astype(np.float32)
        u, v = xx * scale, yy * scale
        ix, iy = u.astype(int), v.astype(int)
        fu, fv = u - ix, v - iy
        fu, fv = fu * fu * (3 - 2 * fu), fv * fv * (3 - 2 * fv)
        a = lattice[iy % scale, ix % scale] * (1 - fu) + lattice[iy % scale, (ix + 1) % scale] * fu
        b = lattice[(iy + 1) % scale, ix % scale] * (1 - fu) + lattice[(iy + 1) % scale, (ix + 1) % scale] * fu
        return a * (1 - fv) + b * fv

    broad, medium, fine = field(5), field(19), field(77)
    grain = field(191)
    phase = yy * 11 + xx * 2 + broad * .75 + medium * .12
    veins = np.exp(-np.square(np.sin(phase * np.pi) / .10))
    veins *= np.clip((field(8) + .3) * 2, 0, 1)
    mineral = np.clip((broad + medium * .3 - .12) * 2, 0, 1)
    height = .5 + medium * .14 + fine * .034 + grain * .009 - veins * .075
    tone = np.clip(.78 + broad * .045 + medium * .035 + fine * .012 - veins * .045, .60, .90)
    colour = np.stack((tone + mineral * .018, tone + mineral * .012, tone), axis=-1)
    # Two metres per tile; keep normal relief in millimetres rather than inflating
    # every pore into a boulder. Blender and glTF both use tangent-space +Y normals.
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * size * .003 / 4
    dy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * size * .003 / 4
    normal = np.stack((-dx, -dy, np.ones_like(dx)), axis=-1)
    normal /= np.linalg.norm(normal, axis=-1, keepdims=True)
    normal = normal * .5 + .5
    roughness = np.clip(.85 + medium * .08 + veins * .08 - mineral * .1, .65, .97)

    def image(name, values, colour_space):
        img = bpy.data.images.new(name, width=size, height=size, alpha=False)
        img.colorspace_settings.name = colour_space
        rgba = np.ones((size, size, 4), dtype=np.float32)
        rgba[:, :, :3] = values
        img.pixels.foreach_set(rgba.ravel())
        img.pack()
        return img

    mat = bpy.data.materials.new('Cavern layered mineral stone — 2m tile')
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes.get('Principled BSDF')
    vertex = nodes.new('ShaderNodeVertexColor'); vertex.layer_name = vertex_layer
    albedo = nodes.new('ShaderNodeTexImage'); albedo.image = image('Cavern stone colour 1024', colour, 'sRGB')
    multiply = nodes.new('ShaderNodeMixRGB'); multiply.blend_type = 'MULTIPLY'; multiply.inputs[0].default_value = 1
    links.new(vertex.outputs['Color'], multiply.inputs[1]); links.new(albedo.outputs['Color'], multiply.inputs[2])
    links.new(multiply.outputs[0], bsdf.inputs['Base Color'])
    normal_tex = nodes.new('ShaderNodeTexImage'); normal_tex.image = image('Cavern stone normal 1024', normal, 'Non-Color')
    normal_node = nodes.new('ShaderNodeNormalMap')
    links.new(normal_tex.outputs['Color'], normal_node.inputs['Color']); links.new(normal_node.outputs['Normal'], bsdf.inputs['Normal'])
    rough = nodes.new('ShaderNodeTexImage'); rough.image = image('Cavern stone roughness 1024', np.repeat(roughness[:, :, None], 3, axis=2), 'Non-Color')
    links.new(rough.outputs['Color'], bsdf.inputs['Roughness'])
    return mat
