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
# Log content function                                         # 日志内容功能
################################################################
logtime = "log%s"%int(time.time()*1000);
mtl = log.new(logtime)
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
                
                response = requests.get(f"https://be.t21c.kro.kr/levels/{id}", headers={"accept": "application/json"})
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
                open(dn_path.get() + '/' + filename, "wb").write();
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
                open(dn_path.get() + '/' + filename, "wb").write();
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
locale = {"2052":"zh_cn",
          "1033":"en_us",
          "1042":"kr"}

app = tk.Tk()
app.title("ADOFAI Tools _ v1.O.3 _ _Achry_")
app.geometry("480x540")
# 创建Notebook
notebook = ttk.Notebook(app, bootstyle='info')


################################################################
# No Effect ui & function                                      # 去特效界面和函数
################################################################
class noEffect():
    def __init__(self):
        self.this = self
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
    def select_file(this):
        filename = askopenfilename()
        if filename:
            if not filename.lower().endswith('.adofai'):
                log_error(language.lang("gui.noeffect.function(except).not_adofai_file"), mtl)
                return
            this.entry_path.delete(0, tk.END)
            this.entry_path.insert(tk.END, filename)

    @staticmethod
    def get_list_effect(this):
        log_insert(this.log_text, language.repl(language.lang("gui.noeffect.get_list_effect"), 1, this.insert_effect), mtl)

    @staticmethod
    def insert(this, no_log=False):
        for get_ in this.array_StringVar:
            get_ = get_.get()
            value = True
            if "T:" in get_:
                for i in this.insert_effect:
                    if i == get_[2:]:
                        value = False
                        break;
                if value:
                    this.insert_effect.append(get_[2:])
                    if (not no_log): log_insert(this.log_text, language.repl(language.lang("gui.noeffect.add_success"), 1, get_[2:]), mtl)
            if "F:" in get_:
                for i in this.insert_effect:
                    if i == get_[2:]:
                        value = False
                        break;
                if not value:
                    this.insert_effect.remove(get_[2:])
                    if (not no_log): log_insert(this.log_text, language.repl(language.lang("gui.noeffect.remove_success"), 1, get_[2:]), mtl)

    @staticmethod
    def process_file(this):
        filename = this.entry_path.get()
        if not filename:
            log_error(language.lang("gui.noeffect.function(except).not_select_file"), mtl)
            return
        if not filename.lower().endswith('.adofai'):
            log_error(language.lang("gui.noeffect.function(except).not_adofai_file"), mtl)
            return
        start = time.time()
        
        # 在这里处理文件  
        try:
            convert = adofai_convert.to_dict(open(filename, 'r', encoding='utf8').readlines())
            file_contents = convert["result"]
            effect = this.insert_effect

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
            else:
                log.inp("not get remove effect", mtl, 1)

            convert["result"] = file_contents
            file_directory = os.path.dirname(filename)
            open(file_directory+'/Non_effect.adofai','w',encoding="utf8").write(adofai_convert.to_json(convert, True))
            end_time = time.time()
            log_insert(this.log_text, language.repl(language.repl(language.lang("gui.noeffect.function(success)"), 1, file_directory), 2, round(end_time-start,3)), mtl)
        except Exception as e:
            log_fail(language.repl(language.repl(language.lang("gui.noeffect.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)
   
    @staticmethod
    def setting(this):
        log_window = tk.Toplevel(app)
        log_window.title(language.lang("gui.noeffect.name"))
        log_window.geometry("480x540")
        style = ttk.Style()
        style.configure("custom.TCheckbutton", font=("Consolas", 10))
        setting_effect = ttk.LabelFrame(log_window, text="不需要去的", style="custom.TCheckbutton")

        select_array = []
        row = 0

        for i in range(len(adofai_const().effect)):
            select_array.append(ttk.Checkbutton(
                setting_effect, 
                text=adofai_const().effect[i].ljust(24, " "), 
                variable=this.array_StringVar[i], 
                onvalue="T:"+adofai_const().effect[i], 
                offvalue="F:"+adofai_const().effect[i], 
                style="custom.TCheckbutton", 
                command=lambda: noEffect.insert(this)
            ))
            select_array[i].grid(row=row, column=0)
            row += 1
        setting_effect.grid(row=0, column=0)

    def main(self):
        self.this = self
        level_conversion_frame = ttk.Frame(app)
        frame = ttk.Frame(level_conversion_frame)
        label_path = ttk.Label(frame, text=language.lang("gui.noeffect.file_path"))
        label_path.grid(row=0, column=0, padx=5, pady=5)
        self.entry_path = ttk.Entry(frame, width=30)
        self.entry_path.grid(row=0, column=1, padx=5, pady=5)
        button_browse = ttk.Button(frame, text=language.lang("gui.noeffect.browse"), command=lambda: self.select_file(self))
        button_browse.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        button_browse = ttk.Button(frame, text=language.lang("gui.noeffect.setting"), command=lambda: self.setting(self))
        button_browse.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        button_browse = ttk.Button(frame, text=language.lang("gui.noeffect.check"), command=lambda: self.get_list_effect(self))
        button_browse.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        frame.pack(fill="x")
        self.log_text = ScrolledText(level_conversion_frame, height=10, width=50)
        self.log_text.pack(fill="both", expand=True)
        button_convert = ttk.Button(level_conversion_frame, text=language.lang("gui.noeffect.convert"), command=lambda: self.process_file(self))
        button_convert.pack(fill="x", padx=5, pady=5)
        notebook.add(level_conversion_frame, text=language.lang("gui.noeffect.name"))
        notebook.pack(fill=tk.BOTH, expand=True)
        for i in range(len(self.array_StringVar)):
            self.array_StringVar[i].set("T:"+adofai_const().effect[i])
        self.insert(self, True)

noEffect().main()
################################################################
# Calc UI                                                      #
################################################################

# 创建计算工具帧
calculation_tool_frame = ttk.Frame(notebook)
notebook.add(calculation_tool_frame, text=language.lang("gui.calc.name"))
# 创建 LabelFrame
calc_label_frame = ttk.LabelFrame(calculation_tool_frame, text="PP")
calc_label_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="we")
# 添加等级
calc_level_label = ttk.Label(calc_label_frame, text=language.lang("gui.calc.level"))
calc_level_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
calc_level_combobox = ttk.Combobox(calc_label_frame, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 18.5, 19, 19.5, 20, 20.05, 20.1, 20.15, 20.2, 20.25, 20.3, 20.35, 20.4, 20.45, 20.5, 20.55, 20.6, 20.65, 20.7, 20.75, 20.8, 20.85, 20.9, 20.95, 21, 21.05, 21.1, 21.15, 21.2, 21.25, 21.3], state="readonly", width=12)
calc_level_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="we")
calc_level_combobox.current(1)
# 添加倍速
calc_speed_label = ttk.Label(calc_label_frame, text=language.lang("gui.calc.speed"))
calc_speed_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
calc_speed_entry = ttk.Entry(calc_label_frame, width=12)
calc_speed_entry.grid(row=0, column=3, padx=5, pady=5, sticky="we")
# 添加 X 精准
calc_x_accuracy_label = ttk.Label(calc_label_frame, text=language.lang("gui.calc.xacc"))
calc_x_accuracy_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
calc_x_accuracy_entry = ttk.Entry(calc_label_frame, width=12)
calc_x_accuracy_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
# 添加是否空敲
calc_empty_hit_label = ttk.Label(calc_label_frame, text=language.lang("gui.calc.is_tooEarly"))
calc_empty_hit_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
calc_empty_hit_combobox = ttk.Combobox(calc_label_frame, values=[language.lang('yes'), language.lang('no')], state="readonly", width=12)
calc_empty_hit_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="we")
calc_empty_hit_combobox.current(1)  # 默认选择否
# 添加是否首通
calc_first_clear_label = ttk.Label(calc_label_frame, text=language.lang("gui.calc.is_firstClear"))
calc_first_clear_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
calc_first_clear_combobox = ttk.Combobox(calc_label_frame, values=[language.lang('yes'), language.lang('no')], state="readonly", width=12)
calc_first_clear_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="we")
calc_first_clear_combobox.current(1)  # 默认选择否
# 添加世界排名输入框
world_rank_label = ttk.Label(calc_label_frame, text=language.lang("gui.calc.is_rank"))
world_rank_label.grid(row=2, column=2, padx=5, pady=5, sticky="e")
world_rank_entry = ttk.Entry(calc_label_frame, width=12)
world_rank_entry.grid(row=2, column=3, padx=5, pady=5, sticky="we")
#计算按钮
calculate_button_pp = ttk.Button(calc_label_frame, text=language.lang("gui.calc.calcScore"), command=calc.clac_score)
calculate_button_pp.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

