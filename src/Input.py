import os
class Input:
    def __init__ (self):
        self.n = 0
        self.nodes = []
        self.coords = {}
        self.adj = []

    def read_input(self, file_name: str):
        with open(os.getcwd() + file_name, 'r') as file:
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
       
    def read_input_coords(self, file_name: str): 
        self.read_input(file_name)
        with open(os.getcwd() + file_name, 'r') as file:
            file.readline()
            # read the nodes
            for _ in range(self.n):
                line = file.readline()
                line = line.split()
                node = line[0]
            # add coords to dictionary
                lat = line[1]
                long = line[2]
                self.coords[node] = (lat, long)
        
    def get_nodes(self):
        return self.nodes

    def get_adj(self):
        return self.adj
    
    def get_coords(self):
        return self.coords
       

if __name__ == "__main__":
    input = Input()

    input.read_input('/test/input.txt')

    nodes = input.get_nodes()

    adj = input.get_adj()

    print('Nodes:')
    for i in range(len(nodes)):
        print(i, nodes[i])
    print('Adjecency:')
    for i in range(len(adj)):
        print(adj[i])
    
    input.read_input_coords('/test/input.txt')

    print('Coords:')
    print(input.get_coords())