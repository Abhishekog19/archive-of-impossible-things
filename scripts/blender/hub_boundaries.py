"""Finish hub enclosure, reverse arrival and the two forest bank noses.

Derived from world-blockout; never opens/saves the user's hub-blockout source.
Existing collision is retained. Only the two new bank noses add collision.
Vertex lighting and shared runtime stone grain avoid another texture atlas.
"""
import bpy, bmesh, math, random, sys, json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
from placed_art import merge, color_material
from boundary_layout import boundary_proxy

bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/source/world-blockout.blend'))
rng=random.Random(51005)
source=list(bpy.context.scene.objects)
ground_verts=[];ground_faces=[]
for obj in source:
    if obj.type!='MESH' or not obj.name.startswith(('Continuous terrain','Forest extension ground')):continue
    offset=len(ground_verts)
    ground_verts.extend(obj.matrix_world@v.co for v in obj.data.vertices)
    ground_faces.extend(tuple(offset+i for i in p.vertices) for p in obj.data.polygons)
ground=BVHTree.FromPolygons(ground_verts,ground_faces)
# Author in a separate scene so each primitive operation does not reevaluate
# the thousands of untouched world source objects. Their transforms stay intact.
author_scene=bpy.context.scene
bpy.context.window.scene=bpy.data.scenes.new('Hub boundary production')
def height(x,z):
    hit=ground.ray_cast(Vector((x,-z,30)),Vector((0,0,-1)))[0]
    return hit.z if hit else -.2

groups={'Stone':[],'Earth':[],'Wood':[],'Foliage':[]};colliders=[]
sun=Vector((-.4,-.3,.85)).normalized()
stone=(.36,.375,.29);earth=(.075,.106,.04);wood=(.11,.12,.058)

def mesh(name,points,faces,kind='Stone',tint=None,solid=False):
    data=bpy.data.meshes.new(name);data.from_pydata(points,[],faces);data.update()
    attr=data.color_attributes.new(name='BoundaryColour',type='BYTE_COLOR',domain='CORNER')
    for p in data.polygons:
        n=p.normal
        illumination=.54+.46*max(0,n.dot(sun))
        if kind=='Foliage':illumination=.72+.28*max(0,n.dot(sun))
        for li in p.loop_indices:
            v=data.vertices[data.loops[li].vertex_index].co
            mottling=.94+.06*math.sin(v.x*3.7+v.y*2.1)+.04*math.sin(v.z*7.1-v.y)
            base=tint or (stone if kind=='Stone' else wood if kind=='Wood' else earth)
            if kind=='Stone':
                # Moss occupies sheltered ledges and connected irregular patches.
                growth=(math.sin(v.x*.83+v.y*.67)+math.sin(v.z*1.9-v.x*.48))*.5
                moss=max(0,min(.74,(growth-.05)*.65+max(0,n.z)*.25))
                base=tuple(a*(1-moss)+b*moss for a,b in zip(base,(.09,.14,.037)))
            attr.data[li].color=tuple(c*illumination*mottling for c in base)+(1,)
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj)
    groups[kind].append(obj)
    if solid:
        copy=obj.copy();copy.data=obj.data.copy();bpy.context.collection.objects.link(copy);colliders.append(copy)
    return obj

def stone_block(centre,size,yaw=0,tint=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=centre)
    obj=bpy.context.object;obj.scale=size;obj.rotation_euler.z=yaw
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    bevel=obj.modifiers.new('Chipped arris','BEVEL');bevel.width=min(.055,min(size)*.07);bevel.segments=1
    bpy.context.view_layer.objects.active=obj;bpy.ops.object.modifier_apply(modifier=bevel.name)
    pts=[]
    for v in obj.data.vertices:
        p=obj.matrix_world@v.co
        p.x+=rng.uniform(-.017,.017);p.y+=rng.uniform(-.017,.017)
        pts.append(p)
    faces=[tuple(p.vertices) for p in obj.data.polygons]
    bpy.data.objects.remove(obj,do_unlink=True)
    return mesh('Weathered boundary masonry',pts,faces,tint=tint)

