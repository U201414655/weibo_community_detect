from Lnode import Lnode


class Louvain():
    def __init__(self, edge_path, node_path):
        self.edges = self.load_edges_file(edge_path)
        self.nodes = self.load_nodes_file(node_path)
        self.w = 0
        self.L_i = [0 for n in self.nodes]
        self.L_i_in = [0 for n in self.nodes]
        self.is_combined = [False for n in self.nodes]
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

    def load_edges_file(self, edge_path):
        edge_file = open(edge_path, "r", encoding="UTF-8")
        edges = {}
        for line in edge_file:
            e = line.split("\t", 2)
            edges[(int(e[0]), int(e[1]))] = int(e[2])
        edge_file.close()
        return edges

    def load_nodes_file(self, node_path):
        attribute_file = open(node_path, "r", encoding="UTF-8")
        nodes = []
        for line in attribute_file:
            nodes.append(Lnode(line))
        attribute_file.close()
        return nodes

    def cluster(self):
        best_q = -1
        while True:
            self.first_phase()
            q = self.compute_modularity()
            print (q)
            if q == best_q:
                return best_q
            best_q = q

    def init_partition(self):
        self.s_in = [self.s_in[node.id] if not self.is_combined[node.id] else 0 for node in self.nodes]
        self.s_tot = [self.L_i[node.id] if not self.is_combined[node.id] else 0 for node in self.nodes]
        for (e, w) in self.edges.items():
            if e[0] == e[1]:
                self.s_in[e[0]] += w
                self.s_in[e[1]] += w

    def get_neighbors(self, id):
        for e in self.edges_of_node[id]:
            if e[0] == e[0]:  # a node is not neighbor with itself
                continue
            if e[0] == id:
                yield e[1]
            if e[1] == id:
                yield e[0]

    def first_phase(self):
        self.init_partition()
        while True:
            improved = False
            current_node = [node for node in self.nodes if not self.is_combined[node.id]]
            for node in current_node:
                id = node.id
                best_gain = 0
                best_shared_links = 0
                best_community = id

                for e in self.edges_of_node[id]:
                    if e[0] == e[1]:
                        continue
                    if e[0] == id and e[1] in self.nodes[id].group or e[1] == id and e[0] in self.nodes[id].group:
                        best_shared_links += self.edges[e]
                self.s_in[id] -= 2 * (best_shared_links + self.L_i_in[id])
                self.s_tot[id] -= self.L_i[id]

                visited_neighbors = set()
                for neighbor in self.get_neighbors(id):
                    if neighbor in visited_neighbors:
                        continue
                    visited_neighbors.add(neighbor)
                    shared_links = 0
                    for e in self.edges_of_node[id]:
                        if e[0] == e[1]:
                            continue
                        if e[0] == id and e[1] in self.nodes[neighbor].group or e[1] == id and e[0] in self.nodes[neighbor].group:
                            shared_links += self.edges[e]
                    # compute modularity gain obtained by moving _node to the community of _neighbor
                    gain = self.compute_modularity_gain(id, neighbor, shared_links)
                    # to-do
                    if gain > best_gain:
                        best_community = neighbor
                        best_gain = gain
                        best_shared_links = shared_links

                self.s_in[best_community] += 2 * (best_shared_links + self.L_i_in[id])
                self.s_tot[best_community] += self.L_i[id]
                if best_community != id:
                    print (id)
                    combine_nodes(best_community, id)
                    combine_edges(best_community, id)
                    self.is_combined[id] = True
                    improved = True
            if not improved:
                return

    def combine_nodes(self, best, id):
        self.nodes[best].group.extend(self.nodes[id].group)
        self.nodes[id].group.clear()

    def combine_edges(self, best, id):
        pass

    def compute_modularity(self):
        q = 0
        for i in range(len(self.nodes)):
            q += self.s_in[i] / (self.w * 2) - (self.s_tot[i] / (self.w * 2)) ** 2
        return q

    def compute_modularity_gain(self, id, neighbor, L_i_in):
        return 2 * L_i_in - self.s_tot[neighbor] * self.L_i[id] / self.w
