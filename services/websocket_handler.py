import asyncio
from asyncio import get_event_loop
from asyncio import sleep
from base64 import b64encode
from io import BytesIO
from typing import Optional

from websockets import serve
from websockets.exceptions import ConnectionClosedError
from websockets.exceptions import ConnectionClosedOK

from backend import PEControl

pe_control: Optional[PEControl] = None


def set_control(pe_control_):
    global pe_control
    pe_control = pe_control_


async def echo(websocket, *args):
    while True:
        try:
            await send_screenshot(websocket)
            await sleep(0.1)
        except (ConnectionClosedOK, ConnectionClosedError):
            break


async def send_screenshot(websocket):
    pil_image = pe_control.get_screenshot()
    pil_image = pil_image.resize((int(pil_image.width * 0.3), int(pil_image.height * 0.3)))

    image_data = BytesIO()
    pil_image.save(image_data, format="JPEG")
    image_data = image_data.getvalue()

    encoded_image_data = b64encode(image_data).decode('utf-8')
    await websocket.send(encoded_image_data)


def run(host, port):
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    get_event_loop().run_until_complete(serve(echo, host, port))
    get_event_loop().run_forever()
