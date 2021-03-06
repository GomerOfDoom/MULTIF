import os, sys
import numpy as np

from .. import SU2
from meshgeneration import *
from runSU2 import *
import SU2postprocessing
import AEROSpostprocessing

from .. import nozzle as nozzlemod

try:
    from runAEROS import *
except ImportError as e:
    print 'Error importing all functions from runAEROS in MEDIUMF/run.py.'
    print e
    print
    

def Run( nozzle, **kwargs ):  
    
    output = 'verbose';
    writeToFile=1;
    postpro = 0;
    skipAero = 0;
    skipAeroPostPro = 0;
    
    if 'output' in kwargs:
        output = kwargs['output'];
        
    if 'writeToFile' in kwargs:
        writeToFile = int(kwargs['writeToFile']);
        
    if 'postpro' in kwargs:
        postpro = int(kwargs['postpro']);

    if 'skipAero' in kwargs and kwargs['skipAero'] == 1:
        skipAero = 1;
    
    if 'skipAeroPostPro' in kwargs and kwargs['skipAeroPostPro'] == 1:
        skipAeroPostPro = 1;

    # # Obtain mass and volume
    # if 'MASS' in nozzle.responses or 'VOLUME' in nozzle.responses:
    #     volume, mass = nozzlemod.geometry.calcVolumeAndMass(nozzle)
    #     if 'MASS' in nozzle.responses:
    #         nozzle.responses['MASS'] = np.sum(mass)
    #     if 'VOLUME' in nozzle.responses:
    #         nozzle.responses['VOLUME'] = np.sum(volume)

    # # Calculate mass gradients if necessary
    # if 'MASS' in nozzle.gradients and nozzle.gradients['MASS'] is not None:
    #     if ( nozzle.gradientsMethod == 'ADJOINT' ):
    #         # Convergence study using B-spline coefs show finite difference mass gradients
    #         # converge. Most accurate gradients use absolute step size 1e-8. RWF 5/10/17
    #         nozzle.gradients['MASS'] = nozzlemod.geometry.calcMassGradientsFD(nozzle,1e-8);
    #     elif ( nozzle.gradientsMethod == 'FINITE_DIFF' ):
    #         nozzle.gradients['MASS'] = nozzlemod.geometry.calcMassGradientsFD(\
    #           nozzle,nozzle.fd_step_size);
    #     else:
	# 	    sys.stderr.write('  ## ERROR : Unknown gradients computation '
	# 	      'method.\n');
	# 	    sys.exit(1);
	
    # # Calculate volume gradients if necessary
    # if 'VOLUME' in nozzle.gradients and nozzle.gradients['VOLUME'] is not None:
    #     sys.stderr.write('\n ## ERROR : gradients for VOLUME are not supported\n\n');
    #     sys.exit(1);
        
    # # Obtain mass of wall and gradients only if requested
    # if 'MASS_WALL_ONLY' in nozzle.responses:
    #     volume, mass = nozzlemod.geometry.calcVolumeAndMass(nozzle)
    #     n_layers = len(nozzle.wall.layer);
    #     nozzle.responses['MASS_WALL_ONLY'] = np.sum(mass[:n_layers]);
        
    # if 'MASS_WALL_ONLY' in nozzle.gradients and nozzle.gradients['MASS_WALL_ONLY'] is not None:
    #     if ( nozzle.gradientsMethod == 'ADJOINT' ):
    #         # Convergence study using B-spline coefs show finite difference mass gradients
    #         # converge. Most accurate gradients use absolute step size 1e-8. RWF 5/10/17
    #         nozzle.gradients['MASS_WALL_ONLY'] = nozzlemod.geometry.calcMassGradientsFD(nozzle,1e-8,components='wall-only');
    #     elif ( nozzle.gradientsMethod == 'FINITE_DIFF' ):
    #         nozzle.gradients['MASS_WALL_ONLY'] = nozzlemod.geometry.calcMassGradientsFD(\
    #           nozzle,nozzle.fd_step_size,components='wall-only');
    #     else:
	# 	    sys.stderr.write('  ## ERROR : Unknown gradients computation '
	# 	      'method.\n');
	# 	    sys.exit(1);

    # Run aero-thermal-structural analysis if necessary
    runAeroThermalStructuralProblem = 0;
    for k in nozzle.responses:
        if k not in ['MASS','VOLUME','MASS_WALL_ONLY']:
            runAeroThermalStructuralProblem = 1;    
    
    # Run aero-thermal-structural gradient analysis if necessary
    if nozzle.gradientsFlag == 1:
        runAeroThermalStructuralGradients = 0;        
        for k in nozzle.gradients:
            # if k not in ['MASS','VOLUME','MASS_WALL_ONLY']:
            if nozzle.gradients[k] is not None:
                runAeroThermalStructuralGradients = 1;
    
    if runAeroThermalStructuralProblem:
        
        CheckSU2Version(nozzle);	
        
        if postpro != 1 :
            if nozzle.aeroFlag == 1:
                # Run aero analysis (and thrust adjoint if necessary)  
    	        #CheckOptions (nozzle);
                curDir = os.path.dirname(os.path.realpath(__file__));	
                if nozzle.runDir != '':
    	            os.chdir(nozzle.runDir);
                if skipAero:
                    sys.stdout.write("WARNING: Skipping medium-fidelity aero analysis.\n")
                else:	
                    gradCalc = runSU2 (nozzle);
	        
	        # Run thermal/structural analyses
            if nozzle.thermalFlag == 1 or nozzle.structuralFlag == 1:
                multif.MEDIUMF.runAEROS(nozzle, output);  
        
        # Assign aero QoI if required
        if nozzle.aeroFlag == 1 and skipAeroPostPro != 1:
            SU2postprocessing.PostProcess(nozzle, output);
        
        # Assign thermal/structural QoI if required
        if nozzle.thermalFlag == 1 or nozzle.structuralFlag == 1:
            AEROSpostprocessing.PostProcess(nozzle, output);             
        
        
    # Obtain mass (volume is currently not accepted as a nozzle response)
    if 'MASS' in nozzle.responses or 'MASS_WALL_ONLY' in nozzle.responses:
        total_mass, wall_mass = getMass(nozzle, output)
        if 'MASS' in nozzle.responses:
            nozzle.responses['MASS'] = total_mass;
        if 'MASS_WALL_ONLY' in nozzle.responses:
            nozzle.responses['MASS_WALL_ONLY'] = wall_mass;
       
    # Calculate gradients if necessary
    if nozzle.gradientsFlag == 1 and runAeroThermalStructuralGradients:

        if ( nozzle.gradientsMethod == 'ADJOINT' ):

