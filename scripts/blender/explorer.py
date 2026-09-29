"""Original Archive explorer: metre-scale skinned mesh and authored in-place clips.

No downloaded model, rig, animation or texture. Blender -Y faces forward; glTF +Z.
Rebuilding overwrites only explorer.blend, explorer.glb and its generated manifest.
"""
import bpy
import math
import json
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.artifacts/blender'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.fps = 30

# Linear RGB, chosen for the natural material palette rather than luminous colour.
COL = {'coat': (.16,.22,.105), 'seam': (.28,.34,.19), 'scarf': (.48,.29,.105),
       'leather': (.12,.065,.035), 'sole': (.036,.029,.022), 'trouser': (.075,.10,.065),
       'skin': (.48,.29,.17), 'hair': (.055,.032,.021), 'eye': (.018,.021,.017),
       'linen': (.46,.44,.31), 'brass': (.32,.23,.10)}
parts = []
mat = bpy.data.materials.new('Explorer natural cloth and leather')
mat.use_nodes = True
attr = mat.node_tree.nodes.new('ShaderNodeVertexColor'); attr.layer_name = 'ExplorerColour'
bsdf = mat.node_tree.nodes.get('Principled BSDF')
mat.node_tree.links.new(attr.outputs['Color'],bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value = .88

def finish(obj, name, colour, bone):
    obj.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.data.materials.clear(); obj.data.materials.append(mat)
    colours = obj.data.color_attributes.new(name='ExplorerColour',type='BYTE_COLOR',domain='CORNER')
    for poly in obj.data.polygons:
        # Quiet plane variation, with no world-light bake on an animated character.
        shade = .94 + .06 * max(0,poly.normal.z)
        for li in poly.loop_indices: colours.data[li].color = (*[c*shade for c in COL[colour]],1)
    group = obj.vertex_groups.new(name=bone)
    group.add(list(range(len(obj.data.vertices))),1,'REPLACE')
    parts.append(obj)
    return obj

def ellipsoid(name, centre, scale, colour, bone, segments=12, rings=8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=centre)
    obj=bpy.context.object; obj.scale=scale
    for p in obj.data.polygons:p.use_smooth=True
    return finish(obj,name,colour,bone)

def box(name, centre, scale, colour, bone, bevel=.015):
    bpy.ops.mesh.primitive_cube_add(size=1,location=centre)
    obj=bpy.context.object; obj.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    mod=obj.modifiers.new('Soft worn edges','BEVEL');mod.width=bevel;mod.segments=2
    bpy.ops.object.modifier_apply(modifier=mod.name)
    return finish(obj,name,colour,bone)

def link(name, a, b, radius, colour, bone, radius2=None):
    av,bv=Vector(a),Vector(b); vec=bv-av
    bpy.ops.mesh.primitive_cone_add(vertices=10,radius1=radius,radius2=radius2 or radius,
        depth=vec.length,location=(av+bv)/2)
    obj=bpy.context.object;obj.rotation_euler=vec.to_track_quat('Z','Y').to_euler()
    return finish(obj,name,colour,bone)

def loft(name, rings, colour, bone):
    vertices=[]
    for z,rx,ry in rings:
        vertices.extend((rx*math.cos(i*math.tau/12),ry*math.sin(i*math.tau/12),z) for i in range(12))
    faces=[tuple(range(11,-1,-1))]
    for row in range(len(rings)-1):
        for i in range(12):
            j=(i+1)%12; a=row*12
            faces.append((a+i,a+j,a+12+j,a+12+i))
    faces.append(tuple(range((len(rings)-1)*12,len(rings)*12)))
    data=bpy.data.meshes.new(name);data.from_pydata(vertices,[],faces);data.update()
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active=obj;obj.select_set(True)
    return finish(obj,name,colour,bone)

loft('Travelling coat',[(.86,.20,.135),(1.02,.165,.12),(1.24,.21,.14),(1.36,.205,.115)],'coat','Spine')
loft('Split coat hem',[(.76,.22,.15),(.88,.20,.14),(.99,.17,.12)],'coat','Hips')
loft('Leather waist belt',[(.98,.175,.128),(1.02,.176,.129)],'leather','Hips')
box('Belt buckle',(0,-.133,1.0),(.06,.012,.04),'brass','Hips',.005)
box('Linen shirt opening',(0,-.123,1.30),(.082,.02,.15),'linen','Spine',.005)
for x in (-.045,.045):link('Coat placket',(x,-.142,1.06),(x,-.144,1.25),.008,'seam','Spine')
for z in (1.08,1.16,1.23):ellipsoid('Wood toggle',(0,-.149,z),(.018,.008,.009),'leather','Spine',8,4)

# Narrow neck, readable face and overlapping hair masses, not a featureless helmet.
link('Neck',(0,0,1.34),(0,0,1.45),.061,'skin','Neck')
ellipsoid('Face',(0,-.006,1.525),(.113,.097,.139),'skin','Head',16,10)
ellipsoid('Hair cap',(0,.012,1.62),(.122,.101,.08),'hair','Head',14,8)
for x in (-.078,-.028,.033,.083):
    ellipsoid('Swept fringe',(x,-.072,1.634-abs(x)*.16),(.047,.039,.043),'hair','Head',8,6)
for side in (-1,1):
    ellipsoid('Ear',(side*.11,0,1.515),(.02,.023,.033),'skin','Head',8,6)
    ellipsoid('Eye',(side*.044,-.097,1.546),(.009,.005,.012),'eye','Head',8,4)
    link('Brow',(side*.026,-.099,1.568),(side*.064,-.092,1.569),.005,'hair','Head')
ellipsoid('Nose',(0,-.107,1.513),(.016,.022,.025),'skin','Head',8,6)
link('Mouth',(-.025,-.099,1.478),(.025,-.099,1.478),.003,'leather','Head')
loft('Woven scarf collar',[(1.34,.115,.105),(1.39,.12,.105),(1.42,.087,.075)],'scarf','Neck')
box('Scarf tail',(.075,-.152,1.235),(.075,.025,.25),'scarf','Spine',.008)

# A small rear satchel and shoulder strap give the third-person silhouette a purpose.
box('Satchel',(0,.176,1.18),(.235,.13,.25),'leather','Spine',.027)
box('Satchel flap',(0,.25,1.235),(.24,.017,.10),'scarf','Spine',.013)
box('Satchel clasp',(0,.264,1.215),(.025,.012,.04),'brass','Spine',.004)
for x in (-.104,.104):link('Satchel straps',(x,-.132,1.11),(x,-.118,1.37),.018,'leather','Spine')

for side,label in [(-1,'L'),(1,'R')]:
    shoulder=(side*.218,0,1.315); elbow=(side*.29,0,1.08); wrist=(side*.305,-.015,.885)
    ellipsoid('Shoulder sleeve',shoulder,(.083,.095,.095),'coat','UpperArm_'+label)
    link('Sleeve',shoulder,elbow,.074,'coat','UpperArm_'+label,.06)
    ellipsoid('Elbow',elbow,(.064,.066,.066),'coat','Forearm_'+label)
    link('Fore sleeve',elbow,wrist,.06,'coat','Forearm_'+label,.044)
    link('Leather cuff',(side*.303,-.013,.918),wrist,.048,'leather','Forearm_'+label)
    ellipsoid('Hand',(side*.305,-.018,.852),(.042,.034,.06),'skin','Hand_'+label,10,6)
    hip=(side*.098,0,.86);knee=(side*.105,0,.475);ankle=(side*.105,0,.155)
    link('Trouser thigh',hip,knee,.088,'trouser','Thigh_'+label,.073)
    ellipsoid('Knee',knee,(.074,.068,.078),'trouser','Shin_'+label,10,6)
    link('Trouser shin',knee,ankle,.069,'trouser','Shin_'+label,.051)
    link('Boot shaft',(side*.105,0,.12),(side*.105,0,.29),.062,'leather','Shin_'+label)
    box('Boot',(side*.105,-.057,.072),(.143,.24,.115),'leather','Foot_'+label,.032)
    box('Boot sole',(side*.105,-.057,.017),(.151,.249,.034),'sole','Foot_'+label,.009)
    for z in (.12,.15,.18):link('Boot lace',(side*.105-.04,-.060,z),(side*.105+.04,-.060,z),.004,'scarf','Foot_'+label)

# One draw call / one skin. Every component has explicit weights retained on join.
bpy.ops.object.select_all(action='DESELECT')
for obj in parts:obj.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.join();mesh=bpy.context.object;mesh.name='Explorer'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)

