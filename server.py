import eventlet
import socketio
import base64
import numpy as np
import cv2 

sio = socketio.Server()
app = socketio.WSGIApp(sio)
all_images = []

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('msg')
def message(sid, data):
    print('message ', data)

@sio.on('data')
def data(sid, data):
    # print('Data: ', data)
    imgdata = base64.b64decode(data)
    # filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    # with open(filename, 'wb') as f:
    #     f.write(imgdata)
    # img = cv2.imread('some_image.jpg')
    # print('1: ', img)
    img_np = np.fromstring(imgdata, np.uint8)
    src = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
    all_images.append(src)
    # print('2: ', src)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5047)), app)