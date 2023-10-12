Main Unity:
- PsiMethod.Init.Data()
- for n trials (ex n=30):
  - PsiMethod.GetCurrentTrial()
  - Show stimulus and collect response
  - PsiMethod.UpdatePrior()
- PsiMethod.SaveResults()

Libraries used: numpy, matplotlib, csv

**InitData**(SOA_min, SOA_max, PSS_min, PSS_max, TBW _min, TBW _max, nVal, nSOA):
  return lookup_table, prior, SOA_space, param_space

  Input:
  - nSOA &rarr; Number of SOA values in SOA_space (sampling)
  - nVal &rarr; Number of values of both PSS and TBW (same for sake of commodity)
  - param_space[0] = linspace(PSS_min, PSS_max, nVal) &rarr; PSS candidate values
  - param_space[1] = linspace(PSS_min, PSS _max, nVal) &rarr; TBW candidate values

  Output:
  - lookup_table &rarr; probabiity tables: success probability for each SOA, PSS and TBW (dim[nSOA,nVal^2])
  - prior &rarr; prior for first trial (uniform for all PSS and TBW)
  - SOA_space = linspace(SOA_min, SOA_max, nSOA) &rarr; All possible SOA values
  - param_space -> All param values: PSS,TBW (dim[nVal,2])

**GetCurrentTrial**(lookup_table, prior, nSOA, nVal):
  return SOA_next, p_success

  Input:
  - lookup_table &rarr; from InitData() (doesn't change trial by trial)
  - nSOA &rarr; from InitData() (doesn't change trial by trial)
  - nVal &rarr; from InitData() (doesn't change trial by trial)
  - prior &rarr; from InitData() on first trial, from UpdatePrior() on next

  Output:
  - SOA_next &rarr; 0-based array index of next stimulus (SOA_space[SOA_next])
  - p_success &rarr; proability of correctly seeing stimulus (for each SOA)

**UpdatePrior**(lookup_table, prior, p_success, response, SOA_next):
  return prior_updated

  Input:
  - lookup_table &rarr; from InitData() (doesn't change trial by trial)
  - prior &rarr; from InitData() on first trial, from UpdatePrior() on next
  - p_success &rarr; from GetCurrentTrial()
  - response &rarr; from observer
  - SOA_next &rarr; from GetCurrentTrial()

  Output:
  - prior_updated &rarr; to send to next call of GetCurrentTrial()

**SaveResults**(nVal, prior,param_space):

  Input:
  - nVal &rarr; from InitData() (doesn't change trial by trial)
  - prior &rarr; from UpdatePrior() (after last trial)
  - param_space &rarr; from InitData() (doesn't change trial by trial)

  Output:
  - ParamEstim.csv (PSS and TBS inferred)
  - ParamValues.csv (all values of PSS and TBW)
  - ParamProbs.csv (marginal probabilities of each PSS and TBW
