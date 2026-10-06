"""PD04 geometry: fractured cavern, open oculus, walkable shores and descent.

PD05 adds metre-scaled UVs and reusable mineral stone textures. PD06 adds the
oculus light surface; light/fog are recreated in R3F. No chamber-sized atlas.
"""
import bpy
import math
import random
import json
import sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
from placed_art import merge
from cavern_materials import stone_material

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'.artifacts/blender'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
rng=random.Random(9284)
visuals=[]
solids=[]


def mesh(name, points, faces, solid=False, shore=False):
    data=bpy.data.meshes.new(name)
    data.from_pydata([(x,-z,y) for x,y,z in points],[],faces)
    data.update()
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj)
    colors=data.color_attributes.new(name='RockColor',type='BYTE_COLOR',domain='CORNER')
    runtime_colors=data.color_attributes.new(name='RuntimeRockColor',type='BYTE_COLOR',domain='CORNER')
    uv=data.uv_layers.new(name='StoneMetres')
    continuous='continuous fractured shell' in name or 'fractured passage' in name
    for poly in data.polygons:
        poly.use_smooth=continuous
        centre=poly.center
        # Broad structural value groups make planes legible without tiny noise.
        variation=rng.uniform(.98,1.02) if continuous else rng.uniform(.9,1.1)
        facing=.75+.25*abs(poly.normal.x)+.2*max(0,poly.normal.z)
        height=max(0,min(1,(centre.z+8)/27))
        shade=(.68+.5*height)*facing*variation
        base=(.13,.16,.19) if shore else (.075,.099,.128)
        # Limestone at the hall end settles gradually into the cavern palette.
        transition=max(0,min(1,(174-centre.y)/33)) if 'Descent' in name else 0
        base=tuple(c*(1-transition)+v*transition for c,v in zip(base,(.24,.245,.19)))
        # Dominant-axis projection at 512 texels/metre. Horizontal shelves use
        # X/Z, cliff faces use their tangent/height; no chamber-sized UV stretch.
        axis=max(range(3),key=lambda k:abs(poly.normal[k]))
        for loop in poly.loop_indices:
            co=data.vertices[data.loops[loop].vertex_index].co
            # Continuous bedrock uses a vertex-height gradient, avoiding the
            # radial triangle colour bands seen in the earlier roof screenshot.
            # Separate fracture plates retain crisp edges and face values.
            local_shade=(.72+.42*max(0,min(1,(co.z+8)/27))) if continuous else shade
            daylight=1
            if 'Descent' in name:
                # Enclosed rock receives progressively less hall daylight. Store
                # this broad occlusion in vertex colour, independent of camera fog.
                depth=max(0,min(1,(co.y-141)/17))
                daylight=1-depth*depth*(3-2*depth)
            colors.data[loop].color=tuple(c*local_shade for c in base)+(1,)
            # The established chamber appearance used the exporter's white
            # COLOR_0 fallback. Preserve it, and explicitly export the descent
            # occlusion in the primary colour channel understood by Three.js.
            value=.24+.66*daylight if 'Descent' in name else 1
            runtime_colors.data[loop].color=(value,value,value,1)
            pair=(co.y,co.z) if axis==0 else (co.x,co.z) if axis==1 else (co.x,co.y)
            uv.data[loop].uv=(pair[0]/2,pair[1]/2)
    visuals.append(obj)
    if solid:solids.append(obj)
    return obj


cx,cz=-12,-195
N=64
angles=[i*math.tau/N for i in range(N)]
levels=[(-9,25.5),(-3,25),(3,24),(9,21),(14,14),(18,4)]
points=[]
for k,(h,r) in enumerate(levels):
    for i,a in enumerate(angles):
        wave=.65*math.sin(a*7+.5)+.35*math.sin(a*13)
        rad=r+wave*(.35 if k==5 else 1)+rng.uniform(-.65,.65)
        shift=-10*(k/5)**2
        # Elongated, irregular fissure at the crown rather than a circular skylight.
        sx,sz=(.7,1.5) if k==5 else (1,1)
        y=h+(1.6*math.sin(a*5+k*.8) if k not in (0,) else 0)
        angle=a+.035*math.sin(i*1.8+k*1.5)
        points.append((cx+sx*rad*math.cos(angle),y,cz+shift+sz*rad*math.sin(angle)))
faces=[]
for k in range(len(levels)-1):
    for i in range(N):
        a=angles[i]+math.pi/N
        # The passage joins only the low northern wall; the roof stays continuous.
        if k<2 and abs(a-math.pi/2)<.16:continue
        j=(i+1)%N
        faces.extend([(k*N+i,(k+1)*N+i,(k+1)*N+j),(k*N+i,(k+1)*N+j,k*N+j)])
mesh('Cavern continuous fractured shell',points,faces,True)

# Long irregular escarpments follow the chamber walls. Their changing profiles
# create tall ledges and deep joints, avoiding a repeated brick/block pattern.
for i in range(42):
    a=i*math.tau/42+rng.uniform(-.04,.04)
    if abs(a-math.pi/2)<.24:continue
    radius=rng.uniform(23.5,25)
    width=rng.uniform(.8,1.8)
    height=rng.uniform(7,18)
    pts=[]
    for level,(h,dr,w) in enumerate([(-8,.5,1),(-4,-.2,.95),(height*.45-8,-.7,.8),(height-8,1,.45)]):
        for side in (-1,1):
            rr=radius+dr+rng.uniform(-.22,.22)
            tangent=side*width*w
            pts.append((cx+rr*math.cos(a)-tangent*math.sin(a),h,cz+rr*math.sin(a)+tangent*math.cos(a)))
    mesh('Vertical jointed rock face',pts,[(0,1,3,2),(2,3,5,4),(4,5,7,6)],True)

# Staggered fracture plates interrupt the chamber's radial construction. Each
# exposes a broad face and chipped side planes, with no common horizontal course.
for band in range(3):
    for i in range(18):
        a=i*math.tau/18+rng.uniform(-.09,.09)
        if abs(a-math.pi/2)<.28:continue
        h=(-4,3,10)[band]+rng.uniform(-1.4,1.4)
        width=rng.uniform(2.5,5.2);height=rng.uniform(5,10)
        # Local U runs around the wall, V rises and D projects into the chamber.
        shape=[(-width,-height*.5,0),(width*.7,-height*.5,.35),
               (width,height*.2,.8),(width*.35,height*.55,.3),
               (-width*.8,height*.42,.1)]
        front=[]
        for u,v,d in shape:
            y=max(-8.8,min(17,h+v))
            level=next(k for k in range(len(levels)-1) if levels[k][0]<=y<=levels[k+1][0])
            t=(y-levels[level][0])/(levels[level+1][0]-levels[level][0])
            # Bury each outline in the shell. The previous constant-radius
            # panels detached from the narrowing upper walls like pasted tiles.
            r=levels[level][1]*(1-t)+levels[level+1][1]*t+.6
            zshift=-10*((level+t)/5)**2
            front.append((cx+r*math.cos(a)-u*math.sin(a),y,cz+zshift+r*math.sin(a)+u*math.cos(a)))
        back=[(x+math.cos(a)*1.1,y,z+math.sin(a)*1.1) for x,y,z in front]
        centre=tuple(sum(p[k] for p in front)/5 for k in range(3))
        depth=rng.uniform(.35,.8)
        centre=(centre[0]-math.cos(a)*depth,centre[1]+.12,centre[2]-math.sin(a)*depth)
        # Broken non-coplanar facets replace the conspicuous flat pasted-on plates.
        mesh('Overlapping rock fracture plate',front+back+[centre],
             [(j,(j+1)%5,10) for j in range(5)]+
             [(j,j+5,(j+1)%5+5,(j+1)%5) for j in range(5)],True)

# Roof splinters reinforce the asymmetric opening, staying out of the sky hole.
for i in range(18):
    a=i*math.tau/18
    x=cx+math.cos(a)*4.1;z=cz-10+math.sin(a)*7.2
    w=rng.uniform(.6,1.25)
    mesh('Oculus fractured tooth',[(x-w,18,z),(x+w,18,z),
         (x+.2,15+rng.uniform(0,2),z+.5),(x,19,z+1.4)],
         [(0,2,1),(0,1,3),(1,2,3),(2,0,3)],True)

