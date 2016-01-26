# APPID 276060
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
    '276060': 'svencoop',
}

class SvenCoopServer(GameServer):
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
        # {'option': '', 'info': ' ', 'default': ''},
        config_options = [
            {'option': 'skill', 'info': 'skill [0-3] ', 'default': '0'},
            {'option': 'mp_allowmonsterinfo', 'info': 'mp_allowmonsterinfo [1] ', 'default': '1'},
            {'option': 'mp_banana', 'info': 'mp_banana [1] ', 'default': '1'},
            {'option': 'mp_chattime', 'info': 'mp_chattime [8] ', 'default': '8'},
            {'option': 'mp_disable_autoclimb', 'info': 'mp_disable_autoclimb [0] ', 'default': '0'},
            {'option': 'mp_disable_pcbalancing', 'info': 'mp_disable_pcbalancing [0] ', 'default': '0'},
            {'option': 'mp_disable_player_rappel', 'info': 'mp_disable_player_rappel [0] ', 'default': '0'},
            {'option': 'mp_dropweapons', 'info': 'mp_dropweapons [1] ', 'default': '1'},
            {'option': 'mp_grapple_mode', 'info': 'mp_grapple_mode [1] ', 'default': '1'},
            {'option': 'mp_multiplespawn', 'info': 'mp_multiplespawn [1] ', 'default': '1'},
            {'option': 'mp_no_akimbo_uzis', 'info': 'mp_no_akimbo_uzis [0] ', 'default': '0'},
            {'option': 'mp_noblastgibs', 'info': 'mp_noblastgibs [0] ', 'default': '0'},
            {'option': 'mp_npckill', 'info': 'mp_npckill [2] ', 'default': '2'},
            {'option': 'mp_playervotedelay', 'info': 'mp_playervotedelay [300] ', 'default': '300'},
            {'option': 'mp_voteallow', 'info': 'mp_voteallow [1] ', 'default': '1'},
            {'option': 'mp_votebanrequired', 'info': 'mp_votebanrequired [100] ', 'default': '100'},
            {'option': 'mp_votekickrequired', 'info': 'mp_votekickrequired [66] ', 'default': '66'},
            {'option': 'mp_votekill_respawndelay', 'info': 'mp_votekill_respawndelay [15] ', 'default': '15'},
            {'option': 'mp_votekillrequired', 'info': 'mp_votekillrequired [51] ', 'default': '51'},
            {'option': 'mp_votemaprequired', 'info': 'mp_votemaprequired [66] ', 'default': '66'},
            {'option': 'mp_votetimebetween', 'info': 'mp_votetimebetween [60] ', 'default': '60'},
            {'option': 'mp_votetimecheck', 'info': 'mp_votetimecheck [20] ', 'default': '20'},
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
        steam_appid = self.gsconfig['steamcmd']['appid']
        srcds_launch = '-console -usercon -debug ' \
                       '-secure -autoupdate ' \
                       '-steam_dir {steam_dir} ' \
                       '-steamcmd_script {runscript} ' \
                       '-maxplayers {maxplayers} ' \
                       '+port {port} ' \
                       '+ip {ip} ' \
                       '+map {map}' \
                       .format(game=GAME[steam_appid],
                               steam_dir=self.path['steamcmd'],
                               runscript='runscript.txt',
                               maxplayers=self.gsconfig[steam_appid]['maxplayers'],
                               port=self.gsconfig[steam_appid]['port'],
                               ip=self.gsconfig[steam_appid]['ip'],
                               map=self.gsconfig[steam_appid]['map']
                              )
        extra_parameters = ''
        srcds_run = 'cd {path}; {path}/svends_run {launch} {extra}' \
                    .format(path=self.path['game'],
                            launch=srcds_launch,
                            extra=extra_parameters
                           )

        s = Screen(steam_appid, True)
        s.send_commands(srcds_run)

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
