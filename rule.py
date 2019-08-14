import json

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
        result=check_03(all_poses,new_pose)
        if result['has_error'] is True or result['finish'] is True:
            return result
        pass
    if dongtac=='04':
        return check_04(all_poses,new_pose)
        pass
        pass
    if dongtac=='05':
        pass

def check_04(all_poses,new_pose):
    if 'RShoulder' in pose and 'MidHip' in pose and ('RWrist' in pose or 'RElbow' in pose):
        ground = [pose['MidHip'][0] , pose['MidHip'][1]+1]
        cos_hip = compute_cos_angle(pose['RShoulder'], pose['MidHip'], ground)
        try:
            arm = pose['RWrist']
        except:
            arm = pose['RElbow']

        ground_arm = [arm[0] , arm[1]+1]
        cos_arm = compute_cos_angle(pose['RShoulder'], arm, ground_arm)

        if pose['MidHip'][1] < pose['RShoulder'][1] and cos_hip > 0.8 and cos_hip < 0.91 and cos_arm < -0.7 and arm[0] > pose['MidHip'][0]-0.05:
            '''ERROR'''
            return {'has_error':True,'finish':False, 'where': 'back'}
        elif pose['MidHip'][1] < pose['RShoulder'][1] and cos_hip > 0.91 and cos_arm < -0.7 and arm[0] > pose['MidHip'][0]-0.05:
            '''CORRECT'''
            return {'has_error':False,'finish':True, 'where': None}
    '''CONTINUE'''
    return {'has_error':False,'finish':False, 'where': None}

if __name__ == '__main__':
    true_form = json_to_dict('./data_json/04_con_co/true_06.json')
    false_form = json_to_dict('./data_json/04_con_co/false_12_lung_cong.json')
