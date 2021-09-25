import argparse
from colorama import init as coloramaInit
from classes.framework import Framework
# for windows
coloramaInit()
def getArguments():
    "adding arguments to get from the user"
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", "-u", dest="username", help="the username to the gateway", required=True)
    parser.add_argument("--password", "-p", dest="password", help="the password to the gateway", required=True)
    parser.add_argument("--url", dest="url", help="the url to the gateway", required=True)
    return parser.parse_args()
args = getArguments()
framework = Framework(args.username,args.password, args.url)
framework.init()
