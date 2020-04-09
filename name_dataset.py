from collections import defaultdict

res = defaultdict(list)
with open('namesets.txt', encoding='utf8') as f:
    for line in f.readlines():
        info = line[:-1].split(' ')
        for i in range(1, len(info)):
            res[info[0]].append(info[i])
