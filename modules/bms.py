class BMSServer(GameServer):
    def __init__(self):
        # Bring the gsconfig and path variables over
        super(GameServer, self).__init__()

    def configure(self):
        config_options = [
            {'option': 'teamplay', 'info': 'mp_teamplay: [0] ', 'default': '0'},
            {'option': 'timelimit', 'info': 'mp_timelimit: [900] ', 'default': '900'},
            {'option': 'warmup_time', 'info': 'mp_warmup_time: [30] ', 'default': '30'},
            {'option': 'fraglimit', 'info': 'mp_fraglimit: [50] ', 'default': '50'},
        ]

    def status(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass
