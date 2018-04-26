from Node import Node


class Louvain():
    def __init__(self, edge_path, node_path):
        edge_file = open(edge_path, "r", encoding="UTF-8")
        self.edges = []
        for line in edge_file:
            temp = line.split("\t", 2)
            self.edges.append(((temp[0], temp[1]), int(temp[2])))
        edge_file.close()

        attribute_file = open(node_path, "r", encoding="UTF-8")
        self.nodes = []
        for line in attribute_file:
            t = Node(line)
            self.nodes.append(t)
        attribute_file.close()


L = Louvain("data/action.txt", "data/attribute.txt")
