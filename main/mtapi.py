import os, _io, sys, time, re, json
from tkinter import messagebox

class log:
  def new(fileNameV1:str, fileNameV2:str, encoding:str="UTF-8"):
    if not os.path.exists("log"): 
      os.system("mkdir log")
      return (open("log\\%s.mt-log"%fileNameV1,"w", encoding=encoding), open("log\\%s.mt-log"%fileNameV2,"w", encoding=encoding));
    else: 
      return (open("log\\%s.mt-log"%fileNameV1,"a", encoding=encoding), open("log\\%s.mt-log"%fileNameV2,"a", encoding=encoding));
  def inp(w:str, this:tuple, level:int=1):
    if type(this) != tuple: print("this variables not is tuple")
    logV1.inp(w, this[0], level)
    logV2.inp(w, this[1], level)
  def out(this:tuple, escaping=False):
    if type(this) != tuple: print("this variables not is tuple")
    V1 = logV1.out(this[0], escaping)
    V2 = logV2.out(this[1], escaping)
    return [V1, V2]
  pass
class logV1:
  def new(fileName:str, encoding:str="UTF-8"):
    if not os.path.exists("log"): 
      os.system("mkdir log")
      return open("log\\%s.mt-log"%fileName,"w", encoding=encoding);
    else: 
      return open("log\\%s.mt-log"%fileName,"a", encoding=encoding);
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
  def new(fileName:str, encoding:str="UTF-8"):
    if not os.path.exists("log"): 
      os.system("mkdir log")
      return open("log\\%s.mt-log"%fileName,"w", encoding=encoding);
    else: 
      return open("log\\%s.mt-log"%fileName,"a", encoding=encoding);
  def inp(w:str, this:str, level:int=1):
    if type(this) != _io.TextIOWrapper: print("this variables not is _io.TextIOWrapper")
    if   level == 1: level = "INFO"
    elif level == 2: level = "WARN"
    elif level == 3: level = "ERROR"
    elif level == 4: level = "FAIL"
    elif level == 5: level = "DEBUG"
    elif level == 6: level = "DEFINDED"
    else: raise(TypeError("Level Value UnDefind"))#bfnrt
    w = w.replace("\\", "\\\\").replace("\b", "\\b").replace("\f", "\\f").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t").replace("\"", "\\\"")
    return this.write("[ModsTag.%s(), %s, \"%s\"]\n"%(level, int(time.time()), w));
  def out(this:str, escaping=False):
    if type(this) != _io.TextIOWrapper: print("this variables not is _io.TextIOWrapper")
    r = open(this.name, "r", encoding=this.encoding).read()
    ### print(r)
    if escaping:
      r = r.replace("\\\\", "\\").replace("\\b", "\b").replace("\\f", "\f").replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t").replace("\\\"", "\"")
    else:
      r = r.replace("\\n", "\n\t")
    return r
  pass

class language:
  def repls(data:str, repl:tuple, start:int=0):
    for value in range(start, len(repl)+start):
      data = language.repl(data, value, repl[value-start])
    return data
  def repl(data:str, value:int, to:str):
      to = str(to)
      return data.replace("${%s}"%value, to)
  def lang(data:str):
      if not os.path.exists("lang.json"):
          messagebox.showerror("error", "Can't read the lang file.If the language file does exist and it still shows this error, contact the developer, or try the following method: \n\nput the program in the English path (without special symbols)")
          sys.exit();
      array = data.split(".")
      try:
          js = json.loads(open("lang.json", 'r', encoding="UTF-8").read())
      except Exception as e:
          messagebox.showerror("error", "file data can't convert to json, please re-download lang.json and pause to \"%s\""%__file__)
          mtlog.inp("file data can't convert to json, please re-download lang.json and pause to \"%s\""%__file__, mtl, 4)
          return data
      try:
          for i in js["language"]:
              for key,val in i.items():
                  if js["getNowLanguage"] == key:
                      ret = val
      except:
          messagebox.showerror('error', traceback.print_exc())

      try: 
          for i in array: ret = ret[i]
      except Exception as e:
          messagebox.showerror('error',"No get lang \"%s\" as lang.json. Please check if your language file is corrupted, and if that doesn't work, contact the developer"%string)
          mtlog.inp("No get lang \"%s\" as lang.json. Please check if your language file is corrupted, and if that doesn't work, contact the developer"%string, mtl, 4)
          return ""
      return str(ret)
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
        if (string_convert.remove_quo(string_list[1])["success"]):
          result["match"].append(string_convert.remove_quo(ii)["match"]);
        elif (string_convert.search(r"false", string_list[1])["success"]):
          result["match"].append(False);
        elif (string_convert.search(r"true", string_list[1])["success"]):
          result["match"].append(True);
        elif (string_convert.search(r"null", string_list[1])["success"]):
          result["match"].append(None);
        elif (string_convert.match(r"(\-?)\d+\.\d+", ii)["success"]):
          result["match"].append(float(ii));
        elif (string_convert.match(r"(\-?)\d+", ii)["success"]):
          result["match"].append(int(ii));
      pass;
    elif (string_convert.search(r"false", string_list[1])["success"]):
      result["match"] = False;
    elif (string_convert.search(r"true", string_list[1])["success"]):
      result["match"] = True;
    elif (string_convert.search(r"null", string_list[1])["success"]):
      result["match"] = None;
    elif (string_convert.search(r"(\-?)\d+\.\d+", string_list[1])["success"]):
      result["match"] = float(string_list[1]);
    elif (string_convert.search(r"(\-?)\d+", string_list[1])["success"]):
      result["match"] = int(string_list[1]);
    else:
      result["success"] = False;
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
      "SetObject",
      "AddObject",
      "SetFilterAdvanced",
      "SetFloorIcon",
      "AnimateTrack",
      "MoveTrack",
      "MoveDecorations",
      "SetText",
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
      "ScreenTile",
      "ScreenScroll",
      "RepeatEvents",
      "SetConditionalEvents",
      "AddDecoration",
      "AddText"
    ]
    # self.action = []
    # self.decorations = []