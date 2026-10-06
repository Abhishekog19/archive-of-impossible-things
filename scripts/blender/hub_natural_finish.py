"""PD12 hub silhouette pass, derived from the PD11 source without accumulating edits.

Decorative crowns, weathered courses and planted edges keep collision unchanged.
Never opens or saves hub-blockout.blend.
"""
import bpy, math, random, sys, os, json
from pathlib import Path
from mathutils import Vector, Matrix

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from placed_art import color_material

bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/source/pd11-hub-art.blend'))
originals = [o for o in bpy.context.selected_objects if o.type in ('MESH','EMPTY')]
assert any(o.name == 'HubArt_Foliage' for o in originals)
rng = random.Random(121004)
verts, faces, colours = [], [], []
sun = Vector((-0.4, -0.25, .85)).normalized()

def face(points, colour):
    start = len(verts)
    verts.extend(points)
    faces.append(tuple(range(start, len(verts))))
    colours.append(colour)

def leaf(p, normal, size, tint):
    # Folded six-sided leaves catch different values instead of flat diamonds.
    u = normal.cross(Vector((0, 0, 1)))
    if u.length < .1: u = normal.cross(Vector((0, 1, 0)))
    u.normalize()
    u = Matrix.Rotation(rng.random()*math.tau, 3, normal) @ u
    v = normal.cross(u).normalized()
    outline = [(-1,0),(-.45,-.52),(.5,-.48),(1,0),(.45,.52),(-.5,.48)]
    ring = [p+size*(u*x+v*y) for x,y in outline]
    ridge = p+normal*size*.16
    for i in range(6):
        shade = tint*(.91 if i < 3 else 1.04)
        face([ring[i], ring[(i+1)%6], ridge], (shade*.30, shade*.39, shade*.16, 1))

def crown_lobe(centre, radius, leaves=110):
    """Low-cost opaque leafy volume plus broken, directional leaf outlines."""
    c = Vector(centre); r = Vector(radius)
    # A modest core closes see-through gaps; uneven rings prevent spherical topiary.
    rings, segments = 7, 14
    points = []
    for row in range(rings):
        latitude = -math.pi/2 + math.pi*row/(rings-1)
        for col in range(segments):
            a = math.tau*col/segments
            n = Vector((math.cos(latitude)*math.cos(a),math.cos(latitude)*math.sin(a),math.sin(latitude)))
            wobble = 1 + .12*math.sin(a*3+row*.9) + rng.uniform(-.065,.065)
            points.append(c+Vector(tuple(n[i]*r[i]*wobble*.73 for i in range(3))))
    for row in range(rings-1):
        for col in range(segments):
            ids = [row*segments+col,row*segments+(col+1)%segments,
                   (row+1)*segments+(col+1)%segments,(row+1)*segments+col]
            p = [points[i] for i in ids]
            n = ((p[1]-p[0]).cross(p[2]-p[0])).normalized()
            light = .17 + .18*max(0,n.dot(sun)) + .10*row/(rings-1)
            light *= rng.uniform(.92,1.06)
            face(p,(light*.28,light*.37,light*.14,1))
    for i in range(leaves):
        # Even shell coverage including drooping sides and undersides.
        z = 1-2*(i+.5)/leaves
        a = i*2.399963+ rng.uniform(-.15,.15)
        n = Vector((math.sqrt(1-z*z)*math.cos(a),math.sqrt(1-z*z)*math.sin(a),z))
        spread = rng.uniform(.88,1.06)
        p = c+Vector(tuple(n[j]*r[j]*spread for j in range(3)))
        light = .18+.23*max(0,n.dot(sun))+.10*max(0,z)
        leaf(p,n,rng.uniform(.40,.64),light)

def finish_mesh(name):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts,[],faces); data.update()
    attr = data.color_attributes.new(name='NaturalColour',type='BYTE_COLOR',domain='CORNER')
    for poly in data.polygons:
        for li in poly.loop_indices: attr.data[li].color = colours[poly.index]
    obj = bpy.data.objects.new(name,data); bpy.context.collection.objects.link(obj)
    color_material(obj)
    verts.clear(); faces.clear(); colours.clear()
    return obj

