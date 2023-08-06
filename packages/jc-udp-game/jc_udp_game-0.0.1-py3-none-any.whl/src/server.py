import json
import signal
import socket
import threading
import time
from json import JSONDecodeError
from threading import Thread

from .core.map import Map
from .helpers.logger_interface import LoggerInterface

global server


class GameServer(LoggerInterface):
    event_count = 0

    def __init__(self, ip: str, port: int, buffer_size=2500):
        self.buffer_size = buffer_size
        self.socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM,
            proto=socket.IPPROTO_UDP
        )
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(2)
        self.socket.bind((ip, port))
        self._setup_logger("GameServer")
        self.logger.info(f"> Creating server at {ip}:{port} ...")
        self.clients = dict()
        self.map = Map(self)
        self.should_run = True
        self.lock = threading.Lock()
        self.broadcaster = Thread(target=self.broadcast_positions)
        self.broadcaster.setName("JC Server Broadcaster")

        self.worker_threads = []

        for thread_id in range(4):
            self.worker_threads.append(Thread(target=self.main_thread, args=(thread_id,)))
            self.worker_threads[thread_id].setName(f"JC Server Main Thread #{thread_id}")

    def broadcast_positions(self):
        while self.should_run:
            positions = {c['nickname']: [c['x'], c['y'], c['color']] for c in self.clients.values()}
            positions = json.dumps(dict(positions=positions)).encode('utf-8')

            clients_copy = self.clients.copy()
            for _, c in clients_copy.items():
                self.socket.sendto(positions, c['address'])
            time.sleep(0.02)
            for _, c in clients_copy.items():
                self.socket.sendto(self.map.to_bytes(), c['address'])
            time.sleep(0.02)

    def start(self, join=True):
        self.logger.info('> Server started')
        self.broadcaster.start()
        for t in self.worker_threads:
            t.start()
        if join:
            self.join()

    def join(self):
        for t in self.worker_threads:
            if t.is_alive():
                t.join()

    def main_thread(self, thread_id):
        def xlog(msg):
            self.logger.info(f'[Thread-{thread_id}]: {msg}')

        xlog('Starting...')
        while self.should_run:
            to_remove = []

            clients_copy = self.clients.copy()

            for cid, c in clients_copy.items():
                if (time.time() - c['last_ping']) > 3:
                    to_remove.append(cid)
            for cid in to_remove:
                self.logger.warning(f'Remove client {cid}')
                if cid in self.clients:
                    del self.clients[cid]

            try:
                bytesAddressPair = self.socket.recvfrom(self.buffer_size)
            except socket.timeout:
                continue

            while self.lock.locked():
                time.sleep(1/1000)
            self.lock.acquire(blocking=True, timeout=1)
            self.event_count += 1
            self.lock.release()
            if self.event_count % 1000 == 0:
                xlog(f'Event count: {self.event_count}')

            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            client_ip, client_port = address
            client_id = f'{client_ip}_{client_port}'

            if client_id not in self.clients:
                self.register_client(client_id, address, message, xlog)
                continue
            # else:
            try:
                data = json.loads(message)

                if self.clients[client_id]['color'] is None:
                    self.clients[client_id]['color'] = tuple(data)
                    self.logger.info(f'Set color for {client_id} -> {tuple(data)}')

                if 'position' in data:
                    x, y = data['position']
                    self.clients[client_id]['x'] = x
                    self.clients[client_id]['y'] = y
                if 'set_block' in data:
                    x, y = data['set_block']['x'], data['set_block']['y']
                    self.map.set_block(x, y)
            except JSONDecodeError:
                if message == b'PING':
                    self.clients[client_id]['last_ping'] = time.time()

    def register_client(self, client_id, address, message, xlog):
        nick_valid = True

        for _, cl in self.clients.items():
            if cl['nickname'] == message.decode('utf-8'):
                nick_valid = False
                break

        if not nick_valid:
            return

        self.clients[client_id] = dict(
            address=address,
            last_ping=time.time(),
            nickname=message.decode('utf-8'),
            x=0,
            y=0,
            color=None
        )
        xlog(f'New client connected with nick: {message.decode("utf-8")} and ip {address}')





def start():
    server = GameServer('0.0.0.0', 4242)

    def signal_handler(sig, frame):
        global server
        print('Stopping server...')
        server.should_run = False

    signal.signal(signal.SIGINT, signal_handler)
    server.start()


if __name__ == "__main__":
    start()
