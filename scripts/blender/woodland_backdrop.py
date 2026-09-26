"""Replace remaining hub/forest crown proxies with grouped broadleaf silhouettes."""
import bpy
import json
import sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
from placed_art import leaf_crown, merge, color_material
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'.artifacts/blender'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/source/world-blockout.blend'))
placements = []
prefixes = ('Woodland middle crown','Woodland upper crown','Woodland lower silhouette',
    'Forest crown','Deep canopy crown','Understory proxy','Woodland shoulder')
def numbered(prefix,i): return prefix+('.'+str(i).zfill(3) if i else '')
hub_crowns = {numbered('Forest crown',i) for i in range(25)}
for obj in bpy.context.scene.objects:
    if obj.type!='MESH' or not obj.name.startswith(prefixes): continue
    centre = sum((obj.matrix_world@Vector(p) for p in obj.bound_box),Vector())/8
    x,z = centre.x,-centre.y
    if not -108<z<25: continue
    # Existing placed art already owns these crowns/shoulders.
    if obj.name in hub_crowns or (abs(x)<27 and -16<z<16): continue
    if -21<x<-4 and -40<z<-17: continue
    if -45<x<16 and -97<z<-40: continue
    radius = tuple(max(.45,d/2) for d in obj.dimensions)
    placements.append((tuple(centre),radius))
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
groups = {i:[] for i in range(5)}
for i,(centre,radius) in enumerate(placements):
    zone = max(0,min(4,int(centre[1]/30)+1))
    groups[zone].append(leaf_crown('Backdrop broadleaf sprays',centre,radius,92700+i,
        360 if max(radius)>3 else 120,leaf_scale=2.1 if max(radius)>3 else 1.5))
exports = []
for zone,objects in groups.items():
    if not objects: continue
    obj = merge('WoodlandBackdrop_'+str(zone),objects)
    color_material(obj)
    exports.append(obj)
bpy.ops.object.select_all(action='DESELECT')
for obj in exports: obj.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/woodland-backdrop.blend'),compress=True)
export = ROOT/'public/models/woodland-backdrop.glb'
bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=True)
report = {'crowns':len(placements),'spatialBatches':len(exports),'triangles':sum(len(o.data.polygons)*2 for o in exports),'bytes':export.stat().st_size}
(OUT/'woodland-backdrop-report.json').write_text(json.dumps(report,indent=2)+'\n')
from world_art_context import export_context
export_context()
print(json.dumps(report),flush=True)
