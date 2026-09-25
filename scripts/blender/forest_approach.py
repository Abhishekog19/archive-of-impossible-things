"""REF5 approach production. Reuses the kit; preserves the resident walking floor."""
import bpy
import math
import random
import json
import sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.artifacts/blender'
rng = random.Random(925)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 32
scene.cycles.max_bounces = 2
scene.render.threads_mode = 'FIXED'
scene.render.threads = 6
scene.world.use_nodes = True
background = scene.world.node_tree.nodes['Background']
background.inputs['Color'].default_value = (.48,.60,.72,1)
background.inputs['Strength'].default_value = .4
bpy.ops.object.light_add(type='SUN')
sun = bpy.context.object
sun.data.energy = 2.1
sun.data.color = (1,.91,.77)
sun.data.angle = .06
sun.rotation_euler = Vector((-6,8,-12)).to_track_quat('-Z','Y').to_euler()

families = ['Fern','Low_Shrub','Grass_Tuft','Broadleaf_Clump']
with bpy.data.libraries.load(str(ROOT/'art/source/archive-kit.blend'),link=False) as (src,dst):
    dst.objects = ['Author_Slab_'+str(i) for i in range(1,7)] + families + [
        'Author_Tree_Tall','Author_Tree_Leaning','Author_Tree_Broadleaf',
        'Tree_Tall_Leaves','Tree_Leaning_Leaves','Tree_Leaves']
sources = {o.name:o for o in dst.objects}
with bpy.data.libraries.load(str(ROOT/'art/source/world-blockout.blend'),link=False) as (src,dst):
    dst.objects = [n for n in src.objects if n.startswith(('Continuous terrain',
        'Canopy approach','Forest extension ground','Connected paving','Continuous forest bank'))]
vertices,faces = [],[]
for o in dst.objects:
    offset = len(vertices)
    # Library objects are unlinked; their world matrix may not be evaluated yet.
    # These terrain objects are unparented, so the authored basis is authoritative.
    vertices.extend(o.matrix_basis@v.co for v in o.data.vertices)
    faces.extend(tuple(offset+i for i in p.vertices) for p in o.data.polygons)
bvh = BVHTree.FromPolygons(vertices,faces)
def height(x,z):
    hit = bvh.ray_cast(Vector((x,-z,25)),Vector((0,0,-1)))[0]
    assert hit is not None, (x,z)
    return hit.z
def road_x(z):
    t = max(0,min(1,(-z-42)/52))
    return -12+3.8*math.sin(t*math.tau)*math.sin(t*math.pi)
def place(source,name,x,z,scale=1,yaw=0,y=None):
    o = bpy.data.objects.new(name,sources[source].data.copy())
    scene.collection.objects.link(o)
    o.location = (x,-z,height(x,z) if y is None else y)
    o.scale = (scale,)*3
    o.rotation_euler.z = yaw
    return o
def mesh(name,verts,faces,material):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts,[],faces)
    data.update()
    data.materials.append(material)
    o = bpy.data.objects.new(name,data)
    scene.collection.objects.link(o)
    return o

stone,wood,earth,leaves = [],[],[],[]
# Four staggered stones follow the existing curved route, from the old patch to REF6.
for row in range(25):
    z = -40.6-row
    derivative = (road_x(z+.1)-road_x(z-.1))/.2
    for col in range(4):
        x = road_x(z)+(col-1.5)*1.12+.065*math.sin(row*1.8)
        o = place('Author_Slab_'+str(1+(row*3+col)%6),'Approach flagstone',x,z,.93,
                  math.atan(derivative)+rng.uniform(-.035,.035),height(x,z)-.075)
        if z>-42: o.rotation_euler.x = math.atan(.055)
        stone.append(o)

# A broken low wall and rock outcrops give the shoulders a readable silhouette.
for side,z in [(-1,-46),(1,-51),(-1,-58),(1,-62)]:
    cx = road_x(z)+side*4.3
    for course in range(3):
        for col in range(4-course):
            x = cx+side*course*.1
            zz = z+(col-1.5)*.9
            o = place('Author_Slab_'+str(1+(col+course)%6),'Fallen roadside masonry',x,zz,
                      1,rng.uniform(-.09,.09),height(x,zz)+course*.38)
            o.scale = (.65,.75,1.8)
            stone.append(o)
    for j in range(4):
        x,zr = cx+side*rng.uniform(.8,3),z+rng.uniform(-2,2)
        o = place('Author_Slab_'+str(j+1),'Mossy shoulder outcrop',x,zr,1,rng.random()*6.28,
                  height(x,zr)-.12)
        o.scale = (rng.uniform(1.1,2.4),rng.uniform(1.2,2.2),rng.uniform(3,6))
        stone.append(o)

