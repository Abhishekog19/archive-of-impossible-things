"""Ruin Runner neutral-model study. Separate from the live explorer and its rig.

Original shaped meshes authored against the user's selected turnaround. Garment
panels stay separate for subsequent skinning/secondary motion. This is a visual
production checkpoint, not an animated or approved replacement character.
"""
import bpy
import json
import math
import numpy as np
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.artifacts' / 'ruin-runner'
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.cycles.use_denoising = True
scene.view_settings.view_transform = 'AgX'
parts = []


def material(name, colour, kind=None, roughness=.8):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*colour, 1)
    bsdf.inputs['Roughness'].default_value = roughness
    if kind:
        # UV textile rather than world-space noise: a quiet directional weave,
        # broad dye variation and a deliberately drawn woven border on cloth.
        size = 512
        v, u = np.mgrid[0:size, 0:size] / (size - 1)
        weave = .022 * np.sin(u * math.tau * 170) + .018 * np.sin(v * math.tau * 140)
        dye = .045 * np.sin(u * 14 + np.sin(v * 9)) + .025 * np.cos(v * 27 - u * 11)
        rgb = np.broadcast_to(np.array(colour), (size, size, 3)).copy()
        rgb *= (1 + weave + dye)[..., None]
        if kind == 'olive':
            line = ((v > .065) & (v < .08)) | ((v > .18) & (v < .192))
            repeat = (u * 13) % 1
            triangle = (v > .094) & (v < .17) & (abs(repeat-.5) < (v-.094)*5)
            rgb[line | triangle] = np.array([.51, .47, .31])
        if kind == 'leather':
            rgb *= (1 - .08 * (np.sin(u*16)**6 * np.cos(v*13)**8))[..., None]
        rgba = np.ones((size, size, 4), dtype=np.float32)
        rgba[:, :, :3] = np.clip(rgb, 0, 1)
        img = bpy.data.images.new(name + ' woven colour', width=size, height=size)
        img.pixels.foreach_set(rgba.ravel())
        img.pack()
        tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex.image = img
        mat.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    return mat


M = {
    'linen': material('Warm unbleached linen', (.76, .70, .59), 'linen'),
    'olive': material('Olive woven shoulder cloth', (.34, .37, .23), 'olive'),
    'pants': material('Umber trouser cloth', (.36, .30, .24), 'linen'),
    'wrap': material('Undyed woven wraps', (.51, .48, .37), 'linen'),
    'leather': material('Weathered chestnut leather', (.29, .20, .13), 'leather', .69),
    'sole': material('Dark worn sole', (.045, .031, .02)),
    'skin': material('Warm skin', (.59, .32, .18), roughness=.68),
    'lip': material('Muted lip and ear', (.33, .12, .071)),
    'hair': material('Deep chestnut hair', (.049, .025, .014), roughness=.65),
    'hairlight': material('Hair strand highlights', (.092, .052, .025), roughness=.72),
    'white': material('Warm eye whites', (.79, .73, .61), roughness=.4),
    'iris': material('Hazel iris', (.18, .09, .028), roughness=.36),
    'pupil': material('Pupil', (.008, .005, .003), roughness=.3),
    'rope': material('Flax rope', (.47, .37, .25), 'linen'),
    'wood': material('Carved wood', (.24, .13, .047)),
    'stitch': material('Linen stitching', (.46, .35, .21)),
}


def mesh(name, verts, faces, mat, uvs=None, smooth=True, sub=0, solid=0):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    data.materials.append(M[mat])
    uv = data.uv_layers.new(name='GarmentUV')
    if uvs:
        for p in data.polygons:
            for li in p.loop_indices:
                uv.data[li].uv = uvs[data.loops[li].vertex_index]
    for p in data.polygons:
        p.use_smooth = smooth
    if sub:
        mod = obj.modifiers.new('Authored surface smoothing', 'SUBSURF')
        mod.levels = sub
        mod.render_levels = sub
    if solid:
        mod = obj.modifiers.new('Garment thickness', 'SOLIDIFY')
        mod.thickness = solid
    parts.append(obj)
    return obj


