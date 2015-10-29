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

class CSGOServer(GameServer):
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
            {'option': 'gamemode', 'info': 'Gamemode: casual , competitive , armsrace , demolition , deathmatch , none : ', 'valid_option': ['casual', 'competitive', 'armsrace', 'demolition', 'deathmatch', 'none']},
            {'option': 'mapgroup', 'info': 'Mapgroup: mg_op_op06 , mg_op_op05 , mg_op_breakout , mg_active , mg_reserves , mg_armsrace , mg_demolition , none : ', 'valid_option': ['mg_op_op06', 'mg_op_op05', 'mg_op_breakout', 'mg_active', 'mg_reserves', 'mg_armsrace', 'mg_demolition', 'none']},
            {'option': 'deadtalk', 'info': 'sv_deadtalk: [0] ', 'default': '0'},
            {'option': 'full_alltalk', 'info': 'sv_full_alltalk: [0] ', 'default': '0'},
            {'option': 'pausable', 'info': 'sv_pausable: [0] ', 'default': '0'},
            {'option': 'limitteams', 'info': 'mp_limitteams: [1] ', 'default': '1'},
            {'option': 'friendlyfire', 'info': 'mp_friendlyfire: [0] ', 'default': '0'},
            {'option': 'teambalance', 'info': 'mp_autoteambalance: [1] ', 'default': '1'},
            {'option': 'autokick', 'info': 'mp_autokick: [1] ', 'default': '1'},
            {'option': 'tkpunish', 'info': 'mp_tkpunish: [1] ', 'default': '1'},
            {'option': 'freezetime', 'info': 'mp_freezetime: [6] ', 'default': '6'},
            {'option': 'maxrounds', 'info': 'mp_maxrounds: [0] ', 'default': '0'},
            {'option': 'roundtime', 'info': 'mp_roundtime: [5] ', 'default': '5'},
            {'option': 'timelimit', 'info': 'mp_timelimit: [5] ', 'default': '5'},
            {'option': 'buytime', 'info': 'mp_buytime: [90] ', 'default': '90'},
            {'option': 'warmup_period', 'info': 'mp_do_warmup_period: [1] ', 'default': '1'},
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
