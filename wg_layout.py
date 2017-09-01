#!/usr/bin/env python ##for python on Linux/Mac

####-------------------------#####
## Si waveguide array spectrometer v1.0
##
## By Jasper Cadusch August 2017
###-------------------------#####

## dependencies

#from IPython import get_ipython
#get_ipython().magic('reset -sf') ## when using IDE (eg spyder)
import numpy as np
from gdsCAD import *

##-- Parameters --##
    
    ### Waveguide Parameters 
L = 300.0 # waveguide length in um
thin = 0.03 ## minimum waveguide width
thick = 0.145 ## maximum waveguide width
step = 0.005 ## waveguide width increment
tck = np.arange(thin,thick,step) ##---- waveguide widths [replace with 23 width values from experiment] ----## 
period = 0.5 # wg array period in um

    ### Pad Parameters
PadLen = 200.0 # pad size side length in um
PadSpace = 750.0 #  pad spacing centre to centre in um
overlap = 0.5 # pad-detector overlap in um
nWg = int(PadLen/(period*np.sqrt(2))) # number of waveguides


    ### Mesa Parameters
MesaLen = 420.0 # mesa size in um
MesaWid = 240.0 # mesa width for pad region
MesaOffset = 5.0 # mesa overhang for waveguide region

    ### Alignment Markers Parameters
AlignMx = 3000.0 # alignment marker x position
AlignMy = AlignMx # alignment marker y position
AlignMw = 20.0 # alignment marker width
AlignMl = 100.0 # alignment marker length

##-- End Parameters --##


## create 23 photodiode positions for 24 pin chip carrier (pin 3 used for back contact)
x = PadSpace*np.array([-7/2,-7/2,-5/2,-3/2,-1/2,1/2,3/2,5/2,7/2,7/2,7/2,7/2,7/2,7/2,5/2,3/2,1/2,-1/2,-3/2,-5/2,-7/2,-7/2,-7/2])
y = PadSpace*np.array([-1/2,-3/2,-7/2,-7/2,-7/2,-7/2,-7/2,-7/2,-5/2,-3/2,-1/2,1/2,3/2,5/2,7/2,7/2,7/2,7/2,7/2,7/2,5/2,3/2,1/2])
AngList = np.array([0.,0.,90.,90.,90.,90.,90.,90.,180.,180.,180.,180.,180.,180.,270.,270.,270.,270.,270.,270.,0.,0.,0.])  ## pad direction list

pin = 1 ## a counter

TopCell=core.Cell('TOP') ## create the main cell

for (posx,posy,ang,w) in zip(x,y,AngList,tck):
    wgcell = core.Cell('wg'+repr(pin))
    
    wgcell2 = core.Cell('wg_2_'+repr(pin))
    
    #### Create Fins for Detector 1 ####

    fin = shapes.Rectangle((-0.5*L,-0.5*w), (0.5*L,0.5*w), layer=4)
              
    fin.rotate(-45)
        
    fin.translate((posx+PadLen/2+(L+w)/np.sqrt(8)-overlap/np.sqrt(2),posy-(L-w)/np.sqrt(8)-PadLen/2+overlap/np.sqrt(2)))
    
    fin.rotate(ang,(posx,posy))
    
    wgcell.add(fin)
    
    wgcellarray = core.CellArray(wgcell,nWg,1,((period*np.cos(np.deg2rad(ang+45)), period*np.sin(np.deg2rad(ang+45))),(0,0)))
    
    TopCell.add(wgcellarray)
            
    del wgcell
    
    ### Fins for Detector 2 ####
    
    fin2 = shapes.Rectangle((-0.5*L,-0.5*w), (0.5*L,0.5*w), layer=4)
              
    fin2.rotate(45)
        
    fin2.translate((posx+PadLen/2+(L+w)/np.sqrt(8)-overlap/np.sqrt(2),posy+(L-w)/np.sqrt(8)+PadLen/2-overlap/np.sqrt(2)))
    
    fin2.rotate(ang,(posx,posy))
    
    wgcell2.add(fin2)
    
    wgcellarray2 = core.CellArray(wgcell2,nWg,1,((period*np.cos(np.deg2rad(ang-45)), period*np.sin(np.deg2rad(ang-45))),(0,0)))
    
    TopCell.add(wgcellarray2)
    
    del wgcell2
    
    pin += 1


    #### Create Mesa ####

        
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

mkr1 = shapes.Rectangle((-AlignMw/2,-AlignML/2),(-AlignMw/2,-AlignML/2),layer=1)

#### Add cells to layout ####
Wg_layout = core.Layout('WgLib')
Wg_layout.add(TopCell)

### Save GDS layout ###
Wg_layout.save('./WG_v02/wg_chip.gds') ### set your own path/filename here
