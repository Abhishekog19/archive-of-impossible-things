"""Opaque, dimensional background crowns with folded leaves and no atlas cost."""
import bpy, bmesh, math, random
from mathutils import Vector


def layered_crown(name, centre, radius, seed):
    rng=random.Random(seed);c=Vector(centre);r=Vector(radius)
    verts=[];faces=[];colours=[]
    sun=Vector((-.4,-.3,.85)).normalized()
    def face(points, shade):
        start=len(verts);verts.extend(points)
        faces.append(tuple(range(start,len(verts))))
        colours.append((.09*shade,.14*shade,.038*shade,1))
    for lobe in range(3):
        a=lobe*2.39996+seed
        offset=Vector((math.cos(a)*r.x*.43,math.sin(a)*r.y*.43,r.z*rng.uniform(-.2,.35)))
        scale=Vector((r.x*.62,r.y*.62,r.z*.82))
        bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=1,radius=1);bm.normal_update()
        for f in bm.faces:
            points=[c+offset+Vector(tuple(v.co[k]*scale[k]*(.84+.12*math.sin(v.co.x*9+v.co.y*6)) for k in range(3))) for v in f.verts]
            face(points,.45+.45*max(0,f.normal.dot(sun)))
        bm.free()
        for i in range(16):
            z=1-2*(i+.5)/16;a=i*2.39996
            n=Vector((math.sqrt(1-z*z)*math.cos(a),math.sqrt(1-z*z)*math.sin(a),z))
            p=c+offset+Vector(tuple(n[k]*scale[k] for k in range(3)))
            u=n.cross(Vector((0,0,1))).normalized();v=n.cross(u)
            size=rng.uniform(.22,.45)*min(1.5,max(radius)*.4)
            ring=[p-u*size,p-v*size*.6,p+u*size,p+v*size*.6]
            peak=p+n*size*.18
            light=.58+.48*max(0,n.dot(sun))
            for j in range(4):face([ring[j],ring[(j+1)%4],peak],light*(.9 if j<2 else 1.05))
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
    attr=data.color_attributes.new(name='CanopyColor',type='BYTE_COLOR',domain='CORNER')
    for p in data.polygons:
        for li in p.loop_indices:attr.data[li].color=colours[p.index]
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj)
    return obj
