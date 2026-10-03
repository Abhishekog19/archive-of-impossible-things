"""Phase 2 metre-scaled surface study, initially confined to the forest patch.

All procedural relief and contact are baked into the existing diffuse atlas.
The exported stone/wood/ground groups retain that atlas and use runtime detail.
"""
import bpy


def study_material(kind):
    mat = bpy.data.materials.new('Study '+kind)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    shader = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
    shader.inputs['Roughness'].default_value = .92
    geo = nodes.new('ShaderNodeNewGeometry')

    def noise(scale, detail=2, vector=None):
        node = nodes.new('ShaderNodeTexNoise')
        node.inputs['Scale'].default_value = scale
        node.inputs['Detail'].default_value = detail
        links.new(vector or geo.outputs['Position'], node.inputs['Vector'])
        return node.outputs['Fac']

    def ramp(value, stops):
        node = nodes.new('ShaderNodeValToRGB')
        for i, (at, color) in enumerate(stops):
            point = node.color_ramp.elements[i] if i < 2 else node.color_ramp.elements.new(at)
            point.position = at
            point.color = (*color, 1)
        links.new(value, node.inputs[0])
        return node.outputs['Color']

    if kind == 'Stone':
        mineral = ramp(noise(5), [(.2,(.27,.29,.235)),(.8,(.43,.425,.34))])
        # Two spatial scales break moss boundaries into small attached patches.
        field = nodes.new('ShaderNodeMath');field.operation='MULTIPLY'
        links.new(noise(2.8),field.inputs[0]);links.new(noise(22),field.inputs[1])
        mask = ramp(field.outputs[0],[(.30,(0,0,0)),(.43,(.66,.66,.66))])
        mix = nodes.new('ShaderNodeMixRGB')
        links.new(mask,mix.inputs[0]);links.new(mineral,mix.inputs[1])
        mix.inputs[2].default_value=(.085,.12,.028,1)
        color = mix.outputs[0]
        relief, strength, distance = noise(38), .16, .035
    elif kind == 'Wood':
        stretch = nodes.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY'
        stretch.inputs[1].default_value=(8,8,.45)
        links.new(geo.outputs['Position'],stretch.inputs[0])
        grain = noise(1,3,stretch.outputs[0])
        color = ramp(grain,[(.25,(.052,.062,.033)),(.53,(.16,.17,.105)),(.75,(.27,.265,.17))])
        relief, strength, distance = grain, .28, .055
    else:
        color = ramp(noise(3.2,3),[(.22,(.032,.028,.015)),(.50,(.074,.085,.027)),(.78,(.12,.15,.040))])
        relief, strength, distance = noise(28), .22, .025

    # Baked local contact keeps plant/root bases attached without a runtime pass.
    contact = nodes.new('ShaderNodeAmbientOcclusion')
    contact.inputs['Distance'].default_value=.35
    contact.samples=8
    links.new(color,contact.inputs['Color'])
    links.new(contact.outputs['Color'],shader.inputs['Base Color'])
    bump=nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value=strength
    bump.inputs['Distance'].default_value=distance
    links.new(relief,bump.inputs['Height'])
    links.new(bump.outputs['Normal'],shader.inputs['Normal'])
    return mat
