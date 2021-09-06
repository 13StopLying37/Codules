#ClownsFactory
import requests
from .. import loader, utils
import io
import dpath.util as dpu
def register(cb):
    cb(TikTokDownMod())
class TikTokDownMod(loader.Module):
    """ты еблан да?"""
    strings = {'name': 'ТикТок даунлодер'}
    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []
    async def client_ready(self, client, db):
        self._db = db
        self._client = client
    async def tikcmd(self, event):
        args = utils.get_args_raw(event)
        reply = await event.get_reply_message()
        if not args:
            if not reply:
                await event.edit("где ссылка, клоун.")
                return
            else:
                args = reply.raw_text
        await event.edit("делается делается.")
        data = {'url': args}
        try:
            response = requests.post('https://tik.fail/api/geturl', data=data).json()
            tik = requests.get(response['direct'])
            file = io.BytesIO(tik.content)
            file.name = response['direct']
            file.seek(0)
            await event.client.send_file(event.to_id, file)
        except:
            await event.edit("нихуя не вышло, подожди немного и попробуй еще раз")

    async def tikhashcmd(self, event):
        args = utils.get_args_raw(event)
        reply = await event.get_reply_message()
        if not args:
            if not reply:
                await event.edit("где хештег, клоун.")
                return
            else:
                args = reply.raw_text
        data = requests.get('https://tik.fail/api/tiktok/v1/hashtag/' + args).json()
        res = dpu.values(data, "/**/webVideoUrl")
        for i in res:
            await event.respond(f"<a href='{i}'>ссылка на видео с хештегом #{args}</a>")