# Receptive Fields

Files:
- LGN.ipynb &rarr; Second layer (after retina), receptive field characterization center on / surround off, various sizes. Inspired by the elaborate layers of the lateral geniculate nucleus (LGN)
- LGN_scales.ipynb &rarr; On-off response to varying scale (pyramidal approach)
- LGN_tuning_curves.ipynb &rarr; Curve tuning (with and without lateral inhibition) as the stimulus offset changes with respect to the center of the receptive field (off-center)
- LGN_param.ipynb &rarr; LGN response characterization as some key parameters vary (synaptic time constants, synaptic efficacy, presence of lateral inhibition)
- V1simple_orientations.ipynb &rarr; Sensitivity to orientations as LGN size (scale) changes, 3x1 only
- V1simple_param.ipynb &rarr; Parameters: synaptic efficacy, lateral inhibition, constant time excitatory synapses
- V1simple_RF_3x1.ipynb &rarr; Creating receptive fields as logical variables (brian2 connections), only 4 orientations
- V1simple_RF_5x1.ipynb &rarr; As above, but 5x1 at 8 orientations
- V1simple_scales.ipynb &rarr; Same as V1simple_orientations.ipynb but with also sensitivity to 8 orientations (5x1)
- V1simple_tuning_curves.ipynb &rarr; Varying offset of preferred direction, perpendicular direction and orientation phase difference
- V1complex_3scales.ipynb &rarr; Introduction of complex cells (stimulus position invariance, sensitivity only to orientation). Two LGN and simple V1 cell cases: single pixels and 2x2 mean (for MNIST, 28x28 and 14x14). Two cases complex cells of spatial averaging: 3x3 and 5x5. (SEE BELOW)
- V1complex_9hist.ipynb &rarr; As above and below, a multiscale analysis with histogram (frequency distribution) of firing rate of all V1 complex cells
- V1complex_9scales.ipynb &rarr; Same as V1complex_3scales.ipynb, but with 3 LGN (1x1, 2x2, 4x4) with each 3 different types of V1 complex: 3x3, 5x5, 7x7 (spatial average)
- V1complex_connection_all_ori.ipynb &rarr; Receptive field V1 complex cells, with connections see V1complex_RF_inter_orientations.ipynb
- V1complex_connection_all_ori_3scales.ipynb &rarr; As above, but with 3 different scales (same V1complex_3scales.ipynb)
- V1complex_RF_inter_orientations &rarr; Characterization receptive field, not only as spatial average from 3x3 or 5x5 simple cells to one complex cell, for each orientation separately, but also between different orientations. The weight is proportional to the cosine of the angle difference: Δθ=0°, w=1; Δθ=45°, w=0; Δθ=90°, w=-1.
