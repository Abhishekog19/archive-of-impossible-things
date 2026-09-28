"""PD07 hub perimeter and distant ruined bell tower; existing walk limits retained."""
import bpy
import math
import random
import json
import sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, str(Path(__file__).parent))
from placed_art import merge, color_material

ROOT = Path(__file__).resolve().parents[2]
rng = random.Random(707)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/source/world-blockout.blend'))
verts, faces = [], []
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH' or not obj.name.startswith('Continuous terrain'): continue
    offset = len(verts)
    verts.extend(obj.matrix_world @ v.co for v in obj.data.vertices)
    faces.extend(tuple(offset + i for i in p.vertices) for p in obj.data.polygons)
ground = BVHTree.FromPolygons(verts, faces)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
parts = []

def block(name, x, y, z, width, height, depth, yaw=0, moss=False):
    # Eight uneven corners retain broad stone planes and chipped silhouettes.
    points=[]
    for h in (-height/2, height/2):
        for u,v in [(-width/2,-depth/2),(width/2,-depth/2),(width/2,depth/2),(-width/2,depth/2)]:
            inset=rng.uniform(-.05,.05)
            points.append((x+u*math.cos(yaw)-v*math.sin(yaw)+inset,
                           -(z+u*math.sin(yaw)+v*math.cos(yaw)), y+h+inset))
    data=bpy.data.meshes.new(name);data.from_pydata(points,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);data.update()
    colours=data.color_attributes.new(name='FinishColour',type='BYTE_COLOR',domain='CORNER')
    for poly in data.polygons:
        light=.63+.25*max(0,poly.normal.z)+.12*max(0,poly.normal.x)
        shade=light*rng.uniform(.88,1.06)
        rgb=(.115,.155,.052) if moss else (.38,.385,.29)
        for loop in poly.loop_indices:colours.data[loop].color=tuple(c*shade for c in rgb)+(1,)
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj);parts.append(obj)

# Same landmark footprint and height as the existing source; staggered courses,
# recessed openings, buttresses and a broken belfry replace its plain shaft.
for side in range(4):
    a=side*math.pi/2
    for row in range(22):
        for col in range(3):
            if col==1 and row in (7,8,14,15): continue
            along=(col-1)*1.08
            x=24+1.35*math.cos(a)-along*math.sin(a)
            z=-74+1.35*math.sin(a)+along*math.cos(a)
            block('Tower worn course',x,1.5+row*1.05,z,1.06,1.02,.55,a+math.pi/2)
    x,z=24+1.63*math.cos(a+.65),-74+1.63*math.sin(a+.65)
    block('Tower buttress',x,11.8,z,.6,22.2,.6,a)
    block('Tower belfry pier',x,26.4,z,.75,5,.75,a)
    # Broken arch-shaped stepped lintels leave clear sky gaps above the shaft.
    for j in range(5):
        offset=(j-2)*.65
        block('Tower belfry arch',24+1.5*math.cos(a)-offset*math.sin(a),
              28.15+.7*math.sqrt(max(0,1-(offset/1.5)**2)),
              -74+1.5*math.sin(a)+offset*math.cos(a),.68,.6,.8,a+math.pi/2)
for y in (6.8,17.4,24.5):
    for side in range(4):
        a=side*math.pi/2
        block('Tower weathered belt',24+1.65*math.cos(a),y,-74+1.65*math.sin(a),3.8,.35,.45,a+math.pi/2)
for i in range(22):
    y=3+i*.82
    block('Tower trailing growth',25.73,y,-74.6+.18*math.sin(i),.09+rng.random()*.09,.55,.09, moss=True)

# Only the existing outer ridge receives masonry; the plaza, paths, game spaces
# and camera corridors remain untouched. Terrain raycasts seat each remnant.
for side,z in [(-1,-15),(-1,0),(-1,17),(1,-12),(1,5),(1,20)]:
    x=side*30
    hit=ground.ray_cast(Vector((x,-z,40)),Vector((0,0,-1)))[0]
    if hit is None: continue
    floor=hit.z
    height=3.1+rng.random()*2.3
    for level in range(int(height/.7)):
        block('Perimeter broken pier',x,floor+.35+level*.7,z,1.15,.68,1.3)
    for j in range(4):
        block('Perimeter low retaining ruin',x,floor+.4,z+(j-1.5)*1.45,.9,.75,1.4)
    block('Perimeter moss cap',x,floor+height-.35,z,1.1,.12,1.15,moss=True)

finish=merge('WorldFinish_Limestone',parts);color_material(finish)
bpy.ops.object.select_all(action='DESELECT');finish.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/world-finish.blend'),compress=True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'public/models/world-finish.glb'),export_format='GLB',use_selection=True)
report={'stage':'PD07 hub perimeter and tower','parts':len(parts),'triangles':len(finish.data.polygons)*2}
from world_art_context import export_context
export_context()
print(json.dumps(report),flush=True)
