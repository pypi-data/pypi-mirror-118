#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 15:02:26 2021

@author: thomas
"""

import sys
import time
import ephem
import pickle
import scipy as sp
import numpy as np
import numpy.linalg as la
from scipy import signal, stats
from datetime import datetime
from datetime import timezone
from tqdm import tqdm
import gc
import os

from maria import resources
from maria import tools
from maria import objects

import pkg_resources
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#exec(open('mpl_defs').read())



default_setup_config = {'fov_tolerance' : 1e-2, # proportion larger of the FOV to make the generated atmosphere 
                            'n_fov_edge' : 64, 
                        'n_center_azimuth_sample' : 16, 
                         'n_sidereal_time_sample' : 16, 
                                   'n_sample_max' : 10000}

class model():
    
    def __init__(self, site_config=None,
                       array_config=None, 
                       beams_config=None, 
                       pointing_config=None, 
                       atmosphere_config=None,
                       setup_config=default_setup_config, verbose=False):
        
        self.site       = objects.site(config=site_config)
        self.array      = objects.array(config=array_config)
        self.beams      = objects.beams(config=beams_config)
        self.pointing   = objects.pointing(config=pointing_config)
        self.atmosphere = objects.atmosphere(config=atmosphere_config)
        
        ### ==================================================================
        ### We've sorted a lot of parameters into interactive classes. But we need to combine them to find some model parameters.
        
        
        # Here we compute parameters related to the beam waists for each layer. This means different things for different beam models.
        self.beams_waists = self.beams.waist(self.atmosphere.depths,
                                             self.beams.aperture,
                                             self.array.band[0])
        
        self.ang_waist = self.beams_waists / self.atmosphere.depths 
        self.ang_res   = self.beams.beam_res * self.ang_waist
        
        # Here we make an imaginary array that bounds the true array, which helps to determine the geometry of the atmosphere to simulate. 
        self.array.edge_r = (1+setup_config['fov_tolerance']) * (np.abs(self.array.z).max() + self.ang_res/2)
        self.array.edge_z = self.array.edge_r[:,None] * np.exp(1j*np.linspace(0,2*np.pi,setup_config['n_fov_edge']+1)[1:])[None,:]
        self.array.edge_x, self.array.edge_y = np.real(self.array.edge_z), np.imag(self.array.edge_z)
        
        self.atmosphere.turb_nu = 5/6
        
        # this defines the relative strength of pwv fluctuations
        self.atmosphere.heights = self.atmosphere.depths * np.sin(self.pointing.center_elev.mean())
        self.atmosphere.wvmd = np.interp(self.atmosphere.heights,self.site.weather['heights'],self.site.weather['water_vapor_mass_density'])
        self.atmosphere.temp = np.interp(self.atmosphere.heights,self.site.weather['heights'],self.site.weather['temperature'])
        self.gen_scaling = self.atmosphere.wvmd * self.atmosphere.temp
        self.lay_scaling = self.atmosphere.config['atmosphere_rms'] * np.sqrt(np.square(self.gen_scaling)/np.square(self.gen_scaling).sum())
        
        
        
        ### ==================================================================
        ### Here we compute time-ordered pointing angles and velocities. 
        
        self.pointing.azim, self.pointing.elev = tools.from_xy(self.array.x[:,None], 
                                                               self.array.y[:,None], 
                                                               self.pointing.focal_azim[None,:], 
                                                               self.pointing.focal_elev[None,:])

        self.pointing.azim_motion = (np.gradient(np.sin(self.pointing.focal_azim)) * np.cos(self.pointing.focal_azim) 
                                    -np.gradient(np.cos(self.pointing.focal_azim)) * np.sin(self.pointing.focal_azim)) / np.gradient(self.pointing.time) 
        
        self.pointing.elev_motion = (np.gradient(np.sin(self.pointing.focal_elev)) * np.cos(self.pointing.focal_elev) 
                                    -np.gradient(np.cos(self.pointing.focal_elev)) * np.sin(self.pointing.focal_elev)) / np.gradient(self.pointing.time) 
        
        # Here we compute the focal angular velocities
        self.atmosphere.wind_east  = np.interp(self.atmosphere.depths,self.site.weather['heights'],self.site.weather['wind_east']) 
        self.atmosphere.wind_north = np.interp(self.atmosphere.depths,self.site.weather['heights'],self.site.weather['wind_north']) 
        self.atmosphere.wind_speed = np.abs(self.atmosphere.wind_north+1j*self.atmosphere.wind_east)
        self.atmosphere.wind_bear  = np.angle(self.atmosphere.wind_north+1j*self.atmosphere.wind_east)
    
        self.pointing.omega_x = (self.atmosphere.wind_east[:,None] * np.cos(self.pointing.focal_azim[None,:]) \
                              - self.atmosphere.wind_north[:,None] * np.sin(self.pointing.focal_azim[None,:])) / self.atmosphere.depths[:,None] \
                           + self.pointing.azim_motion[None,:] * np.cos(self.pointing.focal_elev[None,:]) 
        self.pointing.omega_y = -(self.atmosphere.wind_east[:,None] * np.sin(self.pointing.focal_azim[None,:]) \
                               - self.atmosphere.wind_north[:,None] * np.cos(self.pointing.focal_azim[None,:])) / self.atmosphere.depths[:,None] * np.sin(self.pointing.focal_elev[None,:]) \
                           + self.pointing.elev_motion[None,:]
        self.pointing.omega_z = self.pointing.omega_x + 1j*self.pointing.omega_y
                           
        
        # Here we compute the time-ordered focal angular positions
        
        self.pointing.focal_theta_z = np.cumsum(self.pointing.omega_z * np.gradient(self.pointing.time)[None,:],axis=-1)
        
        self.pointing.theta_z  = self.array.z[None,:,None] + self.pointing.focal_theta_z[:,None,:]
        #self.pointing.theta_z -= self.pointing.theta_z.mean()
        self.pointing.theta_x, self.pointing.theta_y = np.real(self.pointing.theta_z), np.imag(self.pointing.theta_z)
        
        ### These are empty lists we need to fill with chunky parameters (they won't fit together!) for each layer. 
        self.para, self.orth, self.X, self.Y, self.P, self.O = [], [], [], [], [], []
        self.n_para, self.n_orth, self.genz, self.AR_samples = [], [], [], []
        
        self.pointing.zop = np.zeros((self.pointing.theta_z.shape),dtype=complex)
        self.pointing.p   = np.zeros((self.pointing.theta_z.shape))
        self.pointing.o   = np.zeros((self.pointing.theta_z.shape))
        
        self.MARA = []
        self.atmosphere.outer_scale, self.atmosphere.turb_nu = 500, 5/6
        self.ang_outer_scale = self.atmosphere.outer_scale / self.atmosphere.depths
        
        aam_weight = np.square(self.atmosphere.depths * self.lay_scaling)[:,None]
        
        self.atmosphere.aam  = np.sum(aam_weight*self.pointing.omega_z,axis=0) / np.sum(aam_weight*np.square(self.pointing.omega_z),axis=0)
        self.atmosphere.aam /= np.square(np.abs(self.atmosphere.aam))
        
        self.pointing.theta_edge_z = []
        
        for i_l, depth in enumerate(self.atmosphere.depths):
                        
            # an efficient way to compute the minimal observing area that we need to generate
            
            try:
                edge_hull = sp.spatial.ConvexHull(points=np.vstack([np.real(self.pointing.focal_theta_z[i_l]).ravel(),
                                                                    np.imag(self.pointing.focal_theta_z[i_l]).ravel()]).T)
                edge_hull_z  = self.pointing.focal_theta_z[i_l].ravel()[edge_hull.vertices]
            except:
                edge_hull_z = self.pointing.focal_theta_z[i_l][np.array([0,-1])]
            
            
            theta_edge_z = self.array.edge_z[i_l][:,None] + edge_hull_z[None,:]
            
            self.pointing.theta_edge_z.append(theta_edge_z)

            self.MARA.append(tools.get_MARA(theta_edge_z.ravel()))
            RZ = theta_edge_z * np.exp(1j*self.MARA[-1])
            
            para_min, para_max = np.real(RZ).min(), np.real(RZ).max()
            orth_min, orth_max = np.imag(RZ).min(), np.imag(RZ).max()
            
            para_center, orth_center = (para_min + para_max)/2, (orth_min + orth_max)/2
            para_radius, orth_radius = (para_max - para_min)/2, (orth_max - orth_min)/2
            
            para_ = np.linspace(para_center-para_radius,para_center+para_radius,int(np.ceil(2*para_radius/self.ang_res[i_l])))
            orth_ = np.linspace(orth_center-orth_radius,orth_center+orth_radius,int(np.ceil(2*orth_radius/self.ang_res[i_l])))
            
            self.para.append(para_), self.orth.append(orth_)
            self.n_para.append(len(para_)), self.n_orth.append(len(orth_))
        
            ORTH_,PARA_ = np.meshgrid(orth_,para_)
            
            self.genz.append(np.exp(-1j*self.MARA[-1]) * (PARA_[0] + 1j*ORTH_[0] - self.ang_res[i_l]) )
            layer_ZOP = np.exp(-1j*self.MARA[-1]) * (PARA_ + 1j*ORTH_) 
            
            self.X.append(np.real(layer_ZOP)), self.Y.append(np.imag(layer_ZOP))
            self.O.append(ORTH_), self.P.append(PARA_)
            
            self.pointing.zop[i_l] = self.pointing.theta_z[i_l] * np.exp(1j*self.MARA[-1]) 
            self.pointing.p[i_l], self.pointing.o[i_l] = np.real(self.pointing.zop[i_l]), np.imag(self.pointing.zop[i_l])

            cov_args = (1,1)
            
            para_i, orth_i = [],[]
            for i in np.r_[0,2**np.arange(np.ceil(np.log(self.n_para[-1])/np.log(2))),self.n_para[-1]-1]:
                
                #if i * self.ang_res[i_l] > 2 * self.ang_outer_scale[i_l]:
                #    continue
                
                orth_i.append(np.unique(np.linspace(0,self.n_orth[-1]-1,int(np.maximum(self.n_orth[-1]/(i+1),16))).astype(int)))
                para_i.append(np.repeat(i,len(orth_i[-1])).astype(int))
                
            self.AR_samples.append((np.concatenate(para_i),np.concatenate(orth_i)))
            
        if verbose:
            print(f'\n # | depth (m) | d_A (m) | rms (mK) | cm_side | width | length | h2o (g/m3) | temp (K) | ws (m/s) | wb (deg) |')
            
            for i_l, depth in enumerate(self.atmosphere.depths):
                
                row_string  = f'{i_l+1:2} | {depth:9.02f} | {self.beams_waists[i_l]:7.02f} | {self.lay_scaling[i_l]:8.02f} | {len(self.AR_samples[i_l][0]):7} | {self.n_orth[i_l]:5} |'
                row_string += f' {self.n_para[i_l]:6} | {1e3*self.atmosphere.wvmd[i_l]:10.04f} | {self.atmosphere.temp[i_l]:8.02f} |'
                row_string += f' {self.atmosphere.wind_speed[i_l]:8.02f} | {np.degrees(self.atmosphere.wind_bear[i_l]+np.pi):8.02f} |'
                print(row_string)
                
        
        self.prec, self.csam, self.cgen, self.A, self.B = [], [], [], [], []
        
        with tqdm(total=len(self.atmosphere.depths),desc='Computing weights') as prog:
            for i_l, (depth, LX, LY, AR, GZ) in enumerate(zip(self.atmosphere.depths,self.X,self.Y,self.AR_samples,self.genz)):
                
                cov_args  = (self.atmosphere.outer_scale / depth, self.atmosphere.turb_nu)
                
                self.prec.append(la.inv(tools.make_2d_covariance_matrix(self.atmosphere.matern,cov_args,LX[AR],LY[AR])))
                
                self.cgen.append(tools.make_2d_covariance_matrix(self.atmosphere.matern,cov_args,np.real(GZ),np.imag(GZ)))
                
                self.csam.append(tools.make_2d_covariance_matrix(self.atmosphere.matern,cov_args,np.real(GZ),np.imag(GZ),LX[AR],LY[AR],auto=False)) 
                
                self.A.append(np.matmul(self.csam[i_l],self.prec[i_l])) 
                self.B.append(tools.msqrt(self.cgen[i_l]-np.matmul(self.A[i_l],self.csam[i_l].T)))
                
                prog.update(1)
        
    def atmosphere_timestep(self,i): # iterate the i-th layer of atmosphere by one step
        
        self.vals[i] = np.r_[(np.matmul(self.A[i],self.vals[i][self.AR_samples[i]])
                            + np.matmul(self.B[i],np.random.standard_normal(self.B[i].shape[0])))[None,:],self.vals[i][:-1]]

    def generate_atmosphere(self,blurred=False):

        self.vals = [np.zeros(lx.shape) for lx in self.X]
        n_init_   = [n_para for n_para in self.n_para]
        n_ts_     = [n_para for n_para in self.n_para]
        tot_n_init, tot_n_ts = np.sum(n_init_), np.sum(n_ts_)
        #self.gen_data = [np.zeros((n_ts,v.shape[1])) for n_ts,v in zip(n_ts_,self.lay_v_)]

        with tqdm(total=tot_n_init,desc='Generating layers') as prog:
            for i, n_init in enumerate(n_init_):
                for i_init in range(n_init):
                    
                    self.atmosphere_timestep(i)
                    
                    prog.update(1)
            
        #with tqdm(total=tot_n_ts,desc='Generating atmosphere') as prog:
        #    for i, n_ts in enumerate(n_ts_):
        #        for i_ts in range(n_ts):
        #            prog.update(1)
        #            self.atmosphere_timestep(i)
        #            #self.gen_data[i][i_ts] = self.lay_v_[i_layer][0]

        if blurred:
            for i_l, l in enumerate(self.atmosphere.depths):
                self.vals[i_l] = sp.ndimage.gaussian_filter(self.vals[i_l],sigma=self.beams.beam_res/2)
                #self.vals[i_l] = sp.ndimage.gaussian_filter1d(self.vals[i_l],axis=1,sigma=self.beams.beam_res/2)
                
             
    
                
    
    def sim(self, do_atmosphere=True, 
                    do_cmb=False, 
                    do_noise=False,
                    interp_method=None,
                    split_layers=True,
                    sky_per_det=16):
        
        self.generate_atmosphere(blurred=True)
        
        lay_vals = np.zeros(self.pointing.theta_z.shape)
        
        self.pointing.theta_x, self.pointing.theta_y
        
        
        with tqdm(total=len(self.atmosphere.depths),desc='Sampling atmosphere') as prog:
            
            for ilay, depth in enumerate(self.atmosphere.depths): 
                 
                RGI = sp.interpolate.RegularGridInterpolator((self.para[ilay],self.orth[ilay]),self.vals[ilay])
                lay_vals[ilay] = RGI((self.pointing.p[ilay],self.pointing.o[ilay]))
                prog.update(1)
                
                
        

        return (lay_vals*self.lay_scaling[:,None,None]).sum(axis=0) / np.sin(self.pointing.elev)
        
test = True

#tm = model(verbose=True)
#tm.sim()



if test:
        
        #self.build_focal_plane_layers()
        
    atmosphere_config = {'n_layers'        : 16,         # how many layers to simulate, based on the integrated atmospheric model 
                        'min_depth'        : 500,      # the height of the first layer 
                        'max_depth'        : 20000,      # 
                        'atmosphere_rms'   : 50,  
                        'turbulence_model' : 'scale_invariant',
                        'outer_scale'      : 500}
    
    
    time_ = np.linspace(0,600,6000)
     
    phase = 60
    
    focal_x = np.radians(5)*np.cos(1.1*2*np.pi*time_/phase)
    focal_y = np.radians(5)*np.cos(2*np.pi*time_/phase)
    
    focal_azim, focal_elev = tools.from_xy(focal_x,focal_y,0,np.pi/4)
    
    

    
    
    

    
    pointing_config = {'scan_type' : 'lissajous_box',
                        'duration' : 600,'samp_freq' : 50,
                     'center_azim' : -45, 'center_elev' : 30, 
                         'x_throw' : 5, 'x_period' : 21,
                         'y_throw' : 5, 'y_period' : 29}
    
    pointing_config = {'scan_type' : 'lissajous_daisy',
                        'duration' : 60,'samp_freq' : 20,
                     'center_azim' : -45, 'center_elev' : 30, 
                           'throw' : 5, 'r_period' : 21, 'p_period' : 29}
    
    pointing_config = {'scan_type' : 'CES',
                'duration' : 600,'samp_freq' : 20,
             'center_azim' : -45, 'center_elev' : 60, 
                'az_throw' : 5, 'az_speed' : 1.5}
    
            
    array_config = {'shape' : 'hex',
                        'n' : 640,      
                      'fov' : 2,
                     'band' : 1.5e11}    
    
    
    beams_config = {'optical_type' : 'diff_lim',
                    'primary_size' : 5.5,
                      'beam_model' : 'top_hat',
                        'beam_res' : 1 }    
    
    site_config = {'site' : 'ACT',
                   'time' : datetime.now(timezone.utc).timestamp(),
         'weather_source' : 'mean',
                 'region' : 'atacama' } 
    
    heights = np.linspace(0,10000,100)
    
    #site_config = {'site' : 'ACT',
    #               'time' : datetime.now(timezone.utc).timestamp(),
    #            'heights' : heights,
    #            'water_vapor_mass_density' : np.exp(-heights/1000),
    #            'wind_north' : np.sqrt(np.linspace(100,5000,len(heights))) / 2} 
    
    
    
    #print(test_model.pointing.theta_z.shape)
    #print(test_model.pointing.omega_z.shape)
    
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    
    
    mpl.rcParams['figure.dpi'] = 256
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Palatino"],
    })
    
    def equalize(ax):
        xls,yls = ax.get_xlim(),ax.get_ylim()
        x0,y0 = np.mean(xls), np.mean(yls)
        r = np.maximum(-np.subtract(*xls),-np.subtract(*yls))/2
        ax.set_xlim(x0-r,x0+r); ax.set_ylim(y0-r,y0+r)
        return ax
    
    new = True
    sim = True
    
    if new:
        
        #tm = model(verbose=True)
    
        tm = model(atmosphere_config=atmosphere_config,
                   pointing_config=pointing_config,
                   beams_config=beams_config,
                   array_config=array_config,
                   site_config=site_config,
                   verbose=True)
        
        
        
        if sim:
    
            data = tm.sim()
    
    
    
    if sim:
    
        
        fig,ax = plt.subplots(1,1,figsize=(8,8))
        
        ax.pcolormesh(np.degrees(tm.X[-1]),
                      np.degrees(tm.Y[-1]),
                      tm.vals[-1],shading='none',cmap='RdBu_r')
        
        ax.scatter(np.degrees(np.real(tm.pointing.theta_edge_z[-1]).T),
                   np.degrees(np.imag(tm.pointing.theta_edge_z[-1]).T),s=1e-1,c='k')
        
        ax.plot(np.degrees(np.real(tm.pointing.focal_theta_z[-1])),
                np.degrees(np.imag(tm.pointing.focal_theta_z[-1])),c='k')
        
        equalize(ax)
        
        fig,axes = plt.subplots(2,1,figsize=(12,8))
        
        for idet,det in enumerate(np.random.choice(data.shape[0],16,replace=False)):
            axes[0].plot(tm.pointing.time,data[idet])
            axes[1].plot(tm.pointing.time,data[idet]-data.mean(axis=0))
            
        fig,axes = plt.subplots(2,1,figsize=(12,8))
            
        nf = 256
        
        fmids = np.geomspace(1e-3,1e1,nf)
        rfreq = np.exp(np.gradient(np.log(fmids))).mean()
        fbins = np.append(fmids/np.sqrt(rfreq),fmids[-1]*np.sqrt(rfreq)) 
        
        freq = np.fft.fftfreq(tm.pointing.nt,tm.pointing.dt)
        
        ps   = np.square(np.abs(np.fft.fft(data * np.hanning(data.shape[-1])[None,:],axis=-1)))
        mps  = ps.mean(axis=0)
        bmps = sp.stats.binned_statistic(freq,mps,bins=fbins,statistic='mean')[0]
        nn   = ~np.isnan(bmps)
        
        axes[0].plot(fmids[nn],bmps[nn])
        axes[0].plot(fmids[nn],1e2*fmids[nn]**(-8/3))
        axes[0].loglog()
        
        axes[1].scatter(tm.pointing.time,tm.atmosphere.aam)
        
    fig,ax = plt.subplots(1,1,figsize=(6,6))
    
    ax.scatter(np.degrees(tm.array.x),
               np.degrees(tm.array.y))
    
    ax.plot(np.degrees(tm.array.edge_x).T,
            np.degrees(tm.array.edge_y).T)
    
    pt = np.linspace(0,2*np.pi,64)
    
    
    beam_plot_height = int(np.sqrt(len(tm.atmosphere.depths)))
    beam_plot_length = int(np.ceil(len(tm.atmosphere.depths)/beam_plot_height))
    
    if tm.array.n < 200:
        
        fig,axes = plt.subplots(beam_plot_height,beam_plot_length,
                                figsize=(2*beam_plot_length,2*beam_plot_height),constrained_layout=True)#,sharex=True,sharey=True)
        
        fig.suptitle(f'D = {tm.beams.aperture:.02f}m')
        for ilay,depth in enumerate(tm.atmosphere.depths):
            
            iy = ilay % beam_plot_length
            ix = int(ilay / beam_plot_length)
            
            axes[ix,iy].set_title(f'z = {depth:.02f}m')
            axes[ix,iy].plot(np.degrees(tm.array.x+tm.beams_waists[ilay]/depth*np.cos(pt)[:,None]),
                             np.degrees(tm.array.y+tm.beams_waists[ilay]/depth*np.sin(pt)[:,None]),lw=.5)
        
    



    

