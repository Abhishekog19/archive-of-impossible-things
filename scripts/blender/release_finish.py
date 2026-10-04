"""PD11 additive landscape dressing, rebuilt from the untouched production sources.

Preserves collision and authored UV atlases. Output .blend files use pd11-* names;
the source hub-blockout.blend (including the user's edit) is never opened/written.
"""
import bpy, math, random, sys, os
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).parent))
from placed_art import merge, color_material, leaf_crown as flat_crown

ROOT=Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/source/world-blockout.blend'))
vertices=[];faces=[]
for o in bpy.context.scene.objects:
    if o.type!='MESH' or not o.name.startswith(('Continuous terrain','Connected paving',
        'Forest extension ground','Canopy approach','Forest courtyard threshold')):continue
    offset=len(vertices)
    vertices.extend(o.matrix_world@v.co for v in o.data.vertices)
    faces.extend(tuple(offset+i for i in p.vertices) for p in o.data.polygons)
ground=BVHTree.FromPolygons(vertices,faces)

def leaf_crown(name, centre, radius, seed, count=230, leaf_scale=1):
    """Rounded leaf shoulders and layered greens instead of bright diamonds."""
    obj=flat_crown(name,centre,radius,seed,round(count*.7),leaf_scale)
    old=obj.data;verts=[];faces=[];colours=[]
    rng=random.Random(seed+1900)
    for p in old.polygons:
        a,b,c,d=[old.vertices[i].co.copy() for i in p.vertices]
        axis=(c-a)*.24
        start=len(verts)
        verts.extend([a,b-axis,b+axis,c,d+axis,d-axis])
        faces.append(tuple(start+i for i in range(6)))
        colour=old.color_attributes.active_color.data[p.loop_start].color
        elevation=sum(v.z for v in (a,b,c,d))/4-centre[2]
        shade=.40+.35*max(0,min(1,.5+elevation/max(radius[2],.1)))+rng.uniform(-.08,.08)
        colours.append(tuple(value*shade for value in colour[:3])+(1,))
    data=bpy.data.meshes.new(name+' rounded leaves');data.from_pydata(verts,[],faces);data.update()
    attr=data.color_attributes.new(name='CanopyColor',type='BYTE_COLOR',domain='CORNER')
    for p in data.polygons:
        for li in p.loop_indices:attr.data[li].color=colours[p.index]
    obj.data=data;bpy.data.meshes.remove(old)
    return obj

def height(x,z,default=0):
    hit=ground.ray_cast(Vector((x,-z,35)),Vector((0,0,-1)))[0]
    return hit.z if hit else default

def tint(obj, rgb):
    data=obj.data
    attr=data.color_attributes.new(name='FinishColour',type='BYTE_COLOR',domain='CORNER')
    for p in data.polygons:
        shade=.66+.24*max(0,p.normal.z)+.10*max(0,-p.normal.y)
        for i in p.loop_indices:attr.data[i].color=tuple(c*shade for c in rgb)+(1,)
    color_material(obj)

assets=[('hub-art',1101),('forest-approach',1102),('forest-canopy',1103),
        ('archive-exterior',1104),('archive-hall',1105)]
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if '--assets' in args:
    selected=set(args[args.index('--assets')+1].split(','))
    assert selected and selected <= {stem for stem,_ in assets}, 'Unknown finish asset'
    assets=[entry for entry in assets if entry[0] in selected]
