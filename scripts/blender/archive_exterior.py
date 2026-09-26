"""First REF7 production pass: coursed facade, worn arches and fused tree/roots."""
import bpy
import bmesh
import math
import random
import json
import sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
from placed_art import merge, leaf_crown, color_material, lighting, bake
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'.artifacts/blender'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
lighting()
rng = random.Random(9277)
prefixes = ('Stepped archive facade','Archive central crown','Archive upper facade',
    'Archive upper broken belt','Facade broken pinnacle','Archive arch pier',
    'Archive arch voussoir','Archive hero tree','Hero spreading limb','Wrapping facade root',
    'Hero tree crown','Hero secondary crown')
with bpy.data.libraries.load(str(ROOT/'art/source/world-blockout.blend'),link=False) as (src,dst):
    dst.objects = [n for n in src.objects if n.startswith(prefixes)]
sources = dst.objects
with bpy.data.libraries.load(str(ROOT/'art/source/archive-kit.blend'),link=False) as (src,dst):
    dst.objects = ['Author_Slab_1','Author_Tree_Tall']
stone_material = dst.objects[0].data.materials[0]
wood_material = dst.objects[1].data.materials[0]
stone,wood,crowns = [],[],[]
block_count = 0
def worn(obj,amount=.045):
    bpy.context.view_layer.objects.active = obj
    bevel = obj.modifiers.new('Worn stone edges','BEVEL')
    bevel.width = amount
    bevel.segments = 1
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    for v in obj.data.vertices: v.co += Vector(tuple(rng.uniform(-.018,.018) for _ in range(3)))

for source in sources:
    z = -source.location.y
    if source.name.startswith('Archive arch'):
        # The same blockout prefix is also used by the hall; it stays for PD03.
        points = [source.matrix_basis@v.co for v in source.data.vertices]
        z = -sum(p.y for p in points)/len(points)
        if not -117<z<-110: continue
    if source.name.startswith(('Hero tree crown','Hero secondary crown')):
        radius = tuple(source.scale)
        crowns.append(leaf_crown('Hero broadleaf sprays',source.location,radius,len(crowns)+927,1800,leaf_scale=1.5))
        continue
    if source.name.startswith(('Archive hero tree','Hero spreading limb','Wrapping facade root')):
        bpy.context.collection.objects.link(source)
        source.data.materials.clear();source.data.materials.append(wood_material)
        wood.append(source)
        continue
    if source.name.startswith('Archive arch voussoir'):
        bpy.context.collection.objects.link(source)
        source.data.materials.clear();source.data.materials.append(stone_material)
        worn(source)
        stone.append(source)
        continue
    points = [source.matrix_basis@v.co for v in source.data.vertices]
    lo = Vector(tuple(min(p[i] for p in points) for i in range(3)))
    hi = Vector(tuple(max(p[i] for p in points) for i in range(3)))
    rows = max(1,round((hi.z-lo.z)/.7))
    for row in range(rows):
        count = max(1,round((hi.x-lo.x)/1.4))
        cuts = [lo.x]+[lo.x+(hi.x-lo.x)*i/count+rng.uniform(-.16,.16) for i in range(1,count)]+[hi.x]
        for i in range(count):
            bpy.ops.mesh.primitive_cube_add(size=1)
            obj = bpy.context.object
            obj.name = 'Facade limestone course'
            obj.location = ((cuts[i]+cuts[i+1])/2,(lo.y+hi.y)/2+rng.uniform(-.035,.035),lo.z+(row+.5)*(hi.z-lo.z)/rows)
            obj.scale = (cuts[i+1]-cuts[i]-.035,hi.y-lo.y-.025,(hi.z-lo.z)/rows-.035)
            bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
            obj.data.materials.append(stone_material)
            worn(obj)
            stone.append(obj);block_count += 1

stone_obj = merge('ArchiveExterior_Stone',stone)
bm = bmesh.new();bm.from_mesh(stone_obj.data)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
bm.to_mesh(stone_obj.data);bm.free()
wood_obj = merge('ArchiveExterior_Wood',wood)
# Union the interpenetrating root/limb junctions, preserving the authored silhouette.
bpy.context.view_layer.objects.active = wood_obj
sub = wood_obj.modifiers.new('Organic root curves','SUBSURF');sub.levels=2
bpy.ops.object.modifier_apply(modifier=sub.name)
remesh = wood_obj.modifiers.new('Joined roots','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.13
bpy.ops.object.modifier_apply(modifier=remesh.name)
smooth = wood_obj.modifiers.new('Soft branch junctions','SMOOTH');smooth.factor=.55;smooth.iterations=3
bpy.ops.object.modifier_apply(modifier=smooth.name)
dec = wood_obj.modifiers.new('Root detail budget','DECIMATE');dec.ratio=.35
bpy.ops.object.modifier_apply(modifier=dec.name)
for p in wood_obj.data.polygons: p.use_smooth=True
foliage = merge('ArchiveExterior_Foliage',crowns)
color_material(foliage)
bake([(stone_obj,2048),(wood_obj,2048)],OUT)
bpy.ops.object.select_all(action='DESELECT')
for obj in (stone_obj,wood_obj,foliage): obj.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/archive-exterior.blend'),compress=True)
export = ROOT/'public/models/archive-exterior.glb'
bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=True,export_image_format='JPEG',export_image_quality=92)
report = {'stage':'REF7 facade and hero tree first pass','masonryBlocks':block_count,'crowns':len(crowns),'bytes':export.stat().st_size,'atlases':[2048,2048]}
(OUT/'archive-exterior-report.json').write_text(json.dumps(report,indent=2)+'\n')
from world_art_context import export_context
export_context()
print(json.dumps(report),flush=True)
