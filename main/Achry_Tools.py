import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
from tkinter import messagebox
from mtlog import *

from win32clipboard import OpenClipboard,SetClipboardData,CloseClipboard
import re
import time
import requests
import webbrowser
import os
import sys
import json
import logging
import traceback
import win32con

logs = ""
mtl = mtlog.new("log")
def log_error(w, l):
    messagebox.showerror(lang("error"), w)
    mtlog.inp(w, l, 3)
    pass
def log_info(w, l):
    messagebox.showinfo(lang("info"), w)
    mtlog.inp(w, l, 1)
    pass
def log_insert(ins, w, l):
    ins.insert(tk.END, w)
    mtlog.inp(w, l, 1)
    pass
#去特效用到的功能
class noEffect:
    @staticmethod
    def select_file():
        filename = askopenfilename()
        if filename:
            if not noEffect.check_file_extension(filename):
                log_error(lang("gui.noeffect.function(except).not_adofai_file"), mtl)
                return
            entry_path.delete(0, tk.END)
            entry_path.insert(tk.END, filename)

    @staticmethod
    def process_file():
        filename = entry_path.get()
        if not filename:
            log_error(lang("gui.noeffect.function(except).not_select_file"), mtl)
            return
        if not noEffect.check_file_extension(filename):
            log_error(lang("gui.noeffect.function(except).not_adofai_file"), mtl)
            return
        start = time.time()
        
        # 在这里处理文件
        try:
            file_contents = open(filename, 'r', encoding='utf8').read()
            # 用正则把传进来的reList遍历一遍
            for i in ["SetObject","AddObject","SetFilterAdvanced","SetFloorIcon","AnimateTrack", "MoveTrack", "MoveDecorations", "SetText", "PositionTrack", "RecolorTrack", "ColorTrack", "CustomBackground", "Flash", "MoveCamera", "SetFilter", "HallOfMirrors", "ShakeScreen", "Bloom", "ScreenTile", "ScreenScroll", "RepeatEvents", "SetConditionalEvents", "AddDecoration", "AddText"]:
                # 设置正则
                regex_pattern = r'{.*?"' + i + r'".*?},'
                # 进行替换操作
                file_contents = re.sub(regex_pattern, '', file_contents)

            file_directory = os.path.dirname(filename)
            open(file_directory+'/Non_effect.adofai','w',encoding="utf8").write(file_contents)

            end_time = time.time()
            log_insert(log_text, repl(repl(lang("gui.noeffect.function(success)"), 1, file_directory), 2, round(end_time-start,3)), mtl)
        except Exception as e:
            messagebox.showerror(lang("error"), repl(repl(lang("gui.noeffect.function(except).error"), 1, e.__class__.__name__), 2, e))
            logger.error(f"An error occurred.\n{traceback.format_exc()}")
   

    @staticmethod
    def check_file_extension(filename):
        return filename.lower().endswith('.adofai')

