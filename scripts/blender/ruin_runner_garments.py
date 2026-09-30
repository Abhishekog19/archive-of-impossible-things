"""Tailored neutral garments: tension folds, open cuffs and separate cape panel.

These are authored rest shapes, not a cloth simulation. Keep the surfaces separate
for later deformation/secondary bones. Coordinates are metres, -Y forward.
"""
import math
import numpy as np


def build_garments(mesh, cord):
    def patch(name, rows, columns, surface, mat, thickness=.0018, descending=True):
        verts=[];uv=[];faces=[]
        for j in range(rows+1):
            for i in range(columns+1):
                u=i/columns;t=j/rows
                verts.append(surface(u,t));uv.append((u,1-t))
        for j in range(rows):
            for i in range(columns):
                k=j*(columns+1)+i
                face=(k,k+1,k+columns+2,k+columns+1)
                faces.append(tuple(reversed(face)) if descending else face)
        return mesh(name,verts,faces,mat,uv,solid=thickness)

    def fold(u,centre,width,amplitude):
        q=(u-centre)/width
        # Narrow crest with broad, shallow troughs; each fold has its own origin.
        return amplitude*(math.exp(-q*q)-.38*math.exp(-(q/2.0)**2))

    def torso(u,t):
        a=u*math.tau;z=.995+t*.395
        rx=float(np.interp(t,[0,.12,.35,.68,.87,1],[.144,.167,.175,.183,.168,.060]))
        ry=float(np.interp(t,[0,.12,.35,.68,.87,1],[.090,.111,.111,.104,.086,.052]))
        # Folds converge into belt gathers and relax above the stomach.
        f=0
        for centre,amp,width in [(.12,.011,.018),(.28,.007,.023),(.49,.010,.020),
                                  (.60,.008,.024),(.71,.012,.018),(.87,.010,.022)]:
            f+=fold(u,centre+.035*t,width+.025*t,amp)*(1-.6*t)
        # Chest strap pulls a few oblique creases through the front linen.
        front=max(0,-math.sin(a))
        diagonal=.010*math.sin(t*24+u*16)*math.exp(-((t-.42)/.28)**2)*front
        return ((rx+f)*math.cos(a),(ry+f+diagonal)*math.sin(a),z)

    patch('Linen shirt with belt tension folds',34,96,torso,'linen',descending=False)

    # Three overlapping cut pieces replace the flared, uninterrupted skirt cone.
    for label,start,end,layer,low in [
        ('back',0,math.pi,0,.79),
        ('front underlap',math.pi,1.58*math.pi,.002,.83),
        ('front wrap',1.43*math.pi,2.035*math.pi,.005,.745),
    ]:
        def skirt(u,t,start=start,end=end,layer=layer,low=low):
            a=start+(end-start)*u
            radius=.163+.036*t
            bottom=low+.055*u+.016*math.cos(u*math.pi)
            # Cut corners and hem notches; not regular saw-tooth damage.
            bottom+=.006*math.exp(-((u-.16)/.028)**2)+.004*math.exp(-((u-.74)/.015)**2)
            z=1.015+(bottom-1.015)*t
            f=(fold(u,.20+.07*t,.035,.012)+fold(u,.49-.06*t,.06,.009)
                +fold(u,.78+.04*t,.045,.013))*(.35+.65*t)
            x=(radius+f)*math.cos(a)
            y=(.106+.024*t+f*.7+layer)*math.sin(a)
            return x,y,z
        patch('Cut linen '+label,24,48,skirt,'linen')
        cord('Turned hem '+label,[skirt(u,.98) for u in np.linspace(.01,.99,36)],.0012,'linen')

    for s,label in [(-1,'L'),(1,'R')]:
        def sleeve(u,t,s=s):
            a=u*math.tau
            cx=s*float(np.interp(t,[0,.25,.55,1],[.11,.18,.215,.244]))
            z=float(np.interp(t,[0,.25,.55,1],[1.385,1.34,1.275,1.2]))+.009*math.cos(a+.7)*t
            rx=float(np.interp(t,[0,.25,.55,1],[.030,.060,.064,.064]))
            ry=float(np.interp(t,[0,.25,.55,1],[.040,.067,.067,.069]))
            f=(fold(u,.16+.05*t,.08,.007)+fold(u,.43-.08*t,.045,.009)
                +fold(u,.76+.03*t,.06,.008))*t
            return cx+(rx+f)*math.cos(a),(ry+f)*math.sin(a),z+.011*math.cos(a)*s
        patch('Open short sleeve '+label,20,48,sleeve,'linen')
        def cuff(u,t,sleeve=sleeve):
            x,y,z=sleeve(u,.88+.12*t)
            a=u*math.tau
            return x+.0025*math.cos(a),y+.0025*math.sin(a),z
        patch('Turned open sleeve cuff '+label,4,48,cuff,'linen',.0025)

    # Folded scarf wraps the neck then sags over the chest. Radial pleats and
    # varying drop break the previous rigid bell-shaped collar.
    def scarf(u,t):
        a=u*math.tau;front=max(0,-math.sin(a))
        spread=math.sin(t*math.pi/2)
        fold_depth=.006*math.sin(t*math.pi*5.5+.55*math.cos(a))*(math.sin(math.pi*t)**.6)
        rx=.053+.115*spread+fold_depth
        ry=.046+.079*spread+fold_depth
        drop=.048+.084*front+.018*math.cos(a)
        z=1.438-drop*t+.012*math.sin(a)+.004*math.cos(a*3)*t
        return rx*math.cos(a),ry*math.sin(a),z
    patch('Folded asymmetric neck scarf',36,96,scarf,'olive',.002)
    cord('Soft scarf selvedge',[scarf(u,.985) for u in np.linspace(0,1,96)],.0014,'olive')

    # The mantle is a back/shoulder panel, not a complete poncho over both arms.
    def cape(u,t):
        a=-.13+(math.pi+.26)*u
        topx=.166*math.cos(a);topy=.121*math.sin(a)
        width=.205+.012*math.sin(u*math.pi)
        x=(1-t)*topx+t*width*math.cos(a)
        y=(1-t)*topy+t*(.148*math.sin(a)+.008)
        bottom=1.285-.165*u-.034*math.sin(u*math.pi)
        z=(1-t)*(1.389+.014*math.sin(a)+.008*math.cos(a))+t*bottom
        f=(fold(u,.19+.09*t,.055,.016)+fold(u,.46-.03*t,.075,.017)
            +fold(u,.76-.06*t,.06,.012))*t
        y+=f+.004*t**5*math.sin(u*39)
        z+=.004*t**7*math.sin(u*51)
        return x,y,z
    obj=patch('Separate triangular back mantle',28,64,cape,'olive',.002)
    obj['secondary_motion']='Pending: pin shoulder row; weight cape chains after neutral shape acceptance'
    cord('Mantle sewn lower edge',[cape(u,.984) for u in np.linspace(.005,.995,64)],.0012,'olive')
