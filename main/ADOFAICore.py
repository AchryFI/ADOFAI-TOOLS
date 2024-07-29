import os, _io, sys, time, re, json
from tkinter import messagebox

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
      if self.data[self.index] == " " or self.data[self.index] == "\t": self.index += 1
      else: break
  def task_type(self) -> str:
    return self.task_string()
  def task_string(self) -> str:
    self.index += 1
    this_result = ""
    while 1:
      if self.index >= self.max_index: break;
      if self.data[self.index] == "\\": 
        this_result += self.data[self.index]
        this_result += self.data[self.index+1]
        self.index += 2
      elif self.data[self.index] == "\n": 
        this_result += "\\n"
        self.index += 1
      elif self.data[self.index] == "\t": 
        this_result += "\\t"
        self.index += 1
      elif self.data[self.index] == "\"":
        self.index += 1
        break
      else:
        this_result += self.data[self.index]
        self.index += 1
    return this_result
  def task_number(self) -> float|int:
    this_result = ""
    is_float = False;
    while 1:
      if self.data[self.index] in "-0123456789": 
        this_result += self.data[self.index]
        self.index += 1
      elif self.data[self.index] == ".":
        this_result += self.data[self.index]
        is_float = True
        self.index += 1
      else: 
        break
    return float(this_result) if is_float else int(this_result)
  def task_array(self) -> list:
    self.index += 1
    this_result = []
    while 1:
      self.skip_space_and_tab()
      if self.data[self.index] == "\"": 
        this_result.append(self.task_string())
      elif self.data[self.index] in "-0123456789": 
        this_result.append(self.task_number())
      elif self.data[self.index:self.index+5] == "false" and t != None:
        this_result.append(False)
      elif self.data[self.index:self.index+4] == "true" and t != None:
        this_result.append(True)
      elif self.data[self.index] == "[": 
        this_result.append(self.task_array())
      elif self.data[self.index] == "{": 
        this_result.append(self.task_object())
      elif self.data[self.index] == "]":
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
      if self.data[self.index] == "\n": 
        self.index += 1
      elif self.data[self.index] == "\"" and t == None: 
        t = self.task_type()
      elif self.data[self.index] == "\"" and t != None:
        this_result[t] = self.task_string()
        t = None
      elif self.data[self.index] in "-0123456789" and t != None:
        this_result[t] = self.task_number()
        t = None
      elif self.data[self.index:self.index+5] == "false" and t != None:
        this_result[t] = False
        t = None
      elif self.data[self.index:self.index+4] == "true" and t != None:
        this_result[t] = True
        t = None
      elif self.data[self.index] == "[" and t != None:
        this_result[t] = self.task_array()
        t = None
      elif self.data[self.index] == "{" and t != None:
        this_result[t] = self.task_object()
        t = None
      elif self.data[self.index] == "}" and t == None:
        self.index += 1
        break
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