# Terrain remains collision-owned by the world. This thin skin receives dappled light.
soil = bpy.data.materials.new('Approach shaded moss and soil')
soil.use_nodes = True
nodes,links = soil.node_tree.nodes,soil.node_tree.links
coords = nodes.new('ShaderNodeNewGeometry')
noise = nodes.new('ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 1.3
noise.inputs['Detail'].default_value = 2
links.new(coords.outputs['Position'],noise.inputs['Vector'])
ramp = nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].color = (.035,.045,.017,1)
ramp.color_ramp.elements[1].color = (.14,.18,.044,1)
links.new(noise.outputs['Fac'],ramp.inputs[0])
links.new(ramp.outputs[0],nodes['Principled BSDF'].inputs['Base Color'])
nodes['Principled BSDF'].inputs['Roughness'].default_value = 1
verts,faces = [],[]
for row in range(26):
    z = -40.1-row
    for col in range(25):
        x = road_x(z)+col-12
        verts.append((x,-z,height(x,z)+.014))
for row in range(25):
    for col in range(24):
        a = row*25+col
        faces.append((a,a+1,a+26,a+25))
earth.append(mesh('Woodland moss floor',verts,faces,soil))

# Irregular root spacing and three crown shapes form a shaded corridor.
tree_specs = [(-1,-42.5,5.4,13),(1,-43.7,5.7,14),(-1,-49.4,5.2,15),
    (1,-50.2,5.6,13),(-1,-56.2,5.1,14),(1,-56.8,6.0,16),
    (-1,-63,5.5,14),(1,-62.8,5.3,13),(-1,-45,10,17),
    (1,-47,10,17),(-1,-58,10.5,18),(1,-60,10,17)]
for i,(side,z,offset,tall) in enumerate(tree_specs):
    kind,leaf_name = [('Tall','Tree_Tall_Leaves'),('Leaning','Tree_Leaning_Leaves'),
                      ('Broadleaf','Tree_Leaves')][i%3]
    scale = tall/max(v.co.z for v in sources[leaf_name].data.vertices)
    x = road_x(z)+side*offset
    yaw = rng.uniform(-math.pi,math.pi)
    trunk = place('Author_Tree_'+kind,'Approach branching trunk',x,z,scale,yaw)
    trunk.scale.x *= .76
    trunk.scale.y *= .76
    bpy.ops.object.select_all(action='DESELECT')
    trunk.select_set(True)
    bpy.context.view_layer.objects.active = trunk
    remesh = trunk.modifiers.new('Fuse branches','REMESH')
    remesh.mode = 'VOXEL'
    remesh.voxel_size = .075
    remesh.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    smooth = trunk.modifiers.new('Soften junctions','SMOOTH')
    smooth.factor = .6
    smooth.iterations = 3
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    decimate = trunk.modifiers.new('Bound trunk detail','DECIMATE')
    decimate.ratio = .3
    bpy.ops.object.modifier_apply(modifier=decimate.name)
    trunk.data.validate(clean_customdata=True)
    trunk.data.update()
    wood.append(trunk)
    crown = place(leaf_name,'Approach layered crown',x,z,scale,yaw)
    crown.scale.x *= .76
    crown.scale.y *= .76
    old = crown.data
    # Keep a sparse subset of leaf silhouettes, six triangles per leaf. More
    # distant crowns use fewer leaves; openings admit dappled light onto the road.
    count = len(old.vertices)//9
    chosen = range(0,count,3 if i<8 else 4)
    tints,points,polygons = [],[],[]
    low,high = min(v.co.z for v in old.vertices),max(v.co.z for v in old.vertices)
    for j in chosen:
        centre = old.vertices[j*9].co
        base = len(points)
        points.extend(tuple(old.vertices[j*9+k].co) for k in range(1,9))
        polygons.append(tuple(range(base,base+8)))
        c = old.color_attributes.active_color.data[old.polygons[j*8].loop_start].color
        shade = .42+.58*(centre.z-low)/max(.01,high-low)
        tints.append((c[0]*shade,c[1]*shade,c[2]*shade,1))
    data = bpy.data.meshes.new('Approach economical leaves')
    data.from_pydata(points,[],polygons)
    for mat in old.materials: data.materials.append(mat)
    attr = data.color_attributes.new(name='FoliageColor',type='BYTE_COLOR',domain='CORNER')
    for poly in data.polygons:
        poly.use_smooth = True
        for loop in poly.loop_indices: attr.data[loop].color = tints[poly.index]
    data.update()
    crown.data = data
    leaves.append(crown)

prototypes,markers,casters = [],[],[]
# Shade the shared plant geometry once so every visible instance and its bake
# caster uses the same darker woodland palette.
for family in families:
    data = sources[family].data
    colors = data.color_attributes.active_color
    if colors:
        low,high = min(v.co.z for v in data.vertices),max(v.co.z for v in data.vertices)
        for poly in data.polygons:
            for loop in poly.loop_indices:
                z = data.vertices[data.loops[loop].vertex_index].co.z
                factor = .32+.28*(z-low)/max(.01,high-low)
                c = colors.data[loop].color
                colors.data[loop].color = (c[0]*factor,c[1]*factor,c[2]*factor,1)
