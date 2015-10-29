import ConfigParser
import os.path
import sys
import urllib
import subprocess
import tarfile
from jinja2 import Template
from screenutils import list_screens, Screen

from modules.gameserver import GameServer

parser = ConfigParser.RawConfigParser()
CONFIG_FILE = "server.conf"

# Dictionary of game subdirectories for configuration
# Also used for the game name in srcds launching
GAME = {
    '376030': 'ShooterGame',
}

class ARKServer(GameServer):
    def __init__(self, gsconfig):
        # Bring the gsconfig and path variables over
        super(GameServer, self).__init__()
        self.gsconfig = gsconfig
        self.steam_appid = self.gsconfig['steamcmd']['appid']

    def configure_list(self, group, options):
        """
        Method used to loop through configuration lists and prompt the user
        """
        for config_object in options:
            while True:
                user_input = raw_input(config_object['info'])
                if user_input:
                    if config_object.get('valid_option') and not user_input in config_object['valid_option']:
                        print "Invalid option. Please chose one of the following: {}".format(config_object['valid_option'])
                    else:
                        group[config_object['option']] = user_input
                        break
                if not config_object.get('default', None):
                    #loop back and ask again
                    pass
                else:
                    # Default value set!
                    group[config_object['option']] = config_object['default']
                    break
            parser.set(group['id'], config_object['option'], group[config_object['option']])

    def configure(self):
        config_options = [
            {'option': 'ServerPassword', 'info': 'Private Server Password: [none]', 'default': 'ignore'},
            {'option': 'ServerAdminPassword', 'info': 'Admin Password [reset_me]', 'default': 'reset_me'},
        ]
        parser.read(CONFIG_FILE)
        myid = {'id': self.steam_appid}
        self.configure_list(myid,config_options)
        parser.write(open(CONFIG_FILE, 'w'))
        print "Configuration saved as {}".format(CONFIG_FILE)

    def status(self):
        """
        Method to check the server's status
        """
        steam_appid = self.gsconfig['steamcmd']['appid']
        s = Screen(steam_appid)
        is_server_running = s.exists
        return is_server_running

    def start(self):
        steam_appid = self.gsconfig['steamcmd']['appid']
        if self.gsconfig[steam_appid]['serverpassword'] != 'ignore':
                run_commands = '{gamedir}/ShooterGame/Binaries/Linux/ShooterGameServer ' \
                               'TheIsland?Listen?SessionName={hostname}?ServerPassword={serverpassword}' \
                               '?ServerAdminPassword={serveradminpassowrd}' \
                               .format(gamedir=self.path['gamedir'],
                                       hostname=self.gsconfig[steam_appid]['hostname'],
                                       ServerPassowrd=self.gsconfig[steam_appid]['serverpassword'],
                                       serveradminpassword=self.gsconfig[steam_appid]['serveradminpassword']
                                      )
        else:
            run_commands = '{gamedir}/ShooterGame/Binaries/Linux/ShooterGameServer ' \
                           'TheIsland?Listen?SessionName={hostname}?ServerAdminPassword={serveradminpassowrd}' \
                           .format(gamedir=self.path['gamedir'],
                                   hostname=self.gsconfig[steam_appid]['hostname'],
                                   serveradminpassowrd=self.gsconfig[steam_appid]['serveradminpassword']
                                  )
        s = Screen(steam_appid, True)
        s.send_commands(run_commands)

    def stop(self):
        """
        Method to stop the server.
        """
        # Steam appid
        steam_appid = self.gsconfig['steamcmd']['appid']
        if self.status():
            s = Screen(steam_appid)
            s.kill()
            print "Server stopped."
        else:
           print "Server is not running."
