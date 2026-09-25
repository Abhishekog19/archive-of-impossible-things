"""Export art-review context without rewriting the source world."""
import bpy
import bmesh
from pathlib import Path
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[2]

def export_context(include_hub=None):
    if include_hub is None:
        include_hub = (ROOT / "public/models/hub-art.glb").exists()
    bpy.ops.wm.open_mainfile(filepath=str(ROOT / 'art/source/world-blockout.blend'))
    removed = []
    include_approach = (ROOT/'public/models/forest-approach.glb').exists()
    include_canopy = (ROOT/'public/models/forest-canopy.glb').exists()
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
        clearing = x < -17 and -77<z<-61
        approach_region = -27<x<4 and -65<z<-40
        canopy_region = -29<x<4 and -90<z<-65 and not clearing
        approach_plant = obj.name.startswith(('Deep canopy trunk','Deep canopy crown',
            'Forest shoulder','Woodland background trunk','Woodland middle crown',
            'Woodland upper crown','Woodland lower silhouette','Forest crown','Tree trunk','Tree limb','Woodland shoulder'))
        approach_trunk = obj.name.startswith('Collision') and obj.dimensions.z>8 and max(obj.dimensions.x,obj.dimensions.y)<3
        approach_proxy = ((include_approach and approach_region) or (include_canopy and canopy_region)) and (approach_plant or approach_trunk)
        if include_approach and obj.name.startswith('Connected paving'):
            # Replace only the dressed road faces, retaining the independent
            # resident collider and the deeper forest's unfinished paving.
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            limit = -90 if include_canopy else -65
            covered = [f for f in bm.faces if limit < -(obj.matrix_world@f.calc_center_median()).y < -40
                       and not ((obj.matrix_world@f.calc_center_median()).x < -17
                                and -77 < -(obj.matrix_world@f.calc_center_median()).y < -61)]
            bmesh.ops.delete(bm,geom=covered,context='FACES')
            bm.to_mesh(obj.data)
            bm.free()
        if (local and (plant_proxy or trunk_proxy)) or hub_proxy or approach_proxy:
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