for family in families:
    proto = place(family,'ApproachPlantPrototype_'+family,0,0,y=0)
    proto.hide_render = True
    prototypes.append(proto)
for cluster in range(44):
    zc = -41.4-(cluster//2)*1.05
    side = -1 if cluster%2 else 1
    width = rng.uniform(2.7,8)
    for j in range(6):
        z = zc+rng.uniform(-.8,.8)
        x = road_x(z)+side*width+rng.uniform(-.6,.6)
        if abs(x-road_x(z))<2.45: continue
        family = families[(cluster+j)%4]
        size = rng.uniform(.7,1.45)
        plant = place(family,'Approach plant shadow',x,z,size,rng.random()*math.tau,height(x,z)+.025)
        casters.append(plant)
        marker = bpy.data.objects.new('ApproachPlant_'+family+'_'+str(len(markers)).zfill(3),None)
        scene.collection.objects.link(marker)
        marker.location,marker.scale,marker.rotation_euler = plant.location.copy(),plant.scale.copy(),plant.rotation_euler.copy()
        markers.append(marker)

targets = []
for name,objects in [('Stone',stone),('Wood',wood),('Ground',earth)]:
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects: o.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.duplicate()
    bpy.ops.object.join()
    target = bpy.context.object
    target.name = 'ForestApproach_'+name
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    target.data.validate(clean_customdata=True)
    target.data.update()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.009)
    bpy.ops.object.mode_set(mode='OBJECT')
    atlas = bpy.data.images.new('Approach '+name+' diffuse',width=2048,height=2048,alpha=False)
    atlas.filepath_raw = str(OUT/('forest-approach-'+name.lower()+'.png'))
    atlas.file_format = 'PNG'
    for i,original in enumerate(list(target.data.materials)):
        mat = original.copy()
        target.data.materials[i] = mat
        tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex.image = atlas
        mat.node_tree.nodes.active = tex
    targets.append((target,atlas))
for o in stone+wood+earth:
    o.hide_render = True
    o.hide_set(True)
scene.render.bake.use_pass_color = True
scene.render.bake.use_pass_direct = True
scene.render.bake.use_pass_indirect = True
scene.render.bake.margin = 10
for target,atlas in targets:
    bpy.ops.object.select_all(action='DESELECT')
    target.select_set(True)
    bpy.context.view_layer.objects.active = target
    print('BAKING '+target.name,flush=True)
    bpy.ops.object.bake(type='DIFFUSE')
    atlas.save()
    atlas.pack()
# Replace materials only after every target has contributed its source shading.
for target,atlas in targets:
    mat = bpy.data.materials.new(target.name+'_Diffuse')
    mat.use_nodes = True
    tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image = atlas
    mat.node_tree.links.new(tex.outputs['Color'],mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    target.data.materials.clear()
    target.data.materials.append(mat)
    for poly in target.data.polygons: poly.material_index = 0

colliders = []
for trunk in wood:
    bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=.55,depth=4,
        location=trunk.location+Vector((0,0,2)))
    colliders.append(bpy.context.object)
bpy.ops.object.select_all(action='DESELECT')
for o in colliders: o.select_set(True)
bpy.context.view_layer.objects.active = colliders[0]
bpy.ops.object.join()
collision = bpy.context.object
collision.name = 'ForestApproach_Collision'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
collision.hide_render = True
bpy.ops.object.select_all(action='DESELECT')
for o in leaves: o.select_set(True)
bpy.context.view_layer.objects.active = leaves[0]
bpy.ops.object.join()
foliage = bpy.context.object
foliage.name = 'ForestApproach_Foliage'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
mat = bpy.data.materials.new('Approach leaf colour')
mat.use_nodes = True
color = mat.node_tree.nodes.new('ShaderNodeVertexColor')
color.layer_name = foliage.data.color_attributes.active_color.name
mat.node_tree.links.new(color.outputs['Color'],mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
foliage.data.materials.clear()
foliage.data.materials.append(mat)
for poly in foliage.data.polygons: poly.material_index = 0
for o in [collision]+prototypes+markers+[t for t,_ in targets]: o.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/forest-approach.blend'),compress=True)
export = ROOT/'public/models/forest-approach.glb'
bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=True,
    export_image_format='JPEG',export_image_quality=94)
report = {'stage':'REF5 approach expansion','slabs':100,'trees':len(wood),'groundCover':len(markers),
    'atlases':[2048]*3,'bytes':export.stat().st_size,'extentZ':[-40.1,-65.1]}
sys.path.insert(0,str(Path(__file__).parent))
from world_art_context import export_context
report['removedContextProxies'] = export_context()
(OUT/'forest-approach-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('FOREST_APPROACH '+json.dumps({k:v for k,v in report.items() if k!='removedContextProxies'}),flush=True)
