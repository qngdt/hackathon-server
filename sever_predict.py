import os
import json
import tensorflow as tf
from PIL import Image
import base64
import io

from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

def predict_pose(e, image):
    if e == None:
        print('Please pass TfPoseEstimator')
        return None
    image = cv2.resize(image, (432, 368))
    pred_image = np.rot90(np.rot90(np.rot90(image)))
    pred_image = cv2.resize(pred_image, (432, 368))
    humans = e.inference(pred_image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
    if humans:
        pose = dict()
        for k, v in humans[0].body_parts.items():
            #Reversed
            pose[k] = [v.y, 1-v.x, v.score]
        return pose
    else:
        print('No pose detected\n')
        return None

if __name__ == '__main__':
    base64_byte = base64.b64encode(open("images/yoga1.jpg", "rb").read())
    print(type(base64_byte))
    #img = stringToRGB(base64_byte)
    #cv2.imwrite('images/base64_decode.png', img)
