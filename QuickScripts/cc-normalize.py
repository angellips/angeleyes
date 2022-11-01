# simple skeleton structure of script to analyze prompt texts and create normalized data for use in cc-study

import os
import re
from itertools import chain
from collections import Counter

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
        all_modifiers.insert(0, mods) # nested list

all_modifiers = (list(chain.from_iterable(all_modifiers))) # flatten nested list

most_common = []
for m in range(10):
    most = (Counter(all_modifiers).most_common(10)[m][0])
    most_common.append(most) # creates top 10 list of most used modifiers

#    else: print("No PNG files found!"), need to modify this so it spits that if nothing happens and says completed if pngs != []
