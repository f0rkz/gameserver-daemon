class SRCDS(GameServer):
    def __init__(self):
        # Bring the gsconfig and path variables over
        super(GameServer, self).__init__()
        steam_appid = self.gsconfig['steamcmd']['appid']
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
