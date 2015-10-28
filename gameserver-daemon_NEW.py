import sys
import os.path

import ConfigParser
import argparse
import subprocess

from GameServer import GameServer
from GameServer import SRCDSGameServer
from GameServer import UnrealGameServer

# The server.conf fille name.
# Change this if you want things to break.
CONFIG_FILE = "server.conf"

# Don't touch this. This is ConfigParser's shortcut.
parser = ConfigParser.RawConfigParser()

# Load the current configuration and a default suite of args for argparser
if os.path.isfile(CONFIG_FILE):
    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    steam_appid = gameserver['steamcmd']['appid']
    engine = gameserver['steamcmd']['engine']
else:
    gameserver = False

# The default argparse description
argparser = argparse.ArgumentParser(description="f0rkz gameserver daemon. Used to manage gameserver files.")
# Check if steam_appid is loaded up
if steam_appid and gameserver:
    # Basic shared items
    argparser.add_argument("--configure", help="Run the configuration tool and exit.", action="store_true")
    argparser.add_argument("-u", "--update", help="Update the gameserver files.", action="store_true")
    argparser.add_argument("--validate", help="Use the validate switch for steamcmd. This will update the game if no other options are set.", action="store_true")
    argparser.add_argument("--steamcmd", help="Install steamcmd to the configured directory.", action="store_true")

    # Begin loading each option for the configured game
    if engine == 'srcds':
        # Stuff for srcds
        argparser.add_argument("--runscript", help="Generate the runscript.txt file.", action="store_true")
        argparser.add_argument("--servercfg", help="Generate the server.cfg file", action="store_true")
        argparser.add_argument("--motd", help="Generate the motd.txt", action="store_true")
    if engine == 'unreal':
        # Stuff for unreal
        pass
else:
    argparser.add_argument("--configure", help="Run the configuration tool.", action="store_true")

# Load up the arguments processed above
args = argparser.parse_args()