def branch(points,radii):
    pts=[];faces=[]
    for i,p in enumerate(points):
        p=Vector(p);a=Vector(points[max(0,i-1)]);b=Vector(points[min(len(points)-1,i+1)])
        t=(b-a).normalized();u=t.cross(Vector((0,0,1)))
        if u.length<.1:u=t.cross(Vector((1,0,0)))
        u.normalize();v=t.cross(u)
        for j in range(8):pts.append(p+radii[i]*(u*math.cos(j*math.tau/8)+v*math.sin(j*math.tau/8)))
    for i in range(len(points)-1):
        for j in range(8):
            a=i*8+j;b=i*8+(j+1)%8;faces.append((a,b,b+8,a+8))
    faces.extend([tuple(reversed(range(8))),tuple(range(len(pts)-8,len(pts)))])
    mesh('Tapered boundary wood',pts,faces,'Wood')

def crown(centre,radius,tint=(.075,.125,.032),leaves=45):
    # Closed irregular core plus folded edge leaves; no alpha overdraw or cards.
    leaves=max(12,leaves//2)
    bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=2 if max(radius)>1.8 else 1,radius=1)
    bm.verts.ensure_lookup_table();bm.verts.index_update();c=Vector(centre);r=Vector(radius)
    pts=[c+Vector(tuple(v.co[k]*r[k]*(.78+.18*math.sin(v.co.x*7+v.co.y*4)) for k in range(3))) for v in bm.verts]
    faces=[tuple(v.index for v in f.verts) for f in bm.faces];bm.free()
    for i in range(leaves):
        h=1-2*(i+.5)/leaves;a=i*2.39996
        n=Vector((math.sqrt(1-h*h)*math.cos(a),math.sqrt(1-h*h)*math.sin(a),h))
        p=c+Vector(tuple(n[k]*r[k] for k in range(3)))
        u=n.cross(Vector((0,0,1))).normalized();v=n.cross(u)
        size=rng.uniform(.18,.36)*min(1.8,max(radius)*.7)
        base=len(pts);pts.extend([p-u*size,p-v*size*.65,p+u*size,p+v*size*.65,p+n*size*.18])
        faces.extend([(base+j,base+(j+1)%4,base+4) for j in range(4)])
    mesh('Boundary leafy volume',pts,faces,'Foliage',tint)

def rough_skin(obj,only_bank=False):
    data=obj.data.copy();bm=bmesh.new();bm.from_mesh(data)
    if only_bank:
        outside=[f for f in bm.faces if -(obj.matrix_world@f.calc_center_median()).y<-56]
        bmesh.ops.delete(bm,geom=outside,context='FACES')
    bmesh.ops.subdivide_edges(bm,edges=list(bm.edges),cuts=2,use_grid_fill=True)
    bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(data);bm.free();data.update()
    points=[]
    for v in data.vertices:
        p=obj.matrix_world@v.co;n=(obj.matrix_world.to_3x3()@v.normal).normalized()
        wave=.035+.19*math.sin(p.x*1.47+p.y*.51)*math.sin(p.z*2.15+p.y*.79)
        if only_bank:wave*=max(0,min(1,(56-p.y)/4))
        points.append(p+n*wave)
    result=mesh('Continuous boundary outcrop',points,[tuple(p.vertices) for p in data.polygons])
    if only_bank:
        colors=result.data.color_attributes['BoundaryColour']
        for loop in result.data.loops:
            p=result.data.vertices[loop.vertex_index].co
            blend=max(0,min(1,(p.y-50)/6))
            field=.72+.13*math.sin(p.x*.73+p.y*.28)+.12*math.sin(p.y*1.17-p.x*.36)
            old=colors.data[loop.index].color
            colors.data[loop.index].color=tuple(old[k]*(1-blend)+(.033,.046,.012)[k]*field*blend for k in range(3))+(1,)
    bpy.data.meshes.remove(data)
    return result

def outcrop(centre,size):
    # Squat, asymmetric strata interrupt the broad ridge without cube outlines.
    points=[];faces=[];c=Vector(centre)
    offsets=[rng.uniform(.82,1.13) for _ in range(7)]
    for layer,(scale,z) in enumerate(((.85,-.3),(1,0),(.73,.6),(.42,.84))):
        for j in range(7):
            a=j*math.tau/7
            points.append(c+Vector((math.cos(a)*size[0]*scale*offsets[j]+layer*.08,
                                   math.sin(a)*size[1]*scale*offsets[j],z*size[2]+rng.uniform(-.08,.08))))
    for i in range(3):
        for j in range(7):
            a=i*7+j;b=i*7+(j+1)%7;faces.append((a,b,b+7,a+7))
    faces.append(tuple(range(21,28)))
    mesh('Split ledge strata',points,faces,tint=(.26,.29,.20))

