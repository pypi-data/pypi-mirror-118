from . import xmltools
from .settings import Settings
from .layers import Layers
from .board import Board

class Drawing:
  def __init__(self, root):
    self._root = root
    self._settings = None
    self._layers = None
    self._board = None
  
  @property
  def settings(self):
    if self._settings is None:
      self._settings = Settings(next(xmltools.at_path(self._root, 'settings')))
    return self._settings

  @property
  def layers(self):
    if self._layers is None:
      self._layers = Layers(next(xmltools.at_path(self._root, 'layers')))
    return self._layers
  
  @property
  def board(self):
    if self._board is None:
      self._board = Board(next(xmltools.at_path(self._root, 'board')))
    return self._board
