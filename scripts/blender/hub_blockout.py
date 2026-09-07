"""Deterministic Phase 1 composition study. Run with run.cjs blockout.

Authored coordinates are browser X/Y/Z; Blender receives X/-Z/Y.
Only generated hub-blockout outputs are replaced. No user scene is loaded.
"""
import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'art/source/hub-blockout.blend'
EXPORT = ROOT / 'public/models/hub-blockout.glb'
random.seed(41)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system = 'METRIC'

def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = 0.95
    return m

stone = material('Limestone', (0.57, 0.55, 0.40))
edge = material('Stone shade', (0.33, 0.36, 0.29))
earth = material('Moss earth', (0.19, 0.25, 0.10))
bark = material('Trunks', (0.18, 0.20, 0.12))
leaves = [material('Canopy '+str(i), c) for i, c in enumerate([
    (0.12, 0.20, 0.10), (0.20, 0.28, 0.12), (0.28, 0.34, 0.16)])]
distant = material('Distant forest', (0.29, 0.36, 0.27))
collision = material('Collision only', (0.5, 0.5, 0.5))

def pos(p):
    return (p[0], -p[2], p[1])

def finish(obj, name, mat):
    obj.name = name
    obj.data.materials.append(mat)
    return obj

def box(name, p, size, mat, yaw=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos(p))
    o = bpy.context.object
    o.scale = (size[0], size[2], size[1])
    o.rotation_euler.z = yaw
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(o, name, mat)

def solid_box(name, p, size, mat, yaw=0):
    box(name, p, size, mat, yaw)
    box('Collision', p, size, collision, yaw)

def cylinder(name, p, radius, height, mat, vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=height, location=pos(p))
    return finish(bpy.context.object, name, mat)

def mass(name, p, scale, mat):
    coarse = mat == distant or name in ('Woodland shoulder', 'Boundary outcrop')
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1 if coarse else 2, radius=1, location=pos(p))
    o = bpy.context.object
    o.scale = (scale[0], scale[2], scale[1])
    o.rotation_euler.z = random.uniform(-0.5, 0.5)
    for v in o.data.vertices:
        v.co *= random.uniform(0.86, 1.12)
    return finish(o, name, mat)

def surface(name, vertices, faces, mat, solid=False):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([pos(v) for v in vertices], [], faces)
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    finish(o, name, mat)
    if solid:
        proxy = bpy.data.objects.new('Collision', mesh.copy())
        proxy.data.materials.clear()
        proxy.data.materials.append(collision)
        bpy.context.collection.objects.link(proxy)
    return o

def road_height(x, z):
    if x < -5 and z < -14:
        return min(1.65, (-z-14)*0.055)
    return -max(0, z-12)*0.045

def road_distance(x, z):
    # Centreline segments and half widths; also used to keep vegetation off routes.
    routes = [((0,9),(0,29),3.5), ((-6,-8),(-12,-22),2.8),
              ((-12,-22),(-12,-44),2.8), ((8,-5),(17,-15),3),
              ((0,-10),(0,-17),2)]
    nearest = (999, 0)
    for (ax,az),(bx,bz),width in routes:
        dx,dz=bx-ax,bz-az
        t=max(0,min(1,((x-ax)*dx+(z-az)*dz)/(dx*dx+dz*dz)))
        px,pz=ax+t*dx,az+t*dz
        d=math.hypot(x-px,z-pz)-width
        if d<nearest[0]:
            nearest=(d,road_height(px,pz))
    return nearest

def terrain_height(x,z):
    r=math.hypot(x,z)
    if r<13.4:
        return -0.20
    d,h=road_distance(x,z)
    natural=0.7+1.1*math.sin(x*0.16)*math.cos(z*0.11)+0.5*math.sin(z*0.3)
    # A continuous eroded valley separates the broken spur from its far bank.
    channel=21+3*math.sin((-z-17)*0.07)
    if z<-17:
        cut=max(0,1-abs(x-channel)/6)
        natural-=12*min(1,(-z-17)/5)*cut
    shoulder=max(0,min(1,(d-0.5)/4))
    value=(h-0.22)*(1-shoulder)+natural*shoulder
    blend=max(0,min(1,(r-13.4)/4))
    return -0.2*(1-blend)+value*blend

def ribbon(name, points, width):
    vertices=[]
    for i,(x,z) in enumerate(points):
        a=points[max(0,i-1)]
        b=points[min(len(points)-1,i+1)]
        dx,dz=b[0]-a[0],b[1]-a[1]
        length=math.hypot(dx,dz)
        nx,nz=-dz/length,dx/length
        y=road_height(x,z)-0.025
        vertices.extend([(x+nx*width/2,y,z+nz*width/2),(x-nx*width/2,y,z-nz*width/2)])
    faces=[(2*i,2*i+2,2*i+3,2*i+1) for i in range(len(points)-1)]
    surface(name,vertices,faces,stone,True)

