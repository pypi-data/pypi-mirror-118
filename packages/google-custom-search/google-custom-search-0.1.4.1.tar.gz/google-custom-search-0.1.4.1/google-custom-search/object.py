import json

class ImageError(Exception):
  pass

class result(object):
  def __init__(self, api, **kwarg):
    self.api=api
    
  @property
  def titles(self):
    #title=[]
    title=[e["title"] for e in self.api["items"]]
    return title
    
  @property
  def urls(self):
    url=[e["link"] for e in self.api["items"]]
    return url
    
  @property
  def display_urls(self):
    url=[e["displayLink"] for e in self.api["items"]]
    return url
    
  @property
  def html_titles(self):
    title=[i["htmlTitle"] for i in self.api["items"]]
    return title
    
  @property
  def snippets(self):
    snippet=[i["snippet"] for i in self.api["items"]]
    return snippet
    
  @property
  def json(self):
    return self.api