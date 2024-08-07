
import os
import aiohttp
import discord
import simpleaudio
from pydub import AudioSegment

def filetowav(ofn):
    wfn = ofn.replace(ofn.split(".")[-1],'wav') # take the extension and change it
    x = AudioSegment.from_file(ofn)
    x.export(wfn, format='wav') 
    

async def play(client, message: discord.Message, args: str, send):
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
