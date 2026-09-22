"""Phase C connected sun/shade patch, preserving the source world and kit.

Reads author geometry only; never rewrites the kit, corner or user's hub source.
World-space diffuse baking includes canopy and undergrowth contact shadows.
"""
import bpy
import math
import json
import time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.artifacts/blender'
started = time.monotonic()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
names = ['Author_Slab_' + str(i) for i in range(1, 7)] + [
    'Author_Tree_Tall', 'Author_Tree_Leaning', 'Author_Tree_Broadleaf',
    'Tree_Tall_Leaves', 'Tree_Leaning_Leaves', 'Tree_Leaves', 'Fern',
    'Broadleaf_Clump', 'Grass_Tuft', 'Low_Shrub']
with bpy.data.libraries.load(str(ROOT / 'art/source/archive-kit.blend'), link=False) as (src, dst):
    assert all(name in src.objects for name in names)
    dst.objects = names
sources = {obj.name: obj for obj in dst.objects}
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 32
scene.cycles.max_bounces = 2
scene.render.threads_mode = 'FIXED'
scene.render.threads = 6
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (.48, .60, .72, 1)
bg.inputs['Strength'].default_value = .40
bpy.ops.object.light_add(type='SUN')
sun = bpy.context.object
sun.data.energy = 2.1
sun.data.color = (1, .91, .77)
sun.data.angle = .045
sun.rotation_euler = Vector((-6, 8, -12)).to_track_quat('-Z', 'Y').to_euler()

# Sample the actual source surfaces, so new shoulders/roots stay grounded.
with bpy.data.libraries.load(str(ROOT / 'art/source/world-blockout.blend'), link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n.startswith(('Continuous terrain', 'Canopy approach', 'Left path mouth'))]
ground_sources = list(dst.objects)
vertices, faces = [], []
for obj in ground_sources:
    offset = len(vertices)
    vertices.extend(obj.matrix_world @ v.co for v in obj.data.vertices)
    faces.extend(tuple(offset + i for i in p.vertices) for p in obj.data.polygons)
ground_bvh = BVHTree.FromPolygons(vertices, faces)
def height_at(x, z):
    hit = ground_bvh.ray_cast(Vector((x, -z, 20)), Vector((0, 0, -1)))[0]
    assert hit is not None, 'Patch outside source terrain'
    return hit.z
def height(z): return height_at(-12, z)
def position(x, y, z): return (x, -z, y)
visuals = []
def place(name, x, z, scale=1, yaw=0, y=None):
    obj = bpy.data.objects.new(name.replace('Author_', 'Patch_'), sources[name].data.copy())
    scene.collection.objects.link(obj)
    obj.location = position(x, height(z) if y is None else y, z)
    obj.rotation_euler.z = -yaw
    obj.scale = (scale, scale, scale)
    visuals.append(obj)
    return obj

# Follow the existing 5.5% slope. Slabs sit just above its coarse surface.
for row in range(18):
    for col in range(4):
        z = -22.6 - row * 1.0
        x = -12 + (col - 1.5) * 1.12 + .07 * math.sin(row * 2.1)
        obj = place('Author_Slab_' + str(1 + (row * 3 + col) % 6), x, z, .93,
                    .04 * math.sin(row + col), height(z) - .075)
        obj.rotation_euler.x = math.atan(.055)

trees = [place('Author_Tree_Tall', -16.8, -27, .95, .35, height_at(-16.8, -27)),
         place('Author_Tree_Leaning', -8.2, -24, .92, -1.0, height_at(-8.2, -24)),
         place('Author_Tree_Broadleaf', -16.7, -36, 1.2, -.4, height_at(-16.7, -36)),
         place('Author_Tree_Tall', -6.9, -35, 1.1, 2.1, height_at(-6.9, -35))]
for tree in trees:
    # Joined prototype limbs still contain intersecting capped shells. Fuse the
    # junctions before baking so self-occlusion cannot create black collar bands.
    bpy.ops.object.select_all(action='DESELECT')
    tree.select_set(True)
    bpy.context.view_layer.objects.active = tree
    remesh = tree.modifiers.new('Continuous branch junctions', 'REMESH')
    remesh.mode = 'VOXEL'
    remesh.voxel_size = .065
    remesh.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    smooth = tree.modifiers.new('Soften fused junctions', 'SMOOTH')
    smooth.factor = .6
    smooth.iterations = 3
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    simplify = tree.modifiers.new('Bound branch geometry', 'DECIMATE')
    simplify.ratio = .35
    bpy.ops.object.modifier_apply(modifier=simplify.name)
    tree.data.validate(clean_customdata=True)
    tree.data.update()

