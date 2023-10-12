# Psychtoolobx

Files:

- Letters (directory) &rarr; Various files for creation of filtered letters
- contrast2.mat &rarr; Filtered letter in .mat file, created with scripts inside directory ABOVE
- CSF.m &rarr; truncated log-parabola to model CSF of an observer, with 4 parameters (max frequency, max sensitivity, full width at half maximum and truncation level in log units)
- discretesample.m &rarr; from https://it.mathworks.com/matlabcentral/fileexchange/21912-sampling-from-a-discrete-distribution
- entropy.m &rarr; Example of the entripy of a binary event
- main_test_adaptive.m &rarr; qCSF method
- main_test_standard.m &rarr; classic method for CSF, with nT (=nr*nc*nsf) trial (nr, number of repetitions; nc, number of contrasts; nsf, number of spatial frequencies)
- plot_csf.m &rarr; graphical plot from main_test_adaptive.m and main_test_standard.m
- rescale_letters.m &rarr; downsampling letters to modify their spatial frequency (NOT USED)
- weibull.m &rarr; log-weibull function to model contrast sensitivity for a specific spatial frequency
