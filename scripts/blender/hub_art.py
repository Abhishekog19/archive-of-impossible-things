"""Phase C hub stone pass. Preserve the plaza, route and collision layout.

Authored geometry stays editable. Hub, planted shoulders and the existing corner
share placed lighting; small ground-cover prototypes export with instance markers.
"""
import bpy
import math
import random
import json
import time
import sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.artifacts/blender'
started = time.monotonic()
rng = random.Random(2309)
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
bg = scene.world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (.48, .60, .72, 1)
bg.inputs['Strength'].default_value = .40
bpy.ops.object.light_add(type='SUN')
sun = bpy.context.object
sun.data.energy = 2.1
sun.data.color = (1, .91, .77)
sun.data.angle = .045
sun.rotation_euler = Vector((-6, 8, -12)).to_track_quat('-Z', 'Y').to_euler()
with bpy.data.libraries.load(str(ROOT / 'art/source/archive-kit.blend'), link=False) as (src, dst):
    dst.objects = ['Author_Slab_' + str(i) for i in range(1, 5)] + [
        'Author_Tree_Tall', 'Author_Tree_Leaning', 'Author_Tree_Broadleaf',
        'Tree_Tall_Leaves', 'Tree_Leaning_Leaves', 'Tree_Leaves',
        'Fern', 'Low_Shrub', 'Grass_Tuft', 'Broadleaf_Clump']
sources = {obj.name: obj for obj in dst.objects}
stone = [sources['Author_Slab_'+str(i)].data.materials[0] for i in range(1,5)]
with bpy.data.libraries.load(str(ROOT / 'art/source/world-blockout.blend'), link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n.startswith(('Continuous terrain','Plaza paving',
        'Arrival slope','Left path mouth','Canopy approach','Right branch'))]
verts, faces = [], []
for obj in dst.objects:
    offset = len(verts)
    verts.extend(obj.matrix_world @ v.co for v in obj.data.vertices)
    faces.extend(tuple(offset+i for i in p.vertices) for p in obj.data.polygons)
ground_bvh = BVHTree.FromPolygons(verts,faces)
def height_at(x,z):
    hit = ground_bvh.ray_cast(Vector((x,-z,25)),Vector((0,0,-1)))[0]
    assert hit is not None, 'Plant outside the hub terrain'
    return hit.z
moss = bpy.data.materials.new('Hub sheltered joints')
moss.diffuse_color = (.12, .155, .045, 1)
moss.use_nodes = True
moss.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = moss.diffuse_color
moss.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = .95

def mesh(name, verts, faces, material):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    data.materials.append(material)
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    return obj

def clip(poly, nx, ny, limit):
    result = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        da, db = nx*a[0] + ny*a[1] - limit, nx*b[0] + ny*b[1] - limit
        if da <= 0: result.append(a)
        if (da < 0 < db) or (db < 0 < da):
            t = da / (da - db)
            result.append((a[0] + t*(b[0]-a[0]), a[1] + t*(b[1]-a[1])))
    return result

def slab(poly, top, material):
    points = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        points.append(a)
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = math.hypot(dx, dy)
        if length > .4:
            for t in (.28, .58, .79):
                inset = rng.uniform(.006, .025)
                points.append((a[0]+t*dx-dy/length*inset, a[1]+t*dy+dx/length*inset))
    n = len(points)
    verts = [(x, y, z) for z in (-.03, top) for x, y in points]
    return mesh('Hub fractured flagstone', verts,
                [tuple(range(n, 2*n))] + [(i, (i+1)%n, (i+1)%n+n, i+n) for i in range(n)], material)

domain = [(12.78*math.cos(i*math.tau/96), 12.78*math.sin(i*math.tau/96)) for i in range(96)]
paving = [mesh('Hub joint bed', [(x, y, .005) for x, y in domain], [tuple(range(96))], moss)]
seeds = [(x*1.55+rng.uniform(-.20,.20), y*1.5+rng.uniform(-.17,.17))
         for y in range(-10,11) for x in range(-10,11) if math.hypot(x*1.55,y*1.5)<14.2]
