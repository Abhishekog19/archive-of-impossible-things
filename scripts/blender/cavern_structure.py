"""PD04 geometry: fractured cavern, open oculus, walkable shores and descent.

Vertex shading is a structural preview; PD05/06 own textures, water and lighting.
No full-cavern low-density colour atlas is introduced by this pass.
"""
import bpy
import math
import random
import json
import sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
from placed_art import merge, color_material

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'.artifacts/blender'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
rng=random.Random(9284)
visuals=[]
solids=[]


def mesh(name, points, faces, solid=False, shore=False):
    data=bpy.data.meshes.new(name)
    data.from_pydata([(x,-z,y) for x,y,z in points],[],faces)
    data.update()
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj)
    colors=data.color_attributes.new(name='RockColor',type='BYTE_COLOR',domain='CORNER')
    for poly in data.polygons:
        centre=poly.center
        # Broad structural value groups make planes legible without tiny noise.
        variation=rng.uniform(.9,1.1)
        facing=.75+.25*abs(poly.normal.x)+.2*max(0,poly.normal.z)
        height=max(0,min(1,(centre.z+8)/27))
        shade=(.68+.5*height)*facing*variation
        base=(.13,.16,.19) if shore else (.075,.099,.128)
        # Limestone at the hall end settles gradually into the cavern palette.
        transition=max(0,min(1,(174-centre.y)/33)) if 'Descent' in name else 0
        base=tuple(c*(1-transition)+v*transition for c,v in zip(base,(.24,.245,.19)))
        for loop in poly.loop_indices:colors.data[loop].color=tuple(c*shade for c in base)+(1,)
    visuals.append(obj)
    if solid:solids.append(obj)
    return obj


cx,cz=-12,-195
N=64
angles=[i*math.tau/N for i in range(N)]
levels=[(-9,25.5),(-3,25),(3,24),(9,21),(14,14),(18,4)]
points=[]
for k,(h,r) in enumerate(levels):
    for i,a in enumerate(angles):
        wave=.65*math.sin(a*7+.5)+.35*math.sin(a*13)
        rad=r+wave*(.35 if k==5 else 1)+rng.uniform(-.65,.65)
        shift=-10*(k/5)**2
        # Elongated, irregular fissure at the crown rather than a circular skylight.
        sx,sz=(.7,1.5) if k==5 else (1,1)
        y=h+(1.6*math.sin(a*5+k*.8) if k not in (0,) else 0)
        angle=a+.035*math.sin(i*1.8+k*1.5)
        points.append((cx+sx*rad*math.cos(angle),y,cz+shift+sz*rad*math.sin(angle)))
faces=[]
for k in range(len(levels)-1):
    for i in range(N):
        a=angles[i]+math.pi/N
        # The passage joins only the low northern wall; the roof stays continuous.
        if k<2 and abs(a-math.pi/2)<.16:continue
        j=(i+1)%N
        faces.extend([(k*N+i,(k+1)*N+i,(k+1)*N+j),(k*N+i,(k+1)*N+j,k*N+j)])
mesh('Cavern continuous fractured shell',points,faces,True)

# Long irregular escarpments follow the chamber walls. Their changing profiles
# create tall ledges and deep joints, avoiding a repeated brick/block pattern.
for i in range(42):
    a=i*math.tau/42+rng.uniform(-.04,.04)
    if abs(a-math.pi/2)<.24:continue
    radius=rng.uniform(23.5,25)
    width=rng.uniform(.8,1.8)
    height=rng.uniform(7,18)
    pts=[]
    for level,(h,dr,w) in enumerate([(-8,.5,1),(-4,-.2,.95),(height*.45-8,-.7,.8),(height-8,1,.45)]):
        for side in (-1,1):
            rr=radius+dr+rng.uniform(-.22,.22)
            tangent=side*width*w
            pts.append((cx+rr*math.cos(a)-tangent*math.sin(a),h,cz+rr*math.sin(a)+tangent*math.cos(a)))
    mesh('Vertical jointed rock face',pts,[(0,1,3,2),(2,3,5,4),(4,5,7,6)],True)

