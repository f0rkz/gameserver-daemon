import sys
import os.path
import ConfigParser
import tarfile
import urllib
import subprocess
from screenutils import list_screens, Screen

parser = ConfigParser.SafeConfigParser()

CONFIG_FILE = "server.conf"
STEAMCMD_DOWNLOAD = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"

def steamcmd_update(myappid, mysteamcmdpath, mypath, mylogin, mypassword):
    steamcmd_run = '{steamcmdpath}steamcmd.sh +login {login} {password} +force_install_dir {installdir} +app_update {id} validate +quit'.format(steamcmdpath=mysteamcmdpath, login=mylogin, password=mypassword, installdir=mypath, id=myappid)
    return steamcmd_run

def srcds_launch(mygame, mysteamcmdpath, myrunscript, mymaxplayers, mytickrate, myport, myip, mymap, myrcon):
    srcds_run = '-game {game} -console -usercon -secure -autoupdate -steam_dir {steam_dir} -steamcmd_script {runscript} -maxplayers {maxplayers} -tickrate {tickrate} +port {port} +ip {ip} +map {map} +rcon_password {rcon}'.format(game=mygame, steam_dir=mysteamcmdpath, runscript=myrunscript, maxplayers=mymaxplayers, tickrate=mytickrate, port=myport, ip=myip, map=mymap, rcon=myrcon)
    return srcds_run

if os.path.isfile(CONFIG_FILE):
    #load configuration objects here
    parser.read(CONFIG_FILE)

    # Gameserver dict for the gameserver settings
    gameserver = {
        'appid': parser.get("gameserver", "appid"),
        'path': parser.get("gameserver", "path"),
        'name': parser.get("gameserver", "name"),
        'ip': parser.get("gameserver", "ip"),
        'port': parser.get("gameserver", "port"),
        'hostname': parser.get("gameserver", "hostname"),
        'daemon': parser.get("gameserver", "daemon"),
        'tickrate': parser.get("gameserver", "tickrate"),
        'maxplayers': parser.get("gameserver", "maxplayers"),
        'runscript': parser.get("gameserver", "runscript"),
        'map': parser.get("gameserver", "map"),
        'rcon': parser.get("gameserver", "rcon")
        }

    # Steamcmd dict for the steamcmd settings
    steamcmd = {
        'user': parser.get("steamcmd", "user"),
        'password': parser.get("steamcmd", "password")
    }

else:
    #Prompt for configuration information
    print "A configuration file was not found. Doing a first run."

    # Initialize dicts and configuration files.
    gameserver = {}
    steamcmd = {}

    parser.add_section('gameserver')
    parser.add_section('steamcmd')

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
        if user_input and user_input.isalpha():
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

    # Write the configuration file
    parser.write(open(CONFIG_FILE, 'w'))
    print "Configuration file saved as {}".format(CONFIG_FILE)

    # Create the runscript file
    if os.path.exists(os.path.join(gameserver['path'],gameserver['runscript'])) is False:
        f = open(os.path.join(gameserver['path'],gameserver['runscript']), 'w')
        f.write("login {steamlogin} {steampassword}\n".format(steamlogin=steamcmd['user'], steampassword=steamcmd['password']))
        f.write("force_install_dir {}\n".format(os.path.join(gameserver['path'], gameserver['name'])))
        f.write("app_update {} validate\n".format(gameserver['appid']))
        f.write("quit\n")
        f.close()

# Now that our configuration is out of the way, let's move on to installing and updating gameserver files

# Check to see if the gameserver has an active screen
s = Screen(gameserver['name'])
is_server_running = s.exists

if is_server_running == True:
    # The game is running.
    if len(sys.argv):

        if str.lower(sys.argv[1]) == "stop":
            print "Stop command sent"
            # Kill the screen here.
            s = Screen(gameserver['name'])
            s.kill()
            print "Gameserver killed"
            exit()
            
        elif str.lower(sys.argv[1]) == "restart":
            print "Restart command sent"
            #Kill the screen here.
            s = Screen(gameserver['name'])
            s.kill()
            print "Gameserver killed"

        elif str.lower(sys.argv[1]) == "update":
            print "Stopping server for update"
            # Kill the screen here.
            s = Screen(gameserver['name'])
            s.kill()
            print "Gameserver stopped. Moving on to update process."
    else:
        sys.exit("The gameserver is currently running. It is required that you run this script with the stop command before proceeding.")

else:
    print "Gameserver is not running, proceeding to update and start."

# Check if steamcmd is installed, if not, run it.
INSTALL_DIR = os.path.dirname(gameserver['path'])
if os.path.isfile(os.path.join(INSTALL_DIR, 'steamcmd.sh')):
    #Steamcmd is installed in the install path
    print "steamcmd is installed. Updating gameserver files. This may take a while..."
    subprocess.call(steamcmd_update(gameserver['appid'], gameserver['path'], os.path.join(gameserver['path'], gameserver['name']), steamcmd['user'], steamcmd['password']), shell=True)

else:
    #Download steamcmd and extract it
    urllib.urlretrieve(STEAMCMD_DOWNLOAD, os.path.join(gameserver['path'], 'steamcmd_linux.tar.gz'))
    steamcmd_tar = tarfile.open(os.path.join(gameserver['path'], 'steamcmd_linux.tar.gz'), 'r:gz')
    steamcmd_tar.extractall(gameserver['path'])
    print "Steamcmd installed. Starting first run. Downloading gamefiles. This may take a while..."
    subprocess.call(steamcmd_update(gameserver['appid'], gameserver['path'], os.path.join(gameserver['path'], gameserver['name']), steamcmd['user'], steamcmd['password']), shell=True)

print "All done installing/updating gameserver files. Launching the server."

# LAUNCH THE SERVER! \m/

if gameserver['daemon'] == "srcds_run":
    # Gameserver is srcds based. Form up a start command
    launch = srcds_launch(gameserver['name'], gameserver['path'], gameserver['runscript'], gameserver['maxplayers'], gameserver['tickrate'], gameserver['port'], gameserver['ip'], gameserver['map'], gameserver['rcon'])
    srcds_run = '{path}/srcds_run {launch_parameters}'.format(path=os.path.join(INSTALL_DIR, gameserver['name']), launch_parameters=launch)
    print srcds_run

    # Load up the screen
    s = Screen(gameserver['name'], True)
    #s.send_commands('bash')
    s.send_commands(srcds_run)

    print 'Server started. To monitor, attach {} screen'.format(gameserver['name'])