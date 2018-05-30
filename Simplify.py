uid_cnt = {}
uid_select = set()
L1 = 250
L2 = 150

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
    if y > L1:
        uid_select.add(x)

uid_node = set()
edge_ = {}

user_action = open("data/user_action.txt", "r", encoding='UTF-8')
for line in user_action:
    temp = line.split("\t", 4)
    weight = int(temp[2]) * 3 + int(temp[3]) * 2 + int(temp[4])
    n1 = int(temp[0])
    n2 = int(temp[1])
    if n1 > n2:
        n1, n2 = n2, n1
    if n1 in uid_select and n2 in uid_select:
        if (n1, n2) in edge_:
            edge_[(n1, n2)] += weight
        else:
            edge_[(n1, n2)] = weight
user_action.close()

num_of_node = {}

for (e, w) in edge_.items():
    if e[0] in num_of_node:
        num_of_node[e[0]] += 1
    else:
        num_of_node[e[0]] = 1
    if e[1] in num_of_node:
        num_of_node[e[1]] += 1
    else:
        num_of_node[e[1]] = 1

edge = {}
for (e, w) in edge_.items():
    if num_of_node[e[0]] > L2 and num_of_node[e[1]] > L2:
        uid_node.add(e[0])
        uid_node.add(e[1])
        if e in edge:
            edge[e] += w
        else:
            edge[e] = w
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

user = {}
user_keyword = open("data/user_key_word.txt", "r", encoding='UTF-8')
for line in user_keyword:
    temp = line.split("\t", 1)
    n = int(temp[0])
    if n in uid_node:
        user[uid_order[n]] = str(uid_order[n]) + "\t" + uid_profile[n] + "\t" + temp[1]
user_keyword.close()

attribute = open("data/attribute.txt", "w", encoding="UTF-8")
user_keys = list(user.keys())
user_keys.sort()
for k in user_keys:
    attribute.write(user[k])
attribute.close()
