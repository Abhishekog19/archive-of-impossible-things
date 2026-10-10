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
from archive_surface import damp_material, archive_bark, root_tendril, ivy_ribbon
from natural_foliage import layered_crown
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
    dst.objects = ['Author_Slab_'+str(i) for i in range(1,7)]+['Author_Tree_Tall']
kit = {o.name:o for o in dst.objects}
stone_material = kit['Author_Slab_1'].data.materials[0]
wood_material = archive_bark()
stone_variants = [damp_material(stone_material,'Archive damp limestone '+str(i),m) for i,m in enumerate((.12,.32,.65,.85))]
stone,wood,crowns = [],[],[]
block_count = 0
def worn(obj,amount=.025):
    bpy.context.view_layer.objects.active = obj
    bevel = obj.modifiers.new('Worn stone edges','BEVEL')
    bevel.width = amount
    bevel.segments = 1
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    for v in obj.data.vertices: v.co += Vector(tuple(rng.uniform(-.014,.014) for _ in range(3)))

for source in sources:
    z = -source.location.y
    if source.name.startswith('Archive arch'):
        # The same blockout prefix is also used by the hall; it stays for PD03.
        points = [source.matrix_basis@v.co for v in source.data.vertices]
        z = -sum(p.y for p in points)/len(points)
        if not -117<z<-110: continue
    if source.name.startswith(('Hero tree crown','Hero secondary crown')):
        radius = tuple(source.scale)
        crowns.append(layered_crown('Hero layered crown',source.location,radius,len(crowns)+927,woodland=True,near=True))
        continue
    if source.name.startswith('Wrapping facade root'):continue
    if source.name.startswith('Hero spreading limb'):continue
    if source.name.startswith('Archive hero tree'):
        wood.append(root_tendril('Front wrapped hero trunk',
            [(-23,110.8,1.65),(-22,111,9),(-20.8,112.2,15),(-19,115.5,20),(-15,118,27)],
            2.1,wood_material))
        continue
    if source.name.startswith('Archive arch voussoir'):
        bpy.context.collection.objects.link(source)
        source.data.materials.clear();source.data.materials.append(rng.choice(stone_variants))
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
            # Incomplete upper courses make a broken silhouette, not a neat wall top.
            if row==rows-1 and count>2 and rng.random()<.3: continue
            bpy.ops.mesh.primitive_cube_add(size=1)
            obj = bpy.context.object
            obj.name = 'Facade limestone course'
            obj.location = ((cuts[i]+cuts[i+1])/2,(lo.y+hi.y)/2+rng.uniform(-.035,.035),lo.z+(row+.5)*(hi.z-lo.z)/rows)
            obj.scale = (cuts[i+1]-cuts[i]-.035,hi.y-lo.y-.025,(hi.z-lo.z)/rows-.035)
            if row==rows-1:obj.scale.z*=rng.uniform(.55,1)
            obj.rotation_euler.y=rng.uniform(-.012,.012)
            bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
            obj.data.materials.append(rng.choice(stone_variants))
            worn(obj)
            stone.append(obj);block_count += 1

# Paved courtyard and threshold: preserve the existing flat walking elevation.
paving=[]
for row in range(20):
    z=-96.5-row*.96
    for col in range(19):
        x=-12+(col-9)*1.12+(row%2)*.48
        shoulder=3+8*min(1,row/7)
        if abs(x+12)>shoulder+rng.uniform(-.4,.4):continue
        if row>=17 and abs(x+12)>2.8:continue
        if abs(x+12)>4 and rng.random()<.24:continue
        src=kit['Author_Slab_'+str(1+(row+col)%6)]
        obj=bpy.data.objects.new('Courtyard worn flagstone',src.data.copy())
        bpy.context.collection.objects.link(obj)
        obj.location=(x+rng.uniform(-.025,.025),-z,1.56)
        obj.rotation_euler.z=rng.uniform(-.035,.035);obj.scale=(.93,.85,.72)
        obj.data.materials.clear();obj.data.materials.append(rng.choice(stone_variants))
        paving.append(obj)
# Moss floor between stones, with contextual tree/contact shadows in its bake.
points=[]
for side in (-1,1):
    rows=range(12) if side<0 else reversed(range(12))
    for row in rows:
        z=93+row*1.9
        width=3.4+11.2*min(1,row/6)**.8+.35*math.sin(row*1.9)
        points.append((-12+side*width,z,1.625))
