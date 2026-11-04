import subprocess

class Monitor:
  def __init__(self, line:str) -> None:
    line = line.strip()
    self.id:int = -1
    self.connection:str = ""
    self.shape:tuple[int,int] = (-1,-1)
    self.offset:tuple[int,int] = (-1,-1)
    id_string = line
    while (not id_string.isdigit()) and id_string:
      id_string = id_string[0:-1].strip()
    self.id = int(id_string)
    self.connection = line.split()[-1].strip()
    sizeString:str = max(line.split(),key=lambda text : text.count("/")*text.count("x")*text.count("+"))
    width:str
    height:str
    xOffset:str
    yOffset:str
    screenParameters:list[str] = []
    # example
    # 2560/345x1600/215+0+0
    for tempString1 in sizeString.split("/"):
      for tempString2 in tempString1.split("x"):
        for tempString3 in tempString2.split("+"):
          screenParameters.append(tempString3)
    width, _, height, _, xOffset, yOffset = screenParameters
    self.shape = (int(width),int(height))
    self.offset = (int(xOffset),int(yOffset))
  def __str__(self) -> str:
    return f"number:{self.id}, size:{self.shape}, offset:{self.offset}, connection type:{self.connection}"

def getScreenData() -> list[Monitor]:
  proc = subprocess.run(["xrandr","--listmonitors"], stdout=subprocess.PIPE)
  lines:list[str] = proc.stdout.decode("utf8").split("\n")
  temp:list[str] = []
  for l in lines:
    if l:
      temp.append(l)
  lines = temp
  monitorCount = -1
  for line in lines:
    line = line.strip()
    if line.startswith("Monitors: "):
      if monitorCount != -1:
        raise Exception("two monitor counts found")
      try:
        monitorCount = int(line.replace("Monitors: ","").strip())
      except:
        print("invalid monitor output, not in format")
        print("expected format:")
        print("Monitors: {count}")
        print("got:")
        print(line)
      continue
  monitors:list[Monitor] = []
  if len(lines[1:]) != monitorCount:
    raise Exception("monitor count not consistent")
  for monitorLine in lines[1:]:
    monitors.append(Monitor(monitorLine))
  return monitors


if __name__ == "__main__":
  mon = getScreenData()
  for m in mon:
    print(str(m))