def boundary_tree(x,z,y,h,tint):
    lean=rng.uniform(-1.2,1.2)
    branch([(x,-z,y),(x+lean*.4,-z+.2,y+h*.45),(x+lean,-z+.3,y+h*.9)],[.6,.35,.09])
    for j in range(3):
        a=j*2.4+x*.83;spread=rng.uniform(1.8,3.5)
        end=(x+math.cos(a)*spread,-z+math.sin(a)*spread,y+h*(.65+j*.14))
        branch([(x+lean*.4,-z+.2,y+h*.5),end],[.23,.04])
        crown(end,(rng.uniform(2.5,3.5),rng.uniform(2.3,3.3),rng.uniform(1.7,2.8)),tint,leaves=48)
    crown((x,-z,y+1.1),(2.9,2.7,1.5),leaves=30)

replaced=[];islands=[];ridges=[];banks=[]
for obj in source:
    if obj.type!='MESH' or obj.name.startswith('Collision'):continue
    c=sum((obj.matrix_world@Vector(v) for v in obj.bound_box),Vector())/8
    x,z=c.x,-c.y
    if obj.name.startswith('Continuous forest bank'):
        rough_skin(obj,True);banks.append(obj);continue
    if not boundary_proxy(obj.name,x,z):continue
    replaced.append(obj.name)
    if obj.name.startswith('Woodland rock ridge'):
        rough_skin(obj);ridges.append(obj)
    elif obj.name.startswith('Island understory'):
        islands.append((tuple(c),tuple(obj.dimensions*.5)))
    elif obj.name.startswith(('Arrival slope','Overgrown path mouth','Overgrown branch roots')):continue
    else:
        lo=Vector(tuple(min(v.co[k] for v in obj.data.vertices) for k in range(3)))
        hi=Vector(tuple(max(v.co[k] for v in obj.data.vertices) for k in range(3)))
        dims=hi-lo;rows=max(1,math.ceil(dims.z/.52));cols=max(1,math.ceil(dims.x/1.15))
        for row in range(rows):
            width=dims.x/cols
            cuts=[lo.x]+[lo.x+(col+(.5 if row%2 else 1))*width for col in range(cols)]+[hi.x]
            cuts=sorted(set(round(v,6) for v in cuts))
            for a,b in zip(cuts,cuts[1:]):
                if b-a<.01:continue
                centre=Vector(((a+b)/2,(lo.y+hi.y)/2,lo.z+(row+.5)*dims.z/rows))
                tint=tuple(v*rng.uniform(.9,1.04) for v in stone)
                stone_block(obj.matrix_world@centre,(b-a+.012,dims.y+.025,dims.z/rows+.012),obj.rotation_euler.z,tint)
        for side in (-1,1):
            crown((c.x,c.y+side*(dims.y/2+.1),height(c.x,-c.y)+.2),(.5,.4,.32),leaves=24)

# Arrival is a broad stone path that dissolves into planted bedrock at its end.
for row in range(18):
    z=12.7+row*.86
    for col in range(6):
        x=(col-2.5)*1.12+.11*math.sin(row*1.5)
        y=-max(0,z-12)*.045
        slab=stone_block((x,-z,y-.10),(1.09,.85,.21),rng.uniform(-.026,.026))
        # Follow the original 4.5% slope across each slab, including shared edges.
        for v in slab.data.vertices:v.co.z+=.045*(v.co.y+z)
    if row%2==0:
        for side in (-1,1):crown((side*(3.6+rng.random()*.3),-z,height(side*3.8,z)+.2),(.7,.8,.36),leaves=24)

# Replace the blocked northern spur with a seated root/stone junction.
for row in range(6):
    z=-12.7-row*.62
    for col in range(4):stone_block(((col-1.5)*.96,-z,-.17),(.94,.6,.18))
for j in range(3):
    branch([(-2.25,17+.2*j,.2),( -1,17+.2*j,.5+j*.28),(1,17+.2*j,.6+j*.2),(2.3,17+.2*j,.08)],
           [.12,.35,.33,.04])

# Dress ledges with roots and low planting, seated on the actual ridge surface.
rv=[];rf=[]
for obj in ridges:
    off=len(rv);rv.extend(obj.matrix_world@v.co for v in obj.data.vertices)
    rf.extend(tuple(off+i for i in p.vertices) for p in obj.data.polygons)
