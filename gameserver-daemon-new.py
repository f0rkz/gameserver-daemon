import sys
import os.path
import ConfigParser
import argparse
import subprocess
from GameServer import GameServer


CONFIG_FILE = "server.conf"

parser = ConfigParser.RawConfigParser()

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
#argparser.add_argument("--express", help="Express settings.", action="store_true")
args = argparser.parse_args()

# Catch if the user is running the tool without a config.
if not os.path.isfile(CONFIG_FILE) and not args.configure:
    sys.exit("No configuration file found. Run: python gameserver-daemon.py --configure")

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

if args.update:
    if not os.path.isfile(CONFIG_FILE):
        sys.exit("No configuration found. Run the script with the --configure option")

    else:
        parser.read(CONFIG_FILE)
        gameserver = parser._sections
        myserver = GameServer(gsconfig=gameserver)

        install_dir = os.path.dirname(gameserver['gameserver']['path'])

        if not os.path.isfile(os.path.join(install_dir, 'steamcmd.sh')):
            print "Steamcmd was not found. Installing steamcmd."
            myserver.install_steamcmd()

        if args.validate:
            myserver.update_game_validate()

        else:
            myserver.update_game_novalidate()

if args.steamcmd:
    if not os.path.isfile(CONFIG_FILE):
        sys.exit("No configuration found. Run the script with the --configure option")

    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    myserver = GameServer(gsconfig=gameserver)
    myserver.install_steamcmd()

if args.validate:
    if not os.path.isfile(CONFIG_FILE):
        sys.exit("No configuration found. Run the script with the --configure option")
    if args.update is False:
        print "Use the --update argument with --validate to use this option properly."
        print "Example: python gameserver-daemon.py --update --validate"
        exit()

if args.servercfg:
    if not os.path.isfile(CONFIG_FILE):
        sys.exit("No configuration found. Run the script with the --configure option")
    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    myserver = GameServer(gsconfig=gameserver)
    myserver.create_servercfg()

if args.motd:
    if not os.path.isfile(CONFIG_FILE):
        sys.exit("No configuration found. Run the script with the --configure option")
    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    myserver = GameServer(gsconfig=gameserver)
    myserver.create_motd()

if args.runscript:
    if not os.path.isfile(CONFIG_FILE):
        sys.exit("No configuration found. Run the script with the --configure option")
    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    myserver = GameServer(gsconfig=gameserver)
    myserver.create_runscript()


if args.start:
    if not os.path.isfile(CONFIG_FILE):
        sys.exit("No configuration found. Run the script with the --configure option")
    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    myserver = GameServer(gsconfig=gameserver)
    myserver.start()

if args.stop:
    if not os.path.isfile(CONFIG_FILE):
        sys.exit("No configuration found. Run the script with the --configure option")
    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    myserver = GameServer(gsconfig=gameserver)
    myserver.stop()

if args.restart:
    if not os.path.isfile(CONFIG_FILE):
        sys.exit("No configuration found. Run the script with the --configure option")
    parser.read(CONFIG_FILE)
    gameserver = parser._sections
    myserver = GameServer(gsconfig=gameserver)
    myserver.stop()
    myserver.start()



"""
while True:
    if os.path.isfile(CONFIG_FILE) and args.configure is False:
        parser.read(CONFIG_FILE)
        # Load the complete configuration for the gameserver
        gameserver = parser._sections

        myserver = GameServer(gsconfig=gameserver)

        break

    elif not os.path.isfile(CONFIG_FILE) or args.configure is True:
        # There is no configuration found. Need to generate one.
        gameserver = False

        myserver = GameServer(gsconfig=gameserver)

        # Start the configuration process
        myserver.configure()

        if args.configure:
            exit()

print "Gameserver configuration loaded."

# Need to know the constants here
INSTALL_DIR = os.path.dirname(gameserver['gameserver']['path'])

# Check to see if steamcmd is loaded. If not, install it!
if not os.path.isfile(os.path.join(INSTALL_DIR, 'steamcmd.sh')):
    myserver.install_steamcmd()

# Now go on to install game files
print "Downloading/Updating game files. If you wish to validate the gamefiles, use the --validate argument."
if args.validate:
    myserver.update_game_validate()
else:
    myserver.update_game_novalidate()
"""
