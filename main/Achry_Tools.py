import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
from tkinter import messagebox
from mtapi import *

from win32clipboard import OpenClipboard,SetClipboardData,CloseClipboard
import re
import time
import requests
import webbrowser
import os
import sys
import json
import traceback
import win32con
# import logging

################################################################
# hotbar function                                              # 快捷栏函数
################################################################
def new_note(self, notebook, lang):
    # MainBuild
    main_frame = ttk.Frame(notebook)
    notebook.add(main_frame, text=language.lang(lang))
    self.main_frame = main_frame
    return (notebook, main_frame)
################################################################
# Log content function                                         # 日志内容功能
################################################################
logtime = "log%s"%int(time.time()*1000);
mtl = log.new(logtime, "log")
def log_fail(w, l):
    """
    w : content
    l : log file
    """
    messagebox.showerror(language.lang("fail"), w)
    log.inp(traceback.format_exc(), l, 4)
def log_error(w, l):
    """
    w : content
    l : log file
    """
    messagebox.showerror(language.lang("error"), w)
    log.inp(w, l, 3)
def log_info(w, l):
    """
    w : content
    l : log file
    """
    messagebox.showinfo(language.lang("info"), w)
    log.inp(w, l, 1)
def log_insert(ins, w, l, lvl=1, failcustom=False):
    """
    ins : insert id
    w : tkinter input
    l : log file
    """
    ins.insert(tk.END, w+"\n")
    if lvl == 4: 
        if failcustom:  log.inp(w, l, lvl)
        else: log.inp(traceback.format_exc(), l, lvl)
    else: log.inp(w, l, lvl)

<<<<<<< HEAD

