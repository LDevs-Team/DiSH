import discord
import pyautogui


async def press(client, message: discord.Message, args: str, send):
    keys = args.split(" ")
    for a in keys:
        pyautogui.press(a)
    await send(f"Pressed {', '.join(keys)}")


async def typewrite(client, message: discord.Message, args: str, send):
    pyautogui.typewrite(args)
    await send(f"Typed {args}")


async def hotkey(client, message: discord.Message, args: str, send):
    keys = args.split(" ")
    for a in keys:
        pyautogui.keyDown(a)
    for a in reversed(keys):
        pyautogui.keyUp(a)
    await send(f"Sent hotkey with commands {', '.join(keys)}")


async def specialKeys(client, message: discord.Message, args: str, send):
    await send("\n".join(pyautogui.KEY_NAMES))
