from bs4 import BeautifulSoup
import requests
import json
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
        macElements = soup.find_all(attrs={"name":"rml"})
        macValues = []
        for macElement in macElements:
            vendor = self._vendor(macElement['value'])
            macValues.append(f"{vendor} {macElement['value']}")
        return macValues
    def clear(self):
        macs = self.list()
        for mac in macs:
            self.remove(mac)
    def _vendor(self, mac):
        OUI = mac.split(':')[:3]
        OUI = ':'.join(OUI)
        requestToGetVendorName = requests.get(f'http://www.macvendorlookup.com/api/v2/{OUI}')
        if(requestToGetVendorName.status_code == 200):
            vendorName = json.loads(requestToGetVendorName.text)[0]['company']
            return vendorName
        return "unknown"    
    def filter(self,kind):
        if(kind == "whitelist"):
            requestToFilterByWhitelist = self.session.get(f'{self.url}/wlmacflt.cmd?action=save&wlFltMacMode=allow&sessionKey=1656871422')
        elif(kind == "blacklist"):
            requestToFilterByBlacklist = self.session.get(f'{self.url}/wlmacflt.cmd?action=save&wlFltMacMode=deny&sessionKey=1656871422')
        elif(kind == "disable"):
            requestToDisableFiltering = self.session.get(f'{self.url}/wlmacflt.cmd?action=save&wlFltMacMode=disabled&sessionKey=1656871422')
        else:
            print("available lists are:")
            print("\twhitelist")    
            print("\tblacklist")
            print("\tdisable")
            return False
        return True