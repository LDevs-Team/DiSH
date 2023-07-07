# DiSH
[![Build](https://github.com/LDevs-Team/DiSH/actions/workflows/main.yml/badge.svg)](https://github.com/LDevs-Team/DiSH/actions/workflows/main.yml)

> **Warning**  
> Using this software gives no guarantees. If you want stability, use stable confirmed releases (latest is 11.0)
> Turns out I can't bother to update the install instructiosn for now, refer to DiSHLoader code to install.

## DISCLAIMER
DISCLAMER: We started this project only for good purposes - this program is NOT INTENDED FOR MALICIOUS USE. We are not responsable for what people use this software for.

## License

You can obtain a copy of the License [here](LICENSE)

## Usage [outdated, refer to DiSHLoader - WIP)
The easiest way to get started is downloading the zipped archive directly from the [Releases page](https://github.com/LDevs-Team/DiSH/releases/latest)

If you want to use a nightly version, go to the actions tab (you have to be signed in), choose the commit and download the artifact according to your OS

1. Firstly, download the DiSH-{OS}.zip file according to the OS you have (In this case Windows)
2. Unzip the archive, you will find a DiSH zipped folder, extract it.
3. Create a file named `.env`.
4. Create a Discord bot and copy its token.
5. Enable ALL INTENTS in the Discord bot developer portal
6. Create a new discord server or use one you already have
7. Invite there your new bot
8. Create:
- A category
- A channel for the logs
- A channel for global commands
9. In your .env file, put the following:
```env
TOKEN=(your discord bot token)
GUILD_ID=(your discord server ID)
CATEGORY_ID=(your category ID)
LOGS_ID=(your logs channel ID)
GLOBAL_ID=(your global channel ID)
```
10. Start the DiSH executable. If nothing went wrong, you should see a message in your logs channel saying "Bot started successfully on (YOUR PC NAME) as (CURRENT USER)"
11. YOu should be able to use windows command line from the newly created channel or global channel. Type help to get a list of custom commands

## Compatibility
DiSH works on Windows 8.1 and above
<br>Windows Server is not officially supported but you can get DiSH to work by adding certificates.

Python works from 3.9+ officially, 3.8 currently is not tested

## Installation
If you are on windows, you can install DiSH using the installer (setup-shell-startup.bat, setup-registry.bat or setup-task-scheduler.bat)
<br>If you use linux, I recommend starting with systemd at boot the dish executable

MacOS is now supported but untested (also Linux untested)

## Building from source
To build from source, you will need: 
- python
- pip
- git

In a terminal do 
``` bat
git clone [ REPO URL in this case https://github.com/Baracchino-Della-Scuola/DiSH ]
cd (repo name, in this case DiSH)
pip install -r requirements.txt
```
if you want to buil dthe executable, do `python build.py`<br>
if you want to just start it, do `python main.py`. Note that for the bot to start, you will need a .env file (refer to Usage for how to create one)

## Contributing
This program follow the conventional commit standard and, when you open a PR, you should follow the conventional commit standard to avoid you PR not being merged. All PR's should be squashed and merged to keep the commit history clean

