from unittest import TestCase
from Graph import Graph
import json

class TestGraph():

  def setUp(self):
    with open('test_data.json') as data_file:
      data = json.load(data_file)
    self.testGragh = Graph()
    self.testGragh.initGraph(data)
    nodes = self.testGragh.nodes
    for k in nodes:
      if nodes[k] is not None:
        print("=====================================")
        print("Node: " + nodes[k].id)
        if nodes[k].age != 0:
          print(nodes[k].age)
        print("Edge(s): ")
        for ee in nodes[k].edges:
          print(ee.id)

  def testNodeNum(self):
    assert (len(self.nodes) == 6)

  def testEdgeNum(self):
    assert (len(self.edges) == 4)