################################################################
# Search Chart UI                                              #
################################################################

# 创建一个 Frame 用于容纳两个 Frame
get_level_info_frame = ttk.Frame(app)
get_level_info_frame.pack(fill="both", expand=True, padx=10, pady=10)
# 通过ID查询部分
frame_id = ttk.Labelframe(get_level_info_frame,text=language.lang("gui.levelsearch.search_id"))
frame_id.pack(fill="x", padx=10, pady=5)
combo_box_values = ["TUF", "ADOFAI.GG", "AQR"]  # 替换为您的选项
combo_box = ttk.Combobox(frame_id, values=combo_box_values, state="readonly")
combo_box.current(0)  # 设置默认选择
combo_box.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
label_id = ttk.Label(frame_id, text=language.lang("gui.levelsearch.id"))
label_id.grid(row=0, column=0, padx=5, pady=5)
entry_id = ttk.Entry(frame_id,width=35)
entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
button_search_id = ttk.Button(frame_id, text=language.lang("gui.levelsearch.search"), command=search.use_id)
button_search_id.grid(row=0, column=2, padx=5, pady=5)
# 通过信息查询部分
frame_info = ttk.Labelframe(get_level_info_frame,text=language.lang("gui.levelsearch.info_search"))
frame_info.pack(fill="x", padx=10, pady=5)
label_artist = ttk.Label(frame_info, text=language.lang("gui.levelsearch.artist"))
label_artist.grid(row=0, column=0, padx=5, pady=5)
entry_artist = ttk.Entry(frame_info,width=35)
entry_artist.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
label_music = ttk.Label(frame_info, text=language.lang("gui.levelsearch.song"))
label_music.grid(row=1, column=0, padx=5, pady=5)
entry_music = ttk.Entry(frame_info,width=35)
entry_music.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
label_author = ttk.Label(frame_info, text=language.lang("gui.levelsearch.author"))
label_author.grid(row=2, column=0, padx=5, pady=5)
entry_author = ttk.Entry(frame_info,width=35)
entry_author.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
button_search_info = ttk.Button(frame_info, text=language.lang("gui.levelsearch.search"), command=search.query)
button_search_info.grid(row=3, columnspan=2, padx=5, pady=5, sticky="ew")
# 日志部分
frame_log2 = ttk.Frame(get_level_info_frame)
frame_log2.pack(fill="both", expand=True, padx=10, pady=5)
log_text2 = ScrolledText(frame_log2, height=10, width=50)
log_text2.pack(fill="both", expand=True)
notebook.add(get_level_info_frame, text=language.lang("gui.levelsearch.name"))

