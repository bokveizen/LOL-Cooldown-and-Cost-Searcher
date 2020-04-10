import json
from fuzzywuzzy import fuzz
from collections import defaultdict
from urllib.request import urlopen
import os
import pyperclip

name_dict = defaultdict(list)
if os.path.exists('namesets.txt'):
    f = open('namesets.txt', encoding='utf8')
else:
    datasets_url = 'https://raw.githubusercontent.com/bokveizen/lol/master/namesets.txt'
    f = urlopen(datasets_url)
for line in f.readlines():
    if not isinstance(line, str):
        line = line.decode('utf8')
    info = line
    while info and info[-1] == ' ' or info[-1] == '\n':
        info = info[:-1]
    if not info:
        continue
    info = info.split(' ')
    for i in range(len(info)):
        name_dict[info[0]].append(info[i])
champ_name_list = list(name_dict.keys())
f.close()

version_url = 'https://ddragon.leagueoflegends.com/api/versions.json'
with urlopen(version_url) as f:
    data = json.load(f)
    latest_version = data[0]


def select(input_champ):
    for champ_name in champ_name_list:
        for name in name_dict[champ_name]:
            if name.upper() == input_champ.upper():
                return champ_name
    fuzz_ratio_max = 0
    tmp = ''
    for champ_name in champ_name_list:
        ratio = max(fuzz.token_sort_ratio(input_champ.upper(), name.upper()) for name in name_dict[champ_name])
        if ratio > fuzz_ratio_max:
            tmp = champ_name
            fuzz_ratio_max = ratio
    return tmp


while True:
    total_res = ''
    champ_selected = []
    input_champs = input('Input the champ names: ')
    while input_champs and input_champs[-1] == ' ':
        input_champs = input_champs[:-1]
    if not input_champs:
        continue
    input_champs = input_champs.split(' ')
    for input_champ in input_champs:
        champ_selected.append(select(input_champ))
    for champ_name in champ_selected:
        if not champ_name:
            continue
        url = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json'.format(latest_version, champ_name)
        with urlopen(url) as f:
            data = json.load(f)
            data = data['data']
            data = data[champ_name]
            data = data['spells']
            skill_info = []
            for skill in data:
                cd = skill['cooldown']
                if not any(cd):
                    if 'Cooldown' in skill['leveltip']['label']:
                        cd_i = skill['leveltip']['label'].index('Cooldown')
                        ef_i = int(skill['leveltip']['effect'][cd_i][skill['leveltip']['effect'][cd_i].index('e') + 1:
                                                                     skill['leveltip']['effect'][cd_i].index('}') - 1])
                        cd = skill['effect'][ef_i]
                    else:
                        cd = [None]
                skill_info.append([cd, skill['cost']])
            res = champ_name
            for info in skill_info:
                res += '\n'
                res += 'CD:' + str(info[0])
                res += 'Cost:' + str(info[1])
            res += '\n'
            print(res)
            total_res += res
    pyperclip.copy(total_res)
