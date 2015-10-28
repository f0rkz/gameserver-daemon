import ConfigParser
import os.path
import sys
import urllib
import subprocess
import tarfile
from jinja2 import Template
from screenutils import list_screens, Screen

from modules.gameserver import GameServer

parser = ConfigParser.RawConfigParser()
CONFIG_FILE = "server.conf"

class BMSServer(GameServer):
    def __init__(self):
        # Bring the gsconfig and path variables over
        super(GameServer, self).__init__()
        self.gsconfig = gsconfig
        self.steam_appid = self.gsconfig['steamcmd']['appid']

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
        config_options = [
            {'option': 'teamplay', 'info': 'mp_teamplay: [0] ', 'default': '0'},
            {'option': 'timelimit', 'info': 'mp_timelimit: [900] ', 'default': '900'},
            {'option': 'warmup_time', 'info': 'mp_warmup_time: [30] ', 'default': '30'},
            {'option': 'fraglimit', 'info': 'mp_fraglimit: [50] ', 'default': '50'},
        ]
        parser.read(CONFIG_FILE)
        myid = {'id': self.steam_appid}
        parser.add_section(self.steam_appid)
        self.configure_list(myid,config_options)
        parser.write(open(CONFIG_FILE, 'w'))
        print "Configuration saved as {}".format(CONFIG_FILE)

    def status(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass
