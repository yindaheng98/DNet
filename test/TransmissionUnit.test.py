# -*- coding: utf-8 -*-
# @Author  : Yin Daheng

"""
本文件用于测试分支网络组成单元中的计算层核心
"""
import torch
import time
import os
import sys
sys.path.append(os.path.split(__file__)[0])

# Multi-exit Inception v3
from MP_inception_cifar10_Device import Inception_v3_cifar10, cifar10

sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])
from TransmissionUnit.unit.TransmissionUnitTestClient import TransmissionUnitTestClient

import optparse
parser = optparse.OptionParser()
parser.add_option('-a', '--address', dest='address',
                    type='string', help='要测试服务器地址和端口', default='localhost:8080')
parser.add_option('-n', '--number', dest='number',
                    type='int', help='测试多少张图片', default='100')
parser.add_option('-e', '--exit', dest='exit',
                    type='int', help='在第几层退出', default='4')
options, _ = parser.parse_args()
print("对%s进行%d张图片的测试，在第%d层退出"%(options.address, options.number, options.exit))

client = TransmissionUnitTestClient(options.address)

device_exit = options.exit  # which exit for finishing the first block
testloader, testset = cifar10(batch=1, train=False)  # 加载CIFAR10测试集

# 创建模型
net = Inception_v3_cifar10()
print('Multi-exit Inception is ready.')

# 加载模型
SAVE_PATH = os.path.join(os.path.split(__file__)[0], '../ComputationUnit/multi-exit-inception-v3-cifar10-epoch53.pkl')
net.load_state_dict(torch.load(SAVE_PATH, map_location='cpu'))
print('Model is loaded.')

# thres：各出口退出阈值，共15个出口
thres = [0.85, 0.90, 0.90, 0.90,
         0.90, 0.90, 0.90, 0.90,
         0.90, 0.90, 0.92, 0.90,
         0.90, 0.90, 0.90]

if __name__ == "__main__":
    start_time = time.time()

    # 测试集推断
    for i, (test_in, test_labels) in enumerate(testloader):
        net.eval()

        # inception v3 第一分块推断
        inter_data, outputs = net(test_in, device_exit)

        # 取得分最大的类别，所为当前任务推断结果
        prob, category = torch.max(outputs.data, 1)

        # 终端出口小于16且置信度低于阈值则发往边缘
        if inter_data is False:
            print("inter_data is False, don't send, category=%s"%category)
        elif prob.tolist()[0] < thres[device_exit-1]:
            print('prob=%f<%f, Send to %s' % (prob.tolist()[0], thres[device_exit-1], options.address))
            client.call(inter_data, device_exit)
        else:
            print('prob=%f>%f, category=%s' % (prob.tolist()[0], thres[device_exit-1], category))
        if i > options.number:
            break
    
    end_time = time.time()
    print("总结")
    print("测试开始于%s"%time.asctime(time.localtime(start_time)))
    print("测试结束于%s"%time.asctime(time.localtime(end_time)))
    print("测试耗时%.4f秒"%(end_time-start_time))
    print("测试次数%d"%options.number)
    print("单个测试平均用时%.4f秒"%((end_time-start_time)/options.number))