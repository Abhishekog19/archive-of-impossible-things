"""PD03: placed REF8 arcades, broken roof, planted stone floor and exit portal."""
import bpy
import bmesh
import math
import random
import json
import sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).parent))
from placed_art import merge, leaf_crown, color_material, lighting, bake
from archive_surface import damp_material, ivy_ribbon

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.artifacts/blender'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
lighting()
rng = random.Random(9283)
with bpy.data.libraries.load(str(ROOT/'art/source/archive-kit.blend'), link=False) as (src, dst):
    dst.objects = ['Author_Slab_'+str(i) for i in range(1, 7)]
kit = {o.name: o for o in dst.objects}
base = kit['Author_Slab_1'].data.materials[0]
mats = [damp_material(base, 'Hall limestone '+str(i), m) for i, m in enumerate((.08, .23, .48, .72))]
walls, architecture, floor, plants = [], [], [], []


def finish(obj, name, group, material=None, wear=.025):
    obj.name = name
    obj.data.materials.clear()
    obj.data.materials.append(material or rng.choice(mats))
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if wear:
        mod = obj.modifiers.new('Weathered arris', 'BEVEL')
        mod.width = wear
        mod.segments = 1
        bpy.ops.object.modifier_apply(modifier=mod.name)
        for v in obj.data.vertices:
            v.co += Vector(tuple(rng.uniform(-.014, .014) for _ in range(3)))
    group.append(obj)
    return obj


def block(name, at, size, group=architecture, material=None):
    # Public helpers take browser X/Y/Z; convert once into Blender coordinates.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(at[0], -at[2], at[1]))
    obj = bpy.context.object
    obj.scale = (size[0], size[2], size[1])
    return finish(obj, name, group, material)


