import json
import cv2
import numpy as np

def convert_pose(pose):
    new_pose = dict()
    body = {0: 'Nose', 1:  "Neck", 2:  "RShoulder", 3:  "RElbow", 4:  "RWrist", 5:  "LShoulder", 6:  "LElbow",
            7:  "LWrist", 8:  "MidHip", 9:  "RHip", 10: "RKnee", 11: "RAnkle", 12: "LHip", 13: "LKnee",
            14: "LAnkle", 15: "REye", 16: "LEye", 17: "REar", 18: "LEar", 19: "LBigToe", 20: "LSmallToe",
            21: "LHeel", 22: "RBigToe", 23: "RSmallToe", 24: "RHeel", 25: "Background"}
    for idx, value in pose.items():
        new_pose[body[int(idx)]] = value
    return new_pose

def json_to_dict(json_path):
    new_data = dict()
    with open(json_path, 'r') as f:
        data = json.load(f)
    for fr, body in data.items():
        new_data[int(fr)] = convert_pose(body)
    return new_data

def check_value_difference(value1, value2):
    threshold = 0.04
    if value2 < (value1+threshold) and value2 > (value1-threshold):
        return True
    return False

def check_stable(check, previous, current):
    '''
        return 1: correct 1
        return 2: correct 2 ==> stable
    '''
    important = ["RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist",
                "MidHip",  "RHip", "RKnee" , "RAnkle", "LHip", "LKnee", "LAnkle"]
    key_c = list(current.keys())
    stable_or_not = False
    for body_part, value in previous.items():
        if body_part in important and body_part in key_c:
            print('{} - prev: ({},{}) - current: ({},{})'.format(body_part,
                previous[body_part][0], previous[body_part][1],current[body_part][0], current[body_part][1]))
            stable_or_not = check_value_difference(previous[body_part][0], current[body_part][0])
            stable_or_not = check_value_difference(previous[body_part][0], current[body_part][0])
    if stable_or_not:
        check += 1
    elif check != 2:
        check = 0
    return check

if __name__ == '__main__':
    #data = json_to_dict('true_01.json')
    img = cv2.imread('images/rotated90.png', cv2.IMREAD_COLOR)
    cv2.imwrite('images/rerotated90.png', np.rot90(img))
    '''# get image height, width
    (h, w) = img.shape[:2]
    # calculate the center of the image
    center = (w / 2, h / 2)
    scale = 1.0

    M = cv2.getRotationMatrix2D(center, -90, scale)
    rotated90 = cv2.warpAffine(img, M, (w, h))
    #cv2.imshow('image',rotated90)
    cv2.imwrite('images/rotated90.png', rotated90)

    (h, w) = rotated90.shape[:2]
    # calculate the center of the image
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 90, scale)
    rerotated90 = cv2.warpAffine(rotated90, M, (h, w))
    cv2.imwrite('images/rerotated90.png', rerotated90)'''
