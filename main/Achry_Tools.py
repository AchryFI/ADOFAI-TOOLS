import tkinter as tk
from tkinter import ttk as tkinter
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
###from tkinter import messagebox
from mtapi import *
from os import remove, system, path
from re import sub as re_sub
from time import time as time_time
from time import strftime,localtime
from traceback import format_exc
from json import loads, dumps
from win32clipboard import OpenClipboard,SetClipboardData,CloseClipboard

import multiprocessing
import requests
import webbrowser
import sys
import win32con
# import logging

################################################################################################################################
# warning!!!!!!!!!!!! bug not fix success!!! now is only can open!!! not is release!!!                                         #
################################################################################################################################


################################################################
# hotbar function                                              # 快捷栏函数
################################################################
class _NoteBookClass:
	def __init__(self, Tkinter_StartUI):
		self.notebook = ttk.Notebook(Tkinter_StartUI, bootstyle='info')
	def new_note(self, self_self, lang):
		# MainBuild
		main_frame = ttk.Frame(self.notebook)
		self.notebook.add(main_frame, text=LanguageData.get(lang))
		self_self.main_frame = main_frame
		return main_frame
def update_config():
	open("config.json","w",encoding="UTF-8").write(json.dumps(ConfigData))
def update_cache():
	open("cache.json","w",encoding="UTF-8").write(json.dumps(CacheData))
def show_update_info():
	if (not ConfigData["skip_update_info"]):
		r = requests.get('https://hjtbrz.mcfuns.cn/application/casting.txt')
		r.encoding = "utf-8"
		messagebox.showinfo('公告',r.text)
		ConfigData["skip_update_info"] = True
		update_config()
################################################################
# Log content function                                         # 日志内容功能
################################################################
Start_Time = "log%s"%int(time_time()*1000);
ModsTagLog = log.new(Start_Time, "log")
def log_fail(content):
	messagebox.showerror(LanguageData.get("fail"), content)
	ModsTagLog.inp(format_exc(), 4)
def log_error(content):
	messagebox.showerror(LanguageData.get("error"), content)
	ModsTagLog.inp(content, 3)
def log_info(content):
	messagebox.showinfo(LanguageData.get("info"), content)
	ModsTagLog.inp(content, 1)
def log_insert(ins, content, lvl=1, failcustom=False):
	"""
	ins : insert id
	content : tkinter input
	"""
	ins.insert(tk.END, content+"\n")
	if lvl == 4: 
		if failcustom:  ModsTagLog.inp(content, lvl)
		else: ModsTagLog.inp(format_exc(), lvl)
	else: ModsTagLog.inp(content, lvl)

