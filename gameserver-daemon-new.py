import sys
import os.path
import ConfigParser
from GameServer import GameServer


CONFIG_FILE = "server.conf"

parser = ConfigParser.RawConfigParser()

while True:
    if os.path.isfile(CONFIG_FILE):
        parser.read(CONFIG_FILE)
        # Load the complete configuration for the gameserver
        gameserver = parser._sections

        myserver = GameServer(gsconfig=gameserver)

        break

    else:
        # There is no configuration found. Need to generate one.
        gameserver = False

        myserver = GameServer(gsconfig=gameserver)
        
        # Start the configuration process
        myserver.configure()

print "Gameserver configuration loaded."

# Need to know the constants here
INSTALL_DIR = os.path.dirname(gameserver['gameserver']['path'])

# Check to see if steamcmd is loaded. If not, install it!
if not os.path.isfile(os.path.join(INSTALL_DIR, 'steamcmd.sh')):
    myserver.install_steamcmd()
else:
    pass
