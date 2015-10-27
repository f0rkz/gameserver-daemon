class HL2DMServer(GameServer):
    def __init__(self):
        # Bring the gsconfig and path variables over
        super(GameServer, self).__init__()

    def configure(self):
        config_options = [
            {'option': 'fraglimit', 'info': 'mp_fraglimit: [50] ', 'default': '50'},
            {'option': 'timelimit', 'info': 'mp_timelimit: [30] ', 'default': '30'},
            {'option': 'teamplay', 'info': 'mp_teamplay: [0] ', 'default': '0'},
        ]

    def status(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass
