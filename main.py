import json
from fuzzywuzzy import fuzz
from collections import defaultdict

name_dict = defaultdict(list)
with open('namesets.txt', encoding='utf8') as f:
    for line in f.readlines():
        info = line[:-1].split(' ')
        for i in range(len(info)):
            name_dict[info[0]].append(info[i])

data_path = 'champion_en'
champ_name_list = list(name_dict.keys())


def select(input_champ):
    for champ_name in champ_name_list:
        for name in name_dict[champ_name]:
            if name.upper() == input_champ.upper():
                return champ_name
    fuzz_ratio_max = 0
    tmp = input_champ
    for champ_name in champ_name_list:
        ratio = max(fuzz.token_sort_ratio(input_champ.upper(), name.upper()) for name in name_dict[champ_name])
        if ratio > fuzz_ratio_max:
            tmp = champ_name
            fuzz_ratio_max = ratio
    return tmp

while True:
    champ_selected = []
    input_champs = input('Input the champ name: ').split(' ')

    for input_champ in input_champs:
        champ_selected.append(select(input_champ))
    for champ_name in champ_selected:
        with open('{}/{}.json'.format(data_path, champ_name), encoding='utf8') as f:
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
