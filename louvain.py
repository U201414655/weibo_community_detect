class Louvain:
    t_nodes = dict()
    t_edges = []

    nodes = dict()
    edges = []

    def load_node_edge(self, path):
        node_edge = open(path, "r")
        for line in node_edge:
            global t_nodes, t_edges
            temp = line.split("\t", 2)
            t_nodes[temp[0]] = t_nodes[temp[1]] = 1
            t_edges.append(((temp[0], temp[1]), int(temp[2])))
        node_edge.close()

    def load_node_attribute(self, path):
        node_attribute = open(path, "r")
        for line in node_attribute:
            global nodes
            line.rstrip()
        node_attribute.close()

    def rebuild_to_succession(self):
        node_key = list(t_nodes.keys())
        node_key.sort()
        index = 0
        for n in node_key:
            nodes[n] = index
            index = index + 1
        for e in t_edges:
            global edges
            edges.append(((nodes[e[0][0]], nodes[e[0][1]]), nodes[e[1]]))
