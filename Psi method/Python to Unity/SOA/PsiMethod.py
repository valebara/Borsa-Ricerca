def InitData(SOA_min, SOA_max, PSS_min, PSS_max, TBW_min, TBW_max, nVal, nSOA):
    
    import numpy as np
    
    def GAUSSIAN(SOA,PSS,TBW,h=1):
    
        SD = (TBW-PSS)/np.log(4)
    
        g = h * np.exp(-((SOA-PSS)/SD)**2/2)
    
        return g
    
    nPar = 2 # PSS, TWB
    
    # SOA values
    SOA_space = np.linspace(SOA_min,SOA_max,nSOA) # ms
    
    # All possible values of parameters (PSS, TWB)...
    param_space = np.zeros((nVal,nPar))
    param_space[:,0] = np.linspace(PSS_min,PSS_max,nVal) # PSS
    param_space[:,1] = np.linspace(TBW_min,TBW_max,nVal) # TWB

    # ...and combinations (param vectors)
    nComb = nVal**nPar
    param_comb = np.zeros((nComb,nPar))
    for p in range(nPar):
        param_comb[:,p] = np.tile(np.repeat(param_space[:,p],nVal**(nPar-p-1)),nVal**p)

    # Probability of response (success) to stimulus, given parameters (theta)... p(failure) = 1-p(success)
    lookup_table = np.zeros((nSOA,nComb))
    for i,[PSS,TWB] in enumerate(param_comb):
        lookup_table[:,i] = GAUSSIAN(SOA_space,PSS,TWB)
    
    prior = np.ones(nComb)/nComb
    
    return lookup_table, prior, SOA_space, param_space
    
def GetCurrentTrial(lookup_table, prior, nSOA, nVal):
    
    import numpy as np
    
    nComb = nVal**2 # Combinations (param vectors)
    
    # 1) Compute probability of success and failure (for all stimuli)
    p_success = np.matmul(lookup_table,prior)
    p_failure = 1-p_success
    
    # 2) Compute posterior probability (for each param and stimuli), for both success and failure
    posterior_success = np.zeros((nSOA,nComb))
    posterior_failure = np.zeros((nSOA,nComb))
    for i in range(nSOA):
        for j in range(nComb):
            posterior_success[i,j] = lookup_table[i,j]*prior[j]/p_success[i]
            posterior_failure[i,j] = (1-lookup_table[i,j])*prior[j]/p_failure[i]

    # 3) Compute entropy of posterior probability (for each stimuli), for both success and failure
    post_entropy_success = np.zeros(nSOA)
    post_entropy_failure = np.zeros(nSOA) 
    for i in range(nSOA):
        post_entropy_success[i] = -sum(posterior_success[i,:]*np.log(posterior_success[i,:]))
        post_entropy_failure[i] = -sum(posterior_failure[i,:]*np.log(posterior_failure[i,:]))
        
    # 4) Compute total expected entropy
    expected_post_entropy = p_success*post_entropy_success + p_failure*post_entropy_failure
    
    # 5) Find next stimulus (minimizing expected entropy)
    SOA_next = np.argmin(expected_post_entropy)
    
    return SOA_next, p_success

def UpdatePrior(lookup_table, prior, p_success, response, SOA_next):
    
    import numpy as np
    
    if response:
        prior_updated = lookup_table[SOA_next,:]*prior/p_success[SOA_next]
    else:
        prior_updated = (1-lookup_table[SOA_next,:])*prior/(1-p_success[SOA_next])
        
    return prior_updated

def SaveResults(nVal, prior, param_space):
    
    import numpy as np
    import matplotlib.pyplot as plt
    import csv
    
    nComb = nVal**2
    nPar = 2 #PSS,TBW
    prob_param = np.zeros((nVal,nPar))

    for i in range(nVal):
        for p in range(nPar):
            ind = np.arange(nComb/nVal**(nPar-p-1))
            tmp = np.repeat(ind%nVal,nVal**(nPar-p-1))
            x = np.argwhere(tmp==i)
            prob_param[i,p] = sum(prior[x])

    plt.subplot(121)
    plt.plot(param_space[:,0],prob_param[:,0])
    plt.subplot(122)
    plt.plot(param_space[:,1],prob_param[:,1])
    plt.show()

    # PSS_est = theta_space[np.argmax(p_theta[:,0]),0]

    PSS_est, TBW_est =  sum(param_space[:,0]*prob_param[:,0]) , sum(param_space[:,1]*prob_param[:,1])
    # print(f'PSS estimated = {PSS_est:.2f}\nTBW estimated = {TBW_est:.2f}')
    
    with open('ParamEstim.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([PSS_est, TBW_est])
    
    with open('ParamValues.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(param_space)

    with open('ParamProb.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(prob_param)