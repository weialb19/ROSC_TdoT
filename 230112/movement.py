import tornado.websocket
import tornado.ioloop

class MovementClient:

    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop
        pass

    def start(self):
        self.connect()
        pass

    def connect(self):
        tornado.websocket.websocket_connect('ws://localhost:6543/movement',
                                            callback=self.retry_connect,
                                            on_message_callback= self.on_message,
                                            ping_interval=10,
                                            ping_timeout=30)
        pass

    def on_message(self, message):
        print(f'received msg {message}')
        # send data to PINS
        pass

    def retry_connect(self, future):
        try:
            self.connection = future.result()
            print(f'connected')
        except:
            print(f'reconnect failed')
            self.io_loop.call_later(3, self.connect())
        pass

def runTheClient():
    io_loop = tornado.ioloop.IOLoop.current()
    client = MovementClient(io_loop)

    io_loop.add_callback(client.start)
    io_loop.start()

if __name__ == "__main__":
    runTheClient()