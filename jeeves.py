from __future__ import print_function
from segregator.segregator import Segregator
from utils.say import say
from utils.user_input import user_input
# from julius_connector.julius_connector import connect_to_julius

import argparse
import subprocess
import signal
import sys
import os


def signal_handler(signal, frame):
    with open(".CHAT_SERVER_PID") as pid:
        subprocess.call(['kill', pid.readlines()[0].strip()])

    os.remove(".CHAT_SERVER_PID")
    exit(0)


signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(description="P.G. Wodehouse couldn't have imagined me better.")
parser.add_argument("--input", help="specify the input source mic/stdin, default is stdin")
parser.add_argument("--host", help="specify julius' host, default is localhost")
parser.add_argument("--port", help="specify julius' port, default is 10500", type=int)
args = parser.parse_args()

if not os.path.exists(".CHAT_SERVER_PID"):
    process = subprocess.Popen([sys.executable, "chat_ui/chat_ui_server.py"])

    with open(".CHAT_SERVER_PID", "w") as pid:
        pid.write(str(process.pid))
else:
    with open(".CHAT_SERVER_PID") as pid:
        subprocess.call(['kill', pid.readlines()[0].strip()])

    os.remove(".CHAT_SERVER_PID")

src = "mic" if (args.input and args.input == "mic") else "stdin"

say("Hello. I'm at your service.")
while True:
    if src == "stdin":
        sentence = raw_input("Type something: ")
    else:
        sentence = user_input("Say something: ")

    segregator = Segregator(sentence)
    segregator.segregate_and_react()
