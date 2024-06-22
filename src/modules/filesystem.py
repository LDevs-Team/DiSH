
import asyncio
import functools
import os
import shutil

import aiohttp
import discord


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
    print(args)
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

