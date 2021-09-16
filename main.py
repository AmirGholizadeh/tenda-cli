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


class Wireless:
    def __init__(self, username, password, url):
        self.url = url
        self.username = username
        self.password = password

    def authenticate(self):
        session = requests.session()
        
        usernameHash = hashlib.md5(self.username.encode()).hexdigest()
        passwordHash = hashlib.md5(self.password.encode()).hexdigest()
        
        data = f"username={usernameHash}&password={passwordHash}&sessionKey=0.22283898278971725"

        requestToAuthenticate = session.post(f"{self.url}/login.cgi", data=data)
        if "index.html" not in requestToAuthenticate.text:
            print('username or password is incorrect')
            exit(1)
        return session

    def getSSID(self,session):
        requestToGetConfiguration = session.get(f'{self.url}/wlcfg.html')
        soup = BeautifulSoup(requestToGetConfiguration.text, 'html.parser');
        scriptTagContent = soup.find_all('script')[2].contents[0]
        ssidVariable = re.search("var ssid = '\w+'", scriptTagContent)[0]
        ssidValue = re.search("'\w+'",ssidVariable)[0] 
        ssidWithoutQoutes = ssidValue.split("'")[1]
        return ssidWithoutQoutes

    def setSSID(self, session, ssid):
        if requestToSetSSID.status_code == 200:
            return True
        return False

    def getStationList(self, session):
        requestToGetStationList = session.get(f"{self.url}/wlstationlist.cmd")
        soup = BeautifulSoup(requestToGetStationList.text, 'html.parser')
        macAddresses = re.findall("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", f"{soup.contents[0]}")
        stations = []
        for station in macAddresses:
            stations.append(station)
        return stations

    def hide(self, session):


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
    
    def _intro(self, ssid):
        censoredPassword = re.sub(".","*", self.password)
        print("*"*50)
        print(f"username: {self.username}")
        print(f"password: {censoredPassword}")
        print(f"gateway: {self.url}")
        print(f"SSID: {ssid}")
        print("*"*50)    

    def init(self):
        wireless = Wireless(self.username, self.password, self.url)
        session = wireless.authenticate()
        ssid = wireless.getSSID(session)
        self._intro(ssid)
        macController = MACController(self.url, session)
        while True:
            command = input(f"{Fore.GREEN}{Back.BLACK}{ssid}>{Fore.RESET}{Back.RESET} ")
            command = command.strip()
            if command.split(" ")[0] == "add":                
                macController.add(command.split(" ")[1])
                # sleep 1 seconds because the internet will get disconnected and connected again
                sleep(3)
                session = wireless.authenticate()
            elif command.split(" ")[0] == "remove":
                macController.remove(command.split(" ")[1])
                sleep(3)
                session = wireless.authenticate()
            elif command.split(" ")[0] == "set":
                if command.split(" ")[1] == "ssid":
                    if wireless.setSSID(session, command.split(" ")[2]):
                        ssid = command.split(" ")[2]
            elif command == "list":
                macController.list()
            elif command == "stations":
                stations = wireless.getStationList(session)
                for station in stations:
                    print(station)
            elif command == "help":
                print("available options are:")
                print(f"\t{Back.GREEN}add <MAC>{Back.RESET}")
                print(f"\t{Back.GREEN}remove <MAC>{Back.RESET}")
                print(f"\t{Back.GREEN}set ssid <SSID>{Back.RESET}")
                print(f"\t{Back.GREEN}list{Back.RESET}")
                print(f"\t{Back.GREEN}stations{Back.RESET}")
                print(f"\t{Back.GREEN}help{Back.RESET}")
                print(f"\t{Back.GREEN}exit{Back.RESET}")
            elif command == "exit":
                exit(0)
            else:
                print("this command is not recongized")

args = getArguments()
framework = Framework(args.username,args.password, args.url)
framework.init()
