"""qCSF adaptive test (10AFC), observer at 57 cm (1cm~1deg)"""

from psychopy import core, visual, gui, event
from matplotlib import pyplot as plt
from my_functions import weibull, csf, entropy, plot_qCSF
import numpy as np

# Ask name for saving results
output_dialogue = {'Name':'random'}
gui.DlgFromDict(output_dialogue,title="Insert name")
filename = list(output_dialogue.values())[0]

letters = np.array(np.load('letters.npy'))  # Loading letters
nSF = 9                             # number of spatial frequencies
nC = 10                             # number of contrast
spatial_frequencies = np.logspace(-1,2,nSF)
contrast = np.logspace(-3,0,nC)
letter_code = ['c','d','h','k','n','o','r','s','v','z']
nL = len(letters[1,1,:,1])          # number of letters
nP = len(letters[:,1,1,1])          # number of pixels
nTrial = 50                         # number of trials
nPar = 4                            # number of parameters
nVal = 10                           # number of values for each parameter
nSam = 100                          # number of samples (from all param combination)
nVec = nVal**nPar                   # number of all possible param combinations
nStim = nC*nSF                      # number of possible stimuli
stimuli = np.ones((nStim,2))
stimuli[:,0] = np.tile(contrast,nSF)                # contrast
stimuli[:,1] = np.repeat(spatial_frequencies,nC)    # spatial frequency

# 4D param space (log units)
p0a,p0b = -1,2 
p1a,p1b = 0,3 
p2a,p2b = 0,1
p3a,p3b = 0.02,2
param_space = np.ones((nVal,nPar))
param_space[:,0] = np.linspace(p0a,p0b,nVal)    # peak frequency (cpd)
param_space[:,1] = np.linspace(p1a,p1b,nVal)    # peak gain sensitivity (1/cntrast)
param_space[:,2] = np.linspace(p2a,p2b,nVal)    # FWHM (cpd)
param_space[:,3] = np.linspace(p3a,p3b,nVal)    # truncation (decades)

# 4D vectors (all possible param combinations)
param_vector = np.ones((nVec,nPar))
param_vector[:,0] = np.repeat(param_space[:,0],nVal**(nPar-1))
param_vector[:,1] = np.tile(np.repeat(param_space[:,1],nVal**(nPar-2)),nVal**(nPar-3))
param_vector[:,2] = np.tile(np.repeat(param_space[:,2],nVal**(nPar-3)),nVal**(nPar-2))
param_vector[:,3] = np.tile(param_space[:,3],nVal**(nPar-1))
prior = np.ones(nVec)/nVec # flat prior

win = visual.Window([1920,1080], monitor="testMonitor", screen=1,  units="norm")
intro1 = visual.TextStim(win, pos=[0,0.25], text='Press on keyboard the letter you see', color=[-1,-1,-1], height=0.08)
intro2 = visual.TextStim(win, pos=[0,0], text='Turn CAPS LOCK off', color=[-1,-1,-1], height=0.08)
intro3 = visual.TextStim(win, pos=[0,-0.25], text='Press SPACEBAR to start the experiment', color=[-1,-1,-1], height=0.08)
fixation = visual.GratingStim(win, size=0.007, mask='circle', sf=0, color=[-1,-1,-1])
completion = visual.TextStim(win, pos=[-0.92,0.92], color=[-1,-1,-1], height=0.08)
letter_display = visual.TextStim(win, pos=[0.82,0.92], color=[-1,-1,-1], text="".join(letter_code).upper(), height=0.08)
image = visual.ImageStim(win,units="pix",size=nP)

intro1.draw()
intro2.draw()
intro3.draw()
win.flip()
event.waitKeys(keyList=['space'])

for t in range(nTrial):

    string_compl = str(round(100*(t)/nTrial,1))+"%"
    completion.setText(string_compl)
    completion.draw()
    letter_display.draw()
    fixation.draw()
    win.flip()
    core.wait(0.5)
    
    a = np.random.randint(nL)
    info_stimulus = np.ones(nStim)
    ind_sampled = np.random.choice(np.arange(nVec),nSam,p=prior) # sampling param space
    for stim in range(nStim):
        con = stimuli[stim,0]
        sf = stimuli[stim,1]
        prob_stimulus = 0
        for sam in ind_sampled:
            prob_stimulus += prior[sam]*weibull(param_vector[sam,:],np.log10(con),np.log10(sf))/nVec
        info_stimulus[stim] = entropy(prob_stimulus)
    best_stim = np.argsort(-info_stimulus)   # sort in descending order
    ind = np.random.randint(round(nStim/10)) # random pick from top decile
    next_stim = best_stim[ind]
    con_best = stimuli[next_stim,0]
    sf_best = stimuli[next_stim,1]
    
    im = letters[:,:,a,int(np.floor(next_stim/nC))] # choosing next stimulus
    image.setImage(im)
    image.setContrast(con_best)
    completion.draw()
    letter_display.draw()
    image.draw() # display stimulus
    win.flip()
    core.wait(0.1)
    
    completion.draw()
    letter_display.draw()
    fixation.draw()
    win.flip()
    kb = event.waitKeys(keyList=letter_code)
    correctness = letter_code[a]==kb[0]
    
    prob_correct = np.ones(nVec)
    for vec in range(nVec):
        tmp = weibull(param_vector[vec,:],np.log10(con_best),np.log10(sf_best))
        if correctness:
            prob_correct[vec] = tmp
        else:
            prob_correct[vec] = 1 - tmp
    response_rate = np.sum(np.multiply(prob_correct,prior))
    posterior = np.multiply(prob_correct,prior)/response_rate
    prior = posterior

win.close()
ind = np.argmax(posterior)
best_param = param_vector[ind,:]
print(best_param)
plot_qCSF(best_param,posterior,nVal)
np.save(filename,best_param)
core.quit()