shore_shape=json.loads((ROOT/'src/config/cavern-shore.json').read_text())
def shore_radius(a):
    b,c,d=shore_shape['lobes']
    return shore_shape['radius']+b*math.sin(3*a)+c*math.cos(5*a)+d*math.sin(11*a)

# Discontinuous ledges overhang the pool and break the repeated bank arc; existing
# continuous walkable ground and its collision remain behind this visual edge.
for j in range(19):
    a=j*math.tau/19+.08*math.sin(j*2.7)
    if abs(a-math.pi/2)<.32:continue
    radius=shore_radius(a);r=radius-rng.uniform(.45,1.2)
    pts=[]
    for offset,rr in [(-.055,radius+1.1),(-.048,r),(.012,r-.25),(.07,r+.3),(.075,radius+1.1)]:
        pts.append((cx+rr*math.cos(a+offset),-7.45+rng.uniform(0,.025),cz+rr*math.sin(a+offset)))
    lower=[(x,-7.95,z) for x,y,z in pts]
    mesh('Irregular pool edge ledge',pts+lower,[(0,1,2,3,4)]+
         [(k,(k+1)%5,(k+1)%5+5,k+5) for k in range(5)],shore=True)

# The inner contour follows the existing pool, with broad horizontal bedrock
# plates. A continuous base under the fissures retains the resident walking level.
for i in range(N):
    a,b=angles[i],(i+1)*math.tau/N
    ra,rb=shore_radius(a),shore_radius(b)
    mesh('Shore continuous ground',[(cx+r*math.cos(t),-7.51,cz+r*math.sin(t))
         for r,t in ((ra,a),(27,a),(27,b),(rb,b))],[(3,2,1,0)],solid=True,shore=True)
    mesh('Shore fracture lip',[(cx+r*math.cos(t),h,cz+r*math.sin(t))
         for r,t,h in ((ra,a,-7.49),(rb,b,-7.49),(rb+.2,b,-9.1),(ra+.2,a,-9.1))],
         [(0,1,2,3)],shore=True)
    if i%2:continue
    for band in range(3):
        step=2*math.tau/N
        aa=a+step*(band*.37+.2*math.sin(i*1.3))+.0015
        bb=a+step+step*(band*.37+.2*math.sin((i+2)*1.3))-.0015
        def edge(k,t):
            return shore_radius(t)+k*3.2+(0 if k==0 else .55*math.sin(t*11+k*1.7)+.3*math.cos(t*17-k))
        inner_a=edge(band,aa)+.025;inner_b=edge(band,bb)+.025
        outer_a=edge(band+1,aa)-.025;outer_b=edge(band+1,bb)-.025
        mid=(aa+bb)/2
        # Staggered fracture boundaries avoid continuous radial tile joints.
        coords=[(inner_a,aa),(outer_a,aa),(edge(band+1,mid)-.06,mid+(bb-aa)*.1),
                (outer_b,bb),(inner_b,bb),(edge(band,mid)+.08,mid-(bb-aa)*.1)]
        top=[(cx+r*math.cos(t),-7.47+rng.uniform(-.012,.012),cz+r*math.sin(t)) for r,t in coords]
        pts=top+[(x,-7.64,z) for x,y,z in top]
        mesh('Broad shoreline bedrock',pts,[(0,1,2,3,4,5)]+[(j,(j+1)%6,(j+1)%6+6,j+6) for j in range(6)],shore=True)

# Large talus masses stay at the outer wall, away from the navigable shore loop.
for i in range(30):
    a=rng.random()*math.tau
    if abs(a-math.pi/2)<.25:continue
    r=rng.uniform(23,24)
    x,z=cx+r*math.cos(a),cz+r*math.sin(a)
    w=rng.uniform(.8,1.7);h=rng.uniform(.65,2.3)
    mesh('Wall foot fallen rock',[(x-w,-7.5,z-w),(x+w,-7.5,z-w),(x+w,-7.5,z+w),
         (x-w,-7.5,z+w),(x-w*.6,-7.5+h,z-.3),(x+w*.5,-7.5+h*.8,z+.4)],
         [(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4),(4,5,2)],True,True)

