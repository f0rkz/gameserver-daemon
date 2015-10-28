class Unreal(GameServer):
    def __init__(self):
        # Bring the gsconfig and path variables over
        super(GameServer, self).__init__()

    def configure(self):
        config_options = [
            {'option': 'ip', 'info': 'Gameserver IP: [0.0.0.0] ', 'default': '0.0.0.0'},
            {'option': 'hostname', 'info': 'Gameserver Hostname: [My Gameserver] ', 'default': 'My Gameserver'},
        ]
