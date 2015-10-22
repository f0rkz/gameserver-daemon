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
GAME_DIRECTORY = {
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
    def __init__(self,gsconfig):
        self.gsconfig = gsconfig
        if self.gsconfig:
            self.path = {
                'steamcmd': os.path.join(self.gsconfig['steamcmd']['path'], ''),
                'gamedir': os.path.join(self.gsconfig['steamcmd']['path'], self.gsconfig['steamcmd']['appid']),
            }

    """
    Configuration method of the shared information between engines
    """
    def configure(self):
        """
        Method used to loop through configuration lists and prompt the user
        """
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

        """
        Host of steamcmd options and data about the game files
        """
        steamcmd_options = [
                {'option': 'user', 'info': 'Steam login: [anonymous] ', 'default': 'anonymous'},
                {'option': 'password', 'info': 'Steam password: [anonymous] ', 'default': 'anonymous'},
                {'option': 'path', 'info': 'Gameserver base path: (example: /home/steam/mygame.mydomain.com) '},
                {'option': 'appid', 'info': 'Steam AppID: '},
                {'option': 'engine', 'info': 'Gameserver engine (srcds / unreal): [srcds] ', 'default': 'srcds', 'valid_option': ['unreal', 'srcds']}
        ]
        """
        Save the steam cmd configuration items
        """
        steamcmd = {'id': 'steamcmd'}
        parser.add_section('steamcmd')
        configure_list(steamcmd,steamcmd_options)

        parser.write(open(CONFIG_FILE, 'w'))
        print "Configuration file saved as {}".format(CONFIG_FILE)
        # Base configuration is saved now. We can configure it with gameserver options

        """
        Load up the recently saved configuration so we can get basic information
        about the game.
        """
        # Load up the configuration file so we can parse the appid
        parser.read(CONFIG_FILE)
        gameserver_settings = parser._sections
        steam_appid = gameserver_settings['steamcmd']['appid']
        engine = gameserver_settings['steamcmd']['engine']

        """
        Here be options
        """
        # Catch if the server is unreal or srcds. It matters.
        if engine == 'unreal':
            # Shared Unreal Options
            options = [
                {'option': 'ip', 'info': 'Gameserver IP: [0.0.0.0] ', 'default': '0.0.0.0'},
                {'option': 'hostname', 'info': 'Gameserver Hostname: [My Gameserver] ', 'default': 'My Gameserver'},
            ]

            # ARK: Survival Evolved
            if steam_appid == '376030':
                #./ShooterGameServer TheIsland?listen?SessionName=<server_name>?ServerPassword=<join_password>?ServerAdminPassword=<admin_password> -server -log
                options += [
                    {'option': 'ServerPassword', 'info': 'Private Server Password: [none]', 'default': ''},
                    {'option': 'ServerAdminPassword', 'info': 'Admin Password [reset_me]', 'default': 'reset_me'},
                ]

            # Killing Floor 1
            elif steam_appid == '215360':
                pass

            # Killing Floor 2 (lol just kidding.)
            # Probably need to update this whenever KF2 gets linux support
            elif steam_appid == '232130':
                pass

        elif engine == 'srcds':
            # Shared SRCDS Options
            options = [
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

            # Team Fotress 2
            if steam_appid == '232250':
                # Configuration options for TF2
                options += [
                    {'option': 'mvm', 'info': 'Mann Versus Machine: [0] ', 'default': '0'},
                    {'option': 'timelimit', 'info': 'mp_timelimit: [40] ', 'default': '40'},
                    {'option': 'winlimit', 'info': 'mp_winlimit: [0] ', 'default': '0'},
                    {'option': 'overtime_nag', 'info': 'tf_overtime_nag: [0] ', 'default': '0'},
                    {'option': 'tf_mm_servermode', 'info': 'tf_mm_servermode [1] ', 'default': '1', 'valid_option': ['0', '1', '2']},
                    {'option': 'tf_server_identity_account_id', 'info': 'tf_server_identity_account_id: [none]', 'default': 'ignore'},
                    {'option': 'tf_server_identity_token', 'info': 'tf_server_identity_token: [none]', 'default': 'ignore'},
                    {'option': 'mp_disable_respawn_times', 'info': 'mp_disable_respawn_times: [0]', 'default': '0', 'valid_option': ['0', '1']},
                ]

            # Counter-Strike: GO
            elif steam_appid == '740':
                options += [
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

            # Half-Life 2: deathmatch
            elif steam_appid == '232370':
                options += [
                    {'option': 'fraglimit', 'info': 'mp_fraglimit: [50] ', 'default': '50'},
                    {'option': 'timelimit', 'info': 'mp_timelimit: [30] ', 'default': '30'},
                    {'option': 'teamplay', 'info': 'mp_teamplay: [0] ', 'default': '0'},
                ]

            # Black Mesa
            elif steam_appid == '346680':
                options += [
                    {'option': 'teamplay', 'info': 'mp_teamplay: [0] ', 'default': '0'},
                    {'option': 'timelimit', 'info': 'mp_timelimit: [900] ', 'default': '900'},
                    {'option': 'warmup_time', 'info': 'mp_warmup_time: [30] ', 'default': '30'},
                    {'option': 'fraglimit', 'info': 'mp_fraglimit: [50] ', 'default': '50'},
                ]

            # Left4Dead2
            elif steam_appid == '222860':
                options += [
                    {'option': 'fork', 'info': 'How many server forks: [0] ', 'default': '0'},
                    {'option': 'mp_disable_autokick', 'info': 'mp_disable_autokick: [0] ', 'default': '0'},
                    {'option': 'sv_gametypes', 'info': 'sv_gametypes: [coop,realism,survival,versus,teamversus,scavenge,teamscavenge] ', 'default': 'coop,realism,survival,versus,teamversus,scavenge,teamscavenge'},
                    {'option': 'mp_gamemode', 'info': 'sv_gamemode: [coop,realism,survival,versus,teamversus,scavenge,teamscavenge] ', 'default': 'coop,realism,survival,versus,teamversus,scavenge,teamscavenge'},
                    {'option': 'sv_unlag', 'info': 'sv_unlag: [1] ', 'default': '1'},
                    {'option': 'sv_maxunlag', 'info': 'sv_maxunlag: [.5] ', 'default': '.5'},
                    {'option': 'sv_steamgroup_exclusive', 'info': 'sv_steamgroup_exclusive: [0] ', 'default': '0'},
                ]

        else:
            print "Something went wrong. Your engine: '%s' is not supported. You should not even be reading this!" % engine
            print "Reconfigure the script and follow the prompts. Manual configuration is not a wise choice."
            exit()

        # Run through the config options, you filthy animal
        game = {'id': steam_appid}
        parser.add_section(steam_appid)
        configure_list(game,options)

        # Write the configuration file
        parser.write(open(CONFIG_FILE, 'w'))
        print "Configuration file saved as {}".format(CONFIG_FILE)


    """
    Method to install steamcmd from the web. Modify STEAMCMD_DOWNLOAD if the
    link changes. STEAMCMD_DOWNLOAD can be found at the top of this class file.
    """
    def install_steamcmd(self):
        if self.gsconfig:
            while True:
                if os.path.exists(self.path['steamcmd']):
                    INSTALL_DIR = os.path.dirname(self.path['steamcmd'])
                    #Download steamcmd and extract it
                    urllib.urlretrieve(STEAMCMD_DOWNLOAD, os.path.join(INSTALL_DIR, 'steamcmd_linux.tar.gz'))
                    steamcmd_tar = tarfile.open(os.path.join(INSTALL_DIR, 'steamcmd_linux.tar.gz'), 'r:gz')
                    steamcmd_tar.extractall(INSTALL_DIR)
                    break
                else:
                    # Create the directory
                    os.makedirs(self.path['steamcmd'])
        else:
            print "Error: No configuration file found. Please run with the --configure option"

    """
    Method to update game files with the validate option
    """
    def update_game_validate(self):
        steamcmd_run = '{steamcmdpath}steamcmd.sh +login {login} {password} +force_install_dir {installdir} +app_update {id} validate +quit'.format(steamcmdpath=self.path['steamcmd'], login=self.config['steamcmd']['user'], password=self.config['steamcmd']['password'], installdir=self.path['gamedir'], id=self.config['gameserver']['appid'])
        subprocess.call(steamcmd_run, shell=True)

    """
    Method to update game files without the validate option
    """
    def update_game_novalidate(self):
        steamcmd_run = '{steamcmdpath}steamcmd.sh +login {login} {password} +force_install_dir {installdir} +app_update {id} +quit'.format(steamcmdpath=self.path['steamcmd'], login=self.config['steamcmd']['user'], password=self.config['steamcmd']['password'], installdir=self.path['gamedir'], id=self.config['gameserver']['appid'])
        subprocess.call(steamcmd_run, shell=True)

class SRCDSGameServer(GameServer):
    def __init__(self,gsconfig):
        self.gsconfig = gsconfig
        if self.gsconfig:
            self.path = {
                'steamcmd': os.path.join(self.gsconfig['steamcmd']['path'], ''),
                'gamedir': os.path.join(self.gsconfig['steamcmd']['path'], self.gsconfig['steamcmd']['appid'])
            }

    def start(self):
        steam_appid = gameserver_settings['steamcmd']['appid']

    def stop(self):
        if self.status():
            s = Screen(self.config['gameserver']['name'])
            s.kill()
            print "Server stopped."
        else:
           print "Server is not running."

    def create_runscript(self):
            with open(os.path.join('templates', 'runscript.txt'), "r") as file:
                x = file.read()

                template = Template(x)

                runscript_vars = {
                                'steamlogin': self.gsconfig['steamcmd']['user'],
                                'steampassword': self.gsconfig['steamcmd']['password'],
                                'install_dir': os.path.join(self.path['gamedir'], ''),
                                'appid': self.config['steamcmd']['appid']
                }

                output = template.render(runscript_vars)

                with open(os.path.join(self.path['steamcmd']['path'],'runscript.txt'), "wb") as outfile:
                    outfile.write(output)

            print "runscript.txt created"

    def create_servercfg(self):
        with open(os.path.join('templates', 'server.cfg'), "r") as file:
            x = file.read()
            template = Template(x)

            appid = self.gsconfig['steamcmd']['appid']
            srcds_vars = self.gsconfig[appid]

            output = template.render(srcds_vars)

            if appid == '346680':
                with open(os.path.join(self.path['gamedir'],GAME_DIRECTORY[appid],'cfg','servercustom.cfg'), "wb") as outfile:
                    outfile.write(output)
            else:
                with open(os.path.join(self.path['gamedir'],GAME_DIRECTORY[appid],'cfg','server.cfg'), "wb") as outfile:
                    outfile.write(output)
        print "server.cfg saved"

class UnrealGameServer(GameServer):
    def __init__(self,gsconfig):
        self.gsconfig = gsconfig
        if self.gsconfig:
            self.path = {
                'steamcmd': os.path.join(self.gsconfig['steamcmd']['path'], ''),
                'gamedir': os.path.join(self.gsconfig['steamcmd']['path'], self.gsconfig['steamcmd']['appid']),
            }

    def start(self):
        steam_appid = gameserver_settings['steamcmd']['appid']
        # Start Ark
        if steam_appid == '376030':
            run_commands = '{gamedir}'

        s = Screen(steam_appid, True)
        s.send_commands(srcds_run)

    def stop(self):
        if self.status():
            s = Screen(self.config['gameserver']['name'])
            s.kill()
            print "Server stopped."
        else:
           print "Server is not running."