class Calc:
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
                log_error(lang("gui.calc.function(except).write_empty"), mtl)
                return
            
            if world_rank_entry.get() == '':
                ranked_position = 2147483647
                log_error(lang("gui.calc.function(except).write_rank"), mtl)
            else:
                ranked_position = int(world_rank_entry.get())

            
            no_early = (calc_empty_hit_combobox.get() == lang('no') or xacc == 100)

            world_first = calc_first_clear_combobox == lang('yes')

            
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
                score_base = switch.get(difficult, None)
                ### print(score_base)
                
                #判断基础分是否正确（输入不正确的难度会返回None)看上面代码
                if score_base == None:
                    log_error(lang("gui.calc.function(except).error_level"), mtl)
                    return
            
                #xacc基础分计算
                if xacc == 100:
                    xacc_multi = 7
                elif xacc >= 99.8:
                    xacc_multi = (xacc - 99.73334) * 15 + 3
                elif xacc >= 99:
                    xacc_multi = (xacc - 97) ** 1.5484 - 0.9249
                elif xacc >= 95:
                    xacc_multi = ((xacc - 94) ** 1.6) / 12.1326 + 0.9176
                else:
                    log_error(lang("gui.calc.function(except).xacc_so_low"), mtl)
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
                    repl(repl(lang("gui.calc.function(success)")
                    , 1, (round(base_score * 1,2) if (not world_first) else round(base_score * 1.1,2)))
                    , 2, (round(base_score * ((0.9 ** (ranked_position - 1)) if ranked_position <= 20 else 0), 2)))
                    , mtl
                )
        except Exception as e:
            log_error(repl(repl(lang("gui.noeffect.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)

            logger.error(f"An error occurred.\n{traceback.format_exc()}")

class Search:
    @staticmethod
    def use_id():
        try:
            ### print(combo_box.get())
            if combo_box.get() == 'TUF':
                id = entry_id.get()
                if id == '':
                    log_text2.delete(1.0, tk.END) 
                    log_insert(log_text2, repl(lang("gui.levelsearch.function(except).id_is_empty"), 1, id), mtl)
                    return
                
                response = requests.get(f"https://be.t21c.kro.kr/levels/{id}", headers={"accept": "application/json"})
                info = response.json()

                if 'statusCode' in info:
                    log_text2.delete(1.0, tk.END) 
                    log_insert(log_text2, repl(repl(repl(lang("gui.levelsearch.function(except).status_error"), 1, info["message"]), 2, info["statusCode"]), 3, id), mtl)
                    return
                
                log_text2.delete(1.0, tk.END) 
                log_insert(log_text2, 
                repl(repl(repl(repl(repl(repl(repl(repl(repl(lang("gui.levelsearch.function(TUF_success)")
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
                    log_insert(log_text2, repl(lang("gui.levelsearch.function(except).id_is_empty"), 1, id), mtl)
                    return
                
                response = requests.get(f"https://adofai.gg/api/v1/levels/{id}")
                info = response.json()

                if 'errors' in info:
                    msg = info["errors"][0]
                    log_text2.delete(1.0, tk.END) 
                    log_insert(log_text2, repl(repl(repl(lang("gui.levelsearch.function(except).status_error"), 1, msg["message"]), 2, msg["code"]), 3, id), mtl)
                    return

                log_text2.delete(1.0, tk.END) 
                log_insert(log_text2, 
                repl(repl(repl(repl(repl(repl(repl(repl(repl(repl(lang("gui.levelsearch.function(ADOFAIGG_success)")
                , 1, info['id'])
                , 2, [artist['name'] for artist in info['music']['artists']])
                , 3, info['title'])
                , 4, [creator['name'] for creator in info['creators']])
                , 5, info['difficulty'])
                , 6, info['video'])
                , 7, info['download'])
                , 8, info['workshop'])
                , 9, info['tiles'])
                , 10, [tag['name'] for tag in info['tags']]), mtl)
            
            else:
                id = int(entry_id.get())

                if id == '':
                    log_text2.delete(1.0, tk.END) 
                    log_insert(log_text2, repl(lang("gui.levelsearch.function(except).id_is_empty"), 1, id), mtl)
                    return
                
                aqr = requests.get('https://www.adofaiaqr.top/static/buttonsData.js').text[18:-3]
                id = id-1
                info = eval(aqr)[id]

                log_text2.delete(1.0, tk.END) 
                log_insert(log_text2, 
                repl(repl(repl(repl(repl(repl(repl(repl(lang("gui.levelsearch.function(AQR_success)")
                , 1, info['artist'])
                , 2, info['song'])
                , 3, info['author'])
                , 4, info['difficulties'])
                , 5, info['level'])
                , 6, info['vluation'])
                , 7, info['video_herf'])
                , 8, info['href']), mtl)

                
        except Exception as e:
            log_error( repl(repl(lang("gui.levelsearch.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)
            logger.error(f"An error occurred.\n{traceback.format_exc()}")
            #__import__('traceback').print_exc()

    @staticmethod
    def query():
        try:
            url = f"https://be.t21c.kro.kr/levels?artistQuery={entry_artist.get()}&songQuery={entry_music.get()}&creatorQuery={entry_author.get()}&random=false"
            response = requests.get(url, headers={
                "accept": "application/json"
            })
            info = response.json()
            log_text2.delete(1.0, tk.END)
            log_insert(log_text2, repl(lang("gui.levelsearch.function(find)"), 1, info['count']), mtl)
            for infos in info['results']:
                log_insert(log_text2, 
                repl(repl(repl(repl(repl(repl(repl(repl(repl(lang("gui.levelsearch.function(TUF_success)")
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
            log_error(repl(repl(lang("gui.levelsearch.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)
            logger.error(f"An error occurred.\n{traceback.format_exc()}")

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
            log_error(lang("gui.filedownload.function(except).id_is_empty"))
            return
        url = f"https://hjtbrz.mcfuns.cn/application/test/gdrive.php?id={g_file_id_entry.get()}"

        try:
            # 发起 GET 请求
            response = requests.get(url, stream=True)
            dn_status.configure(text=lang("gui.filedownload.function().downloading"))
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
                        dn_status.configure(text=repl(repl(lang("gui.filedownload.function().downloadingprocess"), 1, round(bytes_written / 1048576,2)), 2, round(file_size / 1048576,2)))
                        app.update_idletasks()
                        dn_progress['value'] = bytes_written / file_size * 100
                    if 'Error 404'.encode(encoding='utf-8') in chunk:
                        log_error(repl(lang("gui.filedownload.function(except).id_not_find"), 1, g_file_id_entry.get()), mtl)
                        os.remove(dn_path.get() + '/' + filename)
                        return

                log_info(repl(lang("gui.filedownload.function(success)"), 1, filename), mtl)
            else:
                log_error(lang("error"), repl(lang("gui.filedownload.function(except).fail"), 1, response.status_code), mtl)
        except Exception as e:
            if e.__class__.__name__ == 'PermissionError':
                log_error(lang("error"), repl(repl(repl(repl(lang("gui.filedownload.function(except).error"), 1, dn_path.get()), 2, filename), 3, e.__class__.__name__), 4, e), mtl)
            else:
                log_error(lang("error"), repl(repl(lang("gui.filedownload.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)
            logger.error(f"An error occurred.\n{traceback.format_exc()}")

    @staticmethod
    def discord_download():
        # 构建请求的 URL
        if d_file_link_entry.get() == '':
            log_error(lang("gui.filedownload.function(except).link_is_empty"), mtl)
            return

        try:
            # 发起 GET 请求
            response = requests.get(f'https://hjtbrz.mcfuns.cn/application/test/download.php?file_url={d_file_link_entry.get()}', stream=True)
            dn_status.configure(text=lang("gui.filedownload.function().downloading"))
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
                        dn_status.configure(text=repl(repl(lang("gui.filedownload.function().downloadingprocess"), 1, round(bytes_written / 1048576,2)), 2, round(file_size / 1048576,2)))
                        app.update_idletasks()
                        dn_progress['value'] = bytes_written / file_size * 100
                    if 'Error 404'.encode(encoding='utf-8') in chunk or not chunk:
                        log_error(repl(lang("gui.filedownload.function(except).link_not_find"), 1, g_file_id_entry.get()), mtl)
                        os.remove(dn_path.get() + '/' + filename)
                        return

                log_info(repl(lang("gui.filedownload.function(success)"), 1, filename), mtl)
            else:
                log_error(repl(lang("gui.filedownload.function(except).fail"), 1, response.status_code), mtl)
        except Exception as e:
            if e.__class__.__name__ == 'PermissionError':
                log_error(repl(repl(repl(repl(lang("gui.filedownload.function(except).error"), 1, dn_path.get()), 2, filename), 3, e.__class__.__name__), 4, e), mtl)
            else:
                log_error(repl(repl(lang("gui.filedownload.function(except).error"), 1, e.__class__.__name__), 2, e), mtl)
            logger.error(f"An error occurred.\n{traceback.format_exc()}")


class MenuFunction:

    @staticmethod
    def show_log_ui():
        global log_text_debug, logs
 
        # 新开一个窗口 一个日志界面，有一个框，可以保存日志和复制日志
        log_window = tk.Toplevel(app)
        log_window.title(lang("gui.log.name"))
        log_window.geometry("480x540")
        log_window.resizable(0, 0)
        log_text_debug = ScrolledText(log_window, height=10, width=50, font=("Consolas", 8))
        log_text_debug.pack(fill="both", expand=True)
        log_text_debug.text.config(state=tk.DISABLED)
        # Configure a tag for error messages in red
        log_text_debug.text.config(state=tk.NORMAL)
        # Insert logs into the text widget, highlighting errors in red
        log_text_debug.tag_configure("debug", foreground="gray")
        log_text_debug.tag_configure("info", foreground="green")
        log_text_debug.tag_configure("warning", foreground="orange")
        log_text_debug.tag_configure("error", foreground="red")
        log_text_debug.tag_configure("critical", foreground="purple")

        # wait Achry Edit...
        print(mtlog.out(mtl))
        log_text_debug.insert(tk.END, mtlog.out(mtl))
        logs_lines = logs.split('\n')  # Assuming logs is a string with newline-separated entries
        0
        for line in logs_lines:
             if "error" in line.lower():      log_text_debug.insert("end", line + '\n', "error")
             elif "debug" in line.lower():    log_text_debug.insert("end", line + '\n', "debug")
             elif "info" in line.lower():     log_text_debug.insert("end", line + '\n', "info")
             elif "warning" in line.lower():  log_text_debug.insert("end", line + '\n', "warning")
             else:                            log_text_debug.insert("end", line + '\n', "critical")
            
        log_text_debug.text.config(state=tk.DISABLED)
        button_save = tk.Button(log_window, text=lang("gui.log.save"), command=MenuFunction.save_log)
        button_save.pack(fill="x")
        button_copy = tk.Button(log_window, text=lang("gui.log.copy"), command=lambda: MenuFunction.write_clipboard(logs))
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
        messagebox.showinfo(lang("gui.log.function(copy_success)"), lang("gui.log.function(copy_success)"))

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


#我超这边
def repl(string:str, id:int, to:str):
    to = str(to)
    return string.replace("${%s}"%id, to)

def lang(string:str):
    if not os.path.exists("lang.json"):
        messagebox.showerror("error", "Can't read the lang file.If the language file does exist and it still shows this error, contact the developer, or try the following method: \n\nput the program in the English path (without special symbols)")
        sys.exit();
    array = string.split(".")
    try:
        js = json.loads(open("lang.json", 'r', encoding="UTF-8").read())
    except Exception as e:
        messagebox.showerror("error", "file data can't convert to json, please re-download lang.json and pause to \"%s\""%__file__)
    ret = js["language"][js["getNowLanguage"]]
    try: 
        for i in array: ret = ret[i]
    except Exception as e:
        messagebox.showerror('error',"No get lang \"%s\" as lang.json. Please check if your language file is corrupted, and if that doesn't work, contact the developer"%string)
        logger.error("No get lang \"%s\" as lang.json."%string)
        return ""
    return str(ret)


# 创建一个继承自 logging.Handler 的自定义日志处理器
class CustomHandler(logging.Handler):
    def emit(self, record):
        # 使用日志记录的消息调用自定义函数
        log_message = self.format(record)
        MenuFunction.insert_line_log(log_message)

# 创建一个日志记录器
logger = logging.getLogger('')
logger.setLevel(logging.INFO)

# 创建自定义处理器的实例，并添加到日志记录器
custom_handler = CustomHandler()
logger.addHandler(custom_handler)

# 配置日志消息的格式
formatter = logging.Formatter('[%(asctime)s/%(levelname)s]: %(message)s\n')
custom_handler.setFormatter(formatter)



app = tk.Tk()
app.title("ADOFAI Tools _ v1.O.1 _ _Achry_")
app.geometry("480x540")
# 创建Notebook
notebook = ttk.Notebook(app, bootstyle='info')


"""

------------
去特效ui
___________

"""
level_conversion_frame = ttk.Frame(app)
frame = ttk.Frame(level_conversion_frame)
label_path = ttk.Label(frame, text=lang("gui.noeffect.file_path"))
label_path.grid(row=0, column=0, padx=5, pady=5)
entry_path = ttk.Entry(frame, width=30)
entry_path.grid(row=0, column=1, padx=5, pady=5)
button_browse = ttk.Button(frame, text=lang("gui.noeffect.browse"), command=noEffect.select_file)
button_browse.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
label_path = ttk.Label(frame, text=lang("gui.noeffect.unremoved"))
label_path.grid(row=1, column=0, padx=5, pady=5)
uneffect = ttk.Entry(frame, width=30)
uneffect.grid(row=1, column=1, padx=5, pady=5)
frame.pack(fill="x")
log_text = ScrolledText(level_conversion_frame, height=10, width=50)
log_text.pack(fill="both", expand=True)
button_convert = ttk.Button(level_conversion_frame, text=lang("gui.noeffect.convert"), command=noEffect.process_file)
button_convert.pack(fill="x", padx=5, pady=5)
notebook.add(level_conversion_frame, text=lang("gui.noeffect.name"))

"""

------------
计算工具ui
___________

"""
notebook.pack(fill=tk.BOTH, expand=True)
# 创建计算工具帧
calculation_tool_frame = ttk.Frame(notebook)
notebook.add(calculation_tool_frame, text=lang("gui.calc.name"))
# 创建 LabelFrame
calc_label_frame = ttk.LabelFrame(calculation_tool_frame, text="PP")
calc_label_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="we")
# 添加等级
calc_level_label = ttk.Label(calc_label_frame, text=lang("gui.calc.level"))
calc_level_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
calc_level_combobox = ttk.Combobox(calc_label_frame, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "18.5", "19", "19.5", "20", "20.05", "20.1", "20.15", "20.2", "20.25", "20.3", "20.35", "20.4", "20.45", "20.5", "20.55", "20.6", "20.65", "20.7", "20.75", "20.8", "20.85", "20.9", "20.95", "21", "21.05", "21.1", "21.15", "21.2", "21.25", "21.3"], state="readonly", width=12)
calc_level_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="we")
calc_level_combobox.current(1)
# 添加倍速
calc_speed_label = ttk.Label(calc_label_frame, text=lang("gui.calc.speed"))
calc_speed_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
calc_speed_entry = ttk.Entry(calc_label_frame, width=12)
calc_speed_entry.grid(row=0, column=3, padx=5, pady=5, sticky="we")
# 添加 X 精准
calc_x_accuracy_label = ttk.Label(calc_label_frame, text=lang("gui.calc.xacc"))
calc_x_accuracy_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
calc_x_accuracy_entry = ttk.Entry(calc_label_frame, width=12)
calc_x_accuracy_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
# 添加是否空敲
calc_empty_hit_label = ttk.Label(calc_label_frame, text=lang("gui.calc.is_tooEarly"))
calc_empty_hit_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
calc_empty_hit_combobox = ttk.Combobox(calc_label_frame, values=[lang('yes'), lang('no')], state="readonly", width=12)
calc_empty_hit_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="we")
calc_empty_hit_combobox.current(1)  # 默认选择否
# 添加是否首通
calc_first_clear_label = ttk.Label(calc_label_frame, text=lang("gui.calc.is_firstClear"))
calc_first_clear_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
calc_first_clear_combobox = ttk.Combobox(calc_label_frame, values=[lang('yes'), lang('no')], state="readonly", width=12)
calc_first_clear_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="we")
calc_first_clear_combobox.current(1)  # 默认选择否
# 添加世界排名输入框
world_rank_label = ttk.Label(calc_label_frame, text=lang("gui.calc.is_rank"))
world_rank_label.grid(row=2, column=2, padx=5, pady=5, sticky="e")
world_rank_entry = ttk.Entry(calc_label_frame, width=12)
world_rank_entry.grid(row=2, column=3, padx=5, pady=5, sticky="we")
#计算按钮
calculate_button_pp = ttk.Button(calc_label_frame, text=lang("gui.calc.calcScore"), command=Calc.clac_score)
calculate_button_pp.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")



"""

------------
关卡查询ui
___________

"""
# 创建一个 Frame 用于容纳两个 Frame
get_level_info_frame = ttk.Frame(app)
get_level_info_frame.pack(fill="both", expand=True, padx=10, pady=10)
# 通过ID查询部分
frame_id = ttk.Labelframe(get_level_info_frame,text=lang("gui.levelsearch.search_id"))
frame_id.pack(fill="x", padx=10, pady=5)
combo_box_values = ["TUF", "ADOFAI.GG", "AQR"]  # 替换为您的选项
combo_box = ttk.Combobox(frame_id, values=combo_box_values, state="readonly")
combo_box.current(0)  # 设置默认选择
combo_box.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
label_id = ttk.Label(frame_id, text=lang("gui.levelsearch.id"))
label_id.grid(row=0, column=0, padx=5, pady=5)
entry_id = ttk.Entry(frame_id,width=35)
entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
button_search_id = ttk.Button(frame_id, text=lang("gui.levelsearch.search"), command=Search.use_id)
button_search_id.grid(row=0, column=2, padx=5, pady=5)
# 通过信息查询部分
frame_info = ttk.Labelframe(get_level_info_frame,text=lang("gui.levelsearch.info_search"))
frame_info.pack(fill="x", padx=10, pady=5)
label_artist = ttk.Label(frame_info, text=lang("gui.levelsearch.artist"))
label_artist.grid(row=0, column=0, padx=5, pady=5)
entry_artist = ttk.Entry(frame_info,width=35)
entry_artist.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
label_music = ttk.Label(frame_info, text=lang("gui.levelsearch.song"))
label_music.grid(row=1, column=0, padx=5, pady=5)
entry_music = ttk.Entry(frame_info,width=35)
entry_music.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
label_author = ttk.Label(frame_info, text=lang("gui.levelsearch.author"))
label_author.grid(row=2, column=0, padx=5, pady=5)
entry_author = ttk.Entry(frame_info,width=35)
entry_author.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
button_search_info = ttk.Button(frame_info, text=lang("gui.levelsearch.search"), command=Search.query)
button_search_info.grid(row=3, columnspan=2, padx=5, pady=5, sticky="ew")
# 日志部分
frame_log2 = ttk.Frame(get_level_info_frame)
frame_log2.pack(fill="both", expand=True, padx=10, pady=5)
log_text2 = ScrolledText(frame_log2, height=10, width=50)
log_text2.pack(fill="both", expand=True)
notebook.add(get_level_info_frame, text=lang("gui.levelsearch.name"))

"""

------------
文件下载ui
___________

"""

# Google Drive Section
file_dn = ttk.Frame(app)
g_drive = ttk.LabelFrame(file_dn, text="Google Drive[Use ID]")
g_drive.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

g_file_id_entry = ttk.Entry(g_drive, width=48)
g_file_id_entry.grid(row=0, column=0, padx=5, pady=5)

g_download_button = ttk.Button(g_drive, text=lang("gui.filedownload.download"),command=downloadFile.google_drive_download)
g_download_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Direct Link Section
d_file = ttk.LabelFrame(file_dn, text="discord[Use Link]")
d_file.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

d_file_link = tk.StringVar()
d_file_link_entry = ttk.Entry(d_file, textvariable=d_file_link, width=48)
d_file_link_entry.grid(row=0, column=0, padx=5, pady=5)

d_download_button = ttk.Button(d_file, text=lang("gui.filedownload.download"), command=downloadFile.discord_download)
d_download_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Download Setting Section
dn_setting = ttk.Frame(file_dn)
dn_setting.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

dn_path_label = ttk.Label(dn_setting, text=lang("gui.filedownload.save_path"))
dn_path_label.grid(row=1, column=0, padx=5, pady=5)

dn_path = ttk.Entry(dn_setting)
dn_path.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

browse_button = ttk.Button(dn_setting, text=lang("gui.filedownload.browse"), command=downloadFile.select_file)
browse_button.grid(row=1, column=2, padx=5, pady=5)

dn_status = ttk.Label(dn_setting, text=lang("gui.filedownload.status"))
dn_status.grid(row=2, column=0, padx=5, pady=5)

dn_progress = ttk.Progressbar(file_dn, orient="horizontal", length=200, mode="determinate")
dn_progress.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=1)

notebook.add(file_dn,text=lang("gui.filedownload.name"))

"""

------------
欢迎ui
___________

"""

# 创建关于页面
page = ttk.Frame(notebook)
notebook.add(page, text=lang("gui.about.name"))

label_main = ttk.Label(page, text=lang("gui.about.producer"))
label_main.grid(row=0, column=0, padx=10, pady=5, sticky="w")
link_main = ttk.Label(page, text="_Achry_", foreground="blue", cursor="hand2")
link_main.grid(row=0, column=1, padx=10, pady=5, sticky="w")
link_main.bind("<Button-1>", lambda e: webbrowser.open("https://space.bilibili.com/1232092699"))

label_special = ttk.Label(page, text=lang("gui.about.specialThanks"))
label_special.grid(row=1, column=0, padx=10, pady=5, sticky="w")
link_special = ttk.Label(page, text="ModsTag", foreground="blue", cursor="hand2")
link_special.grid(row=1, column=1, padx=10, pady=5, sticky="w")
link_special.bind("<Button-1>", lambda e: webbrowser.open("https://space.bilibili.com/496716004"))

label_contact = ttk.Label(page, text=lang("gui.about.contact_us"), font=('Helvetica', 16, 'bold'))
label_contact.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

label_qq = ttk.Label(page, text="QQ：377504570")
label_qq.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

label_uid = ttk.Label(page, text="Bili/UID:1232092699")
label_uid.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

label_email = ttk.Label(page, text=lang("gui.about.email")+":37750470@qq.com")
label_email.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")

label_changelog = ttk.Label(page, text=lang("gui.about.updateLog"), font=('Helvetica', 16, 'bold'))
label_changelog.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="w")

changelog_text = tk.Text(page, height=3, width=50)
changelog_text.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

"""

------------
菜单ui
___________

"""

#这里写一个菜单栏，有日志（debug用）
# 创建一个顶级菜单
menubar = ttk.Menu(app)

filemenu = ttk.Menu(menubar, tearoff=False)
filemenu.add_command(label="退出", command=lambda: exit())
menubar.add_cascade(label="文件", menu=filemenu)

editmenu = ttk.Menu(menubar, tearoff=False)
editmenu.add_command(label="日志",command=MenuFunction.show_log_ui)
menubar.add_cascade(label="调试", menu=editmenu)

# 显示菜单
app.config(menu=menubar)

""""""

# 插入默认更新日志
default_changelog = "版本 1.0.1:\n- 更删除了欢迎页面，添加了关于页面\n- 将f-string外层单引号改为双引号"
changelog_text.insert(tk.END, default_changelog)

# 禁止编辑更新日志文本框
changelog_text.config(state=tk.DISABLED)
# 启动Tkinter的事件循环
app.mainloop()
