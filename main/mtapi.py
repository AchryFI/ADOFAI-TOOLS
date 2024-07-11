import os, _io, sys, time, re, json
from tkinter import messagebox

__version__ = 0x010103FF

class log:
  """
    日志信息 包含了Version-1与Version-2的集合
  """
  def __init__(self):
    """
      用于保存非静态变量
      params: 
        self (log)
    """
    self.logV1 = None
    self.logV2 = None
    pass
  def reload(self):
    """
      重载并保存日志信息
      params: 
        self (log)
    """
    self.logV1.flush()
    self.logV2.flush()
    pass
  def new(fileNameV1:str, fileNameV2:str, encoding:str="UTF-8"):
    """
      创建新的日志
      params:
        fileNameV1 (str): 日志V1的文件名称
        fileNameV2 (str): 日志V2的文件名称
        encoding (str, "UTF-8"): 日志所用的编码器
      return:
        log: 日志创建完成后的动态数据 
    """
    new_log = log()
    if not os.path.exists("log"): os.system("mkdir log")
    new_log.logV1 = open("log\\%s.mt-log"%fileNameV1,"a", encoding=encoding)
    new_log.logV2 = open("log\\%s.mt-log"%fileNameV2,"a", encoding=encoding)
    return new_log
  def write(self, w:str, level:int=1):
    """
      往日志中写入内容后并执行reload
      params: 
        self (log)
        w (str): 写入的文本内容
        level (int, 1): 日志的等级
    """
    logV1.write(self.logV1, w, level)
    logV2.write(self.logV2, w, level)
    self.reload()
    pass
  def read(self, escaping=False):
    """
      往日志中读取内容 并且转义 换行 -> \'\\n\\t\'
      params: 
        self (log)
        escaping (bool, False): 允许转义所有内容
      return:
        list(str, str): 读取到的内容
    """
    return [logV1.read(self.logV1, escaping), logV2.read(self.logV2, escaping)]
  pass
class logV1:
  def write(this, w:str, level:int=1):
    """
      往日志中写入内容 如果this类型不符或level值错误则会弹出异常
      params: 
        this (_io.TextIOWrapper)
        w (str): 写入的文本内容
        level (int, 1): 日志的等级
    """
    if type(this) != _io.TextIOWrapper: raise TypeError("\"this\" variables not is _io.TextIOWrapper")
    if   level == 1: level = "INFO"
    elif level == 2: level = "WARN"
    elif level == 3: level = "ERROR"
    elif level == 4: level = "FAIL"
    elif level == 5: level = "DEBUG"
    elif level == 6: level = "DEFINDED"
    else: raise(ValueError("Level Value UnDefind"))#bfnrt
    w = w.replace("\\", "\\\\").replace("\b", "\\b").replace("\f", "\\f").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    this.write("[ModsTag/%s]: %s\n"%(level, w));
  def read(this, escaping=False):
    """
      往日志中写入内容 如果this类型不符或level值错误则会弹出异常
      params: 
        this (_io.TextIOWrapper)
        escaping (bool, False): 允许转义所有内容
    """
    if type(this) != _io.TextIOWrapper: print("this variables not is _io.TextIOWrapper")
    result = open(this.name, "r", encoding=this.encoding).read()
    if escaping:
      return result.replace("\\\\", "\\").replace("\\b", "\b").replace("\\f", "\f").replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t")
    else:
      return result.replace("\\n", "\n\t")
  pass
class logV2:
  def write(this, w:str, level:int=1):
    """
      往日志中写入内容 如果this类型不符或level值错误则会弹出异常
      params: 
        this (_io.TextIOWrapper)
        w (str): 写入的文本内容
        level (int, 1): 日志的等级
    """
    if type(this) != _io.TextIOWrapper: raise TypeError("\"this\" variables not is _io.TextIOWrapper")
    if   level == 1: level = "INFO"
    elif level == 2: level = "WARN"
    elif level == 3: level = "ERROR"
    elif level == 4: level = "FAIL"
    elif level == 5: level = "DEBUG"
    elif level == 6: level = "DEFINDED"
    else: raise(ValueError("Level Value UnDefind"))
    w = w.replace("\\", "\\\\").replace("\b", "\\b").replace("\f", "\\f").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t").replace("\"", "\\\"")
    this.write("[ModsTag.%s(), %s, \"%s\"]\n"%(level, int(time.time()), w));
  def read(this, escaping=False):
    """
      往日志中写入内容 如果this类型不符或level值错误则会弹出异常
      params: 
        this (_io.TextIOWrapper)
        escaping (bool, False): 允许转义所有内容
    """
    if type(this) != _io.TextIOWrapper: print("this variables not is _io.TextIOWrapper")
    result = open(this.name, "r", encoding=this.encoding).read()
    if escaping:
      return result.replace("\\\\", "\\").replace("\\b", "\b").replace("\\f", "\f").replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t").replace("\\\"", "\"")
    else:
      return result.replace("\\n", "\n\t")
  pass

class language:
  def __init__(self):
    """
      用于保存非静态变量
      params: 
        self (language)
    """
    self.mtl = None
    self.not_find_json = ""
    self.lang = None;
    self.locale = {"2052":"zh_cn", "1033":"en_us", "1042":"kr"}
    pass
  def get(self, data:str, repl:object="", start:int=0):
    """
      用于保存非静态变量
      params: 
        self (language)
        data (str): 要获取的格式化文本 
        repl (object, ""): 转换的内容 支持自动检测类型并且转换 
        data (int, 0): 定义"替换"从哪个数字开始
      return: 
        data (except.str)
        result (str)
    """
    from win32api import GetSystemDefaultLangID
    if (self.lang == None): self.lang = self.locale[str(GetSystemDefaultLangID())]
    if not os.path.exists("lang.json"):
      self.mtl.write("Can't read the lang file.If the language file does exist and it still shows this error, contact the developer, or try the following method: \n\nput the program in the English path (without special symbols)")
      return data
    try: result = json.loads(open("lang.json", 'r', encoding="UTF-8").read())
    except:
      self.mtl.write("file data can't convert to json, please re-download lang.json and pause to \"%s\""%__file__, 4)
      return data
    try: 
      for i in [self.lang]+data.split("."): result = result[i]
    except:
      self.mtl.write("No get lang \"%s\" as lang.json. Please check if your language file is corrupted, and if that doesn't work, contact the developer"%data, 4)
      return data
    result = str(result)
    if type(repl) != tuple and type(repl) != list: repl = [repl]
    elif type(repl) == tuple: repl = list(repl)
    for value in range(start, len(repl)+start):
      result = result.replace("${%s}"%value, str(repl[value-start]))
    return result
class string_convert:
  """
    private content!
  """
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