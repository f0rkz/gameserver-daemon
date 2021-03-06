import sys
import os.path

import ConfigParser
import argparse
import subprocess

# Base modules
from modules.gameserver import GameServer
from modules.srcds import SRCDS
from modules.hlds import HLDS
from modules.unreal import Unreal

# Game specific modules
from modules.ark import ARKServer
from modules.bms import BMSServer
from modules.csgo import CSGOServer
from modules.gsmod import GSModServer
from modules.hl2dm import HL2DMServer
from modules.l4d2 import L4D2Server
from modules.tf2 import TF2Server
from modules.svencoop import SvenCoopServer

# The server.conf file name.
# Change this if you want things to break.
CONFIG_FILE = "server.conf"

# Don't touch this. This is ConfigParser's shortcut.
parser = ConfigParser.RawConfigParser()

# Method to load up a configuration file
def load_configuration(config):
    parser.read(config)
    gameserver = parser._sections
    return gameserver

# Load the current configuration and a default suite of args for argparser
if os.path.isfile(CONFIG_FILE):
    gameserver = load_configuration(CONFIG_FILE)
    steam_appid = gameserver['steamcmd']['appid']
    steamcmd_path = gameserver['steamcmd']['path']
    gamedir = os.path.join(steamcmd_path, steam_appid)
    engine = gameserver['steamcmd']['engine']
else:
    gameserver = False
    steam_appid = False
    steamcmd_path = False
    engine = False

# The default argparse description
argparser = argparse.ArgumentParser(description="f0rkz gameserver daemon. Used to manage gameserver files.")
# Check if steam_appid is loaded up
if steam_appid:
    # Basic shared items
    argparser.add_argument("--configure", help="Run the configuration tool and exit.", action="store_true")
    argparser.add_argument("--installcontent", help="Install a game's content.", action="store_true")
    argparser.add_argument("-u", "--update", help="Update the gameserver files.", action="store_true")
    argparser.add_argument("--validate", help="Use the validate switch for steamcmd. This will update the game if no other options are set.", action="store_true")
    argparser.add_argument("--steamcmd", help="Install steamcmd to the configured directory.", action="store_true")

    # Begin loading each option for the configured game
    if engine == 'srcds':
        # Stuff for srcds
        argparser.add_argument("--runscript", help="Generate the runscript.txt file.", action="store_true")
        argparser.add_argument("--servercfg", help="Generate the server.cfg file", action="store_true")
        argparser.add_argument("--motd", help="Generate the motd.txt", action="store_true")
        argparser.add_argument("--start", help="Start the gameserver.", action="store_true")
        argparser.add_argument("--stop", help="Stop the gameserver.", action="store_true")
        argparser.add_argument("--restart", help="Restart the gameserver.", action="store_true")
    if engine == 'hlds':
        # Stuff for hlds
        argparser.add_argument("--runscript", help="Generate the runscript.txt file.", action="store_true")
        argparser.add_argument("--servercfg", help="Generate the server.cfg file", action="store_true")
        argparser.add_argument("--start", help="Start the gameserver.", action="store_true")
        argparser.add_argument("--stop", help="Stop the gameserver.", action="store_true")
        argparser.add_argument("--restart", help="Restart the gameserver.", action="store_true")
    if engine == 'unreal':
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

# --------------------------------------------
# Begin configuration of SRCDS and gameserver
# --------------------------------------------
try:
    if os.path.isfile(CONFIG_FILE) and args.configure:
        user_input = raw_input("server.conf already exists, overwrite? [Y/n]: ")
        if str.lower(user_input) == "y":
            subprocess.call("rm {}".format(CONFIG_FILE), shell=True)
        else:
            sys.exit("Configuration will not be removed. Exiting.")
except AttributeError:
    pass

try:
    if not os.path.isfile(CONFIG_FILE) and args.configure:
        base_config = GameServer(gsconfig = gameserver)
        base_config.configure()

        # Load up the configuration after the base is installed
        gameserver = load_configuration(CONFIG_FILE)
        steam_appid = gameserver['steamcmd']['appid']
        steamcmd_path = gameserver['steamcmd']['path']
        engine = gameserver['steamcmd']['engine']

        # Begin the game engine shared configuration
        # SRCDS configuration
        if engine == 'srcds':
            engine_config = SRCDS(gsconfig = gameserver)
            engine_config.configure()

        elif engine == 'hlds':
            engine_config = HLDS(gsconfig = gameserver)
            engine_config.configure()

        # Unreal configuration
        elif engine == 'unreal':
            engine_config = Unreal(gsconfig = gameserver)
            engine_config.configure()

        # Begin the gameserver's configuration modules
        # CSGO
        if steam_appid == '740':
            game_config = CSGOServer(gsconfig = gameserver)
            game_config.configure()
        # TF2
        elif steam_appid == '232250':
            game_config = TF2Server(gsconfig = gameserver)
            game_config.configure()
        # HL2DM
        elif steam_appid == '232370':
            game_config = HL2DMServer(gsconfig = gameserver)
            game_config.configure()
        # BMS
        elif steam_appid == '346680':
            game_config = BMSServer(gsconfig = gameserver)
            game_config.configure()
        # left4dead2
        elif steam_appid == '222860':
            game_config = L4D2Server(gsconfig = gameserver)
            game_config.configure()
        # ARK
        elif steam_appid == '376030':
            game_config = ARKServer(gsconfig = gameserver)
            game_config.configure()
        # GSMOD
        elif steam_appid == '4020':
            game_config = GSModServer(gsconfig = gameserver)
            game_config.configure()

        # SvenCoopServer
        elif steam_appid == '276060':
            game_config = SvenCoopServer(gsconfig = gameserver)
            game_config.configure()
