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

class SRCDS(GameServer):
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
            {'option': 'hostname', 'info': 'Gameserver hostname: [My Gameserver] ', 'default': 'My Gameserver'},
            {'option': 'ip', 'info': 'Gameserver IP: [0.0.0.0] ', 'default': '0.0.0.0'},
            {'option': 'port', 'info': 'Gameserver port: [27015] ', 'default': '27015'},
            {'option': 'tickrate', 'info': 'Gameserver tickrate: [60] ', 'default': '60'},
            {'option': 'maxplayers', 'info': 'Gameserver max players: [16] ', 'default': '16'},
            {'option': 'map', 'info': 'Gameserver start map: '},
            {'option': 'rcon', 'info': 'Rcon password: '},
            {'option': 'region', 'info': 'Server region: [0] ', 'default': '0'},
            {'option': 'steamgroup', 'info': 'Steamgroup ID: [null]', 'default': 'ignore'},
            {'option': 'lan', 'info': 'LAN Server (sv_lan): [0] ', 'default': '0'},
            {'option': 'alltalk', 'info': 'sv_alltalk: [0] ', 'default': '0'},
            {'option': 'voiceenable', 'info': 'sv_voiceenable: [1] ', 'default': '1'},
            {'option': 'pure', 'info': 'sv_pure: [1] ', 'default': '1'},
            {'option': 'consistency', 'info': 'sv_consistency: [1] ', 'default': '1'},
            {'option': 'password', 'info': 'sv_password: [none]', 'default': 'ignore'},
            {'option': 'rcon_banpenalty', 'info': 'sv_rcon_banpenalty: [15] ', 'default': '15'},
            {'option': 'rcon_minfailures', 'info': 'sv_rcon_minfailures: [5] ', 'default': '5'},
            {'option': 'rcon_maxfailures', 'info': 'sv_rcon_maxfailures: [10] ', 'default': '10'},
            {'option': 'rcon_maxfailuretime', 'info': 'sv_rcon_maxfailuretime: [30] ', 'default': '30'},
            {'option': 'rcon_maxpacketsize', 'info': 'sv_rcon_maxpacketsize: [1024] ', 'default': '1024'},
            {'option': 'rcon_maxpacketbans', 'info': 'sv_rcon_maxpacketbans: [1] ', 'default': '1'},
            {'option': 'log', 'info': 'log: [on] ', 'default': 'on'},
            {'option': 'logbans', 'info': 'sv_logbans: [1] ', 'default': '1'},
            {'option': 'logecho', 'info': 'sv_logecho: [1] ', 'default': '1'},
            {'option': 'log_onefile', 'info': 'sv_log_onefile: [0] ', 'default': '0'},
            {'option': 'net_maxfilesize', 'info': 'net_maxfilesize: [64] ', 'default': '64'},
            {'option': 'downloadurl', 'info': 'sv_downloadurl: [] ', 'default': 'ignore'},
            {'option': 'allowdownload', 'info': 'sv_allowdownload: [1] ', 'default': '1'},
            {'option': 'allowupload', 'info': 'sv_allowupload: [1] ', 'default': '1'},
            {'option': 'pure_kick_clients', 'info': 'sv_pure_kick_clients: [0] ', 'default': '0'},
            {'option': 'pure_trace', 'info': 'sv_pure_trace: [0] ', 'default': '0'},
            {'option': 'motd', 'info': 'MOTD URL: [] ', 'default': 'ignore'},
            {'option': 'sv_setsteamaccount', 'info': 'sv_setsteamaccount: [] ', 'default': 'ignore'},
        ]
        myid = {'id': self.steam_appid}
        parser.add_section(self.steam_appid)
        self.configure_list(myid,config_options)
        parser.write(open(CONFIG_FILE, 'w'))
        print "SRCDS configuration saved as {}".format(CONFIG_FILE)