slab_count = 0
for x, y in seeds:
    poly = domain[:]
    for ox, oy in seeds:
        if (x, y) == (ox, oy) or math.hypot(ox-x, oy-y) > 4: continue
        poly = clip(poly, ox-x, oy-y, (ox*ox+oy*oy-x*x-y*y)/2)
        if len(poly) < 3: break
    if len(poly) < 3: continue
    inset = poly[:]
    for a, b in zip(poly, poly[1:]+poly[:1]):
        nx, ny = b[1]-a[1], a[0]-b[0]
        inset = clip(inset, nx, ny, nx*a[0]+ny*a[1]-.024*math.hypot(nx, ny))
    if len(inset) < 3: continue
    # The existing corner surface sits above this thin paving layer. Its own
    # authored footprint remains intact while the surrounding plaza is dressed.
    slab_count += 1
    top = rng.uniform(.025,.055)
    paving.append(slab(inset, top, rng.choice(stone)))
    if (math.hypot(x,y)>4 and rng.random()<.55) or rng.random()<.10:
        a,b = rng.choice(list(zip(inset,inset[1:]+inset[:1])))
        cx,cy = (a[0]+b[0])/2,(a[1]+b[1])/2
        radius = rng.uniform(.28,.85)
        growth = [(cx+math.cos(i*math.tau/13)*radius*rng.uniform(.6,1.1),
                   cy+math.sin(i*math.tau/13)*radius*rng.uniform(.6,1.1)) for i in range(13)]
        for a,b in zip(inset,inset[1:]+inset[:1]):
            nx,ny = b[1]-a[1],a[0]-b[0]
            growth = clip(growth,nx,ny,nx*a[0]+ny*a[1])
        if len(growth)>2:
            paving.append(mesh('Sheltered stone-edge moss',[(px,py,top+.002) for px,py in growth],
                               [tuple(range(len(growth)))],moss))

# Close the plain connection between the existing corner and forest patch.
for row in range(9):
    z = -13.9-row*.94
    centre = -6-6*min(1,(-z-8)/14)
    for col in range(4):
        obj = bpy.data.objects.new('Hub approach paving',sources['Author_Slab_'+str(1+(row+col)%4)].data.copy())
        scene.collection.objects.link(obj)
        x = centre+(col-1.5)*1.12
        obj.location = (x,-z,height_at(x,z)-.075)
        obj.scale = (.93,)*3
        obj.rotation_euler.x = math.atan(.055)
        paving.append(obj)

# A shallow, interrupted inlay retains the circular motif without floating tubes.
for radius in (.7, 2.2, 4.1):
    for i in range(64):
        if rng.random() < .22: continue
        a, b = i*math.tau/64+.009, (i+1)*math.tau/64-.009
        verts = [(r*math.cos(t), r*math.sin(t), .058) for r,t in
                 [(radius-.035,a),(radius+.035,a),(radius+.035,b),(radius-.035,b)]]
        paving.append(mesh('Worn circular inlay', verts, [(0,1,2,3)], moss))

ruins = []
def block(x, z, base, width, depth, height, crown=False):
    # Unequal clipped corners and displaced courses break the regular box edge.
    c = rng.uniform(.035,.085)
    outline = [(-width/2+c,-depth/2),(width/2-c,-depth/2),(width/2,-depth/2+c),
               (width/2,depth/2-c),(width/2-c,depth/2),(-width/2+c,depth/2),
               (-width/2,depth/2-c),(-width/2,-depth/2+c)]
    verts = [(x+px,-z+py,base) for px,py in outline]
    verts += [(x+px+rng.uniform(-.035,.035),-z+py+rng.uniform(-.025,.025),
               base+max(.06,height-(rng.uniform(.02,.36) if crown else rng.uniform(0,.015)))) for px,py in outline]
    ruins.append(mesh('Weathered hub masonry',verts,[tuple(range(8,16))]+
                      [(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)],rng.choice(stone)))