def arch(name, centre, radius, spring, depth=.85, axis='x', thickness=.66):
    cx, cz = centre
    pieces = 13 if radius > 3 else 11
    for i in range(pieces):
        a, b = i*math.pi/pieces+.008, (i+1)*math.pi/pieces-.008
        pts = []
        for d in (-depth/2, depth/2):
            for r, t in ((radius,a),(radius,b),(radius+thickness,b),(radius+thickness,a)):
                u, h = r*math.cos(t), spring+r*math.sin(t)
                x, z = (cx+u,cz+d) if axis=='x' else (cx+d,cz+u)
                pts.append((x,-z,h))
        data=bpy.data.meshes.new(name)
        data.from_pydata(pts, [], [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
        data.update()
        obj=bpy.data.objects.new(name,data)
        bpy.context.collection.objects.link(obj)
        finish(obj,name,architecture)


# Broad outer walls retain the solid side boundaries. Individual staggered courses
# and missing upper stones break their silhouettes without blocking the arcades.
for x in (-27, 3):
    for row in range(15):
        h=2.05+row*.82
        for col in range(15):
            z=-115-col*1.82-(row%2)*.45
            if z < -141: continue
            if row>11 and rng.random() < .24+(row-11)*.15: continue
            height=.805 if row<12 else rng.uniform(.4,.78)
            block('Hall wall limestone', (x+rng.uniform(-.045,.045),h,z), (1.38,height,1.805), walls)

# Column drums have readable moulded bases, taper, flutes and chipped capitals.
for x in (-19,-5):
    for col,z in enumerate((-119,-127,-135)):
        block('Arcade lower plinth',(x,1.91,z),(2.16,.5,2.16))
        block('Arcade stepped base',(x,2.27,z),(1.66,.23,1.66))
        for row in range(11):
            h=2.78+row*.69
            radius=.76-row*.015
            bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=radius,depth=.655,location=(x,-z,h))
            obj=bpy.context.object
            # Shallow alternating flutes retain a low polygon count and broad highlights.
            for v in obj.data.vertices:
                angle=math.atan2(v.co.y,v.co.x)
                if round(angle/(math.tau/16))%2: v.co.x*=.92;v.co.y*=.92
            obj.rotation_euler.z=(col%2)*.045+rng.uniform(-.014,.014)
            finish(obj,'Fluted limestone drum',architecture)
        block('Column neck',(x,10.12,z),(1.48,.23,1.48))
        block('Broken capital',(x,10.49,z),(1.95,.47,1.95))
    # Longitudinal bays frame the aisle as in REF8; roof is open overhead.
    for z in (-123,-131): arch('Side arcade voussoir',(x,z),3.5,10.35,axis='z',thickness=.73)

# The surviving transverse frame joins the rear bays; front frames are absent.
arch('Rear nave arch',(-12,-135),6,6.65,thickness=.9)
for x in (-18.45,-5.55):
    for row in range(7): block('Rear arch pier',(x,2.0+row*.66,-135),(.88,.63,.82))

# Broken roof islands over the side aisles cast contextual shadows. Their inside
# edge is staggered, with open gaps, instead of a continuous flat ceiling strip.
for side in (-1,1):
    for i in range(12):
        if i in ((2,7,10) if side<0 else (0,5,9)):continue
        width=rng.uniform(3.3,5.7)
        x=(-26.4+width/2) if side<0 else (2.4-width/2)
        block('Broken roof raft',(x,14.05,-119.8-i*1.7),(width,.62,1.63),walls)
        if i%3==0:
            block('Roof fracture crest',(x,14.65,-119.8-i*1.7),(width*.45,.55,1.18),walls)

# Rear portal stays aligned with the existing descent and its five-metre opening.
for row in range(14):
    h=2.05+row*.82
    # Staggered cuts, with two real lancet openings above the solid boundary sill.
    cuts=[-31]+[-31+i*1.98+rng.uniform(-.28,.28) for i in range(1,20)]+[7]
    cuts=sorted(set(c for c in cuts if -31<=c<=7))
    openings=[(-15,-9)]
    for cx in (-22,-2):
        if 4.1<h<9.8:
            width=1.7 if h<=8 else math.sqrt(max(0,1.7**2-(h-8)**2))
            openings.append((cx-width,cx+width))
    for lo,hi in zip(cuts,cuts[1:]):
        spans=[(lo,hi)]
        for a,b in openings:
            spans=[s for l,r in spans for s in ((l,min(r,a)),(max(l,b),r)) if s[1]-s[0]>.12]
        for l,r in spans:
            if row>10 and rng.random()<.18+(row-10)*.15:continue
            block('Rear wall course',((l+r)/2,h,-141+rng.uniform(-.025,.025)),(r-l-.015,.805,1.48),walls)
for cx in (-22,-2):
    arch('Rear lancet window',(cx,-141),1.7,8,1.55,thickness=.5)
    for side in (-1,1):
        for row in range(6):
            block('Window jamb',(cx+side*1.95,4.35+row*.62,-141),(.49,.6,1.54))
    block('Window sill',(cx,3.95,-141),(4.4,.3,1.8))
arch('Descent portal',(-12,-141),2.5,7.15,1.5,thickness=.9)
for x in (-14.95,-9.05):
    for row in range(8):block('Portal jamb',(x,2.0+row*.66,-141),(.88,.63,1.5))
# A pierced circular crown brings the rear silhouette closer to the reference.
for i in range(16):
    a=i*math.tau/16
    obj=block('Oculus ring',(-12+math.cos(a)*1.12,12+math.sin(a)*1.12,-141),(.55,.5,1.4))
    obj.rotation_euler.y=-a
# Masonry shoulders support the oculus, with a ragged crown around its opening.
for row in range(6):
    h=10.05+row*.66
    for side in (-1,1):
        inner=math.sqrt(max(0,1.5**2-(h-12)**2)) if abs(h-12)<1.5 else 0
        outer=2.9-rng.uniform(0,.6) if row>3 else 3
        if outer-inner>.15:
            block('Oculus surrounding masonry',(-12+side*(inner+outer)/2,h,-141),
                  (outer-inner-.025,.64,1.38),walls)

# Keep the 1.65m resident floor as the collision surface; worn flagstones sit on it.
for row in range(25):
    z=-115.6-row*1.01
    for col in range(25):
        x=-12+(col-12)*1.13
        if z>-116 and abs(x+12)>2.8:continue
        if abs(x+12)>4 and rng.random()<.13:continue
        src=kit['Author_Slab_'+str(1+(row+col)%6)]
        obj=bpy.data.objects.new('Hall flagstone',src.data.copy())
        bpy.context.collection.objects.link(obj)
        obj.location=(x+rng.uniform(-.026,.026),-z,1.56)
        obj.scale=(.95,.9,.7)
        obj.rotation_euler.z=rng.uniform(-.035,.035)
        obj.data.materials.clear();obj.data.materials.append(rng.choice(mats))
        floor.append(obj)
soil=bpy.data.materials.new('Hall moss earth');soil.use_nodes=True
nodes,links=soil.node_tree.nodes,soil.node_tree.links
noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=19
ramp=nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].color=(.05,.067,.022,1)
ramp.color_ramp.elements[1].color=(.16,.18,.064,1)
links.new(noise.outputs['Fac'],ramp.inputs[0])
links.new(ramp.outputs[0],nodes['Principled BSDF'].inputs['Base Color'])
# A single upward-facing surface avoids self-intersecting bevels on a thin box.
bpy.ops.mesh.primitive_plane_add(size=1,location=(-12,127.5,1.63))
ground=bpy.context.object;ground.name='Hall planted floor'
ground.scale=(29.8,26.6,1);ground.data.materials.append(soil);floor.append(ground)

