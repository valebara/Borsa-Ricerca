def InitData(slant_min, slant_max, th_min, th_max, b_min, b_max, nVal, nSlant):
    
    import numpy as np
    
    def SIGMOID(x,th,b):
    
        AFC = 1/2
        P = AFC + (1-AFC)*1/(1+1*np.exp(-b*(x-th)))
    
        return P
    
    nPar = 2 # th, b
    
    # slant values
    slant_space = np.linspace(slant_min, slant_max, nSlant)
    
    # All possible values of parameters (th, b)...
    param_space = np.zeros((nVal,nPar))
    param_space[:,0] = np.linspace(th_min, th_max, nVal) # th
    param_space[:,1] = np.linspace(b_min, b_max, nVal)   # b

    # ...and combinations (param vectors)
    nComb = nVal**nPar
    param_comb = np.zeros((nComb,nPar))
    for p in range(nPar):
        param_comb[:,p] = np.tile(np.repeat(param_space[:,p], nVal**(nPar-p-1)), nVal**p)

    # Probability of response (success) to stimulus, given parameters (theta)... p(failure) = 1-p(success)
    lookup_table = np.zeros((nSlant,nComb))
    for i, [th,b] in enumerate(param_comb):
        lookup_table[:,i] = SIGMOID(slant_space, th, b)
    
    prior = np.ones(nComb)/nComb
    
    return lookup_table, prior, slant_space, param_space
    
def GetCurrentTrial(lookup_table, prior, nSlant, nVal):
    
    import numpy as np
    
    nComb = nVal**2 # Combinations (param vectors)
    
    # 1) Compute probability of success and failure (for all stimuli)
    p_success = np.matmul(lookup_table,prior)
    p_failure = 1-p_success
    
    # 2) Compute posterior probability (for each param and stimuli), for both success and failure
    posterior_success = np.zeros((nSlant,nComb))
    posterior_failure = np.zeros((nSlant,nComb))
    for i in range(nSlant):
        for j in range(nComb):
            posterior_success[i,j] = lookup_table[i,j]*prior[j]/p_success[i]
            posterior_failure[i,j] = (1-lookup_table[i,j])*prior[j]/p_failure[i]

    # 3) Compute entropy of posterior probability (for each stimuli), for both success and failure
    post_entropy_success = np.zeros(nSlant)
    post_entropy_failure = np.zeros(nSlant) 
    
    for i in range(nSlant):
        
        tmp = np.log(posterior_success[i,:])
        tmp[np.isinf(tmp)] = 0
        post_entropy_success[i] = -sum(posterior_success[i,:]*tmp)
        
        tmp = np.log(posterior_failure[i,:])
        tmp[np.isinf(tmp)] = 0
        post_entropy_failure[i] = -sum(posterior_failure[i,:]*tmp)
        
    # 4) Compute total expescted entropy
    expected_post_entropy = p_success*post_entropy_success + p_failure*post_entropy_failure
    
    # 5) Find next stimulus (minimizing expected entropy)
    slant_next = np.argmin(expected_post_entropy)
    
    return slant_next, p_success

def UpdatePrior(lookup_table, prior, p_success, response, slant_next):
    
    import numpy as np
    
    if response:
        prior_updated = lookup_table[slant_next,:]*prior/p_success[slant_next]
    else:
        prior_updated = (1-lookup_table[slant_next,:])*prior/(1-p_success[slant_next])
        
    return prior_updated

def SaveResults(nVal, prior, param_space):
    
    import numpy as np
    import matplotlib.pyplot as plt
    import csv
    
    nPar = param_space.shape[1]
    prob_param = np.zeros((nVal,nPar))
    nComb = nVal**2

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

    # th_est = param_space[np.argmax(p_theta[:,0]),0]

    th_est, b_est =  sum(param_space[:,0]*prob_param[:,0]), sum(param_space[:,1]*prob_param[:,1])
    # print(f'th estimated = {th_est:.2f}\nb estimated = {b_est:.2f}')
    
    with open('ParamEstim.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([th_est, b_est])
    
    with open('ParamValues.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(param_space)

    with open('ParamProb.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(prob_param)