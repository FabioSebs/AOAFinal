from queue import PriorityQueue
from prettytable import PrettyTable
from vertex import *
from graph import *
from dataclasses import dataclass, field
from typing import Any

# To help the priority ( object of dijkstra vertex , wrapper class for our data
# We start our node with the priority of 0


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def heuristic(a, b):
    temp = AStarGraph()
    return temp.distanceFrom(a, b)


def a_star_search(map, startNode, goalNode):
    # used to figure out which node to go next
    pq = PriorityQueue()
    # priority starts from 0 (lowest) because we dont want to visit starting node
    pi: PrioritizedItem = PrioritizedItem(0, startNode)

    pq.put(pi)
    came_from = {startNode: None}
    cost_so_far = {startNode: 0}

    # Get Goal Vertex
    goalVertex = None
    for node in map.vertices:
        if node.data.upper() == goalNode:
            goalVertex = node

    # it will keep looping :0
    while not pq.empty():
        # get = will get first item in the queue
        # item = will return DjikstraVertex object
        current = pq.get().item
        # print(f'current:', current)

        if current == goalNode:
            break

        # it will loop to the connected edges
        for key, val in map.edges.items():
            # find the cost by adding up current weight and the weight to the key node

            #  Adds weights of neighbors into cost_so_far
            for nodes in val:
                new_cost = cost_so_far[current] + nodes.weight

            ''' if the new vertex havent been visited or its cost is less than
            the previous cost it will be updated
            since it is looping through the connected edges, it will update the cost with 
            the lowest cost (since there will more than one loop)
            '''

            if val[0].data not in cost_so_far or new_cost < cost_so_far[val[0].data]:

                # updates the cost
                cost_so_far[val[0].data] = new_cost
                # calculate priority level lol
                priority = new_cost + heuristic(goalVertex, val[0])
                pi: PrioritizedItem = PrioritizedItem(priority, val[0].data)
                pq.put(pi)
                # to go to that came from this
                came_from[val[0]] = current

    return came_from, cost_so_far


if __name__ == '__main__':
    graph = Graph()
    graph.addVertex(DjikstraVertex('Kelapa Gading', 2))
    graph.addVertex(DjikstraVertex('Senayan', 8))
    graph.addVertex(DjikstraVertex('Pluit', 11))
    graph.addVertex(DjikstraVertex('Simprug', 14))
    graph.addEdges(graph.vertices[1], graph.vertices[3])
    graph.printGraph()

    print()
    print('came from')
    start = graph.vertices[0]
    goal = graph.vertices[3]
    came_from, cost_so_far = a_star_search(graph, start, goal)
    for key, value in came_from.items():
        print(value.data if value is not None else None, '->', key.data)

    print()
    print('Cost so far')
    for key, value in cost_so_far.items():
        print(key.data, '->', value)

    print()
    for key, value in came_from.items():
        print(key.data, ':', value.data if value is not None else None)
    print()
    print(cost_so_far)


# dataclass is a library from python that generates a class constructor for you and can define a class with the dataclass decorator
# field is for default variables within the dataclass
# typing library is for type checking
# PrioritizedItem is a class with the property of *priority and the *city
# Hueristic Function uses AStarGraph.getDistanceFrom() which has a function that takes two nodes and gets absolute distance from each of their weights
# PrioritizedItem (pi) is what will be put in the PriorityQueue (pq) and be popped until it has reached the GoalNode
# First we put in the startNode in the PriorityQueue as a PrioritizedItem
# Then we loop through always getting the next thing in the PQ as the variable current
# Then we use current as the Key to loop through the nieghbors and add them to cost_so_far if they arent visited
