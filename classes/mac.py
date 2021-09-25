from bs4 import BeautifulSoup
import requests
import json
class Mac:
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
        macElements = soup.find_all(attrs={"name":"rml"})
        macValues = []
        for macElement in macElements:
            vendor = self._vendor(macElement['value'])
            macValues.append(f"{vendor} {macElement['value']}")
        return macValues
    def clear(self):
        clients = self.list()
        for client in clients:
            self.remove(client)
    def _vendor(self, mac):
        OUI = mac.split(':')[:3]
        OUI = ':'.join(OUI)
        requestToGetVendorName = requests.get(f'http://www.macvendorlookup.com/api/v2/{OUI}')
        if(requestToGetVendorName.status_code == 200):
            vendorName = json.loads(requestToGetVendorName.text)[0]['company']
            return vendorName
        return "unknown"    
