from Node import Node
from Edge import Edge
from queue import PriorityQueue


import json

class Graph():
  nodes = dict()
  edges = set()

  def initGraph(self,data):
    nodes = self.nodes
    edges = self.edges
    # add actor nodes
    for a in data['actors']:
      newNode = Node('actor', a)
      if newNode not in nodes:
        nodes[newNode.id] = newNode

    # add film nodes
    for f in data['films']:
      newNode = Node('film', f)
      if newNode not in nodes:
        nodes[newNode.id] = newNode

    # add edges (gross values an actor gained from a movie)
    for v in data['values']:
      nodeSrc = nodes.get(v['connections'][0])
      nodeDes = nodes.get(v['connections'][1])
      newEdge = Edge(nodeSrc, nodeDes, v['value'])
      if nodeDes not in nodeSrc.edges:
        nodeSrc.edges.append(nodeDes)
      if nodeSrc not in nodeDes.edges:
        nodeDes.edges.append(nodeSrc)
      if newEdge not in edges:
        edges.add(newEdge)

 # Find how much a movie has grossed
  def numFilms(self):
    countFilm = 0
    for k in self.nodes:
      if self.nodes[k].label == 'film':
        countFilm += 1
    return countFilm

  # List which movies an actor has worked in
  def actFilms(self,act):
    actfilms = []
    for k in self.nodes:
      if self.nodes[k].id == act:
        actfilms.append(self.nodes[k].edges)
    return actfilms

  # List which actors worked in a movie
  def actFilms(self, mov):
    mvcasts = []
    for k in self.nodes:
      if self.nodes[k].id == mov:
        mvcasts.append(self.nodes[k].casts)
    return mvcasts

  # List the top X actors with the most total grossing value
  def actFilms(self, mov):
    mvcasts = []
    for k in self.nodes:
      if self.nodes[k].id == mov:
        mvcasts.append(self.nodes[k].casts)
    return mvcasts

  # List the oldest X actors
  def oldAct(self, X):
    oldActs = []
    prio_queue = PriorityQueue()
    for k in self.nodes:
      if self.nodes[k].label == 'actor':
        prio_queue.put(self.nodes[k])
    i = 0
    while i < X:
      oldActs.append(prio_queue.get())
    return oldActs
















