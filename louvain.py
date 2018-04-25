class Louvain:
    nodes = dict()
    edges = []

    def load_node_edge(self, path):
        node_edge = open(path, "r")
        for line in node_edge:
            global edges
            temp = line.split("\t", 2)
            edges.append(((temp[0],temp[1]),int(temp[2])))

    def load_node_attribute(self,path):
        node_attribute=open(path,"r")
        for line in node_attribute:
            global nodes
            temp=line.split("\t",)