################################################################
# noEffect ui & function                                       # 去特效界面和函数
################################################################
class noEffect:
	def __init__(self):
		self.this = self
		self.main_frame = None
		self.insert_effect = []
		self.array_StringVar = [
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar(),
			tk.StringVar()
		]
		self.log_text = None
		self.entry_path = None

	@staticmethod
	def select_file(self):
		filename = askopenfilename()
		if filename:
			if not filename.lower().endswith('.adofai') or not filename.lower().endswith('.json'):
				log_error(LanguageData.get("gui.noeffect.function(except).not_adofai_file"))
				return
			self.entry_path.delete(0, tk.END)
			self.entry_path.insert(tk.END, filename)

	@staticmethod
	def get_list_effect(self):
		log_insert(self.log_text, LanguageData.get("gui.noeffect.get_list_effect", [str(self.insert_effect)]))

	@staticmethod
	def insert(self, no_log=False):
		for get_ in self.array_StringVar:
			get_ = get_.get()
			value = True
			for i in self.insert_effect:
				if i == get_[2:]:
					value = False
					break;
			if get_[:2] == "T:" and value:
					self.insert_effect.append(get_[2:])
					if (not no_log): log_insert(self.log_text, LanguageData.get("gui.noeffect.add_success", [get_[2:]]))
			if get_[:2] == "F:" and not value:
					self.insert_effect.remove(get_[2:])
					if (not no_log): log_insert(self.log_text, LanguageData.get("gui.noeffect.remove_success", [get_[2:]]))

	@staticmethod
	def process_file(self):
		filename = self.entry_path.get()
		if not filename:
			log_error(LanguageData.get("gui.noeffect.function(except).not_select_file"))
			return
		if not filename.lower().endswith('.adofai'):
			log_error(LanguageData.get("gui.noeffect.function(except).not_adofai_file"))
			return
		start = time_time()
		
		# 在这里处理文件  
		try:
			convert = adofai_convert.strList_to_dict(open(filename, 'r', encoding='utf8').readlines())
			file_contents = convert["result"]
			effect = self.insert_effect

			if len(effect) > 0 :
				log.inp("get remove effect", 1)
				for i in effect:
					now_file_contenes = []
					for ii in range(len(file_contents["actions"])):
						if file_contents["actions"][ii]["eventType"] != i:
							now_file_contenes.append(file_contents["actions"][ii])
						else:
							log.inp("removed effect(%s) in %s"%(i, ii), 1)
					file_contents["actions"] = now_file_contenes
					now_file_contenes = []
					for ii in range(len(file_contents["decorations"])):
						if file_contents["decorations"][ii]["eventType"] != i:
							now_file_contenes.append(file_contents["decorations"][ii])
						else:
							log.inp("removed effect(%s) in %s"%(i, ii), 1)
					file_contents["decorations"] = now_file_contenes
			else:
				log.inp("not get remove effect", 1)

			convert["result"] = file_contents
			file_directory = path.dirname(filename)
			open(file_directory+'/Non_effect.adofai','w',encoding="utf8").write(adofai_convert.dict_to_json(convert))
			end_time = time_time()
			log_insert(self.log_text, LanguageData.get("gui.noeffect.function(success)", [file_directory, round(end_time-start,3)]))
		except Exception as e:
			del start;
			log_fail(LanguageData.get("gui.noeffect.function(except).error", [e.__class__.__name__, e]))
   
	@staticmethod
	def setting(self):
		log_window = tk.Toplevel(Tkinter_StartUI)
		log_window.title(LanguageData.get("gui.noeffect.name"))
		log_window.geometry("480x540")
		style = ttk.Style()
		style.configure("custom.TCheckbutton", font=("Consolas", 10))
		setting_effect = ttk.LabelFrame(log_window, text="需要去的", width=20)

		select_array = []
		row = 0

		for i in range(len(adofai_const().effect)):
			select_array.append(ttk.Checkbutton(
				setting_effect, 
				text=adofai_const().effect[i].ljust(24, " "), 
				variable=self.array_StringVar[i], 
				onvalue="T:"+adofai_const().effect[i], 
				offvalue="F:"+adofai_const().effect[i], 
				style="custom.TCheckbutton", 
				command=lambda: noEffect.insert(self)
			))
			select_array[i].grid(row=row, column=0)
			row += 1
		setting_effect.grid(row=0, column=0)

	def main(self, NOTEBOOK):
		self.this = self
		self.main_frame = NOTEBOOK.new_note(self, "gui.noeffect.name")
		frame = ttk.Frame(self.main_frame)
		label_path = ttk.Label(frame, text=LanguageData.get("gui.noeffect.file_path"))
		label_path.grid(row=0, column=0, padx=5, pady=5)
		self.entry_path = ttk.Entry(frame, width=30)
		self.entry_path.grid(row=0, column=1, padx=5, pady=5)
		ttk.Button(frame, text=LanguageData.get("gui.noeffect.browse"), command=lambda: self.select_file(self))\
			.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

		ttk.Button(frame, text=LanguageData.get("gui.noeffect.setting"), command=lambda: self.setting(self))\
			.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

		ttk.Button(frame, text=LanguageData.get("gui.noeffect.check"), command=lambda: self.get_list_effect(self))\
			.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
		frame.pack(fill="x")
		self.log_text = ScrolledText(self.main_frame, height=10, width=50)
		self.log_text.pack(fill="both", expand=True)
		button_convert = ttk.Button(self.main_frame, text=LanguageData.get("gui.noeffect.convert"), command=lambda: self.process_file(self))
		button_convert.pack(fill="x")
		for i in range(len(self.array_StringVar)):
			self.array_StringVar[i].set("T:"+adofai_const().effect[i])
		self.insert(self, True)
		pass
