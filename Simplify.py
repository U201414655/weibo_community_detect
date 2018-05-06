import os

uid = set()
uid_edge = dict()
uid_profile = dict()
succession_uid = dict()

# delete edges which two nodes of the edge are same and the weight of the edge between two nodes is 0
user_action = open("data/user_action.txt", "r", encoding='UTF-8')
user_sub_action = open("data/user_sub_action.txt", "w", encoding="UTF-8")
for line in user_action:
    temp = line.split("\t", 4)
    weight = int(temp[2]) * 3 + int(temp[3]) * 2 + int(temp[4])
    if (temp[1], temp[0]) in uid_edge:
        uid.add(temp[0])
        uid.add(temp[1])
        user_sub_action.write(temp[1] + "\t" + temp[0] + "\t" + str(weight + uid_edge[(temp[1], temp[0])]) + "\n")
        del uid_edge[(temp[1], temp[0])]
    else:
        uid_edge[(temp[0], temp[1])] = weight
user_action.close()
user_sub_action.close()


# load user profile to the dict
user_profile = open("data/user_profile.txt", "r", encoding='UTF-8')
for line in user_profile:
    temp = line.split("\t", 4)
    if temp[0] in uid:
        uid_profile[temp[0]] = line.rstrip()
user_profile.close()

# load key word and combine profile and key word to the file
user_key_word = open("data/user_key_word.txt", "r", encoding='UTF-8')
user_sub_attribute = open("data/user_sub_attribute.txt", "w", encoding="UTF-8")
for line in user_key_word:
    temp = line.split("\t", 1)
    if temp[0] in uid:
        user_sub_attribute.write(uid_profile[temp[0]] + "\t" + temp[1])
user_key_word.close()
user_sub_attribute.close()

# rebuild graph with succession nodes
index = 0
uid_ = list(uid)
uid_.sort()

for id_ in uid_:
    succession_uid[id_] = index
    index = index + 1

# make node number in the node attribute file starts from 0
attribute = open("data/attribute.txt", "w", encoding="UTF-8")
user_sub_attribute = open("data/user_sub_attribute.txt", "r", encoding='UTF-8')
for line in user_sub_attribute:
    temp = line.split("\t", 1)
    attribute.write(str(succession_uid[temp[0]]) + "\t" + temp[1])
user_sub_attribute.close()
attribute.close()

# make node number in the node linked file start from 0
action = open("data/action.txt", "w", encoding="UTF-8")
user_sub_action = open("data/user_sub_action.txt", "r", encoding='UTF-8')
for line in user_sub_action:
    temp = line.split("\t", 2)
    action.write(str(succession_uid[temp[0]]) + "\t" + str(succession_uid[temp[1]]) + "\t" + temp[2])
user_sub_action.close()
action.close()

os.remove("data/user_sub_action.txt")
os.remove("data/user_sub_attribute.txt")
