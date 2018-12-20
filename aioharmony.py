import asyncio
import websockets
from aiohttp import ClientSession

hub_ip = "10.9.8.194"
loop = asyncio.get_event_loop()
DEFAULT_HUB_PORT = 8088

class HarmonyHub:

    def __init__(self, ip_address, loop):
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
        self._loop = loop

    async def connect(self):
        if self._remote_id is None:
            self._loop.run_until_complete(self.retrieve_hub_info())

        self._websocket = await websockets.connect(
            'ws://{}:{}/?domain=svcs.myharmony.com&hubId={}'.format(
            self._ip_address, DEFAULT_HUB_PORT, self._remote_id
            ))

        # ToDo: Send message to hub and ensure connection is good.
        # ToDo: Check response, error if bad

    async def retrieve_hub_info(self):
        """Retrieve the harmony Hub information."""
        url = 'http://{}:{}/'.format(self._ip_address, DEFAULT_HUB_PORT)
        headers = {
            'Origin': 'http://localhost.nebula.myharmony.com',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8',
        }
        json_request = {
            "id ": 1,
            "cmd": "connect.discoveryinfo?get",
            "params": {}
        }
        async with ClientSession() as session:
            async with session.post(
                url, json=json_request, headers=headers) as response:
                json_response = await response.json()
                self._friendly_name = json_response['data']['friendlyName']
                self._remote_id = str(json_response['data']['remoteId'])
                self._email = json_response['data']['email']
                self._account_id = str(json_response['data']['accountId'])

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
    hub = HarmonyHub(hub_ip, loop)
    await hub.connect()
    asyncio.ensure_future(hub.listen())

if __name__ == '__main__':
    loop.run_until_complete(harmony_app())
    loop.run_forever()


