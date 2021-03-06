import json
import math

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

def convert_pose(pose):
    new_pose = dict()
    body = {0: 'Nose', 1:  "Neck", 2:  "RShoulder", 3:  "RElbow", 4:  "RWrist", 5:  "LShoulder", 6:  "LElbow",
            7:  "LWrist", 8:  "MidHip", 9:  'RKnee', 10: "RAnkle", 11: "LHip", 12: 'LKnee', 13: "LAnkle",
            14: "RHip", 15: "LEye", 16: "REye", 17: "LEar", 18: "REar", 19: "LBigToe", 20: "LSmallToe",
            21: "LHeel", 22: "RBigToe", 23: "RSmallToe", 24: "RHeel", 25: "Background"}
    for idx, value in pose.items():
        new_pose[body[int(idx)]] = value
    return new_pose

def json_to_dict(json_path):
    new_data = dict()
    with open(json_path, 'r') as f:
        data = json.load(f)
    import os
    max_frame=len(os.listdir(json_path[:-5]))
    for fr in range(max_frame):
        if str(fr) in data:
            new_data[int(fr)] = convert_pose(data[str(fr)])
        else:
            new_data[int(fr)]={}
    # for fr, body in data.items():
    #     new_data[int(fr)] = convert_pose(body)
    return new_data
def check(all_poses,new_pose,dongtac):

    if dongtac=='04':
        return check_04(all_poses,new_pose)
        pass
        pass
    if dongtac=='05':
        return check_05(all_poses,new_pose)
        pass
    else:
        return{'finish':False}

def check_04(all_poses,pose):
    if 'LShoulder' in pose and ('MidHip' in pose or 'LHip' in pose) and ('LWrist' in pose or 'LElbow' in pose):
        hip = pose['MidHip'] if 'MidHip' in pose else pose['LHip']
        ground = [hip[0] , hip[1]+1]
        cos_hip = compute_cos_angle(pose['LShoulder'], hip, ground)
        try:
            arm = pose['LWrist']
        except:
            arm = pose['LElbow']

        ground_arm = [arm[0] , arm[1]+1]
        cos_arm = compute_cos_angle(pose['LShoulder'], arm, ground_arm)

        #print('Arm: ', cos_arm, 'Back: ', cos_hip, 'Dis: ', abs(arm[0]-hip[0]))
        if hip[1] < pose['LShoulder'][1] and cos_hip <0.45 and cos_hip > 0:
            '''ERROR'''
            print('LOI. Lung ban dang bi cong len. Hay chinh lai!!!!')
            return {'has_error':True,'finish':False, 'where': 'lung_cong_len'}
        if hip[1] >= pose['LShoulder'][1] and cos_hip <0.45 and cos_hip > 0:
            '''ERROR'''
            print('LOI. Lung ban dang bi vong. Hay chinh lai!!!!')
            return {'has_error':True,'finish':False, 'where': 'lung_cong_xuong'}
        elif hip[1] < pose['LShoulder'][1] and cos_hip > 0.65:
            '''CORRECT'''
            print('Hoan thanh bai tap 4!!!! CHUC MUNG')
            return {'has_error':False,'finish':True, 'where': None}
        else:
            print('Gap nguoi lai nao')
            return {'has_error':False,'finish':False, 'where': None}
    '''CONTINUE'''

    return {'has_error':False,'finish':False, 'where': None}
def sub_check_05(pose):
    if "LHip" in pose and "LKnee" in pose and "LAnkle" in pose:
        hip = pose['LHip']
        knee = pose['LKnee']
        ankle = pose['LAnkle']
        cos = compute_cos_angle(hip, knee, ankle)
        if cos >0.7 and knee[1] < hip[1]:
            return False
        elif cos > -0.25 and cos < 0.25 :
            return True

def check_05(all_poses,pose):
    if "LHip" in pose and "LKnee" in pose and "LAnkle" in pose:
        hip = pose['LHip']
        knee = pose['LKnee']
        ankle = pose['LAnkle']

        cos = compute_cos_angle(hip, knee, ankle)
        #print("===============cos",cos,knee[1] ,'hip: ', hip[1],'knee' , knee[1])
        if cos >0.7 and knee[1] < hip[1]:
            print('LOI: Mui chan bi day ve sau!!! LAY LAI THANG BANG')
            return {'has_error':True,'finish':False, 'where': 'mui_chan_sau'}
        elif cos > -0.25 and cos < 0.25 and\
         len(all_poses)>3 and sub_check_05(all_poses[-1]) and sub_check_05(all_poses[-2]):
            print('Hoan thanh bai tap 5!!!! CHUC MUNG')
            return {'has_error':False,'finish':True, 'where': None}
        if cos > 0:
            print('Nang mong len nao!')
            return {'has_error':False,'finish':False, 'where': 'nang_mong'}
        elif cos <= 0:
            print('Ha mong xuong di!')
            return {'has_error':False,'finish':False, 'where': 'ha_mong'}
        else:
            return {'has_error':False,'finish':False, 'where': None}

if __name__ == '__main__':
    true_form = json_to_dict('./data_json/04_con_co/true_06.json')
    false_form = json_to_dict('./data_json/04_con_co/false_12_lung_cong.json')
