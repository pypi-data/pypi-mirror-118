from pathlib import Path

class Library:
  def __init__(self):
    pass

def get_boilerplate():
  with open(Path(__file__).parent/'data/boilerplate/library.lbr', 'r') as f:
    raw = f.read()
  return raw
