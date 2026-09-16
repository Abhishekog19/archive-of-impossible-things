"""Reusable Phase B prototypes from the authored corner; never modifies its source.

Native metres, Z-up, bottom-centred pivots. Shared directional preview atlases
prove export; placed production zones must receive their own contextual bake.
"""
import bpy
import math
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
for i in range(3):
    block=combine('Masonry_'+str(i+1),[blocks[i*7]])
    if i>0: block.data.materials[0]=bpy.data.materials['Warm limestone '+str(i)]
    register(block,'Stone',True)
register(combine('Column_Broken',[o for n,o in sources.items() if n.startswith(('Column course','Column plinth','Fractured column crown'))]),'Stone',True)

# Arch: distinct wedge stones and plinths, with a broad four-metre clear opening.
archparts=[];archcollision=[]
mat=blocks[0].data.materials[0]
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
for i,suffix in enumerate(('.001','.004')):
    register(combine('Root_'+str(i+1),[sources['Buttress root'+suffix]]),'Wood')

# Keep the proven opaque leaf geometry/vertex tints, with no alpha overdraw.
for source,name,pivot in [('Corner_Foliage','Tree_Leaves',(3,3,0)),('FernPrototype','Fern',(0,0,0))]:
    original=sources[source]
    o=bpy.data.objects.new(name,original.data.copy());scene.collection.objects.link(o)
    o.data.transform(Matrix.Translation(-Vector(pivot))@original.matrix_world)
    o.location=(180,0,0)  # Out of the atlas bake; reset before export.
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
          'extras':['Tree_Leaves','Fern'],'atlasSizes':[2048,1024],
          'glbBytes':export.stat().st_size,'seconds':round(time.monotonic()-started,1)}
(ROOT/'src/config/asset-kit.json').write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'kit-report.json').write_text(json.dumps(manifest,indent=2))
print('KIT_EXPORTED '+json.dumps(manifest),flush=True)
