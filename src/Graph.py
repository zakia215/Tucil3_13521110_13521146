class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.coords = {}
        self.adj_list = {}

    def add_edge(self, u, v, weight):
        if u not in self.adj_list:
            self.adj_list[u] = []
        self.adj_list[u].append((v, weight))

    def add_coords(self, node, x, y):
        self.coords[node] = (x,y)

    def add_edges_from_matrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    u, v, weight = nodes[i], nodes[j], matrix[i][j]
                    self.add_edge(u, v, weight)

    def get_neighbors(self, u):
        return self.adj_list.get(u, [])

    def getadj_list(self):
        return self.adj_list
    
    def __str__(self):
        return str(self.adj_list)
    

if __name__ == "__main__":
    nodes = ['a', 'b', 'c', 'd', 'e', 'f']
    graph = Graph(nodes)
    matrix = [[0, 0, 0, 0, 0, 10],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 1, 0]]
    graph.add_edges_from_matrix(matrix)
    
    adj  = graph.getadj_list()

    print(adj)

    for node in nodes:
        for n, w in graph.get_neighbors(node):
            print(node, n, w)
