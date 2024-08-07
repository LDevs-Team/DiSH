from io import BytesIO
from PIL import ImageGrab
import discord

async def screenshot(client, message: discord.Message, args: str, send):

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
    await send(file=discord.File(byteio, "screenshot.png"))