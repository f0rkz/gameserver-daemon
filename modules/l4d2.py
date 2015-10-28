class L4D2Server(GameServer):
    def __init__(self):
        # Bring the gsconfig and path variables over
        super(GameServer, self).__init__()

    def configure(self):
        config_options = [
            {'option': 'fork', 'info': 'How many server forks: [0] ', 'default': '0'},
            {'option': 'mp_disable_autokick', 'info': 'mp_disable_autokick: [0] ', 'default': '0'},
            {'option': 'sv_gametypes', 'info': 'sv_gametypes: [coop,realism,survival,versus,teamversus,scavenge,teamscavenge] ', 'default': 'coop,realism,survival,versus,teamversus,scavenge,teamscavenge'},
            {'option': 'mp_gamemode', 'info': 'sv_gamemode: [coop,realism,survival,versus,teamversus,scavenge,teamscavenge] ', 'default': 'coop,realism,survival,versus,teamversus,scavenge,teamscavenge'},
            {'option': 'sv_unlag', 'info': 'sv_unlag: [1] ', 'default': '1'},
            {'option': 'sv_maxunlag', 'info': 'sv_maxunlag: [.5] ', 'default': '.5'},
            {'option': 'sv_steamgroup_exclusive', 'info': 'sv_steamgroup_exclusive: [0] ', 'default': '0'},
        ]

    def status(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass
