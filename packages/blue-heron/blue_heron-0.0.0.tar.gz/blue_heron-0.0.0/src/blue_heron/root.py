from . import xmltools
from .mocknode import MockElementTreeNode
from .drawing import Drawing

class Root(MockElementTreeNode):
  def __init__(self, root):
    MockElementTreeNode.__init__(self, root)
    self._drawing = None
  
  @property
  def drawing(self):
    if self._drawing is None:
      self._drawing = Drawing(next(xmltools.at_path(self._root, 'drawing')))
    return self._drawing
