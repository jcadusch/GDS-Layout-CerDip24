#!/usr/bin/env python ##for python on Linux/Mac

####-------------------------#####
## Si waveguide array spectrometer v1.0
##
## By Jasper Cadusch August 2017
###-------------------------#####

## dependencies
from IPython import get_ipython
get_ipython().magic('reset -sf') ## when using IDE (eg spyder)
 

import matplotlib.pyplot as plt
import numpy as np
import gdspy
from gdsCAD import *

## Parameters
TopCell=core.Cell('TOP')
L = 300.0 # waveguide length in um
w = 0.1 # waveguide width in um
PadLen = 200.0 # pad size side length in um
shelf = 200.0 # pad shelf size side length in um
MesaLen = 420.0 # mesa size in um
MesaWid = 240.0
MesaOffset = 5.0
period = 0.5 # wg array period in um
nWg = int(shelf/period) # number of waveguides
PadSpace = 750.0 #  pad spacing centre to centre in um
overlap = 0.5 # pad-detector overlap in um
AlignMx = 3000.0 # alignment marker x position
AlignMy = AlignMx # alignment marker y position
AlignMw = 20.0 # alignment marker width
AlignMl = 100.0 # alignment marker length

thin = 0.03 ## minimum waveguide width
thick = 0.145 ## maximum waveguide width
step = 0.005 ## waveguide width increment

tck = np.arange(thin,thick,step) ##---- replace with 23 width values from experiment ----## 

## create 23 photodiode positions
x = PadSpace*np.array([-7/2,-7/2,-5/2,-3/2,-1/2,1/2,3/2,5/2,7/2,7/2,7/2,7/2,7/2,7/2,5/2,3/2,1/2,-1/2,-3/2,-5/2,-7/2,-7/2,-7/2])
y = PadSpace*np.array([-1/2,-3/2,-7/2,-7/2,-7/2,-7/2,-7/2,-7/2,-5/2,-3/2,-1/2,1/2,3/2,5/2,7/2,7/2,7/2,7/2,7/2,7/2,5/2,3/2,1/2])

AngList = np.array([0,0,90,90,90,90,90,90,180,180,180,180,180,180,270,270,270,270,270,270,0,0,0])

#### Create Fins ####

#fin = shapes.Rectangle((-0.5*w,-0.5*L), (0.5*w,0.5*L), layer=2)
#
#wgcell = core.Cell('wg')
#
#wgcell.add(fin)
#
#wgcellarray = core.CellArray(wgcell,nWg,1,(period,1))
#
#FinCell = core.Cell('Fins')
#
#FinCell.add(wgcellarray)



#### Create Mesa ####

for (posx,posy,ang) in zip(x,y,AngList):

        
    mesa1 = shapes.Rectangle((-0.5*MesaLen+PadLen/4,-0.5*MesaWid), (0.5*MesaLen+PadLen/4,0.5*MesaWid), layer=3)

    mesa1.translate((posx,posy))
    
    mesa1.rotate(ang,(posx,posy))
    
    mesa2 = shapes.Rectangle((-L/2-MesaOffset,-0.5*PadLen/np.sqrt(2)-MesaOffset), (L/2+MesaOffset,0.5*PadLen/np.sqrt(2)+MesaOffset), layer=3)

    mesa2.rotate(45)
    
    mesa2.translate((posx+L/np.sqrt(8)+3*PadLen/4,posy+L/np.sqrt(8)+PadLen/4))
    
    mesa2.rotate(ang,(posx,posy))
    
    mesa3 = shapes.Rectangle((-L/2-MesaOffset,-0.5*PadLen/np.sqrt(2)-MesaOffset), (L/2+MesaOffset,0.5*PadLen/np.sqrt(2)+MesaOffset), layer=3)

    mesa3.rotate(-45)
    
    mesa3.translate((posx+L/np.sqrt(8)+3*PadLen/4,posy-L/np.sqrt(8)-PadLen/4))
    
    mesa3.rotate(ang,(posx,posy))
    
    TopCell.add([mesa1,mesa2,mesa3])

#### Create Pads ####




        
    pad = shapes.Rectangle((-0.5*PadLen,-0.5*PadLen), (0.5*PadLen,0.5*PadLen), layer=1)

    pad.translate((posx,posy))
    
    TopCell.add(pad)

    points2=[(0,-PadLen/2), (PadLen/2,0), (0,PadLen/2)]
    
    tri = core.Boundary(points2, layer=1)
        
    tri.translate((posx+PadLen/2,posy))
    
    tri.rotate(ang,(posx,posy))
    
    TopCell.add(tri)
#### Create Markers ####

label = shapes.LineLabel('', 70,(x[0]-2*PadLen,y[0]),layer=2)
label.add_text('Pin 1','romant')
TopCell.add(label)

label2 = shapes.LineLabel('', 70,(x[11]+2*PadLen,y[11]),layer=2)
label2.add_text('Pin 13','romant')
TopCell.add(label2)

label3 = shapes.LineLabel('', 70,(x[4]-0.4*PadLen,y[4]-2*PadLen),layer=2)
label3.add_text('Pin 6','romant')
TopCell.add(label3)

label4 = shapes.LineLabel('', 70,(x[16]-0.4*PadLen,y[16]+2*PadLen),layer=2)
label4.add_text('Pin 18','romant')
TopCell.add(label4)

#### Add cells to layout ####

Wg_layout = core.Layout('WgLib')
Wg_layout.add(TopCell)

### Save GDS ###
Wg_layout.save('../GDSII/wg/wg_chip.gds')
#FN_layout.save('../GDSII/fishnet/fishnet_chip.gds')