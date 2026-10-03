"""Phase 3 connector dressing; same wall footprints and unchanged colliders."""
import bpy
import math
import random
from mathutils import Vector, Matrix


def folded_leaves(obj):
    """Fold existing opaque leaf faces; keep stems and triangular grass unchanged."""
    old=obj.data
    attr=old.color_attributes.active_color
    if not attr:return
    points=[];faces=[];colors=[]
    for poly in old.polygons:
        ring=[old.vertices[i].co.copy() for i in poly.vertices]
        color=tuple(attr.data[poly.loop_start].color)
        start=len(points);points.extend(ring)
        if len(ring)==4:
            centre=sum(ring,Vector())/4
            width=min((ring[(i+1)%4]-ring[i]).length for i in range(4))
            centre+=poly.normal*width*.16
            middle=len(points);points.append(centre)
            for j in range(4):
                faces.append((start+j,start+(j+1)%4,middle))
                shade=.88 if j%2 else 1.06
                colors.append(tuple(c*shade for c in color[:3])+(1,))
        else:
            faces.append(tuple(range(start,start+len(ring))));colors.append(color)
    data=bpy.data.meshes.new(obj.name+' folded blades');data.from_pydata(points,[],faces);data.update()
    for mat in old.materials:data.materials.append(mat)
    tint=data.color_attributes.new(name=attr.name,type='BYTE_COLOR',domain='CORNER')
    for poly in data.polygons:
        for loop in poly.loop_indices:tint.data[loop].color=colors[poly.index]
    obj.data=data
    bpy.data.meshes.remove(old)


def dress_walls(root, height_at, visuals, plant):
    rng=random.Random(31003)
    with bpy.data.libraries.load(str(root/'art/source/world-blockout.blend'),link=False) as (src,dst):
        dst.objects=[name for name in src.objects if name.startswith('Broken wall')]
    walls=[]
    for source in dst.objects:
        # Library-loaded, unlinked objects have no evaluated world transform.
        # These authored blockouts are unparented; compose their stored pose.
        matrix=Matrix.LocRotScale(source.location,source.rotation_euler.to_quaternion(),source.scale)
        centre=matrix.translation
        if not (-21<centre.x<-4 and -40<-centre.y<-17):continue
        walls.append(source)
        bounds=[matrix@v.co for v in source.data.vertices]
        lo=Vector(tuple(min(p[k] for p in bounds) for k in range(3)))
        hi=Vector(tuple(max(p[k] for p in bounds) for k in range(3)))
        rows=max(2,math.ceil((hi.z-lo.z)/.48))
        course=(hi.z-lo.z)/rows
        for row in range(rows):
            # Closed courses retain the tested solid footprint, with a chipped
            # outside arris rather than uniformly softened pillow-shaped stones.
            bpy.ops.mesh.primitive_cube_add(size=1,location=((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z+(row+.5)*course))
            obj=bpy.context.object;obj.name='Connector ruin course'
            obj.scale=((hi.x-lo.x)+.025,(hi.y-lo.y)+.03,course+.014)
            bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
            bevel=obj.modifiers.new('Small fractured arris','BEVEL');bevel.width=.018;bevel.segments=1
            bpy.ops.object.modifier_apply(modifier=bevel.name)
            for v in obj.data.vertices:
                v.co.x+=rng.uniform(-.018,.018);v.co.y+=rng.uniform(-.015,.015)
            visuals.append(obj)
        # Small pieces seat the base on both playable approaches, below ankle
        # height so visual rubble does not become a new uncollidable obstacle.
        for j in range(3):
            x=centre.x+rng.uniform(-.58,.58);z=-centre.y+rng.choice((-1,1))*rng.uniform(.45,.72)
            if -14.8<x<-9.2:continue
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(x,-z,height_at(x,z)-.015))
            obj=bpy.context.object;obj.name='Connector embedded rubble'
            obj.scale=(rng.uniform(.22,.42),rng.uniform(.20,.36),.12)
            visuals.append(obj)
        for side in (-1,1):
            x=centre.x;z=-centre.y+side*.52
            plant('Broadleaf_Clump',Vector((x,-z,height_at(x,z)-.025)),(.48,.48,.48),(0,0,rng.random()*math.tau))
    assert len(walls)==8, f'Expected eight connector wall blocks, got {len(walls)}'
    return len(walls)
