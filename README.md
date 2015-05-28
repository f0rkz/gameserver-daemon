# f0rkz Gameserver Daemon
The issue:

I have to set up large volumes of gameservers for LAN events and the like. This takes time 
to interact with steamcmd, get the right information, configure the server, and get the server online.

The solution:

Enter gameserver-daemon.py . An all in one tool to configure gameservers from install to server.cfg and 
everything in between.

# Installation
Step 1: Clone the project

Step 2: Install lib32gcc1 (a dependancy required for steamcmd and srcds based servers)

Step 3: Install the python-pip package

Step 4: Create the gameserver base directory

`mkdir /home/steam/mygame.hostname.com`

Step 5: Install the python prerequisites

`sudo pip install -r requirements.txt`

Step 6: Run the daemon

`python gameserver-daemon.py`

Follow the prompts and enjoy!