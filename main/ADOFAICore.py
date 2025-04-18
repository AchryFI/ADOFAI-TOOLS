import os, _io, sys, re, json

class adofai_level_data:
  class exception(Exception):
    def __init__(self, message):
      super().__init__(message)

  def __init__(self, data):
    self.data = data
    self.index = 0
    self.max_index = len(data)-1
    self.success = False
    self.type = ""
    self.result = {}
  def encode(self) -> str:
    jsonDecode = self.result;
    output = ""
    output += "{\n\t"+json.dumps({self.type : jsonDecode[self.type]}, separators=[", ", ": "])[:-1][1:]+", ";
    output += json.dumps({"settings": jsonDecode["settings"]}, indent="\t", separators=[", ", ": "])[:-2][1:]+", \n\t\"actions\": [ \n";
    for out in jsonDecode["actions"]:
      output += "\t\t";
      output += json.dumps(out, separators=[", ", ": "])+",\n";
      pass;
    output = output[:-2]+"\n\t], \n\t\"decorations\": [ \n";
    for out in jsonDecode["decorations"]:
      output += "\t\t";
      output += json.dumps(out, separators=[", ", ": "])+",\n";
      pass;
    output = output[:-2]+"\n\t]\n}";
    return output;
  def new(file:str) -> object:
    return adofai_level_data(open(file, "r", encoding="UTF-8-SIG").read())
  def decode(self) -> None:
    if self.data[0] != "{": raise adofai_level_data.exception("it not adofai syntax")
    self.result = self.task_object()
    if not "decorations" in self.result: self.result["decorations"] = []
    if not "actions" in self.result: self.result["actions"] = []
    if "pathData" in self.result: self.type = "pathData"
    elif "angleData" in self.result: self.type = "angleData"
    else: raise adofai_level_data.exception("can't find tile data type")
    if self.index >= self.max_index: pass
  def skip_space_and_tab(self) -> None:
    while 1:
      i = self.data[self.index]
      if i == " " or i == "\t": self.index += 1
      else: break
  def task_type(self) -> str:
    return self.task_string()
  def task_string(self) -> str:
    self.index += 1
    this_result = ""
    while 1:
      i = self.data[self.index]
      if self.index >= self.max_index: break;
      if i == "\\":
        this_result += self.data[self.index:self.index+1]
        self.index += 2
      elif i == "\n": 
        this_result += "\\n"
        self.index += 1
      elif i == "\t": 
        this_result += "\\t"
        self.index += 1
      elif i == "\"":
        self.index += 1
        break
      else:
        this_result += i
        self.index += 1
    return this_result
  def task_number(self) -> float|int:
    this_result = ""
    is_float = False;
    while 1:
      i = self.data[self.index]
      if i in "-0123456789": 
        this_result += i
      elif i == "." or i == "E" or i == "e" or i == "+":
        this_result += i
        is_float = True
      else: 
        break
      self.index += 1
    return float(this_result) if is_float else int(this_result)
  def task_array(self) -> list:
    self.index += 1
    this_result = []
    while 1:
      self.skip_space_and_tab()
      i = self.data[self.index] 
      if i == "\"": 
        this_result.append(self.task_string())
      elif i in "-0123456789": 
        this_result.append(self.task_number())
      elif self.data[self.index:self.index+5] == "false":
        this_result.append(False)
        self.index += 5
      elif self.data[self.index:self.index+4] == "true":
        this_result.append(True)
        self.index += 4
      elif i == "[": 
        this_result.append(self.task_array())
      elif i == "{": 
        this_result.append(self.task_object())
      elif i == "]":
        self.index += 2
        break
      else:
        self.index += 1
    return this_result
  def task_object(self) -> dict:
    self.index += 1
    t = None
    this_result = {}
    while 1:
      self.skip_space_and_tab()
      i = self.data[self.index] 
      if i == "\n": 
        self.index += 1
      elif t == None: 
        if i == "\"": 
          t = self.task_type()
        elif i == "}":
          self.index += 1
          break
        else: self.index += 1
      else:
        if i == "\"":
          this_result[t] = self.task_string()
          t = None
        elif i in "-0123456789":
          this_result[t] = self.task_number()
          t = None
        elif self.data[self.index:self.index+5] == "false":
          this_result[t] = False
          self.index += 5
          t = None
        elif self.data[self.index:self.index+4] == "true":
          this_result[t] = True
          self.index += 4
          t = None
        elif i == "[":
          this_result[t] = self.task_array()
          t = None
        elif i == "{":
          this_result[t] = self.task_object()
          t = None
        else: self.index += 1
    return this_result
  pass
class adofai_const:
  def __init__(self):
    self.Rad2Deg = 57.295780181884766
    self.effect = [
      "AddDecoration",
      "MoveDecorations",
      "AddText",
      "SetText",
      "SetObject",
      "AddObject",
      "SetDefaultText",
      "SetFrameRate",
      "SetFilterAdvanced",
      "SetFloorIcon",
      "AnimateTrack",
      "MoveTrack",
      "PositionTrack",
      "RecolorTrack",
      "ColorTrack",
      "CustomBackground",
      "Flash",
      "MoveCamera",
      "SetFilter",
      "HallOfMirrors",
      "ShakeScreen",
      "Bloom",
      "ScalePlanets",
      "ScreenTile",
      "ScreenScroll",
      "RepeatEvents",
      "SetConditionalEvents"
    ]
    # self.action = []
    # self.decorations = []

if __name__ == '__main__':
  import time
  res = 0;
  for i in range(20):
    s = time.time();
    convert = adofai_level_data.new("18616.adofai")
    convert.decode()
    e = time.time();
    res += e-s
    print(e-s)
  print()
  print(res/20)

