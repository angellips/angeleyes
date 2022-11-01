# simple skeleton structure of script to analyze prompt texts and create normalized data for use in cc-study

import os
import re

files = os.listdir('sample_images')

pngs = []
seeds = []

for x in files:
    test = re.search('.*\d[-]\d+[-]\w+', x)
    if test != None:
        z = test.string.replace('.png', '')
        z = z.replace(';', '')
        z = z.split('-')
        s_clean = z[:-1]
        s_clean.pop(0)
        seeds.append(s_clean)
        z.pop(0)
        z.pop(0)
        z = z[0].split()
        pngs.insert(0, z)

#    else: print("No PNG files found!"), need to modify this so it spits that if nothing happens and says completed if pngs != []
