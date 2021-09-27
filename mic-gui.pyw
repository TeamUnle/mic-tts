from pygame import mixer
from urllib import parse
from gtts import gTTS
import pygame
import requests, os, pypresence
from tkinter import *
from tkinter.messagebox import showerror
from tkinter.ttk import Combobox
from pygame._sdl2 import get_num_audio_devices, get_audio_device_name

discord = pypresence.Presence("863718334696128533")

if not os.path.isdir('./sounds/'):
    try:
        os.mkdir('./sounds/')
    except:
        print('cant make the folder!')
try:
    discord.connect()
    discord.update(
        large_image="mint_choco",
        state="파이썬 스테레오 믹스 프로젝트",
        details="★뀨♥라리엘♥뀨★#1004과 \앱#5120이 제작한",
        buttons=[
            {
                "label": "다운로드",
                "url":"https://github.com/TeamUnle/mic-tts"
            }
        ]
    )
except Exception as x:
    print(x)

ii = 0
window = Tk()
window.title( 'tts!' )
window.resizable(False, False)
frame = Frame( window )
wowbox = Listbox( frame, width=40,height=30)
def stop():
    """stop function"""
    if mixer.get_init() == None:
        return showerror('에러', '마이크를 먼저 선택하세요!')
    mixer.music.stop()
    mixer.music.unload()
def play(music, vol=0.7):
    stop()
    """play music function"""
    try:
        mixer.music.load(music)
        mixer.music.set_volume(vol)
        mixer.music.play(0)
    except:
        return print("cant find sound file")
def down(url):
    """download tts"""
    try:
        r = requests.get(url)
        r.raise_for_status()
        if len(r.content) == 360:
            return 'sans'
        f = open("./voice.mp3", "wb")
        f.write(r.content)
        f.close()
        return './voice.mp3'
    except:
        print('cant download the tts file')
        os.remove('./voice.mp3')
        return False
def tts(event):
    """speak tts"""
    stop()
    txt = entry.get()
    entry.delete(0, 'end')
    mi = down(f"https://tts-translate.kakao.com/newtone?message=%s"%parse.quote(txt))
    globals()["wowbox"].insert(ii, txt)
    globals()["ii"] += 1
    if mi:
        if mi != 'sans':
            return play(mi, globals()["value"] / 10000)
        tts = gTTS(text=txt, lang='ko', slow=False)
        if txt.startswith('`en '):
            tts = gTTS(text=txt[4:], lang='en', slow=False)
        tts.save('./voice.mp3')
        return play('./voice.mp3')

scrollbar=Scrollbar(frame)
scrollbar.pack(side="right", fill="y")
listbox = Listbox( frame, width=40,height=30, yscrollcommand = scrollbar.set)
i = 0
files = list(map(lambda x:os.path.splitext(x)[0], os.listdir('./sounds/')))
if not len(files):
    listbox.insert( 1, 'None' )
else:
    for item in files:
        listbox.insert(i, files[i])
        i+=1
def select(self):
    if mixer.get_init() == None:
        print('v')
        return showerror('에러', '마이크를 먼저 선택하세요!')
    globals()["value"]=scale.get()
    mixer.music.set_volume(globals()["value"] / 10000)
def callback(event):
    if mixer.get_init() == None:
        print('l')
        return showerror('에러', '마이크를 먼저 선택하세요!')
    stop()
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        play('./sounds/' + data + '.mp3', globals()["value"] / 10000)
def callb(event):
    if mixer.get_init() == None:
        print('r')
        return showerror('에러', '마이크를 먼저 선택하세요!')
    stop()
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        mi = down(f"https://tts-translate.kakao.com/newtone?message=%s"%parse.quote(data))
        if mi:
            if mi != 'sans':
                return play(mi, globals()["value"] / 10000)
            tts = gTTS(text=data, lang='ko', slow=False)
            if data.startswith('`en '):
                tts = gTTS(text=data[4:], lang='en', slow=False)
            tts.save('./voice.mp3')
            return play('./voice.mp3')
listbox.pack( side = LEFT )
wowbox.pack(side = RIGHT)
scrollbar["command"]=listbox.yview
listbox.bind("<<ListboxSelect>>", callback)
wowbox.bind("<<ListboxSelect>>", callb)
button = Button(window, width=30, command=stop, repeatdelay=100, repeatinterval=100, text="정지")
button.pack( side = BOTTOM)
entry=Entry(window,width=30)
entry.bind("<Return>", tts)
entry.pack( side = BOTTOM)
var=IntVar()
var.set(3000)
value = 3000
scale=Scale(window, variable=var, command=select, orient="horizontal", showvalue=True, tickinterval=2000, to=10000, length=300, label="음량 조절")
scale.pack(side = BOTTOM)
frame.pack( padx = 30, pady = 50 )
listbox.bind("<Return>", tts)

sel_window = Toplevel(window)
sel_window.wm_transient(window)
sel_window.title('select input')
sel_window.resizable(False, False)
sel_window.geometry('240x120')
window.eval(f'tk::PlaceWindow {str(sel_window)} center')
sel_comb = Combobox(sel_window, state='readonly')

def sel_mic():
    index = sel_comb.get()
    if index:
        mixer.init(devicename=index)
        sel_window.destroy()

sel_button = Button(sel_window, width=10, repeatdelay=100, repeatinterval=100, text='확인', command=sel_mic)
sel_button.pack()

pygame.init()
devices = [get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))]
pygame.quit()

sel_comb['values'] = [x for x in devices if 'cable' in x.lower()]
sel_comb.current(0)
sel_comb.pack()

window.mainloop()
