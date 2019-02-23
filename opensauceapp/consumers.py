from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .game import *

class OpenSauceConsumer(AsyncWebsocketConsumer):

    lobby = None

    async def connect(self):

        self.lobby_name = self.scope["url_route"]["kwargs"]["lobby_name"]
        self.lobby_group_name = "lobby_%s" % self.lobby_name

        # Join lobby group
        await self.channel_layer.group_add(
            self.lobby_group_name,
            self.channel_name
        )

        await self.accept()
        # Send the gamestate on load
        await self.update_game_state(None)

    async def disconnect(self, close_code):
        # Leave lobby group
        await self.channel_layer.group_discard(
            self.lobby_group_name,
            self.channel_name
        )
        secKey = str(dict(self.scope["headers"])[b'sec-websocket-key'])[2:-1]
        lobby = Game.getInstance().getLobby(self.lobby_name)
        lobby.removePlayer(secKey)

        print(Game.getInstance())

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        # type of the request
        type = data["type"]
        # convert from byte to string the secret key of the socket
        # to have a unique id that represent the player
        secKey = str(dict(self.scope["headers"])[b'sec-websocket-key'])[2:-1]
        print("$<" + secKey + "> " + str(data))

        shouldInformOthers = False

        lobby = Game.getInstance().getLobby(self.lobby_name)

        # Evaluate the message
        if type == "join":
            lobby.addPlayer(secKey, data["pseudo"])
            shouldInformOthers = True
        elif type == "leave":
            lobby.removePlayer(secKey)
            shouldInformOthers = True
        elif type == "submit":
            shouldInformOthers = lobby.submit(secKey, data["answer"])

        print(Game.getInstance())

        # Inform the other player if needed
        if shouldInformOthers:
            await self.channel_layer.group_send(
                self.lobby_group_name,
                {
                    "type": "update_game_state"
                }
            )

    async def update_game_state(self, event):
        lobby = Game.getInstance().getLobby(self.lobby_name)
        await self.send(text_data=json.dumps({
            "type": "game_state",
            "state": lobby.getStatus()
        }))
