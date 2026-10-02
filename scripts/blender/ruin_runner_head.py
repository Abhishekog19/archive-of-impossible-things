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
    for key,colour in [('hair',(.14,.073,.038)),('hairlight',(.20,.115,.060))]:
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
        [1.461,.010,.016,.018], [1.467,.022,.028,.008], [1.479,.037,.044,.004],
        [1.497,.057,.059,.005], [1.521,.072,.070,.008],
        [1.548,.081,.079,.010], [1.575,.084,.083,.012],
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
        relief=(.022*gaussian(x,z,0,1.586,.012,.036)
            + .029*gaussian(x,z,0,1.558,.015,.017)
            + .009*gaussian(x,z,0,1.525,.035,.018)
            + .004*gaussian(x,z,0,1.490,.038,.022))
        for s in (-1,1):
            relief += .010*gaussian(x,z,s*.051,1.572,.029,.022)
            relief += .006*gaussian(x,z,s*.033,1.622,.028,.014)
            relief -= .008*gaussian(x,z,s*.035,1.600,.024,.019)
            relief -= .0015*gaussian(x,z,s*.059,1.533,.021,.022)
            relief += .004*gaussian(x,z,s*.012,1.550,.007,.007)
            # The superior lid crease belongs to the continuous skin surface.
            # It fades before either corner instead of tracing an entire ring.
            u=np.clip((x-s*.034)/.021,-1,1)
            fade=np.maximum(0,1-u*u)**.70
            lid_z=1.601+.0016*s*u+.010*fade
            relief -= .0008*fade*np.exp(-((z-lid_z-.003)/.0011)**2)
            relief += .0006*fade*np.exp(-((z-lid_z-.001)/.0012)**2)
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
    M['lips']=material('Natural muted lips',(.40,.22,.16),roughness=.64)
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

    eye_width=.021

    def eye_edge(u,side,upper):
        # Unequal arcs, with a lower tear duct and lifted outer corner. A circle
        # makes both the aperture and the lid look like an applied plastic ring.
        fullness=max(0,1-u*u)**.70
        corner=.0016*side*u
        return corner+(.0080 if upper else -.0066)*fullness

    def eye_surface(name,cx,cz,rx,rz,mat,offset):
        verts=[(cx,front_y(cx,cz)-offset,cz)];faces=[]
        for j in range(1,7):
            r=j/6
            for i in range(49):
                a=i/48*math.tau
                x=cx+rx*r*math.cos(a);z=cz+rz*r*math.sin(a)
                side=1 if cx>0 else -1
                if mat=='white':
                    z=cz+eye_edge(math.cos(a),side,math.sin(a)>=0)*r
                if mat in ('iris','pupil'):
                    u=(x-cx)/eye_width
                    z=max(1.601+eye_edge(u,side,False)+.00015,
                        min(1.601+eye_edge(u,side,True)-.00015,z))
                verts.append((x,front_y(x,z)-offset-.002*(1-r*r),z))
        for i in range(48):faces.append((0,1+i,2+i))
        for j in range(5):
            for i in range(48):
                k=1+j*49+i;faces.append((k,k+49,k+50,k+1))
        return mesh(name,verts,faces,mat)

    for s in (-1,1):
        cx=s*.034;cz=1.601
        # Fit the visible corneal patch to the sculpted socket. A whole sphere
        # intersects this neutral sculpt; deformation topology is a later gate.
        eye_surface('Fitted almond eye',cx,cz,eye_width,.010,'white',.0009)
        eye_surface('Hazel iris',cx,cz+.001,.010,.010,'iris',.0020)
        eye_surface('Pupil',cx,cz+.001,.0035,.0035,'pupil',.0027)
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
        for upper in (True,False):
            verts=[];faces=[];uv=[]
            for row in range(6):
                t=row/5
                for i in range(49):
                    u=i/24-1
                    xx=cx+u*(eye_width+.005*t)
                    edge=eye_edge(u,s,upper)
                    zz=cz+edge+(1 if upper else -1)*.005*t*max(0,1-u*u)**.5
                    radius=float(profile_value(zz,1))
                    # Flush outside edge and restrained waterline thickness.
                    yy=front_y(xx,zz)-(.0024 if upper else .0013)*(1-t)**2
                    verts.append((xx,yy,zz))
                    uv.append(((-math.acos(max(-1,min(1,xx/radius))))%math.tau/math.tau,
                        (zz-profile[0,0])/(profile[-1,0]-profile[0,0])))
            for row in range(5):
                for i in range(48):
                    k=row*49+i;faces.append((k,k+49,k+50,k+1))
            mesh('Upper lid transition' if upper else 'Lower lid transition',verts,faces,'face',uv)
        cord('Fine upper lash line',[(cx+u*eye_width,
            front_y(cx+u*eye_width,cz+eye_edge(u,s,True))-.0013,
            cz+eye_edge(u,s,True)) for u in np.linspace(-.97,.97,32)],.00035,'hair')
        # Broad feathered brow silhouette, seated on the actual forehead rather
        # than a floating constant-depth curve.
        verts=[];faces=[]
        for i in range(33):
            t=i/32;xx=s*(.013+t*.049)
            zz=1.620+.005*math.sin(t*math.pi)-.005*t
            width=.0002+.0035*math.sin(math.pi*(.025+.975*t))**.5
            for dz in (-width,width):
                verts.append((xx,front_y(xx,zz+dz)-.0006,zz+dz))
        for i in range(32):
            k=i*2;faces.append((k,k+2,k+3,k+1))
        mesh('Tapered feathered brow',verts,faces,'hair')
        for k in range(26):
            t=k/25;xx=s*(.013+t*.048)
            zz=1.620+.005*math.sin(t*math.pi)-.005*t
            endz=zz+.0025*(1-t)
            cord('Individual brow hair',[(xx,front_y(xx,zz)-.0009,zz),
                (xx+s*.002,front_y(xx+s*.002,endz)-.0009,endz)],.00022,'hairlight',1)
        # Ear rim, concha and tragus; no flat dark oval pasted on the ear.
        orb('Ear cartilage',(s*.084,.011,1.570),(.015,.015,.028),'skin',24,16)
        orb('Ear concha',(s*.090,.003,1.571),(.006,.003,.012),'lid',20,12)
        cord('Ear helix',[(s*(.085+.013*math.cos(a)),-.003+.006*math.cos(a),1.572+.026*math.sin(a))
            for a in np.linspace(-1.8,1.8,20)],.0025,'skin')
        nx=s*.0075;nz=1.548
        orb('Nostril',(nx,front_y(nx,nz)-.0005,nz),(.0014,.0007,.00065),'crease',16,8)

    # Cupid's bow and lips are surfaces with a tapered vermilion border.
    for upper in (True,False):
        verts=[];faces=[]
        for j in range(4):
            t=j/3
            for i in range(41):
                x=(i/40-.5)*.059
                f=max(0,1-(x/.0295)**2)
                seam=1.526+.0015*(abs(x)/.0295)**2+.0008*x/.0295
                height=(.002+.0015*math.exp(-((abs(x)-.008)/.004)**2)) if upper else -.004
                z=seam+height*t*f
                y=front_y(x,z)-.0006-.002*math.sin(t*math.pi)*f
                verts.append((x,y,z))
        for j in range(3):
            for i in range(40):
                k=j*41+i;faces.append((k,k+1,k+42,k+41))
        mesh('Upper lip cupid bow' if upper else 'Lower lip volume',verts,faces,'lips',sub=1)
    cord('Mouth separation',[(x,front_y(x,1.526+.0015*(x/.0295)**2+.0008*x/.0295)-.001,
        1.526+.0015*(x/.0295)**2+.0008*x/.0295)
        for x in np.linspace(-.029,.029,30)],.0003,'crease')

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
            taper=max(.008,math.sin(math.pi*(.10+.90*t))**.8)
            for i in range(sides+1):
                a=i/sides*math.tau
                ridge=1+.06*math.sin(a*5+phase+t*4)
                q=p+across*(math.cos(a)*width*taper)+normal*(math.sin(a)*depth*taper*ridge)
                verts.append(tuple(q));uv.append((i/sides,t))
        for j in range(segments):
            for i in range(sides):
                k=j*(sides+1)+i;faces.append((k,k+1,k+sides+2,k+sides+1))
        faces += [tuple(range(sides-1,-1,-1)),tuple(segments*(sides+1)+i for i in range(sides))]
        mesh(name,verts,faces,'hairlight' if seed%7==0 else 'hair',uv)

    # Fit the cap to the skull itself. The old independent loft passed inside
    # the occiput and exposed a bald crescent in the rear three-quarter view.
    verts=[];faces=[];uv=[]
    for j in range(25):
        t=j/24
        for i in range(73):
            a=i/72*math.tau
            front=max(0,-math.sin(a));back=max(0,math.sin(a))
            hairline=1.605+.048*front-.040*back
            z=hairline+(1.715-hairline)*t
            rx=float(profile_value(z,1))+.004
            ry=float(profile_value(z,2))+.004
            cy=float(profile_value(z,3))
            verts.append((rx*math.cos(a),cy+ry*math.sin(a),z));uv.append((i/72,t))
    for j in range(24):
        for i in range(72):
            k=j*73+i;faces.append((k,k+1,k+74,k+73))
    mesh('Skull fitted hair foundation',verts,faces,'hair',uv)
    # Art-directed primary groups. The reference has a raised offset part and
    # broad swept masses with broken ends, not one evenly spaced comb fringe.
    rng=np.random.default_rng(17)
    groups=[
        ([(.033,-.019,1.696),(.025,-.058,1.766),(-.047,-.105,1.704),(-.098,-.051,1.670)],.024,.008),
        ([(.027,-.035,1.701),(.014,-.090,1.747),(-.055,-.105,1.665),(-.087,-.076,1.621)],.021,.007),
        ([(.026,-.050,1.700),(.009,-.100,1.718),(-.021,-.104,1.651),(-.047,-.078,1.624)],.018,.006),
        ([(.036,-.042,1.696),(.046,-.090,1.720),(.030,-.104,1.657),(.012,-.085,1.642)],.013,.006),
        ([(.044,-.022,1.697),(.085,-.057,1.744),(.086,-.080,1.677),(.077,-.063,1.639)],.021,.008),
        ([(.050,.001,1.696),(.096,-.019,1.720),(.104,-.044,1.665),(.121,-.015,1.643)],.020,.007),
        ([(.017,.016,1.701),(-.006,-.009,1.757),(-.074,-.037,1.724),(-.118,-.005,1.710)],.025,.009),
        ([(-.015,.020,1.701),(-.044,.010,1.742),(-.106,-.025,1.692),(-.123,-.020,1.670)],.022,.008),
        ([(-.055,-.020,1.674),(-.095,-.063,1.689),(-.094,-.066,1.631),(-.107,-.029,1.610)],.018,.007),
        ([(.065,-.007,1.674),(.099,-.037,1.649),(.081,-.043,1.601),(.088,-.008,1.577)],.017,.006),
    ]
    for k,(control,width,depth) in enumerate(groups):
        lock('Sculpted swept hair group',control,width,depth,k+101)
        # A few attached sub-locks split each mass near its tip; their roots and
        # direction follow the primary volume so they cannot float like a comb.
        for j in (-1,1):
            shift=j*width*.42
            fine=[(x+shift,y-.003,z+.0015) for x,y,z in control]
            fine[-1]=(fine[-1][0]+j*.004,fine[-1][1],fine[-1][2]+j*.006)
            lock('Attached split hair tip',fine,width*.27,depth*.35,k*2+j+160)
    for k in range(16):
        a=k/16*math.tau
        lock('Broken crown silhouette',[(.048*math.cos(a),.018+.044*math.sin(a),1.679),
            (.085*math.cos(a+.25),.018+.08*math.sin(a+.25),1.726+.009*math.sin(k*2)),
            (.108*math.cos(a+.45),.018+.10*math.sin(a+.45),1.698),
            (.11*math.cos(a+.55),.018+.107*math.sin(a+.55),1.66+.012*math.cos(k*3))],.016,.006,k+30)
    for k in range(24):
        a=k/23*math.pi
        # Side and back arc only; leave the forehead / eyes exposed.
        lock('Layered side and nape',[(.075*math.cos(a),.014+.059*math.sin(a),1.674),
            (.10*math.cos(a),.014+.09*math.sin(a),1.638),
            (.105*math.cos(a+.08),.014+.09*math.sin(a+.08),1.583),
            (.097*math.cos(a+.13),.014+.09*math.sin(a+.13),1.551+float(rng.uniform(-.009,.012)))],
            .013,.005,k+60)
