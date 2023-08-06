#!/usr/bin/python3

from termcolor import colored
from argparse import ArgumentParser

from lib.Engine import XSST
from lib.Globals import Color
from lib.Functions import starter, exit_handler

parser = ArgumentParser(description=colored("XSS Terminal", color='yellow'), epilog=colored('<script>window.location="https://bit.ly/3n60FQ4";</script>', color='yellow'))
string_group = parser.add_mutually_exclusive_group()
parser.add_argument('-u', '--base-url', type=str, help="Base URL")
parser.add_argument('-p', '--payload', type=str, help="Starting payload")
string_group.add_argument('-e', '--error-string', type=str, help="Error string")
string_group.add_argument('-s', '--match-string', type=str, help="Match string")
#string_group.add_argument('-b', '--blind-string', type=str, help="Blind error string")
parser.add_argument('-m', '--method', type=str, choices=['GET','POST'], help="HTTP Method")
parser.add_argument('-o', '--output', type=str, help="Output file name")
parser.add_argument('-r', '--resume', type=str, help="Filename to resume XSST session")
parser.add_argument('--banner', action="store_true", help="Print banner and exit")
argv = parser.parse_args()

xss_base, xss_payload = starter(argv)
terminal = XSST(xss_base, xss_payload)

def main():
    while True:
        try:
            terminal.make_xss(argv)
        except KeyboardInterrupt:
            exit_handler(terminal.base_url, terminal.xss_payload, filename=argv.output)
            exit()
        except Exception as E:
            print(f"{Color.bad} Unfortunately {E},{E.__class__} occured")
            exit()
