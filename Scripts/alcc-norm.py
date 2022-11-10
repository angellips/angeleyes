# v0.02
# simple script to analyze image generation data and normalize it for use in studies

import os
import re
import itertools
from itertools import chain
from collections import Counter
from difflib import SequenceMatcher
from pprint import pprint
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from pathlib import Path

files = os.listdir('sample_images')
path = Path().absolute()

count = 0
config_set_all = []
single_mods = []
chunk_mods = []
single_most = []
chunk_most = []
chunk_modifiers = []
match_list = []
steps = []
sampler = []
cfg_scale = []
seed = []
model = []
single_modifiers = []
prompts = []

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
    pprint("--------------------------------------------------------------------------")
    seq_gvcount = 0
    for x in g_values:
        seq_gvcount += 1
    for x in range(seq_gvcount):
        pprint(f"{g_values[x][0]} == {g_values[x][1]}")
    pprint("--------------------------------------------------------------------------")
    seq_bvcount = 0
    for x in b_values:
        seq_bvcount += 1
    for x in range(seq_bvcount):
        pprint(f"{b_values[x][0]} == {b_values[x][1]}")

def file_work(mod_most, mod_type, count, prompts):
    if os.path.exists('s_prompts.txt') == False:
        f = open('s_prompts.txt', 'w')
    elif os.path.exists('c_prompts.txt') == False:
        f = open('c_prompts.txt', 'w')
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
        for x in prompts:
            x = ' '.join(x)
            p_txt.write(x.strip() + "\n")
    elif mod_type == "chunk_most":
        p_txt = open("c_prompts.txt","a")
        for x in (map(str, prompts)):                                                   # alters truple elements into strings and then cleans them up for writing to txt
            x = x.replace("'", "")
            x = x.replace(", ", "; ")
            x = re.sub('^[(]', '', x)
            x = re.sub('[)]$', '', x)
            p_txt.write(x.strip() + "\n")
    p_txt.close()

def most_common(single_most, chunk_most):
    for x in Counter(chunk_modifiers).most_common(5):
        chunk_most.append(x[0])
    for x in Counter(single_modifiers).most_common(5):
        single_most.append(x[0])

def misc_clean(chunk_modifiers, chunk_mods, single_mods, match_list):
    chunk_modifiers.append(list(chain.from_iterable(chunk_mods)))           # maybe make a "misc clean up" function for this stragglers
    for x in single_mods:
        matches = re.findall(r'\(.*?\)', x)
        if matches != []:
            match_list.append(matches)

def config_sort(config_set_all):
    
    count = 0
    for x in config_set_all:
        count += 1
    for x in range(count):
        steps.append(config_set_all[x][0])
        sampler.append(config_set_all[x][1].replace(" S", "S"))
        cfg_scale.append(config_set_all[x][2].replace(" C", "C"))
        seed.append(config_set_all[x][3].replace(" S", "S"))
        model.append(config_set_all[x][6].replace(" M", "M"))
    
    config_clean(steps, "steps")
    config_clean(sampler, "sampler")
    config_clean(cfg_scale, "cfg_scale")
    config_clean(seed, "seed")
    config_clean(model, "model")

def config_clean(parameter_list, parameter_type):
    count = 0
    for x in parameter_list:
        count += 1
    if parameter_type == 'steps':
        for x in range(count):
            steps[x] = re.sub('Steps: ', '', parameter_list[x])
    if parameter_type == 'sampler':
        for x in range(count):
            sampler[x] = re.sub('Sampler: ', '', parameter_list[x])
    if parameter_type == 'cfg_scale':
        for x in range(count):
            cfg_scale[x] = re.sub('CFG scale: ', '', parameter_list[x])
    if parameter_type == 'seed':
        for x in range(count):
            seed[x] = re.sub('Seed: ', '', parameter_list[x])
    if parameter_type == 'model':
        for x in range(count):
            model[x] = re.sub('Model: ', '', parameter_list[x])

def file_search(files, config_set_all, single_mods, chunk_mods, single_modifiers):
    for x in files:
        find = re.search('.png', x)
        if find != None:
            img = Image.open(f"{path}/sample_images/{x}")
            img_para = img.text['parameters']
            img_config = re.sub('.*\n', '', img_para)
            img_config = img_config.split(',')        
            img_prompt = re.sub('\n.*', '', img_para)
            img_prompt_chunk = img_prompt.split(';')
            img_prompt = img_prompt.replace(';', '')
            count = 0
            for x in img_prompt_chunk:
                count += 1
            print(count)
            for x in range(count):
                img_prompt_chunk[x] = re.sub('^ ', '', img_prompt_chunk[x])
            print(img_prompt_chunk)
            config_set_all.append(img_config)
            single_mods.extend([img_prompt])
            chunk_mods.extend([img_prompt_chunk])
            for x in (list(chain(single_mods))):
                if re.search('(?:[(])', x) != None:
                    x = x.replace("(", "")
                    x = x.replace(")", "")
                    x = x.split()
                    single_modifiers.append(x)

file_search(files, config_set_all, single_mods, chunk_mods, single_modifiers)
config_sort(config_set_all)
misc_clean(chunk_modifiers, chunk_mods, single_mods, match_list)
single_modifiers = list(chain.from_iterable(single_modifiers))
match_list = (list(chain.from_iterable(match_list)))
chunk_modifiers = (list(chain.from_iterable(chunk_modifiers)))
most_common(single_most, chunk_most)
file_work(single_most, "single_most", count, prompts)
file_work(chunk_most, "chunk_most", count, prompts)
seq_match(single_most)
seq_match(chunk_most)