trees = [(-18,-2,.140054,12), (18,-4,.491365,13), (-17,-13,.980715,12),
         (-17,9,.666705,13), (17,12,.590452,14), (-23,2,1.532772,15),
         (23,5,.717884,16), (-22,-12,1.022115,14)]
for x,z,ground,height in trees:
    # Asymmetric masses occupy branch ends, with daylight between individual lobes.
    spread = height*.28
    yaw = rng.random()*math.tau
    for j in range(8):
        a = yaw+j*2.399963
        ring = spread*(.18 if j == 0 else rng.uniform(.68,1.12))
        centre = (x+math.cos(a)*ring, -z+math.sin(a)*ring,
                  ground+height*(.85 if j == 0 else rng.uniform(.73,.89)))
        crown_lobe(centre,(rng.uniform(2.0,2.8),rng.uniform(1.9,2.7),rng.uniform(1.35,1.9)))
crowns = finish_mesh('PD12_Hub_Foliage_Crowns')
bpy.data.objects['HubArt_Foliage'].hide_render = True
bpy.data.objects['HubArt_Foliage'].hide_set(True)
originals = [o for o in originals if o.name != 'HubArt_Foliage']

# Rotate separate courses gently, retaining their atlas UVs and collision envelope.
ruins = bpy.data.objects['HubArt_Ruins']
adjacency = [[] for _ in ruins.data.vertices]
for edge in ruins.data.edges:
    a,b = edge.vertices; adjacency[a].append(b); adjacency[b].append(a)
seen = set()
for start in range(len(adjacency)):
    if start in seen: continue
    stack = [start]; seen.add(start); group = []
    while stack:
        i = stack.pop(); group.append(i)
        for j in adjacency[i]:
            if j not in seen: seen.add(j); stack.append(j)
    centre = sum((ruins.data.vertices[i].co for i in group),Vector())/len(group)
    rotation = Matrix.Rotation(rng.uniform(-.065,.065),3,'Z')
    for i in group:
        v = ruins.data.vertices[i]
        p = rotation@(v.co-centre)
        p.z += .018*math.sin(p.x*4+p.y*2+centre.z)
        v.co = centre+p
ruins.data.update()

# Cascading creepers use each column's known footprint; no vines across entrances.
columns = [(-10,7,4.2),(10,6,2.4),(-12,-3,2.2),(7,-9,4.8),
           (14,-9,2.6),(-15,-20,2.8),(-8,-27,2.3)]
for x,z,height in columns:
    for strand in range(3):
        a = strand*2.15+.35
        for j in range(17):
            h = .15+(height+.25)*j/17
            drift = .14*math.sin(j*.62+strand)
            n = Vector((math.cos(a),math.sin(a),.12)).normalized()
            p = Vector((x+math.cos(a)*(.63+drift),-z+math.sin(a)*(.63+drift),h))
            leaf(p,n,rng.uniform(.11,.22),rng.uniform(.32,.55))
    for j in range(3):
        a = rng.random()*math.tau
        crown_lobe((x+math.cos(a)*.85,-z+math.sin(a)*.85,.35),(.65,.7,.38),18)

# Low, irregular islands soften the back rim without obstructing the route mouths.
for j in range(11):
    x = -3.8+j*.86; z = -12.9-rng.uniform(.15,2.1)
    crown_lobe((x,-z,.45+rng.uniform(0,.25)),(1.15,.9,.6),24)
dressing = finish_mesh('PD12_Hub_Foliage_Creepers')


bpy.ops.object.select_all(action='DESELECT')
for o in originals+[crowns,dressing]: o.select_set(True)
bpy.context.view_layer.objects.active = crowns
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/pd12-hub-art.blend'),compress=True)
target = ROOT/'public/models/hub-art.glb'
temporary = target.with_name('hub-art.next.glb')
bpy.ops.export_scene.gltf(filepath=str(temporary),export_format='GLB',use_selection=True,
                          export_image_format='JPEG',export_image_quality=94)
os.replace(temporary,target)
report = {'trees':len(trees),'columns':len(columns),'source':'pd11-hub-art.blend',
          'output':'pd12-hub-art.blend','bytes':target.stat().st_size,
          'collisionChanged':False}
(ROOT/'.artifacts/blender/pd12-hub-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('PD12_HUB '+json.dumps(report),flush=True)
