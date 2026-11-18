import xml.etree.ElementTree as ET
import os

# the guide:
# https://casparcg.net/validator/explained.html

class xmlEntry:
  def __init__(self, tag:str, args:dict[str,str], text:str | None):
    self.tag = tag
    self.args = args
    self.children:list['xmlEntry'] = []
    self.text:str = text.strip() if text else ""
  def addChild(self, child:'xmlEntry'):
    self.children.append(child)
  def getChild(self, tag:str) -> 'xmlEntry | None':
    out = None
    for child in self.children:
      if child.tag == tag:
        if out is not None:
          raise Exception("Multiple children with tag " + tag)
        out = child
    return out
  def getChildren(self, tag:str) -> 'list[xmlEntry]':
    out:list['xmlEntry'] = []
    for child in self.children:
      if child.tag == tag:
        out.append(child)
    return out
  def removeChildren(self, tag:str):
    self.children = [child for child in self.children if child.tag != tag]
  def stringify(self, indent:int, useSpaces:bool = True, spaceCount:int = 4) -> str:
    if useSpaces:
      indentStr = " " * indent * spaceCount
    else:
      indentStr = "\t" * indent
    out = indentStr
    
    out += "<" + self.tag 
    for key, val in self.args.items():
      out += " " + key + "=\"" + val + "\""
    if not self.children and not self.text:
      out += " />"
      return out
    
    out += ">"
    
    out += self.text
    if not self.children:
      out += "</" + self.tag + ">"
    
    for child in self.children:
      out += "\n" + child.stringify(indent + 1, useSpaces, spaceCount)
    
    if self.children:
      out += "\n" + indentStr + "</" + self.tag + ">"
    
    return out
  def __str__(self) -> str:
    return self.stringify(0)

def xmlToDict(element:ET.Element | str | list[str]) -> xmlEntry:
  if isinstance(element, str):
    element = ET.fromstring(element)
  if isinstance(element, list):
    element = ET.fromstringlist(element)
  
  out:xmlEntry = xmlEntry(element.tag,element.attrib,element.text)
  for e in element:
    out.addChild(xmlToDict(e))
  return out

def getConfig(path:str = "~/casparCG/casparcg.config"):
  return xmlToDict(open(os.path.expanduser(path)).read())

def saveConfig(config:xmlEntry, path:str = "~/casparCG/casparcg.config"):
  with open(os.path.expanduser(path), "w") as f:
    f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\n")
    f.write(config.stringify(0))

if __name__ == "__main__":
  print(getConfig())