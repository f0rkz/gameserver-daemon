import sys
import os.path

import ConfigParser
import argparse
import subprocess

from GameServer import GameServer
from gameserver/SRCDS import SRCDS
from gameserver/Unreal import Unreal
#from GameServer import SRCDSGameServer
#from GameServer import UnrealGameServer

# The server.conf fille name.
# Change this if you want things to break.
CONFIG_FILE = "server.conf"

# Don't touch this. This is ConfigParser's shortcut.
parser = ConfigParser.RawConfigParser()

# Method to load up a configuration file
def load_configuration(config):
    parser.read(config)
    gameserver = parser._sections
    steam_appid = gameserver['steamcmd']['appid']
    engine = gameserver['steamcmd']['engine']

# Load the current configuration and a default suite of args for argparser
if os.path.isfile(CONFIG_FILE):
    load_configuration(CONFIG_FILE)
else:
    gameserver = False
    steam_appid = False
    engine = False

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
    if engine == 'srcds' and os.path.isdir(gameserver['steamcmd']['path']):
        # Stuff for srcds
        argparser.add_argument("--runscript", help="Generate the runscript.txt file.", action="store_true")
        argparser.add_argument("--servercfg", help="Generate the server.cfg file", action="store_true")
        argparser.add_argument("--motd", help="Generate the motd.txt", action="store_true")
        argparser.add_argument("--start", help="Start the gameserver.", action="store_true")
        argparser.add_argument("--stop", help="Stop the gameserver.", action="store_true")
        argparser.add_argument("--restart", help="Restart the gameserver.", action="store_true")
    if engine == 'unreal' and os.path.isdir(gameserver['steamcmd']['path']):
        # Stuff for unreal
        argparser.add_argument("--start", help="Start the gameserver.", action="store_true")
        argparser.add_argument("--stop", help="Stop the gameserver.", action="store_true")
        argparser.add_argument("--restart", help="Restart the gameserver.", action="store_true")
else:
    argparser.add_argument("--configure", help="Run the configuration tool.", action="store_true")

# Load up the arguments processed above
args = argparser.parse_args()

# Give the user a message if no config file is found.
if not os.path.isfile(CONFIG_FILE) and not args.configure:
    sys.exit("No configuration file found. Run: python gameserver-daemon.py --configure")

# Begin configuration of SRCDS and gameserver
if os.path.isfile(CONFIG_FILE) and args.configure:
    user_input = raw_input("server.conf already exists, overwrite? [Y/n]: ")
    if str.lower(user_input) == "y":
        subprocess.call("rm {}".format(CONFIG_FILE), shell=True)
    else:
        sys.exit("Configuration will not be removed. Exiting.")

if not os.path.isfile(CONFIG_FILE) and args.configure:
    base_config = GameServer(gsconfig=gameserver)
    base_config.configure()
    # Load up the configuration after the base is installed
    load_configuration(CONFIG_FILE)
    # SRCDS configuration
    if engine == 'srcds':
        engine_config = SRCDS(gsconfig=gameserver)
        engine_config.configure()
    # Unreal configuration
    elif engine == 'unreal':
        engine_config = Unreal(gsconfig=gameserver)
        engine_config.configure()