columns = [(-10,7,4.2),(10,6,2.4),(-12,-3,2.2),(7,-9,4.8),
           (14,-9,2.6),(-15,-20,2.8),(-8,-27,2.3)]
for x,z,height in columns:
    block(x,z,0,2,2,.4)
    count = math.ceil(height/.65)
    for j in range(count):
        cap = j == count-1
        block(x+rng.uniform(-.05,.05),z+rng.uniform(-.025,.025),.4+j*.65,
              rng.uniform(.73,.95) if cap else 1.15,1.12,min(.63,height-j*.65),cap)

# Replace the eight established hub trees, preserving roots and trunk proxies.
trees, leaves = [], []
for kind, leaf_name, x, z, ground, height, yaw in [
        ('Tall','Tree_Tall_Leaves',-18,-2,.140054,12,.4),
        ('Broadleaf','Tree_Leaves',18,-4,.491365,13,-.6),
        ('Leaning','Tree_Leaning_Leaves',-17,-13,.980715,12,1.1),
        ('Broadleaf','Tree_Leaves',-17,9,.666705,13,2.3),
        ('Tall','Tree_Tall_Leaves',17,12,.590452,14,-1.8),
        ('Leaning','Tree_Leaning_Leaves',-23,2,1.532772,15,.8),
        ('Broadleaf','Tree_Leaves',23,5,.717884,16,-2.4),
        ('Tall','Tree_Tall_Leaves',-22,-12,1.022115,14,-.8)]:
    leaf_source = sources[leaf_name]
    scale = height/max(v.co.z for v in leaf_source.data.vertices)
    for name, group in [('Author_Tree_'+kind,trees),(leaf_name,leaves)]:
        obj = bpy.data.objects.new('Hub_'+name,sources[name].data.copy())
        scene.collection.objects.link(obj)
        obj.location = (x,-z,ground)
        obj.scale = (scale,)*3
        obj.rotation_euler.z = yaw
        group.append(obj)
    tree, leaf = trees[-1], leaves[-1]
    bpy.ops.object.select_all(action='DESELECT')
    tree.select_set(True)
    bpy.context.view_layer.objects.active = tree
    remesh = tree.modifiers.new('Fuse branch junctions','REMESH')
    remesh.mode = 'VOXEL'
    remesh.voxel_size = .065
    remesh.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    smooth = tree.modifiers.new('Smooth junctions','SMOOTH')
    smooth.factor = .6
    smooth.iterations = 3
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    decimate = tree.modifiers.new('Bound tree geometry','DECIMATE')
    decimate.ratio = .35
    bpy.ops.object.modifier_apply(modifier=decimate.name)
    tree.data.validate(clean_customdata=True)
    tree.data.update()
    # The kit's eight-triangle leaf fans can use six triangles without changing
    # their silhouettes. Keep one tint per leaf and avoid duplicating centre verts.
    old = leaf.data
    if len(old.vertices)%9==0 and len(old.polygons)==len(old.vertices)//9*8:
        count = len(old.vertices)//9
        tints = [tuple(old.color_attributes.active_color.data[old.polygons[i*8].loop_start].color) for i in range(count)]
        data = bpy.data.meshes.new('Hub economical leaf outlines')
        data.from_pydata([tuple(old.vertices[i*9+j].co) for i in range(count) for j in range(1,9)],[],
                         [tuple(range(i*8,i*8+8)) for i in range(count)])
        for mat in old.materials: data.materials.append(mat)
        attr = data.color_attributes.new(name='FoliageColor',type='BYTE_COLOR',domain='CORNER')
        for poly in data.polygons:
            poly.use_smooth = True
            for i in poly.loop_indices: attr.data[i].color = tints[poly.index]
        data.update()
        leaf.data = data
    colors = leaf.data.color_attributes.active_color
    low = min(v.co.z for v in leaf.data.vertices)
    span = max(v.co.z for v in leaf.data.vertices)-low
    for poly in leaf.data.polygons:
        for i in poly.loop_indices:
            v = leaf.data.vertices[leaf.data.loops[i].vertex_index]
            factor = .48+.52*(v.co.z-low)/max(span,.01)
            c = colors.data[i].color
            colors.data[i].color = (c[0]*factor,c[1]*factor,c[2]*factor,1)

