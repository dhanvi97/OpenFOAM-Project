import numpy as np

M = 2	#Camber indicator
P = 4	#Position of maximum camber
T = 12	#Thickness
pi = 3.141592
#Taking chord thickness as 1, for simplicity in calculations

with open("points", "w") as f:
	m = M/100.
	p = P/10.
	t = T/100.
	for beta in np.arange(0, 360, 360/80.):
		x = 1 - (1-np.cos(beta*pi/180.))/2.
		if x < p :
			yc = m*(2*p*x - x**2)/p**2
			grad_yc = 2.*m*(p - x)/p**2
		else :
			yc = m*(1 - 2*p + 2*p*x -x**2)/(1 - p)**2
			grad_yc = 2.*m*(p - x)/(1 - p)**2
		yt = 5*t*(0.2969*x**0.5 - 0.126*x - 0.3516*x**2 + 0.2843*x**3 - 0.1036*x**4)
		theta = np.arctan(grad_yc)
		if beta <= 180 :
			xs = x - yt*np.sin(theta)
			ys = yc + yt*np.cos(theta)
		else :
			xs = x + yt*np.sin(theta)
			ys = yc - yt*np.cos(theta)
		if xs < 0.00001:
			xs = 0.0
		if abs(ys) < 0.00001:
			ys = 0.0
		f.write(str(xs) + " " + str(ys) + "\n")
		
with open("points", "rw") as input_file, open('new_file' , 'w') as f:
	#-----------------------------------------------------------------------------
	# Module for generating points from dat file								 |
	#-----------------------------------------------------------------------------
	f.write("//---------- Airfoil Points ----------\n")
	f.write("\n")
	num_of_points = 0
	for i, line in enumerate(input_file):
		x = line.strip().split()[0]
		y = line.strip().split()[1]
		new_line = "Point(" + str(i+1) + ") =  {" + x + ", " + y + ", 0, 0.004};\n"
		f.write(new_line)
		num_of_points = i + 1
	f.write("\n");
	#------------------------------------------------------------------------------
	# Module for adding bounding box points										  |
	#------------------------------------------------------------------------------
	f.write("//---------- Bounding Box Points ---------\n")
	f.write("\n")
	f.write("Point(" + str(num_of_points + 1) + ") = {5, 4, 0, 1e+22};\n")
	f.write("Point(" + str(num_of_points + 2) + ") = {-4, 4, 0, 1e+22};\n")
	f.write("Point(" + str(num_of_points + 3) + ") = {-4, -4, 0, 1e+22};\n")
	f.write("Point(" + str(num_of_points + 4) + ") = {5, -4, 0, 1e+22};\n")
	f.write("\n")
	#------------------------------------------------------------------------------
	# Module for connecting Airfoil boundary (spline)							  |
	#------------------------------------------------------------------------------
	f.write("//--------- Airfoil Boundary ----------\n")
	f.write("\n")
	l = ""
	for i in xrange(0, num_of_points/2, 1):
		l = l + str(i+1) + ", "
	f.write("Spline (1) = {" + l[:-2] + "};\n")
	l = ""
	for i in xrange(num_of_points/2 - 1, num_of_points + 1, 1):
		l = l + str(1 + i%num_of_points) + ", "
	f.write("Spline (2) = {"  + l[:-2] + "};\n")
	f.write("\n")
	#------------------------------------------------------------------------------
	# Module for connecting the Boundary Box							  		  |
	#------------------------------------------------------------------------------
	f.write("//----------- Bounding Box Boundary -----------\n")
	f.write("\n")
	for i in xrange(0, 4, 1):
		line = "Line (" + str(3+i) + ") = {" + str(num_of_points + i + 1) + ", " + str(num_of_points + 1 + (i+1)%4) + "};\n"
		f.write(line)
	f.write("\n")
	#------------------------------------------------------------------------------
	# Module for defining the surface							  		          |
	#------------------------------------------------------------------------------
	f.write("//------------ Surface Definition --------------\n")
	f.write("\n")
	f.write("Line Loop (1) = {3, 4, 5, 6};\n")
	f.write("Line Loop (2) = {1, 2};\n")
	f.write("Plane Surface (1) = {1, 2};\n")
	f.write("\n")
	#------------------------------------------------------------------------------
	# Module for extruding the surface							  		          |
	#------------------------------------------------------------------------------
	f.write("//------------- Surface Extrusion ---------------\n")
	f.write("\n")
	f.write("out[] = Extrude {0, 0, -1} {\n")
	f.write("Surface {1}; Layers{1}; Recombine; \n")
	f.write("};\n")
	f.write("\n")
	#------------------------------------------------------------------------------
	# Module for Physical Group Definition							  		      |
	#------------------------------------------------------------------------------
	f.write("//---------- Physical Group Definitions ---------\n")
	f.write("\n")
	f.write("Physical Surface (\"inlet\") = {out[3]};\n")
	f.write("Physical Surface (\"outlet\") = {out[5]};\n")
	f.write("Physical Surface (\"frontAndBack\") = {out[0], out[1]};\n")
	f.write("Physical Surface (\"topAndBottom\") = {out[2], out[4]};\n")
	f.write("Physical Surface (\"walls\") = {out[7], out[6]};\n")
	f.write("Physical Volume (\"internal\") = {1};\n")
	f.write("\n")

	
