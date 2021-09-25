from bs4 import BeautifulSoup
import re
class Security:
    def __init__(self, url):
        self.url = url
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