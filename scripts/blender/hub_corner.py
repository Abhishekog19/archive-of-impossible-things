"""Phase 2 benchmark: authored relief + a portable full-colour diffuse bake.

Local metre coordinates use Blender Z-up. R3F places the GLB at (-8, 0, -9).
Rebuild replaces only these generated corner outputs; source objects stay editable.
"""
import bpy
import bmesh
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
scene.cycles.samples = 40
scene.cycles.max_bounces = 3
scene.cycles.use_denoising = True
scene.view_settings.view_transform = 'AgX'
visuals = []
colliders = []
foliage = []
floor_objects = []

def material(name, dark, light, scale=5, growth=False):
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
    if growth:
        # Damp lower masonry carries irregular growth; the dry upper face stays
        # limestone. Bake this mask so runtime needs no extra material/shader.
        position = n.new('ShaderNodeSeparateXYZ')
        links.new(coord.outputs['Position'], position.inputs[0])
        height = n.new('ShaderNodeMapRange')
        height.inputs['From Min'].default_value = .15
        height.inputs['From Max'].default_value = 1.9
        height.inputs['To Min'].default_value = 1
        height.inputs['To Max'].default_value = 0
        links.new(position.outputs['Z'], height.inputs['Value'])
        islands = n.new('ShaderNodeTexNoise')
        islands.inputs['Scale'].default_value = 3.8
        islands.inputs['Detail'].default_value = 3
        streaks = n.new('ShaderNodeVectorMath')
        streaks.operation = 'MULTIPLY'
        streaks.inputs[1].default_value = (1.2,1.2,.4)
        links.new(coord.outputs['Position'], streaks.inputs[0])
        links.new(streaks.outputs[0], islands.inputs['Vector'])
        boundary = n.new('ShaderNodeValToRGB')
        boundary.color_ramp.elements[0].position = .43
        boundary.color_ramp.elements[1].position = .58
        links.new(islands.outputs['Fac'], boundary.inputs[0])
        mask = n.new('ShaderNodeMath')
        mask.operation = 'MULTIPLY'
        links.new(height.outputs['Result'], mask.inputs[0])
        links.new(boundary.outputs[0], mask.inputs[1])
        edge = n.new('ShaderNodeMapRange')
        edge.inputs['From Min'].default_value = .25
        edge.inputs['From Max'].default_value = .40
        links.new(mask.outputs[0], edge.inputs['Value'])
        blend = n.new('ShaderNodeMixRGB')
        blend.inputs[2].default_value = (.105,.16,.038,1)
        links.new(edge.outputs['Result'], blend.inputs[0])
        links.new(ramp.outputs[0], blend.inputs[1])
        links.new(blend.outputs[0], p.inputs['Base Color'])
    if name.startswith('Warm limestone'):
        grain = n.new('ShaderNodeTexNoise')
        grain.inputs['Scale'].default_value = 32
        grain.inputs['Detail'].default_value = 2
        links.new(coord.outputs['Position'], grain.inputs['Vector'])
        bump = n.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = .23
        bump.inputs['Distance'].default_value = .022
        links.new(grain.outputs['Fac'], bump.inputs['Height'])
        links.new(bump.outputs['Normal'], p.inputs['Normal'])
    if name == 'Bark planes':
        stretch = n.new('ShaderNodeVectorMath')
        stretch.operation = 'MULTIPLY'
        stretch.inputs[1].default_value = (2,2,.12)
        links.new(coord.outputs['Position'], stretch.inputs[0])
        links.new(stretch.outputs[0], noise.inputs['Vector'])
    return m

stone = [material('Warm limestone '+str(i),
                 (0.39+i*.025, .40+i*.018, .30),
                 (.57+i*.035, .55+i*.025, .39+i*.02), .9) for i in range(3)]
masonry = [material('Warm limestone sheltered '+str(i),
                    (.39+i*.025,.40+i*.018,.30),
                    (.57+i*.035,.55+i*.025,.39+i*.02), .9, growth=True) for i in range(3)]
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
        if name in ('Eroded wall course','Column course') and random.random()<.55:
            # Remove a real exposed corner before bevelling. Keep the earlier
            # collision copy simple so decorative chips cannot snag movement.
            bm=bmesh.new()
            bm.from_mesh(o.data)
            bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
                                  dist=.00001,plane_co=(size[0]/2-.10,-size[1]/2+.12,size[2]/2-.09),
                                  plane_no=(1,-1,1),clear_outer=True,clear_inner=False)
            bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
            bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
            bm.to_mesh(o.data)
            bm.free()
        # Small unequal chips and skewed faces replace the uniformly rounded blocks.
        for vertex in o.data.vertices:
            vertex.co += Vector((random.uniform(-.035,.035),random.uniform(-.035,.035),random.uniform(-.025,.025)))
        mod = o.modifiers.new('Chipped broad edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 1
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier=mod.name)
    visuals.append(o)
    return o