################################################################
# calc ui & function                                           # 计算界面和函数
################################################################
class calc:
	def __init__(self):
		self.this = self
		self.main_frame = None
		self.calc_level_combobox = None
		self.calc_speed_entry = None
		self.calc_x_accuracy_entry = None
		self.world_rank_entry = None
		self.calc_empty_hit_combobox = None
		self.calc_first_clear_combobox = None
		self.value = {
			"1": 0.05,
			"2": 0.1,
			"3": 0.2,
			"4": 0.3,
			"5": 0.4,
			"6": 0.5,
			"7": 0.6,
			"8": 0.7,
			"9": 0.8,
			"10": 0.9,
			"11": 1,
			"12": 2,
			"13": 3,
			"14": 5,
			"15": 10,
			"16": 15,
			"17": 20,
			"18": 30,
			"18.5": 45,
			"19": 60,
			"19.5": 75,
			"20": 100,
			"20.05": 110,
			"20.1": 120,
			"20.15": 130,
			"20.2": 140,
			"20.25": 150,
			"20.3": 160,
			"20.35": 170,
			"20.4": 180,
			"20.45": 190,
			"20.5": 200,
			"20.55": 210,
			"20.6": 220,
			"20.65": 230,
			"20.7": 240,
			"20.75": 250,
			"20.8": 275,
			"20.85": 300,
			"20.9": 350,
			"20.95": 400,
			"21": 500,
			"21.05": 700,
			"21.1": 1000,
			"21.15": 1600,
			"21.2": 2000,
			"21.25": 3000,
			"21.3": 5000
		}

	@staticmethod
	def action(self):
		try:
			#定义变量
			base_score = None #关卡基础分
			xacc_multi = None #精准分
			speed_multi = None #速度分
			no_early_multi = None #无空敲分

			if self.calc_level_combobox.get() != '' and (self.calc_speed_entry.get()) != '' and self.calc_x_accuracy_entry.get() != '':
				difficult = self.calc_level_combobox.get() #难度
				speed = float(self.calc_speed_entry.get())
				xacc = float(self.calc_x_accuracy_entry.get())
			else:
				log_error(LanguageData.get("gui.calc.function(except).write_empty"))
				return
			
			if self.world_rank_entry.get() != '':
				ranked_position = int(self.world_rank_entry.get())
			else:
				log_error(LanguageData.get("gui.calc.function(except).write_rank"))
				return

			no_early = self.calc_empty_hit_combobox.get() == LanguageData.get('no') or xacc == 100

			world_first = self.calc_first_clear_combobox.get() == LanguageData.get('yes')

			#计算关卡基础分 难度等会获取即diff
			if float(difficult) < 1: return 0

			#基础分
			score_base = self.value.get(str(difficult), None)
			#判断基础分是否正确（输入不正确的难度会返回None)看上面代码
			if score_base == None:
				log_error(LanguageData.get("gui.calc.function(except).error_level"))
				return
		
			#xacc基础分计算
			if xacc == 100: xacc_multi = 7
			elif xacc >= 99.8: xacc_multi = (xacc - 99.73334) * 15 + 3
			elif xacc >= 99: xacc_multi = (xacc - 97) ** 1.5484 - 0.9249
			elif xacc >= 95: xacc_multi = ((xacc - 94) ** 1.6) / 12.1326 + 0.9176
			else:
				log_error(LanguageData.get("gui.calc.function(except).xacc_so_low"))
				return

		
			#速度分
			if speed < 1:       speed_multi = 0
			elif speed < 1.1:   speed_multi = 25   * (speed - 1.1) ** 2 + 0.75
			elif speed < 1.2:   speed_multi = 0.75
			elif speed < 1.25:  speed_multi = 50   * (speed - 1.2) ** 2 + 0.75
			elif speed < 1.3:   speed_multi = -50  * (speed - 1.3) ** 2 + 1
			elif speed < 1.5:   speed_multi = 1
			elif speed < 1.75:  speed_multi = 2    * (speed - 1.5) ** 2 + 1
			elif speed < 2:     speed_multi = -2   * (speed - 2)   ** 2 + 1.25
			else:               speed_multi = 1.25

			#无空敲
			base_score = score_base * xacc_multi * speed_multi * (1.1 if no_early else 1)

			log_info(LanguageData.get("gui.calc.function(success)", [round(base_score * (1.2 if not world_first else 1.1)), round(base_score * ((0.9 ** (ranked_position - 1)) if ranked_position <= 20 else 0))]))
		except Exception as e:
			log_fail(LanguageData.get("gui.noeffect.function(except).error", [e.__class__.__name__, e]))

	def main(self, NOTEBOOK):
		self.this = self
		self.main_frame = NOTEBOOK.new_note(self, "gui.calc.name")
		# 创建 LabelFrame
		frame = ttk.LabelFrame(self.main_frame, text="PP")
		frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="we")
		# 添加等级
		ttk.Label(frame, text=LanguageData.get("gui.calc.level"))\
			.grid(row=0, column=0, padx=5, pady=5, sticky="e")
		self.calc_level_combobox = ttk.Combobox(frame, values=list(self.value.keys()), state="readonly", width=12)
		self.calc_level_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="we")
		self.calc_level_combobox.current(0)
		# 添加倍速
		ttk.Label(frame, text=LanguageData.get("gui.calc.speed"))\
			.grid(row=0, column=2, padx=5, pady=5, sticky="e")
		self.calc_speed_entry = ttk.Entry(frame, width=12)
		self.calc_speed_entry.grid(row=0, column=3, padx=5, pady=5, sticky="we")
		# 添加 X 精准
		ttk.Label(frame, text=LanguageData.get("gui.calc.xacc"))\
			.grid(row=1, column=0, padx=5, pady=5, sticky="e")
		self.calc_x_accuracy_entry = ttk.Entry(frame, width=12)
		self.calc_x_accuracy_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
		# 添加是否空敲
		ttk.Label(frame, text=LanguageData.get("gui.calc.is_tooEarly"))\
			.grid(row=1, column=2, padx=5, pady=5, sticky="e")
		self.calc_empty_hit_combobox = ttk.Combobox(frame, values=[LanguageData.get('yes'), LanguageData.get('no')], state="readonly", width=12)
		self.calc_empty_hit_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="we")
		self.calc_empty_hit_combobox.current(1)  # 默认选择否
		# 添加是否首通
		ttk.Label(frame, text=LanguageData.get("gui.calc.is_firstClear"))\
			.grid(row=2, column=0, padx=5, pady=5, sticky="e")
		self.calc_first_clear_combobox = ttk.Combobox(frame, values=[LanguageData.get('yes'), LanguageData.get('no')], state="readonly", width=12)
		self.calc_first_clear_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="we")
		self.calc_first_clear_combobox.current(1)  # 默认选择否
		# 添加世界排名输入框
		ttk.Label(frame, text=LanguageData.get("gui.calc.is_rank"))\
			.grid(row=2, column=2, padx=5, pady=5, sticky="e")
		self.world_rank_entry = ttk.Entry(frame, width=12)
		self.world_rank_entry.grid(row=2, column=3, padx=5, pady=5, sticky="we")
		#计算按钮
		ttk.Button(frame, text=LanguageData.get("gui.calc.calcScore"), command=lambda: self.action(self))\
			.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
		pass
