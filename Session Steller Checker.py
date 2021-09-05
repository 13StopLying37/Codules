from .. import loader, utils
import requests
@loader.tds
class StealCheckerMod(loader.Module):
    """Session Steller Checker: .scheck (reply to file)"""
    strings = {'name': 'Session Steller Checker'}
    async def scheckcmd(self, message):
        reply = await message.get_reply_message()
        check = []
        triggers = ['DeleteAccountRequest', 'StringSession', 'sh1tn3t.ml', 'getattr']
        if reply.file:
            for trigger in triggers:
                for count, _ in enumerate(open(await reply.download_media(), "r").read().split("\n"), start=1):
                    if trigger in _:
                        check.append((count, _))
        elif reply:
            urll = reply.raw_text.split()
            url = ""
            for url in urll:
                if "://" in url:
                    break
            data = requests.get(url).text
            for trigger in triggers:
                for count, _ in enumerate(data.split("\n")):
                    if trigger in _:
                        check.append((count, _))
        s = ''
        if not len(check) == 0:
            for checks in check:
                    s += f"<b>Line num:</b> <code>{checks[0]}</code>\n<b>Scam code:</b> <code>{' '.join(str(checks[1]).split())}</code>\n\n"
            return await message.edit(f"<b>❗️WARNING❗️</b> ❌SCAM MODULE❌\n\n" + s)
        else:
            return await message.edit(f"<b>Module is clear✅</b>")