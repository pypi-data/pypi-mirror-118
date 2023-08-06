from . import xmltools
from .mocknode import MockElementTreeNode

def get_board(root):
  return Board(xmltools.at_path(root, 'drawing/board'))

class Board(MockElementTreeNode):
  def __init__(self, root):
    MockElementTreeNode.__init__(self, root)
    self._libraries = None
    self._attributes = None
    self._variantdefs = None
    self._classes = None
    self._designrules = None
    self._autorouter = None
    self._elements = None
  
  @property
  def libraries(self):
    if self._libraries is None:
      self._libraries = next(xmltools.at_path(self._root, 'libraries'))
    return self._libraries

  @property
  def attributes(self):
    if self._attributes is None:
      self._attributes = next(xmltools.at_path(self._root, 'attributes'))
    return self._attributes
  
  @property
  def variantdefs(self):
    if self._variantdefs is None:
      self._variantdefs = next(xmltools.at_path(self._root, 'variantdefs'))
    return self._variantdefs

  @property
  def classes(self):
    if self._classes is None:
      self._classes = next(xmltools.at_path(self._root, 'classes'))
    return self._classes

  @property
  def designrules(self):
    if self._designrules is None:
      self._designrules = next(xmltools.at_path(self._root, 'designrules'))
    return self._designrules

  @property
  def autorouter(self):
    if self._autorouter is None:
      self._autorouter = next(xmltools.at_path(self._root, 'autorouter'))
    return self._autorouter

  @property
  def elements(self):
    if self._elements is None:
      elements = next(xmltools.at_path(self._root, 'elements'))
      self._elements = (Element(root, self) for root in xmltools.with_tags(elements, 'element'))
    return self._elements

  # def __iter__(self):
  #   # todo: do not expand element for iterator
  #   self._iterdata = [c for c in self._element]
  #   return self
  
  # def __next__(self):
  #   try:
  #     return self._iterdata.pop(0)
  #   except:
  #     raise StopIteration

  # @property
  # def libraries(self):
  #   return xmltools.at_path(self._element, 'libraries')

  # @property
  # def elements(self):
  #   return xmltools.at_path(self._element, 'elements')


class Element(MockElementTreeNode):
  def __init__(self, root, board):
    MockElementTreeNode.__init__(self, root)
    self._board = board

  @property
  def package(self):
    library_name = self._root.attrib['library']
    package_name = self._root.attrib['package']
    library = next(xmltools.with_attributes(self._board.libraries, {'name': library_name}))
    packages = next(xmltools.at_path(library, 'packages'))
    package = next(xmltools.with_attributes(packages, {'name': package_name}))
    return package

