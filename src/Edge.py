# Edge class
# Simply contains data needed to be stored on edges
from Node import Node
class Edge:
  def __init__(self, src, des, weight):
    self.src = src
    self.des = des
    self.weight = weight
