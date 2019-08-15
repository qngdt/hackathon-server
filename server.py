import eventlet
import socketio
import base64
import numpy as np
import cv2
import time
import math
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

all_poses = []

e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))
move = '05'

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
    #print('Move: ', move)
    img_np = np.fromstring(imgdata, np.uint8)
    src = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
    cv2.imwrite("defore_rotate.png",src)
    # cv2.waitKey(200)
    if move == '05':
        #print("khong rotate")
        image = src
    else:
        image = np.rot90(np.rot90(np.rot90(src)))

    # print("debug")
    start=time.time()
    humans = e.inference(image, resize_to_default=False, upsample_size=4.0)
    #print('Time to predict: ', time.time()-start)
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
    # cv2.circle(image,(int(pose[''][0] * img.shape[0]), int(pose[part][1] * img.shape[0])),15, (255, 255, 0),-1)
    # cv2.circle(img, )
    # cv2.imwrite("debug_rotate.png",image)
    #print(pose.keys())
    all_poses.append(pose)
    result = check(all_poses, pose, move)
    #print('Result: ', result)

    '''
        result: {'has_error':False,'finish':False, 'where': None}
    '''
    if result == None:
        result={'has_error':False,'finish':False, 'where': None}

    if result['finish'] == True:
        all_poses = list()
        if move == '04':
            move = '05'
        elif move == '05':
            move = '04'
    sio.emit('msg',json.dumps(result))
    # print('2: ', src)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5047)), app)
