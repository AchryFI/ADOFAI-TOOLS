import os, _io

class mtlog:
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
    return this.write("[ModsTag/%s]: '%s'\n"%(level, w));
  def out(this:str, escaping=False):
    if type(this) != _io.TextIOWrapper: print("this variables not is _io.TextIOWrapper")
    r = open(this.name, "r", encoding=this.encoding).read()
    print(r)
    if escaping:
      r = r.replace("\\\\", "\\").replace("\\b", "\b").replace("\\f", "\f").replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t")
    return r
  pass
