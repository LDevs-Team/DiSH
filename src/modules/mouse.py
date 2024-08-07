import os
import discord
import pyautogui
import requests


async def loc(client, message: discord.Message, args: str, send):
    if len(message.attachments) == 0:
        return await message.reply("No file specified")
    fileUrl = message.attachments[0].url
    res = requests.get(fileUrl, stream=True)
    with open(message.attachments[0].filename, "wb") as f:
        f.write(res.content)

    try:
        pos = pyautogui.locateOnScreen(message.attachments[0].filename, confidence=0.8)
        if pos == None:
            os.remove(message.attachments[0].filename)
            return await message.reply("Image not found :/")
        pyautogui.click(pos)
        await message.reply("Clicked at " + str(pos))
    except Exception as e:
        print(e)
        await message.reply("No image found :/")
    os.remove(message.attachments[0].filename)

async def click(client, message: discord.Message, args: str, send):
    pos = args.split(" ")
    pyautogui.click(int(pos[0]), int(pos[1]))
    await message.reply("Clicked at " + str(pos))