# Low broken masonry and plants occupy the shoulders, leaving the central aisle
# and west reserved game location open. No tall decorative walking obstacles.
for i in range(72):
    x=-12+rng.choice((-1,1))*rng.uniform(8.3,13.7)
    z=rng.uniform(-139,-117)
    if -25<x<-21 and -125<z<-121:continue
    src=kit['Author_Slab_'+str(1+i%6)]
    obj=bpy.data.objects.new('Hall collapsed stone',src.data.copy());bpy.context.collection.objects.link(obj)
    obj.location=(x,-z,1.56);obj.scale=(rng.uniform(.3,.8),rng.uniform(.3,.8),rng.uniform(.8,1.5))
    obj.rotation_euler.z=rng.random()*math.tau
    obj.data.materials.clear();obj.data.materials.append(mats[2]);floor.append(obj)
for i in range(70):
    side=rng.choice((-1,1));x=-12+side*rng.uniform(6.5,14);z=rng.uniform(-139,-117)
    if -25<x<-21 and -125<z<-121:continue
    plants.append(leaf_crown('Hall fernlike broadleaf',(x,-z,1.85),(.85,.7,.5),93000+i,70,.42))
# Ivy on rear wall faces and tall sidewalls; rotate leaves to cling to the side faces.
for i in range(26):
    side=-1 if i<13 else 1
    z=-116-(i%13)*1.82
    top=rng.uniform(9.5,14);length=rng.uniform(3.5,7.5)
    ivy=ivy_ribbon('Wall ivy',0,0,top,length,93100+i)
    ivy.rotation_euler.z=math.pi/2
    ivy.location=( -26.25 if side<0 else 2.25, -z, 0)
    plants.append(ivy)
for i,x in enumerate((-25,-22,-18,-15.5,-8.4,-5,-1,2)):
    plants.append(ivy_ribbon('Portal hanging ivy',x,140.22,rng.uniform(8.5,11.5),rng.uniform(3,6),93200+i))
for i,(x,z) in enumerate([(-19,-119),(-5,-127),(-19,-135)]):
    plants.append(ivy_ribbon('Column climbing ivy',x,-z-.77,10,7.5,93300+i))
# Low creeping leaves break the paving into organic islands without obstructing
# the walking lane. Sparse branching trails echo REF8's encroaching floor growth.
for i in range(46):
    z=-117-i*.48
    x=-12+math.sin(i*.21)*3.2
    if i%7==0:continue
    plants.append(leaf_crown('Creeping floor ivy',(x,-z,1.77),(.7,.6,.065),93400+i,24,.30))
    if i%3==0:
        plants.append(leaf_crown('Creeping ivy offshoot',(x+1.4,-z+.3,1.77),(.8,.4,.06),93500+i,14,.25))

counts={'wallPieces':len(walls),'architecturalPieces':len(architecture),'floorPieces':len(floor),'plantGroups':len(plants)}
wall_obj=merge('ArchiveHall_Walls',walls)
arch_obj=merge('ArchiveHall_Arcades',architecture)
floor_obj=merge('ArchiveHall_Floor',floor)
foliage=merge('ArchiveHall_Foliage',plants);color_material(foliage)
for obj in (wall_obj,arch_obj,floor_obj):
    bm=bmesh.new();bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    if obj==floor_obj:
        # The earth is an open surface: explicitly retain its upward normal.
        for face in bm.faces:
            if face.calc_area()>20 and face.normal.z<0:face.normal_flip()
    bm.to_mesh(obj.data);bm.free()
bake([(wall_obj,2048),(arch_obj,2048),(floor_obj,2048)],OUT)
bpy.ops.object.select_all(action='DESELECT')
for obj in (wall_obj,arch_obj,floor_obj,foliage):obj.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/archive-hall.blend'),compress=True)
export=ROOT/'public/models/archive-hall.glb'
bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=True,export_image_format='JPEG',export_image_quality=92)
report={'stage':'PD03 archive hall',**counts,'bytes':export.stat().st_size,'atlases':[2048]*3}
(OUT/'archive-hall-report.json').write_text(json.dumps(report,indent=2)+'\n')
from world_art_context import export_context
export_context()
print(json.dumps(report),flush=True)
