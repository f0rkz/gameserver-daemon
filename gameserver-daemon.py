import sys
import os.path
import ConfigParser
import tarfile
import urllib
import subprocess
from screenutils import list_screens, Screen

parser = ConfigParser.SafeConfigParser()

config_file = "server.conf"
steamcmd_download = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"

def steamcmd_update(myappid, mysteamcmdpath, mypath, mylogin, mypassword):
	steamcmd_run = '{steamcmdpath}steamcmd.sh +login {login} {password} +force_install_dir {installdir} +app_update {id} validate +quit'.format(steamcmdpath=mysteamcmdpath, login=mylogin, password=mypassword, installdir=mypath, id=myappid)
	return steamcmd_run

def srcds_launch(mygame, mysteamcmdpath, myrunscript, mymaxplayers, mytickrate, myport, myip):
	srcds_run = '-game {game} -console -usercon -secure -autoupdate -steam_dir {steam_dir} -steamcmd_script {runscript} -maxplayers_override {maxplayers} -tickrate {tickrate} +port {port} +ip {ip}'.format()
	return srcds_run

if os.path.isfile(config_file):
	#load configuration objects here
	parser.read(config_file)

	# Parse configuration to variables
	appid = parser.get("gameserver", "appid")
	path = parser.get("gameserver", "path")
	gameserver_name = parser.get("gameserver", "gameserver_name")
	gameserver_ip = parser.get("gameserver", "gameserver_ip")
	gameserver_port = parser.get("gameserver", "gameserver_port")
	hostname = parser.get("gameserver", "hostname")
	gameserver_daemon = parser.get("gameserver", "gameserver_daemon")
	steam_login = parser.get("steamcmd", "login")
	steam_password = parser.get("steamcmd", "password")

else:
	#Prompt for configuration information
	print "A configuration file was not found. Doing a first run."

	appid = raw_input("Steam AppID: ")
	if appid == '':
		sys.exit("No appid given. Please supply an appid.")

	path = raw_input("Gameserver Install Path (with trailing slash): [/home/steam/{}/] ".format(appid))
	if path == '':
		path = '/home/steam/{}/'.format(appid)

	gameserver_name = raw_input("Gameserver name IE: csgo: [{}] ".format(appid))
	if gameserver_name == '':
		gameserver_name = appid

	steam_login = raw_input("Steam login: [anonymous] ")
	if steam_login == '':
		steam_login = "anonymous"

	steam_password = raw_input("Steam password: [anonymous] ")
	if steam_password == '':
		steam_password = "anonymous"

	gameserver_daemon = raw_input("Gameserver Daemon: [srcds_run] ")
	if gameserver_daemon == '':
		gameserver_daemon = "srcds_run"

	hostname = raw_input("Gameserver Hostname: [My Gameserver] ")
	if hostname == '':
		hostname = "My Gameserver"

	gameserver_ip = raw_input("Gameserver IP: [0.0.0.0] ")
	if gameserver_ip == '':
		gameserver_ip = '0.0.0.0'

	gameserver_port = raw_input("Gameserver Port: [27015] ")
	if gameserver_port == '':
		gameserver_port = '27015'
	
	# Generate the configuration file
	parser.add_section('gameserver')
	parser.add_section('steamcmd')
	parser.set('gameserver', 'appid', appid)
	parser.set('gameserver', 'path', path)
	parser.set('gameserver', 'gameserver_name', gameserver_name)
	parser.set('gameserver', 'gameserver_daemon', gameserver_daemon)
	parser.set('gameserver', 'hostname', hostname)
	parser.set('gameserver', 'gameserver_ip', gameserver_ip)
	parser.set('gameserver', 'gameserver_port', gameserver_port)
	parser.set('steamcmd', 'login', steam_login)
	parser.set('steamcmd', 'password', steam_password)

	# Write the configuration file
	parser.write(open(config_file, 'w'))
	print "Configuration file saved as {}".format(config_file)

# Now that our configuration is out of the way, let's move on to installing and updating gameserver files

# Check to see if the gameserver has an active screen
s = Screen(gameserver_name)
is_game_running = s.exists

if is_game_running == True:
	# The game is running.
	print "The gameserver is currently running."
	if str.lower(sys.argv[1]) == "stop":
		print "Stop command sent"
		# Kill the screen here.
		exit()
else:
	print "Gameserver is not running"

# Check if steamcmd is installed, if not, run it.
INSTALL_DIR = os.path.dirname(path)
if os.path.isfile(os.path.join(INSTALL_DIR, 'steamcmd.sh')):
	#Steamcmd is installed in the install path
	print "steamcmd is installed. Updating gameserver files. This may take a while..."
	subprocess.call(steamcmd_update(appid, path, os.path.join(path, gameserver_name), steam_login, steam_password), shell=True)

else:
	#Download steamcmd and extract it
	urllib.urlretrieve(steamcmd_download, path + "steamcmd_linux.tar.gz")
	steamcmd_tar = tarfile.open(path + "steamcmd_linux.tar.gz", 'r:gz')
	steamcmd_tar.extractall(path)
	print "Steamcmd installed. Starting first run. Downloading gamefiles. This may take a while..."
	subprocess.call(steamcmd_update(appid, path, path + gameserver_name , steam_login, steam_password), shell=True)

print "All done installing/updating gameserver files. Launching the server."

if gameserver_daemon == "srcds_run":
	# Gameserver is srcds based. This part is easy.
	exit()

elif gameserver_daemon == "whatever_killing_floor_2_is":
	# Gameserver is killing floor 2. Need to do up a custom command here.
	exit()