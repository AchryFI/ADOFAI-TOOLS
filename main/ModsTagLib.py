import os, _io, sys, time, re, json, requests
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
class bilibiliDownload:
  def __init__(self, url=""):
    self.url = url
    self.session = requests.session()
    self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37", "Referer": "https://www.bilibili.com"}
    self.data = None
    self.selected = None

  def get(self, _try:int=1):
    result = []
    if _try <= 0: raise ValueError("_try(%s)"%_try)
    for i in range(_try):
      resp = self.session.get(self.url, headers=self.headers)
      try:
        play_info = json.loads(re.findall(r"<script>window\.__playinfo__=(.*?)</script>",resp.text)[0])["data"]["dash"]
      except: 
        play_info = json.loads(re.findall(r"playurlSSRData = (.*\n)",resp.text)[0])["result"]["video_info"]["dash"]

      a_data = {}
      a_result = []
      for audio_data in play_info["audio"]:
        a_data = {}
        a_data["dw_url"] = audio_data["baseUrl"]
        a_data["bandwidth"] = audio_data["bandwidth"]
        a_len = 0
        for a in range(len(a_result)):
          if a_result[a]["bandwidth"] > a_data["bandwidth"]:
            a_len = a+1
        a_result.insert(a_len, a_data)

      v_data = {}
      v_result = []
      for video_data in play_info["video"]:
        v_data = {}
        v_data["bandwidth"] = video_data["bandwidth"]
        v_data["dw_url"] = video_data["baseUrl"]
        v_data["frame_data"] = [video_data["width"], video_data["height"], float(video_data["frameRate"])]
        v_len = 0
        for v in range(len(v_result)):
          if v_result[v]["bandwidth"] > v_data["bandwidth"]:
            v_len = v+1
        v_result.insert(v_len, v_data)
      result.append({"video":v_result,"audio":a_result})
    self.data = result
    
  def get_(self, _data):
    play_info = json.loads(_data)["data"]["dash"]

    a_data = {}
    a_result = []
    for audio_data in play_info["audio"]:
      a_data = {}
      a_data["dw_url"] = audio_data["baseUrl"]
      a_data["bandwidth"] = audio_data["bandwidth"]
      a_len = 0
      for a in range(len(a_result)):
        if a_result[a]["bandwidth"] > a_data["bandwidth"]:
          a_len = a+1
      a_result.insert(a_len, a_data)

    v_data = {}
    v_result = []
    for video_data in play_info["video"]:
      v_data = {}
      v_data["bandwidth"] = video_data["bandwidth"]
      v_data["dw_url"] = video_data["baseUrl"]
      v_data["frame_data"] = [video_data["width"], video_data["height"], float(video_data["frameRate"])]
      v_len = 0
      for v in range(len(v_result)):
        if v_result[v]["bandwidth"] > v_data["bandwidth"]:
          v_len = v+1
      v_result.insert(v_len, v_data)
    self.data = [{"video":v_result,"audio":a_result}]

  def select(self, default:list=None):
    if default == None:
      for get_video in range(len(self.data[0]["video"])):
        print("%s:\n  带宽: %s\n  视频数据: %s"%(get_video+1, self.data[0]["video"][get_video]["bandwidth"],self.data[0]["video"][get_video]["frame_data"]))
      video_select = int(input("\n请选择视频id: "))
      print("\r")
      for get_audio in range(len(self.data[0]["audio"])):
        print("%s:\n  带宽: %s"%(get_audio+1, self.data[0]["audio"][get_audio]["bandwidth"]))
      audio_select = int(input("\n请选择音频id: "))
    else:
     video_select = default[0]+1
     audio_select = default[1]+1
    self.selected = [video_select-1, audio_select-1]

  def download(self):
    audio_content_result = ""
    video_content_result = ""
    audio_content_max = 0
    video_content_max = 0
    print("尝试下载次数: %s"%len(self.data))
    print("尝试下载中...")
    for get in self.data:
      print("  audio: ",end="")
      audio_content = self.session.get(get["audio"][self.selected[1]]["dw_url"],headers=self.headers).content
      if (len(audio_content) > audio_content_max and len(audio_content) > 4096):
        audio_content_result = audio_content
        audio_content_max = len(audio_content)
      print("success")

      print("  video: ",end="")
      video_content = self.session.get(get["video"][self.selected[0]]["dw_url"],headers=self.headers).content
      if (len(video_content) > video_content_max and len(video_content) > 4096):
        video_content_result = video_content
        video_content_max = len(video_content)
      print("success")
    print("下载完成")
    
    return [video_content,audio_content]