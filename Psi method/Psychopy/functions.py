def weibull(param,logCon,logSF):
    
    #   https://www.degruyter.com/document/doi/10.1051/978-2-7598-2518-9.c021/pdf
    
    import numpy as np
    
    logTH = csf(param,logSF)
    w = 0.1 + 0.9*(1-np.exp(-10**(logCon+logTH)))
    
    return min(0.96,w)

def csf(param,logSF):
    
    import numpy as np
    
    logFmax,logSmax,beta,delta = param[0],param[1],param[2],param[3]
    
    trunc = logSmax-delta
    k = np.log10(2)
    logTH = logSmax - 4*k*(((logSF-logFmax)/(k+beta))**2)
    
    if logSF<logFmax:
        logTH = max(logTH,trunc)

    logTH = max(logTH,0) # >0
    
    return logTH

def entropy(p):
    
    import numpy as np
    
    H = -p*np.log(p) - (1-p)*np.log(1-p)
    
    return H
    
def plot_qCSF(param,p,nVal):
    
    # Add title and legends
    
    from matplotlib import pyplot as plt
    import numpy as np
    
    N = 1000
    nVec = nVal**4
    logSF = np.linspace(-1,2,N)
    logCon = np.linspace(-3,0,N)
    
    # qCSF
    fig,ax = plt.subplots(1,2)
    logSens = np.ones(N)
    for i in range(N):
        logSens[i] = csf(param,logSF[i])
    ax[0].plot(logSF,logSens)
    ax[0].set_xlim((-1,2))
    ax[0].set_ylim((0,3))
    ax[0].set_xticks([-1,0,1,2])
    ax[0].set_xticklabels(['0.1','1','10','100'])
    ax[0].set_yticks([0,1,2,3])
    ax[0].set_yticklabels(['1','10','100','1000'])
    
    # Probability  density map
    prob_density = np.ones([N,N])
    for c in range(N):
        for f in range(N):
            prob_density[c,f] = weibull(param,logCon[c],logSF[f])
    ax[1].imshow(prob_density, cmap='jet')
    ax[1].set_xticks([0,333,666,999])
    ax[1].set_xticklabels(['0.1','1','10','100'])
    ax[1].set_yticks([0,333,666,999])
    ax[1].set_yticklabels(['1000','100','10','1'])
    plt.show()
    
    # Marginal probabilities (Posterior)
    prob_param = np.zeros((nVal,4))
    for i in range(nVal):
        for par in range(4):
            ind = np.arange(nVec/nVal**(3-par))
            tmp = np.repeat(ind%nVal,nVal**(3-par))
            x = np.argwhere(tmp==i)
            prob_param[i,par] = sum(p[x])
    fig,axs = plt.subplots(2,2)
    axs[0,0].plot(prob_param[:,0])
    axs[0,1].plot(prob_param[:,1])
    axs[1,0].plot(prob_param[:,2])
    axs[1,1].plot(prob_param[:,3])
    #plt.show()