except AttributeError:
    pass


# --------------------------------------------
# Steamcmd operations
# --------------------------------------------
# Steam cmd install
try:
    if os.path.isfile(CONFIG_FILE) and args.steamcmd:
        gameserver = load_configuration(CONFIG_FILE)
        steamcmd = GameServer(gsconfig = gameserver)
        steamcmd.install_steamcmd()
except AttributeError:
    pass

# Installs a game's content for garry's mod
try:
    if os.path.isfile(CONFIG_FILE) and args.installcontent:
        install_files = GameServer(gsconfig = gameserver)
        install_files.install_content()
except AttributeError:
    pass

# Update gamefiles
try:
    if os.path.isfile(CONFIG_FILE) and args.update:
        gameserver = load_configuration(CONFIG_FILE)
        update = GameServer(gsconfig = gameserver)
        install_dir = os.path.join(gameserver['steamcmd']['path'], '')
        if not os.path.isfile(os.path.join(install_dir, 'steamcmd.sh')):
            print "Steamcmd was not found. Installing steamcmd."
            update.install_steamcmd()
        if args.validate:
            update.update_game_validate()
        else:
            update.update_game_novalidate()
except AttributeError:
    pass


# --------------------------------------------
# Game specific operations
# server.cfg, motd, runscript, etc...
# --------------------------------------------
try:
    if engine == 'srcds' or engine == 'hlds' and os.path.isdir(steamcmd_path):
        # Check if the game is installed before running these.
        if os.path.isdir(gamedir):
            # MOTD
            if os.path.isfile(CONFIG_FILE) and engine == 'srcds' and args.motd:
                gameserver = load_configuration(CONFIG_FILE)
                motd = SRCDS(gsconfig = gameserver)
                motd.create_motd()

            # Runscript creation
            if os.path.isfile(CONFIG_FILE) and engine == 'srcds' and args.runscript:
                gameserver = load_configuration(CONFIG_FILE)
                runscript = SRCDS(gsconfig = gameserver)
                runscript.create_runscript()
            elif os.path.isfile(CONFIG_FILE) and engine == 'hlds' and args.runscript:
                gameserver = load_configuration(CONFIG_FILE)
                runscript = HLDS(gsconfig = gameserver)
                runscript.create_runscript()

            # Server.cfg creation
            if os.path.isfile(CONFIG_FILE) and engine == 'srcds' and args.servercfg:
                gameserver = load_configuration(CONFIG_FILE)
                servercfg = SRCDS(gsconfig = gameserver)
                servercfg.create_servercfg()
            elif os.path.isfile(CONFIG_FILE) and engine == 'hlds' and args.servercfg:
                gameserver = load_configuration(CONFIG_FILE)
                servercfg = HLDS(gsconfig = gameserver)
                servercfg.create_servercfg()
        else:
            sys.exit("Game is not installed. Use the --update command to install the game files.")
except AttributeError:
    pass

