import os
from rule import check,json_to_dict
tocdovideo=24
tocdomang=1
#dongtac='03'
#folder_path='./data_json/03_v_nguoc'
#files=os.listdir(folder_path)

def getbatchposes(poses,tocdovideo,tocdomang,batch_id):
    ans={}
    for i in range(0,tocdomang):
        if batch_id*tocdovideo+i*int(tocdovideo/tocdomang) in poses:
            ans[batch_id*tocdovideo+i*int(tocdovideo/tocdomang)]=poses[batch_id*tocdovideo+i*int(tocdovideo/tocdomang)]
        else:
            ans[batch_id * tocdovideo + i * int(tocdovideo / tocdomang)]={}
    return ans
    pass


'''for file in files:
    current_all_poses={}
    if not 'json' in file:
        continue
    print(file)
    json_path=folder_path+'/'+file
    poses=json_to_dict(json_path)
    print(poses.keys())
    for frame,pose in poses.items():
        current_all_poses.append(pose)
        result=check(current_all_poses,pose,dongtac)
        print('respond result',result)
    break'''