arm=bpy.data.armatures.new('ExplorerRig');rig=bpy.data.objects.new('ExplorerRig',arm)
bpy.context.collection.objects.link(rig)
bpy.context.view_layer.objects.active=rig;rig.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
def bone(name,head,tail,parent=None):
    b=arm.edit_bones.new(name);b.head=head;b.tail=tail
    if parent:b.parent=arm.edit_bones[parent]
    return b
bone('Root',(0,0,0),(0,0,.2))
bone('Hips',(0,0,.86),(0,0,1.02),'Root')
bone('Spine',(0,0,1.02),(0,0,1.34),'Hips')
bone('Neck',(0,0,1.34),(0,0,1.43),'Spine')
bone('Head',(0,0,1.43),(0,0,1.68),'Neck')
for side,label in [(-1,'L'),(1,'R')]:
    bone('UpperArm_'+label,(side*.218,0,1.315),(side*.29,0,1.08),'Spine')
    bone('Forearm_'+label,(side*.29,0,1.08),(side*.305,-.015,.885),'UpperArm_'+label)
    bone('Hand_'+label,(side*.305,-.015,.885),(side*.305,-.015,.80),'Forearm_'+label)
    bone('Thigh_'+label,(side*.098,0,.86),(side*.105,0,.475),'Hips')
    bone('Shin_'+label,(side*.105,0,.475),(side*.105,0,.155),'Thigh_'+label)
    bone('Foot_'+label,(side*.105,0,.155),(side*.105,-.16,.055),'Shin_'+label)
