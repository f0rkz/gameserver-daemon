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

# Dictionary of game subdirectories for configuration
# Also used for the game name in srcds launching
GAME = {
    '276060', 'svencoop',
}

class HLDS(GameServer):
    def __init__(self, gsconfig):
        # Bring the gsconfig and path variables over
        super(GameServer, self).__init__()
        self.gsconfig = gsconfig
        self.steam_appid = self.gsconfig['steamcmd']['appid']
        if self.gsconfig:
            self.path = {
                'steamcmd': os.path.join(self.gsconfig['steamcmd']['path'], ''),
                'game': os.path.join(self.gsconfig['steamcmd']['path'], self.gsconfig['steamcmd']['appid']),
            }

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
            {'option': 'sys_tickrate', 'info': 'sys_tickrate [128] ', 'default': '128'},
            {'option': 'fps_max', 'info': 'fps_max [128] ', 'default': '128'},
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
        ]
        parser.read(CONFIG_FILE)
        myid = {'id': self.steam_appid}
        parser.add_section(self.steam_appid)
        self.configure_list(myid,config_options)
        parser.write(open(CONFIG_FILE, 'w'))
        print "Configuration saved as {}".format(CONFIG_FILE)

    def create_runscript(self):
        """
        A runscript is required for steamcmd to update the server at start.
        Because this is very useful, we provide a method to do just that.
        """
        steam_appid = self.gsconfig['steamcmd']['appid']
        with open(os.path.join('templates', 'runscript.txt'), "r") as file:
            x = file.read()

            template = Template(x)

            runscript_vars = {
                            'steamlogin': self.gsconfig['steamcmd']['user'],
                            'steampassword': self.gsconfig['steamcmd']['password'],
                            'install_dir': os.path.join(self.path['game'], ''),
                            'appid': steam_appid,
            }

            output = template.render(runscript_vars)

            with open(os.path.join(self.path['steamcmd'],'runscript.txt'), "wb") as outfile:
                outfile.write(output)

        print "runscript.txt created"

    def create_motd(self):
        """
        The MOTD is a webpage that loads up when a player enters a SRCDS game.
        The MOTD is formatted with a single URL (http://) included.
        HTTPS is not supported by SRCDS's MOTD.
        Example: http://yoursite.com/motd.html
        """
        steam_appid = self.gsconfig['steamcmd']['appid']
        with open(os.path.join('templates', 'motd.txt'), "r") as file:
            x = file.read()

            template = Template(x)

            motd_vars = {
                        'motd': self.gsconfig[steam_appid]['motd'],
            }

            output = template.render(motd_vars)

            with open(os.path.join(self.path['game'],GAME[steam_appid],'motd.txt'), "wb") as outfile:
                outfile.write(output)
        print "motd.txt saved"

    def create_servercfg(self):
        """
        Create a server.cfg file based on the settings configured by the script.
        A user is not limited to the cvar's set in this script, it allows a good
        base of cvars to use. Users can edit the server.cfg file by hand, but the
        file will be overwritten when --servercfg argument is passed to the script.
        """
        with open(os.path.join('templates', 'server.cfg'), "r") as file:
            x = file.read()
            template = Template(x)

            appid = self.gsconfig['steamcmd']['appid']
            srcds_vars = self.gsconfig[appid]

            output = template.render(srcds_vars)

            # svencoop support
            if appid == '276060':
                with open(os.path.join(self.path['game'],GAME[appid],'svencoop','server.cfg'), "wb") as outfile:
                    outfile.write(output)
            else:
                with open(os.path.join(self.path['game'],GAME[appid],'cfg','server.cfg'), "wb") as outfile:
                    outfile.write(output)
        print "server.cfg saved"
