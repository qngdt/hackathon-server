import eventlet
import socketio
import base64
import numpy as np
import cv2 

sio = socketio.Server()
app = socketio.WSGIApp(sio)

all_image = []

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('msg')
def message(sid, data):
    print('message ', data)

@sio.on('data')
def data(sid, data):
    print('Data: ', data)
    imgdata = base64.b64decode(data)
    img_np = np.fromstring(imgdata, np.uint8)
    src = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
    print('1: ', src)
    all_image.append(src)
    print(len(all_image))


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)