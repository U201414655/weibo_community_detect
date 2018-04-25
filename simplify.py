uid = set()
uid_edge = set()
uid_profile = dict()
succession_uid = dict()

user_sub_action = open("user_sub_action.txt", "w", encoding="UTF-8")
user_sub_attribute = open("user_sub_attribute.txt", "w", encoding="UTF-8")

# delete edges which two nodes of the edge are same and the weight of the edge between two nodes is 0
user_action = open("user_action.txt", "r", encoding='UTF-8')
for line in user_action:
    temp = line.split("\t", 4)
    weight = int(temp[2]) + int(temp[3]) + int(temp[4])
    if temp[0] != temp[1] and weight != 0:
        uid_edge.add((temp[0], temp[1]))
user_action.close()

# delete one way edge and write two nodes and the weight if the edge to file
user_action = open("user_action.txt", "r", encoding='UTF-8')
for line in user_action:
    line.rstrip()
    temp = line.split("\t", 4)
    if (temp[1], temp[0]) in uid_edge:
        uid.add(temp[0])
        uid.add(temp[1])
        weight = int(temp[2]) * 3 + int(temp[3]) * 2 + int(temp[4])
        user_sub_action.write(temp[0] + "\t" + temp[1] + "\t" + str(weight) + "\n")
user_action.close()

# load user profile to the dict
user_profile = open("user_profile.txt", "r", encoding='UTF-8')
for line in user_profile:
    temp = line.split("\t", 4)
    if temp[0] in uid:
        uid_profile[temp[0]] = line.rstrip()
user_profile.close()

# load key word and combine profile and key word to the file
user_key_word = open("user_key_word.txt", "r", encoding='UTF-8')
for line in user_key_word:
    temp = line.split("\t", 1)
    if temp[0] in uid:
        user_sub_attribute.write(uid_profile[temp[0]] + "\t" + temp[1])
user_key_word.close()

user_sub_action.close()
user_sub_attribute.close()

index = 0
uid_ = list(uid)
uid_.sort()

# rebuild graph with succession nodes
for id_ in uid_:
    succession_uid[id_] = index
    index = index + 1

attribute = open("attribute.txt", "w", encoding="UTF-8")
user_sub_attribute = open("user_sub_attribute.txt", "r", encoding='UTF-8')
for line in user_sub_attribute:
    temp = line.split("\t", 1)
    attribute.write(str(succession_uid[temp[0]]) + "\t" + temp[1])
user_sub_attribute.close()
attribute.close()

action_ = open("action_.txt", "w", encoding="UTF-8")
user_sub_action = open("user_sub_action_.txt", "r", encoding='UTF-8')
for line in user_sub_action:
    temp = line.split("\t", 2)
    action_.write(str(succession_uid[temp[0]]) + "\t" + str(succession_uid[temp[1]]) + "\t" + temp[2])
user_sub_action.close()
action_.close()

edge = dict()
action = open("action.txt", "w", encoding="UTF-8")
action_ = open("action_.txt", "r", encoding='UTF-8')
for line in action_:
    line.rstrip()
    temp = line.split("\t", 2)
    if (temp[1], temp[0]) in edge:
        weight = int(temp[2]) + edge[(temp[1], temp[0])]
        action.write(temp[0] + "\t" + temp[1] + "\t" + str(weight) + "\n")
    else:
        edge[(temp[0], temp[1])] = int(temp[2])
action_.close()
action.close()
