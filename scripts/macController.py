from bs4 import BeautifulSoup
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
    