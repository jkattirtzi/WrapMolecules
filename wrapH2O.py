import numpy

class Atom(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

def get_pbcs():
    px=14.76
    py=12.78
    pz=28.0
    return px,py,pz

def get_dist(A1,A2):
    px,py,pz=get_pbcs()
    dmin=px+1.0
    ilist=[-1.0, 0.0, 1.0]
    A1x=A1.x
    A1y=A1.y
    A1z=A1.z
    A2x0=A2.x
    A2y0=A2.y
    A2z0=A2.z
    for x in ilist:
        A2x=A2x0 +x*px
        for y in ilist:
            A2y=A2y0 + y*py
            for z in ilist:
                A2z=A2z0+z*pz
                d=((A1x-A2x)**2+(A1y-A2y)**2+(A1z-A2z)**2)**0.5
                if d < dmin:
                    dmin=d
    return d

def wrapA(O):
    px,py,pz=get_pbcs()
    if O.x > px:
        while O.x > px:
            O.x-=px 
    elif O.x < 0.0:
        while O.x < 0.0:
            O.x+=px 
    if O.y > py:
        while O.y > py:
            O.y-=py 
    elif O.y < 0.0:
        while O.y < 0.0:
            O.y+=py 
    if O.z > pz:
        while O.z > pz:
            O.z-=pz 
    elif O.z < 0.0:
        while O.z < 0.0:
            O.z+=pz 
    return O




def wrapH2O(O,H1,H2):
    px,py,pz=get_pbcs()
    if O.x > px:
        while O.x > px:
            O.x-=px 
            H1.x-=px
            H2.x-=px
    elif O.x < 0.0:
        while O.x < 0.0:
            O.x+=px 
            H1.x+=px
            H2.x+=px
    if O.y > py:
        while O.y > py:
            O.y-=py 
            H1.y-=py 
            H2.y-=py 
    elif O.y < 0.0:
        while O.y < 0.0:
            O.y+=py 
            H1.y+=py 
            H2.y+=py 
    if O.z > pz:
        while O.z > pz:
            O.z-=pz 
            H1.z-=pz 
            H2.z-=pz 
    elif O.z < 0.0:
        while O.z < 0.0:
            O.z+=pz 
            H1.z+=pz 
            H2.z+=pz 
    return O,H1,H2

def read_file():
    Ifile=open("H2O.xyz",'r')
    Ofile=open("H2O_wrapped.xyz",'w')
    j=0
    for line in Ifile:
        l=line.split()
        if len(l)==4:
            name=l[0]
            x=float(l[1])
            y=float(l[2])
            z=float(l[3])
            if name =="C":
                line2=line.strip()
                line2+="    Sur    \n"
                Ofile.write(line2)
            elif name=="Na":
                Na=Atom(x,y,z)
                Na=wrapA(Na)
                Ofile.write("%s %.10f  %.10f  %.10f Ion \n "%(name,Na.x,Na.y, Na.z)) 
            elif name=="Cl":
                Cl=Atom(x,y,z)
                Cl=wrapA(Cl)
                Ofile.write("%s %.10f  %.10f  %.10f Ion \n "%(name,Cl.x,Cl.y, Cl.z)) 
            else:
                j+=1
                if j==1:
                    if name !="O":
                        print "error not O", name
                        print line
                        exit()
                    O=Atom(x,y,z)
                elif j==2:
                    H1=Atom(x,y,z)
                elif j==3:
                    H2=Atom(x,y,z)
                    O,H1,H2=wrapH2O(O,H1,H2)
                    j=0
                    Ofile.write("%s %.10f  %.10f  %.10f H2O \n "%("O",O.x,O.y, O.z)) 
                    Ofile.write("%s %.10f  %.10f  %.10f H2O \n "%("H",H1.x,H1.y, H1.z)) 
                    Ofile.write("%s %.10f  %.10f  %.10f H2O \n "%("H",H2.x,H2.y, H2.z)) 
        else:
            Ofile.write(line)
    Ifile.close()
    Ofile.close()
    return

read_file()

