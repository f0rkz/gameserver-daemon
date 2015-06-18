import ConfigParser
import os.path
import sys
import urllib
import subprocess
import tarfile
from jinja2 import Template
from screenutils import list_screens, Screen


parser = ConfigParser.RawConfigParser()
CONFIG_FILE = "server.conf"

class GameServer(object):
    def __init__(self, gsconfig):
        self.config = gsconfig
        if self.config:
            self.path = {
                'steamcmd': os.path.join(self.config['gameserver']['path'], ''),
                'gamedir': os.path.join(self.config['gameserver']['path'], self.config['gameserver']['name']),
                        }

    def configure(self):
        print "Configuration has been selected."

        """
        Configuration dictionaries template:
        thing [
            {'option': '', 'info': '', 'default': ''},
        ]
        
        If you want to force a user to enter a value:
        thing [
            {'option': '', 'info': ''},
        ]

        If you need to validate based on a list of options:
        thing [
            {'option': '', 'info': '', 'valid_option': ['option1', 'option2', 'option3']},
        ]
        """

        # -----------------------------------------
        # Steamcmd options for configuration
        # -----------------------------------------
        steamcmd_options = [
                {'option': 'user', 'info': 'Steam login: [anonymous] ', 'default': 'anonymous'},
                {'option': 'password', 'info': 'Steam password: [anonymous] ', 'default': 'anonymous'},
        ]

        # -------------------------------------------------
        # Base shared gameserver options for configuration
        # -------------------------------------------------
        gameserver_options = [
                {'option': 'appid', 'info': 'Steam AppID: '},
                {'option': 'path', 'info': 'Gameserver Install Path: '},
                {'option': 'name', 'info': 'Gameserver name, ie: csgo: '},
                {'option': 'daemon', 'info': 'Gameserver daemon: [srcds_run] ', 'default': 'srcds_run'},
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
        ]

        # ------------------------
        # CSGO gameserver options
        # ------------------------
        csgo_options = [
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

        # ------------------------------------
        # Black Mesa (bms) gameserver options
        # ------------------------------------
        bms_options = [
                {'option': 'teamplay', 'info': 'mp_teamplay: [0] ', 'default': '0'},
                {'option': 'timelimit', 'info': 'mp_timelimit: [900] ', 'default': '900'},
                {'option': 'warmup_time', 'info': 'mp_warmup_time: [30] ', 'default': '30'},
                {'option': 'fraglimit', 'info': 'mp_fraglimit: [50] ', 'default': '50'},
        ]

        # ----------------------------
        # TF2 (tf) gameserver options
        # ----------------------------
        tf_options = [
                {'option': 'mvm', 'info': 'Mann Versus Machine: [0] ', 'default': '0'},
                {'option': 'timelimit', 'info': 'mp_timelimit: [40] ', 'default': '40'},
                {'option': 'overtime_nag', 'info': 'tf_overtime_nag: [0] ', 'default': '0'},
                {'option': 'mm_servermode', 'info': 'tf_mm_servermode: [1] ', 'default': '1'},
                {'option': 'tf_server_identity_account_id', 'info': 'tf_server_identity_account_id: [none]', 'default': 'ignore'},
                {'option': 'tf_server_identity_token', 'info': 'tf_server_identity_token: [none]', 'default': 'ignore'}, 
        ]

        # ---------------------------------
        # hl2dm (hl2mp) gameserver options
        # ---------------------------------

        hl2mp_options = [
                {'option': 'fraglimit', 'info': 'mp_fraglimit: [50] ', 'default': '50'},
                {'option': 'timelimit', 'info': 'mp_timelimit: [30] ', 'default': '30'},
                {'option': 'teamplay', 'info': 'mp_teamplay: [0] ', 'default': '0'},
        ]

        # Method to take each options list above and process it. No more redundant loops!

        def configure_list(group, list):
            for config_object in list:
                while True:
                    user_input = raw_input(config_object['info'])
                    if user_input:
                        if config_object.get('valid_option') and not user_input in config_object['valid_option']:
                            print "Invalid option. Please chose one of the following: {}".format(config_object['valid_option'])
                        else:
                            group[config_object['option']] = user_input
                            break
                    if not config_object.get('default', None):
                        pass #loop back and ask again
                    else:
                        group[config_object['option']] = config_object['default']   # Default value set!
                        break
                parser.set(group['id'], config_object['option'], group[config_object['option']])

        # Base steamcmd login info

        steamcmd = {'id': 'steamcmd'}
        parser.add_section('steamcmd')
        configure_list(steamcmd,steamcmd_options)

        # Base gameserver information (common cvars)

        gameserver = {'id': 'gameserver'}
        parser.add_section('gameserver')
        configure_list(gameserver,gameserver_options)

        # Each game that is supported here

        if gameserver['name'] == 'csgo':
            csgo = {'id': 'csgo'}
            parser.add_section('csgo')
            configure_list(csgo,csgo_options)

        elif gameserver['name'] == 'hl2mp':
            hl2mp = {'id': 'hl2mp'}
            parser.add_section('hl2mp')
            configure_list(hl2mp,hl2mp_options)

        elif gameserver['name'] == 'tf':
            tf = {'id': 'tf'}
            parser.add_section('tf')
            configure_list(tf,tf_options)

        elif gameserver['name'] == 'bms':
            bms = {'id': 'bms'}
            parser.add_section('bms')
            configure_list(bms,bms_options)

        else:
            # Let the user know gameserver is not supported. This could be a user error or an actual game not supported.

            print "Gameserver name {} not supported by this script. Base configuration options will be used.".format(gameserver['name'])

        # Write the configuration file
        parser.write(open(CONFIG_FILE, 'w'))
        print "Configuration file saved as {}".format(CONFIG_FILE)

    def install_steamcmd(self):
        INSTALL_DIR = os.path.dirname(self.config['gameserver']['path'])
        STEAMCMD_DOWNLOAD = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"

        #Download steamcmd and extract it
        urllib.urlretrieve(STEAMCMD_DOWNLOAD, os.path.join(INSTALL_DIR, 'steamcmd_linux.tar.gz'))
        steamcmd_tar = tarfile.open(os.path.join(INSTALL_DIR, 'steamcmd_linux.tar.gz'), 'r:gz')
        steamcmd_tar.extractall(INSTALL_DIR)

    def update_game_validate(self):
        steamcmd_run = '{steamcmdpath}steamcmd.sh +login {login} {password} +force_install_dir {installdir} +app_update {id} validate +quit'.format(steamcmdpath=self.path['steamcmd'], login=self.config['steamcmd']['user'], password=self.config['steamcmd']['password'], installdir=self.path['gamedir'], id=self.config['gameserver']['appid'])
        subprocess.call(steamcmd_run, shell=True)

    def update_game_novalidate(self):
        steamcmd_run = '{steamcmdpath}steamcmd.sh +login {login} {password} +force_install_dir {installdir} +app_update {id} +quit'.format(steamcmdpath=self.path['steamcmd'], login=self.config['steamcmd']['user'], password=self.config['steamcmd']['password'], installdir=self.path['gamedir'], id=self.config['gameserver']['appid'])
        subprocess.call(steamcmd_run, shell=True)

    def create_runscript(self):
        with open(os.path.join('templates', 'runscript.txt'), "r") as file:
            x = file.read()

            template = Template(x)

            runscript_vars = {
                            'steamlogin': self.config['steamcmd']['user'],
                            'steampassword': self.config['steamcmd']['password'],
                            'install_dir': os.path.join(self.config['gameserver']['path'], self.config['gameserver']['name']),
                            'appid': self.config['gameserver']['appid']
            }

            output = template.render(runscript_vars)

            with open(os.path.join(self.config['gameserver']['path'],'runscript.txt'), "wb") as outfile:
                outfile.write(output)

        print "runscript.txt created"


    def create_servercfg(self):
        with open(os.path.join('templates', 'server.cfg'), "r") as file:
            x = file.read()
            template = Template(x)

            srcds_vars = self.config['gameserver']

            if srcds_vars['name'] == 'csgo':
                srcds_vars.update(self.config['csgo'])
            
            elif srcds_vars['name'] == 'bms':
                srcds_vars.update(self.config['bms'])

            elif srcds_vars['name'] == 'tf':
                srcds_vars.update(self.config['tf'])

            elif srcds_vars['name'] == 'hl2mp':
                srcds_vars.update(self.config['hl2mp'])

            output = template.render(srcds_vars)

            if srcds_vars['name'] == 'bms':
                with open(os.path.join(srcds_vars['path'],srcds_vars['name'],srcds_vars['name'],'cfg','servercustom.cfg'), "wb") as outfile:
                    outfile.write(output)
            else:
                with open(os.path.join(srcds_vars['path'],srcds_vars['name'],srcds_vars['name'],'cfg','server.cfg'), "wb") as outfile:
                    outfile.write(output)
        print "server.cfg saved"

    def create_motd(self):
        with open(os.path.join('templates', 'motd.txt'), "r") as file:
            x = file.read()

            template = Template(x)

            motd_vars = {
                        'motd': self.config['gameserver']['motd'],
            }

            output = template.render(motd_vars)

            with open(os.path.join(self.config['gameserver']['path'],self.config['gameserver']['name'],self.config['gameserver']['name'],'motd.txt'), "wb") as outfile:
                outfile.write(output)
        print "motd.txt saved"

    def status(self):
        s = Screen(self.config['gameserver']['name'])
        is_server_running = s.exists
        return is_server_running

    def start(self):
        # Catch CSGO gamemode and mapgroup, then start it up
        if self.config['gameserver']['name'] == 'csgo':
            if not self.config['csgo']['mapgroup'] == 'none':
                srcds_launch = '-game {game} -console -usercon -secure -autoupdate -steam_dir {steam_dir} -steamcmd_script {runscript} -maxplayers_override {maxplayers} -tickrate {tickrate} +port {port} +ip {ip} +map {map} +mapgroup {mapgroup}'.format(game=self.config['gameserver']['name'], steam_dir=self.config['gameserver']['path'], runscript='runscript.txt', maxplayers=self.config['gameserver']['maxplayers'], tickrate=self.config['gameserver']['tickrate'], port=self.config['gameserver']['port'], ip=self.config['gameserver']['ip'], map=self.config['gameserver']['map'], mapgroup=self.config['csgo']['mapgroup'])
            
            else:
                srcds_launch = '-game {game} -console -usercon -secure -autoupdate -steam_dir {steam_dir} -steamcmd_script {runscript} -maxplayers_override {maxplayers} -tickrate {tickrate} +port {port} +ip {ip} +map {map}'.format(game=self.config['gameserver']['name'], steam_dir=self.config['gameserver']['path'], runscript='runscript.txt', maxplayers=self.config['gameserver']['maxplayers'], tickrate=self.config['gameserver']['tickrate'], port=self.config['gameserver']['port'], ip=self.config['gameserver']['ip'], map=self.config['gameserver']['map'])
            
            if not self.config['csgo']['gamemode'] == 'none':
                
                gamemode = self.config['csgo']['gamemode']
                
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
            
            
        elif self.config['gameserver']['name'] == 'tf':
            # Catch mann versus machine
            if self.config['tf']['mvm']:
                srcds_launch =  srcds_launch = '-game {game} -console -usercon -secure -autoupdate -steam_dir {steam_dir} -steamcmd_script {runscript} -maxplayers 32 +port {port} +ip {ip} +map {map}'.format(game=self.config['gameserver']['name'], steam_dir=self.config['gameserver']['path'], runscript='runscript.txt', port=self.config['gameserver']['port'], ip=self.config['gameserver']['ip'], map=self.config['gameserver']['map'])
                extra_parameters = "+tf_mm_servermode 2"
            else:
                srcds_launch =  srcds_launch = '-game {game} -console -usercon -secure -autoupdate -steam_dir {steam_dir} -steamcmd_script {runscript} -maxplayers {maxplayers} +port {port} +ip {ip} +map {map}'.format(game=self.config['gameserver']['name'], steam_dir=self.config['gameserver']['path'], runscript='runscript.txt', maxplayers=self.config['gameserver']['maxplayers'], port=self.config['gameserver']['port'], ip=self.config['gameserver']['ip'], map=self.config['gameserver']['map'])
                extra_parameters = ''
            
        elif self.config['gameserver']['name'] == 'bms':
            # Catch alrternative configuration file, then start it up
            srcds_launch =  srcds_launch = '-game {game} -console -usercon -secure -autoupdate -steam_dir {steam_dir} -steamcmd_script {runscript} -maxplayers {maxplayers} +port {port} +ip {ip} +map {map} +servercfgfile servercustom.cfg'.format(game=self.config['gameserver']['name'], steam_dir=self.config['gameserver']['path'], runscript='runscript.txt', maxplayers=self.config['gameserver']['maxplayers'], port=self.config['gameserver']['port'], ip=self.config['gameserver']['ip'], map=self.config['gameserver']['map'])
            extra_parameters = ''

        else:
            srcds_launch =  srcds_launch = '-game {game} -console -usercon -secure -autoupdate -steam_dir {steam_dir} -steamcmd_script {runscript} -maxplayers {maxplayers} +port {port} +ip {ip} +map {map}'.format(game=self.config['gameserver']['name'], steam_dir=self.config['gameserver']['path'], runscript='runscript.txt', maxplayers=self.config['gameserver']['maxplayers'], port=self.config['gameserver']['port'], ip=self.config['gameserver']['ip'], map=self.config['gameserver']['map'])
            extra_parameters = ''

        srcds_run = '{path}/srcds_run {launch} {extra}'.format(path=os.path.join(self.config['gameserver']['path'],self.config['gameserver']['name']), launch=srcds_launch, extra=extra_parameters)

        s = Screen(self.config['gameserver']['name'], True)
        s.send_commands(srcds_run)

    def stop(self):
        if self.status():
            s = Screen(self.config['gameserver']['name'])
            s.kill()
            print "Server stopped."
        else:
           print "Server is not running."