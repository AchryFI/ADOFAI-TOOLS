import os, _io, sys, time, re, json
from tkinter import messagebox

class log:
  def __init__(self):
    self.logV1 = None
    self.logV2 = None
    pass
  def reload(self):
    self.logV1.flush()
    self.logV2.flush()
    pass
  def new(fileNameV1:str, fileNameV2:str, encoding:str="UTF-8"):
    new_log = log()
    if not os.path.exists("log"): os.system("mkdir log")
    new_log.logV1 = open("log\\%s.mt-log"%fileNameV1,"a", encoding=encoding)
    new_log.logV2 = open("log\\%s.mt-log"%fileNameV2,"a", encoding=encoding)
    return new_log
  def inp(self, w:str, level:int=1):
    logV1.inp(w, self.logV1, level)
    logV2.inp(w, self.logV2, level)
    self.reload()
    pass
  def out(self, escaping=False):
    return [logV1.out(self.logV1, escaping), logV2.out(self.logV2, escaping)]
  pass
class logV1:
  def inp(w:str, this:str, level:int=1):
    if type(this) != _io.TextIOWrapper: print("this variables not is _io.TextIOWrapper")
    if   level == 1: level = "INFO"
    elif level == 2: level = "WARN"
    elif level == 3: level = "ERROR"
    elif level == 4: level = "FAIL"
    elif level == 5: level = "DEBUG"
    elif level == 6: level = "DEFINDED"
    else: raise(TypeError("Level Value UnDefind"))#bfnrt
    w = w.replace("\\", "\\\\").replace("\b", "\\b").replace("\f", "\\f").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return this.write("[ModsTag/%s]: %s\n"%(level, w));
  def out(this:str, escaping=False):
    if type(this) != _io.TextIOWrapper: print("this variables not is _io.TextIOWrapper")
    r = open(this.name, "r", encoding=this.encoding).read()
    ### print(r)
    if escaping:
      r = r.replace("\\\\", "\\").replace("\\b", "\b").replace("\\f", "\f").replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t")
    else:
      r = r.replace("\\n", "\n\t")
    return r
  pass
class logV2:
  def inp(w:str, this:str, level:int=1):
    if type(this) != _io.TextIOWrapper: print("this variables not is _io.TextIOWrapper")
    if   level == 1: level = "INFO"
    elif level == 2: level = "WARN"
    elif level == 3: level = "ERROR"
    elif level == 4: level = "FAIL"
    elif level == 5: level = "DEBUG"
    elif level == 6: level = "DEFINDED"
    else: raise(TypeError("Level Value UnDefind"))
    w = w.replace("\\", "\\\\").replace("\b", "\\b").replace("\f", "\\f").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t").replace("\"", "\\\"")
    return this.write("[ModsTag.%s(), %s, \"%s\"]\n"%(level, int(time.time()), w));
  def out(this:str, escaping=False):
    if type(this) != _io.TextIOWrapper: print("this variables not is _io.TextIOWrapper")
    r = open(this.name, "r", encoding=this.encoding).read()
    if escaping:
      return r.replace("\\\\", "\\").replace("\\b", "\b").replace("\\f", "\f").replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t").replace("\\\"", "\"")
    else:
      return r.replace("\\n", "\n\t")
  pass

class language:
  def __init__(self):
    self.mtl = None
    self.not_find_json = ""
    self.lang = None;
    self.locale = {"2052":"zh_cn", "1033":"en_us", "1042":"kr"}
    pass
  def get(self, data:str, repl:object="", start:int=0):
      from win32api import GetSystemDefaultLangID
      if (self.lang == None): self.lang = self.locale[str(GetSystemDefaultLangID())]
      if not os.path.exists("lang.json"):
        messagebox.showerror("error", "Can't read the lang file.If the language file does exist and it still shows this error, contact the developer, or try the following method: \n\nput the program in the English path (without special symbols)")
        return data
      try: result = json.loads(open("lang.json", 'r', encoding="UTF-8").read())
      except:
        self.mtl.inp("file data can't convert to json, please re-download lang.json and pause to \"%s\""%__file__, 4)
        return data
      array = [self.lang]+data.split(".")
      try: 
        for i in array: result = result[i]
      except:
        self.mtl.inp("No get lang \"%s\" as lang.json. Please check if your language file is corrupted, and if that doesn't work, contact the developer"%data, 4)
        return data
      result = str(result)
      if type(repl) != tuple and type(repl) != list: repl = [repl]
      elif type(repl) == tuple: repl = list(repl)
      for value in range(start, len(repl)+start):
        result = result.replace("${%s}"%value, str(repl[value-start]))
      return result
class string_convert:
  def match(patter, string): return {"success": re.match(patter, string) != None, "match": re.match(patter, string) if re.match(patter, string) != None else ""};
  def search(patter, string): return {"success": re.search(patter, string) != None, "match": re.search(patter, string) if re.search(patter, string) != None else ""};
  def fix_comma(string): return re.sub(r",+\s*$", "", string);
  def remove_quo(string): return {"success": ("\"" in string), "match": re.sub(r"\t+", "", string, count=1)[:-1][1:] if ("\"" in string) else string};
