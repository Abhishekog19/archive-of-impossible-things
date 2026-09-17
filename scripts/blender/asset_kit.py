"""Reusable Phase B prototypes from the authored corner; never modifies its source.

Native metres, Z-up, bottom-centred pivots. Shared directional preview atlases
prove export; placed production zones must receive their own contextual bake.
"""
import bpy
import math
import random
import json
import time
from pathlib import Path
from mathutils import Vector, Matrix

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'.artifacts/blender'
started=time.monotonic()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
prefixes=('Fractured limestone slab','Eroded wall course','Column course',
          'Column plinth','Fractured column crown','Rooted tree','Spreading branch',
          'Leaf-bearing twig','Upper crown fork','Buttress root','Corner_Foliage','FernPrototype')
with bpy.data.libraries.load(str(ROOT/'art/source/hub-corner.blend'),link=False) as (src,dst):
    dst.objects=[n for n in src.objects if n.startswith(prefixes)]
sources={o.name:o for o in dst.objects}
scene=bpy.context.scene
for o in sources.values():
    scene.collection.objects.link(o)
    o.hide_render=True
    o.hide_set(True)
bpy.context.view_layer.update()
scene.unit_settings.system='METRIC'
scene.render.engine='CYCLES'
scene.cycles.device='CPU'
scene.cycles.samples=24
scene.cycles.max_bounces=2
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.48,.60,.72,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.40
bpy.ops.object.light_add(type='SUN',location=(6,-8,12))
sun=bpy.context.object
sun.data.energy=2.1
sun.data.color=(1,.91,.77)
sun.data.angle=.07
sun.rotation_euler=Vector((-6,8,-12)).to_track_quat('-Z','Y').to_euler()
assets=[]
exports=[]
colliders=[]

def patchy_stone(name, amount, seed):
    """Broad damp islands, baked once; avoid identical vertical moss stripes."""
    material=bpy.data.materials['Warm limestone 1'].copy()
    material.name=name
    nodes,links=material.node_tree.nodes,material.node_tree.links
    shader=nodes.get('Principled BSDF')
    base=shader.inputs['Base Color'].links[0].from_socket
    geometry=nodes.new('ShaderNodeNewGeometry')
    offset=nodes.new('ShaderNodeVectorMath');offset.operation='ADD'
    offset.inputs[1].default_value=(seed*3.7,seed*1.9,0)
    links.new(geometry.outputs['Position'],offset.inputs[0])
    noise=nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value=2.2
    noise.inputs['Detail'].default_value=2.5
    links.new(offset.outputs[0],noise.inputs['Vector'])
    islands=nodes.new('ShaderNodeMapRange')
    islands.inputs['From Min'].default_value=.43
    islands.inputs['From Max'].default_value=.67
    links.new(noise.outputs['Fac'],islands.inputs['Value'])
    height=nodes.new('ShaderNodeSeparateXYZ')
    links.new(geometry.outputs['Position'],height.inputs[0])
    damp=nodes.new('ShaderNodeMapRange')
    damp.inputs['From Min'].default_value=.1
    damp.inputs['From Max'].default_value=2.4
    damp.inputs['To Min'].default_value=amount
    damp.inputs['To Max'].default_value=.025
    links.new(height.outputs['Z'],damp.inputs['Value'])
    mask=nodes.new('ShaderNodeMath');mask.operation='MULTIPLY'
    links.new(islands.outputs['Result'],mask.inputs[0])
    links.new(damp.outputs['Result'],mask.inputs[1])
    mix=nodes.new('ShaderNodeMixRGB')
    mix.inputs[2].default_value=(.10,.145,.05,1)
    links.new(mask.outputs[0],mix.inputs[0]);links.new(base,mix.inputs[1])
    links.new(mix.outputs[0],shader.inputs['Base Color'])
    return material

stone_variants=[patchy_stone('Kit damp stone '+str(i),amount,i)
                for i,amount in enumerate((.92,.10,.48,.30))]

def combine(name, objects, pivot=None):
    verts=[];faces=[];indices=[];mats=[];smooth=[]
    for o in objects:
        start=len(verts)
        verts.extend(tuple(o.matrix_world@v.co) for v in o.data.vertices)
        mapping=[]
        for mat in o.data.materials:
            if mat not in mats: mats.append(mat)
            mapping.append(mats.index(mat))
        for p in o.data.polygons:
            faces.append(tuple(start+i for i in p.vertices))
            indices.append(mapping[p.material_index] if mapping else 0)
            smooth.append(p.use_smooth)
    low=Vector(tuple(min(v[i] for v in verts) for i in range(3)))
    high=Vector(tuple(max(v[i] for v in verts) for i in range(3)))
    pivot=Vector(pivot) if pivot is not None else Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata([tuple(Vector(v)-pivot) for v in verts],[],faces)
    mesh.update()
    for mat in mats: mesh.materials.append(mat)
    for p,index,shading in zip(mesh.polygons,indices,smooth):
        p.material_index=index;p.use_smooth=shading
    o=bpy.data.objects.new(name,mesh)
    scene.collection.objects.link(o)
    return o