def patch(name, center, radius, mat, count=11):
    x,y,z=center
    verts=[(x,y,z)]
    for i in range(count):
        angle=i*math.tau/count
        r=radius*random.uniform(.6,1.15)
        verts.append((x+math.cos(angle)*r,y+math.sin(angle)*r*.55,z+random.uniform(-.002,.002)))
    return mesh(name,verts,[(0,i+1,(i+1)%count+1) for i in range(count)],mat)

def slab(poly, height, mat):
    # Recess a few points along each edge; neighbouring stones keep their own
    # broken outlines instead of sharing perfectly machined straight seams.
    rng=random.Random(round(sum(x*31+y*17 for x,y in poly)*1000))
    chipped=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        chipped.append(a)
        dx,dy=b[0]-a[0],b[1]-a[1]
        length=math.hypot(dx,dy)
        if length>.45:
            for t in (.28,.53,.76):
                inset=rng.uniform(.004,.035)
                chipped.append((a[0]+dx*t-dy/length*inset,a[1]+dy*t+dx/length*inset))
    poly=chipped
    n=len(poly)
    verts=[(x,y,z) for z in (-.025,height) for x,y in poly]
    # Buried undersides need neither runtime triangles nor precious atlas space.
    faces=[tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    floor_objects.append(mesh('Fractured limestone slab',verts,faces,mat))

def clip_cell(poly, nx, ny, limit):
    """Intersect a convex stone cell with nx*x + ny*y <= limit."""
    result=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        da=nx*a[0]+ny*a[1]-limit
        db=nx*b[0]+ny*b[1]-limit
        if da<=0:
            result.append(a)
        if (da<0<db) or (db<0<da):
            t=da/(da-db)
            result.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
    return result

def flagstones():
    # Jittered Voronoi cells interlock without long row seams or repeated
    # bevelled rectangles. Their shared boundaries keep the joint width honest.
    rng=random.Random(8311)
    seeds=[(-3.6+x*1.18+rng.uniform(-.36,.36),
            -3.9+y*1.15+rng.uniform(-.34,.34)) for y in range(8) for x in range(7)]
    domain=[(-3.9,-4.2),(-2.9,-4.45),(2.8,-4.3),(4,-3.9),
            (4.05,3.5),(3.3,4.35),(-3.1,4.4),(-4.05,3.8)]
    for x,y in seeds:
        poly=domain[:]
        for ox,oy in seeds:
            if (x,y)==(ox,oy):
                continue
            nx,ny=ox-x,oy-y
            poly=clip_cell(poly,nx,ny,(ox*ox+oy*oy-x*x-y*y)/2)
            if not poly:
                break
        if len(poly)<3:
            continue
        # Offset all edges into the convex cell for 3–6 cm total seam width.
        inset=poly[:]
        gap=rng.uniform(.018,.03)
        for a,b in zip(poly,poly[1:]+poly[:1]):
            nx,ny=b[1]-a[1],a[0]-b[0]
            inset=clip_cell(inset,nx,ny,nx*a[0]+ny*a[1]-gap*math.hypot(nx,ny))
        if len(inset)<3:
            continue
        height=rng.uniform(.105,.145)
        chosen=stone[rng.randrange(len(stone))]
        slab(inset,height,chosen)
        # Growth follows selected joints and spills onto a few sheltered edges.
        if abs(x)>2.2 or rng.random()<.28:
            index=rng.randrange(len(inset))
            a,b=inset[index],inset[(index+1)%len(inset)]
            for t in (.18,.43,.7):
                at=(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,height+.004)
                floor_objects.append(patch('Joint edge moss',at,rng.uniform(.055,.15),moss,9))

# Smooth collision is independent of the broken paving and irregular moss edge.
bed=cube('Corner floor collider',(0,0,-.08),(8,9,.28),moss,solid=True)
visuals.remove(bed)
bpy.data.objects.remove(bed,do_unlink=True)
outline=[(-4,-4.3),(-2.2,-4.55),(-.5,-4.1),(1.6,-4.45),(3.75,-4.1),
         (4.05,-1.8),(3.9,1),(4.2,3.8),(2.7,4.4),(.2,4.5),(-2.8,4.35),(-4.1,2),(-3.9,-1)]
floor_objects.append(mesh('Eroded seam bed',[(x,y,.065) for x,y in outline],
                          [tuple(range(len(outline)))],moss))
flagstones()
random.seed(8312)  # Keep the remaining scene stable while tuning paving cells.

# Loose, shallow remnants break up the straight sample perimeter. They sit on
# the existing hub collision plane and taper out into the undressed terrain.
for i in range(22):
    front=i<12
    x=random.uniform(-4.15,4.15) if front else random.choice([-1,1])*random.uniform(4.0,4.65)
    y=random.uniform(-5.65,-4.25) if front else random.uniform(-3.7,3.7)
    radius=random.uniform(.16,.48)
    points=[]
    for j in range(6):
        a=j*math.tau/6
        r=radius*random.uniform(.7,1.1)
        points.append((x+math.cos(a)*r,y+math.sin(a)*r*.7))
    slab(points,random.uniform(.035,.075),random.choice(stone))

# Masonry follows one side of the path; the cap breaks down toward the plaza.
for row in range(5):
    y=-1.2+(row%2)*.19+max(0,row-1)*.40
    end=3.9-max(0,row-1)*.35
    while y<end-.2:
        length=min(random.uniform(.65,1.25),end-y)
        x=-3.5+random.uniform(-.07,.07)
        top=.56+row*.51
        block=cube('Eroded wall course',(x,y+length/2,top-.24),
                   (.7+random.uniform(-.06,.08),length-.025,.48),random.choice(masonry),
                   random.uniform(.015,.045),random.uniform(-.065,.065),solid=True)
        if row>=3:
            for v in block.data.vertices:
                if v.co.z>.1:
                    v.co.z-=max(0,v.co.y+length*.18)*random.uniform(.15,.6)
        if row<=2 and (row==0 or random.random()<.45):
            patch('Moss on sheltered wall ledge',(x,y+length*.45,top+.008),random.uniform(.18,.38),moss)
        y+=length

# Replace the corresponding blockout column at world (-7,-10).
cube('Column plinth',(1,1,.22),(1.7,1.7,.35),masonry[0],.025,solid=True)
for i in range(4):
    cube('Column course',(1+random.uniform(-.035,.035),1,.78+i*.71),
         (1.04,1.07,.69),random.choice(masonry),.032,
         random.uniform(-.025,.025),solid=True)
cap=cube('Fractured column crown',(1.03,1,3.30),(.94,1.05,.72),masonry[0],.02,solid=True)
for v in cap.data.vertices:
    if v.co.z>0:
        v.co.z-=max(0,v.co.x+.25)*.7
patch('Column base moss',(.55,1.15,.401),.52,moss)

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
for i in range(7):
    a=i*2.4+random.uniform(-.3,.3)
    dx,dy=math.cos(a),math.sin(a)
    reach=random.uniform(1.1,2.1)
    limb('Buttress root',[(3,3,random.uniform(.55,1)),(3+dx*.55,3+dy*.6,.32),
                         (3+dx*reach*.65,3+dy*reach*.65,.17),(3+dx*reach,3+dy*reach,.08)],
         [.25,.20,.09,.008],bark,8)

def leaves(name, center, radius, count, mat):
    verts,faces,tints=[],[],[]
    for _ in range(count):
        a=random.uniform(0,math.tau)
        r=radius*math.sqrt(random.random())
        # Rounded leaves occupy an ellipsoid, with shaded lower layers rather
        # than a single flat umbrella. Silhouette gaps expose the branch forks.
        dome=math.sqrt(max(0,1-(r/radius)**2))
        layer=random.uniform(-.65,.75)
        p=Vector((center[0]+math.cos(a)*r,center[1]+math.sin(a)*r*.82,
                  center[2]+dome*radius*layer))
        heading=a+random.uniform(-1.5,1.5)
        tilt=random.uniform(-.7,.4)
        u=Vector((math.cos(heading),math.sin(heading),tilt)).normalized()*random.uniform(.19,.29)
        v=Vector((-math.sin(heading),math.cos(heading),0))*random.uniform(.13,.19)
        k=len(verts)
        verts.append(tuple(p+Vector((0,0,.025))))
        for j in range(8):
            angle=j*math.tau/8
            verts.append(tuple(p+u*math.cos(angle)+v*math.sin(angle)))
            faces.append((k,k+j+1,k+(j+1)%8+1))
        tints.append(random.uniform(.88,1.08)*(.73+.32*layer))
    o=mesh(name,verts,faces,mat)
    visuals.remove(o)
    foliage.append(o)
    colors=o.data.color_attributes.new(name='FoliageColor',type='BYTE_COLOR',domain='CORNER')
    # Broad leaf colour planes stay crisp at every distance without alpha cards
    # or thousands of tiny UV islands stealing resolution from the stone bake.
    for poly in o.data.polygons:
        poly.use_smooth=True
        tint=tints[poly.index//8]
        base=(.115,.185,.042)
        for index in poly.loop_indices:
            colors.data[index].color=(*(c*tint for c in base),1)
    return o

for i in range(7):
    a=i*2.4
    reach=random.uniform(2.1,3.3)
    end=(2.8+math.cos(a)*reach,2.5+math.sin(a)*reach,5.4+random.uniform(-.35,1.7))
    fork=(end[0]*.55+1.35,end[1]*.55+1.35,end[2]-.7)
    limb('Spreading branch',[(3,3,3.2+i*.19),(2.9,3,4.4),fork,end],[.22,.17,.10,.015],bark,8)
    for j in range(3):
        tip=(end[0]+random.uniform(-.9,.9),end[1]+random.uniform(-.9,.9),end[2]+random.uniform(-.4,.6))
        limb('Leaf-bearing twig',[fork,end,tip],[.055,.025,.003],bark,5)
        leaves('Layered broadleaf crown',tip,random.uniform(.8,1.15),60,leaf_mats[i%3])

for tip in [(2.0,3.1,7.3),(3.25,3.4,7.65),(2.9,2.1,7.2)]:
    limb('Upper crown fork',[(3.2,3.2,5),(2.6,3.1,6.6),tip],[.15,.08,.01],bark,7)
    leaves('Upper broadleaf crown',tip,1.05,60,leaf_mats[1])

# One authored fern prototype. Blender copies cast into the bake; exported marker
# transforms are consumed by one R3F InstancedMesh, not one draw per plant.
fern_verts,fern_faces=[],[]
for frond in range(9):
    angle=frond*math.tau/9
    axis=Vector((math.cos(angle),math.sin(angle),0))
    side=Vector((-math.sin(angle),math.cos(angle),0))
    reach=random.uniform(.4,.65)
    for j in range(1,9):
        t=j/9
        center=axis*(t*reach)+Vector((0,0,.07+math.sin(t*math.pi*.8)*.4))
        for sign in (-1,1):
            tip=center+side*sign*(1-t)*.20+axis*.10+Vector((0,0,-.025))
            base=center-axis*.035
            k=len(fern_verts)
            fern_verts.extend([tuple(base),tuple(center+axis*.04),tuple(tip)])
            fern_faces.append((k,k+1,k+2))
fern=mesh('FernPrototype',fern_verts,fern_faces,leaf_mats[1])
visuals.remove(fern)
colors=fern.data.color_attributes.new(name='FoliageColor',type='BYTE_COLOR',domain='CORNER')
for poly in fern.data.polygons:
    shade=random.uniform(.7,1.15)
    for index in poly.loop_indices:
        colors.data[index].color=(.09*shade,.17*shade,.038*shade,1)
fern.hide_render=True
fern.hide_set(True)
fern_markers=[]
fern_casters=[]

# Ground cover grows at wall bases and outer shoulders, leaving the route open.
for i in range(24):
    x=random.choice([-1,1])*random.uniform(2.9,3.8)
    y=random.uniform(-4,4.1)
    plant=fern.copy()
    plant.name='Fern bake caster'
    bpy.context.collection.objects.link(plant)
    plant.hide_render=False
    plant.hide_set(False)
    plant.location=(x,y,.14)
    plant.rotation_euler.z=random.uniform(0,math.tau)
    size=random.uniform(.65,1.15)
    plant.scale=(size,size,size)
    fern_casters.append(plant)
    marker=bpy.data.objects.new('GroundFern_'+str(i),None)
    bpy.context.collection.objects.link(marker)
    marker.location=plant.location
    marker.rotation_euler=plant.rotation_euler
    marker.scale=plant.scale
    fern_markers.append(marker)
for i in range(12):
    x,y=-3+random.uniform(-.2,.5),random.uniform(-3.5,3.6)
    cube('Fallen wall stone',(x,y,.2),(random.uniform(.3,.8),.45,.32),random.choice(masonry),.04,random.uniform(-1,1))

# Warm directional illumination and a cool sky become image data, not runtime lights.
scene.world.use_nodes=True
background=scene.world.node_tree.nodes.get('Background')
background.inputs['Color'].default_value=(.48,.60,.72,1)
background.inputs['Strength'].default_value=.32
bpy.ops.object.light_add(type='SUN',location=(5,6,10))
sun=bpy.context.object
sun.name='Bake warm afternoon'
sun.data.energy=2.4
sun.data.color=(1,.91,.73)
sun.data.angle=math.radians(2.5)
sun.rotation_euler=(Vector((-3,-4,0))-sun.location).to_track_quat('-Z','Y').to_euler()

# Separate paving and architecture atlases keep close-view stone relief from
# sharing a single low-density texture with a seven-metre tree.
for c in colliders:
    c.hide_render=True
    c.hide_set(True)
bake_targets=[]
groups=[('Corner_Paving',floor_objects,2048),
        ('Corner_Baked',[o for o in visuals if o not in floor_objects],1024)]
for name,objects,resolution in groups:
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.object.duplicate()
    bpy.ops.object.join()
    target=bpy.context.object
    target.name=name
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.003)
    bpy.ops.object.mode_set(mode='OBJECT')
    atlas=bpy.data.images.new(name+' diffuse atlas',width=resolution,height=resolution,alpha=False)
    atlas.file_format='PNG'
    atlas.filepath_raw=str(DIAGNOSTICS/(name+'-baked.png'))
    for index,mat in enumerate(list(target.data.materials)):
        unique=mat.copy()
        target.data.materials[index]=unique
        node=unique.node_tree.nodes.new('ShaderNodeTexImage')
        node.image=atlas
        unique.node_tree.nodes.active=node
    bake_targets.append((target,atlas))
for o in visuals:
    o.hide_render=True
    o.hide_set(True)
scene.render.bake.use_pass_direct=True
scene.render.bake.use_pass_indirect=True
scene.render.bake.use_pass_color=True
scene.render.bake.margin=6
for target,atlas in bake_targets:
    bpy.ops.object.select_all(action='DESELECT')
    target.select_set(True)
    bpy.context.view_layer.objects.active=target
    print('BAKING '+target.name,flush=True)
    bpy.ops.object.bake(type='DIFFUSE')
    atlas.save()
    atlas.pack()
for target,atlas in bake_targets:
    baked=bpy.data.materials.new(target.name)
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
fern.data.materials.clear()
fern.data.materials.append(leaf_material)

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
for target,_ in bake_targets:
    target.select_set(True)
leaf_mesh.select_set(True)
fern.hide_set(False)
fern.select_set(True)
for marker in fern_markers:
    marker.select_set(True)
SOURCE.parent.mkdir(parents=True,exist_ok=True)
EXPORT.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True)
export_options={'filepath':str(EXPORT),'export_format':'GLB',
                'use_selection':True,'export_image_format':'JPEG'}
if 'export_jpeg_quality' in bpy.ops.export_scene.gltf.get_rna_type().properties:
    export_options['export_jpeg_quality']=90
if 'export_image_quality' in bpy.ops.export_scene.gltf.get_rna_type().properties:
    export_options['export_image_quality']=90
bpy.ops.export_scene.gltf(**export_options)
report={'seconds':round(time.monotonic()-started,1),'atlases':[[2048,2048],[1024,1024]],
        'glbBytes':EXPORT.stat().st_size,'sourceBytes':SOURCE.stat().st_size,
        'bake':'DIFFUSE: colour + direct + indirect, 40 CPU samples',
        'fernInstances':len(fern_markers),
        'runtime':'two UV0 diffuse bakes, canopy vertex colours, instanced fern prototype'}
(DIAGNOSTICS/'corner-report.json').write_text(json.dumps(report,indent=2))
print('CORNER_EXPORTED '+json.dumps(report),flush=True)
