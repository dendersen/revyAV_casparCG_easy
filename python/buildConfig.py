from configParser import getConfig, xmlEntry, saveConfig
from getScreens import Monitor, getScreenData
import argparse

def setChild(parent:xmlEntry, childName:str, childValue:str):
  child = parent.getChild(childName)
  if child:
    child.text = childValue
  else:
    parent.addChild(xmlEntry(childName, {}, childValue))

def createChannel(screen:xmlEntry, videoMode:str = "720p5000", isMain:bool = False) -> xmlEntry:
  consumers = xmlEntry("consumers", {}, "")
  consumers.addChild(screen)
  if isMain:
    # Set system audio for main consumer
    setChild(consumers, "system-audio", "")
  
  channel = xmlEntry("channel", {}, "")
  setChild(channel, "video-mode", videoMode)
  channel.addChild(consumers)
  
  return channel

def createScreenEntry(screen:Monitor, fullScreen:bool = True) -> xmlEntry:
  entry = xmlEntry("screen", {}, "")
  setChild(entry, "width", str(screen.shape[0]))
  setChild(entry, "height", str(screen.shape[1]))
  setChild(entry, "x", str(screen.offset[0]))
  setChild(entry, "y", str(screen.offset[1]))
  if fullScreen:
    setChild(entry, "borderless", "true")
  return entry

if __name__ == "__main__":
  print("WARNING: this will overwrite existing fullscreen settings")
  config = getConfig()
  screens = getScreenData()
  doFulscreen = len(screens) > 1

  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--screenCount", type=int, help="Number of screens to set up for fullscreen", default=len(screens) - 1 if len(screens) != 1 else 1)
  parser.add_argument("-n", "--noFullscreen", action="store_true", help="Do not set up screens as fullscreen")
  args = parser.parse_args()
  screenCount = args.screenCount
  if screenCount == len(screens):
    print("WARNING: screen count exceeds unused screens")
    userInput = input("type y to continue ")
    if userInput.lower().strip() != "y":
      raise Exception("User aborted")
  if screenCount > len(screens):
    raise Exception("Screen count exceeds available screens")
  if screenCount <= 0:
    raise Exception("Screen count must be greater than 0")
  if args.noFullscreen:
    doFulscreen = False

  if doFulscreen:
    print("WARNING: this program will set up the config file for fullscreen screens")

  if screenCount < len(screens):
    print("please select a screen that should not be setup")
  while screenCount < len(screens):
    print("Current screens:")
    for i in range(len(screens)):
      print(f"{screens[i]}")
    userInput = input("Select screen index to exclude: ")
    try:
      excludeIndex = int(userInput)
      for i in range(len(screens)):
        if screens[i].id == excludeIndex:
          screens.pop(i)
          break
      else:
        print("Invalid index")
    except ValueError:
      print("Invalid input")
  
  channels = config.getChild("channels")
  if channels is None:
    channels = xmlEntry("channels", {}, "")
    config.addChild(channels)
  channels.removeChildren("channel")
  for i in range(screenCount):
    channel = createChannel(createScreenEntry(screens[i], fullScreen=doFulscreen), isMain=(i == 0))
    channels.addChild(channel)
  
  saveConfig(config)