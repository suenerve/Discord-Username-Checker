# This is a very early build you may face some bugs, unknown bugs. But with your informing help, we can make it better.
# Open issues at: https://github.com/suegdu/DSV/issues/new
# NOTE : Spamming Discord's API is against TOS, You may get your account suspended and I am not responsible. For a further caution, Use an alt's token.


TOKEN = "PASTE YOUR TOKEN HERE"


import random
import string 
import requests
import os
import time
import json
from colorama import Fore,Back,init
import sys
init(autoreset=True)
__version__ = "Author: suegdu DSV 1.0"
__github__= "https://github.com/suegdu"

Delay:int = 1 # Seconds

URL = "https://discord.com/api/v9/users/@me"
HEADERS = {
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",

    "Authorization":TOKEN
}
available_usernames = []
dir_path = os.path.dirname(os.path.realpath(__file__))
av_list = os.path.join(dir_path, f"available_usernames.txt")
Lb = Fore.LIGHTBLACK_EX
Ly = Fore.LIGHTYELLOW_EX
def main():
    os.system(f"title {__version__}")
    print(f"""{Fore.LIGHTYELLOW_EX}
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
  {__version__} 
  {__github__}

  ██████╗ ███████╗██╗   ██╗                     
  ██╔══██╗██╔════╝██║   ██║                     
  ██║  ██║███████╗██║   ██║                     
  ██║  ██║╚════██║╚██╗ ██╔╝                     {Fore.LIGHTCYAN_EX}1-{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Generate names and check{Fore.LIGHTBLACK_EX}]{Fore.LIGHTYELLOW_EX}
  ██████╔╝███████║ ╚████╔╝ 
  ╚═════╝ ╚══════╝  ╚═══╝                       {Fore.LIGHTCYAN_EX}2-{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Check a specific list{Fore.LIGHTBLACK_EX}]{Fore.LIGHTYELLOW_EX}

                 
  Discord Username's availability validator.
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
""")
    proc0()
    
def setdelay():
   global Delay
   d_input = input(f"{Lb}[{Ly}Delay (Seconds | Default is 1, the longer the safer avoiding suspension.){Lb}]:> ")
   try:
      int(d_input)
      Delay = int(d_input)
   except ValueError:
      print(f"{Lb}[!]{Fore.RED}Error: You must enter a valid integer. No strings.")
      setdelay()

def proc0():
    m_input = input(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTGREEN_EX}DSV{Fore.LIGHTBLACK_EX}]:> {Fore.LIGHTYELLOW_EX}").lower()
    if m_input=="":
        proc0()
    elif m_input=="2":
        setdelay()
        opt2load()
    elif m_input=="1":
       setdelay()
       opt1load()
    else:
        proc0()
def validate_names(opt,usernames:str):
   global available_usernames
   if opt == 2:
    for username in usernames:
       time.sleep(Delay)
       body = {
           "username": username
       }
       response = requests.patch(URL, headers=HEADERS, data=json.dumps(body))
       if response.status_code == 429:
           sleep_time = response.json()["retry_after"]
           print(f"{Lb}[!]{Fore.RED} Rate limit hit. Sleeping for {sleep_time}s")
           time.sleep(sleep_time)
       if 'errors' in response.json() :
        if 'username' in response.json()['errors']:
           print(f"{Lb}[!]{Fore.RED} '{username}' taken.")
        else :
           print(f"{Lb}[!]{Fore.LIGHTGREEN_EX} '{username}' available.")
       else:
           print(Delay)
           print(f"{Lb}[!]{Fore.RED} Error validating '{username}': {response.json()['message']}")
           input(f"{Fore.YELLOW}Press Enter to exit.")
           sys.exit(0)
   elif opt == 1:

       body = {
           "username": usernames
       }
       response = requests.patch(URL, headers=HEADERS, data=json.dumps(body))
       if response.status_code == 429:
           sleep_time = response.json()["retry_after"]
           print(f"{Lb}[!]{Fore.RED} Rate limit hit. Sleeping for {sleep_time}s")
           time.sleep(sleep_time)
           available_usernames.append(usernames)
       if 'errors' in response.json() :
        if 'username' in response.json()['errors']:
           print(f"{Lb}[!]{Fore.RED} '{usernames}' taken.")
        else :
           print(f"{Lb}[!]{Fore.LIGHTGREEN_EX} '{usernames}' available.")
       else:
           print(f"{Lb}[!]{Fore.RED} Error validating '{usernames}': {response.json()['message']}")
           input(f"{Fore.YELLOW}Press Enter to exit.")
           sys.exit(0)
 
       
def opt2load():
    global av_list
    global dir_path
    list_path = os.path.join(dir_path, f"usernames.txt")
    print(f"{Lb}[!]{Ly}Checking 'usernames.txt' for a valid list...")
    try:
     with open(list_path) as file:
      usernames = [line.strip() for line in file]
      validate_names(2,usernames)
     with open(av_list, "w") as file:
        save()
        print(f"\n{Lb}[!]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
        input(f"{Fore.YELLOW}Press Enter to exit.")
        sys.exit(0)
    except FileNotFoundError:
       print(f"{Lb}[!]{Fore.RED}Error: Couldn't find the list (usernames.txt). Please make sure to create a valid list file in the same directory: \n({dir_path}\\)")
       input(f"{Fore.YELLOW}Press Enter to exit.")
       sys.exit(0)
def opt1load():
   opt1_input:int = input(f"{Lb}[{Ly}How many letters in a username{Lb}]:> ")
   try:
    int(opt1_input)
    if int(opt1_input) >32 or int(opt1_input) <2:
       print(f"{Lb}[!]{Fore.RED}Error: The username must contain at least 2 letters, and not more than 32 letters.")
       opt1load()
    opt2_input:int = input(f"{Lb}[{Ly}How many usernames to generate{Lb}]:> ")
    opt1func(int(opt2_input),int(opt1_input))
   except ValueError:
      print(f"{Lb}[!]{Fore.RED}Error: You must enter a valid integer. No strings.")
      opt1load()
def save():
   with open(av_list, "w") as file:
        file.write("\n".join(available_usernames))
def opt1func(v1,v2):
   for i in range(v1):
    name = get_names(int(v2))
    validate_names(1,name)
    time.sleep(Delay)
   save()
   print(f"\n{Lb}[!]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
   input(f"{Fore.YELLOW}Press Enter to exit.")
   sys.exit(0)

def get_names(length: int) ->str:
   return ''.join(random.sample(string.ascii_letters, length))
    
if __name__ == "__main__":
 main()
