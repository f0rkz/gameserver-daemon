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

# Argparser's arguments!
argparser = argparse.ArgumentParser(description="f0rkz gameserver daemon. Used to manage gameserver files.")
argparser.add_argument("--configure", help="Run the configuration tool and exit.", action="store_true")
argparser.add_argument("-u", "--update", help="Update the gameserver files.", action="store_true")
argparser.add_argument("--validate", help="Use the validate switch for steamcmd. This will update the game if no other options are set.", action="store_true")
argparser.add_argument("--runscript", help="Generate the runscript.txt file.", action="store_true")
argparser.add_argument("--steamcmd", help="Install steamcmd to the configured directory.", action="store_true")
argparser.add_argument("--start", help="Start the gameserver.", action="store_true")
argparser.add_argument("--stop", help="Stop the gameserver.", action="store_true")
argparser.add_argument("--restart", help="Restart the gameserver.", action="store_true")
argparser.add_argument("--servercfg", help="Generate the server.cfg file", action="store_true")
argparser.add_argument("--motd", help="Generate the motd.txt", action="store_true")
args = argparser.parse_args()

# Catch if the user is running the tool without a config.
if not os.path.isfile(CONFIG_FILE) and not args.configure:
    sys.exit("No configuration file found. Run: python gameserver-daemon.py --configure")

# Configure the gameserver. This is apart of the GameServer class.
if args.configure:
    if os.path.isfile(CONFIG_FILE):
        user_input = raw_input("server.conf already exists, overwrite? [Y/n]: ")
        if str.lower(user_input) == "y":
            subprocess.call("rm {}".format(CONFIG_FILE), shell=True)
            # Need to pass a blank configuration to the class.
            gameserver = False
            myserver = GameServer(gsconfig=gameserver)
            myserver.configure()
        else:
            sys.exit("Configuration will not be removed. Exiting.")
    else:
        gameserver = False
        myserver = GameServer(gsconfig=gameserver)
        myserver.configure()

# Update the gameserver. This is apart of the GameServer class.
if args.update:
    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    myserver = GameServer(gsconfig=gameserver)

    install_dir = os.path.join(gameserver['steamcmd']['path'], '')

    if not os.path.isfile(os.path.join(install_dir, 'steamcmd.sh')):
        print "Steamcmd was not found. Installing steamcmd."
        myserver.install_steamcmd()

    if args.validate:
        myserver.update_game_validate()

    else:
        myserver.update_game_novalidate()

# Install steacmd. This is apart of the GameServer class.
if args.steamcmd:
    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    myserver = GameServer(gsconfig=gameserver)
    myserver.install_steamcmd()

# Update with validate. This is apart of the GameServer class.
if args.validate:
    if args.update is False:
        print "Use the --update argument with --validate to use this option properly."
        print "Example: python gameserver-daemon.py --update --validate"
        exit()

# -------------------------
# Game specific operations!
# -------------------------
if os.path.isfile(CONFIG_FILE):
    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    engine = gameserver['steamcmd']['engine']

    # SRCDS specific operations
    if engine == "srcds":
        myserver = SRCDSGameServer(gsconfig=gameserver)
        if args.servercfg:
            myserver.create_servercfg()

        if args.motd:
            myserver.create_motd()

        if args.runscript:
            myserver.create_runscript()

        if args.start:
            if myserver.status():
                sys.exit("Server is running. Please stop or restart your server.")
            else:
                myserver.start()

        if args.stop:
            myserver.stop()

        if args.restart:
            myserver.stop()
            myserver.start()

    # Unreal specific operations
    if engine == "unreal":
        myserver = UnrealGameServer(gsconfig=gameserver)
        if args.start:
            if myserver.status():
                sys.exit("Server is running. Please stop or restart your server.")
            else:
                myserver.start()

        if args.stop:
            myserver.stop()

        if args.restart:
            myserver.stop()
            myserver.start()
