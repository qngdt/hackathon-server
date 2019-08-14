import argparse
import logging
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

logger = logging.getLogger('TfPoseEstimatorRun')
logger.handlers.clear()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.WARN)
    import os
    #print(os.listdir('.'))
    parser = argparse.ArgumentParser(description='tf-pose-estimation run')
    parser.add_argument('--video', type=str, default='images/yoga2.jpg')
    parser.add_argument('--model', type=str, default='cmu',
                        help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. '
                             'default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')
    parser.add_argument('--img_folder', type=str, default='')
    parser.add_argument('--output_json', type=str, default='')
    parser.add_argument('--mode', type=str, default='drive')

    args = parser.parse_args()

    w, h = model_wh(args.resize)
    if w == 0 or h == 0:
        e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))

    cap = cv2.VideoCapture(args.video if args.mode !='drive' else '/content/drive/My Drive/Openpose/'+ args.video)
    count = 0
    data = dict()

    if cap.isOpened() is False:
        print("Error opening video stream or file")
    while cap.isOpened():
        # estimate human poses from a single image !
        ret_val, image = cap.read()
        if image is None:
            logger.error('Image can not be read')
            print(count)
            break
        #pred_image = np.rot90(np.rot90(np.rot90(image)))
        pred_image = image
        pred_image = cv2.resize(pred_image, (432, 368))
        '''For squat only'''
        pred_image = image
        #print(image.shape)

        humans = e.inference(pred_image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
        #print(humans)
        pred_image = TfPoseEstimator.draw_humans(pred_image, humans, imgcopy=False)
        cv2.putText(pred_image, "Frame: %d" % (count), (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        path = args.img_folder if args.mode !='drive' else '/content/drive/My Drive/Openpose/'+ args.img_folder
        path += '/{}.png'.format(count)
        #cv2.imwrite(path, np.rot90(pred_image))
        cv2.imwrite(path, pred_image)
        pose = dict()
        if humans:
            #print('Save frame: ', count)
            #print(type(humans[0]))
            #print(type(humans[0].body_parts))
            for k, v in humans[0].body_parts.items():
                #print('Id: {} - {}-{} - conf:{}'.format(k, v.x, v.y, v.score))
                #pose[k] = [v.y, 1-v.x, v.score]
                pose[k] = [v.x, v.y, v.score]
            data[count] = pose
        count += 1

    with open(args.output_json if args.mode !='drive' else '/content/drive/My Drive/Openpose/' + args.output_json, 'w') as outfile:
        json.dump(data, outfile)
