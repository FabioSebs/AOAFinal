from os import read
import vertex
import json
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
        Latdegrees, Latminutes = int(position[1:3]), int(position[3:5])
        Londegrees, Lonminutes = int(position[5:7]), int(position[7:9])

        Latdegrees *= 60
        Londegrees *= 60
        x = Latdegrees + Latminutes
        y = Londegrees + Lonminutes

        return (x+y)


class DjikstraGraph(Graph):
    def __init__(self):
        super().__init__()

    def populateGraphDjikstra(self, amount):
        data = self.readJson()

        if not len(self.vertices):
            root = vertex.DjikstraVertex(data[0]["name"], 0)
            self.addVertex(root)

        for i in range(1, amount+1):
            city = vertex.DjikstraVertex(
                data[i]["name"], self.calculateDistance(data[0]["position"]) - self.calculateDistance(data[i]["position"]))
            self.addVertex(city)


class AStarGraph(Graph):
    def __init__(self):
        super().__init__()

    def populateGraphAStar(self, amount):
        data = self.readJson()

        if not len(self.vertices):
            root = vertex.AStarVertex(data[0]["name"], 0, 0)
            self.addVertex(root)

        for i in range(amount+1):
            city = vertex.AStarVertex(data[i]["name"], self.calculateDistance(
                data[0]["position"]) - self.calculateDistance(data[i]["position"]), 0)
            self.addVertex(city)

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
