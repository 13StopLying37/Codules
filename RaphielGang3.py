import asyncio
import time
from random import randint
from userbot.events import register
@register(outgoing=True, pattern='^.ghoul(?: |$)(.*)')
async def typewriter(typew):
	a = 1000
	while a > 0:
	    await typew.edit(f'{a} - 7 = {a - 7}')
	    a-=7
	time.sleep(1)
	await typew.edit('Я гуль.')
#Сделано арсеном.
