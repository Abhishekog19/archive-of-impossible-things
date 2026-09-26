"""Small shared helpers for placed, baked production assets (Blender coordinates)."""
import bpy
import math
import random
from mathutils import Vector


def merge(name, objects):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.hide_set(False)
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def leaf_crown(name, centre, radius, seed, count=230, leaf_scale=1):
    """Grouped broadleaf sprays, with lit tops and open, irregular edges."""
    rng = random.Random(seed)
    verts, faces, colors = [], [], []
    clusters = []
    for i in range(9):
        a = i * 2.399
        clusters.append(Vector((math.cos(a)*.57, math.sin(a)*.57, rng.uniform(-.3,.35))))
    for i in range(count):
        cluster = clusters[i % len(clusters)]
        offset = cluster + Vector((rng.uniform(-.43,.43),rng.uniform(-.43,.43),rng.uniform(-.35,.35)))
        p = Vector(centre) + Vector(tuple(offset[j]*radius[j] for j in range(3)))
        a = rng.random()*math.tau
        size = rng.uniform(.25,.56)*leaf_scale
        u = Vector((math.cos(a), math.sin(a), rng.uniform(-.3,.3)))*size
        v = Vector((-math.sin(a), math.cos(a), rng.uniform(-.3,.3)))*size*.55
        base = len(verts)
        verts.extend([p-u, p-v, p+u, p+v])
        faces.append((base,base+1,base+2,base+3))
        shade = .6 + .32*max(0,min(1,offset.z+.5)) + rng.uniform(-.08,.08)
        colors.append((.19*shade,.275*shade,.085*shade,1))
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts,[],faces)
    data.update()
    attr = data.color_attributes.new(name='CanopyColor',type='BYTE_COLOR',domain='CORNER')
    for poly in data.polygons:
        for loop in poly.loop_indices: attr.data[loop].color = colors[poly.index]
    obj = bpy.data.objects.new(name,data)
    bpy.context.collection.objects.link(obj)
    return obj


def color_material(obj):
    mat = bpy.data.materials.new(obj.name+' colour')
    mat.use_nodes = True
    node = mat.node_tree.nodes.new('ShaderNodeVertexColor')
    node.layer_name = obj.data.color_attributes.active_color.name
    mat.node_tree.links.new(node.outputs['Color'],mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    for poly in obj.data.polygons: poly.material_index = 0


def lighting():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 24
    scene.cycles.max_bounces = 2
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 6
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (.48,.60,.72,1)
    bg.inputs['Strength'].default_value = .4
    bpy.ops.object.light_add(type='SUN')
    sun = bpy.context.object
    sun.data.energy = 2.1
    sun.data.color = (1,.91,.77)
    sun.data.angle = .07
    sun.rotation_euler = Vector((-6,8,-12)).to_track_quat('-Z','Y').to_euler()


def bake(targets, output):
    """Bake all source materials before replacing them with exported maps."""
    scene = bpy.context.scene
    images = []
    for obj,size in targets:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.006)
        bpy.ops.object.mode_set(mode='OBJECT')
        atlas = bpy.data.images.new(obj.name+' placed diffuse',width=size,height=size,alpha=False)
        atlas.filepath_raw = str(output/(obj.name+'.png'))
        atlas.file_format = 'PNG'
        for i,original in enumerate(list(obj.data.materials)):
            mat = original.copy()
            obj.data.materials[i] = mat
            tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
            tex.image = atlas
            mat.node_tree.nodes.active = tex
        images.append((obj,atlas))
    scene.render.bake.use_pass_color = True
    scene.render.bake.use_pass_direct = True
    scene.render.bake.use_pass_indirect = True
    scene.render.bake.margin = 8
    for obj,atlas in images:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        print('BAKING '+obj.name,flush=True)
        bpy.ops.object.bake(type='DIFFUSE')
        atlas.save()
        atlas.pack()
    for obj,atlas in images:
        mat = bpy.data.materials.new(obj.name+' baked')
        mat.use_nodes = True
        tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex.image = atlas
        mat.node_tree.links.new(tex.outputs['Color'],mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        for poly in obj.data.polygons: poly.material_index = 0
