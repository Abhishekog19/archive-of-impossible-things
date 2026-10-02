"""Fit the authored Ruin Runner study to the established locomotion skeleton.

The neutral source remains editable. Semantic weights preserve garment anchors;
only the derived game mesh is reduced and joined. No automatic nearest-bone
binding of eyes, fingers, straps or clothing panels.
"""
import bpy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/source/ruin-runner-study.blend'))
scene = bpy.context.scene
parts = [o for o in scene.objects if o.type == 'MESH' and 'stage' in o]
assert len(parts) > 200, 'Expected the authored neutral study'
for obj in list(scene.objects):
    if obj not in parts:
        bpy.data.objects.remove(obj, do_unlink=True)
with bpy.data.libraries.load(str(ROOT/'art/source/explorer.blend'), link=False) as (source, dest):
    dest.objects = ['ExplorerRig']
    dest.actions = list(source.actions)
rig = dest.objects[0]
scene.collection.objects.link(rig)
rig.animation_data.action = None
for track in rig.animation_data.nla_tracks:
    track.mute = True
for p in rig.pose.bones:
    p.rotation_euler = (0,0,0)
    p.location = (0,0,0)
bpy.context.view_layer.objects.active = rig
rig.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
fit = {
    'Cape': ((0,.135,1.40),(0,.175,1.22)),
    'CapeTip': ((0,.175,1.22),(0,.18,1.065)),
    'Scarf': ((.02,-.13,1.43),(.025,-.16,1.28)),
    'Rope': ((-.035,-.135,.985),(-.04,-.15,.76)),
    'Satchel': ((.196,0,.995),(.196,0,.80)),
}
for name,(head,tail) in fit.items():
    b = rig.data.edit_bones[name]
    b.head = head
    b.tail = tail
bpy.ops.object.mode_set(mode='OBJECT')

def ramp(value, low, high):
    t = max(0,min(1,(value-low)/(high-low)))
    return t*t*(3-2*t)

def blend(a,b,t):
    return {a:1-t,b:t}

def weights(name, v):
    x,y,z = v
    side = 'L' if x < 0 else 'R'
    if any(s in name for s in ('satchel','Satchel','bag stud')):
        return {'Satchel':1}
    if name.startswith(('Diagonal chest','Diagonal back')):
        return blend('Hips','Spine',ramp(z,1.0,1.20))
    if name.startswith(('Hanging rope','Rope tassel')):
        return blend('Hips','Rope',1-ramp(z,.84,.98))
    if name.startswith(('Rope waist','Waist tie','Wooden waist','Token spiral')):
        return {'Hips':1}
    if name.startswith(('Separate triangular','Mantle sewn')):
        if z > 1.25:
            return blend('Cape','Spine',ramp(z,1.25,1.40))
        return blend('CapeTip','Cape',ramp(z,1.07,1.25))
    if name.startswith(('Folded asymmetric','Soft scarf')):
        return blend('Scarf','Neck',ramp(z,1.29,1.43))
    if name.startswith(('Cut linen','Turned hem')):
        # Pin the waist. Rear fabric stays hip-driven above the moving legs.
        if y > .015:
            return {'Hips':1}
        return blend('Hem_'+side,'Hips',ramp(z,.81,1.0))
    if name.startswith('Linen shirt'):
        return blend('Hips','Spine',ramp(z,1.00,1.17))
    if name.startswith(('Open short sleeve','Turned open sleeve')):
        return blend('Spine','UpperArm_'+side,ramp(abs(x),.13,.23))
    if name.startswith('Arm anatomy'):
        return blend('Forearm_'+side,'UpperArm_'+side,ramp(z,1.045,1.13))
    if name.startswith('Woven forearm'):
        return {'Forearm_'+side:1}
    if name.startswith(('Palm','Finger','Thumb')):
        return {'Hand_'+side:1}
    if name.startswith('Gathered trousers'):
        if z > .79:
            return blend('Thigh_'+side,'Hips',ramp(z,.79,.97))
        return blend('Shin_'+side,'Thigh_'+side,ramp(z,.43,.54))
    if name.startswith(('Wrapped calf','Broad calf','Crossed calf')):
        return {'Shin_'+side:1}
    if name.startswith(('Boot','Crossed boot')):
        return {'Foot_'+side:1}
    if name.startswith('Neck'):
        return blend('Neck','Head',ramp(z,1.42,1.48))
    if name.startswith(('Attached split hair','Layered side and nape')):
        return blend('Hair','Head',ramp(z,1.55,1.69))
    if z > 1.43:
        return {'Head':1}
    raise ValueError('Unclassified character part: '+name)

bpy.ops.object.select_all(action='DESELECT')
for obj in parts:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    # Preserve tiny facial features and the continuous face's silhouette.
    ratio = .65 if 'face skull' in obj.name else .28
    if any(s in obj.name.lower() for s in ('eye','iris','pupil','lip','brow','nostril')):
        ratio = 1
    if len(obj.data.polygons) > 180 and ratio < 1:
        mod = obj.modifiers.new('Runtime silhouette reduction','DECIMATE')
        mod.ratio = ratio
        bpy.ops.object.modifier_apply(modifier=mod.name)
    obj.vertex_groups.clear()
    for vertex in obj.data.vertices:
        for bone,weight in weights(obj.name,vertex.co).items():
            if weight < 1e-5:
                continue
            group = obj.vertex_groups.get(bone) or obj.vertex_groups.new(name=bone)
            group.add([vertex.index],weight,'REPLACE')
    obj.select_set(False)

for obj in parts:
    obj.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
mesh = bpy.context.object
mesh.name = 'RuinRunner'
mesh['stage'] = 'PD11 fitted runtime character; visual acceptance pending'
mesh.parent = rig
mod = mesh.modifiers.new('Ruin Runner skin','ARMATURE')
mod.object = rig
# Per-asset limits accompany the rig, rather than forcing old garment dimensions.
rig['secondaryProfile'] = 'ruin-runner'
for name in ('Cape','CapeTip','Scarf','Hem_L','Hem_R','Hair','Rope','Satchel'):
    rig.data.bones[name]['secondaryLength'] = rig.data.bones[name].length
scene.frame_set(1)
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
asset = ROOT/'public/models/ruin-runner.glb'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/ruin-runner-runtime.blend'),compress=True)
bpy.ops.export_scene.gltf(filepath=str(asset),export_format='GLB',use_selection=True,
    export_animations=True,export_animation_mode='ACTIONS',export_force_sampling=True,
    export_anim_single_armature=True,export_extras=True)
report = {'stage':'runtime replacement; visual review pending','heightMetres':1.742,
    'triangles':sum(len(p.vertices)-2 for p in mesh.data.polygons),
    'materials':len(mesh.data.materials),'bones':len(rig.data.bones),
    'clips':['Idle','Walk','Run','Jump','Fall','Land'],'bytes':asset.stat().st_size,
    'source':'art/source/ruin-runner-study.blend',
    'secondaryMotion':'Constrained spring bones; not a cloth simulation',
    'provenance':'Original authored meshes, textures, semantic skin weights and repository locomotion clips'}
(ROOT/'src/config/ruin-runner.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