#                # Convergence study using B-spline coefs show finite difference mass gradients
#                # converge. Most accurate gradients use absolute step size 1e-8. RWF 5/10/17
#                sys.stdout.write("Compute mass gradients.\n");
#                nozzle.mass_grad = nozzlemod.geometry.calcMassGradientsFD(nozzle,1e-8);
#                sys.stdout.write("Done mass gradients.\n");				

            if gradCalc == 0: # i.e. failed adjoint calculation, use finite differences
                # Rerun center point with same number of cores as differences.
                # This is to avoid a bug where SU2 converges differently when
                # run on different number of processors.
                multif.gradients.calcGradientsFD(nozzle,nozzle.fd_step_size,rerun_center=1,output=output);
            else:
                # Check for other required gradients
                otherRequiredGradients = 0;
                for k in nozzle.gradients:
                    #if k not in ['MASS','VOLUME','MASS_WALL_ONLY','THRUST']:
                    if k not in ['THRUST']:
                        otherRequiredGradients = 1;
                        sys.stderr.write(' ## WARNING: QoI gradients desired using ADJOINT '
                            'method which do not have an associated adjoint calculation.\n'
                            ' Namely: %s. The current implementation requires finite '
                            'differencing across the aero analysis, so this method is '
                            'equivalent in computational cost to choosing the FINITE_DIFF'
                            ' method\n' % k);
                # Do finite difference for other QoI if there are any, but use
                # adjoint gradients for thrust
                if otherRequiredGradients:
                    saveThrustGradients = nozzle.gradients['THRUST'];
                    saveThrustResponse = nozzle.responses['THRUST'];
                    nozzle.gradients.pop('THRUST',None);
                    nozzle.responses.pop('THRUST',None); # avoid calculating thrust
                    thrustIndex = nozzle.outputTags.index('THRUST');
                    nozzle.outputTags.remove('THRUST'); # temporarily remove THRUST
                    # Rerun center point with same number of cores as differences.
                    # This is to avoid a bug where SU2 converges differently when
                    # run on different number of processors.
                    multif.gradients.calcGradientsFD(nozzle,nozzle.fd_step_size,rerun_center=1,output=output);
                    nozzle.gradients['THRUST'] = saveThrustGradients;
                    nozzle.responses['THRUST'] = saveThrustResponse;
                    nozzle.outputTags.insert(thrustIndex,'THRUST');
                    
        elif ( nozzle.gradientsMethod == 'FINITE_DIFF' ):
            # Rerun center point with same number of cores as differences.
            # This is to avoid a bug where SU2 converges differently when
            # run on different number of processors.            
            multif.gradients.calcGradientsFD(nozzle,nozzle.fd_step_size,rerun_center=1,output=output);  
                        
        else:
            sys.stderr.write('  ## ERROR : Unknown gradients computation '
                'method.\n');
            sys.exit(1);
            
        # Write separate gradients file
        # gradFile = open(nozzle.gradientsFile,'w');
        # for k in nozzle.outputTags:
        #     np.savetxt(gradFile,nozzle.gradients[k]);
        # gradFile.close();

    # Write data
    if writeToFile:
        
        #tag_out, val_out, gra_out, gratag_out = nozzle.GetOutputFunctions();
                
        if nozzle.outputFormat == 'PLAIN':
            nozzle.WriteOutputFunctions_Plain();
        else:
            nozzle.WriteOutputFunctions_Dakota();
        
    return 0;
