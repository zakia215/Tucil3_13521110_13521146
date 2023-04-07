import heapq
import math
from Input import Graph

def distance(coord1, coord2):
    """
    Calculate the distance between two 2-dimensional coordinates

    :param coord1: coordinates for point 1
    :param coord2: coordinates for point 2
    :return: Euclidean distance between two coordinates
    """

    return math.sqrt((float(coord2[0]) - float(coord1[0])) ** 2 + (float(coord2[1]) - float(coord1[1])) ** 2)

def a_star(weighted_matrix, coords, start, goal):
    """
    Find the shortest path from start to goal using A* algorithm

    Parameters:
    weighted_matrix: 2D list that represents the weighted adjacency matrix of the graph
    coords: a dictionary mapping each node to their respective (x, y) coordinate
    start: the start node
    goal: the goal node

    Returns:
    (path, distance): tuple where path is the list of nodes in the shortest path
    """
    queued_node = [(0, start)]
    discovered = set()

    # Initialize the g_value (distance from start to current node) of each node with infinity (not explored yet)
    g_value = {node: float("inf") for node in range(len(weighted_matrix))}
    g_value[start] = 0

    # Initialize f_value (distance from start + straight line distance between current node and goal)
    f_value = {node: float("inf") for node in range(len(weighted_matrix))}
    f_value[start] = distance(coords[start], coords[goal])

    # Dictionary of the parents of each node
    parent = {}

    # Keep iterating while the priority queue is not empty
    while queued_node:
        cur_node = heapq.heappop(queued_node)[1]

        # If goal found then backtrack through the parent dictionary and return the result
        if cur_node == goal:
            path = [cur_node]
            while cur_node in parent:
                cur_node = parent[cur_node]
                path.append(cur_node)
            # Return the path and the cost of the path (g_value)
            return (path[::-1], g_value[goal])

        discovered.add(cur_node)

        for neighbor in range(len(weighted_matrix)):
            if (weighted_matrix[cur_node][neighbor]) > 0 and neighbor not in discovered:
                test_g_value = g_value[cur_node] + weighted_matrix[cur_node][neighbor]

                # To prevent repetition of the same node, we only add this to the prio_queue if it has a better g_value than the current available g_value
                if test_g_value < g_value[neighbor]:
                    parent[neighbor] = cur_node
                    g_value[neighbor] = test_g_value

                    # g_value is added to the straight line distance between the coordinates
                    f_value[neighbor] = g_value[neighbor] + distance(coords[neighbor], coords[goal])
                    heapq.heappush(queued_node, (f_value[neighbor], neighbor))

    return None;

if __name__ == "__main__":
    input = Graph()

    input.read_input('/test/arad.txt')
    nodes = input.get_nodes()

    adj = input.get_adj()

    # print('Nodes:')
    # for i in range(len(nodes)):
    #     print(i, nodes[i])
    # print('Adjecency:')
    # for i in range(len(adj)):
    #     print(adj[i])
    
    input.read_input_coords('/test/arad.txt')
    input.calculate_weighted();

    # weighted_graph = input.get_weighted();

    # print('Coords:')
    # print(input.get_coords())

    # for i in range(len(weighted_graph)):
    #     print(weighted_graph[i])

    res = a_star(input.get_weighted(), input.get_coords(), 0, 1)
    print(res)