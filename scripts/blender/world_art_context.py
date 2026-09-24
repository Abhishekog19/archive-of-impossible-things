"""Export art-review context without rewriting the source world."""
import bpy
from pathlib import Path
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[2]

def export_context(include_hub=None):
    if include_hub is None:
        include_hub = (ROOT / "public/models/hub-art.glb").exists()
    bpy.ops.wm.open_mainfile(filepath=str(ROOT / 'art/source/world-blockout.blend'))
    removed = []
    def numbered(prefix,index): return prefix+('.'+str(index).zfill(3) if index else '')
    hub_trees = {numbered('Tree trunk',i) for i in (0,1,2,3,4,80,81,82)}
    # Distant trees use three crowns, so their crown indices differ from trunks.
    # Match the remaining foreground crowns by their positions below instead.
    hub_trees.update(numbered(prefix,i) for prefix in ('Tree limb','Forest crown') for i in range(25))
    for obj in list(bpy.context.scene.objects):
        if obj.type != 'MESH': continue
        centre = sum((obj.matrix_world @ Vector(p) for p in obj.bound_box), Vector()) / 8
        x, z = centre.x, -centre.y
        local = -21 < x < -4 and -40 < z < -17
        plant_proxy = obj.name.startswith(('Tree trunk', 'Tree limb', 'Forest crown', 'Woodland shoulder'))
        hub_region = abs(x)<27 and -16<z<16
        hub_plant = hub_region and obj.name.startswith(('Tree trunk','Tree limb','Forest crown','Understory proxy','Woodland shoulder'))
        trunk_proxy = obj.name.startswith('Collision') and obj.dimensions.z > 7 and obj.dimensions.x < 1.2 and obj.dimensions.y < 1.2
        hub_proxy = include_hub and (obj.name.startswith(('Plaza paving', 'Plaza ring', 'Column base', 'Broken column course')) or obj.name in hub_trees or hub_plant)
        if (local and (plant_proxy or trunk_proxy)) or hub_proxy:
            removed.append(obj.name)
            bpy.data.objects.remove(obj, do_unlink=True)
    for mat in list(bpy.data.materials):
        objects = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.data.materials and o.data.materials[0] == mat]
        if not objects: continue
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects: obj.select_set(True)
        bpy.context.view_layer.objects.active = objects[0]
        bpy.ops.object.join()
        obj = bpy.context.object
        obj.name = 'Collision' if mat.name == 'Collision only' else mat.name.replace(' ', '_')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.export_scene.gltf(filepath=str(ROOT / 'public/models/world-art-context.glb'), export_format='GLB', export_texcoords=False)

    return removed
