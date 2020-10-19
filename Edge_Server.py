import torch
import os

# Multi-exit Inception v3
from MP_inception_cifar10 import Inception_v3_cifar10


def sendtocloud(info_to_cloud):
    print("hhhhh")
    pass  # to do


def edge_infer(edge_exit, inter_data, start_layer):
    print('Loading model........')
    net = Inception_v3_cifar10()
    print('inception is ready..........')
    SAVE_PATH = os.path.join(os.path.split(__file__)[0], 'multi-exit-inception-v3-cifar10-epoch53.pkl')
    net.load_state_dict(torch.load(SAVE_PATH, map_location='cpu'))

    # thres：各出口退出阈值，共15个出口
    thres = [0.85, 0.90, 0.90, 0.90, 0.90,
             0.90, 0.90, 0.90, 0.90, 0.90,
             0.92, 0.90, 0.90, 0.90, 0.90]
    net.eval()
    # inter_data = inter_data.cuda() # 数据载入GPU

    # inception v3 第二分块推断
    edge_inter_data, outputs = net(inter_data, edge_exit, start_layer)

    # 取得分最大的类别，所为当前任务推断结果
    prob, category = torch.max(outputs.data, 1)

    # 终端出口小于16且置信度低于阈值则发往云端
    if edge_inter_data is not False and prob.tolist()[0] < thres[edge_exit-1]:
        info_to_cloud = {'start_layer': edge_exit + 1,
                         'inter_data': edge_inter_data}
        sendtocloud(info_to_cloud)

    # 向终端返回结果
    return(category)
