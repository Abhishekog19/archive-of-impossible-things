"""REF10 lighting risk study, extracted from the existing editable world blockout.

Retains the authored cavern outline. Source world and user hub files are read-only.
The atlas proves portable illumination, not the Phase E final rock/material pass.
"""
import bpy
import math
import json
import time
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.artifacts/blender'
started = time.monotonic()
bpy.ops.wm.open_mainfile(filepath=str(ROOT / 'art/source/world-blockout.blend'))
prefixes = ('Cavern wall shell', 'Cavern shore', 'Shore rock lip',
            'Cavern rock buttress', 'Cavern game shelf', 'Continuous descent shell',
            'Archive descent', 'Descent shoulder')
visuals = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name.startswith(prefixes)]
pool = bpy.data.objects.get('Cavern pool')
assert pool and len(visuals) > 50, 'Expected editable cavern objects in world source'
for obj in list(bpy.context.scene.objects):
    if obj not in visuals and obj != pool:
        bpy.data.objects.remove(obj, do_unlink=True)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 40
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 6
scene.render.threads_mode = 'FIXED'
scene.render.threads = 6
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get('Background')
bg.inputs['Color'].default_value = (.42, .55, .68, 1)
bg.inputs['Strength'].default_value = .045

def point(p): return Vector((p[0], -p[2], p[1]))

# Broad daylight enters the existing upper opening; illumination is baked.
bpy.ops.object.light_add(type='AREA', location=point((-12, 20, -205)))
light = bpy.context.object
light.name = 'Oculus diffuse bake source'
light.data.energy = 5000
light.data.shape = 'DISK'
light.data.size = 2.5
light.data.color = (.76, .86, 1)
light.rotation_euler = (point((-10, -7.5, -202)) - light.location).to_track_quat('-Z', 'Y').to_euler()

# The pool is a separate runtime shader, never part of the diffuse atlas.
pool.name = 'Pool_study'
pool.hide_render = True
pool.hide_set(True)
colliders = []
for obj in visuals:
    obj.hide_render = False
    obj.hide_set(False)
    if not obj.name.startswith(('Shore rock lip', 'Cavern rock buttress')):
        proxy = obj.copy()
        proxy.data = obj.data.copy()
        proxy.data.materials.clear()
        bpy.context.collection.objects.link(proxy)
        proxy.hide_render = True
        proxy.hide_set(True)
        colliders.append(proxy)

stone = bpy.data.materials.new('Cavern study diffuse slate')
stone.use_nodes = True
nodes = stone.node_tree.nodes
bsdf = nodes.get('Principled BSDF')
bsdf.inputs['Roughness'].default_value = .95
noise = nodes.new('ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = .35
noise.inputs['Detail'].default_value = 1.5
coords = nodes.new('ShaderNodeTexCoord')
stone.node_tree.links.new(coords.outputs['Object'], noise.inputs['Vector'])
ramp = nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position = .2
ramp.color_ramp.elements[0].color = (.21, .26, .29, 1)
ramp.color_ramp.elements[1].position = .8
ramp.color_ramp.elements[1].color = (.235, .28, .31, 1)
stone.node_tree.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
stone.node_tree.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
for obj in visuals:
    obj.data.materials.clear()
    obj.data.materials.append(stone)

bpy.ops.object.select_all(action='DESELECT')
for obj in visuals: obj.select_set(True)
bpy.context.view_layer.objects.active = visuals[0]
bpy.ops.object.join()
target = bpy.context.object
target.name = 'Cavern_Baked'
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=.006)
bpy.ops.object.mode_set(mode='OBJECT')
atlas = bpy.data.images.new('Cavern study diffuse atlas', width=1024, height=1024, alpha=False)
atlas.file_format = 'PNG'
atlas.filepath_raw = str(OUT / 'cavern-study-atlas.png')
tex = nodes.new('ShaderNodeTexImage')
tex.image = atlas
nodes.active = tex
scene.render.bake.use_pass_direct = True
scene.render.bake.use_pass_indirect = True
scene.render.bake.use_pass_color = True
scene.render.bake.margin = 8
print('BAKING cavern study', flush=True)
bpy.ops.object.bake(type='DIFFUSE')
atlas.save()
atlas.pack()

mat = bpy.data.materials.new('Cavern portable diffuse')
mat.use_nodes = True
tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
tex.image = atlas
mat.node_tree.links.new(tex.outputs['Color'], mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
target.data.materials.clear()
target.data.materials.append(mat)
for polygon in target.data.polygons: polygon.material_index = 0
bpy.ops.object.select_all(action='DESELECT')
for obj in colliders:
    obj.hide_set(False)
    obj.select_set(True)
bpy.context.view_layer.objects.active = colliders[0]
bpy.ops.object.join()
collision = bpy.context.object
collision.name = 'Cavern_Collision'
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
pool.hide_set(False)
pool.select_set(True)
bpy.context.view_layer.objects.active = pool
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
target.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'art/source/cavern-study.blend'), compress=True)
export = ROOT / 'public/models/cavern-study.glb'
bpy.ops.export_scene.gltf(filepath=str(export), export_format='GLB', use_selection=True,
                          export_image_format='JPEG', export_image_quality=92)
report = {'bytes': export.stat().st_size, 'seconds': round(time.monotonic()-started, 1),
          'atlas': [1024, 1024], 'samples': 40, 'source': 'art/source/cavern-study.blend',
          'scope': 'Existing cavern blockout with baked diffuse light; final rock art remains Phase E'}
(OUT / 'cavern-study-report.json').write_text(json.dumps(report, indent=2)+'\n')
print('CAVERN_STUDY '+json.dumps(report), flush=True)