def loft(name, rows, mat, n=32, folds=0, sub=1):
    # Rows: z, x radius, y radius, x centre, y centre. Duplicated UV seam.
    verts, uv, faces = [], [], []
    for j, (z, rx, ry, cx, cy) in enumerate(rows):
        for i in range(n+1):
            a = i / n * math.tau
            f = folds * (math.sin(7*a+j*.8) + .6*math.cos(11*a-j*.95))
            verts.append((cx+(rx+f)*math.cos(a), cy+(ry+f*.6)*math.sin(a), z))
            uv.append((i/n, j/(len(rows)-1)))
    for j in range(len(rows)-1):
        for i in range(n):
            k = j*(n+1)+i
            faces.append((k, k+1, k+n+2, k+n+1))
    faces += [tuple(range(n-1,-1,-1)), tuple((len(rows)-1)*(n+1)+i for i in range(n))]
    return mesh(name, verts, faces, mat, uv, sub=sub)


def orb(name, pos, scale, mat, segments=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=pos)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(M[mat])
    for p in obj.data.polygons:
        p.use_smooth = True
    parts.append(obj)
    return obj


def cord(name, points, radius, mat, resolution=2):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.resolution_u = resolution
    data.bevel_depth = radius
    data.bevel_resolution = 1
    spline = data.splines.new('BEZIER')
    spline.bezier_points.add(len(points)-1)
    for p, co in zip(spline.bezier_points, points):
        p.co = co
        p.handle_left_type = p.handle_right_type = 'AUTO'
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    data.materials.append(M[mat])
    parts.append(obj)
    return obj


def ribbon(name, points, widths, mat, bulge=.005, width_axis='x'):
    verts, faces, uv = [], [], []
    for j, point in enumerate(points):
        for i, t in enumerate((-1, -.5, 0, .5, 1)):
            verts.append((point[0]+t*widths[j], point[1]-bulge*(1-t*t), point[2])
                if width_axis == 'x' else
                (point[0]+bulge*(1-t*t), point[1]+t*widths[j], point[2]))
            uv.append(((t+1)/2, j/(len(points)-1)))
    for j in range(len(points)-1):
        for i in range(4):
            k = j*5+i
            faces.append((k,k+1,k+6,k+5))
    return mesh(name, verts, faces, mat, uv, sub=1, solid=.002)


def binding(name, z0, z1, centre, radius, turns, width, mat='wrap', reverse=False):
    """Flat overlapping woven tape following the limb, with a lifted sewn edge."""
    verts=[];uv=[];faces=[]
    steps=round(turns*32)
    for j in range(steps+1):
        t=j/steps
        a=t*turns*math.tau*(-1 if reverse else 1)
        base=z0+(z1-z0)*t
        for i in range(5):
            q=i/4-.5
            z=base+q*width+.008*math.sin(a)
            cx,cy=centre(z)
            rr=radius(z)+.0015*math.cos(q*math.pi)
            verts.append((cx+rr*math.cos(a),cy+rr*.93*math.sin(a),z))
            uv.append((i/4,t*turns))
    for j in range(steps):
        for i in range(4):
            k=j*5+i;faces.append((k,k+1,k+6,k+5))
    return mesh(name,verts,faces,mat,uv,solid=.0015)


# Torso and draped tunic: full sleeves are separate, hems overlap instead of a cone.
loft('Linen torso with gathered waist', [
    (.98,.142,.087,0,0),(1.015,.15,.094,0,0),(1.06,.177,.112,0,0),
    (1.15,.183,.11,0,0),(1.27,.191,.105,0,0),(1.345,.178,.086,0,0),
    (1.385,.11,.068,0,0),(1.39,.063,.056,0,0)], 'linen', folds=.01)
loft('Neck',[(1.36,.047,.043,0,.018),(1.44,.039,.039,0,.018),
    (1.495,.039,.034,0,.020),(1.53,.043,.040,0,.018)],'skin')

