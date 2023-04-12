import heapq
from Input import Graph

def count_distance(path, weighted) -> float:
    distance = 0
    for i in range(len(path) - 1):
        distance += weighted[path[i]][path[i + 1]]
    return distance

def ucs(graph, start, goal) -> tuple:
    """
    Finds the shortest path from start to goal using Uniform Cost Search algorithm.

    :param graph: the weighted adjacency matrix of the graph
    :param start: the starting node
    :param goal: the goal node
    :return: the shortest path as a list of nodes
    """

    # Create a dictionary to store the parent node of each visited node
    parent = {}

    # Create a dictionary to store the cost of the path from the starting node to each visited node
    cost = {}

    # Initialize the cost of the starting node to 0
    cost[start] = 0

    # Create a priority queue to store the nodes to visit
    pq = []

    # Add the starting node to the priority queue with cost 0
    heapq.heappush(pq, (0, start))

    # Loop until the priority queue is empty
    while pq:
        # Pop the node with the smallest cost from the priority queue
        node_cost, node = heapq.heappop(pq)

        # If the goal node is reached, return the shortest path
        if node == goal:
            path = [node]
            while node in parent:
                node = parent[node]
                path.append(node)
            return (path[::-1], count_distance(path[::-1], graph))

        # Loop through the neighbors of the current node
        for neighbor, weight in enumerate(graph[node]):
            # Ignore nodes that is not the neighbor or have already been visited with a lower cost
            if weight == 0 or neighbor in cost and cost[neighbor] <= node_cost + weight:
                continue

            # Update the cost and parent of the neighbor
            cost[neighbor] = node_cost + weight
            parent[neighbor] = node

            # Add the neighbor to the priority queue with its new cost
            heapq.heappush(pq, (cost[neighbor], neighbor))

    # If the goal node cannot be reached, return None
    return None

if __name__ == "__main__":
    import os
    input = Graph()

    file_path = os.getcwd() + '/test/arad.txt'
    print(file_path)


    # print('Nodes:')
    # for i in range(len(nodes)):
    #     print(i, nodes[i])
    # print('Adjecency:')
    # for i in range(len(adj)):
    #     print(adj[i])
    
    input.read_input_coords(file_path)
    input.calculate_weighted()

    weighted_graph = input.get_weighted()

    # print('Coords:')
    # print(input.get_coords())

    # for i in range(len(weighted_graph)):
    #     print(weighted_graph[i])

    res = ucs(input.get_weighted(), 0, 1)
    print(res)
    