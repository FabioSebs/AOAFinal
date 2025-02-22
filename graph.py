from os import read
import vertex
import json
import random
import numpy as np
from prettytable import PrettyTable


class Graph():
    def __init__(self):
        print("Created Graph! \n")
        self.vertices = []
        self.edges = {}

    def addVertex(self, vertex):
        if (self.isEmpty()):
            self.vertices.append(vertex)
            self.edges.update({vertex: []})
        else:
            self.vertices.append(vertex)
            self.edges.update({vertex: []})
            # Connecting last two vertexes in graph together
            self.addEdges(self.vertices[len(
                self.vertices)-1], self.vertices[len(self.vertices)-2])

    def addEdges(self, vertex1, vertex2):
        self.edges[vertex1].append(vertex2)
        self.edges[vertex2].append(vertex1)

    def isEmpty(self):
        return True if not len(self.vertices) else False

    def printGraph(self):
        x = PrettyTable()
        x.field_names = [
            "Vertices (Cities)", "Edges (Cities/Distance)"]

        try:
            for v in self.vertices:
                x.add_row([v.data, [x.getInfo() for x in self.edges[v]]])
            print(x)
        except:
            print("Graph Vertices is not consisted of Cities from JSON file.")

    # UTILITY FUNCTION

    def readJson(self):
        with open("./dataset/cities.json") as f:
            data = json.load(f)
        data = np.asarray(data)
        data = np.delete(data, 0, 0)  # dropping first row
        data = np.delete(data, -1, 0)  # dropping last row
        return np.asarray(data)  # format [{name:, position:}]

    # Converting Latitude and Longitude to Map Coordinates
    # Explained in the link below (Skip Step 4)
    # https://lweb.cfa.harvard.edu/space_geodesy/ATLAS/cme_convert.html
    # Note: All Indonesian Cities will have South Latitude and East Longitude
    def calculateDistance(self, position):
        try:
            Latdegrees, Latminutes = int(position[0:2]), int(position[2:4])
            Londegrees, Lonminutes = int(position[4:6]), int(position[6:])

        except Exception:
            print("Calculating Distance \n")
            # Latdegrees, Latminutes = int(position[0:2]), int(position[2:4])
            # Londegrees, Lonminutes = int(position[4:6]), int(position[6:8])

        finally:
            Latdegrees, Latminutes = int(position[0:2]), int(position[2:4])
            Londegrees, Lonminutes = int(position[4:6]), 0

        Latdegrees *= 60
        Londegrees *= 60
        x = Latdegrees + Latminutes
        y = Londegrees + Lonminutes

        return (x+y)

    def getDest():
        pass

    def getGoal():
        pass


class DjikstraGraph(Graph):
    def __init__(self):
        super().__init__()

    def populateGraphDjikstra(self, amount):
        data = self.readJson()

        for i in range(1, amount+1):
            city = vertex.DjikstraVertex(
                data[i]["name"], self.calculateDistance(str(data[i]["position"])))
            self.addVertex(city)

    def mapify(self, startNode, goalNode):
        for v in self.vertices:
            for i in range(len(self.edges[v])):
                self.edges[v][i].weight = abs(
                    self.edges[v][i].weight - v.weight)

                for x in self.edges[v]:
                    if x.data.upper() == goalNode.upper():
                        x.weight = 0
                        x.changeWeight(0)

            if goalNode.upper() == v.data.upper():
                v.changeWeight(0)

        # self.printGraph()
        return (startNode.upper(), goalNode.upper())


class AStarGraph(Graph):
    def __init__(self):
        super().__init__()

    def populateGraphAStar(self, amount):
        data = self.readJson()

        for i in range(amount+1):
            city = vertex.AStarVertex(
                data[i]["name"], self.calculateDistance(str(data[i]["position"])), 0)
            self.addVertex(city)

    def mapify(self, startNode, goalNode):
        goalNodeIndex = 0
        # Getting the Start Node Index
        for idx, val in enumerate(self.vertices):
            if goalNode.upper() == val.data.upper():
                goalNodeIndex = idx

        # Changing the Weights and Hueristics
        for v in self.vertices:
            for i in range(len(self.edges[v])):
                self.edges[v][i].weight = abs(
                    self.edges[v][i].weight - v.weight)

                self.edges[v][i].hueristic = self.distanceFrom(
                    self.vertices[goalNodeIndex], self.edges[v][i])

                if startNode.upper() == self.edges[v][i].data.upper():
                    self.edges[v][i].weight = 0
                    self.edges[v][i].hueristic = 0

            if startNode.upper() == v.data.upper():
                v.weight = 0
                v.hueristic = 0

        self.printGraph()
        return (startNode.upper(), goalNode.upper())

    def distanceFrom(self, vertex1, vertex2):
        return abs(vertex1.weight - vertex2.weight)

    def printGraph(self):
        x = PrettyTable()
        x.field_names = [
            "Vertices (Cities)", "Edges (Cities/Distance/Hueristic)"]

        try:
            for v in self.vertices:
                x.add_row([v.data, [x.getInfo() for x in self.edges[v]]])
            print(x)
        except:
            print("Graph Vertices is not consisted of Cities from JSON file.")
