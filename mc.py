import time
from minecraft.networking.connection import Connection
from minecraft.networking.packets.clientbound.play import ChatMessagePacket, DisconnectPacket
from minecraft.networking.packets.clientbound.play import JoinGamePacket
from minecraft.networking.packets.serverbound.play import ChatPacket


class MC:

    def __init__(self, server_info: tuple):
        host = server_info[0]
        port = server_info[1]
        username = server_info[2]
        version = server_info[3]
        self.connection = Connection(host, port, username=username, initial_version=version, allowed_versions=[version])

    def message(self, message: str):
        packet = ChatPacket()
        packet.message = message
        self.connection.write_packet(packet)

    def login(self, command: str):
        time.sleep(1)
        self.message(command)

    def register_packet_listener(self, method, *packet_types, **kwds):
        self.connection.register_packet_listener(method, packet_types, kwds)

    def register_chat_listener(self, method):
        self.connection.register_packet_listener(method, ChatMessagePacket)

    def register_join_game_listener(self, method):
        self.connection.register_packet_listener(method, JoinGamePacket)

    def register_disconnect_listener(self, method):
        self.connection.register_packet_listener(method, DisconnectPacket)

    def handle_join_game(self, join_game_packet):
        print('Connected.')

    def handle_disconnect_game(self, disconnect_packet):
        print('Disconnected.')

    def connect(self):
        print("Connecting to Server...")
        self.register_join_game_listener(self.handle_join_game)
        self.register_disconnect_listener(self.handle_disconnect_game)
        self.connection.connect()
