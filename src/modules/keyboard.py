

import discord
import pyautogui


async def press(client, message: discord.Message, args: str):
    keys = args.split(" ")
    for a in keys:
        pyautogui.press(a)
    await message.reply(f"Pressed {', '.join(keys)}")


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
