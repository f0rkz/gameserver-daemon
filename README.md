# f0rkz Gameserver Daemon
The issue:

I have to set up large volumes of gameservers for LAN events and the like. This takes time
to interact with steamcmd, get the right information, configure the server, and get the server online.

The solution:

Enter gameserver-daemon.py . An all in one tool to configure gameservers from install to server.cfg and
everything in between.

# Installation
- Step 1: Clone the project

`git clone http://codemonkey.f7lans.com/f0rkz/gameserver-daemon.git`

- Step 2: Install lib32gcc1 (a dependancy required for steamcmd and srcds based servers)

`sudo apt-get install lib32gcc1`

- Step 3: Install the python-pip package

`sudo apt-get install python-pip`

- Step 4: Create the gameserver base directory

`mkdir /home/steam/mygame.hostname.com`

- Step 5: Install the python prerequisites

`sudo pip install -r requirements.txt`

# Running
Running the gameserver-daemon.py script alone will not do anything. Arguments are required to do different
operations in the script.

To view the various arguments gameserver-daemon.py has, run the following:

`python gameserver-daemon.py --help`

## --configure
To configure your gameserver for the first time, you will need to add the `--configure` argument to the script.

`python gameserver-daemon.py --configure`

This will build a ini-like configuration file called `server.conf` in the script's directory.

There are a select group of games currently supported by the script. For the `Gameserver Name` configuration prompt
choose from the following:

- csgo
- tf
- hl2mp
- bms

More games are planned for the future. To properly set your server up, use one of the above (for the game you are planning on running.)

## --steamcmd
Install steamcmd. This is required for proper running. Your server will not start without steamcmd!

## --update or -u
Assuming you already configured your server, the `-u` or `--update` argument will run a steamcmd update. You can add `--validate` to use the validate option while updating your gameserver.

## --validate
See: `--update`

## --runscript
Generate the runscript.txt file used to update the gameserver at launch. Not required, but helpful!

## --servercfg
Generate server.cfg from settings set in `--configure`. This is not required, but it is very helpful for automation.

Important note: running this will overwrite any server.cfg file currently in production. You can run this at initial launch and change/add cvars as needed. Alternatively, you can change the preset cvars in server.conf and run this again.

## --motd
Generate the motd.txt set in `--configure`. This is a URL IE: http://www.mygamingcommunity.com/motd.html

# Example usage
## Initial install

`python gameserver-daemon.py --configure --steamcmd --update --validate`

This will configure the gameserver, install steamcmd, install the gameserver files with the validate option.

## Update the gameserver (without validate), install runscript.txt, install server.cfg, install motd.txt, and start the server

`python gameserver-daemon.py --update --runscript --servercfg --motd --start`

## Restart the gameserver

`python gameserver-daemon.py --restart`

Alternative method

`python gameserver-daemon.py --stop --start`

# Modding

Feel free to modify the script at your free will. If you see a cvar that is not supported adding is quite easy.

The following areas will need to be modified:

GameServer.py line 26 has documentation on adding additional cvars:

"""
Configuration dictionaries template:
thing [
    {'option': '', 'info': '', 'default': ''},
]

If you want to force a user to enter a value:
thing [
    {'option': '', 'info': ''},
]

If you need to validate based on a list of options:
thing [
    {'option': '', 'info': '', 'valid_option': ['option1', 'option2', 'option3']},
]
"""

The next place is adding the cvar in the template file. Pretty easy to figure out if you take a look at it.

If you run the --configure line, you should see your new cvar.

# Questions?

Email me (f0rkz@f0rkznet.net) or create a new issue. I use this script heavily for my gameservers so any problems or extensibilites are gladly accepted!
