from colorama import Fore, Back
import re
import re
from time import sleep
from scripts.wireless import Wireless
from scripts.macController import MACController

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
                sleep(1)
                session = wireless.authenticate()
            elif command.split(" ")[0] == "remove":
                macController.remove(command.split(" ")[1])
                sleep(1)
                session = wireless.authenticate()
            elif command.split(" ")[0] == "set":
                splittedCommand = command.split(" ")
                if splittedCommand[1] == "ssid":
                    if wireless.setSSID(session, splittedCommand[2]):
                        ssid = splittedCommand[2]
                if splittedCommand[1] == "password":
                    wireless.setPassword(session, splittedCommand[2], splittedCommand[3])
            elif command == "list":
                macController.list()
            elif command == "stations":
                stations = wireless.getStationList(session)
                for station in stations:
                    print(station)
            elif command == "hide":
                wireless.hide(session)
            elif command == "unhide":
                wireless.unhide(session)
            elif command == "visibility":
                visibility = wireless.visibility(session)
                print(visibility)
            elif command == "help":
                print("available options are:")
                print(f"\t{Back.GREEN}add <MAC>{Back.RESET}")
                print(f"\t{Back.GREEN}remove <MAC>{Back.RESET}")
                print(f"\t{Back.GREEN}set ssid <SSID>{Back.RESET}")
                print(f"\t{Back.GREEN}set password <CURRENT_PASSWORD> <NEW_PASSWORD>{Back.RESET}")
                print(f"\t{Back.GREEN}list{Back.RESET}")
                print(f"\t{Back.GREEN}stations{Back.RESET}")
                print(f"\t{Back.GREEN}hide{Back.RESET}")
                print(f"\t{Back.GREEN}unhide{Back.RESET}")
                print(f"\t{Back.GREEN}visibility{Back.RESET}")
                print(f"\t{Back.GREEN}help{Back.RESET}")
                print(f"\t{Back.GREEN}exit{Back.RESET}")
            elif command == "exit":
                exit(0)
            else:
                print("this command is not recongized")