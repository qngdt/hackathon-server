import eventlet
import socketio
import base64
import numpy as np
import cv2

import sys
import time
import os
import json
import tensorflow as tf

from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

from rule import *

sio = socketio.Server()
app = socketio.WSGIApp(sio)
all_image = []

all_poses = dict()

e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))
move = '04'

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('msg')
def message(sid, data):
    print('message ', data)

@sio.on('data')
def data(sid, data):
    global move
    global all_poses
    #global e
    # print('Data: ', data)
    imgdata = base64.b64decode(data)
    # filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    # with open(filename, 'wb') as f:
    #     f.write(imgdata)
    # img = cv2.imread('some_image.jpg')
    # print('1: ', img)
    img_np = np.fromstring(imgdata, np.uint8)
    src = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)

    if move == '05':
        image = src
    else:
        image = np.rot90(np.rot90(np.rot90(src)))
    humans = e.inference(image, resize_to_default=False, upsample_size=4.0)
    pose = dict()
    if humans and move == '05':
        #print('Save frame: ', count)
        #print(type(humans[0]))
        #print(type(humans[0].body_parts))
        for k, v in humans[0].body_parts.items():
            #print('Id: {} - {}-{} - conf:{}'.format(k, v.x, v.y, v.score))
            pose[k] = [v.x, v.y, v.score]
    elif humans:
        for k, v in humans[0].body_parts.items():
            #print('Id: {} - {}-{} - conf:{}'.format(k, v.x, v.y, v.score))
            pose[k] = [v.y, 1-v.x, v.score]

    pose = convert_pose(pose)
    print(pose)
    result = check(all_poses, pose, move)
    sio.emit('msg',json.dumps(result))
    '''
        result: {'has_error':False,'finish':False, 'where': None}
    '''
    if result['has_error'] == True:
        print('False move')
    elif result['finish'] == True:
        all_poses = dict()
        if move == '03':
            move = '04'
        elif move == '04':
            move = '05'
        elif move == '05':
            move = '03'
    # print('2: ', src)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5047)), app)
