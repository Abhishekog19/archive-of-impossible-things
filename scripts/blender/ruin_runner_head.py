"""Connected facial relief, fitted eyelids and closed swept hair locks for PD08.

Coordinates are metres, -Y forward. This is an authored neutral sculpt study,
not deformation topology. Facial masks are also used to paint the UV skin map.
"""
import bpy
import math
import numpy as np
from mathutils import Vector


def build_head(mesh, loft, orb, cord, materials, material):
    M = materials
    # Directional fibre colour/normal detail travels with each curved hair lock.
    for key,colour in [('hair',(.22,.145,.095)),('hairlight',(.265,.18,.12))]:
        size=512
        v,u=np.mgrid[0:size,0:size]/(size-1)
        phase=u*math.tau*23+.35*np.sin(v*8)
        fibres=.065*np.sin(phase)+.035*np.sin(u*math.tau*61+v*3)
        rgba=np.ones((size,size,4),dtype=np.float32)
        rgba[:,:,:3]=np.array(colour)*(1+fibres+.07*v)[...,None]
        img=bpy.data.images.new(key+' directional strands',width=size,height=size)
        img.pixels.foreach_set(rgba.ravel());img.pack()
        mat=M[key];nodes=mat.node_tree.nodes;bsdf=nodes.get('Principled BSDF')
        tex=nodes.new('ShaderNodeTexImage');tex.image=img
        mat.node_tree.links.new(tex.outputs['Color'],bsdf.inputs['Base Color'])
        normal=np.ones((size,size,4),dtype=np.float32)
        normal[:,:,0]=.5+.055*np.cos(phase)
        normal[:,:,1]=.5
        normal[:,:,2]=.998
        nimg=bpy.data.images.new(key+' fine strand normals',width=size,height=size)
        nimg.colorspace_settings.name='Non-Color';nimg.pixels.foreach_set(normal.ravel());nimg.pack()
        nt=nodes.new('ShaderNodeTexImage');nt.image=nimg
        nm=nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.45
        mat.node_tree.links.new(nt.outputs['Color'],nm.inputs['Color'])
        mat.node_tree.links.new(nm.outputs['Normal'],bsdf.inputs['Normal'])
    profile = np.array([
        [1.467,.019,.030,-.008], [1.479,.035,.045,-.004],
        [1.497,.055,.060,.002], [1.521,.073,.070,.008],
        [1.548,.080,.079,.010], [1.575,.086,.083,.012],
        [1.600,.081,.083,.014], [1.627,.082,.082,.015],
        [1.657,.079,.078,.017], [1.682,.064,.062,.018],
        [1.704,.029,.032,.019], [1.711,.002,.002,.019],
    ])

    def gaussian(x, z, cx, cz, sx, sz):
        return np.exp(-((x-cx)/sx)**2-((z-cz)/sz)**2)

    def profile_value(z, column):
        # C1-continuous Hermite cross sections avoid horizontal shading shelves
        # at jaw/cheek/temple control rows, visible with ordinary directional light.
        xs=profile[:,0];ys=profile[:,column]
        slopes=np.gradient(ys,xs)
        i=np.clip(np.searchsorted(xs,z,side='right')-1,0,len(xs)-2)
        span=xs[i+1]-xs[i];t=np.clip((z-xs[i])/span,0,1)
        return ((2*t**3-3*t*t+1)*ys[i]+(t**3-2*t*t+t)*span*slopes[i]
            +(-2*t**3+3*t*t)*ys[i+1]+(t**3-t*t)*span*slopes[i+1])

    def surface(a, z):
        rx=profile_value(z,1)
        ry=profile_value(z,2)
        cy=profile_value(z,3)
        x=rx*np.cos(a)
        y=cy+ry*np.sin(a)
        front=np.maximum(0,-np.sin(a))**6
        relief=(.014*gaussian(x,z,0,1.589,.012,.035)
            + .025*gaussian(x,z,0,1.558,.012,.012)
            + .009*gaussian(x,z,0,1.525,.035,.018)
            + .010*gaussian(x,z,0,1.487,.029,.016))
        for s in (-1,1):
            relief += .011*gaussian(x,z,s*.051,1.572,.024,.021)
            relief += .009*gaussian(x,z,s*.033,1.622,.025,.012)
            relief -= .008*gaussian(x,z,s*.035,1.600,.022,.013)
            relief -= .004*gaussian(x,z,s*.059,1.533,.016,.018)
            relief += .004*gaussian(x,z,s*.012,1.550,.007,.007)
        return x,y-front*relief,z

    # Painted skin variation follows anatomy; small freckles on cheeks and nose.
    n=1024
    v,u=np.mgrid[0:n,0:n]/(n-1)
    a=u*math.tau
    z=profile[0,0]+v*(profile[-1,0]-profile[0,0])
    x,_,_=surface(a,z)
    front=np.maximum(0,-np.sin(a))**6
    rgb=np.broadcast_to([.72,.535,.425],(n,n,3)).copy()
    blush=front*(gaussian(x,z,0,1.556,.024,.018)
        + gaussian(x,z,-.052,1.568,.025,.017)+gaussian(x,z,.052,1.568,.025,.017))
    rgb+=blush[...,None]*np.array([.035,-.008,-.008])
    rng=np.random.default_rng(203)
    pores=rng.normal(0,.0025,(n,n))
    rgb+=pores[...,None]
    for _ in range(65):
        cx=rng.uniform(-.065,.065);cz=rng.uniform(1.554,1.582)
        freckle=gaussian(x,z,cx,cz,rng.uniform(.0003,.0008),rng.uniform(.0004,.0009))*front
        rgb-=freckle[...,None]*np.array([.09,.085,.063])
    face=material('Anatomically painted skin',(.72,.535,.425),roughness=.64)
    image=bpy.data.images.new('Face skin cheek variation and freckles',width=n,height=n)
    rgba=np.ones((n,n,4),dtype=np.float32);rgba[:,:,:3]=rgb
    image.pixels.foreach_set(rgba.ravel());image.pack()
    nodes=face.node_tree.nodes;bsdf=nodes.get('Principled BSDF')
    tex=nodes.new('ShaderNodeTexImage');tex.image=image
    face.node_tree.links.new(tex.outputs['Color'],bsdf.inputs['Base Color'])
    # Subtle pore normals survive GLB export; no baked
    # directional shadows or a painted highlight that would stick to the face.
    normal=np.ones((n,n,4),dtype=np.float32)
    normal[:,:,0]=.5+rng.normal(0,.008,(n,n))
    normal[:,:,1]=.5+rng.normal(0,.008,(n,n))
    normal[:,:,2]=.999
    skin_normal=bpy.data.images.new('Skin pore normals',width=n,height=n)
    skin_normal.colorspace_settings.name='Non-Color'
    skin_normal.pixels.foreach_set(normal.ravel());skin_normal.pack()
    nt=nodes.new('ShaderNodeTexImage');nt.image=skin_normal
    nm=nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.28
    face.node_tree.links.new(nt.outputs['Color'],nm.inputs['Color'])
    face.node_tree.links.new(nm.outputs['Normal'],bsdf.inputs['Normal'])
    M['face']=face
    M['lid']=material('Eyelid warm skin',(.46,.255,.175),roughness=.7)
    M['lips']=material('Natural muted lips',(.33,.15,.107),roughness=.64)
    M['crease']=material('Soft facial creases',(.12,.05,.03))

    verts=[];uv=[];faces=[]
    rows=105;columns=144
    for j in range(rows+1):
        zz=profile[0,0]+j/rows*(profile[-1,0]-profile[0,0])
        for i in range(columns+1):
            verts.append(tuple(float(v) for v in surface(i/columns*math.tau,zz)))
            uv.append((i/columns,j/rows))
    for j in range(rows):
        for i in range(columns):
            k=j*(columns+1)+i
            face_indices=(k,k+1,k+columns+2,k+columns+1)
            x,y,z=np.mean([verts[q] for q in face_indices],axis=0)
            faces.append(face_indices)
    mesh('Continuous sculpted face skull jaw and nose',verts,faces,'face',uv)

    def front_y(x,z):
        radius=float(profile_value(z,1))
        return float(surface(-math.acos(max(-1,min(1,x/radius))),z)[1])

    def eye_surface(name,cx,cz,rx,rz,mat,offset):
        verts=[(cx,front_y(cx,cz)-offset,cz)];faces=[]
        for j in range(1,7):
            r=j/6
            for i in range(49):
                a=i/48*math.tau
                x=cx+rx*r*math.cos(a);z=cz+rz*r*math.sin(a)
                if mat in ('iris','pupil'):
                    aperture=.0078*math.sqrt(max(0,1-((x-cx)/.019)**2))
                    z=max(1.601-aperture+.00025,min(1.601+aperture-.00025,z))
                verts.append((x,front_y(x,z)-offset-.001*(1-r*r),z))
        for i in range(48):faces.append((0,1+i,2+i))
        for j in range(5):
            for i in range(48):
                k=1+j*49+i;faces.append((k,k+49,k+50,k+1))
        return mesh(name,verts,faces,mat)

    for s in (-1,1):
        cx=s*.034;cz=1.601
        # Fit the visible corneal patch to the sculpted socket. A whole sphere
        # intersects this neutral sculpt; deformation topology is a later gate.
        eye_surface('Fitted almond eye',cx,cz,.019,.0078,'white',.0012)
        eye_surface('Hazel iris',cx,cz+.0013,.007,.007,'iris',.0024)
        eye_surface('Pupil',cx,cz+.0013,.003,.0035,'pupil',.0032)
        # Small directional fibre strokes give the iris depth without a giant
        # anime highlight or painted black outline around the entire eye.
        for k in range(26):
            a=k/26*math.tau
            points=[]
            for radius in (.0035,.006):
                x=cx+math.cos(a)*radius;z=cz+math.sin(a)*radius
                points.append((x,front_y(x,z)-.0032,z))
            cord('Iris radial fibre',points,.00015,'hairlight',1)
        orb('Corneal highlight',(cx-.002,front_y(cx-.002,cz+.002)-.004,cz+.002),(.00065,.0003,.00065),'white',12,8)
        verts=[];faces=[];uv=[]
        for row in range(4):
            t=row/3
            for i in range(49):
                a=i/48*math.tau
                dx=(.019+.006*t)*math.cos(a)
                dz=(.0078+.006*t)*math.sin(a)
                xx=cx+dx;zz=cz+dz
                radius=float(profile_value(zz,1))
                _,outer,_=surface(-math.acos(max(-1,min(1,xx/radius))),zz)
                yy=float(outer)-.0012*(1-t)-.0012*math.sin(t*math.pi)
                verts.append((cx+dx,yy,cz+dz))
                uv.append(((-math.acos(max(-1,min(1,xx/radius))))%math.tau/math.tau,
                    (zz-profile[0,0])/(profile[-1,0]-profile[0,0])))
        for row in range(3):
            for i in range(48):
                k=row*49+i;faces.append((k,k+49,k+50,k+1))
        mesh('Contoured upper and lower eyelid',verts,faces,'face',uv,sub=1)
        cord('Fine upper eyelash edge',[(cx+.019*math.cos(a),
            front_y(cx+.019*math.cos(a),cz+.0078*math.sin(a))-.002,
            cz+.0078*math.sin(a)) for a in np.linspace(.08,math.pi-.08,25)],.00048,'hair')
        cord('Brow base',[(s*(.015+t*.046),-.075+.025*t*t,1.621+.006*math.sin(t*math.pi)-.004*t)
            for t in np.linspace(0,1,18)],.0015,'hair')
        for k in range(40):
            t=k/39
            xx=s*(.015+t*.046)
            zz=1.621+.006*math.sin(t*math.pi)-.004*t
            yy=-.075+.025*t*t
            cord('Individual brow hair',[(xx,yy,zz),(xx+s*.003,yy-.001,zz+.0025*(1-t))],.00045,'hair',1)
        # Ear rim, concha and tragus; no flat dark oval pasted on the ear.
        orb('Ear cartilage',(s*.084,.011,1.570),(.015,.015,.028),'skin',24,16)
        orb('Ear concha',(s*.093,-.001,1.571),(.007,.006,.015),'lid',20,12)
        cord('Ear helix',[(s*(.085+.013*math.cos(a)),-.003+.006*math.cos(a),1.572+.026*math.sin(a))
            for a in np.linspace(-1.8,1.8,20)],.0025,'skin')
        orb('Nostril',(s*.008,-.09,1.551),(.0018,.001,.0012),'crease',16,8)

    # Cupid's bow and lips are surfaces with a tapered vermilion border.
    for upper in (True,False):
        verts=[];faces=[]
        for j in range(4):
            t=j/3
            for i in range(41):
                x=(i/40-.5)*.052
                f=max(0,1-(x/.026)**2)
                seam=1.526+.0017*(abs(x)/.026)**2
                height=(.0035+.002*math.exp(-((abs(x)-.008)/.004)**2)) if upper else -.006
                z=seam+height*t*f
                y=-.073-.007*f-.002*math.sin(t*math.pi)*f
                verts.append((x,y,z))
        for j in range(3):
            for i in range(40):
                k=j*41+i;faces.append((k,k+1,k+42,k+41))
        mesh('Upper lip cupid bow' if upper else 'Lower lip volume',verts,faces,'lips',sub=1)
    cord('Mouth separation',[(x,-.0805+.007*(x/.026)**2,1.526+.0017*(x/.026)**2)
        for x in np.linspace(-.025,.025,30)],.00045,'crease')

    # Closed, tapered locks follow cubic curves in a transported local frame.
    # Unlike flat strips, they retain volume from side/back and cannot reveal
    # black undersides when the camera or light changes.
    def lock(name,control,width,depth,seed):
        control=[Vector(p) for p in control]
        verts=[];faces=[];uv=[]
        segments=18;sides=10
        rng=np.random.default_rng(seed)
        phase=rng.uniform(0,math.tau)
        for j in range(segments+1):
            t=j/segments
            p=(1-t)**3*control[0]+3*(1-t)**2*t*control[1]+3*(1-t)*t*t*control[2]+t**3*control[3]
            tangent=(3*(1-t)**2*(control[1]-control[0])+6*(1-t)*t*(control[2]-control[1])+3*t*t*(control[3]-control[2])).normalized()
            normal=(p-Vector((0,.017,1.62))).normalized()
            across=tangent.cross(normal).normalized()
            normal=across.cross(tangent).normalized()
            taper=max(.015,math.sin(math.pi*(.18+.82*t))**.65)
            for i in range(sides+1):
                a=i/sides*math.tau
                ridge=1+.10*math.sin(a*5+phase+t*4)
                q=p+across*(math.cos(a)*width*taper)+normal*(math.sin(a)*depth*taper*ridge)
                verts.append(tuple(q));uv.append((i/sides,t))
        for j in range(segments):
            for i in range(sides):
                k=j*(sides+1)+i;faces.append((k,k+1,k+sides+2,k+sides+1))
        faces += [tuple(range(sides-1,-1,-1)),tuple(segments*(sides+1)+i for i in range(sides))]
        mesh(name,verts,faces,'hairlight' if seed%7==0 else 'hair',uv)

    loft('Fitted hair mass',[(1.594,.073,.064,0,.023),(1.63,.088,.079,0,.02),
        (1.672,.078,.07,0,.019),(1.705,.045,.044,-.006,.018),
        (1.720,.004,.006,-.009,.018)],'hair',n=36,sub=1)
    # Deliberately varied direction, length and grouping around an offset part.
    rng=np.random.default_rng(17)
    for k in range(27):
        x=-.075+k/26*.145
        lift=float(rng.uniform(-.008,.012))
        lock('Swept volumetric fringe',[(.035+.012*math.sin(k),.015,1.69),
            (x+.041,-.035,1.737+lift),(x-.027,-.091,1.68+lift),
            (x-.036,-.084,1.615+float(rng.uniform(-.004,.04)))],
            float(rng.uniform(.005,.010)),.0045,k+1)
    for k in range(16):
        a=k/16*math.tau
        lock('Broken crown silhouette',[(.048*math.cos(a),.018+.044*math.sin(a),1.679),
            (.085*math.cos(a+.25),.018+.08*math.sin(a+.25),1.726),
            (.108*math.cos(a+.45),.018+.10*math.sin(a+.45),1.698),
            (.11*math.cos(a+.55),.018+.107*math.sin(a+.55),1.66)],.012,.006,k+30)
    for k in range(24):
        a=k/23*math.pi
        # Side and back arc only; leave the forehead / eyes exposed.
        lock('Layered side and nape',[(.075*math.cos(a),.014+.059*math.sin(a),1.674),
            (.10*math.cos(a),.014+.09*math.sin(a),1.638),
            (.105*math.cos(a+.08),.014+.09*math.sin(a+.08),1.583),
            (.097*math.cos(a+.13),.014+.09*math.sin(a+.13),1.551+float(rng.uniform(-.009,.012)))],
            .013,.005,k+60)
