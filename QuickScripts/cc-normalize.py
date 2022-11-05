# simple script to analyze prompt texts from filenames and create normalized data for use in cc-study

import os
import re
import itertools
from itertools import chain
from collections import Counter
from difflib import SequenceMatcher

files = os.listdir('sample_images')

all_seeds = []
single_modifiers = []
single_most = []
chunk_modifiers = []
chunk_most = []


def seq_match(mod_most):

    seq_pcount = 0

    seq_txt = []
    seq_float = []
    seq_pairs = []
    seq_nest = []

    for x in itertools.combinations(mod_most, 2):                                       # determines all combinations of 2 values within single_most and chunk_most
        seq_pairs.append(x)

    for x in seq_pairs:
        seq_pcount += 1

    for x, y in seq_pairs:
        seq_txt.append(x)
        seq_float.append(y)

    seq_ncount = 0

    for x in range(seq_pcount):
        # print(seq_txt[x], seq_float[x])
        y = [seq_txt[x], seq_float[x], (SequenceMatcher(None, seq_txt[x], seq_float[x]).ratio())]
        seq_nest.append(y)
        seq_ncount += 1

    g_values = []
    b_values = []

    for x in range(seq_ncount):                                                         # sorts all txt and float data in seq_nest by similarity into 'good' and 'bad' values
        if seq_nest[x][2] <= 0.1:
            b_values.append([seq_nest[x][0] + " " + seq_nest[x][1], [seq_nest[x][2]]])
        else: 
            g_values.append([seq_nest[x][0] + " " + seq_nest[x][1], [seq_nest[x][2]]])

    g_values = sorted(g_values, key = lambda x: x[1], reverse = True)                   # resorts value list into order of highest to lowest
    b_values = sorted(b_values, key = lambda x: x[1], reverse = True)

    print("-------------------------------------")

    seq_gvcount = 0
    for x in g_values:
        seq_gvcount += 1

    for x in range(seq_gvcount):
        print(f"{g_values[x][0]} == {g_values[x][1]}")

    print("-------------------------------------")

    seq_bvcount = 0
    for x in b_values:
        seq_bvcount += 1

    for x in range(seq_bvcount):
        print(f"{b_values[x][0]} == {b_values[x][1]}")

    #print(g_values[0][0])
    #print("BREAK")
    #print(b_values)

def file_work(mod_most, mod_type):

    if os.path.exists('s_prompts.txt') == False:
        f = open('s_prompts.txt', 'w')
    elif os.path.exists('c_prompts.txt') == False:
        f = open('c_prompts.txt', 'w')

    if mod_type == "single_most":
        global dp
        dp = ""
        for x in mod_most:
            dp = dp + f"{x}" + " "

    global count
    count = 0
    prompts = []
    for x in itertools.permutations(mod_most):
        count += 1
        prompts.append(x)

    if mod_type == "single_most":
        del_lines = open('s_prompts.txt', 'r+')                                     # clear all lines from s_prompts.txt (if any) and then open for appending prompt variations
    elif mod_type == "chunk_most":
        del_lines = open('c_prompts.txt', 'r+')                                     # clear all lines from s_prompts.txt (if any) and then open for appending prompt variations

    del_lines.truncate(0)
    del_lines.close()

    if mod_type == "single_most":
        p_txt = open("s_prompts.txt","a")
    elif mod_type == "chunk_most":
        p_txt = open("c_prompts.txt","a")

    for x in (map(str, prompts)):                                                   # alters truple elements into strings and then cleans them up for writing to txt
        x = x[1:]
        x = x[:-1]
        x = x.replace("'", "")
        if mod_type == "single_most":
            x = x.replace(",", "")
        elif mod_type == "chunk_most":
            x = x.replace(", ", ";")
        p_txt.write(x.strip() + "\n")

    p_txt.close()

def file_search(files, single_modifiers, chunk_modifiers):
    for x in files:
        find = re.search('.*\d[-]\d+[-]\w+', x)                                         # finds match in format of "00001-2259320428-green", inherently excludes all other files.
        if find != None:
            find = re.sub('(?<![a-z])-(?![a-z])', '_', x)
            find = re.sub('(?<![a-z])-(?!\d)', '_', x)
            mods = find.replace('.png', '')
            c_mods = mods.split('_')
            c_mods = c_mods[1:]
            chunk_modifiers.append(c_mods[0].split(";"))                                # creates chunk-modifiers, e.g., "hello world; blue sky; cool dog", returns each ; separated chunk of text
            s_mods = mods.replace(';', '')
            s_mods = s_mods.split('_')
            s_mods = s_mods[1:]
            single_modifiers.append(s_mods[0].split())                                  # creates single modifiers, e.g., "hello", "world", "blue", etc..
            mods = mods.split('-')
            seed_clean = mods[1:]
            seed_clean = seed_clean[0].split('_')
            seed_clean = seed_clean[:-1]
            all_seeds.append(seed_clean)                                                # creates nested list of all seeds

    chunk_modifiers = (list(chain.from_iterable(chunk_modifiers)))                      # flatten nested list
    single_modifiers = (list(chain.from_iterable(single_modifiers)))                    # flatten nested list

    for m in range(5):
        s_most = (Counter(single_modifiers).most_common(5)[m][0])
        single_most.append(s_most)                                                      # creates top 5 list of most used single modifiers
        
        if re.search('^\w', (Counter(chunk_modifiers).most_common(5)[m][0])) != None:   # fixes lack of space after c_mods = mods.split('-')
            c_most = (Counter(chunk_modifiers).most_common(5)[m][0])
            c_most = " " + c_most
            chunk_most.append(c_most)
        else:
            c_most = (Counter(chunk_modifiers).most_common(5)[m][0])
            chunk_most.append(c_most)

file_search(files, single_modifiers, chunk_modifiers)
file_work(single_most, "single_most")
file_work(chunk_most, "chunk_most")

while not(count % 8) == False:                                                      # rounds up prompt count until batch_size will actually allow all images to be generated; # of img generated stays the same
    count += 1

batch_size = int(count / 8)

print(f"\nThe following will generate {count} prompt permutations in Dynamic Prompting:")
print("\n" + dp)
print(f"\nThe following settings are needed to produce all permutations using the combinatorial option:\n\nBatch Size: {batch_size} \nBatch Count: 8")
print("\nText files containing all prompt permutations for top used single and chunk modifiers generated!\nUse with Prompts from File extension!\n")

seq_match(single_most)
seq_match(chunk_most)