# Connected terrain replaces the disconnected floating plates.
vertices=[]
faces=[]
nx,nz=81,91
for j in range(nz):
    z=34-j*1.5
    for i in range(nx):
        x=-60+i*1.5
        vertices.append((x,terrain_height(x,z),z))
for j in range(nz-1):
    for i in range(nx-1):
        k=j*nx+i
        faces.extend([(k,k+1,k+nx+1),(k,k+nx+1,k+nx)])
surface('Continuous terrain',vertices,faces,earth,True)

# Main plaza: 26 metres across, origin at walkable ground height.
cylinder('Plaza foundation', (0, -0.68, 0), 13, 1.04, edge, 64)
cylinder('Plaza paving', (0, -0.08, 0), 12.8, 0.16, stone, 64)
cylinder('Collision', (0, -0.3, 0), 13, 0.6, collision, 64)
# Concentric inlaid bands communicate the reference's circular composition.
for radius in (0.7, 2.2, 4.1, 6.0):
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=0.045,
        major_segments=64, minor_segments=4, location=(0, 0, 0.012))
    finish(bpy.context.object, 'Plaza ring', earth)

# Foreground approach; left route runs thirty metres beneath the canopy.
ribbon('Arrival slope',[(0,z) for z in range(9,30)],7)
ribbon('Left path mouth',[(-6-6*t/14,-8-t) for t in range(15)],5.6)
ribbon('Canopy approach',[(-12,z) for z in range(-22,-45,-1)],5.6)
ribbon('Right branch',[(8+0.9*t,-5-t) for t in range(11)],6)
solid_box('Far broken bridge', (24, -1, -24), (5, 1.2, 9), edge, -0.55)
# Fallen masonry ends the traversable right spur before the gap.
solid_box('Broken branch barrier', (17, 0.8, -15), (5.5, 1.6, 1.3), edge, -0.55)
solid_box('Overgrown path mouth', (0, -0.44, -15), (4, 0.8, 7), stone)
solid_box('Overgrown branch roots', (0, 0.7, -17), (4.5, 1.4, 1.2), bark)
solid_box('Approach end rocks', (-12, 3, -44), (6, 2.7, 2), edge)

# Terrain masses hold the central green island and the edges of the routes.
for z in range(-23,-65,-5):
    for x in (15+2*math.sin(z*0.07),29+2*math.sin(z*0.07)):
        h=terrain_height(x,z)
        mass('Ravine cliff',(x,h-3,z),(2.3,5,3.6),edge)

# Broken columns frame the plaza without cluttering the circular centre.
for x,z,h in [(-10,7,4.2),(10,6,2.4),(-12,-3,2.2),(-7,-10,4.0),
               (7,-9,4.8),(14,-9,2.6),(-15,-20,2.8),(-8,-27,2.3)]:
    solid_box('Column base', (x,0.2,z), (2,0.4,2), edge)
    # Broad broken profiles, not surface weathering: stepped-off block courses.
    for j in range(math.ceil(h/0.65)):
        level=min(0.63,h-j*0.65)
        if level<=0:
            continue
        width=1.15 if j<h/0.65-1 else random.uniform(0.6,1.0)
        solid_box('Broken column course',(x+random.uniform(-0.07,0.07),0.4+j*0.65+level/2,z),
                  (width,level,1.12),stone,random.uniform(-0.05,0.05))
    for j in range(3):
        rx,rz=x+random.uniform(-1.5,1.5),z+random.uniform(-1.5,1.5)
        if road_distance(rx,rz)[0]>0:
            solid_box('Fallen masonry',(rx,0.25,rz),(0.7,0.5,1),edge,random.uniform(-1,1))

# Ruined wall shoulders frame the island; clear openings remain walkable.
for x,z in [(-5,-16),(6,-16),(-17,-23),(-7,-29)]:
    base=terrain_height(x,z)
    for j in range(4):
        height=2.9-j*0.55
        solid_box('Broken wall',(x+j*0.95,base+height/2,z),(0.9,height,0.8),stone)

