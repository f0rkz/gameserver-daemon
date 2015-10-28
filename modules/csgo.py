class CSGOServer(GameServer):
    def __init__(self):
        # Bring the gsconfig and path variables over
        super(GameServer, self).__init__()

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

    def status(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass
