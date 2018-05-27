from Lnode import Lnode


class Louvain():
    def __init__(self, edge_path, node_path):
        self.nodes = self.load_nodes_file(node_path)
        self.edges = self.load_edges_file(edge_path)
        self.w = 0
        self.L_i = [0 for n in self.nodes]
        self.L_i_in = [0 for n in self.nodes]
        self.edges_of_node = {}

        for (e, w) in self.edges.items():
            self.w += w
            self.L_i[e[0]] += w
            self.L_i[e[1]] += w
            if e[0] not in self.edges_of_node:
                self.edges_of_node[e[0]] = [e]
            else:
                self.edges_of_node[e[0]].append(e)
            if e[1] not in self.edges_of_node:
                self.edges_of_node[e[1]] = [e]
            elif e[0] != e[1]:
                self.edges_of_node[e[1]].append(e)

        # s_in: sum of the weights of the links inside community
        # s_tot:sum of the weights of the links incident to nodes in community
        self.s_in = [0 for node in self.nodes]
        self.s_tot = [self.L_i[node.id] for node in self.nodes]
        self.communities = [n.id for n in self.nodes]
        for (e, w) in self.edges.items():
            if e[0] == e[1]:
                self.s_in[e[0]] += 2 * w

    def load_edges_file(self, edge_path):
        edge_file = open(edge_path, "r", encoding="UTF-8")
        edges = {}
        for line in edge_file:
            e = line.split("\t", 2)
            n1 = int(e[0])
            n2 = int(e[1])
            if n1 > n2:
                n1, n2 = n2, n1
            edges[(n1, n2)] = int(e[2])
        edge_file.close()
        print ("Tne number of edges:\t", len(edges))
        return edges

    def load_nodes_file(self, node_path):
        attribute_file = open(node_path, "r", encoding="UTF-8")
        nodes = []
        for line in attribute_file:
            nodes.append(Lnode(line))
        attribute_file.close()
        print ("Tne number of nodes:\t", len(nodes))
        return nodes

    def community_detect(self):
        best_q = -1
        while True:
            self.cluster()
            q = self.compute_modularity()
            print (q)
            if q == best_q:
                partition = [node.group for node in self.nodes if node.group]
                return (best_q, partition)
            self.rebuild_graph()
            best_q = q

    def get_neighbors(self, id):
        for e in self.edges_of_node[id]:
            if e[0] == e[1]:  # a node is not neighbor with itself
                continue
            elif e[0] == id:
                yield e[1]
            else:
                yield e[0]

    def cluster(self):
        current_node = [node for node in self.nodes if not node.is_merged]
        while True:
            improved = False
            for node in current_node:
                id = node.id
                node_community = self.communities[id]
                best_community = node_community
                best_gain = 0
                best_shared_links = 0

                for e in self.edges_of_node[id]:
                    if e[0] == e[1]:
                        continue
                    if e[0] == id and self.communities[e[1]] == node_community:
                        best_shared_links += self.edges[e]
                    elif e[1] == id and self.communities[e[0]] == node_community:
                        best_shared_links += self.edges[e]
                self.s_in[node_community] -= 2 * (best_shared_links + self.L_i_in[id])
                self.s_tot[node_community] -= self.L_i[id]

                visited_communities = set()
                for neighbor in self.get_neighbors(id):
                    neighbor_community = self.communities[neighbor]
                    if neighbor_community in visited_communities:
                        continue
                    visited_communities.add(neighbor_community)
                    shared_links = 0
                    for e in self.edges_of_node[id]:
                        if e[0] == e[1]:
                            continue
                        if e[0] == id and self.communities[e[1]] == neighbor_community:
                            shared_links += self.edges[e]
                        elif e[1] == id and self.communities[e[0]] == neighbor_community:
                            shared_links += self.edges[e]
                    # compute modularity gain obtained by moving node to the community of its neighbor
                    gain = self.compute_modularity_gain(id, neighbor_community, shared_links)


                    node_similar = Lnode.are_nodes_similar(self.nodes[id], self.nodes[neighbor_community])

                    if gain + node_similar > best_gain:
                        best_community = neighbor_community
                        best_gain = gain + node_similar
                        best_shared_links = shared_links
                    """

                    if gain > best_gain:
                        best_community = neighbor_community
                        best_gain = gain
                        best_shared_links = shared_links
                    """

                self.s_in[best_community] += 2 * (best_shared_links + self.L_i_in[id])
                self.s_tot[best_community] += self.L_i[id]
                self.communities[id] = best_community

                if best_community != node_community:
                    Lnode.merge_nodes(self.nodes[best_community], self.nodes[id])
                    improved = True
            if not improved:
                return

    def rebuild_graph(self):
        t_edges = {}
        for (e, w) in self.edges.items():
            n1 = self.communities[e[0]]
            n2 = self.communities[e[1]]
            if n1 > n2:
                n1, n2 = n2, n1
            try:
                t_edges[(n1, n2)] += w
            except KeyError:
                t_edges[(n1, n2)] = w
        self.edges = t_edges
        self.edges_of_node = {}
        self.L_i = [0 for n in self.nodes]
        self.L_i_in = [0 for n in self.nodes]
        for (e, w) in self.edges.items():
            self.L_i[e[0]] += w
            self.L_i[e[1]] += w
            if e[0] not in self.edges_of_node:
                self.edges_of_node[e[0]] = [e]
            else:
                self.edges_of_node[e[0]].append(e)
            if e[1] not in self.edges_of_node:
                self.edges_of_node[e[1]] = [e]
            elif e[0] != e[1]:
                self.edges_of_node[e[1]].append(e)
        self.communities = [n.id for n in self.nodes]

        self.s_in = [0 for node in self.nodes]
        self.s_tot = [self.L_i[node.id] for node in self.nodes]

        for (e, w) in self.edges.items():
            if e[0] == e[1]:
                self.s_in[e[0]] += 2 * w

    def compute_modularity(self):
        q = 0
        for i in range(len(self.nodes)):
            q += self.s_in[i] / (self.w * 2) - (self.s_tot[i] / (self.w * 2)) ** 2
        return q

    def compute_modularity_gain(self, id, neighbor, L_i_in):
        return 2 * L_i_in - self.s_tot[neighbor] * self.L_i[id] / self.w