# Repeating trunks are silhouette proxies, not final vegetation assets.
def tree(x,z,h,far=False):
    base=terrain_height(x,z)
    cylinder('Tree trunk', (x,base+h/2,z), 0.3 if far else 0.5, h, bark, 7)
    if not far:
        cylinder('Collision', (x,base+h/2,z), 0.5, h, collision, 8)
    crown=random.uniform(0.8,1.3)
    for i in range(5 if not far else 3):
        angle=random.uniform(0,math.tau)
        reach=random.uniform(0.5,3)
        dx,dz=math.cos(angle)*reach,math.sin(angle)*reach
        s=random.uniform(0.7,1.2)*crown
        mass('Forest crown', (x+dx,base+h+random.uniform(-1,1.5),z+dz), (3.4*s,2.5*s,3*s),
             distant if far else random.choice(leaves))
        if not far:
            start=Vector(pos((x,base+h*0.6,z)))
            end=Vector(pos((x+dx,base+h,z+dz)))
            delta=end-start
            bpy.ops.mesh.primitive_cone_add(vertices=6,radius1=0.3,radius2=0.12,depth=delta.length,location=(start+end)/2)
            branch=bpy.context.object
            branch.rotation_euler=delta.to_track_quat('Z','Y').to_euler()
            finish(branch,'Tree limb',bark)

for x,z,h in [(-17,9,12),(17,12,13),(-18,-2,11),(18,-4,12),
              (-17,-13,11),(-7,-20,10),(-17,-25,12),(-8,-32,11),
              (-17,-37,11),(-7,-42,12),(0,-23,10),(6,-28,12)]:
    tree(x,z,h)
for i in range(75):
    x=random.uniform(-55,55)
    z=random.uniform(-95,-45)
    if 14<x<30 and z>-65:
        continue
    tree(x,z,random.uniform(9,17),True)

# Midground and foreground enclosure; keep gaps over paths and the distant tower.
for x,z,h in [(-23,2,14),(23,5,15),(-22,-12,13),(3,-36,12),(10,-37,13),
               (-22,-35,12),(-4,-42,13),(-20,20,15),(19,22,15)]:
    tree(x,z,h)

# Central forest island is the compositional wedge between the two clear routes.
for i in range(28):
    x=random.uniform(-4,6)
    z=random.uniform(-36,-17)
    mass('Island understory',(x,terrain_height(x,z)+0.8,z),(2.2,1.6,2.4),random.choice(leaves))

# Low forest masses leave the plaza and path interiors readable.
for i in range(65):
    angle=random.uniform(0,math.tau)
    radius=random.uniform(14,23)
    x,z=math.cos(angle)*radius,math.sin(angle)*radius
    if abs(x)<5 or (x < -7 and z < -6) or (x>7 and z<-4):
        continue
    mass('Understory proxy',(x,0.7,z),(2.5,1.6,2.3),random.choice(leaves))

# Continuous woodland shoulders close the bare horizon beneath crowns.
for i in range(150):
    x,z=random.uniform(-48,48),random.uniform(-90,27)
    if math.hypot(x,z)<14 or road_distance(x,z)[0]<1.3 or (14<x<30 and z<-17):
        continue
    mass('Woodland shoulder',(x,terrain_height(x,z)+0.8,z),
         (random.uniform(2,4),random.uniform(1.2,2.8),random.uniform(2,4)),random.choice(leaves))

# Natural boulder perimeter bounds the current playable area, including the arrival.
for x,z in [(x,z) for x in range(-29,34,3) for z in (-48,30)]+[(x,z) for x in (-29,33) for z in range(-45,30,3)]:
    y=terrain_height(x,z)
    mass('Boundary outcrop',(x,y+1.7,z),(2.4,3.1,2.6),edge)
    box('Collision',(x,y+2,z),(3.4,5,3.4),collision)

# Tower silhouette sits above the distant crown line, toward frame right.
box('Tower shaft',(24,13,-74),(3.5,24,3.5),stone)
for x in (22.6,25.4):
    for z in (-75.4,-72.6):
        box('Tower belfry pier',(x,27,z),(0.65,4,0.65),stone)
box('Tower crown',(24,29,-74),(4,0.8,4),stone)

# Preserve individual editable source objects before merging the runtime export.
SOURCE.parent.mkdir(parents=True,exist_ok=True)
EXPORT.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.object.camera_add(location=pos((0,13,30)))
camera=bpy.context.object
camera.name='ReferenceCamera'
camera.rotation_euler=(Vector(pos((0,4,-8)))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.lens=36
bpy.context.scene.camera=camera
bpy.context.scene.render.resolution_x=1672
bpy.context.scene.render.resolution_y=941
for o in bpy.context.scene.objects:
    if o.type=='MESH' and o.data.materials and o.data.materials[0]==collision:
        o.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))

# Merge by material to keep the study inexpensive in WebGL.
for mat in list(bpy.data.materials):
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.data.materials and o.data.materials[0]==mat]
    if not objects:
        continue
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.object.join()
    joined=bpy.context.object
    joined.name='Collision' if mat==collision else mat.name.replace(' ','_')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

bpy.ops.export_scene.gltf(filepath=str(EXPORT),export_format='GLB',export_cameras=True)
print(f'BLOCKOUT_EXPORTED {EXPORT.stat().st_size} bytes')
