"""Phase 2 benchmark: authored relief + a portable full-colour diffuse bake.

Local metre coordinates use Blender Z-up. R3F places the GLB at (-8, 0, -9).
Rebuild replaces only these generated corner outputs; source objects stay editable.
"""
import bpy
import math
import random
import json
import time
from pathlib import Path
from mathutils import Vector

started = time.monotonic()
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'art/source/hub-corner.blend'
EXPORT = ROOT / 'public/models/hub-corner.glb'
DIAGNOSTICS = ROOT / '.artifacts/blender'
random.seed(83)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 24
scene.cycles.max_bounces = 3
scene.cycles.use_denoising = True
scene.view_settings.view_transform = 'AgX'
visuals = []
colliders = []
foliage = []

def material(name, dark, light, scale=5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n, links = m.node_tree.nodes, m.node_tree.links
    p = n.get('Principled BSDF')
    p.inputs['Roughness'].default_value = 0.92
    coord = n.new('ShaderNodeNewGeometry')
    noise = n.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Detail'].default_value = 2
    links.new(coord.outputs['Position'], noise.inputs['Vector'])
    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.25
    ramp.color_ramp.elements[0].color = (*dark, 1)
    ramp.color_ramp.elements[1].position = 0.78
    ramp.color_ramp.elements[1].color = (*light, 1)
    links.new(noise.outputs['Fac'], ramp.inputs[0])
    links.new(ramp.outputs[0], p.inputs['Base Color'])
    return m

stone = [material('Warm limestone '+str(i),
                 (0.43+i*.02, .43+i*.012, .31),
                 (.61+i*.035, .59+i*.025, .40+i*.02), 3) for i in range(3)]
moss = material('Moss in seams', (.055,.095,.026), (.23,.31,.065), 11)
bark = material('Bark planes', (.09,.105,.06), (.32,.29,.16), 15)
leaf_mats = [material('Leaf '+str(i), (.05+i*.018,.105+i*.023,.035),
                      (.20+i*.05,.31+i*.045,.075+i*.014), 2) for i in range(3)]

def mesh(name, verts, faces, mat):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    o = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    visuals.append(o)
    return o

def cube(name, at, size, mat, bevel=0, yaw=0, solid=False):
    bpy.ops.mesh.primitive_cube_add(size=1, location=at)
    o = bpy.context.object
    o.name = name
    o.scale = size
    o.rotation_euler.z = yaw
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if solid:
        c = o.copy()
        c.data = o.data.copy()
        c.name = 'Corner_Collision'
        bpy.context.collection.objects.link(c)
        colliders.append(c)
    if bevel:
        mod = o.modifiers.new('Chipped broad edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 1
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier=mod.name)
    visuals.append(o)
    return o

# Smooth collision and a darker seam bed are separate from decorative slab relief.
cube('Moss seam bed', (0,0,-.08), (8,9,.28), moss, solid=True)
for row in range(9):
    y = -4 + row
    offset = .45 if row % 2 else 0
    for col in range(7):
        x = -3.4 + col*1.08 + offset
        if x > 3.8:
            continue
        w, d = random.uniform(.89,1.02), random.uniform(.83,.96)
        h = random.uniform(.10,.15)
        # Eight corners form a chipped rectangle, with a separate dark vertical edge.
        cut = random.uniform(.08,.18)
        poly = [(-w/2+cut,-d/2),(w/2-cut,-d/2),(w/2,-d/2+cut),
                (w/2,d/2-cut),(w/2-cut,d/2),(-w/2+cut,d/2),
                (-w/2,d/2-cut),(-w/2,-d/2+cut)]
        verts = [(x+px+random.uniform(-.025,.025),y+py,z)
                 for z in (-.025,h) for px,py in poly]
        faces = [tuple(range(7,-1,-1)),tuple(range(8,16))]
        faces += [(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
        mesh('Weathered paving slab', verts, faces, random.choice(stone))

# Masonry follows one side of the path; the cap breaks down toward the plaza.
for row in range(5):
    for j in range(6-row//2):
        y = -.9+j*.77+(row%2)*.15
        x = -3.5+random.uniform(-.045,.045)
        cube('Broken wall course',(x,y,.32+row*.52),
             (.68,.72,random.uniform(.46,.51)),random.choice(stone),.065,
             random.uniform(-.035,.035),solid=True)

# Replace the corresponding blockout column at world (-7,-10).
cube('Column plinth',(1,1,.22),(1.7,1.7,.35),stone[0],.06,solid=True)
for i in range(6):
    cube('Column drum',(1+random.uniform(-.035,.035),1,.65+i*.53),
         (1.04 if i<5 else .77,1.07,.50),random.choice(stone),.07,
         random.uniform(-.035,.035),solid=True)

def limb(name, points, radii, mat, sides=9):
    verts=[]
    for i,p in enumerate(points):
        direction=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        direction.normalize()
        u=direction.cross(Vector((0,1,0)))
        if u.length<.01:
            u=direction.cross(Vector((1,0,0)))
        u.normalize()
        v=direction.cross(u).normalized()
        for j in range(sides):
            angle=j*math.tau/sides
            vert=Vector(p)+(math.cos(angle)*u+math.sin(angle)*v)*radii[i]*(1+.1*math.sin(j*2.4))
            verts.append(tuple(vert))
    faces=[tuple(reversed(range(sides)))]
    for i in range(len(points)-1):
        for j in range(sides):
            a=i*sides+j
            b=i*sides+(j+1)%sides
            faces.append((a,b,b+sides,a+sides))
    faces.append(tuple(range(len(verts)-sides,len(verts))))
    return mesh(name,verts,faces,mat)

trunk=limb('Rooted tree',[(3,3,0),(3.1,3,1.4),(2.8,3.1,3),(3.2,3.2,5),(2.6,3.1,7.5)],
           [.64,.46,.36,.24,.07],bark)
cube('Tree collider',(3,3,2),(.9,.9,4),bark,solid=True)
visuals.pop()  # This box is collision-only.
bpy.data.objects.remove(bpy.context.object,do_unlink=True)
for i in range(8):
    a=i*math.tau/8
    dx,dy=math.cos(a),math.sin(a)
    limb('Buttress root',[(3,3,.7),(3+dx*.7,3+dy*.7,.25),(3+dx*1.7,3+dy*1.7,.10)],
         [.27,.16,.015],bark,7)

def leaves(name, center, radius, count, mat):
    verts,faces=[],[]
    for _ in range(count):
        a=random.uniform(0,math.tau)
        r=radius*math.sqrt(random.random())
        p=Vector((center[0]+math.cos(a)*r,center[1]+math.sin(a)*r,
                  center[2]+random.uniform(-.4,.4)*radius))
        tilt=random.uniform(-.3,.5)
        u=Vector((math.cos(a),math.sin(a),tilt)).normalized()*random.uniform(.12,.27)
        v=Vector((-math.sin(a),math.cos(a),0))*random.uniform(.055,.12)
        k=len(verts)
        verts.extend([tuple(p-u),tuple(p+v),tuple(p+Vector((0,0,.035))),tuple(p-v),tuple(p+u)])
        faces.extend([(k,k+1,k+2),(k,k+2,k+3),(k+1,k+4,k+2),(k+2,k+4,k+3)])
    o=mesh(name,verts,faces,mat)
    visuals.remove(o)
    foliage.append(o)
    colors=o.data.color_attributes.new(name='FoliageColor',type='BYTE_COLOR',domain='CORNER')
    # Broad leaf colour planes stay crisp at every distance without alpha cards
    # or thousands of tiny UV islands stealing resolution from the stone bake.
    for poly in o.data.polygons:
        tint=random.uniform(.8,1.12)
        up=max(0,poly.normal.z)
        base=(.055+.085*up,.105+.12*up,.025+.03*up)
        for index in poly.loop_indices:
            colors.data[index].color=(*(c*tint for c in base),1)
    return o

for i in range(9):
    a=i*2.4
    end=(2.8+math.cos(a)*2.3,3+math.sin(a)*2,5.6+random.uniform(-.3,1.7))
    limb('Spreading branch',[(3,3,3.6),(end[0]*.5+1.5,end[1]*.5+1.5,end[2]-.5),end],[.22,.12,.015],bark,7)
    leaves('Layered leaf spray',end,1.2,140,leaf_mats[i%3])

# Ground cover grows at wall bases and outer shoulders, leaving the route open.
for i in range(24):
    x=random.choice([-1,1])*random.uniform(2.9,3.8)
    y=random.uniform(-4,4.1)
    leaves('Ground leaf cluster',(x,y,.18),random.uniform(.3,.55),20,leaf_mats[i%3])
for i in range(12):
    x,y=-3+random.uniform(-.2,.5),random.uniform(-3.5,3.6)
    cube('Fallen wall stone',(x,y,.2),(random.uniform(.3,.6),.45,.32),random.choice(stone),.06,random.uniform(-1,1))

# Warm directional illumination and a cool sky become image data, not runtime lights.
scene.world.use_nodes=True
background=scene.world.node_tree.nodes.get('Background')
background.inputs['Color'].default_value=(.48,.60,.72,1)
background.inputs['Strength'].default_value=.45
bpy.ops.object.light_add(type='SUN',location=(5,-6,10))
sun=bpy.context.object
sun.name='Bake warm afternoon'
sun.data.energy=2.1
sun.data.color=(1,.88,.62)
sun.data.angle=math.radians(5)
sun.rotation_euler=(Vector((-3,3,0))-sun.location).to_track_quat('-Z','Y').to_euler()

# UV the merged bake target, but save the editable objects and procedural materials.
for c in colliders:
    c.hide_render=True
    c.hide_set(True)
bpy.ops.object.select_all(action='DESELECT')
for o in visuals:
    o.select_set(True)
bpy.context.view_layer.objects.active=visuals[0]
bpy.ops.object.duplicate()
bpy.ops.object.join()
target=bpy.context.object
target.name='Corner_Baked'
for o in visuals:
    o.hide_render=True
    o.hide_set(True)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.003)
bpy.ops.object.mode_set(mode='OBJECT')
atlas=bpy.data.images.new('Corner diffuse lighting atlas',width=1024,height=1024,alpha=False)
atlas.file_format='PNG'
atlas.filepath_raw=str(DIAGNOSTICS/'corner-baked.png')
for mat in target.data.materials:
    node=mat.node_tree.nodes.new('ShaderNodeTexImage')
    node.image=atlas
    mat.node_tree.nodes.active=node
scene.render.bake.use_pass_direct=True
scene.render.bake.use_pass_indirect=True
scene.render.bake.use_pass_color=True
scene.render.bake.margin=6
print('CORNER_BAKE_START',flush=True)
bpy.ops.object.bake(type='DIFFUSE')
atlas.save()
atlas.pack()

baked=bpy.data.materials.new('Corner_Baked')
baked.use_nodes=True
nodes=baked.node_tree.nodes
texture=nodes.new('ShaderNodeTexImage')
texture.image=atlas
baked.node_tree.links.new(texture.outputs['Color'],nodes.get('Principled BSDF').inputs['Base Color'])
nodes.get('Principled BSDF').inputs['Roughness'].default_value=.95
target.data.materials.clear()
target.data.materials.append(baked)
for p in target.data.polygons:
    p.material_index=0

bpy.ops.object.select_all(action='DESELECT')
for o in foliage:
    o.select_set(True)
bpy.context.view_layer.objects.active=foliage[0]
bpy.ops.object.join()
leaf_mesh=bpy.context.object
leaf_mesh.name='Corner_Foliage'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
leaf_material=bpy.data.materials.new('Corner_Foliage')
leaf_material.use_nodes=True
color_node=leaf_material.node_tree.nodes.new('ShaderNodeVertexColor')
color_node.layer_name='FoliageColor'
leaf_material.node_tree.links.new(color_node.outputs['Color'],leaf_material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
leaf_mesh.data.materials.clear()
leaf_mesh.data.materials.append(leaf_material)
for p in leaf_mesh.data.polygons:
    p.material_index=0

# Export only baked geometry + simple collision; no authoring duplicates or lights.
bpy.ops.object.select_all(action='DESELECT')
for c in colliders:
    c.hide_set(False)
    c.select_set(True)
bpy.context.view_layer.objects.active=colliders[0]
bpy.ops.object.join()
collider=bpy.context.object
collider.name='Corner_Collision'
collider.data.materials.clear()
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
target.select_set(True)
leaf_mesh.select_set(True)
SOURCE.parent.mkdir(parents=True,exist_ok=True)
EXPORT.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True)
export_options={'filepath':str(EXPORT),'export_format':'GLB',
                'use_selection':True,'export_image_format':'JPEG'}
if 'export_jpeg_quality' in bpy.ops.export_scene.gltf.get_rna_type().properties:
    export_options['export_jpeg_quality']=90
bpy.ops.export_scene.gltf(**export_options)
report={'seconds':round(time.monotonic()-started,1),'atlas':[1024,1024],
        'glbBytes':EXPORT.stat().st_size,'sourceBytes':SOURCE.stat().st_size,
        'bake':'DIFFUSE: colour + direct + indirect, 24 CPU samples',
        'runtime':'UV0 diffuse bake + vertex-tinted two-sided foliage; two MeshBasicMaterials'}
(DIAGNOSTICS/'corner-report.json').write_text(json.dumps(report,indent=2))
print('CORNER_EXPORTED '+json.dumps(report),flush=True)
