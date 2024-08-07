
from io import BytesIO
import traceback
import webbrowser

import discord
import pyperclip


async def browser(client, message: discord.Message, args: str, send):
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

async def dish_help(client, message: discord.Message, args: str, send):
    modules = client.modules.values()
    print(modules)
    docs = []
    print(iter(modules))
    for a in modules:
        try:
            docs.append(str(a.__name__ + " : "+ str(a.__doc__)))
        except:
            traceback.print_exc()
    print(docs)
    try:
        
        await send("Available commands:\n"+"\n".join(docs))
    except:
        help_message = "Available commands\n"+"\n".join(docs)
        f = BytesIO(help_message.encode())
        await send(file=discord.File(f, "output.txt"))

async def clipboard(client, message:discord.Message, args:str, send):
    
    await send(pyperclip.paste())