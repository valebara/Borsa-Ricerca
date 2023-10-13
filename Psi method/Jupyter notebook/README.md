# Jupyter notebook

In this folder there are few examples (step by step, with also graphs) of Psi Method for different physical stimuli and for different psychometric functions (weibull/sigmoid). This method consists of 3 steps:

- Selection of the most informative stimulus
- Presentation to observer and collection of his reponse (e.g. forced choice)
- Parameter bayesian update

Files:
- ex_contrast_weibull.ipynb &rarr; psychometric weibull function (log domain), contrast as visual stimulus
- ex_disparity_sigmoid.ipynb &rarr; sigmoidal psychometric, binocular disparity as stimulus
- ex_sigmoid_threshold.ipynb &rarr; generic stimulus, method applied only to infer threshold
- try_qCSF.ipynb &rarr; refer to Psychopy folder for more in-depth explanation
- try_SOA.ipynb &rarr; examples of applying the method for multisensory stimuli (visuo-auditory) with peculiar psychometrics, in this case gaussian
- try_SOA_v2.ipynb &rarr; see above
- recap_bayesian_update.ipynb &rarr; parameter update with bayesian approach, trial by trial
