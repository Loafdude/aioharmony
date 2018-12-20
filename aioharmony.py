import asyncio
import websockets

hub_ip = "10.9.8.194"

DEFAULT_HUB_PORT = 8088

class HarmonyHub:

    def __init__(self, ip_address):
        self._ip_address = ip_address
        self._friendly_name = None
        self._remote_id = None
        self._email = None
        self._account_id = None
        self._websocket = None
        self._msgid = 0
        self._config = None
        self._activities = None
        self._devices = None

    async def connect(self):
        self._websocket = await websockets.connect(
            'ws://{}:{}/?domain=svcs.myharmony.com&hubId={}'.format(
            self._ip_address, DEFAULT_HUB_PORT, self._remote_id
            ))

        # ToDo: Send message to hub and ensure connection is good.
        # ToDo: Check response, error if bad

    async def send(self, message):
        return await self._websocket.send(message)

    async def listen(self):
        return await self._websocket.recv()
        while True:
            await asyncio.sleep(0)
            try:
                print('Listening for a message...')
                message = await self._websocket.recv()
                print("Message: {}".format(message))

            except self._websocket.ConnectionClosed as cc:
                print('Connection closed')

            except Exception as e:
                print('Something happened')


async def harmony_app():
    async with HarmonyHub(hub_ip) as hub:
        await hub.connect()
        asyncio.ensure_future(hub.listen_for_message())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(harmony_app())
    loop.run_forever()


