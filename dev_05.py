from dev_rule import *
from rule import *
import math
import numpy as np
import cv2

tocdovideo=24
tocdomang=1

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def compute_cos_angle(point1,point2,point3):
    point1 = point1[0:2]
    point2 = point2[0:2]
    point3 = point3[0:2]

    vector21 = [point1[0] - point2[0], point1[1] - point2[1]]
    vector23 = [point3[0] - point2[0], point3[1] - point2[1]]
    #print('Math: ', vector21[0] ** 2 + vector21[1] ** 2)
    cos = (vector21[0] * vector23[0] + vector21[1] * vector23[1]) / (
                math.sqrt(vector21[0] ** 2 + vector21[1] ** 2) * math.sqrt(vector23[0] ** 2 + vector23[1] ** 2))

    return cos

def check_04(all_poses,new_pose,json_path=None):
    print(json_path[:-5])
    #print(all_poses)
    #print(new_pose.keys())
    for frame,pose in all_poses.items():
        if frame % 12 != 0:
            continue
        if json_path is not None:
            img=cv2.imread(json_path[:-5]+'/'+str(frame)+'.png')
            img=cv2.resize(img,(500,500))
        #print(pose)
            if 'RShoulder' in pose and 'MidHip' in pose and ('RWrist' in pose or 'RElbow' in pose):
                ground = [pose['MidHip'][0] , pose['MidHip'][1]+1]
                cos_hip = compute_cos_angle(pose['RShoulder'], pose['MidHip'], ground)
                try:
                    arm = pose['RWrist']
                except:
                    arm = pose['RElbow']

                ground_arm = [arm[0] , arm[1]+1]
                cos_arm = compute_cos_angle(pose['RShoulder'], arm, ground_arm)

                if pose['MidHip'][1] < pose['RShoulder'][1] and cos_hip > 0.8 and cos_hip < 0.87 and cos_arm < -0.7 and arm[0] > pose['MidHip'][0]-0.05:
                    #ground = [pose['MidHip'][0] , pose['MidHip'][1]+1]
                    #cos = compute_cos_angle(pose['RShoulder'], pose['MidHip'], ground)
                    #ground_arm = [arm[0] , arm[1]+1]
                    #cos_arm = compute_cos_angle(pose['RShoulder'], arm, ground_arm)
                    print('F: {} - cos_hip: {} - cos_arm: {} - distance: {}'.format(frame, cos_hip, cos_arm, pose['MidHip'][0] - arm[0]))

                    cv2.circle(img,(int(pose['MidHip'][0]*img.shape[0]),int(pose['MidHip'][1]*img.shape[0])),20,(0,0,255),-1)
                    cv2.circle(img,(int(pose['RShoulder'][0]*img.shape[0]),int(pose['RShoulder'][1]*img.shape[0])),20,(0,0,255),-1)
                    cv2.circle(img,(int(arm[0]*img.shape[0]),int(arm[1]*img.shape[0])),20,(0,0,255),-1)
                    cv2.waitKey(600)
                elif pose['MidHip'][1] < pose['RShoulder'][1] and cos_hip > 0.87 and cos_arm < -0.7 and arm[0] > pose['MidHip'][0]-0.05:
                    print('T: {} - cos_hip: {} - cos_arm: {} - distance: {}'.format(frame, cos_hip, cos_arm, pose['MidHip'][0] - arm[0]))

                    cv2.circle(img,(int(pose['MidHip'][0]*img.shape[0]),int(pose['MidHip'][1]*img.shape[0])),20,(0,255,0),-1)
                    cv2.circle(img,(int(pose['RShoulder'][0]*img.shape[0]),int(pose['RShoulder'][1]*img.shape[0])),20,(0,255,0),-1)
                    cv2.circle(img,(int(arm[0]*img.shape[0]),int(arm[1]*img.shape[0])),20,(0,255,0),-1)
                    cv2.waitKey(600)

            cv2.imshow("debug",img)
            if cv2.waitKey(20)==27:
                exit(-1)
                    #return {'has_error':True,'finish':False, 'where': 'back'}

    return {'has_error':False,'finish':False, 'where': None}

if __name__ == '__main__':
    true_form = json_to_dict('data_json/04_con_co/true_06.json')
    false_form = json_to_dict('data_json/04_con_co/false_12_lungcong.json')

    dongtac = '04'
    current_all_poses = []

    #print('False form: ', false_form[133])
    #print('True form: ', true_form[237])
    #bd_parts = intersection(false_form[126].keys(), true_form[233].keys())

    #print('True: ', compute)
    check_04(false_form, None, 'data_json/04_con_co/false_12_lungcong.json')
    check_04(true_form, None, 'data_json/04_con_co/true_06.json')
