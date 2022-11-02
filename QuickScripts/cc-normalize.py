# simple skeleton structure of script to analyze prompt texts and create normalized data for use in cc-study

import os
import re
import itertools
from itertools import chain
from collections import Counter

files = os.listdir('sample_images')

all_modifiers = []
all_seeds = []
most_common = []

for x in files:
    find = re.search('.*\d[-]\d+[-]\w+', x) # finds match in format of "00001-2259320428-green tree; bright sun; blue water.png" 
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

for m in range(5):
    most = (Counter(all_modifiers).most_common(5)[m][0])
    most_common.append(most) # creates top 5 list of most used modifiers

dp = "{"

for x in most_common:
    dp = dp + f"{x}" + "|"

dp = dp[:-1] + "}"

count = 0
for x in itertools.permutations(most_common):
    count += 1

while not(count % 8) == False:
    count += 1

batch_size = int(count / 8) # batch size * batch count in Dynamic Prompting sets the *max* number of images to produce; count of img would remain same and is produced via combinatorial option.

print(f"\nThe following would generate {count} different variations in Dynamic Prompting:")
print("\n" + dp)
print(f"\nBatch Size: {batch_size} \nBatch Count: 8\n\nAre the settings needed to run all permutations.")