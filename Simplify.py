uid_cnt = {}
uid_select = set()

user_action = open("data/user_action.txt", "r", encoding='UTF-8')
for line in user_action:
    temp = line.split("\t", 2)
    n1 = int(temp[0])
    n2 = int(temp[1])
    if n1 in uid_cnt:
        uid_cnt[n1] += 1
    else:
        uid_cnt[n1] = 1
    if n2 in uid_cnt:
        uid_cnt[n2] += 1
    else:
        uid_cnt[n2] = 1
user_action.close()

for (x, y) in uid_cnt.items():
    if y > 200:
        uid_select.add(x)
#print(len(uid_select))

uid_node = set()
edge = {}

user_action = open("data/user_action.txt", "r", encoding='UTF-8')
for line in user_action:
    temp = line.split("\t", 4)
    weight = int(temp[2]) * 3 + int(temp[3]) * 2 + int(temp[4])
    n1 = int(temp[0])
    n2 = int(temp[1])
    if n1 > n2:
        n1, n2 = n2, n1
    if n1 in uid_select and n2 in uid_select:
        uid_node.add(n1)
        uid_node.add(n2)
        if (n1, n2) in edge:
            edge[(n1, n2)] += weight
        else:
            edge[(n1, n2)] = weight
user_action.close()

print(len(uid_node), len(edge))

uid_list = list(uid_node)
uid_list.sort()

index = 0
uid_order = {}
for n in uid_list:
    uid_order[n] = index
    index += 1

action = open("data/action.txt", "w", encoding='UTF-8')
for (e, w) in edge.items():
    action.write(str(uid_order[e[0]]) + '\t' + str(uid_order[e[1]]) + '\t' + str(w) + '\n')
action.close()

uid_profile = {}
user_profile = open("data/user_profile.txt", "r", encoding='UTF-8')
for line in user_profile:
    temp = line.split("\t", 1)
    n = int(temp[0])
    if n in uid_node:
        uid_profile[n] = temp[1].rstrip()
user_profile.close()

attribute = open("data/attribute.txt", "w", encoding="UTF-8")
user_keyword = open("data/user_key_word.txt", "r", encoding='UTF-8')
for line in user_keyword:
    temp = line.split("\t", 1)
    n = int(temp[0])
    if n in uid_node:
        attribute.write(str(uid_order[n]) + "\t" + uid_profile[n] + "\t" + temp[1])
user_keyword.close()
attribute.close()