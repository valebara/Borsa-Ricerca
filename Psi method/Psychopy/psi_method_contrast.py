"""psi method for contrast sensitivity (2AFC), observer at 57 cm (1cm~1deg)"""

from psychopy import core, visual, gui, event
from matplotlib import pyplot as plt
from my_functions import weibull, csf, entropy, plot_qCSF
import numpy as np

# Define some functions

def sigmoid

def entropy

# Set some variables
nC = 100                            # number of contrast
contrast = np.logspace(-3,0,nC)
nTrial = 50                         # number of trials
nPar = 2                            # number of parameters
nVal = 20                           # number of values for each parameter
nSam = 100                          # number of samples (from all param combination)
nVec = nVal**nPar                   # number of all possible param combinations

# 2D param space
param_space = np.ones((nVal,nPar))
param_space[:,0] = np.logspace(-3,0,nVal)    # threshold
param_space[:,1] = np.logspace(0,0.5,nVal)   # slope

# 2D vectors (all possible param combinations)
param_vector = np.ones((nVec,nPar))
param_vector[:,0] = np.repeat(param_space[:,0],nVal**(nPar-1))
param_vector[:,1] = np.tile(np.repeat(param_space[:,1],nVal**(nPar-2)),nVal**(nPar-3))

# Define prior (i.e. flat or from previous experiment)
prior = np.ones(nVec)/nVec 

# Intro to experiment
win = visual.Window([1920,1080], monitor="testMonitor", screen=1,  units="norm")
intro = visual.TextStim(win, text='Press SPACEBAR to start the experiment', color=[-1,-1,-1], height=0.08)
completion = visual.TextStim(win, pos=[-0.92,0.92], color=[-1,-1,-1], height=0.08)
stimulus = visual.GratingStim(win,mask='gauss',units='deg')

intro.draw()
win.flip()
event.waitKeys(keyList=['space'])

''' Experiment trials '''

for t in range(nTrial):

    # Show completion percentage
    string_compl = str(round(100*(t)/nTrial,1))+"%"
    completion.setText(string_compl)
    completion.draw()
    win.flip()
    #core.wait(0.5)
    
    # Random location for stimulus
    loc = np.random.randint(1)
    
    # Information gain for each stimulus (i.e. contrast level)
    info_gain = np.ones(nC) 
    for i,con in enumerate(contrast):
        prob_stimulus = 0       # Probability stimulus is correctly seen (for all possible param combination...
        for j,param in enumerate(param_vector):
            prob_stimulus += prior[j] * sigmoid(param,con) # ...weighted with prior)
        info_gain[i] = entropy(prob_stimulus)
    best_stim = np.argsort(-info_gain)[0] # Sorted in descending order
    
    # Show stimulus... 
    completion.draw()
    stimulus.setContrast(contrast(best_stim))
    stimulus.setPos([15*loc-7.5,0])
    stimulus.draw()
    win.flip()
    
    # ...and collect response
    kb = event.waitKeys(keyList=['left','right'])
    if kb[0] = 'left':
        kb_val = 0
    else:
        kb_val = 1
    correctness = loc==kb_val
    
    # Calculate p(response|param,stim) for each param combination and for each stimulus
    prob_response = np.ones(nVec)
    for j,param in enumerate(param_vector):
        tmp = sigmoid(param,con)
        if correctness:
            prob_response[j] = tmp
        else:
            prob_response[j] = 1 - tmp
    
    # Calculate marginal probability of the response
    prob_response_marginal = sum(np.multiply(prob_correct,prior))
    
    # Update prior to posterior with bayes rule
    posterior = np.multiply(prob_correct,prior)/response_rate
    
    # Prior at trial t+1 is set as posterior at trial t 
    prior = posterior

# Estimate the parameters as the mean of the marginal posterior
ind = np.argmax(posterior)

win.close()
core.quit()