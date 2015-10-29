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

class L4D2Server(GameServer):
    def __init__(self, gsconfig):
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
            {'option': 'fork', 'info': 'How many server forks: [0] ', 'default': '0'},
            {'option': 'mp_disable_autokick', 'info': 'mp_disable_autokick: [0] ', 'default': '0'},
            {'option': 'sv_gametypes', 'info': 'sv_gametypes: [coop,realism,survival,versus,teamversus,scavenge,teamscavenge] ', 'default': 'coop,realism,survival,versus,teamversus,scavenge,teamscavenge'},
            {'option': 'mp_gamemode', 'info': 'sv_gamemode: [coop,realism,survival,versus,teamversus,scavenge,teamscavenge] ', 'default': 'coop,realism,survival,versus,teamversus,scavenge,teamscavenge'},
            {'option': 'sv_unlag', 'info': 'sv_unlag: [1] ', 'default': '1'},
            {'option': 'sv_maxunlag', 'info': 'sv_maxunlag: [.5] ', 'default': '.5'},
            {'option': 'sv_steamgroup_exclusive', 'info': 'sv_steamgroup_exclusive: [0] ', 'default': '0'},
        ]
        parser.read(CONFIG_FILE)
        myid = {'id': self.steam_appid}
        self.configure_list(myid,config_options)
        parser.write(open(CONFIG_FILE, 'w'))
        print "Configuration saved as {}".format(CONFIG_FILE)

    def status(self):
        """
        Method to check the server's status
        """
        steam_appid = self.gsconfig['steamcmd']['appid']
        s = Screen(steam_appid)
        is_server_running = s.exists
        return is_server_running

    def start(self):
        pass

    def stop(self):
        """
        Method to stop the server.
        """
        # Steam appid
        steam_appid = self.gsconfig['steamcmd']['appid']
        if self.status():
            s = Screen(steam_appid)
            s.kill()
            print "Server stopped."
        else:
           print "Server is not running."