ridge_bvh=BVHTree.FromPolygons(rv,rf)
for obj in ridges:
    bounds=[obj.matrix_world@Vector(v) for v in obj.bound_box]
    x=min(p.x for p in bounds)+1
    while x<max(p.x for p in bounds):
        y=min(p.y for p in bounds)+.7+rng.random()
        while y<max(p.y for p in bounds):
            hit,normal,_,_=ridge_bvh.ray_cast(Vector((x,y,25)),Vector((0,0,-1)))
            if hit and normal.z>.25:
                outcrop(hit-Vector((0,0,.22)),(rng.uniform(1.8,3),rng.uniform(.8,1.5),rng.uniform(.4,.85)))
                if rng.random()<.75:
                    crown(hit+Vector((.25,.2,.45)),(rng.uniform(.65,1.15),.8,.55),(.1,.155,.045),leaves=24)
            y+=2.8+rng.random()
        x+=3+rng.random()

# Round both abrupt forest-bank starts into the hub terrain. The six profile
# rings meet the existing bank at z=-40. Only these noses add physical surfaces.
for side in (-1,1):
    inner=-31 if side<0 else 7;points=[]
    for i in range(6):
        t=i/5;z=-36-4*t;s=t*t*(3-2*t)
        for offset,target in [(0,1.55),(.5,5.75),(5,7.25),(9,.4)]:
            x=inner+side*offset
            base=height(x,z)
            points.append((x,-z,base*(1-s)+target*s+.018))
    faces=[]
    for i in range(5):
        for j in range(3):
            a=i*4+j;faces.append((a,a+4,a+5,a+1))
    if side>0:faces=[tuple(reversed(f)) for f in faces]
    nose=mesh('Rounded forest bank nose',points,faces,'Stone',solid=True)
    for j in range(5):
        x=inner+side*(.8+j*.95);z=-39.2
        # Sample the cap itself for rooted vegetation rather than hide its join.
        cap=BVHTree.FromPolygons(points,faces)
        hit=cap.ray_cast(Vector((x,-z,20)),Vector((0,0,-1)))[0]
        if hit:crown(hit+Vector((0,0,.25)),(.8,.95,.55),leaves=25)
    for j in range(5):
        z=-40-j*2.8
        crest=5.75+max(0,-z-40)*.018
        branch([(inner+side*1.4,-z,crest+.4),(inner+side*.54,-z+.25,crest),
                (inner+side*.28,-z+.4,crest*.5),(inner-side*.03,-z+.6,1.48)], [.28,.24,.14,.015])
        crown((inner+side*1.3,-z,crest+.5),(1.3,.9,.6),leaves=24)
    for j in range(8):
        x=inner+side*(12+(j%2)*4);z=-35-j*3
        boundary_tree(x,z,height(x,z),rng.uniform(10,16),(.1+(j%2)*.04,.16+(j%2)*.04,.065))

for centre,radius in islands:
    for j in range(3):
        p=Vector(centre)+Vector((math.cos(j*2.4)*radius[0]*.4,math.sin(j*2.4)*radius[1]*.4,-.2))
        crown(p,tuple(v*.7 for v in radius),leaves=35)

# Layered reverse-arrival woodland behind the closed boundary. Trees are outside
# the walking area; lower growth ties their trunks into the rock ridge silhouette.
for i in range(13):
    x=-30+i*5+rng.uniform(-.8,.8);z=36+(i%3)*4.5;y=.3
    h=rng.uniform(10,15)
    boundary_tree(x,z,y,h,[(.085,.14,.055),(.13,.19,.08),(.18,.23,.11)][i%3])

for obj in source:bpy.data.objects.remove(obj,do_unlink=True)
bpy.data.scenes.remove(author_scene)
exports=[]
for kind,objects in groups.items():
    if not objects:continue
    obj=merge('HubBoundary_'+kind,objects);color_material(obj);exports.append(obj)
collision=merge('HubBoundary_Collision',colliders);collision.data.materials.clear();exports.append(collision)
bpy.ops.object.select_all(action='DESELECT')
for obj in exports:obj.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/hub-boundaries.blend'),compress=True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'public/models/hub-boundaries.glb'),export_format='GLB',use_selection=True,
                         export_vertex_color='NAME',export_vertex_color_name='BoundaryColour',export_all_vertex_colors=False)
report={'replaced':replaced,'bankNoses':2,'triangles':sum(len(p.vertices)-2 for o in exports for p in o.data.polygons),
        'collisionTriangles':sum(len(p.vertices)-2 for p in collision.data.polygons),'newAtlases':0}
(ROOT/'.artifacts/blender/hub-boundaries-report.json').write_text(json.dumps(report,indent=2)+'\n')
from world_art_context import export_context
export_context()
print(json.dumps(report),flush=True)
