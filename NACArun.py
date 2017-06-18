#!/usr/bin/python

import os
import numpy as np
import subprocess as s
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Execution.BasicRunner import BasicRunner
from PyFoam.Basics.DataStructures import DictProxy

#vel = ParsedParameterFile("0/U")
pproc = "postProcessing/forceCoeffs/0/forceCoeffs_1.dat"
'''
#Obtain Value of Velocity from dummy vel file
U = 0
with open("vel", "r") as f:
	for line in f:
		U = float(line.split("e")[0])*10**(float(line.split("e")[1]))
theta_max = 0
pi = 3.1415926
ratio_max = 0
theta = 0
#Obtain Value of Theta from dummy theta file
with open("theta", "r") as f:
	for line in f:
		theta =float(line.split("e")[0])*10**(float(line.split("e")[1]))
#Calculate new velocity
Ux = U*np.cos(theta*pi/180.)
Uy = U*np.sin(theta*pi/180.)
#Replace the existing U boundary conditions
new_vel = "uniform ("+ str(Ux) + " " + str(Uy) + " 0)"
vel["internalField"] = new_vel
vel.writeFile()
'''
#Run the solver
BasicRunner(argv=["simpleFoam","-case","."]).start()
#Store the Cl/Cd ratio in a dummy file
cl = 0
cd = 0
count = 0
with open(pproc, "r") as p:
	for i,line in enumerate(p):
		if i > 9:
			cl_i = abs(float(line.split()[3]))
			cd_i = abs(float(line.split()[2]))
			cl = cl_i
			cd = cd_i
			#count = count + 1
cl = float(cl)
cd = float(cd)
ratio = cl/cd
with open("ratio", "w") as f:
	f.write(str(ratio))