################################################################
# search chart ui & function                                   # 搜索谱面界面和函数
################################################################
class search:
	def __init__(self):
		self.this = self
		self.main_frame = None
		self.combo_box = None
		self.entry_id = None
		self.entry_artist = None
		self.entry_music = None
		self.entry_author = None
		self.log_text = None
	def cache_data(self, skip_get_config_item = True):
		try:
			CacheData["search"]["TUF"]
		except:
			try: CacheData["search"]
			except: CacheData["search"] = {}
			CacheData["search"]["TUF"] = requests.get(f"https://hjtbrz.mcfuns.cn/application/FileDownload/download.php?file_url=https://be.tuforums.com/levels").json()["results"]
			if 'statusCode' in CacheData["search"]["TUF"]:
				self.log_text.delete(1.0, tk.END) 
				log_insert(self.log_text, LanguageData.get("gui.levelsearch.function(except).status_error", [info["message"], info["statusCode"]]), 3)
				CacheData["search"]["TUF"] = []
		try:
			CacheData["search"]["ADOFAI.GG"]
		except:
			try: CacheData["search"]
			except: CacheData["search"] = {}
			CacheData["search"]["ADOFAI.GG"] = requests.get(f"https://hjtbrz.mcfuns.cn/application/FileDownload/download.php?file_url=https://adofai.gg/api/v1/levels").json()["results"]
			if 'errors' in CacheData["search"]["ADOFAI.GG"]:
				msg = info["errors"][0]
				self.log_text.delete(1.0, tk.END) 
				log_insert(self.log_text, LanguageData.get("gui.levelsearch.function(except).status_error", (msg["message"], msg["code"])), 3)
				CacheData["search"]["ADOFAI.GG"] = []
		try:
			CacheData["search"]["AQR"]
		except:
			try: CacheData["search"]
			except: CacheData["search"] = {}
			CacheData["search"]["AQR"] = requests.get(f"https://kdocs.adofaiaqr.top").json()
			update_cache()
	def get_info(self, result, ref_id:int):
		result = CacheData["search"][self.combo_box.get()]
		ref_id = int(ref_id)
		for array in result:
			if (int(array["id"]) == ref_id):
				return array
		return None

	@staticmethod
	def use_id(self):
		try:
			id = self.entry_id.get()
			if id == '':
				self.log_text.delete(1.0, tk.END) 
				log_insert(self.log_text, LanguageData.get("gui.levelsearch.function(except).id_is_empty", (id)), 3)
				return
			self.log_text.delete(1.0, tk.END) 
			if self.combo_box.get() == 'TUF':
				info = self.get_info(id)
				log_insert(self.log_text, LanguageData.get("gui.levelsearch.function(TUF_success)", 
				 	[info['id'], info['artist'], info['song'], info['creator'], info['diff'], info['pguDiff'], info['vidLink'], info['dlLink'], info['workshopLink']]
				))
			elif self.combo_box.get() == 'ADOFAI.GG':
				info = self.get_info(CacheData["search"]["ADOFAI.GG"], id)

				try: info["artists"] = [artist['name'] for artist in info['music']['artists']]
				except:  info["artists"] = "-"
				try: info["creators"] = [creator['name'] for creator in info['creators']]
				except: info["creators"] = "-"
				try: info["tags"] = [tag['name'] for tag in info['tags']]
				except: info["tags"] = "-"
				
				log_insert(self.log_text, LanguageData.get("gui.levelsearch.function(ADOFAIGG_success)",
					[info['id'], info["artists"], info['title'], info["creators"], info['difficulty'], info['video'], info['download'], info['workshop'], info['tiles'], info["tags"]]
				))
			elif self.combo_box.get() == 'AQR':
				info = self.get_info(int(id)+10000)
				log_insert(self.log_text, LanguageData.get("gui.levelsearch.function(AQR_success)", 
					[info['artist'], info['song'], info['author'], info['difficulties'], info['level'], info['vluation'], info['video_herf'], info['href']]
				))
			else:
				raise ValueError("combo_box not find")
	  
		except Exception as e:
			log_fail(LanguageData.get("gui.levelsearch.function(except).error", [e.__class__.__name__, e]))

	@staticmethod
	def query(self):
		try:
			url = f"https://be.tuforums.com/levels?query=&artistQuery={self.entry_artist.get()}&songQuery={self.entry_music.get()}&creatorQuery={self.entry_author.get()}&offset=10&random=false&lim"
			response = requests.get(url, headers={"accept": "application/json"})
			info = response.json()
			self.log_text.delete(1.0, tk.END)
			log_insert(self.log_text, LanguageData.get("gui.levelsearch.function(find)", [info['count']]))
			for infos in info['results']:
				log_insert(self.log_text, LanguageData.get("gui.levelsearch.function(TUF_success)", 
					[infos['id'], infos['artist'], infos['song'], infos['creator'], infos['diff'], infos['pguDiff'], infos['vidLink'], infos['dlLink'], infos['workshopLink']]
				) + '\n\n--------\n\n')

		except Exception as e:
			log_fail(LanguageData.get("gui.levelsearch.function(except).error", [e.__class__.__name__, e]))

	def main(self, NOTEBOOK):
		self.this = self
		self.main_frame = NOTEBOOK.new_note(self, "gui.levelsearch.name")
		self.cache_data()

		# 通过ID查询部分
		id_frame = ttk.Labelframe(self.main_frame, text=LanguageData.get("gui.levelsearch.search_id"))
		id_frame.pack(fill="x", padx=10, pady=5)
		self.combo_box = ttk.Combobox(id_frame, values=["TUF", "ADOFAI.GG", "AQR"], state="readonly")
		self.combo_box.current(0)  # 设置默认选择
		self.combo_box.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
		ttk.Label(id_frame, text=LanguageData.get("gui.levelsearch.id"))\
			.grid(row=0, column=0, padx=5, pady=5)
		self.entry_id = ttk.Entry(id_frame,width=35)
		self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
		ttk.Button(id_frame, text=LanguageData.get("gui.levelsearch.search"), command=lambda: self.use_id(self))\
			.grid(row=0, column=2, padx=5, pady=5)
		# 通过信息查询部分
		info_frame = ttk.Labelframe(self.main_frame,text=LanguageData.get("gui.levelsearch.info_search"))
		info_frame.pack(fill="x", padx=10, pady=5)
		ttk.Label(info_frame, text=LanguageData.get("gui.levelsearch.artist"))\
			.grid(row=0, column=0, padx=5, pady=5)
		self.entry_artist = ttk.Entry(info_frame,width=35)
		self.entry_artist.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
		ttk.Label(info_frame, text=LanguageData.get("gui.levelsearch.song"))\
			.grid(row=1, column=0, padx=5, pady=5)
		self.entry_music = ttk.Entry(info_frame,width=35)
		self.entry_music.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
		ttk.Label(info_frame, text=LanguageData.get("gui.levelsearch.author"))\
			.grid(row=2, column=0, padx=5, pady=5)
		self.entry_author = ttk.Entry(info_frame,width=35)
		self.entry_author.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
		ttk.Button(info_frame, text=LanguageData.get("gui.levelsearch.search"), command=lambda: self.query(self))\
			.grid(row=3, columnspan=2, padx=5, pady=5, sticky="ew")
		# 日志部分
		log_frame = ttk.Frame(self.main_frame)
		log_frame.pack(fill="both", expand=True, padx=10, pady=5)
		self.log_text = ScrolledText(log_frame, height=10, width=50)
		self.log_text.pack(fill="both", expand=True)
################################################################
# downloadFile ui & function                                   # 下载文件界面和函数
################################################################
class downloadFile:
	def __init__(self):
		self.this = self
		self.main_frame = None
		self.google_entry = None
		self.discord_entry = None
		self.status = None
		self.path = None
		self.progress = None

	@staticmethod
	def select_file(self):
		filename = askdirectory()
		if filename:
			# How???
			self.path.delete(0, tk.END)
			self.path.insert(tk.END, filename)

	@staticmethod
	def google_action(self):
		# 构建请求的 URL，将 ID 作为参数传递
		if self.google_entry.get() == '':
			log_error(LanguageData.get("gui.filedownload.function(except).id_is_empty"))
			return

		try:
			# 发起 GET 请求
			response = requests.get(f"https://hjtbrz.mcfuns.cn/application/FileDownload/gdrive.php?id={self.google_entry.get()}", stream=True)
			if response.status_code != 200:
				log_error(LanguageData.get("error"), LanguageData.get("gui.filedownload.function(except).fail", [response.status_code]))
				return

			self.status.configure(text=LanguageData.get("gui.filedownload.function().downloading"))
			file_size = float('nan') if not response.headers.get('Content-Length') else int(file_size)

			content_disposition = response.headers.get('Content-Disposition')
			if content_disposition:
				filename_index = content_disposition.find('filename=')
				if filename_index != -1:
					filename = content_disposition[filename_index + len('filename='):]
					filename = filename.strip('"')
				else:
					filename = 'downloaded_file'
			else:
				filename = 'downloaded_file'

			bytes_written = 0
			# total_size = int(response.headers.get('content-length', 0))
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:
					open(self.path.get() + '/' + filename, "ab").write(chunk)
					bytes_written += len(chunk)
					self.status.configure(text=LanguageData.get("gui.filedownload.function().downloadingprocess", [round(bytes_written / 1048576,2), round(file_size / 1048576,2)]))
					self.progress['value'] = bytes_written / file_size * 100
					Tkinter_StartUI.update_idletasks()
				if 'Error 404'.encode(encoding='utf-8') in chunk:
					log_error(LanguageData.get("gui.filedownload.function(except).id_not_find", [self.google_entry.get()]))
					remove(self.path.get() + '/' + filename)
					return

			log_info(LanguageData.get("gui.filedownload.function(success)", [filename]))
		except Exception as e:
			if e.__class__.__name__ == 'PermissionError':
				log_fail(LanguageData.get("gui.filedownload.function(except).error_dict", [self.path.get(), filename, e.__class__.__name__, e]))
			else:
				log_fail(LanguageData.get("gui.filedownload.function(except).error", [e.__class__.__name__, e]))

	@staticmethod
	def discord_action(self):
		# 构建请求的 URL
		if self.discord_entry.get() == '':
			log_error(LanguageData.get("gui.filedownload.function(except).link_is_empty"))
			return

		try:
			# 发起 GET 请求
			response = requests.get(f'https://hjtbrz.mcfuns.cn/application/FileDownload/download.php?file_url={self.discord_entry.get()}', stream=True)
			if response.status_code != 200:
				log_error(LanguageData.get("gui.filedownload.function(except).fail", [response.status_code]))
				return

			self.status.configure(text=LanguageData.get("gui.filedownload.function().downloading"))
			file_size = float('nan') if not response.headers.get('Content-Length') else int(file_size)

			content_disposition = response.headers.get('Content-Disposition')
			if content_disposition:
				filename_index = content_disposition.find('filename=')
				if filename_index != -1:
					filename = content_disposition[filename_index + len('filename='):]
					filename = filename.strip('"')
				else:
					filename = 'downloaded_file'
			else:
				filename = 'downloaded_file'

			bytes_written = 0
			# total_size = int(response.headers.get('content-length', 0))
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:
					open(self.path.get() + '/' + filename, "ab").write(chunk)
					bytes_written += len(chunk)
					self.status.configure(text=LanguageData.get("gui.filedownload.function().downloadingprocess", [round(bytes_written / 1048576,2), round(file_size / 1048576,2)]))
					self.progress['value'] = bytes_written / file_size * 100
					Tkinter_StartUI.update_idletasks()
				if 'Error 404'.encode(encoding='utf-8') in chunk or not chunk:
					log_error(LanguageData.get("gui.filedownload.function(except).link_not_find", [self.discord_entry.get()]))
					remove(self.path.get() + '/' + filename)
					return

			log_info(LanguageData.get("gui.filedownload.function(success)", [filename]))
		except Exception as e:
			if e.__class__.__name__ == 'PermissionError':
				log_fail(LanguageData.get("gui.filedownload.function(except).error_dict", [self.path.get(), filename, e.__class__.__name__, e]))
			else:
				log_fail(LanguageData.get("gui.filedownload.function(except).error", [e.__class__.__name__, e]))

	def main(self, NOTEBOOK):
		# Google Drive Section
		self.this = self
		self.main_frame = NOTEBOOK.new_note(self, "gui.filedownload.name")

		google_frame = ttk.LabelFrame(self.main_frame, text="Google Drive[Use ID]")
		google_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
		self.google_entry = ttk.Entry(google_frame, width=48)
		self.google_entry.grid(row=0, column=0, padx=5, pady=5)
		ttk.Button(google_frame, text=LanguageData.get("gui.filedownload.download"),command=lambda: downloadFile.google_action(self))\
			.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

		discord_frame = ttk.LabelFrame(self.main_frame, text="discord[Use Link]")
		discord_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
		self.discord_entry = ttk.Entry(discord_frame, width=48)
		self.discord_entry.grid(row=0, column=0, padx=5, pady=5)
		ttk.Button(discord_frame, text=LanguageData.get("gui.filedownload.download"), command=lambda: downloadFile.discord_action(self))\
			.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

		# Download Setting Section
		setting_frame = ttk.Frame(self.main_frame)
		setting_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

		ttk.Label(setting_frame, text=LanguageData.get("gui.filedownload.save_path"))\
			.grid(row=1, column=0, padx=5, pady=5)

		self.path = ttk.Entry(setting_frame)
		self.path.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

		ttk.Button(setting_frame, text=LanguageData.get("gui.filedownload.browse"), command=lambda: downloadFile.select_file(self))\
			.grid(row=1, column=2, padx=5, pady=5)

		self.status = ttk.Label(setting_frame, text=LanguageData.get("gui.filedownload.status"))
		self.status.grid(row=2, column=0, padx=5, pady=5)

		self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=200, mode="determinate")
		self.progress.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=1)
		pass