class adofai_convert:
  def value_convert(string_list):
    result = {"success": True, "match": ""}
    if (string_convert.remove_quo(string_list[1])["success"]):
      result["match"] = string_convert.remove_quo(string_list[1])["match"];
    elif (string_convert.search(r"\[", string_list[1])["success"]):
      tmp2 = re.sub(r"\[|\]", "", string_list[1]);
      result["match"] = [];
      if (tmp2 == ""): return result;
      for ii in tmp2.split(", "): 
        if   (string_convert.remove_quo(string_list[1])["success"]):       result["match"].append(string_convert.remove_quo(ii)["match"]);
        elif (string_convert.search(r"false", string_list[1])["success"]): result["match"].append(False);
        elif (string_convert.search(r"true", string_list[1])["success"]):  result["match"].append(True);
        elif (string_convert.search(r"null", string_list[1])["success"]):  result["match"].append(None);
        elif (string_convert.match(r"(\-?)\d+\.\d+", ii)["success"]):      result["match"].append(float(ii));
        elif (string_convert.match(r"(\-?)\d+", ii)["success"]):           result["match"].append(int(ii));
      pass;
    elif (string_convert.search(r"false", string_list[1])["success"]):         result["match"] = False;
    elif (string_convert.search(r"true", string_list[1])["success"]):          result["match"] = True;
    elif (string_convert.search(r"null", string_list[1])["success"]):          result["match"] = None;
    elif (string_convert.search(r"(\-?)\d+\.\d+", string_list[1])["success"]): result["match"] = float(string_list[1]);
    elif (string_convert.search(r"(\-?)\d+", string_list[1])["success"]):      result["match"] = int(string_list[1]);
    else: result["success"] = False;
    return result;
  # main
  def dict_to_json(dict_data):
    jsonDecode = dict_data["result"];
    typ = dict_data["type"];
    output = ""
    data = {typ : jsonDecode[typ]};
    actions = {"actions": jsonDecode["actions"]};
    decorations = {"decorations": jsonDecode["decorations"]};
    settings = {"settings": jsonDecode["settings"]};
    output += "{\n\t"+json.dumps(data, separators=[", ", ": "])[:-1][1:]+", ";
    output += json.dumps(settings, indent="\t", separators=[", ", ": "])[:-2][1:]+", \n\t\"actions\": [ \n";
    for out in range(len(actions["actions"])):
      output += "\t\t";
      output += json.dumps(actions["actions"][out], separators=[", ", ": "])+",\n";
      pass;
    output = output[:-2]+"\n\t], \n\t\"decorations\": [ \n";
    for out in range(len(decorations["decorations"])):
      output += "\t\t";
      output += json.dumps(decorations["decorations"][out], separators=[", ", ": "])+",\n";
      pass;
    output = output[:-2]+"\n\t]\n}";
    return output;
  def strList_to_dict(string_data):
    is_angleData = False;
    is_pathData = False;
    is_setting = False;
    is_actions = False;
    is_decorations = False;
    jsonDecode = {};
    fixFuckYouWithNextLineBugFix = "";
    string_data.append("");
    tmp_string_data = string_data;
    string_data = [];
    for now_text in tmp_string_data:
      now_text = now_text.replace("\n", "");
      if (string_convert.match(r"\\n", now_text)["success"]):
        fixFuckYouWithNextLineBugFix += now_text;
      else:
        string_data.append(fixFuckYouWithNextLineBugFix);
        fixFuckYouWithNextLineBugFix = now_text;
        pass;
      pass;
    for now_text in string_data:
      # is type first
      if (is_setting):
        if (string_convert.match(r"\t+}", now_text)["success"]): 
          is_setting = False;
          continue;
        if (string_convert.match(r"\t+{", now_text)["success"]): continue;
        tmp = [string_convert.remove_quo(now_text.split(": ")[0]), string_convert.fix_comma(now_text.split(": ")[1])];

        if (adofai_convert.value_convert(tmp)["success"]):
          jsonDecode["settings"][tmp[0]["match"]] = adofai_convert.value_convert(tmp)["match"];
        pass;
      elif (is_actions):
        if (string_convert.match(r"\t+\](,?)", now_text)["success"]):
          is_actions = False;
          continue;
        now_text = now_text[:-2].rstrip(" ,").lstrip("\t") + "}";
        if (now_text == "}"): continue;
        jsonDecode["actions"].append(json.loads(now_text));
        pass;
      elif (is_decorations):
        if (string_convert.match(r"\t+\](,?)", now_text)["success"]):
          is_decorations = False;
          continue;
        now_text = now_text[:-2].rstrip(" ,").lstrip("\t") + "}";
        if (now_text == "}"): continue;
        jsonDecode["decorations"].append(json.loads(now_text));
        pass;

      elif (now_text == "\ufeff{" or now_text == "﻿{"):
        jsonDecode = {};
        jsonDecode["settings"] = {};
        jsonDecode["actions"] = [];
        jsonDecode["decorations"] = [];
        pass;
      elif (string_convert.match(r"\t+\"pathData\"", now_text)["success"]): 
        jsonDecode["pathData"] = re.sub(r"\"pathData\"|\"|\s|\:|,", "", now_text);
        is_pathData = True;
        pass;
      elif (string_convert.match(r"\t+\"angleData\"", now_text)["success"]):
        jsonDecode["angleData"] = [];
        is_angleData = True;
        tmp = re.sub(r"\[|\]|\"angleData\"|\s|\:", "", now_text).split(",")
        for ii in tmp:
          if (ii == ""): continue;
          try: jsonDecode["angleData"].append(int(ii))
          except: 
            try:jsonDecode["angleData"].append(float(ii));
            except: print("convertError");
            pass;
          pass;
        pass;
      elif (string_convert.match(r"\t+\"settings\"", now_text)["success"]):
        is_setting = True;
        pass;
      elif (string_convert.match(r"\t+\"actions\"", now_text)["success"]):
        is_actions = True;
        pass;
      elif (string_convert.match(r"\t+\"decorations\"", now_text)["success"]):
        is_decorations = True;
        pass;
      pass;
    return {"result": jsonDecode, "type": "angleData" if is_angleData else "pathData" if is_pathData else "None"};
  pass;
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