# A thin terrain-following surface receives the canopy/contact bake. The resident
# world floor retains collision; the patch never introduces a second floor body.
verts, faces = [], []
xs = [-21.5, -20, -18.5, -17, -15.5, -14.8, -14, -13, -12, -11, -10, -9.2, -8.5, -7, -5.5, -4, -3.5]
for row in range(20):
    z = -21.8 - row
    for col, x in enumerate(xs):
        if col in (0, len(xs) - 1): x += .65 * math.sin(row * 1.7)
        verts.append(position(x, height_at(x, z) + .018, z))
for row in range(19):
    for col in range(len(xs) - 1):
        a = row * len(xs) + col
        faces.append((a, a + 1, a + 1 + len(xs), a + len(xs)))
data = bpy.data.meshes.new('Patch ground')
data.from_pydata(verts, [], faces)
data.update()
soil = bpy.data.materials.new('Patch moss earth')
soil.use_nodes = True
nodes, links = soil.node_tree.nodes, soil.node_tree.links
noise = nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = .8
noise.inputs['Detail'].default_value = 1.2
coords = nodes.new('ShaderNodeNewGeometry'); links.new(coords.outputs['Position'], noise.inputs['Vector'])
ramp = nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].color = (.045, .064, .021, 1)
ramp.color_ramp.elements[1].color = (.16, .19, .058, 1)
links.new(noise.outputs['Fac'], ramp.inputs[0])
links.new(ramp.outputs[0], nodes['Principled BSDF'].inputs['Base Color'])
nodes['Principled BSDF'].inputs['Roughness'].default_value = .95
data.materials.append(soil)
ground = bpy.data.objects.new('Patch woodland ground', data)
scene.collection.objects.link(ground)
visuals.append(ground)

foliage = []
def plant(name, location, scale, rotation):
    obj = bpy.data.objects.new('Patch_' + name, sources[name].data.copy())
    scene.collection.objects.link(obj)
    obj.location = location
    obj.scale = scale
    obj.rotation_euler = rotation
    # Darker inner/lower leaves, lighter exposed upper layers; no alpha cards.
    colors = obj.data.color_attributes.active_color
    if colors:
        low = min(v.co.z for v in obj.data.vertices)
        span = max(v.co.z for v in obj.data.vertices) - low
        for poly in obj.data.polygons:
            for i in poly.loop_indices:
                v = obj.data.vertices[obj.data.loops[i].vertex_index]
                factor = .48 + .52 * ((v.co.z - low) / max(span, .01))
                c = colors.data[i].color
                colors.data[i].color = (c[0] * factor, c[1] * factor, c[2] * factor, 1)
    foliage.append(obj)
    return obj
for tree, name in zip(trees, ['Tree_Tall_Leaves', 'Tree_Leaning_Leaves', 'Tree_Leaves', 'Tree_Tall_Leaves']):
    plant(name, tree.location.copy(), tree.scale.copy(), tree.rotation_euler.copy())
for i in range(72):
    cluster, within = divmod(i, 6)
    side = -1 if cluster % 2 else 1
    z = -24 - (cluster // 2) * 2.7 + .85 * math.sin(within * 2.399)
    x = -12 + side * (3.35 + .55 * math.sin(cluster * 1.3)) + .45 * math.cos(within * 2.399)
    scale = .7 + .35 * (i % 4) / 3
    plant(['Fern', 'Broadleaf_Clump', 'Grass_Tuft', 'Low_Shrub'][(i + cluster) % 4],
          Vector(position(x, height_at(x, z) + .02, z)), (scale,) * 3, (0, 0, i * 2.399))

# Retain originals for the second-half bake and future editing.
author = bpy.data.collections.new('Authoring patch')
scene.collection.children.link(author)
for obj in visuals + foliage:
    for collection in list(obj.users_collection): collection.objects.unlink(obj)
    author.objects.link(obj)

bpy.ops.object.select_all(action='DESELECT')
for obj in visuals: obj.select_set(True)
bpy.context.view_layer.objects.active = visuals[0]
bpy.ops.object.duplicate()
bpy.ops.object.join()
target = bpy.context.object
target.name = 'ForestPatch_Baked'
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
target.data.validate(clean_customdata=True)
target.data.update()
for obj in visuals:
    obj.hide_render = True
    obj.hide_set(True)

# Preserve world-space procedural bark continuity, with wider UV gutters than
# the shared prototype atlas. Bake AFTER final placement, never rotate the bake.
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=.015)
bpy.ops.object.mode_set(mode='OBJECT')
atlas = bpy.data.images.new('Forest patch placed diffuse', width=2048, height=2048, alpha=False)
atlas.filepath_raw = str(OUT / 'forest-patch-atlas.png')
atlas.file_format = 'PNG'
for i, original in enumerate(list(target.data.materials)):
    mat = original.copy()
    target.data.materials[i] = mat
    tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image = atlas
    mat.node_tree.nodes.active = tex