data=bpy.data.meshes.new('Irregular courtyard soil');data.from_pydata(points,[],[tuple(reversed(range(len(points))))]);data.update()
ground=bpy.data.objects.new('Courtyard moss earth',data);bpy.context.collection.objects.link(ground)
soil=bpy.data.materials.new('Archive moss soil');soil.use_nodes=True
nodes,links=soil.node_tree.nodes,soil.node_tree.links
noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=24
ramp=nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].color=(.055,.079,.023,1)
ramp.color_ramp.elements[1].color=(.19,.22,.07,1)
links.new(noise.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs[0],nodes['Principled BSDF'].inputs['Base Color'])
ground.data.materials.append(soil);paving.append(ground)
# Rubble gathers at the facade feet and outer edges, leaving the central lane clear.
for i in range(54):
    x=rng.choice((-1,1))*rng.uniform(5,12)-12;z=rng.uniform(-110,-99)
    src=kit['Author_Slab_'+str(i%6+1)]
    obj=bpy.data.objects.new('Archive fallen masonry',src.data.copy());bpy.context.collection.objects.link(obj)
    obj.location=(x,-z,1.56);obj.scale=(rng.uniform(.5,1.1),rng.uniform(.5,1.1),rng.uniform(1.4,3.1))
    obj.rotation_euler=(rng.uniform(-.25,.25),rng.uniform(-.2,.2),rng.random()*math.tau)
    obj.data.materials.clear();obj.data.materials.append(stone_variants[i%4]);paving.append(obj)
# Roots begin inside the trunk or a connected parent and taper into soil/stone.
# Broad primary flares stay by the left buttress; two thinner roots follow the
# masonry ledges above the doorway instead of covering the whole facade.
root_paths=[
    # Tapered canopy limbs replace the blockout's blunt cones. Their tips end
    # inside the existing crown masses; the door and ground route stay clear.
    ([(-19,116,20),(-15,116.6,22.5),(-10,117,25),(-7,117,26)],1.2),
    ([(-19,116,20),(-23,116.8,21),(-26,117.4,22),(-28,118,23)],1.15),
    ([(-19,116,20),(-17.8,119,23.5),(-17,122,27),(-16,124,30)],1.1),
    ([(-22,111,8.8),(-23.2,110.4,6),(-25,110.5,2.3),(-28,105,1.61)],1.05),
    ([(-22.3,110.8,6),(-21,110.4,4),(-19.4,110.4,2),(-17.9,107.5,1.60)],.7),
    ([(-21,111.8,13),(-20.6,111,12.1),(-16,111.65,11.45),(-10,111.7,11.5),(-5.4,111,9.7),(-4.7,111,5),(-3.8,110,1.61)],.68),
    ([(-19.3,115,18.8),(-18.3,113.8,18.5),(-15,113.5,19),(-10,114,19.5),(-6.1,114,18.8),(-5,114,17.6)],.6),
    ([(-22.6,110.8,4.8),(-25,112.2,2.2),(-27,117,1.6)],.5),
]
for points,radius in root_paths:
    wood.append(root_tendril('Attached fluted facade root',points,radius,wood_material))
for i in range(8):
    side=-1 if i<4 else 1
    origin=(-24.8,110.5,2.25) if side<0 else (-19.5,110.5,2.1)
    wood.append(root_tendril('Buried root branch',[origin,
        (origin[0]+side*.9,109.8-i*.2,1.85),
        (origin[0]+side*(1.5+i*.24),108.4-i*.32,1.59)],.18,wood_material))
# Clinging vines sit on front faces and hang from ledges, not across the doorway.
for i,(x,y,top,length) in enumerate([(-25,111.46,7,4),(-23.2,111.45,6.7,3.8),
    (-20.5,111.43,10.8,6),(-18.1,111.46,11,3),(-6.5,111.46,10,5),(-3.2,111.44,10,6),
    (-1,111.45,6,3),(-17.8,112.94,19,5),(-16,112.94,19.4,3),(-7,112.94,18,4)]):
    crowns.append(ivy_ribbon('Facade hanging ivy',x,y,top,length,92720+i))
