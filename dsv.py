# Author: suegdu
# I demand my credits to the code wherever it's used.
# Open issues at: https://github.com/suegdu/DSV/issues/new
# NOTE : Spamming Discord's API is against TOS, You may get your account suspended and I am not responsible. For a further caution, use an alt's token and a higher delay.




import random
import string 
import requests
import os
import time
import json
from colorama import Fore,Back,init
from configparser import ConfigParser
import sys
init(autoreset=True)
__version__ = "Author: suegdu DSV 1.8"
__github__= "https://github.com/suegdu"
dir_path = os.path.dirname(os.path.realpath(__file__))
configur = ConfigParser()
configur.read(os.path.join(dir_path, f"config.ini"))

sys_url = "https://discord.com/api/v9/users/@me"
URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"
HEADERS = {
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",

    "Authorization":configur.get("sys","TOKEN")
}
available_usernames = []
av_list = os.path.join(dir_path, f"available_usernames.txt")
sample_0 = r"_."
Lb = Fore.LIGHTBLACK_EX
Ly = Fore.LIGHTYELLOW_EX
Delay = configur.getfloat("other","default_delay")
def setconf():
   global string_0
   global digits_0
   global punctuation_0
   global sat_string
   global sat_digits
   global sat_punct
   sat_string = configur.getboolean("config","string")
   sat_digits = configur.getboolean("config","digits")
   sat_punct = configur.getboolean("config","punctuation")
   if sat_string == True:
      string_0 = string.ascii_lowercase
   elif sat_string == False:
      string_0 = ""
   else:
      string_0 = string.ascii_lowercase
      sat_string = True
   if sat_digits == True:
      digits_0 = string.digits
   elif sat_digits == False:
      digits_0 = ""
   else:
      digits_0 = string.digits
      sat_digits = True
   if sat_punct == True:
      punctuation_0 = sample_0
   elif sat_punct == False:
      punctuation_0 = ""
   else:
      punctuation_0 = sample_0
      sat_punct = True
   if sat_punct == False and sat_digits == False and sat_string == False:
      punctuation_0 = sample_0
      digits_0 = string.digits
      string_0 = string.ascii_lowercase

def main():
    if configur.get("sys","TOKEN") == "":
        print(f"{Lb}[!]{Fore.RED} No token found. You must paste your token inside the 'config.ini' file, in front of the value 'TOKEN'.")
        exit()
    os.system(f"title {__version__} - Connected as {requests.get(sys_url,headers=HEADERS).json()['username']}")
    setconf()    
    print(f"""{Fore.LIGHTYELLOW_EX}
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
  {__version__} 
  {__github__}                     {Fore.LIGHTCYAN_EX}Connected as {requests.get(sys_url,headers=HEADERS).json()['username']}{Ly}#{Fore.LIGHTCYAN_EX}{requests.get(sys_url,headers=HEADERS).json()['discriminator']}{Ly}
                            
  ██████╗ ███████╗██╗   ██╗                     {Fore.LIGHTCYAN_EX}1-{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Generate names and check{Fore.LIGHTBLACK_EX}]{Ly}             
  ██╔══██╗██╔════╝██║   ██║                     {Fore.LIGHTCYAN_EX}2-{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Check a specific list{Fore.LIGHTBLACK_EX}]{Ly}             
  ██║  ██║███████╗██║   ██║                     
  ██║  ██║╚════██║╚██╗ ██╔╝                     Config.ini:
  ██████╔╝███████║ ╚████╔╝                        {Fore.LIGHTCYAN_EX}Digits: {Fore.YELLOW}{sat_digits}{Ly}
  ╚═════╝ ╚══════╝  ╚═══╝                         {Fore.LIGHTCYAN_EX}String: {Fore.YELLOW}{sat_string}{Ly}
                                                  {Fore.LIGHTCYAN_EX}Punctuation: {Fore.YELLOW}{sat_punct}{Ly}
                                                  {Fore.LIGHTCYAN_EX}Delay: {Fore.YELLOW}{Delay}{Ly}
                                                  
  Discord Username's availability validator.
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
""")
    proc0()
    
