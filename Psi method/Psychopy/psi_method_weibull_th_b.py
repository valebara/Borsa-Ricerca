from psychopy import core, visual, gui, event
import matplotlib.pyplot as plt
import numpy as np

def WEIBULL(x,th,b,g=0.5,d=0.02):
    
    # x   stimulus intensity
    # th  threshold
    # b   slope
    # g   guess rate
    # d   lapse rate
    
    w = 1-d - (1-g-d)*np.exp(-(x/th)**b)
    
    return w

nStim = 100
nVal = 20
nPar = 2     # th,b

# All stimulus intensities (i.e. contrast values)
x_space = np.logspace(-3,0,nStim)

# All possible values of parameters (th,b)...
theta_space = np.zeros((nVal,nPar))
theta_space[:,0] = np.logspace(-3,-1,nVal)      # th
theta_space[:,1] = np.logspace(0,1,nVal)        # b

# ...and combinations (param vectors)
nVec = nVal**nPar
theta_vector = np.zeros((nVec,nPar))
for p in range(nPar):
    theta_vector[:,p] = np.tile(np.repeat(theta_space[:,p],nVal**(nPar-p-1)),nVal**p)

# Probability of response (success) to stimulus x, given parameters (theta)... p(failure) = 1-p(success)
psi = np.zeros((nStim,nVec))
for i,[th,b] in enumerate(theta_vector):
    psi[:,i] = WEIBULL(x_space,th,b)
    
prior = np.ones(nVec)/nVec

# List of posterior update and expectd entropy
POSTERIOR = []
ENTROPY = []

nTrial = 30

# Create window, stimulus and intro
win = visual.Window([1920,1080], monitor="testMonitor", screen=1,  units="norm")
stimulus = visual.GratingStim(win,mask='gauss',units='deg',size=5, sf=0)
intro = visual.TextStim(win, text='Press SPACEBAR to start the experiment', color=[-1,-1,-1], height=0.08)
intro.draw()
win.flip()
event.waitKeys(keyList=['space'])
location = ['left','right']

for t in range(nTrial):
    
    # 1)
    p_success = np.matmul(psi,prior)
    p_failure = 1-p_success
    
    # 2)
    posterior_success = np.zeros((nStim,nVec))
    posterior_failure = np.zeros((nStim,nVec))
    for i in range(nStim):
        for j in range(nVec):
            posterior_success[i,j] = psi[i,j]*prior[j]/p_success[i]
            posterior_failure[i,j] = (1-psi[i,j])*prior[j]/p_failure[i]

    # 3)
    post_entropy_success = np.zeros(nStim)
    post_entropy_failure = np.zeros(nStim) 
    for i in range(nStim):
        post_entropy_success[i] = -sum(posterior_success[i,:]*np.log(posterior_success[i,:]))
        post_entropy_failure[i] = -sum(posterior_failure[i,:]*np.log(posterior_failure[i,:]))
        
    # 4)
    expected_post_entropy = p_success*post_entropy_success + p_failure*post_entropy_failure
    ENTROPY.append(expected_post_entropy)
    
    # 5)
    ind_next = np.argmin(expected_post_entropy)
    x_next = x_space[ind_next]
    
    # 6)
    stimulus.setContrast(x_next)
    loc = np.random.randint(2)
    stimulus.setPos([15*loc-7.5,0])
    stimulus.draw()
    win.flip()
    core.wait(0.5)
    win.flip()
    kb = event.waitKeys(keyList=location)
    correctness = location[loc]==kb[0]
    
    # 7)
    if correctness:
        prior = psi[ind_next,:]*prior/p_success[ind_next]
    else:
        prior = (1-psi[ind_next,:])*prior/p_failure[ind_next]
        
    POSTERIOR.append(prior)

p_theta = np.zeros((nVal,nPar))

for i in range(nVal):
        for p in range(nPar):
            ind = np.arange(nVec/nVal**(nPar-p-1))
            tmp = np.repeat(ind%nVal,nVal**(nPar-p-1))
            x = np.argwhere(tmp==i)
            p_theta[i,p] = sum(prior[x])
th_est, b_est =  sum(theta_space[:,0]*p_theta[:,0]) , sum(theta_space[:,1]*p_theta[:,1])

win.close()

plt.subplot(121)
plt.plot(theta_space[:,0],p_theta[:,0],label='Posterior th')
plt.title(f'th estimated = {th_est:.2f}')
plt.legend()
plt.subplot(122)
plt.plot(theta_space[:,1],p_theta[:,1],label='Posterior th')
plt.title(f'b estimated = {b_est:.2f}')
plt.legend()
plt.show()

core.quit()