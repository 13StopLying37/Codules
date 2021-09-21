from telethon import events, functions, types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import Channel
from aiogram import Bot

from .. import loader, utils
from random import choice
from bs4 import BeautifulSoup as bs4
from string import ascii_lowercase
from requests import get



class KickLastMod(loader.Module):
    """Удаляет из чата последних Х зашедших"""

    strings = {'name': 'KickLast'}


    async def masskicklastcmd(self, message):
        """.masskicklst <колличество> <юзернем, если канал>"""
        await kick(message, True)
    async def kicklastcmd(self, message):
        """.kicklst <колличество> <юзернем, если канал>"""
        await kick(message, False)

    
async def kick(message, bot=False):
    args = utils.get_args(message)
    if not args:
        return await message.edit("Сколько нужно кикнуть?\n0 если всех зашедших за 42 часа")
    limit = int(args[0])
    limit = limit or 99999
    group = args[-1] if len(args) > 1 else message.chat.id
    try: group = await message.client.get_entity(group)
    except:  await message.edit("Такого чата не существует")
    if not isinstance(group, Channel):
        return await message.edit("Такого чата не существует")
    if bot:
        botfather = 93372553
        bantoolbot = "".join([choice(list(ascii_lowercase)) for _ in range(29)])+"bot"
        async with message.client.conversation(botfather) as conv:
            await (await message.client.send_message(botfather, "/newbot")).delete()
            newbot = await conv.wait_event(events.NewMessage(incoming=True, from_users=botfather))
            await newbot.delete()
            if "Sorry" in newbot.text:
                return await message.edit("Создание бота недоступно.\nПовтори попытку через"+newbot.text[45:])
            await (await message.client.send_message(botfather, "BanTool")).delete()
            await (await conv.wait_event(events.NewMessage(incoming=True, from_users=botfather))).delete()
            await (await message.client.send_message(botfather, bantoolbot)).delete()
            html = await conv.wait_event(events.NewMessage(incoming=True, from_users=botfather))
            await html.delete()
            soup = bs4(html.text, "html.parser")
            token = soup.findAll("code")[0].text
        await message.client(InviteToChannelRequest(group, [bantoolbot]))
        await message.client(functions.channels.EditAdminRequest(
            channel=group,
            user_id=bantoolbot,
            admin_rights=types.ChatAdminRights(ban_users=True), rank='BanToolBot'))
            
    banlist = [x.user_id async for x in message.client.iter_admin_log(group, join=True, limit=limit)]
    if len(banlist) == 0:
        return await message.edit("Не могу обнаружить зашедших...")
    await message.reply(str(banlist))
    for banid in banlist:
        if bot:
            await Bot(token).kick_chat_member(f"-100{group}", banid)
        else:
            await message.client.kick_participant(group, banid)
    if bot:
        await message.client.kick_participant(group, bantoolbot)
        async with message.client.conversation(botfather) as conv:
            await message.client.send_message(botfather, "/deletebot")
            await conv.wait_event(events.NewMessage(incoming=True, from_users=botfather))
            await message.client.send_message(botfather, "@"+bantoolbot)
            await conv.wait_event(events.NewMessage(incoming=True, from_users=botfather))
            await message.client.send_message(botfather, "Yes, I am totally sure.")
    return await message.edit("Успех.")
