import ConfigParser
import os.path
import sys
import urllib
import tarfile

parser = ConfigParser.RawConfigParser()
CONFIG_FILE = "server.conf"

class GameServer(object):
    def __init__(self, gsconfig):
        self.config = gsconfig

    def configure(self):
        print "A configuration file was not found. Doing a first run."
        # Initialize dicts and configuration files.
        gameserver = {}
        steamcmd = {}

        parser.add_section('gameserver')
        parser.add_section('steamcmd')
        # -----------------------------------------
        # Base configuration options here.
        # -----------------------------------------

        while True:
            user_input = raw_input("Steam AppID: ")
            if user_input and user_input.isdigit():
                gameserver['appid'] = user_input
                break
            print "No AppID Given. Please supply an AppID"

        parser.set('gameserver', 'appid', gameserver['appid'])

        while True:
            user_input = raw_input("Gameserver Install Path (with trailing slash): ")
            if user_input and os.path.isdir(user_input):
                gameserver['path'] = user_input
                break
            print "Directory is empty or does not exist. Try creating directory: {}".format(user_input)

        parser.set('gameserver', 'path', gameserver['path'])

        while True:
            user_input = raw_input("Gameserver name IE: csgo: ")
            if user_input:
                gameserver['name'] = user_input
                break
            print "No input or invalid input given. Please try again."

        parser.set('gameserver', 'name', gameserver['name'])

        while True:
            user_input = raw_input("Steam login: [anonymous] ")
            if user_input:
                steamcmd['user'] = user_input
                break
            steamcmd['user'] = "anonymous"
            break

        parser.set('steamcmd', 'user', steamcmd['user'])

        while True:
            user_input = raw_input("Steam password: [anonymous] ")
            if user_input:
                steamcmd['password'] = user_input
                break
            steamcmd['password'] = "anonymous"
            break

        parser.set('steamcmd', 'password', steamcmd['password'])

        while True:
            user_input = raw_input("Gameserver Daemon: [srcds_run] ")
            if user_input:
                gameserver['daemon'] = user_input
                break
            gameserver['daemon'] = "srcds_run"
            break

        parser.set('gameserver', 'daemon', gameserver['daemon'])

        while True:
            user_input = raw_input("Gameserver Hostname: [My Gameserver] ")
            if user_input:
                gameserver['hostname'] = user_input
                break
            gameserver['hostname'] = "My Gameserver"
            break

        parser.set('gameserver', 'hostname', gameserver['hostname'])

        while True:
            user_input = raw_input("Gameserver IP: [0.0.0.0] ")
            if user_input:
                gameserver['ip'] = user_input
                break
            gameserver['ip'] = '0.0.0.0'
            break

        parser.set('gameserver', 'ip', gameserver['ip'])

        while True:
            user_input = raw_input("Gameserver Port: [27015] ")
            if user_input:
                gameserver['port'] = user_input
                break
            gameserver['port'] = '27015'
            break

        parser.set('gameserver', 'port', gameserver['port'])

        while True:
            user_input = raw_input("Gameserver Runscript: [runscript.txt] ")
            if user_input:
                gameserver['runscript'] = user_input
                break
            gameserver['runscript'] = 'runscript.txt'
            break

        parser.set('gameserver', 'runscript', gameserver['runscript'])

        while True:
            user_input = raw_input("Gameserver Tickrate: [60] ")
            if user_input:
                gameserver['tickrate'] = user_input
                break
            gameserver['tickrate'] = '60'
            break

        parser.set('gameserver', 'tickrate', gameserver['tickrate'])

        while True:
            user_input = raw_input("Gameserver Max Players: [16] ")
            if user_input:
                gameserver['maxplayers'] = user_input
                break
            gameserver['maxplayers'] = '16'
            break

        parser.set('gameserver', 'maxplayers', gameserver['maxplayers'])

        while True:
            user_input = raw_input("Gameserver starting map: ")
            if user_input:
                gameserver['map'] = user_input
                break
            print "No map specified. Please put a map here."

        parser.set('gameserver', 'map', gameserver['map'])

        while True:
            user_input = raw_input("Gameserver rcon/admin password: ")
            if user_input:
                gameserver['rcon'] = user_input
                break
            print "Please enter a rcon or admin password."

        parser.set('gameserver', 'rcon', gameserver['rcon'])

        while True:
            user_input = raw_input("Server region: [0] ")
            if user_input:
                gameserver['region'] = user_input
                break
            gameserver['region'] = '0'
            break

        parser.set('gameserver', 'region', gameserver['region'])

        while True:
            user_input = raw_input("Steamgroup ID: [null] ")
            if user_input:
                gameserver['steamgroup'] = user_input
                break
            gameserver['steamgroup'] = "False"
            break

        parser.set('gameserver', 'steamgroup', gameserver['steamgroup'])

        while True:
            user_input = raw_input("LAN Server (sv_lan): [0] ")
            if user_input:
                gameserver['lan'] = user_input
                break
            gameserver['lan'] = "0"
            break

        parser.set('gameserver', 'lan', gameserver['lan'])

        while True:
            user_input = raw_input("sv_alltalk: [0] ")
            if user_input:
                gameserver['alltalk'] = user_input
                break
            gameserver['alltalk'] = "0"
            break

        parser.set('gameserver', 'alltalk', gameserver['alltalk'])

        while True:
            user_input = raw_input("sv_voiceenable: [1] ")
            if user_input:
                gameserver['voiceenable'] = user_input
                break
            gameserver['voiceenable'] = "1"
            break

        parser.set('gameserver', 'voiceenable', gameserver['voiceenable'])

        while True:
            user_input = raw_input("sv_pure: [1] ")
            if user_input:
                gameserver['pure'] = user_input
                break
            gameserver['pure'] = "1"
            break

        parser.set('gameserver', 'pure', gameserver['pure'])

        while True:
            user_input = raw_input("sv_consistency: [1] ")
            if user_input:
                gameserver['consistency'] = user_input
                break
            gameserver['consistency'] = "1"
            break

        parser.set('gameserver', 'consistency', gameserver['consistency'])

        while True:
            user_input = raw_input("sv_password: [none] ")
            if user_input:
                gameserver['password'] = user_input
                break
            gameserver['password'] = ""
            break

        parser.set('gameserver', 'password', gameserver['password'])


        while True:
            user_input = raw_input("sv_rcon_banpenalty: [15] ")
            if user_input:
                gameserver['rcon_banpenalty'] = user_input
                break
            gameserver['rcon_banpenalty'] = "15"
            break

        parser.set('gameserver', 'rcon_banpenalty', gameserver['rcon_banpenalty'])

        while True:
            user_input = raw_input("sv_rcon_minfailures: [5] ")
            if user_input:
                gameserver['rcon_minfailures'] = user_input
                break
            gameserver['rcon_minfailures'] = "5"
            break

        parser.set('gameserver', 'rcon_minfailures', gameserver['rcon_minfailures'])

        while True:
            user_input = raw_input("sv_rcon_maxfailures: [10] ")
            if user_input:
                gameserver['rcon_maxfailures'] = user_input
                break
            gameserver['rcon_maxfailures'] = "10"
            break

        parser.set('gameserver', 'rcon_maxfailures', gameserver['rcon_maxfailures'])

        while True:
            user_input = raw_input("sv_rcon_maxfailuretime: [30] ")
            if user_input:
                gameserver['rcon_maxfailuretime'] = user_input
                break
            gameserver['rcon_maxfailuretime'] = "30"
            break

        parser.set('gameserver', 'rcon_maxfailuretime', gameserver['rcon_maxfailuretime'])

        while True:
            user_input = raw_input("sv_rcon_maxpacketsize: [1024] ")
            if user_input:
                gameserver['rcon_maxpacketsize'] = user_input
                break
            gameserver['rcon_maxpacketsize'] = "1024"
            break

        parser.set('gameserver', 'rcon_maxpacketsize', gameserver['rcon_maxpacketsize'])

        while True:
            user_input = raw_input("sv_rcon_maxpacketbans: [1] ")
            if user_input:
                gameserver['rcon_maxpacketbans'] = user_input
                break
            gameserver['rcon_maxpacketbans'] = "1"
            break

        parser.set('gameserver', 'rcon_maxpacketbans', gameserver['rcon_maxpacketbans'])

        while True:
            user_input = raw_input("log : [on] ")
            if user_input:
                gameserver['log'] = user_input
                break
            gameserver['log'] = "on"
            break

        parser.set('gameserver', 'log', gameserver['log'])

        while True:
            user_input = raw_input("sv_logbans : [1] ")
            if user_input:
                gameserver['logbans'] = user_input
                break
            gameserver['logbans'] = "1"
            break

        parser.set('gameserver', 'logbans', gameserver['logbans'])

        while True:
            user_input = raw_input("sv_logecho : [1] ")
            if user_input:
                gameserver['logecho'] = user_input
                break
            gameserver['logecho'] = "1"
            break

        parser.set('gameserver', 'logecho', gameserver['logecho'])

        while True:
            user_input = raw_input("sv_logfile : [1] ")
            if user_input:
                gameserver['logfile'] = user_input
                break
            gameserver['logfile'] = "on"
            break

        parser.set('gameserver', 'logfile', gameserver['logfile'])

        while True:
            user_input = raw_input("sv_log_onefile : [0] ")
            if user_input:
                gameserver['log_onefile'] = user_input
                break
            gameserver['log_onefile'] = "0"
            break

        parser.set('gameserver', 'log_onefile', gameserver['log_onefile'])

        while True:
            user_input = raw_input("net_maxfilesize: [64] ")
            if user_input:
                gameserver['net_maxfilesize'] = user_input
                break
            gameserver['net_maxfilesize'] = "64"
            break

        parser.set('gameserver', 'net_maxfilesize', gameserver['net_maxfilesize'])

        while True:
            user_input = raw_input("sv_downloadurl: [] ")
            if user_input:
                gameserver['downloadurl'] = user_input
                break
            gameserver['downloadurl'] = ""
            break

        parser.set('gameserver', 'downloadurl', gameserver['downloadurl'])

        while True:
            user_input = raw_input("sv_allowdownload: [1] ")
            if user_input:
                gameserver['allowdownload'] = user_input
                break
            gameserver['allowdownload'] = "1"
            break

        parser.set('gameserver', 'allowdownload', gameserver['allowdownload'])

        while True:
            user_input = raw_input("sv_allowupload: [1] ")
            if user_input:
                gameserver['allowupload'] = user_input
                break
            gameserver['allowupload'] = "1"
            break

        parser.set('gameserver', 'allowupload', gameserver['allowupload'])

        while True:
            user_input = raw_input("sv_pure_kick_clients: [0] ")
            if user_input:
                gameserver['pure_kick_clients'] = user_input
                break
            gameserver['pure_kick_clients'] = "0"
            break

        parser.set('gameserver', 'pure_kick_clients', gameserver['pure_kick_clients'])

        while True:
            user_input = raw_input("sv_pure_trace: [0] ")
            if user_input:
                gameserver['pure_trace'] = user_input
                break
            gameserver['pure_trace'] = "0"
            break

        parser.set('gameserver', 'pure_trace', gameserver['pure_trace'])

        while True:
            user_input = raw_input("MOTD URL: []")
            if user_input:
                gameserver['motd'] = user_input
                break
            gameserver['motd'] = ""
            break

        parser.set('gameserver', 'motd', gameserver['motd'])
        
        # ----------------------
        # CSGO Specific options
        # ----------------------

        if gameserver['name'] == 'csgo':
            #stuff for csgo things here
            print "Gameserver configuration options for CSGO"
            csgo = {}
            parser.add_section('csgo')

            while True:
                print "Configuration types: esl | custom"
                user_input = raw_input("Please select a configuration type: ")
                if user_input == "esl" or user_input == "custom":
                    csgo['template'] = user_input
                    break
                print "Please type an option"

            parser.set('csgo', 'template', csgo['template'])

            if csgo['template'] == "custom":

                while True:
                    user_input = raw_input("Gamemode: casual , competitive , armsrace , demolition , deathmatch , none : ")
                    if user_input == 'casual' or user_input == 'competitive' or user_input == 'armsrace' or user_input == 'demolition' or user_input == 'deathmatch' or user_input == 'none':
                        csgo['gamemode'] = user_input
                        break
                    print "Please select a gametype: casual, competitive , armsrace , demolition , deathmatch , none"

                parser.set('csgo', 'gamemode', csgo['gamemode'])

                while True:
                    user_input = raw_input("Mapgroup: mg_op_op06 , mg_op_op05 , mg_op_breakout , mg_active , mg_reserves , mg_armsrace , mg_demolition , none : ")
                    if user_input == 'mg_op_op06' or user_input == 'mg_op_op05' or user_input == 'mg_op_breakout' or user_input == 'mg_active' or user_input == 'mg_reserves' or user_input == 'mg_armsrace' or user_input == 'mg_demolition' or user_input == 'none':
                        csgo['mapgroup'] = user_input
                        break
                    print "Please select a mapgroup: mg_op_op06 , mg_op_op05 , mg_op_breakout , mg_active , mg_reserves , mg_armsrace , mg_demolition , none : "

                parser.set('csgo', 'mapgroup', csgo['mapgroup'])

                while True:
                    user_input = raw_input("sv_deadtalk: [0]")
                    if user_input:
                        csgo['deadtalk'] = user_input
                        break
                    csgo['deadtalk'] = "0"
                    break

                parser.set('csgo', 'deadtalk', csgo['deadtalk'])

                while True:
                    user_input = raw_input("sv_full_alltalk: [0] ")
                    if user_input:
                        csgo['full_alltalk'] = user_input
                        break
                    csgo['full_alltalk'] = "0"
                    break

                parser.set('csgo', 'full_alltalk', csgo['full_alltalk'])

                while True:
                    user_input = raw_input("sv_pausable: [0] ")
                    if user_input:
                        csgo['pausable'] = user_input
                        break
                    csgo['pausable'] = "0"
                    break

                parser.set('csgo', 'pausable', csgo['pausable'])

                while True:
                    user_input = raw_input("mp_limitteams: [1] ")
                    if user_input:
                        csgo['limitteams'] = user_input
                        break
                    csgo['limitteams'] = "1"
                    break

                parser.set('csgo', 'limitteams', csgo['limitteams'])

                while True:
                    user_input = raw_input("mp_friendlyfire: [0] ")
                    if user_input:
                        csgo['friendlyfire'] = user_input
                        break
                    csgo['friendlyfire'] = "0"
                    break

                parser.set('csgo', 'friendlyfire', csgo['friendlyfire'])

                while True:
                    user_input = raw_input("mp_autoteambalance: [1] ")
                    if user_input:
                        csgo['teambalance'] = user_input
                        break
                    csgo['teambalance'] = "1"
                    break

                parser.set('csgo', 'teambalance', csgo['teambalance'])

                while True:
                    user_input = raw_input("mp_autokick: [1] ")
                    if user_input:
                        csgo['autokick'] = user_input
                        break
                    csgo['autokick'] = "1"
                    break

                parser.set('csgo', 'autokick', csgo['autokick'])

                while True:
                    user_input = raw_input("mp_tkpunish: [1] ")
                    if user_input:
                        csgo['tkpunish'] = user_input
                        break
                    csgo['tkpunish'] = "1"
                    break

                parser.set('csgo', 'tkpunish', csgo['tkpunish'])

                while True:
                    user_input = raw_input("mp_freezetime: [6] ")
                    if user_input:
                        csgo['freezetime'] = user_input
                        break
                    csgo['freezetime'] = "6"
                    break

                parser.set('csgo', 'freezetime', csgo['freezetime'])

                while True:
                    user_input = raw_input("mp_maxrounds: [0] ")
                    if user_input:
                        csgo['maxrounds'] = user_input
                        break
                    csgo['maxrounds'] = "0"
                    break

                parser.set('csgo', 'maxrounds', csgo['maxrounds'])

                while True:
                    user_input = raw_input("mp_roundtime: [5] ")
                    if user_input:
                        csgo['roundtime'] = user_input
                        break
                    csgo['roundtime'] = "5"
                    break

                parser.set('csgo', 'roundtime', csgo['roundtime'])

                while True:
                    user_input = raw_input("mp_timelimit: [5] ")
                    if user_input:
                        csgo['timelimit'] = user_input
                        break
                    csgo['timelimit'] = "5"
                    break

                parser.set('csgo', 'timelimit', csgo['timelimit'])

                while True:
                    user_input = raw_input("mp_buytime: [90] ")
                    if user_input:
                        csgo['buytime'] = user_input
                        break
                    csgo['buytime'] = "90"
                    break

                parser.set('csgo', 'buytime', csgo['buytime'])

                while True:
                    user_input = raw_input("mp_do_warmup_period: [1] ")
                    if user_input:
                        csgo['warmup_period'] = user_input
                        break
                    csgo['warmup_period'] = "1"
                    break

                parser.set('csgo', 'warmup_period', csgo['warmup_period'])
        # ------------------------------
        # Black Mesa config options
        # ------------------------------

        if gameserver['name'] == 'bms':
            # Set black mesa source configs here.
            bms = {}
            parser.add_section('bms')

            #Start while statements here...
            while True:
                user_input = raw_input("mp_teamplay: [0] ")
                if user_input:
                    bms['teamplay'] = user_input
                    break
                bms['teamplay'] = "0"
                break

            parser.set('bms', 'teamplay', bms['teamplay'])

            while True:
                user_input = raw_input("mp_timelimit: [900] ")
                if user_input:
                    bms['timelimit'] = user_input
                    break
                bms['timelimit'] = "900"
                break

            parser.set('bms', 'timelimit', bms['timelimit'])

            while True:
                user_input = raw_input("mp_warmup_time: [30] ")
                if user_input:
                    bms['warmup_time'] = user_input
                    break
                bms['warmup_time'] = "30"
                break

            parser.set('bms', 'warmup_time', bms['warmup_time'])

            while True:
                user_input = raw_input("mp_fraglimit: [50] ")
                if user_input:
                    bms['fraglimit'] = user_input
                    break
                bms['fraglimit'] = "50"
                break

            parser.set('bms', 'fraglimit', bms['fraglimit'])
        
        # ------------------------------
        # Team Fortress 2 config options
        # ------------------------------

        # Extra_parameters is special. This is a hacky way of doing it, but let's do it.
        if not gameserver['name'] == 'tf':
            gameserver['extra_parameters'] = ""
            parser.set('gameserver', 'extra_parameters', gameserver['extra_parameters'])
        
        if gameserver['name'] == 'tf':
            # Set Team Fortress 2 configs here
            tf = {}
            parser.add_section('tf')

            #Start while statements here...
            while True:
                user_input = raw_input("Mann Versus Machine: [0] ")
                if user_input:
                    gameserver['extra_parameters'] = "+tf_mm_servermode 2"
                    mvm_enable = True
                    break
                gameserver['extra_parameters'] = ""
                mvm_enable = False
                break

            parser.set('gameserver', 'extra_parameters', gameserver['extra_parameters'])

            if mvm_enable is False:
                while True:
                    user_input = raw_input("mp_timelimit: [40] ")
                    if user_input:
                        tf['timelimit'] = user_input
                        break
                    tf['timelimit'] = "40"
                    break

                parser.set('tf', 'timelimit', tf['timelimit'])

                while True:
                    user_input = raw_input("tf_overtime_nag: [0] ")
                    if user_input:
                        tf['overtime_nag'] = user_input
                        break
                    tf['overtime_nag'] = "0"
                    break

                parser.set('tf', 'overtime_nag', tf['overtime_nag'])

                if not mvm_enable:
                    while True:
                        user_input = raw_input("tf_mm_servermode: [1] ")
                        if user_input:
                            tf['mm_servermode'] = user_input
                            break
                        tf['mm_servermode'] = "1"
                        break
                    parser.set('tf', 'mm_servermode', tf['mm_servermode'])

            # Since this is set after the server is running, just give it a blank value for configuration later
            parser.set('tf', 'tf_server_identity_account_id', "")
            parser.set('tf', 'tf_server_identity_token', "")

        # ------------------------------
        # Half-Life Deathmatch options
        # ------------------------------

        if gameserver['name'] == 'hl2mp':
            # Set HL2MP configs here.
            hl2mp = {}
            parser.add_section('hl2mp')

            #Start while statements here...

            #mp_fraglimit 100
            #mp_timelimit 20
            #mp_teamplay 0
            while True:
                user_input = raw_input("mp_fraglimit: [50] ")
                if user_input:
                    hl2mp['fraglimit'] = user_input
                    break
                hl2mp['fraglimit'] = "50"
                break

            parser.set('hl2mp', 'fraglimit', hl2mp['fraglimit'])

            while True:
                user_input = raw_input("mp_timelimit: [30] ")
                if user_input:
                    hl2mp['timelimit'] = user_input
                    break
                hl2mp['timelimit'] = "30"
                break

            parser.set('hl2mp', 'timelimit', hl2mp['fraglimit'])

            while True:
                user_input = raw_input("mp_teamplay: [0] ")
                if user_input:
                    hl2mp['teamplay'] = user_input
                    break
                hl2mp['teamplay'] = "0"
                break

            parser.set('hl2mp', 'teamplay', hl2mp['teamplay'])

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

    def create_runscript():
        pass

    def create_servercfg():
        pass

    def create_motd():
        pass

    def steamcmd_update():
        pass

    def srcds_launch():
        pass

