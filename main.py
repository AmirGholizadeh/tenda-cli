import requests
import hashlib
import json
import argparse
import re
from bs4 import BeautifulSoup
from colorama import init, Fore, Back
from time import sleep

# from colorama to use with windows
init()

def getArguments():
    "adding arguments to get from the user"
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", "-u", dest="username", help="the username to the gateway", required=True)
    parser.add_argument("--password" "-p", dest="password", help="the password to the gateway", required=True)
    parser.add_argument("--url", dest="url", help="the url to the gateway", required=True)
    return parser.parse_args()


class MACController:
    "a class for controlling the actions on MAC addresses"
    def __init__(self, url, session):
        self.url = url
        self.session = session
    def add(self, mac):
        requestToAddMAC = self.session.get(f"{self.url}/wlmacflt.cmd?action=add&wlFltMacAddr={mac}&wlSyncNvram=1&sessionKey=1449869715")
        if requestToAddMAC.status_code == 200:
            return True
        return False
    def remove(self, mac):
        requestToRemoveMAC = self.session.get(f"{self.url}/wlmacflt.cmd?action=remove&rmLst={mac},%20&sessionKey=1449869715")
        if requestToRemoveMAC.status_code == 200:
            return True
        return False
    def list(self):
        requestToGetMACs = self.session.get(f'{self.url}/wlmacflt.cmd?action=view')
        soup = BeautifulSoup(requestToGetMACs.text, "html.parser")
        for mac in soup.find_all(attrs={"name":"rml"}):
            print(mac['value'])
    

class Framework:
    def __init__(self,username, password, url):
        self.username = username
        self.password = password
        self.url = url
    
    def _intro(self):
        censoredPassword = re.sub(".","*", self.password)
        print("*"*50)
        print(f"username: {self.username}")
        print(f"password: {censoredPassword}")
        print(f"gateway: {self.url}")
        print("*"*50)    

    def _authenticate(self):
        session = requests.session()
        
        usernameHash = hashlib.md5(self.username.encode()).hexdigest()
        passwordHash = hashlib.md5(self.password.encode()).hexdigest()
        
        data = f"username={usernameHash}&password={passwordHash}&sessionKey=0.22283898278971725"

        requestToAuthenticate = session.post(f"{self.url}/login.cgi", data=data)
        if "index.html" not in requestToAuthenticate.text:
            print('username or password is incorrect')
            exit(1)
        
        return session

    def init(self):
        session = self._authenticate()
        self._intro()
        macController = MACController(self.url, session)
        while True:
            command = input(f"{Fore.GREEN}{Back.BLACK}{self.url}>{Fore.RESET}{Back.RESET} ")
            if command.split(" ")[0] == "add":                
                macController.add(command.split(" ")[1])
                # sleep 1 seconds because the internet will get disconnected and connected again
                sleep(3)
                session = self._authenticate()
            elif command.split(" ")[0] == "remove":
                macController.remove(command.split(" ")[1])
                sleep(3)
                session = self._authenticate()
            elif command == "list":
                macController.list()
            elif command == "help":
                print("available options are:")
                print(f"\t{Back.GREEN}add <MAC>{Back.RESET}")
                print(f"\t{Back.GREEN}remove <MAC>{Back.RESET}")
                print(f"\t{Back.GREEN}list{Back.RESET}")
                print(f"\t{Back.GREEN}help{Back.RESET}")
            else:
                print("this command is not recongized")

args = getArguments()
framework = Framework(args.username,args.password, args.url)
framework.init()
