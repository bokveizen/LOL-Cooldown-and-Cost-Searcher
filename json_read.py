import json
import os
from fuzzywuzzy import fuzz

data_path = 'champion_en'
champ_name_list = [i[:-5] for i in os.listdir(data_path)]
champ_selected = []
input_champs = input('Input the champ name: ').split(' ')
for input_champ in input_champs:
    if input_champ not in champ_name_list:
        for champ in champ_name_list:
            if champ.upper() == input_champ.upper():
                input_champ = champ
        fuzz_ratio_max = 0
        tmp = input_champ
        for champ in champ_name_list:
            if fuzz.token_sort_ratio(input_champ.upper(), champ.upper()) > fuzz_ratio_max:
                tmp = champ
                fuzz_ratio_max = fuzz.token_sort_ratio(input_champ, champ)
        input_champ = tmp
    champ_selected.append(input_champ)
for champ_name in champ_selected:
    with open('{}/{}.json'.format(data_path, champ_name)) as f:
        data = json.load(f)
        # print(data)
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
        res = champ_name.ljust(20)
        for info in skill_info:
            res += str(info[0]).ljust(35)
        print(res)