################################################################
# calc function                                                # 计算函数
################################################################
class calc:
    @staticmethod
    def clac_score():
        try:
            #定义变量
            base_score = None #关卡基础分
            xacc_multi = None #精准分
            speed_multi = None #速度分
            no_early_multi = None #无空敲分

            if calc_level_combobox.get() != '' and (calc_speed_entry.get()) != '' and calc_x_accuracy_entry.get() != '':
                difficult = calc_level_combobox.get() #难度
                speed = float(calc_speed_entry.get())
                xacc = float(calc_x_accuracy_entry.get())
            else:
                log_error(language.lang("gui.calc.function(except).write_empty"), mtl)
                return
            
            if world_rank_entry.get() == '':
                ranked_position = 2147483647
                log_error(language.lang("gui.calc.function(except).write_rank"), mtl)
            else:
                ranked_position = int(world_rank_entry.get())

            no_early = (calc_empty_hit_combobox.get() == language.lang('no') or xacc == 100)

            world_first = calc_first_clear_combobox == language.lang('yes')

            #计算关卡基础分 难度等会获取即diff
            if float(difficult) < 1: return 0
            else:
                switch = {
                    '1': 0.05,
                    '2': 0.1,
                    '3': 0.2,
                    '4': 0.3,
                    '5': 0.4,
                    '6': 0.5,
                    '7': 0.6,
                    '8': 0.7,
                    '9': 0.8,
                    '10': 0.9,
                    '11': 1,
                    '12': 2,
                    '13': 3,
                    '14': 5,
                    '15': 10,
                    '16': 15,
                    '17': 20,
                    '18': 30,
                    '18.5': 45,
                    '19': 60,
                    '19.5': 75,
                    '20': 100,
                    '20.05': 110,
                    '20.1': 120,
                    '20.15': 130,
                    '20.2': 140,
                    '20.25': 150,
                    '20.3': 160,
                    '20.35': 170,
                    '20.4': 180,
                    '20.45': 190,
                    '20.5': 200,
                    '20.55': 210,
                    '20.6': 220,
                    '20.65': 230,
                    '20.7': 240,
                    '20.75': 250,
                    '20.8': 275,
                    '20.85': 300,
                    '20.9': 350,
                    '20.95': 400,
                    '21': 500,
                    '21.05': 700,
                    '21.1': 1000,
                    '21.15': 1600,
                    '21.2': 2000,
                    '21.25': 3000,
                    '21.3': 5000
                }

                #基础分
                ### print(difficult)
                score_base = switch.get(str(difficult), None)
                ### print(score_base)
                
                #判断基础分是否正确（输入不正确的难度会返回None)看上面代码
                if score_base == None:
                    log_error(language.lang("gui.calc.function(except).error_level"), mtl)
                    return
            
                #xacc基础分计算
                if xacc == 100: xacc_multi = 7
                elif xacc >= 99.8: xacc_multi = (xacc - 99.73334) * 15 + 3
                elif xacc >= 99: xacc_multi = (xacc - 97) ** 1.5484 - 0.9249
                elif xacc >= 95: xacc_multi = ((xacc - 94) ** 1.6) / 12.1326 + 0.9176
                else:
                    log_error(language.lang("gui.calc.function(except).xacc_so_low"), mtl)
                    return

            
                #速度分
                if speed < 1:       speed_multi = 0
                elif speed < 1.1:   speed_multi = 25 * (speed - 1.1) ** 2 + 0.75
                elif speed < 1.2:   speed_multi = 0.75
                elif speed < 1.25:  speed_multi = 50 * (speed - 1.2) ** 2 + 0.75
                elif speed < 1.3:   speed_multi = -50 * (speed - 1.3) ** 2 + 1
                elif speed < 1.5:   speed_multi = 1
                elif speed < 1.75:  speed_multi = 2 * (speed - 1.5) ** 2 + 1
                elif speed < 2:     speed_multi = -2 * (speed - 2) ** 2 + 1.25
                else:               speed_multi = 1.25

                #无空敲
                base_score = score_base * xacc_multi * speed_multi * (1.1 if no_early else 1)

                log_info(
                    language.repl(language.repl(language.lang("gui.calc.function(success)")
                    , 1, (round(base_score * 1,2) if (not world_first) else round(base_score * 1.1,2)))
                    , 2, (round(base_score * ((0.9 ** (ranked_position - 1)) if ranked_position <= 20 else 0), 2)))
                    , mtl
                )
        except Exception as e:
            log_fail(language.repl(language.repl(language.lang("gui.noeffect.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

################################################################
# search function                                              # 搜索函数
################################################################
class search:
    @staticmethod
    def use_id():
        try:
            ### print(combo_box.get())
            if combo_box.get() == 'TUF':
                id = entry_id.get()
                if id == '':
                    log_text2.delete(1.0, tk.END) 
                    log_insert(log_text2, language.repl(language.lang("gui.levelsearch.function(except).id_is_empty"), 1, id), mtl, 3)
                    return
                
                response = requests.get(f"https://be.tuforums.com/levels/{id}", headers={"accept": "application/json"})
                info = response.json()

                if 'statusCode' in info:
                    log_text2.delete(1.0, tk.END) 
                    log_insert(log_text2, language.repl(language.repl(language.repl(language.lang("gui.levelsearch.function(except).status_error"), 1, info["message"]), 2, info["statusCode"]), 3, id), mtl, 3)
                    return
                
                log_text2.delete(1.0, tk.END) 
                log_insert(log_text2, 
                language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.lang("gui.levelsearch.function(TUF_success)")
                , 1, info['id'])
                , 2, info['artist'])
                , 3, info['song'])
                , 4, info['creator'])
                , 5, info['diff'])
                , 6, info['pguDiff'])
                , 7, info['vidLink'])
                , 8, info['dlLink'])
                , 9, info['workshopLink']), mtl)

            elif combo_box.get() == 'ADOFAI.GG':
                id = entry_id.get()
                if id == '':
                    log_text2.delete(1.0, tk.END) 
                    log_insert(log_text2, language.repl(language.lang("gui.levelsearch.function(except).id_is_empty"), 1, id), mtl, 3)
                    return
                
                response = requests.get(f"https://adofai.gg/api/v1/levels/{id}")
                info = response.json()

                if 'errors' in info:
                    msg = info["errors"][0]
                    log_text2.delete(1.0, tk.END) 
                    log_insert(log_text2, language.repl(language.repl(language.repl(language.lang("gui.levelsearch.function(except).status_error"), 1, msg["message"]), 2, msg["code"]), 3, id), mtl, 3)
                    return
                try: info["artists"] = [artist['name'] for artist in info['music']['artists']]
                except: 
                    log.inp("not artist in info[\"artist\"]", mtl, 3)
                    info["artists"] = "-"
                try: info["creators"] = [creator['name'] for creator in info['creators']]
                except: 
                    log.inp("not creators in info[\"creators\"]", mtl, 3)
                    info["creators"] = "-"
                try: info["tags"] = [tag['name'] for tag in info['tags']]
                except: 
                    log.inp("not tags in info[\"tags\"]", mtl, 3)
                    info["tags"] = "-"
                
                log_text2.delete(1.0, tk.END) 
                log_insert(log_text2, 
                language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.lang("gui.levelsearch.function(ADOFAIGG_success)")
                , 1, info['id'])
                , 2, info["artists"])
                , 3, info['title'])
                , 4, info["creators"])
                , 5, info['difficulty'])
                , 6, info['video'])
                , 7, info['download'])
                , 8, info['workshop'])
                , 9, info['tiles'])
                , 10, info["tags"]), mtl)
            
            else:
                id = entry_id.get()

                if id == '':
                    log_text2.delete(1.0, tk.END) 
                    log_insert(log_text2, language.repl(language.lang("gui.levelsearch.function(except).id_is_empty"), 1, id), mtl, 3)
                    return
                aqr = requests.get('https://www.adofaiaqr.top/static/buttonsData.js').text[18:-3]
                info = eval(aqr)[int(id)-1]

                log_text2.delete(1.0, tk.END) 
                log_insert(log_text2, 
                language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.lang("gui.levelsearch.function(AQR_success)")
                , 1, info['artist'])
                , 2, info['song'])
                , 3, info['author'])
                , 4, info['difficulties'])
                , 5, info['level'])
                , 6, info['vluation'])
                , 7, info['video_herf'])
                , 8, info['href']), mtl)
      
        except Exception as e:
            log_fail(language.repl(language.repl(language.lang("gui.levelsearch.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

    @staticmethod
    def query():
        try:
            url = f"https://be.t21c.kro.kr/levels?artistQuery={entry_artist.get()}&songQuery={entry_music.get()}&creatorQuery={entry_author.get()}&random=false"
            response = requests.get(url, headers={
                "accept": "application/json"
            })
            info = response.json()
            log_text2.delete(1.0, tk.END)
            log_insert(log_text2, language.repl(language.lang("gui.levelsearch.function(find)"), 1, info['count']), mtl)
            for infos in info['results']:
                log_insert(log_text2, 
                language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.repl(language.lang("gui.levelsearch.function(TUF_success)")
                , 1, infos['id'])
                , 2, infos['artist'])
                , 3, infos['song'])
                , 4, infos['creator'])
                , 5, infos['diff'])
                , 6, infos['pguDiff'])
                , 7, infos['vidLink'])
                , 8, infos['dlLink'])
                , 9, infos['workshopLink']) + '\n\n--------\n\n', mtl)

        except Exception as e:
            log_fail(language.repl(language.repl(language.lang("gui.levelsearch.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

################################################################
# downloadFile function                                        # 下载文件函数
################################################################
class downloadFile:
    @staticmethod
    def select_file():
        filename = askdirectory()
        if filename:
            # How???
            dn_path.delete(0, tk.END)
            dn_path.insert(tk.END, filename)

    @staticmethod
    def google_drive_download():
        # 构建请求的 URL，将 ID 作为参数传递
        if g_file_id_entry.get() == '':
            log_error(language.lang("gui.filedownload.function(except).id_is_empty"), mtl)
            return
        url = f"https://hjtbrz.mcfuns.cn/application/test/gdrive.php?id={g_file_id_entry.get()}"

        try:
            # 发起 GET 请求
            response = requests.get(url, stream=True)
            dn_status.configure(text=language.lang("gui.filedownload.function().downloading"))
            if response.status_code == 200:
                # 使用彩色的 tqdm 进度条
                # with tqdm.wrapattr(open(dn_path.get() + filename, "wb"), "write", miniters=1,
                #                 total=int(response.headers.get('content-length', 0)),
                #                 desc=filename, colour=True) as f:
                #     for chunk in response.iter_content(chunk_size=1024):
                #         if chunk:
                #             f.write(chunk)
                #             f.flush()
                file_size = response.headers.get('Content-Length')
                if not file_size:
                    file_size = float('nan')
                else:
                    file_size = int(file_size)

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
                        open(dn_path.get() + '/' + filename, "ab").write(chunk)
                        bytes_written += len(chunk)
                        # progress = int(bytes_written / total_size * 100 + 0.01)
                        # dn_progress["value"] = progress
                        dn_status.configure(text=language.repl(language.repl(language.lang("gui.filedownload.function().downloadingprocess"), 1, round(bytes_written / 1048576,2)), 2, round(file_size / 1048576,2)))
                        app.update_idletasks()
                        dn_progress['value'] = bytes_written / file_size * 100
                    if 'Error 404'.encode(encoding='utf-8') in chunk:
                        log_error(language.repl(language.lang("gui.filedownload.function(except).id_not_find"), 1, g_file_id_entry.get()), mtl)
                        os.remove(dn_path.get() + '/' + filename)
                        return

                log_info(language.repl(language.lang("gui.filedownload.function(success)"), 1, filename), mtl)
            else:
                log_error(language.lang("error"), language.repl(language.lang("gui.filedownload.function(except).fail"), 1, response.status_code), mtl)
        except Exception as e:
            if e.__class__.__name__ == 'PermissionError':
                log_fail(language.repl(language.repl(language.repl(language.repl(language.lang("gui.filedownload.function(except).error"), 1, dn_path.get()), 2, filename), 3, e.__class__.__name__), 4, e), mtl)
            else:
                log_fail(language.repl(language.repl(language.lang("gui.filedownload.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

    @staticmethod
    def discord_download():
        # 构建请求的 URL
        if d_file_link_entry.get() == '':
            log_error(language.lang("gui.filedownload.function(except).link_is_empty"), mtl)
            return

        try:
            # 发起 GET 请求
            response = requests.get(f'https://hjtbrz.mcfuns.cn/application/test/download.php?file_url={d_file_link_entry.get()}', stream=True)
            dn_status.configure(text=language.lang("gui.filedownload.function().downloading"))
            if response.status_code == 200:
                file_size = response.headers.get('Content-Length')
                if not file_size:
                    file_size = float('nan')
                else:
                    file_size = int(file_size)

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
                        open(dn_path.get() + '/' + filename, "ab").write(chunk)
                        bytes_written += len(chunk)
                        dn_status.configure(text=language.repl(language.repl(language.lang("gui.filedownload.function().downloadingprocess"), 1, round(bytes_written / 1048576,2)), 2, round(file_size / 1048576,2)))
                        app.update_idletasks()
                        dn_progress['value'] = bytes_written / file_size * 100
                    if 'Error 404'.encode(encoding='utf-8') in chunk or not chunk:
                        log_error(language.repl(language.lang("gui.filedownload.function(except).link_not_find"), 1, g_file_id_entry.get()), mtl)
                        os.remove(dn_path.get() + '/' + filename)
                        return

                log_info(language.repl(language.lang("gui.filedownload.function(success)"), 1, filename), mtl)
            else:
                log_error(language.repl(language.lang("gui.filedownload.function(except).fail"), 1, response.status_code), mtl)
        except Exception as e:
            if e.__class__.__name__ == 'PermissionError':
                log_fail(language.repl(language.repl(language.repl(language.repl(language.lang("gui.filedownload.function(except).error"), 1, dn_path.get()), 2, filename), 3, e.__class__.__name__), 4, e), mtl)
            else:
                log_fail(language.repl(language.repl(language.lang("gui.filedownload.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

################################################################
# menuFunction function                                        # 菜单函数
################################################################
class menuFunction:

    @staticmethod
    def show_log_ui():
        global log_text_debug, mtl
 
        # 新开一个窗口 一个日志界面，有一个框，可以保存日志和复制日志=
        log_window = tk.Toplevel(app)
        log_window.title(language.lang("gui.log.name"))
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

        mtl.close()
        mtl = log.new(logtime)
        logs = log.out(mtl)
        this_endLog = "INFO"
        logs_lines = re.sub(r"\n\n", "\n", logs).split('\n')  # Assuming logs is a string with newline-separated entries
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
        button_save = tk.Button(log_window, text=language.lang("gui.log.save"), command=menuFunction.save_log)
        button_save.pack(fill="x")
        button_copy = tk.Button(log_window, text=language.lang("gui.log.copy"), command=lambda: menuFunction.write_clipboard(logs))
        button_copy.pack(fill="x")

        log_window.mainloop()
    
    def insert_line_log(log):
        global logs
        print(log)
        logs += log


    @staticmethod
    def write_clipboard(text):
        print(text)
        OpenClipboard()
        SetClipboardData(win32con.CF_UNICODETEXT, text)
        CloseClipboard()
        messagebox.showinfo(language.lang("gui.log.function(copy_success)"), language.lang("gui.log.function(copy_success)"))

    def save_log():
        # Define the content to be saved
        global logs
        
        # Ask the user for a filename to save the content
        file_path = asksaveasfilename(defaultextension=".log",
                                                filetypes=[("log files", "*.log"), ("All files", "*.*")])
        
        # Check if the user entered a file path
        if file_path:
            # Open the file at the specified path and write the content
            with open(file_path, 'w') as file:
                file.write(logs)


print(__import__("win32api").GetSystemDefaultLangID())
=======
print(__import__("win32api").GetSystemDefaultLangID(), type(__import__("win32api").GetSystemDefaultLangID()))
>>>>>>> 27685b8 (tool normalization(?))
locale = {"2052":"zh_cn",
          "1033":"en_us",
          "1042":"kr"}

app = tk.Tk()
app.title("ADOFAI Tools _ v1.O.3 _ _Achry_")
app.geometry("480x540")
# 创建Notebook
notebook = ttk.Notebook(app, bootstyle='info')


################################################################
# noEffect ui & function                                       # 去特效界面和函数
################################################################
class noEffect:
    def __init__(self):
        self.this = None
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
            if not filename.lower().endswith('.adofai'):
                log_error(language.lang("gui.noeffect.function(except).not_adofai_file"), mtl)
                return
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(tk.END, filename)

    @staticmethod
    def get_list_effect(self):
        log_insert(self.log_text, language.repl(language.lang("gui.noeffect.get_list_effect"), 1, self.insert_effect), mtl)

    @staticmethod
    def insert(self, no_log=False):
        for get_ in self.array_StringVar:
            get_ = get_.get()
            value = True
            if "T:" in get_:
                for i in self.insert_effect:
                    if i == get_[2:]:
                        value = False
                        break;
                if value:
                    self.insert_effect.append(get_[2:])
                    if (not no_log): log_insert(self.log_text, language.repl(language.lang("gui.noeffect.add_success"), 1, get_[2:]), mtl)
            if "F:" in get_:
                for i in self.insert_effect:
                    if i == get_[2:]:
                        value = False
                        break;
                if not value:
                    self.insert_effect.remove(get_[2:])
                    if (not no_log): log_insert(self.log_text, language.repl(language.lang("gui.noeffect.remove_success"), 1, get_[2:]), mtl)

    @staticmethod
    def process_file(self):
        filename = self.entry_path.get()
        if not filename:
            log_error(language.lang("gui.noeffect.function(except).not_select_file"), mtl)
            return
        if not filename.lower().endswith('.adofai'):
            log_error(language.lang("gui.noeffect.function(except).not_adofai_file"), mtl)
            return
        start = time.time()
        
        # 在这里处理文件  
        try:
            convert = adofai_convert.strList_to_dict(open(filename, 'r', encoding='utf8').readlines())
            file_contents = convert["result"]
            effect = self.insert_effect

            if len(effect) > 0 :
                log.inp("get remove effect", mtl, 1)
                for i in effect:
                    now_file_contenes = []
                    for ii in range(len(file_contents["actions"])):
                        if file_contents["actions"][ii]["eventType"] != i:
                            now_file_contenes.append(file_contents["actions"][ii])
                        else:
                            log.inp("removed effect(%s) in %s"%(i, ii), mtl, 1)
                    file_contents["actions"] = now_file_contenes
                    now_file_contenes = []
                    for ii in range(len(file_contents["decorations"])):
                        if file_contents["decorations"][ii]["eventType"] != i:
                            now_file_contenes.append(file_contents["decorations"][ii])
                        else:
                            log.inp("removed effect(%s) in %s"%(i, ii), mtl, 1)
                    file_contents["decorations"] = now_file_contenes
            else:
                log.inp("not get remove effect", mtl, 1)

            convert["result"] = file_contents
            file_directory = os.path.dirname(filename)
            open(file_directory+'/Non_effect.adofai','w',encoding="utf8").write(adofai_convert.dict_to_json(convert))
            end_time = time.time()
            log_insert(self.log_text, language.repl(language.repl(language.lang("gui.noeffect.function(success)"), 1, file_directory), 2, round(end_time-start,3)), mtl)
        except Exception as e:
            log_fail(language.repl(language.repl(language.lang("gui.noeffect.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)
   
    @staticmethod
    def setting(self):
        log_window = tk.Toplevel(app)
        log_window.title(language.lang("gui.noeffect.name"))
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

    def main(self, notebook):
        self.this = self
        notebook, main_frame = new_note(self, notebook, "gui.noeffect.name")
        frame = ttk.Frame(main_frame)
        label_path = ttk.Label(frame, text=language.lang("gui.noeffect.file_path"))
        label_path.grid(row=0, column=0, padx=5, pady=5)
        self.entry_path = ttk.Entry(frame, width=30)
        self.entry_path.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text=language.lang("gui.noeffect.browse"), command=lambda: self.select_file(self))\
            .grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        ttk.Button(frame, text=language.lang("gui.noeffect.setting"), command=lambda: self.setting(self))\
            .grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Button(frame, text=language.lang("gui.noeffect.check"), command=lambda: self.get_list_effect(self))\
            .grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        frame.pack(fill="x")
        self.log_text = ScrolledText(main_frame, height=10, width=50)
        self.log_text.pack(fill="both", expand=True)
        button_convert = ttk.Button(main_frame, text=language.lang("gui.noeffect.convert"), command=lambda: self.process_file(self))
        button_convert.pack(fill="x")
        for i in range(len(self.array_StringVar)):
            self.array_StringVar[i].set("T:"+adofai_const().effect[i])
        self.insert(self, True)
        return notebook

################################################################
# calc ui & function                                           # 计算界面和函数
################################################################
class calc:
    def __init__(self):
        self.this = None
        self.main_frame = None
        self.calc_level_combobox = None
        self.calc_speed_entry = None
        self.calc_x_accuracy_entry = None
        self.world_rank_entry = None
        self.calc_empty_hit_combobox = None
        self.calc_first_clear_combobox = None
        self.value = {
            1: 0.05,
            2: 0.1,
            3: 0.2,
            4: 0.3,
            5: 0.4,
            6: 0.5,
            7: 0.6,
            8: 0.7,
            9: 0.8,
            10: 0.9,
            11: 1,
            12: 2,
            13: 3,
            14: 5,
            15: 10,
            16: 15,
            17: 20,
            18: 30,
            18.5: 45,
            19: 60,
            19.5: 75,
            20: 100,
            20.05: 110,
            20.1: 120,
            20.15: 130,
            20.2: 140,
            20.25: 150,
            20.3: 160,
            20.35: 170,
            20.4: 180,
            20.45: 190,
            20.5: 200,
            20.55: 210,
            20.6: 220,
            20.65: 230,
            20.7: 240,
            20.75: 250,
            20.8: 275,
            20.85: 300,
            20.9: 350,
            20.95: 400,
            21: 500,
            21.05: 700,
            21.1: 1000,
            21.15: 1600,
            21.2: 2000,
            21.25: 3000,
            21.3: 5000
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
                log_error(language.lang("gui.calc.function(except).write_empty"), mtl)
                return
            
            if self.world_rank_entry.get() == '':
                ranked_position = 2147483647
                log_error(language.lang("gui.calc.function(except).write_rank"), mtl)
            else:
                ranked_position = int(self.world_rank_entry.get())

            no_early = (self.calc_empty_hit_combobox.get() == language.lang('no') or xacc == 100)

            world_first = calc_first_clear_combobox.get() == language.lang('yes')

            #计算关卡基础分 难度等会获取即diff
            if float(difficult) < 1: return 0
            else:

                #基础分
                ### print(difficult)
                score_base = self.value.get(str(difficult), None)
                ### print(score_base)
                
                #判断基础分是否正确（输入不正确的难度会返回None)看上面代码
                if score_base == None:
                    log_error(language.lang("gui.calc.function(except).error_level"), mtl)
                    return
            
                #xacc基础分计算
                if xacc == 100: xacc_multi = 7
                elif xacc >= 99.8: xacc_multi = (xacc - 99.73334) * 15 + 3
                elif xacc >= 99: xacc_multi = (xacc - 97) ** 1.5484 - 0.9249
                elif xacc >= 95: xacc_multi = ((xacc - 94) ** 1.6) / 12.1326 + 0.9176
                else:
                    log_error(language.lang("gui.calc.function(except).xacc_so_low"), mtl)
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

                log_info(
                    language.repl(language.repl(language.lang("gui.calc.function(success)")
                    , 1, (round(base_score * 1,2) if (not world_first) else round(base_score * 1.1,2)))
                    , 2, (round(base_score * ((0.9 ** (ranked_position - 1)) if ranked_position <= 20 else 0), 2)))
                    , mtl
                )
        except Exception as e:
            log_fail(language.repl(language.repl(language.lang("gui.noeffect.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

    def main(self, notebook):
        self.this = self
        notebook, main_frame = new_note(self, notebook, "gui.calc.name")
        # 创建 LabelFrame
        frame = ttk.LabelFrame(main_frame, text="PP")
        frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="we")
        # 添加等级
        ttk.Label(frame, text=language.lang("gui.calc.level"))\
            .grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.calc_level_combobox = ttk.Combobox(frame, values=list(self.value.keys()), state="readonly", width=12)
        self.calc_level_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.calc_level_combobox.current(0)
        # 添加倍速
        ttk.Label(frame, text=language.lang("gui.calc.speed"))\
            .grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.calc_speed_entry = ttk.Entry(frame, width=12)
        self.calc_speed_entry.grid(row=0, column=3, padx=5, pady=5, sticky="we")
        # 添加 X 精准
        ttk.Label(frame, text=language.lang("gui.calc.xacc"))\
            .grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.calc_x_accuracy_entry = ttk.Entry(frame, width=12)
        self.calc_x_accuracy_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        # 添加是否空敲
        ttk.Label(frame, text=language.lang("gui.calc.is_tooEarly"))\
            .grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.calc_empty_hit_combobox = ttk.Combobox(frame, values=[language.lang('yes'), language.lang('no')], state="readonly", width=12)
        self.calc_empty_hit_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="we")
        self.calc_empty_hit_combobox.current(1)  # 默认选择否
        # 添加是否首通
        ttk.Label(frame, text=language.lang("gui.calc.is_firstClear"))\
            .grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.calc_first_clear_combobox = ttk.Combobox(frame, values=[language.lang('yes'), language.lang('no')], state="readonly", width=12)
        self.calc_first_clear_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="we")
        self.calc_first_clear_combobox.current(1)  # 默认选择否
        # 添加世界排名输入框
        ttk.Label(frame, text=language.lang("gui.calc.is_rank"))\
            .grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.world_rank_entry = ttk.Entry(frame, width=12)
        self.world_rank_entry.grid(row=2, column=3, padx=5, pady=5, sticky="we")
        #计算按钮
        ttk.Button(frame, text=language.lang("gui.calc.calcScore"), command=lambda: self.action(self))\
            .grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        return notebook

################################################################
# search chart ui & function                                   # 搜索谱面界面和函数
################################################################
class search:
    def __init__(self):
        self.this = None
        self.main_frame = None
        self.combo_box = None
        self.entry_id = None
        self.entry_artist = None
        self.entry_music = None
        self.entry_author = None
        self.log_text = None
    @staticmethod
    def use_id(self):
        try:
            ### print(combo_box.get())
            if self.combo_box.get() == 'TUF':
                id = self.entry_id.get()
                if id == '':
                    self.log_text.delete(1.0, tk.END) 
                    log_insert(self.log_text, language.repl(language.lang("gui.levelsearch.function(except).id_is_empty"), 1, id), mtl, 3)
                    return
                
                response = requests.get(f"https://be.tuforums.com/levels/{id}", headers={"accept": "application/json"})
                info = response.json()

                if 'statusCode' in info:
                    self.log_text.delete(1.0, tk.END) 
                    log_insert(self.log_text, language.repl(language.repl(language.repl(language.lang("gui.levelsearch.function(except).status_error"), 1, info["message"]), 2, info["statusCode"]), 3, id), mtl, 3)
                    return
                
                self.log_text.delete(1.0, tk.END) 
                log_insert(self.log_text, language.repls(language.lang("gui.levelsearch.function(TUF_success)"),
                    [info['id'], info['artist'] ,info['song'] ,info['creator'] ,info['diff'] ,info['pguDiff'] ,info['vidLink'] ,info['dlLink'] ,info['workshopLink']], 1
                ), mtl)

            elif self.combo_box.get() == 'ADOFAI.GG':
                id = self.entry_id.get()
                if id == '':
                    self.log_text.delete(1.0, tk.END) 
                    log_insert(self.log_text, language.repl(language.lang("gui.levelsearch.function(except).id_is_empty"), 1, id), mtl, 3)
                    return
                
                response = requests.get(f"https://adofai.gg/api/v1/levels/{id}")
                info = response.json()

                if 'errors' in info:
                    msg = info["errors"][0]
                    self.log_text.delete(1.0, tk.END) 
                    log_insert(self.log_text, language.repl(language.repl(language.repl(language.lang("gui.levelsearch.function(except).status_error"), 1, msg["message"]), 2, msg["code"]), 3, id), mtl, 3)
                    return
                try: info["artists"] = [artist['name'] for artist in info['music']['artists']]
                except: 
                    log.inp("not artist in info[\"artist\"]", mtl, 3)
                    info["artists"] = "-"
                try: info["creators"] = [creator['name'] for creator in info['creators']]
                except: 
                    log.inp("not creators in info[\"creators\"]", mtl, 3)
                    info["creators"] = "-"
                try: info["tags"] = [tag['name'] for tag in info['tags']]
                except: 
                    log.inp("not tags in info[\"tags\"]", mtl, 3)
                    info["tags"] = "-"
                
                self.log_text.delete(1.0, tk.END) 
                log_insert(self.log_text, language.repls(language.lang("gui.levelsearch.function(ADOFAIGG_success)"), 
                    [info['id'], info["artists"], info['title'], info["creators"], info['difficulty'], info['video'], info['download'], info['workshop'], info['tiles'], info["tags"]], 1
                ), mtl)
            
            else:
                id = self.entry_id.get()

                if id == '':
                    self.log_text.delete(1.0, tk.END) 
                    log_insert(self.log_text, language.repl(language.lang("gui.levelsearch.function(except).id_is_empty"), 1, id), mtl, 3)
                    return
                aqr = requests.get('https://www.adofaiaqr.top/static/buttonsData.js').text[18:-3]
                info = eval(aqr)[int(id)-1]

                self.log_text.delete(1.0, tk.END) 
                log_insert(self.log_text, language.repls(language.lang("gui.levelsearch.function(AQR_success)"), 
                    [info['artist'], info['song'], info['author'], info['difficulties'], info['level'], info['vluation'], info['video_herf'], info['href']], 1
                ), mtl)
      
        except Exception as e:
            log_fail(language.repl(language.repl(language.lang("gui.levelsearch.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

    @staticmethod
    def query(self):
        try:
            url = f"https://be.t21c.kro.kr/levels?artistQuery={self.entry_artist.get()}&songQuery={self.entry_music.get()}&creatorQuery={self.entry_author.get()}&random=false"
            response = requests.get(url, headers={
                "accept": "application/json"
            })
            info = response.json()
            self.log_text.delete(1.0, tk.END)
            log_insert(self.log_text, language.repl(language.lang("gui.levelsearch.function(find)"), 1, info['count']), mtl)
            for infos in info['results']:
                log_insert(self.log_text, language.repls(language.lang("gui.levelsearch.function(TUF_success)"), 
                    [infos['id'], infos['artist'], infos['song'], infos['creator'], infos['diff'], infos['pguDiff'], infos['vidLink'], infos['dlLink'], infos['workshopLink']], 1
                ) + '\n\n--------\n\n', mtl)

        except Exception as e:
            log_fail(language.repl(language.repl(language.lang("gui.levelsearch.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

    def main(self, notebook):
        self.this = self
        notebook, main_frame = new_note(self, notebook, "gui.levelsearch.name")
        # 通过ID查询部分
        id_frame = ttk.Labelframe(main_frame, text=language.lang("gui.levelsearch.search_id"))
        id_frame.pack(fill="x", padx=10, pady=5)
        self.combo_box = ttk.Combobox(id_frame, values=["TUF", "ADOFAI.GG", "AQR"], state="readonly")
        self.combo_box.current(0)  # 设置默认选择
        self.combo_box.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        ttk.Label(id_frame, text=language.lang("gui.levelsearch.id"))\
            .grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(id_frame,width=35)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(id_frame, text=language.lang("gui.levelsearch.search"), command=lambda: self.use_id(self))\
            .grid(row=0, column=2, padx=5, pady=5)
        # 通过信息查询部分
        info_frame = ttk.Labelframe(main_frame,text=language.lang("gui.levelsearch.info_search"))
        info_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(info_frame, text=language.lang("gui.levelsearch.artist"))\
            .grid(row=0, column=0, padx=5, pady=5)
        self.entry_artist = ttk.Entry(info_frame,width=35)
        self.entry_artist.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(info_frame, text=language.lang("gui.levelsearch.song"))\
            .grid(row=1, column=0, padx=5, pady=5)
        self.entry_music = ttk.Entry(info_frame,width=35)
        self.entry_music.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(info_frame, text=language.lang("gui.levelsearch.author"))\
            .grid(row=2, column=0, padx=5, pady=5)
        self.entry_author = ttk.Entry(info_frame,width=35)
        self.entry_author.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(info_frame, text=language.lang("gui.levelsearch.search"), command=lambda: self.query(self))\
            .grid(row=3, columnspan=2, padx=5, pady=5, sticky="ew")
        # 日志部分
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_text = ScrolledText(log_frame, height=10, width=50)
        self.log_text.pack(fill="both", expand=True)
        return notebook

################################################################
# downloadFile ui & function                                   # 下载文件界面和函数
################################################################
class downloadFile:
    def __init__(self):
        self.this = None
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
            log_error(language.lang("gui.filedownload.function(except).id_is_empty"), mtl)
            return

        try:
            # 发起 GET 请求
            response = requests.get(f"https://hjtbrz.mcfuns.cn/application/test/gdrive.php?id={self.google_entry.get()}", stream=True)
            if response.status_code != 200:
                log_error(language.lang("error"), language.repl(language.lang("gui.filedownload.function(except).fail"), 1, response.status_code), mtl)
                return

            self.status.configure(text=language.lang("gui.filedownload.function().downloading"))
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
                    self.status.configure(text=language.repls(language.lang("gui.filedownload.function().downloadingprocess"), [round(bytes_written / 1048576,2), round(file_size / 1048576,2)], 1))
                    self.progress['value'] = bytes_written / file_size * 100
                    app.update_idletasks()
                if 'Error 404'.encode(encoding='utf-8') in chunk:
                    log_error(language.repl(language.lang("gui.filedownload.function(except).id_not_find"), 1, self.google_entry.get()), mtl)
                    os.remove(self.path.get() + '/' + filename)
                    return

            log_info(language.repl(language.lang("gui.filedownload.function(success)"), 1, filename), mtl)
        except Exception as e:
            if e.__class__.__name__ == 'PermissionError':
                log_fail(language.repls(language.lang("gui.filedownload.function(except).error_dict"), [self.path.get(), filename, e.__class__.__name__, e], 1), mtl)
            else:
                log_fail(language.repl(language.repl(language.lang("gui.filedownload.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

    @staticmethod
    def discord_action(self):
        # 构建请求的 URL
        if self.discord_entry.get() == '':
            log_error(language.lang("gui.filedownload.function(except).link_is_empty"), mtl)
            return

        try:
            # 发起 GET 请求
            response = requests.get(f'https://hjtbrz.mcfuns.cn/application/test/download.php?file_url={self.discord_entry.get()}', stream=True)
            if response.status_code != 200:
                log_error(language.repl(language.lang("gui.filedownload.function(except).fail"), 1, response.status_code), mtl)
                return

            self.status.configure(text=language.lang("gui.filedownload.function().downloading"))
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
                    self.status.configure(text=language.repls(language.lang("gui.filedownload.function().downloadingprocess"), [round(bytes_written / 1048576,2), round(file_size / 1048576,2)], 1))
                    self.progress['value'] = bytes_written / file_size * 100
                    app.update_idletasks()
                if 'Error 404'.encode(encoding='utf-8') in chunk or not chunk:
                    log_error(language.repl(language.lang("gui.filedownload.function(except).link_not_find"), 1, self.discord_entry.get()), mtl)
                    os.remove(self.path.get() + '/' + filename)
                    return

            log_info(language.repl(language.lang("gui.filedownload.function(success)"), 1, filename), mtl)
        except Exception as e:
            if e.__class__.__name__ == 'PermissionError':
                log_fail(language.repls(language.lang("gui.filedownload.function(except).error_dict"), [self.path.get(), filename, e.__class__.__name__, e], 1), mtl)
            else:
                log_fail(language.repl(language.repl(language.lang("gui.filedownload.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

    def main(self, notebook):
        # Google Drive Section
        self.this = self
        notebook, main_frame = new_note(self, notebook, "gui.filedownload.name")

        google_frame = ttk.LabelFrame(main_frame, text="Google Drive[Use ID]")
        google_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.google_entry = ttk.Entry(google_frame, width=48)
        self.google_entry.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(google_frame, text=language.lang("gui.filedownload.download"),command=lambda: downloadFile.google_action(self))\
            .grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        discord_frame = ttk.LabelFrame(main_frame, text="discord[Use Link]")
        discord_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.discord_entry = ttk.Entry(discord_frame, width=48)
        self.discord_entry.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(discord_frame, text=language.lang("gui.filedownload.download"), command=lambda: downloadFile.discord_action(self))\
            .grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Download Setting Section
        setting_frame = ttk.Frame(main_frame)
        setting_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(setting_frame, text=language.lang("gui.filedownload.save_path"))\
            .grid(row=1, column=0, padx=5, pady=5)

        self.path = ttk.Entry(setting_frame)
        self.path.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(setting_frame, text=language.lang("gui.filedownload.browse"), command=lambda: downloadFile.select_file(self))\
            .grid(row=1, column=2, padx=5, pady=5)

        self.status = ttk.Label(setting_frame, text=language.lang("gui.filedownload.status"))
        self.status.grid(row=2, column=0, padx=5, pady=5)

        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=200, mode="determinate")
        self.progress.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=1)

        return notebook

################################################################
# menu function                                                # 菜单函数
################################################################
class menu:
    def __init__(self):
        self.this = None
        self.main_frame = None
        self.changelog = [
            "版本 1.0.1:\n- 更删除了欢迎页面，添加了关于页面\n- 将f-string外层单引号改为双引号",
            "版本 1.0.2:\n- 允许选择不需要删除的特效类型 并且允许它保存在Non-Effect里\n- 在文件下载中添加了进度栏\n- 添加了logging 库\n- 添加了日志功能",
            "版本 1.0.3:\n- 删除了logging库 转用log 这使得允许自动保存日志(更方便调试)\n- 更新了日志颜色区分",
            "版本 1.0.4:\n- 优化noeffect逻辑\n- 添加中英注释\n- 优化代码排版",
        ]
    @staticmethod
    def show_log_ui_V1():
        global mtl
 
        # 新开一个窗口 一个日志界面，有一个框，可以保存日志和复制日志=
        log_window = tk.Toplevel(app)
        log_window.title(language.lang("gui.logV1.name"))
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

        mtl[0].close()
        mtl[1].close()
        mtl = log.new(logtime, "log")
        logs = log.out(mtl)
        this_endLog = "INFO"
        logs_lines = re.sub(r"\n\n", "\n", logs[0]).split('\n')  # Assuming logs is a string with newline-separated entries
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
        button_save = tk.Button(log_window, text=language.lang("gui.logV1.open_log_dir"), command=menu.open_log)
        button_save.pack(fill="x")
        button_copy = tk.Button(log_window, text=language.lang("gui.logV1.copy"), command=lambda: menu.write_clipboard(logs))
        button_copy.pack(fill="x")

        log_window.mainloop()

    @staticmethod
    def write_clipboard(text):
        OpenClipboard()
        SetClipboardData(win32con.CF_UNICODETEXT, text)
        CloseClipboard()
        messagebox.showinfo(language.lang("gui.logV1.function(copy_success)"), language.lang("gui.logV1.function(copy_success)"))

    @staticmethod
    def open_log():        
        # Ask the user for a filename to save the content
        os.system("explorer log")

    def main(self, notebook):
        self.this = self
        notebook, main_frame = new_note(self, notebook, "gui.menu.name")

        ttk.Label(main_frame, text=language.lang("gui.menu.producer"))\
            .grid(row=0, column=0, padx=10, pady=5, sticky="w")
        link = ttk.Label(main_frame, text="_Achry_", foreground="blue", cursor="hand2")
        link.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        link.bind("<Button-1>", lambda e: webbrowser.open("https://space.bilibili.com/1232092699"))

        ttk.Label(main_frame, text=language.lang("gui.menu.specialThanks"))\
            .grid(row=1, column=0, padx=10, pady=5, sticky="w")
        link = ttk.Label(main_frame, text="ModsTag", foreground="blue", cursor="hand2")
        link.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        link.bind("<Button-1>", lambda e: webbrowser.open("https://space.bilibili.com/496716004"))

        ttk.Label(main_frame, text=language.lang("gui.menu.github"))\
            .grid(row=2, column=0, padx=10, pady=5, sticky="w")
        link = ttk.Label(main_frame, text="AchryFI/ADOFAI-TOOLS", foreground="blue", cursor="hand2")
        link.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/AchryFI/ADOFAI-TOOLS/"))


        ttk.Label(main_frame, text=language.lang("gui.menu.contact_us"), font=('Helvetica', 16, 'bold'))\
            .grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        ttk.Label(main_frame, text="QQ: 377504570")\
            .grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        ttk.Label(main_frame, text="Bili/UID: 1232092699")\
            .grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        ttk.Label(main_frame, text=language.lang("gui.menu.email")+"achry@achry.space")\
            .grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        ttk.Label(main_frame, text=language.lang("gui.menu.updateLog"), font=('Helvetica', 16, 'bold'))\
            .grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        changelog_text = tk.Text(main_frame, height=12, width=63)
        changelog_text.grid(row=8, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # 插入默认更新日志
        for i in self.changelog:
            changelog_text.insert(tk.END, i+"\n")
        changelog_text.config(state=tk.DISABLED)

        menu_menu = ttk.Menu(app)

        filemenu = ttk.Menu(menu_menu, tearoff=False)
        filemenu.add_command(label="退出", command=lambda: exit())
        menu_menu.add_cascade(label="文件", menu=filemenu)

        editmenu = ttk.Menu(menu_menu, tearoff=False)
        editmenu.add_command(label=language.lang("gui.logV1.name"),command=menu.show_log_ui_V1)
        menu_menu.add_cascade(label="调试", menu=editmenu)

        app.config(menu=menu_menu)
        return notebook

################################################################
# start function                                               # 启动函数
################################################################
# 固定的函数
new_function = {
    "noEffect": noEffect(),
    "calc": calc(),
    "search": search(),
    "downloadFile": downloadFile(),
    "menu": menu(),
}
notebook = noEffect.main(new_function["noEffect"], notebook)
notebook = calc.main(new_function["calc"], notebook)
notebook = search.main(new_function["search"], notebook)
notebook = downloadFile.main(new_function["downloadFile"], notebook)
notebook = menu.main(new_function["menu"], notebook)
notebook.pack(fill=tk.BOTH, expand=True)
################################################################
# pb content pls pause to this (if ok)                         # 如果要修改代码并且pb 在可行情况下放置在这里 谢谢
################################################################
# 启动Tkinter的事件循环
app.mainloop()
