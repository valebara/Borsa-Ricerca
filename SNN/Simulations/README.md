# Simulations

Files:
- Results (folder) &rarr; Performance analysis and comparison from Test.ipynb, for all conditions (firing rate thresholds or STDP learning rate, see below)
- digit_imprinting.ipynb &rarr; Example graphical response of the last layer (complex cells V1) to input from MNIST databse
- dRF_mean.ipynb &rarr; Script for creating the receptive fields of the classification layer from the firing rate obtained with Training.ipynb. The threshold (excitatory and inhibitory weights) is the average among all firing rates
- dRF_quantiles.ipynb &rarr; As above, but more quantiles are used as the threshold
- saving_mfr.ipynb &rarr; Script to reorder and divide firing rates relative to the digit (MNIST) used as input
- Test.ipynb &rarr; Performance testing script, for the two below
- Training.ipynb &rarr; Network that saves the firing rate for each digit of the training set in the MNIST database
- Training_STDP.ipynb &rarr; Learning with synaptic plasticity (STDP), not using firing rate as synaptic weight after training
- STDP_W.ipynb &rarr; Graphical response of the last layer (complex cells V1) to input from MNIST databse with STDP learning
