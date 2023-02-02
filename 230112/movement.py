import json

import tornado.websocket
import tornado.ioloop
import board
import busio
import adafruit_pca9685
import time

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 60
motor0 = pca.channels[0]
motor0reverse = pca.channels[1]
motor1 = pca.channels[2]
motor1reverse = pca.channels[3]


class MovementClient:

    def __init__(self, io_loop):
        self.io_loop = io_loop
        self.connection = None
        pass

    def start(self):
        self.connect()
        pass

    def connect(self):
        tornado.websocket.websocket_connect(url=f'ws://localhost:6543/movement', callback=self.retry_connect,
                                            on_message_callback=self.on_message,
                                            ping_interval=10, ping_timeout=30)
        pass

    def on_message(self, message):
        print(f'message: {message}')
        #json_str = json.dumps(message)
        resp = json.loads(message)
        x = resp["x"]
        y = resp["y"]
        self.make_move(x, y)
        pass

    def retry_connect(self, future):
        try:
            self.connection = future.result()
            print(f'connected')
        except:
            print(f'reconnect failed')
            self.io_loop.call_later(3, self.connect())
        pass

    def make_move(self, x, y):
        if x == 0 and y == 1:
            # print(x)
            # print(y)
            motor0.duty_cycle = 65535
            motor1.duty_cycle = 65535
        elif x == 0 and y == -1:
            # print(x)
            # print(y)
            motor0reverse.duty_cycle = 65535
            motor1reverse.duty_cycle = 65535
        pass



def runTheClient():
    io_loop = tornado.ioloop.IOLoop.current()
    client = MovementClient(io_loop)
    io_loop.add_callback(client.start)
    io_loop.start()
    pass


if __name__ == "__main__":
    runTheClient()