# Ground cover uses four exported prototypes, not hundreds of duplicate meshes.
plant_rng = random.Random(2409)
plant_casters, plant_markers, plant_prototypes = [], [], []
families = ['Fern','Low_Shrub','Grass_Tuft','Broadleaf_Clump']
for family in families:
    obj = bpy.data.objects.new('HubPlantPrototype_'+family,sources[family].data.copy())
    scene.collection.objects.link(obj)
    obj.hide_render = True
    plant_prototypes.append(obj)
for cluster in range(32):
    angle = cluster*2.399
    radius = plant_rng.uniform(13.4,23)
    cx,cz = math.cos(angle)*radius,math.sin(angle)*radius
    if cluster<7:
        cx,cz,_ = columns[cluster]
        cx += 1.3
    for j in range(5):
        x,z = cx+plant_rng.uniform(-1.7,1.7),cz+plant_rng.uniform(-1.7,1.7)
        # Keep the arrival and both route mouths readable at player height.
        left = -6-6*min(1,max(0,(-z-8)/14))
        right = 8+.9*(-z-5)
        if (abs(x)<4 and z>8) or (-23<z<-8 and abs(x-left)<2.9) or (-20<z<-4 and abs(x-right)<3): continue
        family = families[(cluster+j)%4]
        plant = bpy.data.objects.new('Hub plant caster',sources[family].data.copy())
        scene.collection.objects.link(plant)
        plant.location = (x,-z,height_at(x,z)+.025)
        size = plant_rng.uniform(.8,1.7) if family=='Low_Shrub' else plant_rng.uniform(.6,1.2)
        plant.scale = (size,)*3
        plant.rotation_euler.z = plant_rng.uniform(0,math.tau)
        plant_casters.append(plant)
        marker = bpy.data.objects.new('HubPlant_'+family+'_'+str(len(plant_markers)).zfill(3),None)
        scene.collection.objects.link(marker)
        marker.location,marker.scale,marker.rotation_euler = plant.location.copy(),plant.scale.copy(),plant.rotation_euler.copy()
        plant_markers.append(marker)

# Reuse the corner's raw authoring objects, not its old illuminated texture.
# Translation happens before the bake so shadows agree across the whole junction.
floor_prefix = ('Fractured limestone slab','Eroded seam bed','Joint edge moss')
architecture_prefix = ('Eroded wall course','Moss on sheltered wall ledge','Column plinth',
    'Column course','Fractured column crown','Column base moss','Rooted tree','Buttress root',
    'Spreading branch','Leaf-bearing twig','Upper crown fork','Fallen wall stone')
with bpy.data.libraries.load(str(ROOT/'art/source/hub-corner.blend'),link=False) as (src,dst):
    dst.objects = [n for n in src.objects if n.startswith(floor_prefix+architecture_prefix) or n=='Corner_Foliage']
corner_paving,corner_stone = [],[]
for obj in dst.objects:
    scene.collection.objects.link(obj)
    obj.hide_set(False)
    obj.hide_render = False
    obj.location += Vector((-8,9,0))
    if obj.name.startswith(floor_prefix): corner_paving.append(obj)
    elif obj.name.startswith(architecture_prefix): corner_stone.append(obj)
assert corner_paving and corner_stone, 'Corner authoring source is required'