bpy.ops.object.mode_set(mode='OBJECT')
mesh.parent=rig
modifier=mesh.modifiers.new('Explorer skin','ARMATURE');modifier.object=rig
rig.animation_data_create()
clips={'Idle':3.2,'Walk':1.0,'Run':.7,'Jump':.42,'Fall':1.0,'Land':.26}
for name,duration in clips.items():
    action=bpy.data.actions.new(name);rig.animation_data.action=action
    frames=round(duration*30)
    for f in range(frames+1):
        t=f/frames;phase=math.tau*t
        for p in rig.pose.bones:
            p.rotation_mode='XYZ';p.rotation_euler=(0,0,0);p.location=(0,0,0)
        def rotate(b,x=0,y=0,z=0):rig.pose.bones[b].rotation_euler=(x,y,z)
        if name=='Idle':
            rotate('Spine',.014*math.sin(phase));rotate('Head',y=.035*math.sin(phase))
            rig.pose.bones['Hips'].location.y=.003*(1-math.cos(phase))
        elif name in ('Walk','Run'):
            run=name=='Run';swing=.78 if run else .44
            for sign,label in [(1,'L'),(-1,'R')]:
                s=math.sin(phase)*sign
                rotate('Thigh_'+label,-s*swing)
                rotate('Shin_'+label,max(0,-s)*(1.22 if run else .70))
                rotate('Foot_'+label,.10*s)
                rotate('UpperArm_'+label,s*(.62 if run else .34))
                rotate('Forearm_'+label,-(.8 if run else .16)-max(0,s)*.16)
            rotate('Spine',.12 if run else .035,z=.022*math.sin(phase))
            rig.pose.bones['Hips'].location.y=(.028 if run else .016)*math.sin(phase)**2
        elif name in ('Jump','Fall'):
            k=math.sin(t*math.pi/2) if name=='Jump' else 1
            for sign,label in [(1,'L'),(-1,'R')]:
                rotate('Thigh_'+label,-.22*k if sign==1 else .08*k)
                rotate('Shin_'+label,(.55 if sign==1 else .30)*k)
                rotate('UpperArm_'+label,-.20*k,z=sign*.18*k)
                rotate('Forearm_'+label,-.40*k)
            rotate('Spine',.07*k)
        else:
            k=math.sin(t*math.pi)
            rig.pose.bones['Hips'].location.y=-.09*k
            for label in ('L','R'):
                rotate('Thigh_'+label,-.26*k);rotate('Shin_'+label,.48*k)
                rotate('UpperArm_'+label,-.2*k);rotate('Forearm_'+label,-.25*k)
            rotate('Spine',.12*k)
        for p in rig.pose.bones:
            p.keyframe_insert(data_path='rotation_euler',frame=f+1,group=p.name)
            if p.name=='Hips':p.keyframe_insert(data_path='location',frame=f+1,group=p.name)
    track=rig.animation_data.nla_tracks.new();track.name=name
    track.strips.new(name,1,action);track.mute=True
    action.use_fake_user=True
rig.animation_data.action=None
for p in rig.pose.bones:p.rotation_euler=(0,0,0);p.location=(0,0,0)
scene.frame_set(1)
bpy.ops.object.select_all(action='DESELECT');mesh.select_set(True);rig.select_set(True)
bpy.context.view_layer.objects.active=rig
source=ROOT/'art/source/explorer.blend';asset=ROOT/'public/models/explorer.glb'
bpy.ops.wm.save_as_mainfile(filepath=str(source),compress=True)
bpy.ops.export_scene.gltf(filepath=str(asset),export_format='GLB',use_selection=True,
    export_animations=True,export_animation_mode='ACTIONS',export_force_sampling=True,
    export_anim_single_armature=True)
report={'name':'Archive explorer','heightMetres':1.70,'forward':'+Z in glTF',
    'triangles':sum(len(p.vertices)-2 for p in mesh.data.polygons),'bones':len(arm.bones),
    'clips':list(clips),'bytes':asset.stat().st_size,'provenance':'Original procedural modelling, rigging and animation authored for this repository. No external asset inputs.'}
(ROOT/'src/config/explorer.json').write_text(json.dumps(report,indent=2)+'\n')
(OUT/'explorer-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
