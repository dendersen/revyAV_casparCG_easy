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
  def stringify(self, indent:int, useSpaces:bool = True, spaceCount:int = 4) -> str:
    if useSpaces:
      indentStr = " " * indent * spaceCount
    else:
      indentStr = "\t" * indent
    out = indentStr
    
    out += "<" + self.tag 
    for key, val in self.args.items():
      out += " " + key + "=\"" + val + "\""
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

if __name__ == "__main__":
  print(getConfig())