# One continuous passage skin, with staggered fractures along the slope. Its
# floor remains the resident ramp; the 5m lane is not narrowed by decoration.
pts=[]
for i in range(18):
    z=-141-i*33/17;y=1.65-i*9.15/17
    for j,(x,h) in enumerate([(-2.85,-.3),(-3.15,3.6),(-1.8,6.2),(0,6.8),(1.9,6.4),(3.2,3.5),(2.85,-.3)]):
        offset=0 if i in (0,17) else rng.uniform(-.13,.13)
        hh=h+(2 if i==0 and h>6 else 0)+offset
        pts.append((-12+x+offset,y+hh,z))
faces=[]
for i in range(17):
    for j in range(6):
        a=i*7+j;b=a+7
        faces.extend([(a,b,a+1),(a+1,b,b+1)])
passage=mesh('Descent fractured passage collision source',pts,faces,True)
visuals.remove(passage)
# Retain the tested collision shell. The visible rock vault opens above it at
# the hall end, so the descending roof no longer reads as a flat portal infill.
# Rounded, offset ring shoulders add depth without narrowing the five-metre lane.
vault=[]
for index,(x,y,z) in enumerate(pts):
    ring,j=divmod(index,7)
    t=ring/17
    lift=3.2*math.sin(min(1,t*3.5)*math.pi/2)*(1-t)**1.3
    weight=(0,.2,.85,1,.85,.2,0)[j]
    vault.append((x+(0 if j in (0,6) else .18*math.sin(ring*.9+j)),y+lift*weight,z))
mesh('Descent fractured passage',vault,faces)
# Connected, uneven rock ribs articulate the slope in silhouette. Their edges
# overlap the vault and feet are outside the walking lane, avoiding floating fins.
for ring in (2,5,9,13):
    rib=[]
    for dz in (-.22,.22):
        for j in range(7):
            x,y,z=vault[ring*7+j]
            inset=(0,.12,.20,.24,.20,.12,0)[j]
            rib.append((x+(inset if x<-12 else -inset),y-inset,z+dz))
    mesh('Descent connected rock seam',rib,[(j,j+7,j+8,j+1) for j in range(6)])
def descent_floor(z):return 1.65+(z+141)*9.15/33

# A buried continuous bed closes the daylight slit below the hall threshold and
# supports the joints. Visual only: the existing five-metre ramp stays resident.
za,zb=-140.65,-174.2
ya,yb=descent_floor(za)+.015,descent_floor(zb)+.015
mesh('Descent continuous floor bed',
     [(-14.86,ya,za),(-9.14,ya,za),(-9.14,yb,zb),(-14.86,yb,zb),
      (-14.86,ya-.38,za),(-9.14,ya-.38,za),(-9.14,yb-.38,zb),(-14.86,yb-.38,zb)],
     [(0,1,2,3),(0,4,5,1),(3,2,6,7),(0,3,7,4),(1,5,6,2)],shore=True)

# Irregular, staggered bedrock joints replace the straight centre seam. All top
# points remain on the walkable ramp plane; side skirts bury the outer joins.
for side in (-1,1):
    for i in range(23):
        za=min(-140.7,-140.7-i*1.5+(0 if side<0 else .65))
        zb=max(-174.15,min(-140.7,-140.7-(i+1)*1.5+(0 if side<0 else .65))+.015)
        if za<=-174.15:continue
        mid_a=-12+.26*math.sin(za*.69)
        mid_b=-12+.26*math.sin(zb*.69)
        edge_a=-12+side*(2.86+.08*math.sin(za*1.13))
        edge_b=-12+side*(2.86+.08*math.sin(zb*1.13))
        pts=[(edge_a,descent_floor(za)+.035,za),(mid_a+side*.012,descent_floor(za)+.035,za),
             (mid_b+side*.012,descent_floor(zb)+.035,zb),(edge_b,descent_floor(zb)+.035,zb)]
        mesh('Descent worn ledge',pts,[(0,1,2,3)],shore=True)