# Preserve originals for future contextual rebakes and manual authoring.
author = bpy.data.collections.new('Hub editable stonework')
scene.collection.children.link(author)
for obj in paving+ruins+trees+corner_paving+corner_stone:
    for collection in list(obj.users_collection): collection.objects.unlink(obj)
    author.objects.link(obj)
targets = []
for name, objects, size in [('HubArt_Paving',paving,2048),('HubArt_Ruins',ruins,1024),
                            ('HubArt_Trees',trees,2048),('HubArt_CornerPaving',corner_paving,2048),
                            ('HubArt_CornerStone',corner_stone,1024)]:
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects: obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.duplicate()
    bpy.ops.object.join()
    target = bpy.context.object
    target.name = name
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.004)
    bpy.ops.object.mode_set(mode='OBJECT')
    atlas = bpy.data.images.new(name+' placed diffuse',width=size,height=size,alpha=False)
    atlas.filepath_raw = str(OUT / (name+'-atlas.png'))
    atlas.file_format = 'PNG'
    for i, original in enumerate(list(target.data.materials)):
        mat = original.copy()
        target.data.materials[i] = mat
        node = mat.node_tree.nodes.new('ShaderNodeTexImage')
        node.image = atlas
        mat.node_tree.nodes.active = node
    targets.append((target,atlas))
for obj in paving+ruins+trees+corner_paving+corner_stone:
    obj.hide_render = True
    obj.hide_set(True)
scene.render.bake.use_pass_color = True
scene.render.bake.use_pass_direct = True
scene.render.bake.use_pass_indirect = True
scene.render.bake.margin = 6
for target, atlas in targets:
    bpy.ops.object.select_all(action='DESELECT')
    target.select_set(True)
    bpy.context.view_layer.objects.active = target
    print('BAKING '+target.name,flush=True)
    bpy.ops.object.bake(type='DIFFUSE')
    atlas.save()
    atlas.pack()
for target, atlas in targets:
    mat = bpy.data.materials.new(target.name+' diffuse')
    mat.use_nodes = True
    tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image = atlas
    mat.node_tree.links.new(tex.outputs['Color'],mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    target.data.materials.clear()
    target.data.materials.append(mat)
    for poly in target.data.polygons: poly.material_index = 0
bpy.ops.object.select_all(action='DESELECT')
for leaf in leaves: leaf.select_set(True)
bpy.context.view_layer.objects.active = leaves[0]
bpy.ops.object.join()
foliage = bpy.context.object
foliage.name = 'HubArt_Foliage'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
leaf_material = bpy.data.materials.new('HubArt leaf colour')
leaf_material.use_nodes = True
colour = leaf_material.node_tree.nodes.new('ShaderNodeVertexColor')
colour.layer_name = foliage.data.color_attributes.active_color.name
leaf_material.node_tree.links.new(colour.outputs['Color'],leaf_material.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
foliage.data.materials.clear()
foliage.data.materials.append(leaf_material)
for poly in foliage.data.polygons: poly.material_index = 0
for target,_ in targets: target.select_set(True)
for obj in plant_prototypes+plant_markers: obj.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'art/source/hub-art.blend'),compress=True)
export = ROOT / 'public/models/hub-art.glb'
bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=True,
                          export_image_format='JPEG',export_image_quality=94)
sys.path.insert(0,str(Path(__file__).parent))
from world_art_context import export_context
removed = export_context(include_hub=True)
report = {'stage':'hub vegetation, planted paving and unified corner lighting','slabs':slab_count,'columns':len(columns),
          'trees':len(trees),'groundCover':len(plant_markers),'approachSlabs':36,
          'bytes':export.stat().st_size,'atlases':[2048,1024,2048,2048,1024],'seconds':round(time.monotonic()-started,1),
          'removedContextProxies':removed}
(OUT/'hub-art-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('HUB_ART '+json.dumps(report),flush=True)
