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
def check_03(all_poses,new_pose):
    pass
def check(all_poses,new_pose,dongtac):
    if dongtac=='03':
        return None
        pass
    if dongtac=='04':
        return check_04(all_poses,new_pose)
        pass
        pass
    if dongtac=='05':
        return check_05(all_poses,new_pose)
        pass

def check_04(all_poses,pose):
    if 'RShoulder' in pose and 'MidHip' in pose and ('RWrist' in pose or 'RElbow' in pose):
        ground = [pose['MidHip'][0] , pose['MidHip'][1]+1]
        cos_hip = compute_cos_angle(pose['RShoulder'], pose['MidHip'], ground)
        try:
            arm = pose['RWrist']
        except:
            arm = pose['RElbow']

        ground_arm = [arm[0] , arm[1]+1]
        cos_arm = compute_cos_angle(pose['RShoulder'], arm, ground_arm)

        if pose['MidHip'][1] < pose['RShoulder'][1] and cos_hip > 0.75 and cos_hip < 0.91 and cos_arm < -0.75 and arm[0] > pose['MidHip'][0]-0.05:
            '''ERROR'''
            return {'has_error':True,'finish':False, 'where': 'back'}
        elif pose['MidHip'][1] < pose['RShoulder'][1] and cos_hip > 0.91 and cos_arm < -0.7 and arm[0] > pose['MidHip'][0]-0.05:
            '''CORRECT'''
            return {'has_error':False,'finish':True, 'where': None}
    '''CONTINUE'''

    return {'has_error':False,'finish':False, 'where': None}
def sub_check_05(pose):
    if ("RHip" in pose or "LHip" in pose) and ("RKnee" in pose or "LKnee" in pose) and ("RAnkle" in pose or "LAnkle" in pose):
        hip = pose['RHip'] if 'RHip' in pose else pose['LHip']
        knee = pose['RKnee'] if 'RKnee' in pose else pose['LKNee']
        ankle = pose['RAnkle'] if 'RAnkle' in pose else pose['LAnkle']
        cos = compute_cos_angle(hip, knee, ankle)
        if cos < -0.8 and knee[1] > hip[1]:
            return False
        elif knee[1] < hip[1]+0.02 and knee[1] > hip[1]-0.02:
            return True

def check_05(all_poses,pose):
    if ("RHip" in pose or "LHip" in pose) and ("RKnee" in pose or "LKnee" in pose) and ("RAnkle" in pose or "LAnkle" in pose):
        hip = pose['RHip'] if 'RHip' in pose else pose['LHip']
        knee = pose['RKnee'] if 'RKnee' in pose else pose['LKNee']
        ankle = pose['RAnkle'] if 'RAnkle' in pose else pose['LAnkle']

        cos = compute_cos_angle(hip, knee, ankle)
        print("cos",cos,knee[1] , hip[1],(cos > 0.8 or cos < -0.8) , knee[1] < hip[1])
        if (cos < -0.8) and knee[1] > hip[1]:
            return {'has_error':True,'finish':False, 'where': 'knee'}
        elif knee[1] < hip[1]+0.02 and knee[1] > hip[1]-0.02 and len(all_poses)>3 and sub_check_05(all_poses[-1]) and sub_check_05(all_poses[-2]):

            return {'has_error':False,'finish':True, 'where': None}
        return {'has_error':False,'finish':False, 'where': None}

if __name__ == '__main__':
    true_form = json_to_dict('./data_json/04_con_co/true_06.json')
    false_form = json_to_dict('./data_json/04_con_co/false_12_lung_cong.json')
