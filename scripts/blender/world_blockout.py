"""Connected layout study. Generates separate assets; never opens the user's hub source.

Browser coordinates are X/Y/Z. This reuses the deterministic hub generator into
an editable scene in memory, then extends it before a single save/merged export.
"""
import bpy
import bmesh
import math
import random
import runpy
import json
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
base = runpy.run_path(str(ROOT / 'scripts/blender/hub_blockout.py'), init_globals={'WORLD_LAYOUT': True})
SOURCE = ROOT / 'art/source/world-blockout.blend'
EXPORT = ROOT / 'public/models/world-blockout.glb'
random.seed(912)
stone = bpy.data.materials['Limestone']
earth = bpy.data.materials['Moss earth']
bark = bpy.data.materials['Trunks']
edge = bpy.data.materials['Stone shade']
collision = bpy.data.materials['Collision only']
leaves = [bpy.data.materials['Canopy '+str(i)] for i in range(3)]

def pos(p): return (p[0], -p[2], p[1])
def finish(o, name, mat):
    o.name = name
    o.data.materials.append(mat)
    return o
def proxy(o):
    c = o.copy()
    c.data = o.data.copy()
    c.data.materials.clear()
    c.data.materials.append(collision)
    c.name = 'Collision'
    bpy.context.collection.objects.link(c)
    return c
def box(name, at, size, mat, solid=False):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos(at))
    o = bpy.context.object
    o.scale = (size[0], size[2], size[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    finish(o, name, mat)
    if solid: proxy(o)
    return o
def mesh(name, points, faces, mat, solid=False):
    data = bpy.data.meshes.new(name)
    data.from_pydata([pos(p) for p in points], [], faces)
    data.update()
    o = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(o)
    finish(o, name, mat)
    if solid: proxy(o)
    return o
def mass(name, at, scale, mat):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1, location=pos(at))
    o = bpy.context.object
    o.scale = (scale[0], scale[2], scale[1])
    for v in o.data.vertices: v.co *= random.uniform(.85, 1.15)
    return finish(o, name, mat)
def branch(name, a, b, radius, mat, solid=False):
    av, bv = Vector(pos(a)), Vector(pos(b))
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=radius, radius2=radius*.65,
                                    depth=(bv-av).length, location=(av+bv)/2)
    o = bpy.context.object
    o.rotation_euler = (bv-av).to_track_quat('Z', 'Y').to_euler()
    finish(o, name, mat)
    if solid: proxy(o)
    return o
def road(points, width, name='Connected paving'):
    verts=[]
    for i,p in enumerate(points):
        a,b=points[max(0,i-1)],points[min(len(points)-1,i+1)]
        dx,dz=b[0]-a[0],b[2]-a[2]
        length=math.hypot(dx,dz)
        verts.extend([(p[0]-dz/length*width/2,p[1],p[2]+dx/length*width/2),
                      (p[0]+dz/length*width/2,p[1],p[2]-dx/length*width/2)])
    return mesh(name,verts,[(2*i,2*i+2,2*i+3,2*i+1) for i in range(len(points)-1)],stone,True)
