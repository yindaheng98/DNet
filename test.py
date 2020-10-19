import torch
import os
from Device.MP_inception_cifar10 import Inception_v3_cifar10, cifar10
from Edge_Server import edge_infer

if __name__ == '__main__':
    print('Loading model........')
    net = Inception_v3_cifar10()
    print('inception is ready..........')
    SAVE_PATH = os.path.join(os.path.split(__file__)[0],
                             'Device/multi-exit-inception-v3-cifar10-epoch53.pkl')

    net.load_state_dict(torch.load(SAVE_PATH, map_location='cpu'))

    edge_exit = 10

    """以下代码为测试用"""

    device_exit = 4  # which exit for finishing the first block
    testloader, testset = cifar10(batch=1, train=False)  # 加载CIFAR10测试集

    # thres：各出口退出阈值，共15个出口
    thres = [0.85, 0.90, 0.90, 0.90, 0.90,
             0.90, 0.90, 0.90, 0.90, 0.90,
             0.92, 0.90, 0.90, 0.90, 0.90]

    # 测试集推断
    for i, (test_in, test_labels) in enumerate(testloader):
        net.eval()
        # test_in, test_labels = test_in.cuda(), test_labels.cuda()  # 数据载入GPU

        # inception v3 第一分块推断
        inter_data, outputs = net(test_in, device_exit)

        # 取得分最大的类别，所为当前任务推断结果
        prob, category = torch.max(outputs.data, 1)

        # 终端出口小于16且置信度低于阈值则发往边缘
        if inter_data is not False and prob.tolist()[0] < thres[device_exit-1]:
            print('prob=%f<%f, Send to RabbitMQ' %
                  (prob.tolist()[0], thres[device_exit-1]))
            edge_infer(edge_exit, inter_data, device_exit)
        else:
            print('prob=%f>%f, category=%s' %
                  (prob.tolist()[0], thres[device_exit-1], category))
