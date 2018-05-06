from Node import Node


class Louvain():
    def __init__(self, edge_path, node_path):
        self.edges = self.load_edges_file(edge_path)
        self.nodes = self.load_nodes_file(node_path)
        self.w = 0
        self.L_i = [0 for n in self.nodes]
        self.L_i_in = [0 for n in self.nodes]
        self.edges_of_node = {}

        for e in self.edges:
            self.w += e[1]
            self.L_i[e[0][0]] += e[1]
            self.L_i[e[0][1]] += e[1]
            if e[0][0] not in self.edges_of_node:
                self.edges_of_node[e[0][0]] = [e]
            else:
                self.edges_of_node[e[0][0]].append(e)
            if e[0][1] not in self.edges_of_node:
                self.edges_of_node[e[0][1]] = [e]
            elif e[0][0] != e[0][1]:
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
        index = 0
        for line in attribute_file:
            temp = line.split("\t", 1)
            nodes.append(Node(line, index))
            index += 1
        attribute_file.close()
        return nodes

    def cluser(self):
        network = (self.nodes, self.edges)
        best_q = -1
        while True:
            self.Combine_Nodes(network)
            q = self.compute_modularity()
            partition = [n for n in self.nodes if n.group]

            network = self.relabel_graph(network)
            if q == best_q:
                return
            best_q = q

    def init_partition(self, network):
        # s_in: sum of the weights of the links inside community
        # s_tot:    sum of the weights of the links incident to nodes in community
        self.s_in = [0 for node in network[0]]
        self.s_tot = [self.L_i[node.no] for node in network[0]]
        for e in network[1]:
            if e[0][0] == e[0][1]:
                self.s_in[e[0][0]] += e[1]
                self.s_in[e[0][1]] += e[1]

    def get_neighbors(self, node):
        for e in self.edges_of_node[node]:
            if e[0][0] == e[0][1]:  # a node is not neighbor with itself
                continue
            if e[0][0] == node:
                yield e[0][1]
            if e[0][1] == node:
                yield e[0][0]

    def Combine_Nodes(self, network):
        best_partition = self.init_partition(network)
        while True:
            improved = False
            for node in network[0]:

                best_gain = 0
                best_shared_links = 0
                best_community = node.no

                for e in self.edges_of_node[node.no]:
                    if e[0][0] == e[0][1]:
                        continue
                    if e[0][0] == node.no and e[0][1] in self.nodes[node.no].group or \
                            e[0][1] == node.no and e[0][0] in self.nodes[node.no].group:
                        best_shared_links += e[1]
                self.s_in[node.no] -= (best_shared_links + self.L_i_in[node.no])
                self.s_tot[node.no] -= self.L_i[node.no]

                visited_neighbors = set()
                for neighbor in self.get_neighbors(node.no):
                    if neighbor in visited_neighbors:
                        continue
                    visited_neighbors.add(neighbor)
                    shared_links = 0
                    for e in self.edges_of_node[node.no]:
                        if e[0][0] == e[0][1]:
                            continue
                        if e[0][0] == node.no and e[0][1] in self.nodes[node.no].group or \
                                e[0][1] == node.no and e[0][0] in self.nodes[node.no].group:
                            shared_links += e[1]
                    # compute modularity gain obtained by moving _node to the community of _neighbor
                    gain = self.compute_modularity_gain(node, neighbor, shared_links)
                    # to-do
                    if gain > best_gain:
                        best_community = neighbor
                        best_gain = gain
                        best_shared_links = shared_links

                self.s_in[best_community] += (best_shared_links + self.L_i_in[node.no])
                self.s_tot[best_community] += self.L_i[node.no]
                if best_community != node.no:
                    self.nodes[best_community].group.extend(self.nodes[node.no].group)
                    self.nodes[node.no].group.clear()
                    improved = True
            if not improved:
                return

    def compute_modularity(self):
        q = 0
        for i in range(len(self.nodes)):
            q += self.s_in[i] / (self.w * 2) - (self.s_tot[i] / (self.w * 2)) ** 2
        return q

    def compute_modularity_gain(self, node, c, L_i_in):
        return L_i_in - self.s_tot[c] * self.L_i[node.no] / self.w

    def relabel_graph(self, network):
        return network