################################################################
# File Download UI                                             #
################################################################

# Google Drive Section
file_dn = ttk.Frame(app)
g_drive = ttk.LabelFrame(file_dn, text="Google Drive[Use ID]")
g_drive.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

g_file_id_entry = ttk.Entry(g_drive, width=48)
g_file_id_entry.grid(row=0, column=0, padx=5, pady=5)

g_download_button = ttk.Button(g_drive, text=language.lang("gui.filedownload.download"),command=downloadFile.google_drive_download)
g_download_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Direct Link Section
d_file = ttk.LabelFrame(file_dn, text="discord[Use Link]")
d_file.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

d_file_link = tk.StringVar()
d_file_link_entry = ttk.Entry(d_file, width=48)
d_file_link_entry.grid(row=0, column=0, padx=5, pady=5)

d_download_button = ttk.Button(d_file, text=language.lang("gui.filedownload.download"), command=downloadFile.discord_download)
d_download_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Download Setting Section
dn_setting = ttk.Frame(file_dn)
dn_setting.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

dn_path_label = ttk.Label(dn_setting, text=language.lang("gui.filedownload.save_path"))
dn_path_label.grid(row=1, column=0, padx=5, pady=5)

dn_path = ttk.Entry(dn_setting)
dn_path.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

browse_button = ttk.Button(dn_setting, text=language.lang("gui.filedownload.browse"), command=downloadFile.select_file)
browse_button.grid(row=1, column=2, padx=5, pady=5)