def root_curve(points, radius, name='Wrapping facade root'):
    """Continuous tapered rings avoid the seams of overlapping capped cones."""
    vertices=[];sides=8
    for i,p in enumerate(points):
        tangent=(Vector(points[min(i+1,len(points)-1)])-
                 Vector(points[max(0,i-1)])).normalized()
        axis=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((1,0,0))
        normal=tangent.cross(axis).normalized();binormal=tangent.cross(normal)
        r=radius*(1-.65*i/(len(points)-1))
        for j in range(sides):
            angle=j*math.tau/sides
            vertices.append(tuple(Vector(p)+r*(normal*math.cos(angle)+binormal*math.sin(angle))))
    faces=[tuple(reversed(range(sides))),tuple(range(len(vertices)-sides,len(vertices)))]
    for i in range(len(points)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides
            faces.append((a,b,b+sides,a+sides))
    return mesh(name,vertices,faces,bark,True)
def forest_x(z):
    t=max(0,min(1,(-z-42)/52))
    return -12+3.8*math.sin(t*math.tau)*math.sin(t*math.pi)
def terrain_bank(side):
    """Continuous steep inner bank: visible terrain supplies the boundary proxy."""
    points=[]
    for i,z in enumerate(range(-40,-117,-4)):
        # Narrow into the archive walls, with space around the west game clearing.
        taper=max(0,min(1,(-z-96)/16))
        inner=(-31 if side<0 else 7)-side*4*taper
        inner+=side*(.65*math.sin(i*1.7))
        crest=5.4+.8*math.sin(i*.9)+.35*math.cos(i*2.1)
        points.extend([(inner,1.55,z),(inner+side*.5,crest,z),
                       (inner+side*5,crest+1.5,z),(inner+side*9,.4,z)])
    faces=[]
    for i in range(len(points)//4-1):
        for j in range(3):
            a=4*i+j;b=a+4
            faces.extend([(a,b,a+1),(b,b+1,a+1)])
    if side>0: faces=[tuple(reversed(f)) for f in faces]
    mesh('Continuous forest bank',points,faces,earth,True)
def arch(x,y,z,width=5,height=7,depth=1.2):
    r=width/2
    spring=y+height-r
    for side in (-1,1):
        box('Archive arch pier',(x+side*(r+.45),(y+spring)/2,z),(.9,spring-y,depth),stone,True)
    for i in range(10):
        a,b=i*math.pi/10,(i+1)*math.pi/10
        pts=[(x+rad*math.cos(t),spring+rad*math.sin(t),zz)
             for zz in (z-depth/2,z+depth/2) for rad,t in ((r,a),(r,b),(r+.9,b),(r+.9,a))]
        mesh('Archive arch voussoir',pts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],stone,True)

# Open only the north continuation. Existing hub generator/source is untouched.
for o in list(bpy.context.scene.objects):
    if o.type != 'MESH': continue
    bounds=[o.matrix_world @ Vector(v) for v in o.bound_box]
    xs=[v.x for v in bounds]; zs=[-v.y for v in bounds]
    cx=(min(xs)+max(xs))/2; cz=(min(zs)+max(zs))/2
    north_ridge = max(xs)-min(xs)>55 and -55<cz<-43 and max(zs)-min(zs)<15
    end_block = -16<cx<-8 and -46<cz<-42 and max(xs)-min(xs)<8
    corridor_tree = -36<cx<8 and cz<-42 and o.name.startswith(('Tree trunk','Forest crown','Woodland shoulder','Distant forest'))
    if north_ridge or end_block or corridor_tree:
        bpy.data.objects.remove(o,do_unlink=True)
    elif max(xs)-min(xs)>110 and max(zs)-min(zs)>130:
        # Cut the old terrain beneath the extension, including its collision copy.
        bm=bmesh.new();bm.from_mesh(o.data)
        remove=[v for v in bm.verts if -34<v.co.x<10 and -v.co.y<-42]
        bmesh.ops.delete(bm,geom=remove,context='VERTS')
        bm.to_mesh(o.data);bm.free()

# REF5/6: the existing approach flows into a second, more enclosed forest section.
box('Forest extension ground',(-12,.90,-76),(42,1.4,70),earth,True)
road([(forest_x(z),1.65,z) for z in range(-42,-92,-2)],5.6)
for z in range(-48,-95,-7):
    for side in (-1,1):
        x=forest_x(z)+side*random.uniform(5.2,8)
        tree_z=z+random.uniform(-1.8,1.8)
        h=random.uniform(10,15)
        root_curve([(x,1.65,tree_z),(x-side*.25,h*.43,tree_z+.3),
                    (x+side*.8,h*.76,tree_z-.5),(x+side*.3,h,tree_z-1)],
                   .65,'Deep canopy trunk')
        for dx in (-2,1,3):
            mass('Deep canopy crown',(x+dx,h,tree_z),(4,2.3,4.7),random.choice(leaves))
        if z%3:
            box('Forest ruin remnant',(x+side*2,3,z),(1.5,2.7,2),stone,True)
    # Shoulders conceal the flat study boundary without filling the walking lane.
    for x in (-28,3):
        # Keep the west clearing and its four-metre camera orbit out of foliage.
        shoulder_x=-36 if x==-28 and abs(z+68)<14 else x
        mass('Forest shoulder',(shoulder_x,3,z),(5,3,5),earth)
box('Forest game clearing',(-23,1.4,-68),(10,.5,9),stone,True)
road([(forest_x(-68),1.65,-68),(-23,1.65,-68)],3)
for side in (-1,1): terrain_bank(side)

# REF5/6 need foliage behind the foreground trunks, not an empty side horizon.
# A local random stream keeps new woodland from changing the cavern's geometry.
woodland_state=random.getstate();random.seed(914)
for i,z in enumerate(range(-43,-107,-8)):
    for side in (-1,1):
        x=forest_x(z)+side*(18+1.8*math.sin(i*1.3))
        # The west game clearing includes a four-metre camera orbit.
        if side<0 and abs(z+68)<17: x=min(x,-36)
        # Keep the exterior comparison sightline outside the background crowns.
        if side>0 and z<-86: x=max(x,20)
        h=14+3*math.sin(i*.8+side)
        branch('Woodland background trunk',(x,1.6,z),(x-side,h,z-2),.65,bark)
        mass('Woodland middle crown',(x,7.5,z),(6,4.5,6),leaves[i%3])
        mass('Woodland upper crown',(x-side*1.5,h,z-1),(7,4,6),leaves[(i+1)%3])
        mass('Woodland lower silhouette',(x+side*1.5,4.5,z+3),(5,3.5,5),leaves[0])
random.setstate(woodland_state)

# REF7: a readable exterior courtyard and tree-wrapped facade, not a solid box.
box('Archive courtyard',(-12,1.10,-103),(30,1,22),earth,True)
mesh('Forest courtyard threshold',
     [(x+side*w/2,1.65,z) for x,z,w in [(forest_x(-90),-90,5.6),(-12,-96,6),(-12,-103,7)]
      for side in (-1,1)],[(0,1,3,2),(2,3,5,4)],stone,True)
road([(-12,1.65,-103),(-12,1.65,-113)],7)
for x,h in [(-24,6),(-19.5,10),(-4.5,9),(0,5)]:
    box('Stepped archive facade',(x,1.65+h/2,-113),(5,h,3),stone,True)
arch(-12,1.65,-113,6,9,2)
box('Archive central crown',(-12,11.7,-114),(12,1.5,4),stone,True)
# Raise the central structure above its lower ruined wings, as in REF7.
for x,h in [(-17,7.2),(-7,5.8)]:
    box('Archive upper facade',(x,12.4+h/2,-115),(3,h,4),stone,True)
arch(-12,12.4,-115,5,6,3)
box('Archive upper broken belt',(-13,19.5,-115),(10,.8,4),stone,True)
for x,h in [(-20,14),(-5,12)]:
    box('Facade broken pinnacle',(x,h/2+1.65,-115),(1.5,h,2),stone,True)
root_curve([(-23,1.65,-113),(-22,9,-114),(-19,18,-116),(-15,27,-118)],
           2.1,'Archive hero tree')
for end in [(-7,26,-117),(-28,23,-118),(-16,30,-124)]:
    branch('Hero spreading limb',(-19,20,-116),end,1.2,bark)
    mass('Hero tree crown',end,(6.5,4,6),leaves[1])
hero_state=random.getstate();random.seed(9147)
for at,scale in [((-10,29,-119),(4.5,3.5,5)),((-25,26,-116),(5,3,4)),
                 ((-18,25,-121),(5,4,5))]:
    mass('Hero secondary crown',at,scale,leaves[2])
random.setstate(hero_state)
for points in [
    [(-22,10,-114),(-24,6,-112),(-25,3,-108),(-28,1.5,-103)],
    [(-22,8,-114),(-20,5,-112),(-18,2.8,-109),(-17,1.5,-105)],
    [(-22,9,-114),(-25,5,-119),(-26,1.5,-125)],
    [(-21,12,-115),(-20,11.8,-112),(-15,12.4,-111.9),(-9,12.4,-111.9),
     (-5.4,10.5,-112),(-4.5,7,-112.2),(-3.8,1.5,-110)],
    [(-18.5,19,-116),(-18,17,-113),(-15,15.3,-113),(-9,14.5,-113),
     (-6.5,12,-112.6),(-5.8,8,-112.5),(-4.3,1.5,-111)],
]: root_curve(points,1.1)

# REF8: open central aisle, side arcades and a broken roof framing the sky.
box('Archive hall floor',(-12,1.15,-127),(30,1,28),stone,True)
for x in (-27,3):
    box('Archive side wall',(x,8,-128),(1.4,12.7,28),stone,True)
for z in (-119,-127,-135):
    for x in (-19,-5):
        box('Hall column plinth',(x,1.95,z),(2.2,.6,2.2),edge,True)
        branch('Hall column',(x,2.25,z),(x,10.8,z),.65,stone,True)
    arch(-12,1.65,z,12,11,.8)
for x in (-24,0):
    # Set roof remnants behind the facade, avoiding a detached-looking front lip.
    box('Broken roof shoulder',(x,14,-130),(6,.8,21),stone,True)
arch(-12,1.65,-141,5,8,1.5)
for x in (-23,-1):
    box('Archive rear wall',(x,6.65,-141),(16,10,1.5),stone,True)

# Descending passage reserves real clearance and joins the cavern's near shore.
road([(-12,1.65,-141),(-12,-7.5,-174)],5,'Archive descent')
# Closed side/roof rings replace disconnected decorative rocks. Keep a minimum
# 5.6 m opening and 6.2 m roof clearance; ends remain open for both transitions.
tunnel=[]
for i,z in enumerate([-141,-146,-151,-156,-161,-166,-171,-174]):
    y=1.65-(-z-141)/33*9.15
    bulge=.3*math.sin(i*1.4)
    for x,h in [(-2.8,-.35),(-3.15,3.6),(-1.8,6.2+bulge),
                (0,6.8+bulge),(1.9,6.4-bulge),(3.2,3.5),(2.8,-.35)]:
        # First ring overlaps the arch crown; no daylight seam above the tunnel.
        if i==0 and h>6: h+=2
        tunnel.append((-12+x,y+h,z))
faces=[]
for i in range(len(tunnel)//7-1):
    for j in range(6):
        a=i*7+j;b=a+7
        faces.extend([(a,b,a+1),(a+1,b,b+1)])
mesh('Continuous descent shell',tunnel,faces,edge,True)
# Narrow shoulders join the paving to its walls, preventing falls through verges.
for side in (-1,1):
    mesh('Descent shoulder',
         [(-12+side*x,y,z) for y,z in [(1.65,-141),(-7.5,-174)] for x in [2.5,2.85]],
         [(0,1,3,2)],edge,True)

# REF10: faceted chamber shell, central pool, broad usable bank and overhead oculus.
rock=bpy.data.materials.new('Cavern slate');rock.diffuse_color=(.22,.28,.32,1)
water=bpy.data.materials.new('Pool study');water.diffuse_color=(.09,.17,.20,1)
for mat in (rock,water):
    mat.use_nodes=True
    shader=mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value=mat.diffuse_color
    shader.inputs['Roughness'].default_value=.9 if mat==rock else .25
cx,cz=-12,-195
radial=[[random.uniform(-2,2) for _ in range(24)] for _ in range(4)]
for i in range(24):
    a,b=i*math.tau/24,(i+1)*math.tau/24
    # The entrance cuts only the lower wall, not a slit through the entire roof.
    pts=[]
    for level,(y,r) in enumerate([(-8,25),(3,24),(13,17),(18,4)]):
        for j,t in ((i,a),((i+1)%24,b)):
            radius=r+radial[level][j]*(.3 if r==4 else 1)
            shift=-10*(level/3)**2
            pts.append((cx+radius*math.cos(t),y,cz+shift+radius*math.sin(t)))
    faces=[(2,3,4),(3,5,4),(4,5,7),(4,7,6)]
    if i not in (5,6): faces=[(0,1,3),(0,3,2)]+faces
    mesh('Cavern wall shell',pts,faces,rock,True)
    # Shore bank is continuous; central water has no walkable collider.
def shore_radius(t): return 15.5+1.2*math.sin(3*t)+.7*math.cos(5*t)
for i in range(32):
    a,b=i*math.tau/32,(i+1)*math.tau/32
    pts=[(cx+r*math.cos(t),-7.5,cz+r*math.sin(t)) for r,t in ((shore_radius(a),a),(28,a),(28,b),(shore_radius(b),b))]
    mesh('Cavern shore',pts,[(3,2,1,0)],edge,True)
    lip=[(cx+shore_radius(t)*math.cos(t),y,cz+shore_radius(t)*math.sin(t)) for t,y in ((a,-7.5),(b,-7.5),(b,-9),(a,-9))]
    mesh('Shore rock lip',lip,[(0,1,2,3)],rock)
mesh('Cavern pool',[(cx+(shore_radius(i*math.tau/32)+.15)*math.cos(i*math.tau/32),-7.8,
                     cz+(shore_radius(i*math.tau/32)+.15)*math.sin(i*math.tau/32)) for i in range(32)],
     [tuple(reversed(range(32)))],water)
for x,z,h in [(-33,-207,10),(8,-204,12),(-4,-217,13),(-22,-216,8)]:
    mass('Cavern rock buttress',(x,-7.5+h*.45,z),(3,h*.75,3.5),rock)
box('Cavern game shelf',(-33,-8,-195),(9,1,12),edge,True)

views={
 'reference':{'position':[0,13,30],'target':[0,4,-8],'ref':'REF4'},
 'forest':{'position':[-12,4,-43],'target':[-10,5,-64],'ref':'REF5'},
 'canopy':{'position':[-12,4,-67],'target':[-14,6,-89],'ref':'REF6'},
 'exterior':{'position':[1,7,-91],'target':[-13,13,-115],'ref':'REF7'},
 'interior':{'position':[-12,4,-116],'target':[-12,8,-140],'ref':'REF8'},
 'cavern':{'position':[-26,-3,-176],'target':[-12,4,-201],'ref':'REF10'},
}
for name,v in views.items():
    bpy.ops.object.camera_add(location=pos(v['position']))
    cam=bpy.context.object;cam.name='View_'+name
    cam.rotation_euler=(Vector(pos(v['target']))-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.lens=36
for name,at in {'Hub':[5,0,5],'Forest':[-23,1.65,-68],'Hall':[-23,1.65,-123],'Cavern':[-33,-7.5,-195]}.items():
    bpy.ops.object.empty_add(location=pos(at));bpy.context.object.name='FutureGame_'+name
for o in bpy.context.scene.objects:
    if o.type=='MESH' and o.data.materials and o.data.materials[0]==collision: o.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
for mat in list(bpy.data.materials):
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.data.materials and o.data.materials[0]==mat]
    if not objects: continue
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects: o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join()
    o=bpy.context.object;o.name='Collision' if mat==collision else mat.name.replace(' ','_')
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bpy.ops.export_scene.gltf(filepath=str(EXPORT),export_format='GLB',export_cameras=True,export_texcoords=False)
(ROOT/'src/config/world-views.json').write_text(json.dumps(views,indent=2)+'\n')
print('WORLD_EXPORTED',EXPORT.stat().st_size,'bytes; six comparison cameras and four future game anchors')
