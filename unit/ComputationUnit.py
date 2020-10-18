# -*- coding: utf-8 -*-
# @Author  : Yin Daheng

"""
本文件定义了分支网络组成单元中的计算层
"""

import torch


class ComputationUnit:
    """
    分支网络组成单元中的计算层
    """
    def __init__(self, net, thres):
        """
        初始化函数
        @param net: 要使用的网络，类参考MP_inception_cifar10.py文件
        @param thres: 一个数组，每个退出点的退出阈值
        """
        self.net = net
        self.thres = thres

    def compute(self, x, start_layer, exit_layer):
        """
        执行一次计算
        @param x: 输入矩阵
        @param start_layer: 计算起始层数
        @param exit_layer: 计算截止层数
        @return 第一个值是是否识别成功，如果识别成功，则后面跟识别结果；否则跟(下一层输入，下一个Unit的起始层)
        """

        # 执行推断
        x, outputs = self.net(x, exit_layer, start_layer)
        # TODO: 如果需要更加通用的计算层，最好自定义一个抽象的网络单元结构（就像torch.nn.Module那样）

        # 取得分最大的类别，所为当前任务推断结果
        prob, category = torch.max(outputs.data, 1)

        # 终端出口小于16且置信度低于阈值则发往云端
        if x is not False and prob.tolist()[0] < self.thres[exit_layer-1]:
            return False, (x, exit_layer + 1)
        # 否则返回识别结果
        return True, category