################################################################
# mod download function                                        # mod下载
################################################################
class modDownload:
	def __init__(self):
		self.this = self
		self.main_frame = None
		self.data = {}
		self.info = []

	def cache_data(self, skip_get_config_item = True):
		self.data = {}
		self.info = []

		if skip_get_config_item:
			try: 
				if (type(CacheData["modDownload"]["data"]) == dict):
					self.data = CacheData["modDownload"]["data"]
				else:
					raise ValueError("")
			except: 
				self.cache_data(False)
		else:
			for item in requests.get("https://hjtbrz.mcfuns.cn/application/FileDownload/download.php?file_url=https://bot.adofai.gg/api/mods/").json():
				if item['id'] not in self.data:
					self.data[item['id']] = item
				else:
					current_version = self.data[item['id']]['version']
					new_version = item.get('version')
					if new_version is None: continue

					# Compare version numbers
					if new_version == self.compare_versions(current_version, new_version):
						self.data[item['id']] = item
			try: CacheData["modDownload"]["data"]
			except: CacheData["modDownload"] = {}
			CacheData["modDownload"]["data"] = self.data
			update_cache()
		for item in self.data.values():
			self.info.append((
				item['name'],
				item.get('version'),
				item['cachedUsername'],
				strftime("%Y-%m-%d %H:%M:%S", localtime(round(item['uploadedTimestamp']/1000,0)))
			))
		pass

	def compare_versions(version1, version2):
		v1 = list(map(int, version1.split(".")))
		v2 = list(map(int, version2.split(".")))
		return v1 if v1 > v2 else v2 if v1 < v2 else 0
	
	def get_selecting(self, table):
		return table.item(table.selection()[0])

	def download_mod(self, mod):
		# mod = self.get_selecting()['values'][0]
		for item in self.data.values():
			if mod == item['name']:
				link = item['parsedDownload']

		webbrowser.open(link)

	def main(self, NOTEBOOK, Patch_NOTEBOOK_To_mainframe = False):
		self.this = self
		self.main_frame = NOTEBOOK.new_note(self, "gui.moddownload.name")
		self.cache_data()

		columns = [LanguageData.get("gui.moddownload.signName"), LanguageData.get("gui.moddownload.version"), LanguageData.get("gui.moddownload.author"), LanguageData.get("gui.moddownload.updateTime")]
		table = ttk.Treeview(
				master=self.main_frame,  # 父容器
				height=20,  # 表格显示的行数,height行
				columns=columns,  # 显示的列
				show='headings',  # 隐藏首列	
				)
		table.heading(columns[0], text=columns[0], anchor='w', command=lambda: self.get_selecting(table))  # 定义表头
		table.heading(columns[1], text=columns[1])  # 定义表头
		table.heading(columns[2], text=columns[2])  # 定义表头
		table.heading(columns[3], text=columns[3])  # 定义表头

		table.column(columns[0], width=200, minwidth=200, anchor=S)  # 定义列
		table.column(columns[1], width=50, minwidth=50, anchor=S)  # 定义列
		table.column(columns[2], width=100, minwidth=100, anchor=S)  # 定义列
		table.column(columns[3], width=200, minwidth=50, anchor=S)  # 定义列
		table.pack(pady=10)
		for s in self.info:
			table.insert('','end',values=s)

		VScroll1 = tk.Scrollbar(self.main_frame, orient='vertical', command=table.yview)	
		VScroll1.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.658)
		table.configure(yscrollcommand=VScroll1.set)

		ttk.Button(self.main_frame,text=LanguageData.get("gui.moddownload.download"),command=lambda: self.download_mod(self.get_selecting(table)['values'][0])).pack()
		#ttk.Button(self.main_frame,text=LanguageData.get("gui.moddownload.reload"),command=lambda: self.cache_data(False)).pack()
		pass
