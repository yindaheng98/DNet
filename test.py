import torch
import time
import os
import pika

# Multi-exit Inception v3
from MP_inception_cifar10 import Inception_v3_cifar10, cifar10
from ComputationUnitClient import ComputationUnitClient

conn_params = pika.ConnectionParameters(host='localhost')
client = ComputationUnitClient(conn_params)

device_exit = 4  # which exit for finishing the first block
testloader, testset = cifar10(batch=1, train=False)  # 加载CIFAR10测试集

# 创建模型
net = Inception_v3_cifar10()
print('Multi-exit Inception is ready.')

# 加载模型
SAVE_PATH = './multi-exit-inception-v3-cifar10-epoch53.pkl'
net.load_state_dict(torch.load(SAVE_PATH, map_location='cpu'))
print('Model is loaded.')

# thres：各出口退出阈值，共15个出口
thres = [0.85, 0.90, 0.90, 0.90,
         0.90, 0.90, 0.90, 0.90,
         0.90, 0.90, 0.92, 0.90,
         0.90, 0.90, 0.90]

if __name__ == "__main__":

    # 测试集推断
    for i, (test_in, test_labels) in enumerate(testloader):
        net.eval()
        # test_in, test_labels = test_in.cuda(), test_labels.cuda()  # 数据载入GPU
        start = time.time()

        # inception v3 第一分块推断
        inter_data, outputs = net(test_in, device_exit)

        # 取得分最大的类别，所为当前任务推断结果
        prob, category = torch.max(outputs.data, 1)

        # 终端出口小于16且置信度低于阈值则发往边缘
        if inter_data is not False and prob.tolist()[0] < thres[device_exit-1]:
            print('Send to RabbitMQ')
            client.call(inter_data, device_exit + 1)
        if i > 10:
            break
    client.wait()