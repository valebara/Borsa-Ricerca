# Main Unity:
- PsiMethod.Init.Data()
- for n trials (ex n=30):
  - PsiMethod.GetCurrentTrial()
  - Show stimulus and collect response
  - PsiMethod.UpdatePrior()
- PsiMethod.SaveResults()

th &rarr; threshold \
b &rarr; slope

Libraries used: numpy, matplotlib, csv

# InitData()
  **InitData**(slant_min, slant_max, th_min, th_max, b _min, b_max, nVal, nSlant):\
  return lookup_table, prior, slant_space, param_space

  Input:
  - nSlant &rarr; Number of Slant values in slant_space (sampling)
  - nVal &rarr; Number of values of both th and b (same for sake of commodity)
  - param_space[0] = linspace(th_min, th_max, nVal) &rarr; th candidate values
  - param_space[1] = linspace(b_min, b_max, nVal) &rarr; b candidate values

  Output:
  - lookup_table &rarr; probabiity tables: success probability for each slant, th and b (dim[nSlant,nVal^2])
  - prior &rarr; prior for first trial (uniform for all th and b)
  - slant_space = linspace(slant_min, slant_max, nSlant) &rarr; All possible slant values
  - param_space -> All param values: th,b (dim[nVal,2])

# GetCurrentTrial()
  **GetCurrentTrial**(lookup_table, prior, nSlant, nVal):\
  return slant_next, p_success

  Input:
  - lookup_table &rarr; from InitData() (doesn't change trial by trial)
  - nSlant &rarr; from InitData() (doesn't change trial by trial)
  - nVal &rarr; from InitData() (doesn't change trial by trial)
  - prior &rarr; from InitData() on first trial, from UpdatePrior() on next

  Output:
  - slant_next &rarr; 0-based array index of next stimulus (slant_space[slant_next])
  - p_success &rarr; proability of correctly seeing stimulus (for each slant)

# UpdatePrior()
  **UpdatePrior**(lookup_table, prior, p_success, response, slant_next):\
  return prior_updated

  Input:
  - lookup_table &rarr; from InitData() (doesn't change trial by trial)
  - prior &rarr; from InitData() on first trial, from UpdatePrior() on next
  - p_success &rarr; from GetCurrentTrial()
  - response &rarr; from observer
  - SOA_next &rarr; from GetCurrentTrial()

  Output:
  - prior_updated &rarr; to send to next call of GetCurrentTrial()

# SaveResults()
  **SaveResults**(nVal, prior,param_space):

  Input:
  - nVal &rarr; from InitData() (doesn't change trial by trial)
  - prior &rarr; from UpdatePrior() (after last trial)
  - param_space &rarr; from InitData() (doesn't change trial by trial)

  Output:
  - ParamEstim.csv (th and b inferred)
  - ParamValues.csv (all values of th and b)
  - ParamProbs.csv (marginal probabilities of each th and b)