def bounds(o):
    return [[min(v.co[i] for v in o.data.vertices) for i in range(3)],
            [max(v.co[i] for v in o.data.vertices) for i in range(3)]]

def register(o,family,collision=False):
    index=len(assets)
    # Isolate prototypes so one asset cannot cast onto another's reusable atlas.
    o.location=(index%5*15,index//5*15,0)
    low,high=bounds(o)
    assets.append({'name':o.name,'object':o,'family':family,'bounds': [low,high]})
    if collision:
        bpy.ops.mesh.primitive_cube_add(size=1)
        c=bpy.context.object;c.name='Collider_'+o.name
        if o.name.startswith('Tree'):
            c.scale=(.85,.85,4);c.location=(0,0,2)
        else:
            c.scale=tuple(high[i]-low[i] for i in range(3))
            c.location=tuple((high[i]+low[i])/2 for i in range(3))
        bpy.ops.object.transform_apply(location=True,rotation=False,scale=True)
        c.hide_render=True;c.hide_set(True);colliders.append(c)
    return o

slabs=sorted((o for n,o in sources.items() if n.startswith('Fractured limestone slab')),
             key=lambda o:sum(p.area for p in o.data.polygons),reverse=True)
for i,o in enumerate(slabs[:6]): register(combine('Slab_'+str(i+1),[o]),'Stone')
blocks=sorted((o for n,o in sources.items() if n.startswith('Eroded wall course')),key=lambda o:o.name)
for i in range(4):
    block=combine('Masonry_'+str(i+1),[blocks[(i*7)%len(blocks)]])
    if i==3:
        # A sloping broken cap changes the wall outline without extra debris.
        for vertex in block.data.vertices:
            if vertex.co.z>.25:
                vertex.co.z-=max(0,vertex.co.y+.2)*.28
        block.data.update()
    for slot in range(len(block.data.materials)):
        block.data.materials[slot]=stone_variants[i]
    register(block,'Stone',True)
column=combine('Column_Broken',[o for n,o in sources.items() if n.startswith(('Column course','Column plinth','Fractured column crown'))])
for slot in range(len(column.data.materials)): column.data.materials[slot]=stone_variants[0]
register(column,'Stone',True)

# Arch: distinct wedge stones and plinths, with a broad four-metre clear opening.
archparts=[]
mat=stone_variants[2]
for side in (-1,1):
    for row in range(6):
        bpy.ops.mesh.primitive_cube_add(size=1,location=(side*2.32,0,.25+row*.48))
        p=bpy.context.object;p.scale=(.64,.85,.46)
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        p.data.materials.append(mat)
        archparts.append(p)
for i in range(11):
    a=(i+.025)*math.pi/11;b=(i+.975)*math.pi/11
    pts=[(r*math.cos(t),y,2.88+r*math.sin(t)) for y in (-.425,.425)
         for r,t in ((2,a),(2,b),(2.66,b),(2.66,a))]
    data=bpy.data.meshes.new('Wedge')
    data.from_pydata(pts,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
    data.materials.append(mat)
    p=bpy.data.objects.new('Wedge',data);scene.collection.objects.link(p);archparts.append(p)
arch=combine('Arch_Ruin',archparts,pivot=(0,0,0))
c=arch.copy();c.data=arch.data.copy();c.name='Collider_Arch_Ruin';scene.collection.objects.link(c)
c.data.materials.clear();c.hide_render=True;c.hide_set(True);colliders.append(c)
for p in archparts: bpy.data.objects.remove(p,do_unlink=True)
bpy.context.view_layer.objects.active=arch
mod=arch.modifiers.new('Worn wedge edges','BEVEL');mod.width=.028;mod.segments=1
bpy.ops.object.modifier_apply(modifier=mod.name)
register(arch,'Stone')

wood=[o for n,o in sources.items() if n.startswith(('Rooted tree','Spreading branch','Leaf-bearing twig','Upper crown fork','Buttress root'))]
register(combine('Tree_Broadleaf',wood,pivot=(3,3,0)),'Wood',True)

def shape_tree(mesh, variant):
    """Deform wood and attached leaves together, keeping the root origin fixed."""
    for vertex in mesh.vertices:
        x,y,z=vertex.co
        height=max(0,z)/8
        crown=max(0,min(1,(z-3)/4))
        if variant=='Tall':
            # Raised, narrow crown and an S-shaped leader for the forest approach.
            angle=.28*crown
            spread=.74-.18*crown
            vertex.co=(spread*(x*math.cos(angle)-y*math.sin(angle))+.22*math.sin(height*math.pi),
                       spread*(x*math.sin(angle)+y*math.cos(angle)),z*1.30)
        else:
            # Low spreading crown, leaning upper trunk and unequal lateral growth.
            spread=1+.24*crown
            vertex.co=(x*spread+1.45*height*height,
                       y*(.92+.15*crown)+.30*height*height,z*.88+.09*x*crown)
    mesh.update()

for variant in ('Tall','Leaning'):
    tree=combine('Tree_'+variant,wood,pivot=(3,3,0))
    shape_tree(tree.data,variant)
    register(tree,'Wood',True)
    shape_tree(colliders[-1].data,variant)
for i,suffix in enumerate(('.001','.004')):
    register(combine('Root_'+str(i+1),[sources['Buttress root'+suffix]]),'Wood')

# Keep the proven opaque leaf geometry/vertex tints, with no alpha overdraw.
for source,name,pivot in [('Corner_Foliage','Tree_Leaves',(3,3,0)),('FernPrototype','Fern',(0,0,0))]:
    original=sources[source]
    o=bpy.data.objects.new(name,original.data.copy());scene.collection.objects.link(o)
    o.data.transform(Matrix.Translation(-Vector(pivot))@original.matrix_world)
    o.location=(180,0,0)  # Out of the atlas bake; reset before export.
    exports.append(o)

def ground_cover(name, kind, seed):
    rng=random.Random(seed)
    verts=[];faces=[];tints=[]
    count={'Grass_Tuft':15,'Broadleaf_Clump':11,'Low_Shrub':28}[name]
    for i in range(count):
        angle=i*2.399+rng.uniform(-.3,.3)
        axis=Vector((math.cos(angle),math.sin(angle),0))
        side=Vector((-axis.y,axis.x,0))
        if kind=='grass':
            base=axis*rng.uniform(.015,.10)
            height=rng.uniform(.25,.62);reach=rng.uniform(.10,.30)
            middle=base+axis*reach*.3+Vector((0,0,height*.65))
            tip=base+axis*reach+Vector((0,0,height))
            width=rng.uniform(.018,.035)
            points=[base-side*width,middle-side*width*.6,tip,
                    middle+side*width*.6,base+side*width]
            local_faces=[(0,1,4),(1,3,4),(1,2,3)]
        else:
            reach=rng.uniform(.24,.52) if kind=='broadleaf' else rng.uniform(.20,.43)
            height=rng.uniform(.12,.32) if kind=='broadleaf' else rng.uniform(.20,.68)
            base=axis*rng.uniform(.01,.07)
            if kind=='shrub': base+=axis*rng.uniform(.03,.16)+Vector((0,0,height*.35))
            middle=base+axis*reach*.5+Vector((0,0,height))
            tip=base+axis*reach+Vector((0,0,height*.60))
            width=reach*(.28 if kind=='broadleaf' else .22)
            points=[base,middle-side*width,middle+Vector((0,0,.035)),
                    tip,middle+side*width]
            local_faces=[(0,1,2),(1,3,2),(3,4,2),(4,0,2)]
        start=len(verts);verts.extend(tuple(p) for p in points)
        faces.extend(tuple(start+j for j in face) for face in local_faces)
        tints.extend([rng.uniform(.72,1.1)]*len(local_faces))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    mesh.materials.append(sources['FernPrototype'].data.materials[0])
    colors=mesh.color_attributes.new(name='FoliageColor',type='BYTE_COLOR',domain='CORNER')
    base=(.12,.18,.055) if kind=='grass' else (.075,.145,.035)
    for poly,tint in zip(mesh.polygons,tints):
        for index in poly.loop_indices: colors.data[index].color=(*(c*tint for c in base),1)
    obj=bpy.data.objects.new(name,mesh);scene.collection.objects.link(obj)
    obj.location=(180,0,0);exports.append(obj)

for name,kind,seed in [('Grass_Tuft','grass',171),('Broadleaf_Clump','broadleaf',172),
                       ('Low_Shrub','shrub',173)]:
    ground_cover(name,kind,seed)

leaves=next(o for o in exports if o.name=='Tree_Leaves')
for variant in ('Tall','Leaning'):
    o=bpy.data.objects.new('Tree_'+variant+'_Leaves',leaves.data.copy())
    scene.collection.objects.link(o)
    shape_tree(o.data,variant)
    o.location=(180,0,0)
    exports.append(o)

for family,res in [('Stone',2048),('Wood',1024)]:
    bpy.context.view_layer.update()
    members=[a for a in assets if a['family']==family]
    spans=[];v=0;p=0
    for a in members:
        o=a['object'];spans.append((a,v,len(o.data.vertices),p,len(o.data.polygons)))
        v+=len(o.data.vertices);p+=len(o.data.polygons)
    target=combine('Bake_'+family,[a['object'] for a in members],pivot=(0,0,0))
    for a in members: a['object'].hide_render=True;a['object'].hide_set(True)
    bpy.ops.object.select_all(action='DESELECT');target.select_set(True)
    bpy.context.view_layer.objects.active=target
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.008)
    bpy.ops.object.mode_set(mode='OBJECT')
    atlas=bpy.data.images.new('Kit_'+family,width=res,height=res,alpha=False)
    atlas.filepath_raw=str(OUT/('kit-'+family+'.png'));atlas.file_format='PNG'
    for j,mat in enumerate(list(target.data.materials)):
        copy=mat.copy();target.data.materials[j]=copy
        node=copy.node_tree.nodes.new('ShaderNodeTexImage');node.image=atlas
        copy.node_tree.nodes.active=node
    scene.render.bake.use_pass_direct=True;scene.render.bake.use_pass_indirect=True
    scene.render.bake.use_pass_color=True;scene.render.bake.margin=8
    print('BAKING_KIT '+family,flush=True)
    bpy.ops.object.bake(type='DIFFUSE');atlas.save();atlas.pack()
    material=bpy.data.materials.new('Kit_'+family);material.use_nodes=True
    nodes=material.node_tree.nodes
    texture=nodes.new('ShaderNodeTexImage');texture.image=atlas
    material.node_tree.links.new(texture.outputs['Color'],nodes['Principled BSDF'].inputs['Base Color'])
    for a,first,count,start,polys in spans:
        offset=a['object'].location.copy()
        verts=[tuple(target.data.vertices[i].co-offset) for i in range(first,first+count)]
        faces=[tuple(i-first for i in poly.vertices) for poly in target.data.polygons[start:start+polys]]
        data=bpy.data.meshes.new(a['name']+'_Runtime');data.from_pydata(verts,[],faces);data.update()
        uv=data.uv_layers.new(name='UVMap')
        for dest,source in zip(data.polygons,target.data.polygons[start:start+polys]):
            dest.use_smooth=source.use_smooth
            for dl,sl in zip(dest.loop_indices,source.loop_indices):
                uv.data[dl].uv=target.data.uv_layers.active.data[sl].uv
        data.materials.append(material)
        a['object'].name='Author_'+a['name']
        o=bpy.data.objects.new(a['name'],data);scene.collection.objects.link(o);exports.append(o)
        o.hide_render=True # Keep later atlas bakes free of exported duplicates.
    bpy.data.objects.remove(target,do_unlink=True)

bpy.ops.object.select_all(action='DESELECT')
for o in exports+colliders:
    o.location=(0,0,0);o.hide_set(False);o.select_set(True)
    if o in exports: o.hide_render=False
source=ROOT/'art/source/archive-kit.blend';export=ROOT/'public/models/archive-kit.glb'
bpy.ops.wm.save_as_mainfile(filepath=str(source),compress=True)
bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=True,
                          export_image_format='JPEG',export_image_quality=90)
manifest={'version':1,'units':'metres','pivot':'bottom-centre, except tree trunk origin',
          'previewLighting':'Directional diffuse preview only; rebake assembled zones before final delivery.',
          'assets':[{'name':a['name'],'family':a['family'],'boundsBlender':a['bounds']} for a in assets],
          'extras':['Tree_Leaves','Tree_Tall_Leaves','Tree_Leaning_Leaves','Fern',
                    'Grass_Tuft','Broadleaf_Clump','Low_Shrub'],
          'groundCover':['Fern','Grass_Tuft','Broadleaf_Clump','Low_Shrub'],
          'treeVariants':['Tree_Broadleaf','Tree_Tall','Tree_Leaning'],'atlasSizes':[2048,1024],
          'glbBytes':export.stat().st_size,'seconds':round(time.monotonic()-started,1)}
(ROOT/'src/config/asset-kit.json').write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'kit-report.json').write_text(json.dumps(manifest,indent=2))
print('KIT_EXPORTED '+json.dumps(manifest),flush=True)
