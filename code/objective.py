import subprocess
import os
import sys
import ROOT
import getopt
import numpy as np
import json
from daniel import dmetric

def objective(StrawPitch = 1.7, OffsetLayer12 = 1.76/2, OffsetPlane12 = 1.76/4, DeltazLayer = 1.1,\
              DeltazPlane = 2.6, DeltazView = 10., ViewAngle = 5, nEvents=500):

    ViewAngle = int(ViewAngle)
    
    FairShip = str(os.getenv('FAIRSHIP'))
    with open(FairShip+'/geometry/geometry_config_original.py', 'r') as input_file,\
         open(FairShip+'/geometry/geometry_config.py', 'w') as output_file:

        for i, line in enumerate(input_file):
            if i == 129:
                output_file.write('    c.strawtubes.StrawPitch         = '+str(StrawPitch)+'*u.cm\n')
            elif i == 130:
                output_file.write('    c.strawtubes.OffsetLayer12      = '+str(OffsetLayer12)+'*u.cm\n')
            elif i == 131:
                output_file.write('    c.strawtubes.OffsetPlane12      = '+str(OffsetPlane12)+'*u.cm\n')
            elif i == 132:
                output_file.write('    c.strawtubes.DeltazLayer        = '+str(DeltazLayer)+'*u.cm\n')
            elif i == 133:
                output_file.write('    c.strawtubes.DeltazPlane        = '+str(DeltazPlane)+'*u.cm\n')
            elif i == 136:
                output_file.write('    c.strawtubes.ViewAngle          = '+str(ViewAngle)+'\n')
            elif i == 138:
                output_file.write('    c.strawtubes.DeltazView         = '+str(DeltazView)+'*u.cm\n')
            else:
                output_file.write(line)

    #Run simulation
    ShipOpt = str(os.getenv('SHIPOPT'))
    os.chdir(ShipOpt+'/temp/')
    os.system('source $SHIPSOFT/FairShipRun/config.sh')
    os.system('python $FAIRSHIP/macro/run_simScript.py -f $FAIRSHIP/files/Cascade-parp16-MSTP82-1-MSEL4-76Mpot_1_5000.root --nEvents '+str(nEvents))

    #Metric calculation
    input_file = ShipOpt+'/temp/ship.conical.Pythia8-TGeant4.root'
    geo_file = ShipOpt+'/temp/geofile_full.conical.Pythia8-TGeant4.root'
    dy = None
    reconstructiblerequired = 2
    threeprong = 0

    return dmetric(input_file, geo_file, dy, reconstructiblerequired, threeprong)


if __name__=='__main__':
    
    argv = sys.argv[1:]
    
    #default values for parameters
    StrawPitch = 1.7
    OffsetLayer12 = 1.76/2
    OffsetPlane12 = 1.76/4
    DeltazLayer = 1.1
    DeltazPlane = 2.6
    DeltazView = 10.
    ViewAngle = 5
    nEvents = 500
    output_file = "/output/output.txt"
    
    try:
        opts, args = getopt.getopt(argv, "", ["pitch=", "yoffset_layer=", "yoffset_plane=", "zshift_layer=", "zshift_plane=", "zshift_view=", "alpha=", "output=", "nEvents="])
    except getopt.GetoptError:
        print "Wrong parameters. Available params: pitch, yoffset_layer, yoffset_plane, zshift_layer, zshift_plane, zshift_view, alpha, output, nEvents.\n"
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == "--pitch":
            StrawPitch = arg
        elif opt == "--yoffset_layer":
            OffsetLayer12 = arg
        elif opt == "--yoffset_plane":
            OffsetPlane12 = arg
        elif opt == "--zshift_layer":
            DeltazLayer = arg
        elif opt == "--zshift_plane":
            DeltazPlane = arg
        elif opt == "--zshift_view":
            DeltazView = arg
        elif opt == "--alpha":
            ViewAngle = arg
        elif opt == "--output":
            output_file = arg
        elif opt == "--nEvents":
            nEvents = arg
    
    with open(output_file, 'w') as tf:
	tf.write(str(objective(StrawPitch, OffsetLayer12, OffsetPlane12, DeltazLayer, DeltazPlane, DeltazView, ViewAngle, nEvents)))