# A skirt-like tunic is made from two asymmetric open panels with an overlapping
# side seam, rippled hanging folds, an actual edge, and a separate under layer.
for back in (False, True):
    verts, uv, faces = [], [], []
    for j in range(9):
        t=j/8
        for i in range(25):
            a=math.pi+i/24*math.pi if not back else i/24*math.pi
            x=(.176+.059*t)*math.cos(a)
            y=(.115+.037*t)*math.sin(a)
            z=1.015-t*(.235+.068*math.cos(a+.4))+.002*t**6*math.sin(i*2.8)
            y += .012*t*math.sin(i*1.6+t*2)
            verts.append((x,y,z));uv.append((i/24,1-t))
    for j in range(8):
        for i in range(24):
            k=j*25+i;faces.append((k,k+25,k+26,k+1))
    mesh('Overlapping tunic '+('back' if back else 'front'),verts,faces,'linen',uv,sub=1,solid=.003)

# Connected facial sculpt and volumetric hair replace the rejected primitive face.
import sys
sys.path.insert(0, str(Path(__file__).parent))
from ruin_runner_head import build_head
build_head(mesh, loft, orb, cord, M, material)

# Relaxed A-pose allows the sleeve openings, underarms, hands and satchel to read.
for s,label in [(-1,'L'),(1,'R')]:
    loft('Short folded sleeve '+label,[(1.19,.064,.065,s*.231,0),
        (1.21,.071,.072,s*.227,0),(1.26,.075,.079,s*.211,0),
        (1.33,.063,.07,s*.18,0),(1.35,.042,.054,s*.17,0)],'linen',folds=.007)
    loft('Arm anatomy '+label,[(.924,.032,.026,s*.329,-.012),(.975,.037,.032,s*.32,-.003),
        (1.05,.046,.04,s*.294,0),(1.1,.044,.041,s*.276,0),
        (1.16,.049,.043,s*.254,0),(1.23,.056,.049,s*.235,0)],'skin')
    binding('Woven forearm binding '+label,.942,1.035,
        lambda z:(s*(.327-(z-.937)*.29),-.006),
        lambda z:.035+.008*(z-.942)/.093,5,.022)
    loft('Palm '+label,[(.847,.022,.016,s*.345,-.013),(.878,.031,.02,s*.342,-.013),
        (.914,.03,.023,s*.333,-.013),(.93,.026,.023,s*.33,-.013)],'skin',n=24)
    for i in range(4):
        x=s*(.32+i*.015)
        end=.802+(.01 if i in (0,3) else 0)
        cord('Finger %s %s'%(label,i),[(x,-.014,.87),(x+s*.008,-.02,.833),
            (x+s*.007,-.029,end)],.007,'skin')
    cord('Thumb '+label,[(s*.313,-.011,.897),(s*.305,-.032,.869),(s*.31,-.037,.847)],.01,'skin')
    x=s*.091
    loft('Gathered trousers '+label,[(.38,.051,.053,x,0),(.425,.058,.056,x,0),
        (.45,.076,.066,x,.012),(.475,.088,.079,x,.014),(.493,.079,.068,x,.002),
        (.52,.089,.078,x,.008),(.55,.083,.067,x,-.003),(.59,.074,.069,x,0),
        (.67,.10,.085,x,0),(.8,.11,.098,x,0),(.93,.089,.09,x,0),
        (.985,.072,.066,x,0)],'pants',folds=.007,n=32)
    loft('Wrapped calf '+label,[(.12,.042,.041,x,.003),(.18,.046,.043,x,0),
        (.27,.055,.049,x,0),(.38,.055,.052,x,0),(.43,.053,.048,x,0)],'wrap')
    binding('Broad calf binding '+label,.17,.407,lambda z:(x,0),
        lambda z:float(np.interp(z,[.15,.27,.40],[.048,.056,.057])),7,.041)
    binding('Crossed calf straps '+label,.18,.397,lambda z:(x,0),
        lambda z:float(np.interp(z,[.15,.27,.40],[.051,.059,.060])),2,.025,'linen',True)
    loft('Boot upper '+label,[(.03,.063,.117,x,-.039),(.047,.062,.116,x,-.039),
        (.085,.059,.109,x,-.04),(.123,.048,.066,x,-.005),(.19,.049,.05,x,.003),
        (.22,.05,.049,x,.004)],'leather',n=32)
    loft('Boot sole '+label,[(.006,.063,.118,x,-.039),(.015,.065,.12,x,-.039),
        (.032,.063,.118,x,-.039)],'sole',n=32)
    for j in range(3):
        z=.118+j*.025
        cord('Crossed boot lace '+label,[(x-.042,-.048,z+.014),(x,-.058,z),
            (x+.042,-.048,z+.014)],.0035,'rope')

