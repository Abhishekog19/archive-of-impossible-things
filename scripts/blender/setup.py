"""Phase 0 tooling check only. Creates no environment geometry or game assets."""
import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
output = Path(args.output).resolve()
output.mkdir(parents=True, exist_ok=True)

# Empty, editable starting file. Keep startup/user preferences untouched.
bpy.ops.wm.read_factory_settings(use_empty=True)
# Background setup does not need OS thumbnails or numbered backup files.
bpy.context.preferences.filepaths.file_preview_type = 'NONE'
bpy.context.preferences.filepaths.save_version = 0
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
for name in ['Terrain', 'Architecture', 'Vegetation', 'Water', 'Colliders', 'Landmarks', 'Cameras']:
    scene.collection.children.link(bpy.data.collections.new(name))
scene['project'] = 'Archive of Impossible Things'
scene['stage'] = 'Phase 0 - setup only; no environment authored'
scene['units'] = '1 Blender unit = 1 metre; glTF exporter handles axis conversion'
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
bpy.ops.wm.save_as_mainfile(filepath=str(output / 'environment-template.blend'))

# Disposable cube checks rendering and GLB round-trip. Never exported to public/.
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
cube = bpy.context.object
cube.name = 'SETUP_ONLY_cube_1m'
material = bpy.data.materials.new('SETUP_ONLY_stone')
material.use_nodes = True
shader = material.node_tree.nodes.get('Principled BSDF')
shader.inputs['Base Color'].default_value = (0.39, 0.37, 0.30, 1)
shader.inputs['Roughness'].default_value = 0.9
cube.data.materials.append(material)
cube.data.uv_layers.new(name='LightmapUV')

bpy.ops.object.camera_add(location=(2, -3, 2))
camera = bpy.context.object
camera.rotation_euler = (Vector((0, 0, 0.5)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
camera.data.lens = 45
scene.camera = camera
bpy.ops.object.light_add(type='AREA', location=(1, -2, 4))
light = bpy.context.object
light.data.energy = 300
light.data.shape = 'DISK'
light.data.size = 3
light.rotation_euler = (Vector((0, 0, 0.5)) - light.location).to_track_quat('-Z', 'Y').to_euler()
scene.world = bpy.data.worlds.new('SETUP_ONLY_world')
scene.world.use_nodes = True
scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value = 0.25
scene.render.resolution_x = 128
scene.render.resolution_y = 128
scene.render.resolution_percentage = 100
scene.cycles.samples = 8
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(output / 'setup-render.png')
bpy.ops.render.render(write_still=True)

bpy.ops.object.select_all(action='DESELECT')
cube.select_set(True)
bpy.context.view_layer.objects.active = cube
glb = output / 'setup-only.glb'
bpy.ops.export_scene.gltf(filepath=str(glb), export_format='GLB', use_selection=True, export_texcoords=True)
assert glb.read_bytes()[:4] == b'glTF', 'Invalid GLB header'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(glb))
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
assert len(meshes) == 1, 'GLB must contain exactly one test mesh'
assert all(abs(value - 1) < 0.001 for value in meshes[0].dimensions), 'Metre scale did not survive export'
assert len(meshes[0].data.materials) == 1, 'Material did not survive export'
report = {
    'blender_version': bpy.app.version_string,
    'python_version': sys.version.split()[0],
    'background_python': 'PASS',
    'cycles_cpu_render': 'PASS',
    'glb_export_import': 'PASS',
    'metre_scale': 'PASS',
    'material_round_trip': 'PASS',
    'exported_uv_layers': len(meshes[0].data.uv_layers),
    'glb_bytes': glb.stat().st_size,
    'template': str(output / 'environment-template.blend'),
    'environment_phase_1_started': False,
    'not_tested': ['Lightmap baking and browser binding', 'Vegetation instancing', 'Final visual quality', 'GPU performance'],
}
(output / 'setup-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf8')
print('AOIT_BLENDER_SETUP ' + json.dumps(report))
