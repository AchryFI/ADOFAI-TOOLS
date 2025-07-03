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
    self.all_keys = ('None', 'Backspace', 'Delete', 'Tab', 'Clear', 'Return', 'Pause', 'Escape', 'Space', 'Keypad0', 'Keypad1', 'Keypad2', 'Keypad3', 'Keypad4', 'Keypad5', 'Keypad6', 'Keypad7', 'Keypad8', 'Keypad9', 'KeypadPeriod', 'KeypadDivide', 'KeypadMultiply', 'KeypadMinus', 'KeypadPlus', 'KeypadEnter', 'KeypadEquals', 'UpArrow', 'DownArrow', 'RightArrow', 'LeftArrow', 'Insert', 'Home', 'End', 'PageUp', 'PageDown', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'Alpha0', 'Alpha1', 'Alpha2', 'Alpha3', 'Alpha4', 'Alpha5', 'Alpha6', 'Alpha7', 'Alpha8', 'Alpha9', 'Exclaim', 'DoubleQuote', 'Hash', 'Dollar', 'Percent', 'Ampersand', 'Quote', 'LeftParen', 'RightParen', 'Asterisk', 'Plus', 'Comma', 'Minus', 'Period', 'Slash', 'Colon', 'Semicolon', 'Less', 'Equals', 'Greater', 'Question', 'At', 'LeftBracket', 'Backslash', 'RightBracket', 'Caret', 'Underscore', 'BackQuote', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'LeftCurlyBracket', 'Pipe', 'RightCurlyBracket', 'Tilde', 'Numlock', 'CapsLock', 'ScrollLock', 'RightShift', 'LeftShift', 'RightControl', 'LeftControl', 'RightAlt', 'LeftAlt', 'LeftApple', 'LeftWindows', 'RightApple', 'RightWindows', 'AltGr', 'Help', 'Print', 'SysReq', 'Break', 'Menu', 'Mouse0', 'Mouse1', 'Mouse2', 'Mouse3', 'Mouse4', 'Mouse5', 'Mouse6', 'JoystickButton0', 'JoystickButton1', 'JoystickButton2', 'JoystickButton3', 'JoystickButton4', 'JoystickButton5', 'JoystickButton6', 'JoystickButton7', 'JoystickButton8', 'JoystickButton9', 'JoystickButton10', 'JoystickButton11', 'JoystickButton12', 'JoystickButton13', 'JoystickButton14', 'JoystickButton15', 'JoystickButton16', 'JoystickButton17', 'JoystickButton18', 'JoystickButton19', 'Joystick1Button0', 'Joystick1Button1', 'Joystick1Button2', 'Joystick1Button3', 'Joystick1Button4', 'Joystick1Button5', 'Joystick1Button6', 'Joystick1Button7', 'Joystick1Button8', 'Joystick1Button9', 'Joystick1Button10', 'Joystick1Button11', 'Joystick1Button12', 'Joystick1Button13', 'Joystick1Button14', 'Joystick1Button15', 'Joystick1Button16', 'Joystick1Button17', 'Joystick1Button18', 'Joystick1Button19', 'Joystick2Button0', 'Joystick2Button1', 'Joystick2Button2', 'Joystick2Button3', 'Joystick2Button4', 'Joystick2Button5', 'Joystick2Button6', 'Joystick2Button7', 'Joystick2Button8', 'Joystick2Button9', 'Joystick2Button10', 'Joystick2Button11', 'Joystick2Button12', 'Joystick2Button13', 'Joystick2Button14', 'Joystick2Button15', 'Joystick2Button16', 'Joystick2Button17', 'Joystick2Button18', 'Joystick2Button19', 'Joystick3Button0', 'Joystick3Button1', 'Joystick3Button2', 'Joystick3Button3', 'Joystick3Button4', 'Joystick3Button5', 'Joystick3Button6', 'Joystick3Button7', 'Joystick3Button8', 'Joystick3Button9', 'Joystick3Button10', 'Joystick3Button11', 'Joystick3Button12', 'Joystick3Button13', 'Joystick3Button14', 'Joystick3Button15', 'Joystick3Button16', 'Joystick3Button17', 'Joystick3Button18', 'Joystick3Button19', 'Joystick4Button0', 'Joystick4Button1', 'Joystick4Button2', 'Joystick4Button3', 'Joystick4Button4', 'Joystick4Button5', 'Joystick4Button6', 'Joystick4Button7', 'Joystick4Button8', 'Joystick4Button9', 'Joystick4Button10', 'Joystick4Button11', 'Joystick4Button12', 'Joystick4Button13', 'Joystick4Button14', 'Joystick4Button15', 'Joystick4Button16', 'Joystick4Button17', 'Joystick4Button18', 'Joystick4Button19', 'Joystick5Button0', 'Joystick5Button1', 'Joystick5Button2', 'Joystick5Button3', 'Joystick5Button4', 'Joystick5Button5', 'Joystick5Button6', 'Joystick5Button7', 'Joystick5Button8', 'Joystick5Button9', 'Joystick5Button10', 'Joystick5Button11', 'Joystick5Button12', 'Joystick5Button13', 'Joystick5Button14', 'Joystick5Button15', 'Joystick5Button16', 'Joystick5Button17', 'Joystick5Button18', 'Joystick5Button19', 'Joystick6Button0', 'Joystick6Button1', 'Joystick6Button2', 'Joystick6Button3', 'Joystick6Button4', 'Joystick6Button5', 'Joystick6Button6', 'Joystick6Button7', 'Joystick6Button8', 'Joystick6Button9', 'Joystick6Button10', 'Joystick6Button11', 'Joystick6Button12', 'Joystick6Button13', 'Joystick6Button14', 'Joystick6Button15', 'Joystick6Button16', 'Joystick6Button17', 'Joystick6Button18', 'Joystick6Button19', 'Joystick7Button0', 'Joystick7Button1', 'Joystick7Button2', 'Joystick7Button3', 'Joystick7Button4', 'Joystick7Button5', 'Joystick7Button6', 'Joystick7Button7', 'Joystick7Button8', 'Joystick7Button9', 'Joystick7Button10', 'Joystick7Button11', 'Joystick7Button12', 'Joystick7Button13', 'Joystick7Button14', 'Joystick7Button15', 'Joystick7Button16', 'Joystick7Button17', 'Joystick7Button18', 'Joystick7Button19', 'Joystick8Button0', 'Joystick8Button1', 'Joystick8Button2', 'Joystick8Button3', 'Joystick8Button4', 'Joystick8Button5', 'Joystick8Button6', 'Joystick8Button7', 'Joystick8Button8', 'Joystick8Button9', 'Joystick8Button10', 'Joystick8Button11', 'Joystick8Button12', 'Joystick8Button13', 'Joystick8Button14', 'Joystick8Button15', 'Joystick8Button16', 'Joystick8Button17', 'Joystick8Button18', 'Joystick8Button19')
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
    self.all_margins = [ 
      "TooEarly",
      "VeryEarly",
      "EarlyPerfect",
      "Perfect",
      "LatePerfect",
      "VeryLate",
      "TooLate",
      "Multipress",
      "FailMiss",
      "FailOverload",
      "Auto",
      "OverPress"
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

