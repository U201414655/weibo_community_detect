import csv

action = open("data/action.txt", "r", encoding='UTF-8')
csv_dege = open("data/edge.csv", 'w')
csv_edge_write = csv.writer(csv_dege)
csv_edge_write.writerow(["Source", "Target", "Weight","Type"])
for line in action:
    # line.rstrip()
    temp = line.split("\t", 2)
    t = [int(temp[0]), int(temp[1]), int(temp[2]),"undirected"]
    csv_edge_write.writerow(t)
csv_dege.close()

node = {}
index = 0
attribute = open("data/result.txt", "r", encoding="UTF-8")
for line in attribute:
    index += 1
    line = line.lstrip("[")
    line = line.rstrip("]\n")
    line = line.split(", ")
    for x in line:
        node[int(x)] = index
attribute.close()

csv_node = open("data/node.csv", 'w')
csv_node_write = csv.writer(csv_node)
csv_node_write.writerow(["Id", "Lable"])
for (x, y) in node.items():
    t = [x, y]
    csv_node_write.writerow(t)
csv_node.close()