def setdelay():
   global Delay
   print(f"{Lb}[!]{Ly} Default delay is: {Delay}s (config.ini){Lb}")
   d_input = input(f"{Lb}[{Ly}Edit Delay (Press Enter to skip){Lb}]:> ")
   if d_input=="" or d_input.isspace():
      return
   else:   
    try:
      int(d_input)
      Delay = int(d_input)
    except ValueError:
      print(f"{Lb}[!]{Fore.RED}Error: You must enter a valid integer. No strings.")
      setdelay()

def proc0():
    m_input = input(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTGREEN_EX}DSV{Fore.LIGHTBLACK_EX}]:> {Fore.LIGHTYELLOW_EX}").lower()
    if m_input=="exit":
        sys.exit(0)
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
def validate_names(opt,usernames):
   global available_usernames
   if opt == 2:
    for username in usernames:
       body = {
           "username": username
       }
       time.sleep(Delay)
       endpoint = requests.post(URL, headers=HEADERS, json=body)
       json_endpoint = endpoint.json()
       if endpoint.status_code == 429:
           sleep_time = endpoint.json()["retry_after"]
           print(f"{Lb}[!]{Fore.RED} Rate limit hit. Sleeping for {sleep_time}s")
           time.sleep(sleep_time)
       if json_endpoint.get("taken") is not None:
           if json_endpoint["taken"] is False:
            print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} '{username}' available.")
            save(username)
            available_usernames.append(username)
           elif json_endpoint["taken"] is True:
              print(f"{Lb}[-]{Fore.RED} '{username}' taken.")
       else:
           print(f"{Lb}[?]{Fore.RED} Error validating '{username}': {endpoint.json()['message']}")
           exit()
   elif opt == 1:
       body = {
           "username": usernames
       }
       endpoint = requests.post(URL, headers=HEADERS, json=body)
       json_endpoint = endpoint.json()
       if endpoint.status_code == 429:
           sleep_time = endpoint.json()["retry_after"]
           print(f"{Lb}[!]{Fore.RED} Rate limit hit. Sleeping for {sleep_time}s")
           time.sleep(sleep_time)
       if json_endpoint.get("taken") is not None:
           if json_endpoint["taken"] is False:
            print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} '{usernames}' available.")
            save(usernames)
            available_usernames.append(usernames)
           elif json_endpoint["taken"] is True:
              print(f"{Lb}[-]{Fore.RED} '{usernames}' taken.")
       else:
           print(f"{Lb}[?]{Fore.RED} Error validating '{usernames}': {endpoint.json()['message']}")
           exit()
def exit():
   input(f"{Fore.YELLOW}Press Enter to exit.")
   sys.exit(0)
def checkavail():
   if len(available_usernames) < 1:
      print(f"{Lb}[!]{Fore.RED}Error: No available usernames found.")
      exit()
   else:
      return
def opt2load():
    global av_list
    global dir_path
    list_path = os.path.join(dir_path, f"usernames.txt")
    print(f"{Lb}[!]{Ly}Checking 'usernames.txt' for a valid list...")
    try:
     with open(list_path) as file:
      usernames = [line.strip() for line in file]
      validate_names(2,usernames)
     checkavail()
     print(f"\n{Lb}[!]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
     exit()
    except FileNotFoundError:
       print(f"{Lb}[!]{Fore.RED}Error: Couldn't find the list (usernames.txt). Please make sure to create a valid list file in the same directory: \n({dir_path}\\)")
       exit()
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
def save(content:string):
   with open(av_list, "a") as file:
        file.write(f"\n{content}")
def opt1func(v1,v2):
   for i in range(v1):
    name = get_names(int(v2))
    validate_names(1,name)
    time.sleep(Delay)
   checkavail()
   print(f"\n{Lb}[!]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
   exit()

def get_names(length: int) ->str:
   return ''.join(random.sample(string_0 + digits_0 + punctuation_0, length))
    
if __name__ == "__main__":
    main()
