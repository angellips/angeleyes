# simple skeleton structure of script to analyze prompt texts and create normalized data for use in cc-study

import os
import re

files = os.listdir('sample_images')

all_modifiers = []
all_seeds = []

for x in files:
    find = re.search('.*\d[-]\d+[-]\w+', x)
    if find != None:
        mods = find.string.replace('.png', '')
        mods = mods.replace(';', '')
        mods = mods.split('-')
        seed_clean = mods[:-1]
        seed_clean.pop(0)
        all_seeds.append(seed_clean)
        mods.pop(0)
        mods.pop(0)
        mods = mods[0].split()
        all_modifiers.insert(0, mods)

#    else: print("No PNG files found!"), need to modify this so it spits that if nothing happens and says completed if pngs != []