################################################################
# menu function                                                # 菜单函数
################################################################
class menu:
	def __init__(self):
		self.this = self
		self.main_frame = None
		self.changelog = [
			"版本 1.0.1:\n- 删除了欢迎页面，添加了关于页面\n- 将f-string外层单引号改为双引号",
			"版本 1.0.2:\n- 允许选择不需要删除的特效类型 并且允许它保存在Non-Effect里\n- 在文件下载中添加了进度栏\n- 添加了logging 库\n- 添加了日志功能",
			"版本 1.0.3:\n- 删除了logging库 转用log 这使得允许自动保存日志(更方便调试)\n- 更新了日志颜色区分",
			"版本 1.0.4:\n- 优化noeffect逻辑\n- 添加中英注释\n- 优化代码排版",
			"版本 1.1.0:\n- 添加了模组下载\n- 修复代码bug\n- 修复无法正常选择语言问题\n- 修复url错误问题",
		]
	@staticmethod
	def show_log_ui_V1():
		global ModsTagLog
 
		# 新开一个窗口 一个日志界面，有一个框，可以保存日志和复制日志
		log_window = tk.Toplevel(Tkinter_StartUI)
		log_window.title(LanguageData.get("logV1.name"))
		log_window.geometry("480x540")
		log_window.resizable(0, 0)
		log_text_debug = ScrolledText(log_window, height=10, width=50, font=("Consolas", 8))
		log_text_debug.pack(fill="both", expand=True)
		log_text_debug.text.config(state=tk.DISABLED)
		# Configure a tag for error messages in red
		log_text_debug.text.config(state=tk.NORMAL)
		# Insert logs into the text widget, highlighting errors in red
		log_text_debug.tag_configure("INFO", foreground="#FFFFFF", background="#303841")
		log_text_debug.tag_configure("WARN", foreground="#FFFF00", background="#303841")
		log_text_debug.tag_configure("ERROR", foreground="#FFFFFF", background="#FF5555")
		log_text_debug.tag_configure("FAIL", foreground="#FFFFFF", background="#BF0000")
		log_text_debug.tag_configure("DEBUG", foreground="#BFBFBF", background="#303841")

		ModsTagLog.reload()
		ModsTagLog = log.new(Start_Time, "log")
		logs = log.out(ModsTagLog)
		this_endLog = "INFO"
		logs_lines = re_sub(r"\n\n", "\n", logs[0]).split('\n')  # Assuming logs is a string with newline-separated entries
		for line in logs_lines:
			if "[ModsTag/INFO]" in line:    
				log_text_debug.insert("end", line + '\n', "INFO")
				this_endLog = "INFO"
			elif "[ModsTag/WARN]" in line:  
				log_text_debug.insert("end", line + '\n', "WARN")
				this_endLog = "WARN"
			elif "[ModsTag/ERROR]" in line: 
				log_text_debug.insert("end", line + '\n', "ERROR")
				this_endLog = "ERROR"
			elif "[ModsTag/FAIL]" in line:  
				log_text_debug.insert("end", line + '\n', "FAIL")
				this_endLog = "FAIL"
			elif "[ModsTag/DEBUG]" in line: 
				log_text_debug.insert("end", line + '\n', "DEBUG")
				this_endLog = "DEBUG"
			else: 
				log_text_debug.insert("end", line + '\n', this_endLog)
			
		log_text_debug.text.config(state=tk.DISABLED)
		button_save = tk.Button(log_window, text=LanguageData.get("logV1.open_log_dir"), command=menu.open_log)
		button_save.pack(fill="x")
		button_copy = tk.Button(log_window, text=LanguageData.get("logV1.copy"), command=lambda: menu.write_clipboard(logs))
		button_copy.pack(fill="x")

		log_window.mainloop()

	@staticmethod
	def write_clipboard(text):
		OpenClipboard()
		SetClipboardData(win32con.CF_UNICODETEXT, text)
		CloseClipboard()
		messagebox.showinfo(LanguageData.get("logV1.function(copy_success)"), LanguageData.get("logV1.function(copy_success)"))

	@staticmethod
	def open_log():        
		# Ask the user for a filename to save the content
		system("explorer log")

	def main(self, NOTEBOOK):
		self.this = self
		self.main_frame = NOTEBOOK.new_note(self, "gui.menu.name")

		ttk.Label(self.main_frame, text=LanguageData.get("gui.menu.producer"))\
			.grid(row=0, column=0, padx=10, pady=5, sticky="w")
		link = ttk.Label(self.main_frame, text="_Achry_", foreground="blue", cursor="hand2")
		link.grid(row=0, column=1, padx=10, pady=5, sticky="w")
		link.bind("<Button-1>", lambda e: webbrowser.open("https://space.bilibili.com/1232092699"))

		ttk.Label(self.main_frame, text=LanguageData.get("gui.menu.specialThanks"))\
			.grid(row=1, column=0, padx=10, pady=5, sticky="w")
		link = ttk.Label(self.main_frame, text="ModsTag", foreground="blue", cursor="hand2")
		link.grid(row=1, column=1, padx=10, pady=5, sticky="w")
		link.bind("<Button-1>", lambda e: webbrowser.open("https://space.bilibili.com/496716004"))

		ttk.Label(self.main_frame, text=LanguageData.get("gui.menu.github"))\
			.grid(row=2, column=0, padx=10, pady=5, sticky="w")
		link = ttk.Label(self.main_frame, text="AchryFI/ADOFAI-TOOLS", foreground="blue", cursor="hand2")
		link.grid(row=2, column=1, padx=10, pady=5, sticky="w")
		link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/AchryFI/ADOFAI-TOOLS/"))


		ttk.Label(self.main_frame, text=LanguageData.get("gui.menu.contact_us"), font=('Helvetica', 16, 'bold'))\
			.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

		ttk.Label(self.main_frame, text="QQ: 377504570")\
			.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

		ttk.Label(self.main_frame, text="Bili/UID: 1232092699")\
			.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")

		ttk.Label(self.main_frame, text=LanguageData.get("gui.menu.email")+"achry@achry.space")\
			.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

		ttk.Label(self.main_frame, text=LanguageData.get("gui.menu.updateLog"), font=('Helvetica', 16, 'bold'))\
			.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="w")

		changelog_text = tk.Text(self.main_frame, height=12, width=63)
		changelog_text.grid(row=8, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

		# 插入默认更新日志
		for i in self.changelog:
			changelog_text.insert(tk.END, i+"\n")
		changelog_text.config(state=tk.DISABLED)

		menu_menu = ttk.Menu(Tkinter_StartUI)

		filemenu = ttk.Menu(menu_menu, tearoff=False)
		filemenu.add_command(label="退出", command=lambda: exit())
		menu_menu.add_cascade(label="文件", menu=filemenu)

		editmenu = ttk.Menu(menu_menu, tearoff=False)
		editmenu.add_command(label=LanguageData.get("logV1.name"),command=menu.show_log_ui_V1)
		menu_menu.add_cascade(label="调试", menu=editmenu)

		Tkinter_StartUI.config(menu=menu_menu)
		pass
################################################################
# start function                                               # 启动函数
################################################################

Tkinter_StartUI = tk.Tk()
Tkinter_StartUI.title("ADOFAI Tools _ v1.O.3 _ _Achry_")
Tkinter_StartUI.geometry("640x560")
# 创建Notebook
NOTEBOOK = _NoteBookClass(Tkinter_StartUI)

open("cache.json", "a", encoding="utf-8").close()
if (open("cache.json", "r", encoding="utf-8").read() == ""): 
	open("cache.json", "w", encoding="utf-8").write("{}")
CacheData = json.loads(open("cache.json", "r", encoding="utf-8").read())

open("config.json", "a", encoding="utf-8").close()
if (open("config.json", "r", encoding="utf-8").read() == ""): 
	open("config.json", "w", encoding="utf-8").write("{\n\t\"version\": [1,1,1],\n\t\"lang\": null,\n\t\"skip_update_info\": false,\n\t\"Acceleration\": false\n}")
ConfigData = json.loads(open("config.json", "r", encoding="utf-8").read())

try:
	show_update_info()
except:
	ConfigData["skip_update_info"] = False
	show_update_info()

if (ConfigData["Acceleration"]): Acceleration = "https://hjtbrz.mcfuns.cn/application/FileDownload/download.php?file_url="
else: Acceleration = ""

LanguageData = language()
LanguageData.lang = ConfigData["lang"]
LanguageData.log = log
LanguageData.mtl = ModsTagLog

# 固定的函数
NewSelf = {
	"noEffect": noEffect(),
	"calc": calc(),
	"search": search(),
	"downloadFile": downloadFile(),
	"menu": menu(),
	"modDownload": modDownload()
}
noEffect.main(NewSelf["noEffect"], NOTEBOOK)
calc.main(NewSelf["calc"], NOTEBOOK)
search.main(NewSelf["search"], NOTEBOOK)
downloadFile.main(NewSelf["downloadFile"], NOTEBOOK)
modDownload.main(NewSelf["modDownload"], NOTEBOOK)
menu.main(NewSelf["menu"], NOTEBOOK)
NOTEBOOK.notebook.pack(fill=tk.BOTH, expand=True)
################################################################
# pb content pls paste to this (if ok)                         # 如果要修改代码并且pb 在可行情况下放置在这里 谢谢
################################################################

# tkinter loop
Tkinter_StartUI.mainloop()