# --------------------------------------------
# Server related operations
# Start, stop, restart, etc.
# --------------------------------------------
# Start operations
try:
    if engine == 'srcds' or engine == 'hlds' or engine == 'unreal' and os.path.isdir(steamcmd_path):
        # Check if the game is installed
        if os.path.isdir(gamedir):
            # CSGO
            if steam_appid == '740' and args.start:
                gameserver = load_configuration(CONFIG_FILE)
                csgo = CSGOServer(gsconfig = gameserver)
                csgo.start()
            # TF2
            elif steam_appid == '232250' and args.start:
                gameserver = load_configuration(CONFIG_FILE)
                tf2 = TF2Server(gsconfig = gameserver)
                tf2.start()
            # HL2DM
            elif steam_appid == '232370' and args.start:
                gameserver = load_configuration(CONFIG_FILE)
                hl2dm = HL2DMServer(gsconfig = gameserver)
                hl2dm.start()
            # BMS
            elif steam_appid == '346680' and args.start:
                gameserver = load_configuration(CONFIG_FILE)
                bms = BMSServer(gsconfig = gameserver)
                bms.start()
            # left4dead2
            elif steam_appid == '222860' and args.start:
                gameserver = load_configuration(CONFIG_FILE)
                l4d2 = L4D2Server(gsconfig = gameserver)
                l4d2.start()
            # ARK
            elif steam_appid == '376030' and args.start:
                gameserver = load_configuration(CONFIG_FILE)
                ark = ARKServer(gsconfig = gameserver)
                ark.start()
            # GSMOD
            elif steam_appid == '4020' and args.start:
                gameserver = load_configuration(CONFIG_FILE)
                gsmod = GSModServer(gsconfig = gameserver)
                gsmod.start()

            # Sven coop
            elif steam_appid == '276060' and args.start:
                gameserver = load_configuration(CONFIG_FILE)
                svencoop = SvenCoopServer(gsconfig = gameserver)
                svencoop.start()

            # Stop operations
            # CSGO
            if steam_appid == '740' and args.stop:
                gameserver = load_configuration(CONFIG_FILE)
                csgo = CSGOServer(gsconfig = gameserver)
                csgo.stop()
            # TF2
            elif steam_appid == '232250' and args.stop:
                gameserver = load_configuration(CONFIG_FILE)
                tf2 = TF2Server(gsconfig = gameserver)
                tf2.stop()
            # HL2DM
            elif steam_appid == '232370' and args.stop:
                gameserver = load_configuration(CONFIG_FILE)
                hl2dm = HL2DMServer(gsconfig = gameserver)
                hl2dm.stop()
            # BMS
            elif steam_appid == '346680' and args.stop:
                gameserver = load_configuration(CONFIG_FILE)
                bms = BMSServer(gsconfig = gameserver)
                bms.stop()
            # left4dead2
            elif steam_appid == '222860' and args.stop:
                gameserver = load_configuration(CONFIG_FILE)
                l4d2 = L4D2Server(gsconfig = gameserver)
                l4d2.stop()
            # ARK
            elif steam_appid == '376030' and args.stop:
                gameserver = load_configuration(CONFIG_FILE)
                ark = ARKServer(gsconfig = gameserver)
                ark.stop()
            # GSMOD
            elif steam_appid == '4020' and args.stop:
                gameserver = load_configuration(CONFIG_FILE)
                gsmod = GSModServer(gsconfig = gameserver)
                gsmod.stop()

            # SvenCoop
            elif steam_appid == '276060' and args.stop:
                gameserver = load_configuration(CONFIG_FILE)
                svencoop = SvenCoopServer(gsconfig = gameserver)
                svencoop.stop()

            # Restart operations
            # CSGO
            if steam_appid == '740' and args.restart:
                gameserver = load_configuration(CONFIG_FILE)
                csgo = CSGOServer(gsconfig = gameserver)
                csgo.stop()
                csgo.start()
            # TF2
            elif steam_appid == '232250' and args.restart:
                gameserver = load_configuration(CONFIG_FILE)
                tf2 = TF2Server(gsconfig = gameserver)
                tf2.stop()
                tf2.start()
            # HL2DM
            elif steam_appid == '232370' and args.restart:
                gameserver = load_configuration(CONFIG_FILE)
                hl2dm = HL2DMServer(gsconfig = gameserver)
                hl2dm.stop()
                hl2dm.start()
            # BMS
            elif steam_appid == '346680' and args.restart:
                gameserver = load_configuration(CONFIG_FILE)
                bms = BMSServer(gsconfig = gameserver)
                bms.stop()
                bms.start()
            # left4dead2
            elif steam_appid == '222860' and args.restart:
                gameserver = load_configuration(CONFIG_FILE)
                l4d2 = L4D2Server(gsconfig = gameserver)
                l4d2.stop()
                l4d2.start()
            # ARK
            elif steam_appid == '376030' and args.restart:
                gameserver = load_configuration(CONFIG_FILE)
                ark = ARKServer(gsconfig = gameserver)
                ark.stop()
                ark.start()
            # GSMOD
            elif steam_appid == '4020' and args.restart:
                gameserver = load_configuration(CONFIG_FILE)
                gsmod = GSModServer(gsconfig = gameserver)
                gsmod.stop()
                gsmod.start()
            # SvenCoop
            elif steam_appid == '4020' and args.restart:
                gameserver = load_configuration(CONFIG_FILE)
                svencoop = SvenCoopServer(gsconfig = gameserver)
                svencoop.stop()
                svencoop.start()
        else:
            sys.exit("Game is not installed. Use the --update command to install the game files.")
except (AttributeError, NameError):
    pass