scene.render.bake.use_pass_color = True
scene.render.bake.use_pass_direct = True
scene.render.bake.use_pass_indirect = True
scene.render.bake.margin = 12
print('BAKING placed forest patch', flush=True)
bpy.ops.object.bake(type='DIFFUSE')
atlas.save()
atlas.pack()
material = bpy.data.materials.new('ForestPatch_Diffuse')
material.use_nodes = True
tex = material.node_tree.nodes.new('ShaderNodeTexImage')
tex.image = atlas
material.node_tree.links.new(tex.outputs['Color'], material.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
target.data.materials.clear()
target.data.materials.append(material)
for polygon in target.data.polygons: polygon.material_index = 0

# The original road remains the walking surface; only new trunks need proxies.
colliders = []
for tree in trees:
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=.5, depth=3.8,
        location=tree.location + Vector((0, 0, 1.9)))
    obj = bpy.context.object
    obj.name = 'ForestPatch_Collider'
    colliders.append(obj)
bpy.ops.object.select_all(action='DESELECT')
for obj in colliders: obj.select_set(True)
bpy.context.view_layer.objects.active = colliders[0]
bpy.ops.object.join()
collision = bpy.context.object
collision.name = 'ForestPatch_Collision'
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
collision.hide_render = True
for obj in foliage: obj.hide_render = False
bpy.ops.object.select_all(action='DESELECT')
for obj in foliage: obj.select_set(True)
bpy.context.view_layer.objects.active = foliage[0]
bpy.ops.object.join()
leaf_mesh = bpy.context.object
leaf_mesh.name = 'ForestPatch_Foliage'
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
leaf_material = bpy.data.materials.new('ForestPatch_LeafColour')
leaf_material.use_nodes = True
colour_node = leaf_material.node_tree.nodes.new('ShaderNodeVertexColor')
colour_node.layer_name = leaf_mesh.data.color_attributes.active_color.name
leaf_material.node_tree.links.new(colour_node.outputs['Color'], leaf_material.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
leaf_mesh.data.materials.clear()
leaf_mesh.data.materials.append(leaf_material)
for polygon in leaf_mesh.data.polygons: polygon.material_index = 0
collision.select_set(True)
target.select_set(True)
source = ROOT / 'art/source/forest-patch.blend'
export = ROOT / 'public/models/forest-patch.glb'
bpy.ops.wm.save_as_mainfile(filepath=str(source), compress=True)
bpy.ops.export_scene.gltf(filepath=str(export), export_format='GLB', use_selection=True,
    export_image_format='JPEG', export_image_quality=94)
report = {'stage': 'assembled sun/shade patch',
          'source': str(source.relative_to(ROOT)), 'bytes': export.stat().st_size,
          'atlas': 2048, 'samples': 32, 'slabs': 72, 'trees': len(trees), 'groundCover': 72,
          'seconds': round(time.monotonic() - started, 1)}
(OUT / 'forest-patch-report.json').write_text(json.dumps(report, indent=2) + '\n')
print('FOREST_PATCH ' + json.dumps(report), flush=True)

# Rebuild only the review context; original world stays unchanged.
import sys
sys.path.insert(0, str(Path(__file__).parent))
from world_art_context import export_context
report['removedContextProxies'] = export_context()
(OUT / 'forest-patch-report.json').write_text(json.dumps(report, indent=2) + '\n')
