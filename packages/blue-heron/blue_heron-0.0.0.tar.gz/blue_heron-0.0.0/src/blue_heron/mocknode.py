class MockElementTreeNode:
  def __init__(self, root):
    self._root = root
  
  def __iter__(self):
    return (c for c in self._root)
  
  @property
  def attrib(self):
    return self._root.attrib
