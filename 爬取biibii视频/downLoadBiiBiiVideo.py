import os
from threading import Thread
import requests
import re
from bs4 import BeautifulSoup
import json
import subprocess
from tkinter import  messagebox
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
# 请求头
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        "Referer": "https://www.bilibili.com/",
        "Cookie":"自己的用户cookie"
    };
def downloadResource(sourceUrl,url, fileName, fileType,logFile):
    print(f"正在下载[{fileName}.{fileType}]中.......")
    data = requests.get(url, headers=headers);
    file_size = int(data.headers['content-length']);
    index = 0;
    if data.status_code == 200:
        with open(f"log\\{logFile}", 'a+', encoding="UTF-8") as log:
            address = '视频地址' if fileType == 'mp4' else '音频地址';
            vieaoUrlInfo = f"源地址：{sourceUrl}===>标题：{fileName}===>{address}：{url}";
            log.write(vieaoUrlInfo);
            log.write("\n");
        with open(f"{fileName}.{fileType}", 'wb') as w:
            for chunk in data.iter_content(chunk_size=1048576):
                w.write(chunk);
                index += 1048576;
                progress_bar['value'] = index / file_size * 100

            print("下载成功")
    return fileName + "." + fileType;

def downloadVideo(url):
    videaData = requests.get(url, headers=headers);
    playinfo = re.findall(r'<script>window.__playinfo__=(.*?)</script>', videaData.text)[0];
    soup = BeautifulSoup(videaData.text, 'html.parser');
    title = soup.find("h1", {"class": "video-title special-text-indent"}).text;
    playinfo = json.loads(playinfo);
    videoUrl = playinfo['data']['dash']['video'][1]['baseUrl'];
    audioUrl = playinfo['data']['dash']['audio'][0]['baseUrl'];
    title = title.replace(' ','').replace('/','').replace("//",'').replace("\\",'');
    videoFile_path = downloadResource(url,videoUrl, title, "mp4","VideoUrllog.txt");
    audioFile_path = downloadResource(url,audioUrl, title, "mp3","AudioUrllog.txt");
    mergeVideoFilePath = "video/" + title + ".mp4";

    # 通过ffmpeg将视频和音频合并
    mergeCommand = f"ffmpeg -i {videoFile_path} -i {audioFile_path} -c:v copy -c:a aac -strict experimental {mergeVideoFilePath}";
    progress_bar.forget();
    merge_label.pack();
    res = subprocess.run(mergeCommand);
    if res.returncode == 0:
        messagebox.showinfo("提示", "下载成功!");
        if os.path.exists(videoFile_path) and os.path.exists(audioFile_path):
            os.remove(videoFile_path);
            os.remove(audioFile_path);
    else:
        messagebox.showinfo("错误", "下载失败!!");
    merge_label.forget();
    progress_bar.pack();

def confirm_action(url):
    if not url:
        messagebox.showerror("错误", "地址不能为空");
    elif not url.isascii():
        messagebox.showerror("错误", "输入不合法");
    elif "https://www.bilibili.com/video/" not in url:
        messagebox.showerror("错误", "只能是B站的视频地址");
    else:
        Thread(target=downloadVideo, args=(url,)).start();

def cancel_action():
    print("销毁窗口!")
    root.destroy();

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root = tk.Tk()
root.title("下载B站的视频")
root.geometry("430x150")
root.configure(bg="#D9AFD9")

style = ThemedStyle(root)
style.theme_use('arc')

entry_frame = tk.Frame(root, bg="#D9AFD9")
entry_frame.pack(pady=(20, 0))

label = tk.Label(entry_frame, text="视频地址:", bg="#D9AFD9", fg="black", font=("宋体", 12))
label.grid(row=0, column=0, padx=(10, 5))

text_box = tk.Entry(entry_frame, width=30, bg="white", font=("宋体", 12), relief=tk.GROOVE)
text_box.grid(row=0, column=1)

button_frame = tk.Frame(root, bg="#D9AFD9",padx=25, pady=25)
button_frame.pack()

confirm_button = ttk.Button(button_frame, text="下载", command=lambda: confirm_action(text_box.get()), style="AccentButton.TButton")
confirm_button.grid(row=0, column=0, padx=(10, 5))

cancel_button = ttk.Button(button_frame, text="取消", command=cancel_action, style="DangerButton.TButton")
cancel_button.grid(row=0, column=1, padx=(5, 10))

style.configure("AccentButton.TButton", background="#4CAF50", foreground="#4CAF50")
style.map("AccentButton.TButton", background=[("active", "#45a049")])
style.configure("DangerButton.TButton", background="#F44336", foreground="#F44336")
style.map("DangerButton.TButton", background=[("active", "#d32f2f")])

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
merge_label = tk.Label(root, text="视频合并中...", bg="#D9AFD9", font=("宋体", 12))
progress_bar.pack();
center_window(root)

root.mainloop()