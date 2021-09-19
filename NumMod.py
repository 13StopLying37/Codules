from .. import loader, utils
import asyncio

class NumMod(loader.Module):
	strings={"name": "NumMod"}
	
	async def numcmd(self, message):
		await message.delete()
		reply = await message.get_reply_message()
		a = reply.text
		count_st = 0
		count_hf = 0
		if not a:
			await message.edit('Нет реплая.')
			return
		args = utils.get_args_raw(message)
		list_args=[]
		for i in args.split(' '):
			list_args.append(i)
		if not args:
			await message.edit('Нет аргументов')
			return
		lis = []
		for i in a.splitlines():
			lis.append(i)
		for start in list_args:
			if start.isdigit():
				if not start[:-1] == '.':
					start+='.'
			for x in lis:
				if x.lower().startswith(str(start.lower())):
					count_st = 1
					if 'href="' in x:
						count_hf = 1
						b=x.find('href="')+6
						c=x.find('">')
						link = x[b:c]
						if link.startswith('tg'):
							list = []
							for i in link.split('='):
								list.append(i)
							await message.reply(f'заразить @{list[1]}')
						else:
							await message.reply(f'заразить {link}')
			await asyncio.sleep(3)
				
		if not count_st:
			await message.edit('Не найдено ни одного совпадения в начале строк с аргументами.')
			return
			
		if not count_hf:
			await message.edit('Не найдено ни одной ссылки.')
			return