# Asymmetric triangular shoulder mantle drapes from collar across one shoulder
# and falls down the back. Dense enough to preserve folds and later weight rows.
verts, uv, faces = [], [], []
for j in range(17):
    t=j/16
    for i in range(33):
        a=i/32*math.tau
        radius=.067+.17*min(t*3,1)
        # Back extends farther; front remains a short scarf, clear of belt/strap.
        drop=.12+.27*(.5+.5*math.sin(a))+.08*math.cos(a)
        z=1.422-.03*min(t*4,1)-t*drop
        x=radius*math.cos(a)
        y=(.06+.067*min(t*4,1))*math.sin(a)
        y+=.012*t*math.sin(a*9+t*2)
        z+=.014*t*math.sin(a*7)+.003*t**8*math.sin(a*47)
        verts.append((x,y,z));uv.append((i/32,1-t))
for j in range(16):
    for i in range(32):
        k=j*33+i;faces.append((k,k+33,k+34,k+1))
cape=mesh('Separate olive mantle panel',verts,faces,'olive',uv,sub=1,solid=.003)
cape['secondary_motion'] = 'Pending: pin shoulder rows; weight cape chain after silhouette review'
verts=[];uv=[];faces=[]
for j in range(13):
    t=j/12
    for i in range(65):
        a=i/64*math.tau
        fold=.004*math.sin(a*4+t*math.pi*3)*math.sin(t*math.pi)
        x=(.064+.074*t+fold)*math.cos(a)
        y=(.052+.051*t+fold)*math.sin(a)
        z=1.45-.078*t+.014*math.cos(a+.8)+.018*math.sin(a)*t+.009*math.cos(a*3+.6)*math.sin(t*math.pi)
        verts.append((x,y,z));uv.append((i/64,.45+t*.55))
for j in range(12):
    for i in range(64):
        k=j*65+i;faces.append((k,k+65,k+66,k+1))
mesh('Draped folded shoulder cowl',verts,faces,'olive',uv,sub=1,solid=.002)

# Rope coils, knot and hanging ends. Braiding silhouettes kept restrained.
for j in range(3):
    cord('Rope waist coil',[(.155*math.cos(a),.102*math.sin(a),1.013+j*.013+.006*math.sin(a*2))
        for a in np.linspace(0,math.tau,48)],.006,'rope')
cord('Waist tie loop',[(-.04,-.113,1.03),(-.082,-.134,1.005),(-.089,-.134,1.035),(-.04,-.113,1.03)],.005,'rope')
for x,length in [(-.04,.16),(-.021,.12)]:
    cord('Hanging rope end',[(x,-.116,1.025),(x+.018,-.142,.97),(x+.011,-.153,1.025-length)],.0045,'rope')
    for k in range(4):
        cord('Rope tassel',[(x+.011,-.153,1.025-length),(x+.008+(k-1.5)*.004,-.153,1.0-length)],.0015,'rope')
orb('Wooden waist token',(.01,-.113,1.018),(.025,.007,.025),'wood')
cord('Token spiral',[(.01+.016*t*math.cos(t*math.tau*1.5),-.122,1.018+.016*t*math.sin(t*math.tau*1.5))
    for t in np.linspace(.1,1,28)],.0015,'rope')

# Strap follows the front/back torso, terminates at a side bag instead of backpack.
ribbon('Diagonal chest strap',[(-.14,-.103,1.375),(-.08,-.142,1.27),
    (.04,-.13,1.12),(.15,-.106,.997),(.21,-.054,.94)], [.017]*5,'leather',.002)