# Staggered fracture plates interrupt the chamber's radial construction. Each
# exposes a broad face and chipped side planes, with no common horizontal course.
for band in range(3):
    for i in range(24):
        a=i*math.tau/24+rng.uniform(-.09,.09)
        if abs(a-math.pi/2)<.28:continue
        h=(-4,3,10)[band]+rng.uniform(-1.4,1.4)
        radius=(24.2,23.1,18.2)[band]+rng.uniform(-.5,.5)
        zshift=(0,-1.4,-5)[band]
        width=rng.uniform(1.2,3.1);height=rng.uniform(2.2,5.5)
        # Local U runs around the wall, V rises and D projects into the chamber.
        shape=[(-width,-height*.5,0),(width*.7,-height*.5,.35),
               (width,height*.2,.8),(width*.35,height*.55,.3),
               (-width*.8,height*.42,.1)]
        front=[]
        for u,v,d in shape:
            r=radius-d
            front.append((cx+r*math.cos(a)-u*math.sin(a),h+v,cz+zshift+r*math.sin(a)+u*math.cos(a)))
        back=[(x+math.cos(a)*1.1,y,z+math.sin(a)*1.1) for x,y,z in front]
        mesh('Overlapping rock fracture plate',front+back,[(0,1,2,3,4)]+
             [(j,j+5,(j+1)%5+5,(j+1)%5) for j in range(5)],True)

# Roof splinters reinforce the asymmetric opening, staying out of the sky hole.
for i in range(18):
    a=i*math.tau/18
    x=cx+math.cos(a)*4.1;z=cz-10+math.sin(a)*7.2
    w=rng.uniform(.6,1.25)
    mesh('Oculus fractured tooth',[(x-w,18,z),(x+w,18,z),
         (x+.2,15+rng.uniform(0,2),z+.5),(x,19,z+1.4)],
         [(0,2,1),(0,1,3),(1,2,3),(2,0,3)],True)

def shore_radius(a):return 15.5+1.2*math.sin(3*a)+.7*math.cos(5*a)

# The inner contour follows the existing pool, with broad horizontal bedrock
# plates. A continuous base under the fissures retains the resident walking level.
for i in range(N):
    a,b=angles[i],(i+1)*math.tau/N
    ra,rb=shore_radius(a),shore_radius(b)
    mesh('Shore continuous ground',[(cx+r*math.cos(t),-7.51,cz+r*math.sin(t))
         for r,t in ((ra,a),(27,a),(27,b),(rb,b))],[(0,1,2,3)],shore=True)
    mesh('Shore fracture lip',[(cx+r*math.cos(t),h,cz+r*math.sin(t))
         for r,t,h in ((ra,a,-7.49),(rb,b,-7.49),(rb+.2,b,-9.1),(ra+.2,a,-9.1))],
         [(0,1,2,3)],shore=True)
    for band in range(3):
        step=math.tau/N
        aa=a+step*(band*.37+.2*math.sin(i*1.3))+.0015
        bb=b+step*(band*.37+.2*math.sin((i+1)*1.3))-.0015
        def edge(k,t):
            return shore_radius(t)+k*3.2+(0 if k==0 else .55*math.sin(t*11+k*1.7)+.3*math.cos(t*17-k))
        inner_a=edge(band,aa)+.025;inner_b=edge(band,bb)+.025
        outer_a=edge(band+1,aa)-.025;outer_b=edge(band+1,bb)-.025
        mid=(aa+bb)/2
        # Staggered fracture boundaries avoid continuous radial tile joints.
        coords=[(inner_a,aa),(outer_a,aa),(edge(band+1,mid)-.06,mid+(bb-aa)*.1),
                (outer_b,bb),(inner_b,bb),(edge(band,mid)+.08,mid-(bb-aa)*.1)]
        top=[(cx+r*math.cos(t),-7.47+rng.uniform(-.012,.012),cz+r*math.sin(t)) for r,t in coords]
        pts=top+[(x,-7.64,z) for x,y,z in top]
        mesh('Broad shoreline bedrock',pts,[(0,1,2,3,4,5)]+[(j,(j+1)%6,(j+1)%6+6,j+6) for j in range(6)],shore=True)

