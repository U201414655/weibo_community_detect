user_sub_action = open("user_sub_action.txt", "w", encoding="UTF-8")
user_sub_profile_keyword = open("user_sub_profile_keyword.txt", "w", encoding="UTF-8")

uid = set()
uid_edge = set()
uid_profile = dict()


def del_self_edge(s):
    temp = s.split("\t", 4)
    if temp[0] != temp[1]:
        global uid_edge
        uid_edge.add((temp[0], temp[1]))


def del_one_way_edge(s):
    temp = s.split("\t", 4)
    global uid, uid_edge
    if (temp[1], temp[0]) in uid_edge:
        uid.add(temp[0])
        uid.add(temp[1])
        weight = int(temp[2]) * 3 + int(temp[3]) * 2 + int(temp[4])
        user_sub_action.write(temp[0] + "\t" + temp[1] + "\t" + str(weight) + "\n")


def del_unused_profile(s):
    global uid
    temp = s.split("\t", 4)
    if temp[0] in uid:
        uid_profile[temp[0]] = s.rstrip()


def del_unused_keyword(s):
    global uid
    temp = s.split("\t", 1)
    if temp[0] in uid:
        user_sub_profile_keyword.write(uid_profile[temp[0]] + "\t" + temp[1])


for line in open("user_action.txt", encoding='UTF-8'):
    del_self_edge(line)

for line in open("user_action.txt", encoding='UTF-8'):
    del_one_way_edge(line)

for line in open("user_profile.txt", encoding='UTF-8'):
    del_unused_profile(line)

for line in open("user_key_word.txt", encoding='UTF-8'):
    del_unused_keyword(line)

del uid, uid_edge, uid_profile
