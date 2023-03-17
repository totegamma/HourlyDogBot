import asyncio
import json
import os
import websockets
import urllib.request
from misskey import Misskey

TOKEN = os.getenv('BOT_TOKEN')
DOGENDPOINT = os.getenv('DOG_ENDPOINT')
MESSAGE = os.getenv('MESSAGE')
msk = Misskey('fluffy.social', i=TOKEN)
MY_ID = msk.i()['id']
WS_URL = 'wss://fluffy.social/streaming?i='+TOKEN


async def runner():
    response = urllib.request.urlopen(DOGENDPOINT)
    json_data = json.loads(response.read())
    if json_data.get('status', '') != 'success':
        return
    dogurl = json_data['message']
    async with websockets.connect(WS_URL) as ws:
        await ws.send(json.dumps({
                "type": "connect",
                "body": {
                    "channel": "localTimeline",
                    "id": "local"
                }
            }))
        file = msk.drive_files_create(urllib.request.urlopen(dogurl))
        print(file)
        hello = msk.notes_create(text=MESSAGE, file_ids=[file['id']])
        print(hello)

asyncio.get_event_loop().run_until_complete(runner())
