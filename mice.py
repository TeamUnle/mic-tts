from pygame import mixer
from urllib import parse
from pygame._sdl2 import get_num_audio_devices, get_audio_device_name
import pygame, keyboard, requests, os
mixer.init()
print('[아래중 입력]\n'+'\n'.join([get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))]))
mixer.quit()
mixer.init(devicename=input("디바이스 이름: "))
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
        return print("cant find sound file")
def down(url):
    """download tts"""
    try:
        r = requests.get(url)
        r.raise_for_status()
        # if 'Server Error' in r.text:
        #     return False
        f = open("./voice.mp3", "wb")
        f.write(r.content)
        f.close()
        return 'voice.mp3'
    except:
        print('cant download the tts file')
        os.remove('./voice.mp3')
        return False

def tts(txt):
    """speak tts"""
    txt = txt.replace("'", '')
    mi = down(f"https://tts-translate.kakao.com/newtone?message=%s"%parse.quote(txt))
    if mi:
        return play(mi)
print('stop playing is F7')

if __name__ == "__main__":
    if not os.path.isdir('./sounds/'):
        print('starting settings...')
        try:
            os.mkdir('./sounds/')
        except:
            print('cant make the folder!')
        print('finished setting!')
    while 1:
        an = input('play: ')
        if an.startswith("/"):
            if an == '/':
                files = list(map(lambda x:os.path.splitext(x)[0], os.listdir('./sounds/')))
                if not len(files):
                    files.append("None")
                print(f'-Sounds-\n<%s>'%'>\n<'.join(files))
                continue
            play(f'./sounds/%s.mp3'%an[1:], 0.3)
        else:
            tts(an)