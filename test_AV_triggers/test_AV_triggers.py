#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:45:20 2019
I have coded this small script just to test whether the triggers are send
@author: alex
"""

import numpy as np
import os
import matplotlib.pyplot as plt

from psychopy import visual, logging, core, event,  gui, data, monitors
from psychopy.tools.filetools import fromFile, toFile # wrappers to save pickles
from psychopy.preferences import prefs
from pandas import DataFrame
from psychopy import parallel
import serial

# Some general presets
event.globalKeys.clear() # implementing a global event to quit the program at any time by pressing ctrl+q
event.globalKeys.add(key='q', modifiers=['ctrl'], func=core.quit)


# Test parameters
ppt = False # Using parallel port to send triggers
sst = True # Using parallel port to send triggers
fullscreen = True
ntrials = 30
gap_dur = 1
grating_dur = 0.2


prefs.hardware['audioLib']=['pyo'] # use Pyo audiolib for good temporal resolution
from psychopy.sound import Sound # This should be placed after changing the audio library

if ppt: p_port = parallel.ParallelPort(address=u'0x0378') # this is for windows
if sst: 
    p_port = serial.Serial('COM3', 115200, timeout = 0) # this is for windows
    p_port.write(b'00')
    core.wait(0.2)
    p_port.write(b'RR')
#p_port_2 = parallel.ParallelPort(address=u'0x0378')
#p_port = parallel.ParallelPort(address='/dev/parport0') # this is for linux

#create a window
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr = fullscreen)

#create some stimuli
grating = visual.GratingStim(win=win, mask="circle", size=3, pos=[-4,0], sf=3)
circle = visual.PatchStim(win, color= [1, 1, 1], tex=None, pos=[-4,0],mask='circle', size=3)
fixation = visual.GratingStim(win=win, size=0.5, pos=[0,0], sf=0, color = [-1,-1,-1])

Hz = 0
while (Hz < 50 or  Hz > 150):
    Hz = win.getActualFrameRate(nIdentical=20, nMaxFrames=80,nWarmUpFrames=10)
    Hz = round(Hz)
    print(Hz)
ifi = 1/Hz




gap_frames = round(gap_dur/ifi)
grating_frames = round(grating_dur/ifi)

# create sound
medf_s = Sound(800, sampleRate=44100, secs=grating_frames*ifi, stereo=True ,loops=0)

trial_times = np.array([]) 
 
trial_times = win.flip()
for itrial in range(ntrials):
    for gframe in range(int(gap_frames)):
        #print(gframe)
        fixation.draw()
        win.flip()
        
    for gtframe in range(int(grating_frames)):   
        if gtframe == 0:     
            if ppt: win.callOnFlip(p_port.setData, int(itrial+1))
            if sst: win.callOnFlip(p_port.write, b'01')
            medf_s.play()
        if gtframe == 1: 
            if ppt: win.callOnFlip(p_port.setData, int(0))
            if sst: win.callOnFlip(p_port.write, b'00')
        #print(gtframe) 
        #grating.draw()
        circle.draw()
        fixation.draw()
        
        if gtframe == 0: 
            t = win.flip()
            trial_times = np.append(trial_times, t)
        else:
            win.flip
            
        
#p_port.stop()
diff_times  =  np.diff( trial_times)
win.close()
if ppt: p_port.close()
if sst: p_port.close()
#core.quit()
