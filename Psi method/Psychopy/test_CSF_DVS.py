"""CSF test (2AFC), observer at 57 cm (1cm~1deg)"""

from psychopy import core, visual, gui, data, event
import numpy as np
import csv

data = np.loadtxt('DVS_input.csv', delimiter=",", dtype=float, skiprows=1)

win = visual.Window([1920,1080], monitor="testMonitor", screen=1,  units="norm")
stimulus = visual.GratingStim(win,mask='gauss',units='deg')

for t in range(len(data)):
    stimulus.sf = data[t,0]
    stimulus.setContrast(data[t,1])
    stimulus.setPos([15*data[t,2]-7.5,0])
    stimulus.draw()
    win.flip()
    core.wait(0.1) # 100 ms stimulus presentation
    win.flip()
    core.wait(0.1) # 100 ms blank screen

win.close()
core.quit()