dn_status = ttk.Label(dn_setting, text=language.lang("gui.filedownload.status"))
dn_status.grid(row=2, column=0, padx=5, pady=5)

dn_progress = ttk.Progressbar(file_dn, orient="horizontal", length=200, mode="determinate")
dn_progress.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=1)

notebook.add(file_dn,text=language.lang("gui.filedownload.name"))

################################################################
# Welcome UI                                                   #
################################################################

# 创建关于页面
page = ttk.Frame(notebook)
notebook.add(page, text=language.lang("gui.about.name"))

label_main = ttk.Label(page, text=language.lang("gui.about.producer"))
label_main.grid(row=0, column=0, padx=10, pady=5, sticky="w")
link_main = ttk.Label(page, text="_Achry_", foreground="blue", cursor="hand2")
link_main.grid(row=0, column=1, padx=10, pady=5, sticky="w")
link_main.bind("<Button-1>", lambda e: webbrowser.open("https://space.bilibili.com/1232092699"))

label_special = ttk.Label(page, text=language.lang("gui.about.specialThanks"))
label_special.grid(row=1, column=0, padx=10, pady=5, sticky="w")
link_special = ttk.Label(page, text="ModsTag", foreground="blue", cursor="hand2")
link_special.grid(row=1, column=1, padx=10, pady=5, sticky="w")
link_special.bind("<Button-1>", lambda e: webbrowser.open("https://space.bilibili.com/496716004"))

label_special = ttk.Label(page, text=language.lang("gui.about.github"))
label_special.grid(row=2, column=0, padx=10, pady=5, sticky="w")
link_special = ttk.Label(page, text="AchryFI/ADOFAI-TOOLS", foreground="blue", cursor="hand2")
link_special.grid(row=2, column=1, padx=10, pady=5, sticky="w")
link_special.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/AchryFI/ADOFAI-TOOLS/"))


label_contact = ttk.Label(page, text=language.lang("gui.about.contact_us"), font=('Helvetica', 16, 'bold'))
label_contact.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

label_qq = ttk.Label(page, text="QQ：377504570")
label_qq.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

label_uid = ttk.Label(page, text="Bili/UID:1232092699")
label_uid.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")

label_email = ttk.Label(page, text=language.lang("gui.about.email")+":achry@achry.space")
label_email.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

label_changelog = ttk.Label(page, text=language.lang("gui.about.updateLog"), font=('Helvetica', 16, 'bold'))
label_changelog.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="w")

changelog_text = tk.Text(page, height=12, width=63)
changelog_text.grid(row=8, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

################################################################
# Menu UI                                                      #
################################################################

#这里写一个菜单栏，有日志（debug用）
# 创建一个顶级菜单
menubar = ttk.Menu(app)

filemenu = ttk.Menu(menubar, tearoff=False)
filemenu.add_command(label="退出", command=lambda: exit())
menubar.add_cascade(label="文件", menu=filemenu)

editmenu = ttk.Menu(menubar, tearoff=False)
editmenu.add_command(label="日志",command=menuFunction.show_log_ui)
menubar.add_cascade(label="调试", menu=editmenu)

# 显示菜单
app.config(menu=menubar)

""""""

# 插入默认更新日志
default_changelog = [
    "版本 1.0.1:\n- 更删除了欢迎页面，添加了关于页面\n- 将f-string外层单引号改为双引号",
    "版本 1.0.2:\n- 允许选择不需要删除的特效类型 并且允许它保存在Non-Effect里\n- 在文件下载中添加了进度栏\n- 添加了logging 库\n- 添加了日志功能",
    "版本 1.0.3:\n- 删除了logging库 转用log 这使得允许自动保存日志(更方便调试)\n- 更新了日志颜色区分",
    "版本 1.0.4:\n- 优化noeffect逻辑\n- 添加中英注释\n- (未完成)优化代码排版",
]
for i in default_changelog:
    changelog_text.insert(tk.END, i+"\n")

# 禁止编辑更新日志文本框
changelog_text.config(state=tk.DISABLED)
# 启动Tkinter的事件循环
app.mainloop()
