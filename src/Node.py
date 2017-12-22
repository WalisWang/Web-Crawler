class Node:
  label = ''
  id = ''
  age = 0.0
  year = 0
  casts = ''
  edges = []
  # Assigns values as constructor
  def __init__(self, label, data):
    if label == 'actor':
        self.label = label
        self.id = data['name']
        self.age = data['age']
    if label == 'film':
        self.label = label
        self.id = data['name']
        self.casts = data['casts']
        self.year = data['year']
    self.edges = []

  # Get adjacants of the node
  def get_adjs(self):
    adjs = []
    for edge in self.edges:
      adjs.append(edge.id)
    return adjs
