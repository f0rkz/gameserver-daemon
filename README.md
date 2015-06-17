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

## --update or -u
Assuming you already configured your server, the `-u` or `--update` argument will run a steamcmd update. You can add `--validate` to use the validate option while updating your gameserver.

## --validate
See: `--update`