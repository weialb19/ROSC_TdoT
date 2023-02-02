# we try to build our own websocket server
import base64
from datetime import datetime
from typing import Optional, Awaitable

#webServer? we need an async framework -> tornado
import cv2 as cv
import tornado
import tornado.web
import tornado.websocket
import tornado.ioloop
import numpy as np


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")


class WebPageHandler(tornado.websocket.WebSocketHandler):

    connections = set()

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self):
        if len(self.connections) > 3:
            self.close()
        else:
            print('Webpage established')
            self.connections.add(self)

    def on_close(self):
        if self in self.connections:
            self.connections.remove(self)

    def on_message(self, message):
        print(f'received message: {message}')
        [client.write_message(message) for client in MovementHandler.connections]


class MovementHandler(tornado.websocket.WebSocketHandler):

    connections = set()

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self):
        if len(self.connections) > 3:
            self.close()
        else:
            print('Movement established')
            self.connections.add(self)

    def on_close(self):
        if self in self.connections:
            self.connections.remove(self)

    def on_message(self, message):
        print(f'received message: {message}')


class CameraHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        if len(self.connections) > 3:
            self.clear()
        else:
            print('Connection established')
            self.connections.add(self)

    def on_close(self):
        if self in self.connections:
            self.connections.remove(self)

    def on_message(self, cameraImage):
        #print('received message')
        array_image = np.frombuffer(cameraImage, dtype=np.uint8)

        frame = cv.imdecode(array_image, cv.IMREAD_COLOR)

        frame = self.add_time_to_image(frame)
        _, webpageImage = cv.imencode('.JPEG', frame)

        [client.write_message(base64.b64encode(webpageImage)) for client in WebPageHandler.connections]

    def add_time_to_image(self, frame):
        font = cv.FONT_HERSHEY_SIMPLEX
        position = (30,30)
        color = (255, 0, 0)
        font_scale = 1
        thickness = 1
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        cv.putText(frame, current_time, position, font, font_scale, color, thickness, cv.LINE_AA)
        return frame


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler), # endpoints and the handler class
        (r'/camera', CameraHandler),
        (r'/webpage', WebPageHandler),
        (r'/movement', MovementHandler)
    ])


if __name__ == '__main__':
    app = make_app() # make_app is my own function and returns an tornado.web.application
    app.listen(6543)
    tornado.ioloop.IOLoop.current().start()
