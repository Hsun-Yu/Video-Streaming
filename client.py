import asyncio
import logging
from datetime import datetime
from aiowebsocket.converses import AioWebSocket
import base64

import io
from PIL import Image
import cv2
import numpy as np

import sys

async def startup(uri):
    async with AioWebSocket(uri) as aws:
        converse = aws.manipulator
        message = b'next'
        while True:
            await converse.send(message)
            print('{time}-Client send: {message}'
                  .format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message=message))
            mes = await converse.receive()
            print('{time}-Client receive: {rec}'
                  .format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rec=mes))
            imgData = base64.b64decode(mes)
            nparr = np.fromstring(imgData, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow('video', img_np)
            cv2.waitKey(delay = 1)

if __name__ == '__main__':
    ip = sys.argv[1]
    # remote = 'ws://10.0.1.11:5012/stream'
    remote = 'ws://'+ ip +':5012/stream'
    print(remote)
    try:
        asyncio.get_event_loop().run_until_complete(startup(remote))
    except KeyboardInterrupt as exc:
        logging.info('Quit.')