# Psychopy

The qCSF method takes the Psi method, which is characterized by a Bayesian approach for the estimation of psychometric curve parameters, and adapts it for the CSF test. The underlying assumption is that the CSF can be represented by a function (log-parabola), whereby the response to each trial will update the entire function, no longer just the threshold value (and slope) relative to a single spatial frequency. By doing so, the number of trials drops exponentially (even from 2000 to only 50) with very high reliability.

Files:
-	DVS_input.csv -> Rows (2000 trial), columns (spatial frequencies, contrasts, part of the screen where the stimulus will be presented: 0 left; 1 right)
-	functions.py -> Functions for test_CSF_adaptive.py and psi_method_contrast.py: log-weibull psychometric function, log-parabola for qCSF, entropy (information theory) e graphs (qCSF e map of probability)
-	letters.npy (**MISSING HERE**) -> Bandpass filtered letters (different spatial frequencies), from Matlab script in Psychtoolbox directory
-	test_CSF_adaptive.py -> qCSF
-	test_CSF_adaptive_v2.py -> Another version of qCSF (SEE ABOVE)
-	test_CSF_DVS.py -> Visual stimuli for DVS camera for a neurometric test of the CSF
-	psi_method_contrast.py -> Psi-method for the threshold of contrast sensitivity (sf=0) with sigmoidal psychometric function
-	psi_method_weibull_th_b.py -> SEE ABOVE, but with weibull pscyhometric function, for inferring threshold and slope
