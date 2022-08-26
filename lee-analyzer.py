#!/bin/env python3
import re
import json
import os
from tqdm import tqdm
import colour 
from colour.plotting import *

sd_shape = colour.SpectralShape(405, 700, 5)
#illuminant = colour.sd_blackbody(3200, sd_shape)
illuminant = colour.sd_CIE_illuminant_D_series

colors = {}
f=open('colors.json', 'r')
colors = json.loads(f.read())
f.close()

# convert gel spectras into library readable form
for key in colors.keys():
    color = colors[key]
    sd = colour.SpectralDistribution(color['spect_graph'])
    plot_single_sd(sd)
    plot_visible_spectrum()
    plot_single_sd(colour.sd_blackbody(3200, sd_shape))
    sd = sd * colour.sd_blackbody(3200, sd_shape)
    plot_single_sd(sd)
    exit()


