# by Mateusz Maciejewski (matt@mattmaciejewski.com), August 2010
# This script will draw the eigenvectors of the inertia tensor of selection.
# It should be placed in the same folder as the pdb for which the analysis
# is carried out. In PyMOL the script can be loaded by issuing 
# "run inertiaTensor.py". Then it can be used within PyMOL via the tensor
# command, e.g.:
# tensor molecule_object, name="tensor", resids=24-65+78-122, atoms="n+ca+c"
# requires: PyMOL, numpy.

from pymol.cgo import *
from pymol import cmd
import sys
import re
import math
import numpy


def tensor(molecule, name="tensor", resids="*", atoms="*", state=1):


    def draw_axes(start,ends,radius=.2,name_obj="tensor"):
        radius = float(radius)
        size = radius*15.
        origin_offset = radius * -25.
        obj = [
            CYLINDER, start[0],start[1],start[2],ends[0][0]+start[0],ends[0][1]+start[1],ends[0][2]+start[2], radius, 1.0, 1.0, 1.0, 1.0, 0.0, 0.,  # red Ixx
            CYLINDER, start[0],start[1],start[2],(-1)*ends[0][0]+start[0],(-1)*ends[0][1]+start[1],(-1)*ends[0][2]+start[2], radius, 1.0, 1.0, 1.0, 1.0, 0.0, 0.,
            CYLINDER, start[0],start[1],start[2],ends[1][0]+start[0],ends[1][1]+start[1],ends[1][2]+start[2], radius, 1.0, 1.0, 1.0, 0., 1.0, 0.,   # green Iyy
            CYLINDER, start[0],start[1],start[2],(-1)*ends[1][0]+start[0],(-1)*ends[1][1]+start[1],(-1)*ends[1][2]+start[2], radius, 1.0, 1.0, 1.0, 0., 1.0, 0.,
            CYLINDER, start[0],start[1],start[2],ends[2][0]+start[0],ends[2][1]+start[1],ends[2][2]+start[2], radius, 1.0, 1.0, 1.0, 0., 0.0, 1.0,  # blue Izz
            CYLINDER, start[0],start[1],start[2],(-1)*ends[2][0]+start[0],(-1)*ends[2][1]+start[1],(-1)*ends[2][2]+start[2], radius, 1.0, 1.0, 1.0, 0., 0.0, 1.0,

            ]

        cmd.load_cgo(obj,name_obj)



    residues = []

    if resids != "*":
        if resids.find("+") != -1:
            resids = resids.split("+")

            for res in resids:
                if res.find("-") != -1:
                    residues += range(int(res.split("-")[0]),int(res.split("-")[1])+1)
                else:
                    residues += [int(res)]
        else:
            if resids.find("-") != -1:
                residues += range(int(resids.split("-")[0]),int(resids.split("-")[1])+1)
            else:
                residues += [int(resids)]

    print residues

    if atoms != "*":
        atoms = atoms.split("+")

    totmass=0.0
    x_com,y_com,z_com=0,0,0
    I11,I12,I13,I21,I22,I23,I31,I32,I33=0,0,0,0,0,0,0,0,0
    model=cmd.get_model(molecule,state)

    for a in model.atom:
        if (a.resi_number in residues or resids == "*") and \
           (a.name.lower() in atoms or atoms == "*") and \
           (a.resn != "ANI"):

            #print a.name
            x_com+= a.coord[0]*a.get_mass()
            y_com+= a.coord[1]*a.get_mass()
            z_com+= a.coord[2]*a.get_mass()
            totmass+=a.get_mass()

    x_com /= totmass; y_com /= totmass; z_com /= totmass

    print x_com, y_com, z_com

    I=[]

    for index in range(9):
        I.append(0)

    for a in model.atom:
        if (a.resi_number in residues or resids == "*") and \
           (a.name.lower() in atoms or atoms == "*") and \
           (a.resn != "ANI"):


            temp_x,temp_y,temp_z=a.coord[0],a.coord[1],a.coord[2]
            temp_x-=x_com; temp_y-=y_com; temp_z-=z_com

            I[0]+=a.get_mass()*(temp_y**2+temp_z**2)
            I[4]+=a.get_mass()*(temp_x**2+temp_z**2)
            I[8]+=a.get_mass()*(temp_x**2+temp_y**2)
            I[1]-=a.get_mass()*temp_x*temp_y
            I[3]-=a.get_mass()*temp_x*temp_y
            I[2]-=a.get_mass()*temp_x*temp_z
            I[6]-=a.get_mass()*temp_x*temp_z
            I[5]-=a.get_mass()*temp_y*temp_z
            I[7]-=a.get_mass()*temp_y*temp_z
   
    print I[0:3]
    print I[3:6]
    print I[6:9]

    tensor = numpy.array([(I[0:3]),(I[3:6]),(I[6:9])])
    print tensor
    eigens = numpy.linalg.eig(tensor)
    vals,vects = numpy.linalg.eig(tensor) # they come out unsorted, so the below is needed

    eig_ord = numpy.argsort(vals) # a thing to note is that here COLUMN i corrensponds to eigenvalue i.
    print eig_ord
    print vals[eig_ord]
    print vects[:,eig_ord]

    ord_vals = vals[eig_ord]
    ord_vects = vects[:,eig_ord].T

    print ord_vals
    print ord_vals[0], ord_vals[1], ord_vals[2]
    print ord_vects
    print ord_vects[1][2]


    start=[x_com,y_com,z_com]
    ends=[[10*ord_vects[0][0],10*ord_vects[0][1],10*ord_vects[0][2]],
          [10*ord_vects[1][0],10*ord_vects[1][1],10*ord_vects[1][2]],
          [10*ord_vects[2][0],10*ord_vects[2][1],10*ord_vects[2][2]]]

    draw_axes(start,ends,name_obj=molecule+name)


cmd.extend("tensor", tensor)
