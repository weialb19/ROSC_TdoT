import websockets
import asyncio
import cv2 as cv

capture = cv.VideoCapture(0)


async def send_capture():
   # print('try to send capture')
    async with websockets.connect("ws://192.168.0.167:6543/camera") as websocket:
        while True:
            #print('capture frame')
            encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 30]
            ret, frame = capture.read()
            other_ret, buffer = cv.imencode(".JPEG", frame, encode_param)


            await websocket.send(buffer.tobytes())

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    asyncio.run(send_capture())