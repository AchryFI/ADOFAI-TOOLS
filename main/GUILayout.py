########
# 参考: 
#   ModsTagLib.Unity
#   Unity
########

#库
import os
import sys
import json
import time

import tkinter as tk
import ttkbootstrap
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename

class FrameExtend():
	def __init__(self, f):
		self.Frames = [[f,0,0]]
		self.Index = 0
		self.Row = 0
		self.Column = 0
	def LastFrame(self):
		return self.Frames[self.Index][0]
	def Frame(self):
		return self.Frames[0][0]
	def is_Passengers(self):
		return self.Index > 0
	def Add(self, frame):
		self.Frames.append([frame, 0, 0])
		self.Index += 1
	def PP(self, fill):
		self.Frames.pop()[0].pack(fill=fill)
		self.Index -= 1
		self.AddV()
	def AddH(self):
		self.Frames[self.Index][1] += 1
	def AddV(self):
		self.Frames[self.Index][2] += 1
class Instance():
	Notebook:tk.ttk.Notebook = None
	CurrnetFrame:FrameExtend = None
	Frames:list[FrameExtend] = []
	Row:int = 0

# static variables with class
Instance:Instance = Instance()
function = type(lambda:True)
# internal method
def check_type(p,t,strict=False):
	if (type(p) == t):
		return
	elif (not strict and p == None):
		return
	else:
		raise Exception("type not equals %s"%t)


# public static method
@staticmethod
def set_Notebook(nb):
	check_type(nb, tk.ttk.Notebook, True)
	Instance.Notebook = nb
	return
@staticmethod
def set_Frame(f):
	check_type(f, tk.ttk.Frame, True)
	for i in Instance.Frames:
		if (i.Frame == f):
			Instance.CurrnetFrame = i
			return
	frame = FrameExtend(f)
	Instance.Frames.append(frame)
	Instance.CurrnetFrame = frame
	return
@staticmethod
def CreateFrame(name):
	check_type(name, str, True)
	frame = ttkbootstrap.Frame(Instance.Notebook)
	Instance.Notebook.add(frame, text=name)
	set_Frame(frame)
	return frame

@staticmethod
def BeginHorizontal(f=None):
	if (f == None):
		Instance.CurrnetFrame.Add(ttkbootstrap.Frame(Instance.CurrnetFrame.Frame()))
	else:
		check_type(name, tk.ttk.Frame, True)
		Instance.CurrnetFrame.Add(f)
	Instance.CurrnetFrame.Column = 0
@staticmethod
def EndHorizontal(fill="x"):
	Instance.CurrnetFrame.Row += 1
	Instance.CurrnetFrame.PP(fill)


@staticmethod
def BaseInvoke(core, x=5):
	if (Instance.CurrnetFrame.is_Passengers()):
		core.grid(row=Instance.CurrnetFrame.Row, column=Instance.CurrnetFrame.Column, padx=x, pady=5)
	else:
		core.pack(fill="x")
	Instance.CurrnetFrame.Column += 1


@staticmethod
def Label(text, x=5):
	check_type(text, str, True)
	ins = ttkbootstrap.Label(Instance.CurrnetFrame.LastFrame(), text=text)
	if (Instance.CurrnetFrame.is_Passengers()):
		ins.grid(row=Instance.CurrnetFrame.Row, column=Instance.CurrnetFrame.Column, padx=x, pady=5)
	else:
		ins.pack(fill="x")
	Instance.CurrnetFrame.Column += 1
@staticmethod
def Button(text, command, x=5):
	check_type(text, str, True)
	check_type(command, function, True)
	ins = ttkbootstrap.Button(Instance.CurrnetFrame.LastFrame(), text=text, command=command)
	if (Instance.CurrnetFrame.is_Passengers()):
		ins.grid(row=Instance.CurrnetFrame.Row, column=Instance.CurrnetFrame.Column, padx=x, pady=5, sticky="ew")
	else:
		ins.pack(fill="x")
	Instance.CurrnetFrame.Column += 1
@staticmethod
def TextField(width, x=5):
	ins = ttkbootstrap.Entry(Instance.CurrnetFrame.LastFrame(), width=width)
	if (Instance.CurrnetFrame.is_Passengers()):
		ins.grid(row=Instance.CurrnetFrame.Row, column=Instance.CurrnetFrame.Column, padx=x, pady=5)
	else:
		ins.pack(fill="x")
	Instance.CurrnetFrame.Column += 1
	return ins
@staticmethod
def TextArea(size, x=5):
	ins = ScrolledText(Instance.CurrnetFrame.LastFrame(), height=size[1], width=size[0])
	if (Instance.CurrnetFrame.is_Passengers()):
		ins.grid(row=Instance.CurrnetFrame.Row, column=Instance.CurrnetFrame.Column, padx=x, pady=5)
	else:
		ins.pack(fill="both", expand=True)
	Instance.CurrnetFrame.Column += 1
	return ins



if __name__ == '__main__':
	pass