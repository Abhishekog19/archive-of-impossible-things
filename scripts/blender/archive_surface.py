"""Shared archive stone and organic-detail tools, reusable for the hall."""
import bpy
import math
from mathutils import Vector


def damp_material(source, name, moss=.65):
    mat = source.copy();mat.name=name
    nodes,links=mat.node_tree.nodes,mat.node_tree.links
    shader=nodes.get('Principled BSDF')
    base=shader.inputs['Base Color'].links[0].from_socket
    geo=nodes.new('ShaderNodeNewGeometry')
    noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.85
    noise.inputs['Detail'].default_value=2
    links.new(geo.outputs['Position'],noise.inputs['Vector'])
    ramp=nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position=.46
    ramp.color_ramp.elements[1].position=.66
    ramp.color_ramp.elements[1].color=(moss,moss,moss,1)
    links.new(noise.outputs['Fac'],ramp.inputs[0])
    mix=nodes.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.13,.175,.047,1)
    links.new(ramp.outputs['Color'],mix.inputs[0]);links.new(base,mix.inputs[1])
    links.new(mix.outputs[0],shader.inputs['Base Color'])
    return mat


def root_tendril(name, points, radius, material):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D'
    curve.resolution_u=5;curve.bevel_depth=radius;curve.bevel_resolution=1
    spline=curve.splines.new('BEZIER');spline.bezier_points.add(len(points)-1)
    for i,(p,co) in enumerate(zip(spline.bezier_points,points)):
        p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
        p.radius=max(.07,1-i/(len(points)-.4))
    obj=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    bpy.ops.object.select_all(action='DESELECT');obj.select_set(True)
    bpy.context.view_layer.objects.active=obj;bpy.ops.object.convert(target='MESH')
    return bpy.context.object


def ivy_ribbon(name, x, y, top, length, seed):
    import random
    rng=random.Random(seed);verts=[];faces=[];tints=[]
    for i in range(int(length*12)):
        if rng.random()<.2:continue
        h=top-i/12
        cx=x+math.sin(i*.27)*.18
        for side in (-1,1):
            width=.15+.35*(.5+.5*math.sin(i*.36+seed))
            p=Vector((cx+side*rng.uniform(.02,width),y+rng.uniform(-.025,.025),h+rng.uniform(-.06,.06)))
            size=rng.uniform(.07,.17);base=len(verts)
            verts.extend([p+Vector((0,0,size)),p+Vector((size,-.02,0)),p+Vector((0,-.04,-size*.65)),p+Vector((-size,-.02,0))])
            faces.append(tuple(range(base,base+4)))
            shade=rng.uniform(.65,1)
            tints.append((.062*shade,.112*shade,.026*shade,1))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    colors=mesh.color_attributes.new(name='CanopyColor',type='BYTE_COLOR',domain='CORNER')
    for poly in mesh.polygons:
        for loop in poly.loop_indices:colors.data[loop].color=tints[poly.index]
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
    return obj
