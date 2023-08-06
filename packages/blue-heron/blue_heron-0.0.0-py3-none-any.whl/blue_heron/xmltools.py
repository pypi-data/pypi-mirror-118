# xmltools generally expects an etree compatible api for iterators, though in some cases other iterators may be used as well 

def with_tags(iter, tags):
  if not isinstance(tags, list):
    tags = [tags]
  for child in iter:
    if child.tag in tags:
      yield child

def at_path(iter, path):
  # note: use only for unique unambiguous paths...
  #       if multiple child elements on one level share the same tag the resulting element is undefined
  g = iter
  for level in path.split('/'):
    g = next(with_tags(g, level))
  yield g

def with_attributes(iter, dict):
  def filter_fn_factory(key, value):
    def filter_fn(element):
      try:
        return element.attrib[key] == value
      except KeyError:
        return False
    return filter_fn
  
  f = iter
  for key, value in dict.items():
    f = filter(filter_fn_factory(key, value), f)
  return f