for stem,seed in assets:
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'art/source/{stem}.blend'))
    originals=[o for o in bpy.context.selected_objects if o.type in ('MESH','EMPTY')]
    assert originals,stem
    rng=random.Random(seed);foliage=[];stone=[]
    hub=stem=='hub-art';forest=stem.startswith('forest')
    # Reproducible clusters with pockets of open ground, not evenly spaced scatter.
    clusters=[]
    if hub:
        for i in range(108):
            a=i*math.tau/108
            radius=rng.uniform(13.3,21)
            x=math.cos(a)*radius;z=math.sin(a)*radius
            if (abs(x)<3.4 and z>10) or (-18<x<-5 and z<-14) or (x>15 and -1<z<9):continue
            clusters.append((x,z))
        # Frame the far side of the plaza with a layered forest island.
        for j in range(22):
            x=rng.uniform(-5,8);z=rng.uniform(-24,-15)
            y=height(x,z)
            foliage.append(leaf_crown('PD11 woodland island',(x,-z,y+rng.uniform(.7,1.5)),
                (2,1.8,1.35),1450+j,140,.8))
    elif forest:
        for z in range(-41 if stem=='forest-approach' else -67,-66 if stem=='forest-approach' else -96,-3):
            t=max(0,min(1,(-z-42)/52));centre=-12+3.8*math.sin(t*math.tau)*math.sin(t*math.pi)
            for side in (-1,1):
                x=centre+side*rng.uniform(4,7)
                if -32<x<-17 and -77<z<-61:continue
                clusters.append((x,z))
    elif stem=='archive-exterior':
        clusters=[(-12+side*rng.uniform(8,13),z) for z in range(-98,-113,-2) for side in (-1,1)]
    else:
        clusters=[(-12+side*rng.uniform(6,9),z) for z in range(-118,-141,-3) for side in (-1,1)]
    for j,(x,z) in enumerate(clusters):
        for k in range(rng.randint(4,7)):
            xx=x+rng.uniform(-1.1,1.1);zz=z+rng.uniform(-1.1,1.1)
            y=height(xx,zz,1.65 if 'archive' in stem else 0)
            if 'archive' in stem:y=1.65
            foliage.append(leaf_crown('PD11 broadleaf shoulder',(xx,-zz,y+.45),
                (rng.uniform(.65,1.1),rng.uniform(.6,1.0),rng.uniform(.4,.8)),seed+j*13+k,52,.65))
        if j%2==0:
            y=height(x,z,1.65 if 'archive' in stem else 0)
            if 'archive' in stem:y=1.65
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(x,-z,y+.08))
            o=bpy.context.object;o.name='PD11 embedded shoulder stone'
            o.scale=(rng.uniform(.45,.95),rng.uniform(.4,.8),rng.uniform(.18,.48))
            o.rotation_euler=(rng.uniform(-.2,.2),rng.uniform(-.2,.2),rng.random()*6.28)
            bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
            tint(o,(.30,.32,.235));stone.append(o)
    # Texture atlases stay attached while broad roots gain asymmetrical ridges.
    if stem=='archive-exterior':
        for o in originals:
            if o.type=='MESH' and 'Wood' in o.name:
                for v in o.data.vertices:
                    p=v.co;amount=.085*math.sin(p.z*1.9+p.x*.65)+.045*math.sin(p.y*3+p.z*.9)
                    v.co+=v.normal*amount
                o.data.update()
    # Smaller hanging sprays create an intermediate canopy layer at REF6's exit.
    if stem=='forest-canopy':
        for j in range(9):
            x=-12+rng.choice((-1,1))*rng.uniform(2.8,5.2);z=-78-j*1.8
            foliage.append(leaf_crown('PD11 layered canopy',(x,-z,rng.uniform(8,11)),
                (2.5,2.1,1.2),1200+j,110,1.0))
    additions=[]
    if foliage:
        o=merge('PD11_Foliage_'+stem,foliage);color_material(o);additions.append(o)
    if stone:
        o=merge('PD11_Stone_'+stem,stone);color_material(o);additions.append(o)
    bpy.ops.object.select_all(action='DESELECT')
    for o in originals+additions:o.select_set(True)
    bpy.context.view_layer.objects.active=originals[0]
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f'art/source/pd11-{stem}.blend'),compress=True)
    # OneDrive may hold the destination open. Export a complete sibling then
    # replace atomically, so a failed export cannot leave a truncated live asset.
    target=ROOT/f'public/models/{stem}.glb'
    temporary=target.with_name(stem+'.next.glb')
    bpy.ops.export_scene.gltf(filepath=str(temporary),export_format='GLB',
        use_selection=True,export_image_format='JPEG',export_image_quality=94)
    os.replace(temporary,target)
    print('PD11_FINISH '+stem+' clusters='+str(len(clusters)),flush=True)