# Connected rock toes grow out of the wall and sink below the bed. Their inner
# edge stays outside the tested 5m lane, with broad planes instead of loose fins.
for side in (-1,1):
    for i in range(9):
        z=-142.2-i*3.65+(0 if side<0 else -.8)
        za,zb=max(-140.9,z+1.45),max(-174,z-1.55)
        foot_a,foot_b=descent_floor(za),descent_floor(zb)
        x=-12+side*2.56;outer=-12+side*3.35
        top=.55+.23*math.sin(i*1.8+side)
        mesh('Descent embedded wall toe',[(x,foot_a-.14,za),(x,foot_b-.14,zb),
             (outer,foot_b-.32,zb),(outer,foot_a-.32,za),
             (-12+side*2.85,foot_a+top,za-.15),(-12+side*3.02,foot_b+top*.7,zb+.18)],
             [(0,1,5,4),(0,4,3),(1,2,5),(3,4,5,2)],shore=True)

visual_count=len(visuals)
# The new chamber/passage skin supplies matching physical boundaries. Flat shore
# and ramp collision stay resident; the pool still has no walking floor.
copies=[]
for o in solids:
    c=o.copy();c.data=o.data.copy();bpy.context.collection.objects.link(c);copies.append(c)
collision=merge('CavernStructure_Collision',copies)
collision.data.materials.clear()
rock=merge('CavernStructure_Rock',visuals)
rock.data.materials.clear();rock.data.materials.append(stone_material('RuntimeRockColor'))
for poly in rock.data.polygons:poly.material_index=0
# Bright sky beyond the irregular roof slit. The surrounding rock masks this
# backing surface; it is visual only and belongs to the pool-reflection layer.
sky_points=[]
for i in range(24):
    a=i*math.tau/24
    r=1+.06*math.sin(a*7)+.04*math.cos(a*3)
    sky_points.append((-12+5*r*math.cos(a),205-9*r*math.sin(a),20.3))
sky_data=bpy.data.meshes.new('Cavern oculus sky surface')
sky_data.from_pydata(sky_points,[],[tuple(range(24))]);sky_data.update()
oculus=bpy.data.objects.new('Cavern_Oculus',sky_data);bpy.context.collection.objects.link(oculus)
sky_mat=bpy.data.materials.new('Cavern daylight opening');sky_mat.use_nodes=True
sky_nodes=sky_mat.node_tree.nodes;sky_nodes.clear()
emission=sky_nodes.new('ShaderNodeEmission');emission.inputs['Color'].default_value=(.67,.75,.78,1)
output=sky_nodes.new('ShaderNodeOutputMaterial')
sky_mat.node_tree.links.new(emission.outputs[0],output.inputs['Surface'])
oculus.data.materials.append(sky_mat)
for obj in (collision,rock):obj.data.validate(clean_customdata=True);obj.data.update()
bpy.ops.object.select_all(action='DESELECT')
for obj in (rock,collision,oculus):obj.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/cavern-structure.blend'),compress=True)
export=ROOT/'public/models/cavern-structure.glb'
bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=True,
                         export_vertex_color='NAME',export_vertex_color_name='RuntimeRockColor',
                         export_all_vertex_colors=False)
report={'stage':'PD07 continuous bedrock shading and cavern integration','structuralParts':visual_count,'solidParts':len(solids),
        'bytes':export.stat().st_size,'visualTriangles':sum(len(p.vertices)-2 for p in rock.data.polygons),
        'collisionTriangles':sum(len(p.vertices)-2 for p in collision.data.polygons),
        'openingTriangles':22,
        'materialStatus':'1024px colour/normal/roughness tiles at 2m repeat; runtime wet shoreline, local atmosphere and opening light',
        'texelsPerMetre':512}
(OUT/'cavern-structure-report.json').write_text(json.dumps(report,indent=2)+'\n')
from world_art_context import export_context
export_context()
print(json.dumps(report),flush=True)
