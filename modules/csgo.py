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
    '740': 'csgo',
}

class CSGOServer(GameServer):
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
        """
        Method to start the SRCDS gameserver.
        There is a lot of customization going on here for each game.
        """
        steam_appid = self.gsconfig['steamcmd']['appid']
        # Figure out if there is a mapgroup to go with this launch.
        if not self.gsconfig[steam_appid]['mapgroup'] == 'none':
            srcds_launch = '-game {game} ' \
                           ' -console -usercon -secure -autoupdate ' \
                           '-steam_dir {steam_dir} ' \
                           '-steamcmd_script {runscript} ' \
                           '-maxplayers_override {maxplayers} ' \
                           '-tickrate {tickrate} ' \
                           '+port {port} ' \
                           '+ip {ip} ' \
                           '+map {map} ' \
                           '+mapgroup {mapgroup}' \
                           .format(game=GAME[steam_appid],
                                   steam_dir=self.path['steamcmd'],
                                   runscript='runscript.txt',
                                   maxplayers=self.gsconfig[steam_appid]['maxplayers'],
                                   tickrate=self.gsconfig[steam_appid]['tickrate'],
                                   port=self.gsconfig[steam_appid]['port'],
                                   ip=self.gsconfig[steam_appid]['ip'],
                                   map=self.gsconfig[steam_appid]['map'],
                                   mapgroup=self.gsconfig[steam_appid]['mapgroup'],
                                   steamaccount=self.gsconfig[steam_appid]['sv_setsteamaccount']
                                  )
        else:
            srcds_launch = '-game {game} ' \
                           '-console -usercon -secure -autoupdate ' \
                           '-steam_dir {steam_dir} ' \
                           '-steamcmd_script {runscript} ' \
                           '-maxplayers_override {maxplayers} ' \
                           '-tickrate {tickrate} ' \
                           '+port {port} ' \
                           '+ip {ip} ' \
                           '+map {map}' \
                           .format(game=GAME[steam_appid],
                                   steam_dir=self.path['steamcmd'],
                                   runscript='runscript.txt',
                                   maxplayers=self.gsconfig[steam_appid]['maxplayers'],
                                   tickrate=self.gsconfig[steam_appid]['tickrate'],
                                   port=self.gsconfig[steam_appid]['port'],
                                   ip=self.gsconfig[steam_appid]['ip'],
                                   map=self.gsconfig[steam_appid]['map'],
                                   steamaccount=self.gsconfig[steam_appid]['sv_setsteamaccount']
                                  )
        # Catch the gamemode and throw it as an extra launch option
        if not self.gsconfig[steam_appid]['gamemode'] == 'none':
                gamemode = self.gsconfig[steam_appid]['gamemode']

                if gamemode == 'casual':
                    extra_parameters = "+game_type 0 +game_mode 0"

                elif gamemode == 'competitive':
                    extra_parameters = "+game_type 0 +game_mode 1"

                elif gamemode == 'armsrace':
                    extra_parameters = "+game_type 1 +game_mode 0"

                elif gamemode == 'demolition':
                    extra_parameters = "+game_type 1 +game_mode 1"

                elif gamemode == 'deathmatch':
                    extra_parameters = "+game_type 1 +game_mode 2"
                else:
                    gamemode_launch = ''

        # Form up the SRCDS launch command
        srcds_run = '{path}/srcds_run {launch} {extra}' \
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
