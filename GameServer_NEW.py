import ConfigParser
import os.path
import sys
import urllib
import subprocess
import tarfile
from jinja2 import Template
from screenutils import list_screens, Screen

# Important constants within the class
CONFIG_FILE = "server.conf"
STEAMCMD_DOWNLOAD = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"

# Dictionary of game subdirectories for configuration
# Also used for the game name in srcds launching
GAME = {
    '232250': 'tf',
    '740': 'csgo',
    '232370': 'hl2mp',
    '346680': 'bms',
    '222860': 'left4dead2',
    '376030': 'ShooterGame',
}

# Configuration parser variable. Don't touch this.
parser = ConfigParser.RawConfigParser()

class GameServer(object):
    """docstring for GameServer"""
    def __init__(self, gsconfig):
        super(GameServer, self).__init__()
        self.gsconfig = gsconfig
    def configure_list(self, group, options):
        """
        Method used to loop through configuration lists and prompt the user
        """
        for config_object in options:
            while True:
                user_input = raw_input(config_object['info'])
                if user_input:
                    if config_object.get('valid_option') and not user_input in config_object['valid_option']:
                        print "Invalid option. Please chose one of the following: {}".format(config_object['valid_option'])
                    else:
                        group[config_object['option']] = user_input
                        break
                if not config_object.get('default', None):
                    #loop back and ask again
                    pass
                else:
                    # Default value set!
                    group[config_object['option']] = config_object['default']
                    break
        parser.set(group['id'], config_object['option'], group[config_object['option']])
    def configure(self):
        """
        configure docstring
        """
        # Configure the base srcds setup
        configure_options = [
            {'option': 'user', 'info': 'Steam login: [anonymous] ', 'default': 'anonymous'},
            {'option': 'password', 'info': 'Steam password: [anonymous] ', 'default': 'anonymous'},
            {'option': 'path', 'info': 'Gameserver base path: (example: /home/steam/mygame.mydomain.com) '},
            {'option': 'appid', 'info': 'Steam AppID: '},
            {'option': 'engine', 'info': 'Gameserver engine (srcds / unreal): [srcds] ', 'default': 'srcds', 'valid_option': ['unreal', 'srcds']}
        ]
        steamcmd = {'id': 'steamcmd'}
        parser.add_section('steamcmd')
        self.configure_list(steamcmd,configure_options)
        parser.write(open(CONFIG_FILE, 'w'))
        print "Base configuration file saved as {}".format(CONFIG_FILE)