# Large talus masses stay at the outer wall, away from the navigable shore loop.
for i in range(30):
    a=rng.random()*math.tau
    if abs(a-math.pi/2)<.25:continue
    r=rng.uniform(23,24)
    x,z=cx+r*math.cos(a),cz+r*math.sin(a)
    w=rng.uniform(.8,1.7);h=rng.uniform(.65,2.3)
    mesh('Wall foot fallen rock',[(x-w,-7.5,z-w),(x+w,-7.5,z-w),(x+w,-7.5,z+w),
         (x-w,-7.5,z+w),(x-w*.6,-7.5+h,z-.3),(x+w*.5,-7.5+h*.8,z+.4)],
         [(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4),(4,5,2)],True,True)

# One continuous passage skin, with staggered fractures along the slope. Its
# floor remains the resident ramp; the 5m lane is not narrowed by decoration.
pts=[]
for i in range(18):
    z=-141-i*33/17;y=1.65-i*9.15/17
    for j,(x,h) in enumerate([(-2.85,-.3),(-3.15,3.6),(-1.8,6.2),(0,6.8),(1.9,6.4),(3.2,3.5),(2.85,-.3)]):
        offset=0 if i in (0,17) else rng.uniform(-.13,.13)
        hh=h+(2 if i==0 and h>6 else 0)+offset
        pts.append((-12+x+offset,y+hh,z))
faces=[]
for i in range(17):
    for j in range(6):
        a=i*7+j;b=a+7
        faces.extend([(a,b,a+1),(a+1,b,b+1)])
mesh('Descent fractured passage',pts,faces,True)
for i in range(22):
    za=-141-i*1.5;zb=max(-174,za-1.48)
    ya=1.65+ (za+141)*9.15/33+.02;yb=1.65+(zb+141)*9.15/33+.02
    for side in (-1,1):
        lo,hi=(-14.48,-12.02) if side<0 else (-11.98,-9.52)
        mesh('Descent worn ledge',[(lo,ya,za),(hi,ya,za),(hi,yb,zb),(lo,yb,zb)],[(0,1,2,3)],shore=True)

visual_count=len(visuals)
# The new chamber/passage skin supplies matching physical boundaries. Flat shore
# and ramp collision stay resident; the pool still has no walking floor.
copies=[]
for o in solids:
    c=o.copy();c.data=o.data.copy();bpy.context.collection.objects.link(c);copies.append(c)
collision=merge('CavernStructure_Collision',copies)
collision.data.materials.clear()
rock=merge('CavernStructure_Rock',visuals);color_material(rock)
for obj in (collision,rock):obj.data.validate(clean_customdata=True);obj.data.update()
bpy.ops.object.select_all(action='DESELECT')
for obj in (rock,collision):obj.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/cavern-structure.blend'),compress=True)
export=ROOT/'public/models/cavern-structure.glb'
bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=True)
report={'stage':'PD04 cavern structure','structuralParts':visual_count,'solidParts':len(solids),
        'bytes':export.stat().st_size,'visualTriangles':sum(len(p.vertices)-2 for p in rock.data.polygons),
        'collisionTriangles':sum(len(p.vertices)-2 for p in collision.data.polygons),
        'materialStatus':'vertex-colour structural preview; PD05/06 texture, water and lighting passes pending'}
(OUT/'cavern-structure-report.json').write_text(json.dumps(report,indent=2)+'\n')
from world_art_context import export_context
export_context()
print(json.dumps(report),flush=True)
