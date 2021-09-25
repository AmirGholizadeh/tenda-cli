from colorama import Fore, Back
import re
from classes.basic import Basic
from classes.mac import Mac
from classes.security import Security

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
        basic = Basic(self.username, self.password, self.url)
        session = basic.authenticate()
        ssid = basic.getSSID(session)
        self._intro(ssid)
        mac = Mac(self.url, session)
        security = Security(self.url)
        while True:
            command = input(f"{Fore.WHITE}{Back.CYAN}{ssid}>{Fore.RESET}{Back.RESET} ")
            command = command.strip()
            if command.split(" ")[0] == "add":                
                mac.add(command.split(" ")[1])
                #session = basic.authenticate() TODO wireless 
            elif command.split(" ")[0] == "remove":
                mac.remove(command.split(" ")[1])
                #session = basic.authenticate() TODO wireless
            elif command.split(" ")[0] == "set":
                splittedCommand = command.split(" ")
                if splittedCommand[1] == "ssid":
                    if basic.setSSID(session, splittedCommand[2]):
                        ssid = splittedCommand[2]
                if splittedCommand[1] == "password":
                    security.setPassword(session, splittedCommand[2], splittedCommand[3])
                if  splittedCommand[1] == "filter":
                    security.filter(splittedCommand[2])
            elif command == "list":
                clients = mac.list()
                for client in clients:
                    print(client)
            elif command == "clear":
                mac.clear()
            elif command == "stations":
                stations = basic.getStationList(session)
                for station in stations:
                    print(station)
            elif command == "hide":
                security.hide(session)
            elif command == "unhide":
                security.unhide(session)
            elif command == "visibility":
                visibility = security.visibility(session)
                print(visibility)
            elif command == "help":
                print("\n")
                # BASIC
                print(f"{Fore.CYAN}Basic{Back.RESET}{Fore.RESET}")
                print(f"\t{Back.CYAN}set ssid <SSID>{Back.RESET}")
                print(f"\t{Back.CYAN}stations{Back.RESET}")
                print("\n")
                # MAC
                print(f"{Fore.CYAN}MAC{Back.RESET}{Fore.RESET}")
                print(f"\t{Back.CYAN}add <MAC>{Back.RESET}")
                print(f"\t{Back.CYAN}remove <MAC>{Back.RESET}")
                print(f"\t{Back.CYAN}clear{Back.RESET}")
                print(f"\t{Back.CYAN}list{Back.RESET}")
                print("\n")
                # SECURITY
                print(f"{Fore.CYAN}Security{Back.RESET}{Fore.RESET}")
                print(f"\t{Back.CYAN}set password <CURRENT_PASSWORD> <NEW_PASSWORD>{Back.RESET}")
                print(f"\t{Back.CYAN}set filter <OPTION>{Back.RESET}")
                print(f"\t{Back.CYAN}hide{Back.RESET}")
                print(f"\t{Back.CYAN}unhide{Back.RESET}")
                print(f"\t{Back.CYAN}visibility{Back.RESET}")
                print("\n")
                print(f"\thelp")
                print(f"\t{Fore.RED}exit{Fore.RESET}")
                print("\n")
            elif command == "exit":
                exit(0)
            else:
                print("this command is not recongized")