ribbon('Diagonal back strap',[(-.14,.106,1.375),(-.08,.144,1.26),
    (.04,.14,1.12),(.15,.108,.997),(.21,.055,.94)], [.017]*5,'leather',-.002)
loft('Side satchel body',[(.796,.059,.04,.213,-.007),(.81,.071,.048,.213,-.007),
    (.93,.075,.051,.213,-.007),(.977,.067,.04,.213,-.007)],'leather',n=24)
ribbon('Side satchel flap',[(.213,.03,.979),(.213,-.045,.975),(.213,-.066,.938),
    (.213,-.065,.895)], [.072,.076,.071,.06],'leather',.005)
for x in (.182,.244):
    ribbon('Satchel fastening',[(x,-.068,.95),(x,-.072,.925),(x,-.069,.868)],
        [.008,.008,.007],'leather',.002)
    orb('Wood bag stud',(x,-.076,.903),(.005,.003,.005),'wood',12,8)
for x in np.linspace(.163,.263,12):
    cord('Hand stitched satchel seam',[(x,-.073,.902),(x+.0025,-.073,.902)],.001,'stitch',1)

# Freeze modeling modifiers into export meshes; preserve semantic part names and
# individual UVs for manual edits / future garment skinning in the saved source.
bpy.ops.object.select_all(action='DESELECT')
for obj in parts:
    obj.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.convert(target='MESH')
parts=list(bpy.context.selected_objects)
for obj in parts:
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    # Reference has a slender upper body relative to the head. Taper smoothly
    # into the neck, leaving facial proportions untouched.
    for vertex in obj.data.vertices:
        blend=max(0,min(1,(vertex.co.z-1.38)/.08))
        vertex.co.x *= .92+.08*blend
    obj['stage']='PD08 neutral study; not skinned or approved'
asset=ROOT/'public/models/ruin-runner-study.glb'
bpy.ops.export_scene.gltf(filepath=str(asset),export_format='GLB',use_selection=True,export_animations=False)
report={'stage':'neutral model study; visual acceptance pending','heightMetres':round(max(v.co.z for o in parts for v in o.data.vertices),3),
    'triangles':sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),
    'meshParts':len(parts),'materials':len(M),'bytes':asset.stat().st_size,
    'reference':'User-selected Image 3 Ruin Runner turnaround (local concept/character/ruin-runner-approved.png)',
    'provenance':'Original authored meshes and UV textile images; no downloaded model or animation',
    'notImplemented':['skinning','locomotion replacement','runtime cloth','production player replacement']}
(ROOT/'src/config/ruin-runner-study.json').write_text(json.dumps(report,indent=2)+'\n')

# Neutral, repeatable orthographic evidence: no world fog or dramatic lighting to
# conceal shape defects. These lights are for review only, not runtime assets.
scene.world.color=(.3,.3,.3)
ground=material('Review warm grey',(.29,.27,.24))
bpy.ops.mesh.primitive_plane_add(size=200)
bpy.context.object.name='Review floor'
bpy.context.object.data.materials.append(ground)
for name,pos,power,size in [('Key',(-3,-4,5),420,4),('Fill',(3,-2,3),240,3),('Rim',(0,3,4),360,3)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=pos
    obj.rotation_euler=(Vector((0,0,.9))-obj.location).to_track_quat('-Z','Y').to_euler()
camera_data=bpy.data.cameras.new('Neutral review camera');camera_data.type='ORTHO'
camera=bpy.data.objects.new('Neutral review camera',camera_data);scene.collection.objects.link(camera)
scene.camera=camera
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
views={'front':((0,-4,1.0),(0,0,.88),1.95),'side':((4,0,1.0),(0,0,.88),1.95),
       'back':((0,4,1.0),(0,0,.88),1.95),'face':((.35,-3,1.64),(0,-.01,1.58),.42)}
for name,(pos,target,scale) in views.items():
    camera.location=pos;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    camera_data.ortho_scale=scale
    scene.render.resolution_x=600;scene.render.resolution_y=800 if name!='face' else 600
    scene.render.filepath=str(OUT/(name+'.png'))
    bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/ruin-runner-study.blend'),compress=True)
print(json.dumps(report),flush=True)
