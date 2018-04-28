from Node import Node


class Louvain():
    def __init__(self, edge_path, node_path):
        self.edges = self.load_edges_file(edge_path)
        self.nodes = self.load_nodes_file(node_path)
        self.all_sum_weight = 0
        self.node_sum_weight = [0 for n in self.nodes]
        self.node_weight = [0 for n in self.nodes]
        self.edges_of_node = {}
        self.communities = [n for n in self.nodes]
        self.final_communities = []
        for e in self.edges:
            self.all_sum_weight += e[1]
            self.node_sum_weight[e[0][0]] += e[1]
            self.node_sum_weight[e[0][1]] += e[1]
            if e[0][0] not in self.edges_of_node:
                self.edges_of_node[e[0][0]] = [e]
            else:
                self.edges_of_node[e[0][0]].append(e)
            if e[0][1] not in self.edges_of_node:
                self.edges_of_node[e[0][1]] = [e]
            else:
                self.edges_of_node[e[0][1]].append(e)

    def load_edges_file(self, edge_path):
        edge_file = open(edge_path, "r", encoding="UTF-8")
        edges = []
        for line in edge_file:
            temp = line.split("\t", 2)
            edges.append(((int(temp[0]), int(temp[1])), int(temp[2])))
        edge_file.close()
        return edges

    def load_nodes_file(self, node_path):
        attribute_file = open(node_path, "r", encoding="UTF-8")
        nodes = []
        for line in attribute_file:
            t = Node(line)
            nodes.append(t)
        attribute_file.close()
        return nodes

    def cluser(self):
        pass

    def init_partition(self):
        partition = [[node] for n in self.nodes]
        self.s_in = [0 for n in self.nodes]
        self_s_tot = [self.node_sum_weight[n] for n in self.nodes]
        return partition

    def fisrt_step(self):
        best_partition = self.init_partition()
        while True:
            improvement = 0
            for n in self.nodes:
                node_community = self.communities[n]
                best_community = node_community
                best_gain = 0


L = Louvain("data/action.txt", "data/attribute.txt")
