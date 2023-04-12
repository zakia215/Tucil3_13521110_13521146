import os
from haversine import haversine, Unit

class Graph:
    def __init__ (self):
        self.n : int = 0              # number of nodes
        self.nodes : list = []         # list of nodes
        
        # dictionary of coordinates (key = node, value = (lat, long))
        self.coords : dict = {} 

        self.adj : list = []           # adjecency matrix
        self.weighted : list = []      # weighted adjecency matrix

    # read input from file (without coordinates)
    def read_input(self, file_name: str):
        with open(file_name, 'r') as file:
            line = file.readline()
            # number of nodes
            self.n = int(line)
            # read the nodes
            for _ in range(self.n):
                line = file.readline()
                line = line.split()
                node = line[0]
                self.nodes.append(node)
            # read the adjecency matrix
            for _ in range(self.n):
                line = file.readline()
                line = line.split()
                line = [int(x) for x in line]
                self.adj.append(line)

    # read input from file (with coordinates)            
    def read_input_coords(self, file_name: str): 
        self.read_input(file_name)
        with open(file_name, 'r') as file:
            file.readline()
            # read the nodes
            for i in range(self.n):
                line = file.readline()
                line = line.split()
                # add coords to dictionary
                if (len(line) < 3):
                    raise Exception('Invalid input file')
                lat = line[1]
                long = line[2]
                self.coords[i] = (lat, long)
    
    # calculate the weighted adjecency matrix
    def calculate_weighted(self): 
        distance = {}
        self.weighted = []
        for i in range(len(self.adj)):
            line = []
            for j in range(len(self.adj[i])):
                if self.adj[i][j] == 1:
                    string_key = self.nodes[i] + self.nodes[j]
                    flipped_key = self.nodes[j] + self.nodes[i]
                    if string_key in distance:
                        line.append(distance[string_key])
                    elif flipped_key in distance:
                        line.append(distance[flipped_key])
                    else :
                        coord_a = self.coords[i]
                        coord_b = self.coords[j]
                        float_a = (float(coord_a[0]), float(coord_a[1]))
                        float_b = (float(coord_b[0]), float(coord_b[1]))
                        res = haversine(float_a, float_b)
                        distance[string_key] = res
                        line.append(distance[string_key])
                else:
                    line.append(0)
            self.weighted.append(line)
        
    # getters    
    def get_nodes(self) -> list:
        return self.nodes
    def get_adj(self) -> list:
        return self.adj
    def get_coords(self) -> dict:
        return self.coords
    def get_weighted(self) -> list:
        return self.weighted
       

if __name__ == "__main__":
    input = Graph()

    file_path = os.getcwd() + '/test/arad.txt'

    input.read_input(file_path)

    nodes = input.get_nodes()

    adj = input.get_adj()

    print('Nodes:')
    for i in range(len(nodes)):
        print(i, nodes[i])
    print('Adjecency:')
    for i in range(len(adj)):
        print(adj[i])
    
    # input.read_input_coords(file_path)

    # print('Coords:')
    # print(input.get_coords())