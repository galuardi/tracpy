import numpy as np
import sys
import os
import op
import netCDF4 as netCDF
from mpl_toolkits.basemap import Basemap
import pdb
from matplotlib import delaunay
from matplotlib.pyplot import *
import glob
from datetime import datetime, timedelta
import time
from matplotlib.mlab import *
import inout
#import init
import plotting
import tools
from scipy import ndimage

def run(tp, date, lon0, lat0, T0=None, U=None, V=None):
# def run(loc, nsteps, ndays, ff, date, tseas, ah, av, lon0, lat0, z0, 
#         zpar, do3d, doturb, name, grid=None, dostream=0, N=1, 
#         T0=None, U=None, V=None, zparuv=None, tseas_use=None):
    '''
    FIX THIS FOR USING TRACPY CLASS
    To re-compile tracmass fortran code, type "make clean" and "make f2py", which will give 
    a file tracmass.so, which is the module we import above. Then in ipython, "run run.py"
    xend,yend,zend are particle locations at next step
    some variables are not specifically because f2py is hiding them from me:
     imt, jmt, km, ntractot
    Look at tracmass.step to see what it is doing and making optional at the end.
    Do this by importing tracmass and then tracmass.step?

    I am assuming here that the velocity field at two times are being input into tracmass
    such that the output is the position for the drifters at the time corresponding to the
    second velocity time. Each drifter may take some number of steps in between, but those
    are not saved.

    tp          TracPy object, from the Tracpy class.

    loc         Path to directory of grid and output files
    nsteps      Number of steps to do between model outputs (iter in tracmass) - sets the max 
                time step between drifter steps. Does not control the output sampling anymore.
    ndays       number of days to track the particles from start date
    ff          ff=1 to go forward in time and ff=-1 for backward in time
    date        Start date in datetime object
    tseas       Time between outputs in seconds
    ah          Horizontal diffusion in m^2/s. 
                See project values of 350, 100, 0, 2000. For -turb,-diffusion
    av          Vertical diffusion in m^2/s.
    do3d        for 3d flag, do3d=0 makes the run 2d and do3d=1 makes the run 3d
    doturb      turbulence/diffusion flag. 
                doturb=0 means no turb/diffusion,
                doturb=1 means adding parameterized turbulence
                doturb=2 means adding diffusion on a circle
                doturb=3 means adding diffusion on an ellipse (anisodiffusion)
    lon0        Drifter starting locations in x/zonal direction.
    lat0        Drifter starting locations in y/meridional direction.
    z0/zpar     For 3D drifter movement, turn off twodim flag in makefile.
                Then z0 should be an array of initial drifter depths. 
                The array should be the same size as lon0 and be negative
                for under water. Currently drifter depths need to be above 
                the seabed for every x,y particle location for the script to run.
                To do 3D but start at surface, use z0=zeros(ia.shape) and have
                 either zpar='fromMSL'
                choose fromMSL to have z0 starting depths be for that depth below the base 
                time-independent sea level (or mean sea level).
                choose 'fromZeta' to have z0 starting depths be for that depth below the
                time-dependent sea surface. Haven't quite finished the 'fromZeta' case.
                For 2D drifter movement, turn on twodim flag in makefile.
                Then: 
                set z0 to 's' for 2D along a terrain-following slice
                 and zpar to be the index of s level you want to use (0 to km-1)
                set z0 to 'rho' for 2D along a density surface
                 and zpar to be the density value you want to use
                 Can do the same thing with salinity ('salt') or temperature ('temp')
                 The model output doesn't currently have density though.
                set z0 to 'z' for 2D along a depth slice
                 and zpar to be the constant (negative) depth value you want to use
                To simulate drifters at the surface, set z0 to 's' 
                 and zpar = grid['km']-1 to put them in the upper s level
                 z0='s' is currently not working correctly!!!
                 In the meantime, do surface using the 3d set up option but with 2d flag set
    zparuv      (optional) Use this if the k index for the model output fields (e.g, u, v) is different
                 from the k index in the grid. This might happen if, for example, only the surface current
                 were saved, but the model run originally did have many layers. This parameter
                 represents the k index for the u and v output, not for the grid.
    tseas_use   (optional) Desired time between outputs in seconds, as opposed to the actual time between outputs
                 (tseas). Should be >= tseas since this is just an ability to use model output at less 
                 frequency than is available, probably just for testing purposes or matching other models.
                 Should to be a multiple of tseas (or will be rounded later).
    xp          x-locations in x,y coordinates for drifters
    yp          y-locations in x,y coordinates for drifters
    zp          z-locations (depths from mean sea level) for drifters
    t           time for drifter tracks
    name        Name of simulation to be used for netcdf file containing final tracks
    grid        (optional) Grid information, as read in by tracpy.inout.readgrid().
    N           Controls the output sampling. The length of time between model outputs is divided by N.
                Default is 1.

    The following inputs are for calculating Lagrangian stream functions
    dostream    Calculate streamfunctions (1) or not (0). Default is 0.
    U0, V0      (optional) Initial volume transports of drifters (m^3/s)
    U, V  (optional) Array aggregating volume transports as drifters move [imt-1,jmt], [imt,jmt-1]
    '''

    tic_start = time.time()
    tic_initial = time.time()

    # Initialize everything for a simulation
    tinds, nc, t0save, ufnew,vfnew,dztnew,zrtnew,zwtnew, \
     xend, yend, zend, zp, ttend, t, flag = tp.prepareForSimulation(date, lon0, lat0)

    # loop, call tp.step()

    # finish, call tp.finish()


    # # Calculate subloop steps using input parameter dtFromTracmass. 
    # subloopsteps = 

    # Loop through model outputs. tinds is in proper order for moving forward
    # or backward in time, I think.
    for j,tind in enumerate(tinds[:-1]):

        print j


        # # Replace the time stepping loop
        # tp.compute_time_step()

        # dtstep = 0.
        # while dtstep <= dtFromTracmass:

            # # interpolation constant. =1 if dtFromTracmass==tseas
            # r = dtFromTracmass/tseas

        #     ind = (flag[:] == 0) # indices where the drifters are still inside the domain
        #     xstart = xend[:,j*tp.N+i]
        #     ystart = yend[:,j*tp.N+i]
        #     zstart = zend[:,j*tp.N+i]



        #     dtstep = dtstep + dtFromTracmass



        # # # Loop over substeps between model outputs. This is for use with GNOME. Substeps will not necessarily divide
        # # # evenly into model output time, so there is a special statement for that. Also, if one doesn't need to 
        # # # access steps individually, such as in regular TracPy use, then this loop should collapse.
        # # for i in loopsteps:

        # # tic_read[j] = time.time()

        #     # mask out drifters that have exited the domain
        #     xstart = np.ma.masked_where(flag[:]==1,xstart)
        #     ystart = np.ma.masked_where(flag[:]==1,ystart)
        #     zstart = np.ma.masked_where(flag[:]==1,zstart)

        #     if not np.ma.compressed(xstart).any(): # exit if all of the drifters have exited the domain
        #         break

        #     # Do stepping in Tracpy class
        #     if tp.dostream:
        #         ufnew, vfnew, dztnew, zrtnew, zwtnew, xend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
        #             yend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
        #             zend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
        #             zp[ind,j*tp.N+1:j*tp.N+tp.N+1],\
        #             flag[ind],\
        #             ttend[ind,j*tp.N+1:j*tp.N+tp.N+1], U, V = tp.step(tinds[j+1], nc, j, ttend[ind,j*tp.N], ufnew, vfnew, dztnew, zrtnew, zwtnew, 
        #                 xstart, ystart, zstart, T0[ind], U, V)
        #     else:
        #         ufnew, vfnew, dztnew, zrtnew, zwtnew, xend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
        #             yend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
        #             zend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
        #             zp[ind,j*tp.N+1:j*tp.N+tp.N+1],\
        #             flag[ind],\
        #             ttend[ind,j*tp.N+1:j*tp.N+tp.N+1], U, V = tp.step(tinds[j+1], nc, j, ttend[ind,j*tp.N], ufnew, vfnew, dztnew, zrtnew, zwtnew, 
        #                 xstart, ystart, zstart)

        ind = (flag[:] == 0) # indices where the drifters are still inside the domain
        xstart = xend[:,j*tp.N]
        ystart = yend[:,j*tp.N]
        zstart = zend[:,j*tp.N]

        # mask out drifters that have exited the domain
        xstart = np.ma.masked_where(flag[:]==1,xstart)
        ystart = np.ma.masked_where(flag[:]==1,ystart)
        zstart = np.ma.masked_where(flag[:]==1,zstart)

        if not np.ma.compressed(xstart).any(): # exit if all of the drifters have exited the domain
            break

        # Do stepping in Tracpy class
        if tp.dostream:
            ufnew, vfnew, dztnew, zrtnew, zwtnew, xend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
                yend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
                zend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
                zp[ind,j*tp.N+1:j*tp.N+tp.N+1],\
                flag[ind],\
                ttend[ind,j*tp.N+1:j*tp.N+tp.N+1], U, V = tp.step(tinds[j+1], nc, j, ttend[ind,j*tp.N], ufnew, vfnew, dztnew, zrtnew, zwtnew, 
                    xstart, ystart, zstart, T0[ind], U, V)
        else:
            ufnew, vfnew, dztnew, zrtnew, zwtnew, xend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
                yend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
                zend[ind,j*tp.N+1:j*tp.N+tp.N+1],\
                zp[ind,j*tp.N+1:j*tp.N+tp.N+1],\
                flag[ind],\
                ttend[ind,j*tp.N+1:j*tp.N+tp.N+1], U, V = tp.step(tinds[j+1], nc, j, ttend[ind,j*tp.N], ufnew, vfnew, dztnew, zrtnew, zwtnew, 
                    xstart, ystart, zstart)

    nc.close()
    # pdb.set_trace()
    ttend = ttend + t0save # add back in base time in seconds

    ## map coordinates interpolation
    # xp2, yp2, dt = tools.interpolate(xg,yg,grid,'m_ij2xy')
    # tic = time.time()
    lonp, latp, dt = tools.interpolate2d(xend,yend,tp.grid,'m_ij2ll',mode='constant',cval=np.nan)
    # print '2d interp time=', time.time()-tic

    # pdb.set_trace()

    runtime = time.time()-tic_start


    print "============================================="
    print ""
    print "Simulation name: ", tp.name
    print ""
    print "============================================="
    print "run time:\t\t\t", runtime
    print "---------------------------------------------"
    print "Time spent on:"

    # initialtime = toc_initial-tic_initial
    # print "\tInitial stuff: \t\t%4.2f (%4.2f%%)" % (initialtime, (initialtime/runtime)*100)

    # readtime = np.sum(toc_read-tic_read)
    # print "\tReading in fields: \t%4.2f (%4.2f%%)" % (readtime, (readtime/runtime)*100)

    # zinterptime = np.sum(toc_zinterp-tic_zinterp)
    # print "\tZ interpolation: \t%4.2f (%4.2f%%)" % (zinterptime, (zinterptime/runtime)*100)

    # tractime = np.sum(toc_tracmass-tic_tracmass)
    # print "\tTracmass: \t\t%4.2f (%4.2f%%)" % (tractime, (tractime/runtime)*100)
    # print "============================================="

    # Save results to netcdf file
    if tp.dostream:
        inout.savetracks(lonp, latp, zp, ttend, tp.name, tp.nsteps, tp.N, tp.ff, tp.tseas_use, tp.ah, tp.av, \
                            tp.do3d, tp.doturb, tp.currents_filename, tp.T0, tp.U, tp.V)
        return lonp, latp, zp, ttend, tp.grid, T0, U, V
    else:
        inout.savetracks(lonp, latp, zp, ttend, tp.name, tp.nsteps, tp.N, tp.ff, tp.tseas_use, tp.ah, tp.av, \
                            tp.do3d, tp.doturb, tp.currents_filename)
        return lonp, latp, zp, ttend, tp.grid

# def start_run():
#     '''
#     Choose what initialization from above and then run.
#     '''

#     # Choose which initialization to use
#     loc,nsteps,ndays,ff,date,tseas,ah,av,lon0,lat0,z0,zpar,do3d,doturb,name = init.test1()

#     # Run tracmass!
#     lonp,latp,zp,t,grid = run(loc,nsteps,ndays,ff,date,tseas,ah,av,lon0,lat0,z0,zpar,do3d,doturb,name)

#     # pdb.set_trace()

#     # Plot tracks
#     plotting.tracks(lonp,latp,name,grid=grid)

#     # Plot final location (by time index) histogram
#     plotting.hist(lonp,latp,name,grid=grid,which='contour')
#     plotting.hist(lonp,latp,name,grid=grid,which='pcolor')  