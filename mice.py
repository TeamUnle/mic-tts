from pygame import mixer
from urllib import parse
import pygame, keyboard, requests, os
mixer.init(devicename="CABLE Input(VB-Audio Virtual Cable)")
def play(music, vol=0.7):
    """play music function"""
    def stop():
        """stop function"""
        mixer.music.stop()
        mixer.music.unload()
    try:
        mixer.music.load(music)
        mixer.music.set_volume(vol)
        mixer.music.play(0)
        while mixer.music.get_busy():
            if keyboard.is_pressed('f7'):
                return stop()
            pygame.time.Clock().tick(100)
        return stop()
    except:
        return print("cant find file")
def down(url):
    """download tts"""
    r = requests.get(url)
    r.raise_for_status()
    f = open("./voice.mp3", "wb")
    f.write(r.content)
    f.close()
    return 'voice.mp3'

def tts(txt):
    """speak tts"""
    mi = down(f"https://tts-translate.kakao.com/newtone?message=%s"%parse.quote(txt))
    return play(mi)
print('stop playing is F7')

while 1:
    an = input('play: ')
    if an.startswith("/"):
        if an == '/':
            files = list(map(lambda x:os.path.splitext(x)[0], os.listdir('./sounds/')))
            print(f'-Sounds-\n<%s>'%'>\n<'.join(files))
            continue
        play(f'./sounds/%s.mp3'%an[1:], 0.3)
    else:
        tts(an)