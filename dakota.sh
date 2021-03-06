#!/bin/sh
# Description
#   Run the dakota tool and run the process chain
#
# ------------------------------------------------------------------------------


# Dakota change the parameters in this file
# ------------------------------------------------------------------------------
dprepro $1 theta.dakota theta
dprepro $1 vel.dakota vel
   
    # Get angle 
    #---------------------------------------------------------------------------
    theta=`head theta`
    theta=`echo ${theta} | sed -e 's/[eE]+*/\\*10\\^/'`
    theta=`echo "scale=6; $theta/1" | bc`
    
    vel=`head vel`
    vel=`echo ${vel} | sed -e 's/[eE]+*/\\*10\\^/'`
    vel=`echo "scale=6; $vel/1" | bc`


    # Get the loop number
    #---------------------------------------------------------------------------
    loopNumber=`cat .optimizationLoop`
    >&2 echo  "   ++++ Optimisation loop $loopNumber"
    >&2 echo  "   |"
    >&2 echo  "   |--> theta = $theta"
    >&2 echo  "   |--> Velocity = $vel"

    # Make loop folder for log files
    #---------------------------------------------------------------------------
    logFolder_="Log/Optimization"$loopNumber
    mkdir -p $logFolder_


    #Run python script
    #---------------------------------------------------------------------------
    ./NACArun.py


    # Get ratio  (average of inlet / outlet would be better here)
    #---------------------------------------------------------------------------
    >&2 echo "   |--> Ratio calculation"
    ratio=`head ratio`


    # Remove time directorys (reg expression would be nicer)
    #---------------------------------------------------------------------------
    rm -rf 1* 2* 3* 4* 5* 6* 7* 8* 9*


    # We use a gradient scheme, the function has to be maximized
    #---------------------------------------------------------------------------
    funct=`echo "scale=6; $ratio" | bc`



    >&2 echo "   |--> Drag ratio is: $ratio"
    >&2 echo "   |--> Function for dakota is: $ratio"
    >&2 echo "   |"
    echo -e "$dp\t$ratio\t$funct" >> analyseData.dat
    echo $funct > .dakotaInput.dak
    

    # Increase the loop number and store in dummy file
    #--------------------------------------------------------------------------
    echo $((loopNumber+1)) > .optimizationLoop


# Generate ouput file for DAKOTA's algorithm
#------------------------------------------------------------------------------
cp .dakotaInput.dak $2 

sleep 0.1

#------------------------------------------------------------------------------
