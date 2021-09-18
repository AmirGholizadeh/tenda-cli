import requests
import hashlib
from bs4 import BeautifulSoup
import re

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
        requestToSetSSID = session.get(f'{self.url}/wlcfg.wl?wlSsid={ssid}&sessionKey=361939628')
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
        requestToHideAP = session.get(f'{self.url}/wlcfg.wl?wlHide=1&sessionKey=361939628')
        if requestToHideAP.status_code == 200:
            return True
        return False
    def unhide(self, session):
        requestToUnhideAP = session.get(f'{self.url}/wlcfg.wl?wlHide=0&sessionKey=361939628')
        if requestToUnhideAP.status_code == 200:
            return True
        return False
    def visibility(self, session):
        requestToGetVisibility = session.get(f'{self.url}/wlcfg.html')
        soup = BeautifulSoup(requestToGetVisibility.text, "html.parser")
        findValue = re.search("var hide = '[01]'", f"{soup}")
        valueItself = findValue[0].split("'")[1]
        if valueItself == "0":
            return "visible"
        else:
            return "hidden"
    def setPassword(self, session, currentPassword, newPassword):
        requestToGetCurrentPassword = session.get(f'{self.url}/wlsecurity.html')
        soup = BeautifulSoup(requestToGetCurrentPassword.text, "html.parser")
        findPassword = re.search("var wpaPskKey = '\w+'", f"{soup}")
        passwordItself = findPassword[0].split("'")[1]
        if currentPassword != passwordItself:
            print("the password you have entered is incorrect, please try again.")
            return False
        if len(newPassword) < 8:
            print('the length of the password must be greater than 8.')
            return False
        requestToSetPassword = session.get(f'{self.url}/wlsecurity.wl?wlWpaPsk={newPassword}&sessionKey=102574560')
        return True