for i in range(44):
    x=-12+rng.choice((-1,1))*rng.uniform(4.4,13);z=rng.uniform(-112,-96)
    crowns.append(leaf_crown('Courtyard broadleaf cluster',(x,-z,1.8),(.65,.6,.4),92800+i,65,.48))
# Recessed solid tympanum connects the seal to the upper facade. Its curved top
# fits inside the existing arch; it is well above the traversable entrance.
panel_rng=random.Random(100807)
for row in range(10):
    bottom=12.35+row*.59;top=bottom+.60
    width=2.53 if top<=15.9 else math.sqrt(max(0,2.53**2-(top-15.9)**2))
    if width<.1:continue
    count=max(1,round(width*2/1.2))
    for col in range(count):
        left=-12-width+col*2*width/count;right=left+2*width/count
        bpy.ops.mesh.primitive_cube_add(size=1,location=((left+right)/2,114.5,(bottom+top)/2))
        panel=bpy.context.object;panel.name='Recessed seal masonry'
        panel.scale=(right-left-.008,.55,top-bottom)
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        panel.data.materials.append(stone_variants[panel_rng.randrange(2)])
        worn(panel,.012);stone.append(panel)
# Shallow stone medallion under the upper arch echoes REF7's carved archive seal.
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=1.7,depth=.22,location=(-12,114.1,15.7),rotation=(math.pi/2,0,0))
seal=bpy.context.object;seal.name='Carved archive seal';seal.data.materials.append(stone_variants[1]);worn(seal,.03);stone.append(seal)
for i in range(12):
    a=i*math.tau/12
    bpy.ops.mesh.primitive_cube_add(size=1,location=(-12+math.cos(a)*1.12,113.93,15.7+math.sin(a)*1.12))
    mark=bpy.context.object;mark.name='Seal radial carving';mark.scale=(.6,.09,.10);mark.rotation_euler.y=-a
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    mark.data.materials.append(stone_variants[0]);worn(mark,.02);stone.append(mark)
stone_obj = merge('ArchiveExterior_Stone',stone)
bm = bmesh.new();bm.from_mesh(stone_obj.data)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
bm.to_mesh(stone_obj.data);bm.free()
wood_obj = merge('ArchiveExterior_Wood',wood)
bm=bmesh.new();bm.from_mesh(wood_obj.data)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
bm.to_mesh(wood_obj.data);bm.free()
# Union the interpenetrating root/limb junctions, preserving the authored silhouette.
bpy.context.view_layer.objects.active = wood_obj
sub = wood_obj.modifiers.new('Organic root curves','SUBSURF');sub.levels=2
bpy.ops.object.modifier_apply(modifier=sub.name)
remesh = wood_obj.modifiers.new('Joined roots','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.13
bpy.ops.object.modifier_apply(modifier=remesh.name)
smooth = wood_obj.modifiers.new('Soft branch junctions','SMOOTH');smooth.factor=.35;smooth.iterations=2
bpy.ops.object.modifier_apply(modifier=smooth.name)
dec = wood_obj.modifiers.new('Root detail budget','DECIMATE');dec.ratio=.35
bpy.ops.object.modifier_apply(modifier=dec.name)
wood_obj.data.validate(clean_customdata=True)
wood_obj.data.update()
for p in wood_obj.data.polygons: p.use_smooth=True
foliage = merge('ArchiveExterior_Foliage',crowns)
color_material(foliage)
paving_obj=merge('ArchiveExterior_Courtyard',paving)
bake([(stone_obj,2048),(wood_obj,2048),(paving_obj,2048)],OUT)
bpy.ops.object.select_all(action='DESELECT')
for obj in (stone_obj,wood_obj,foliage,paving_obj): obj.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/archive-exterior.blend'),compress=True)
export = ROOT/'public/models/archive-exterior.glb'
bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=True,export_image_format='JPEG',export_image_quality=92)
report = {'stage':'Phase 5 connected roots and courtyard','masonryBlocks':block_count,'courtyardPieces':len(paving),'vegetationGroups':len(crowns),'rootFingers':8,'bytes':export.stat().st_size,'atlases':[2048]*3}
(OUT/'archive-exterior-report.json').write_text(json.dumps(report,indent=2)+'\n')
from world_art_context import export_context
from archive_exterior_collision import export_with_collision
export_with_collision()
export_context()
print(json.dumps(report),flush=True)
