class ARKServer(GameServer):
    def __init__(self):
        # Bring the gsconfig and path variables over
        super(GameServer, self).__init__()

    def configure(self):
        config_options = [
            {'option': 'ServerPassword', 'info': 'Private Server Password: [none]', 'default': 'ignore'},
            {'option': 'ServerAdminPassword', 'info': 'Admin Password [reset_me]', 'default': 'reset_me'},
        ]
        return config_options

    def status(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass
