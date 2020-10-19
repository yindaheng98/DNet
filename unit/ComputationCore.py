# -*- coding: utf-8 -*-
# @Author  : Yin Daheng

"""
本文件定义了分支网络组成单元中的计算层核心
"""

import torch


class ComputationCore(object):
    """
    分支网络组成单元中的计算层核心
    """

    def __init__(self, net, thres, exit_layer):
        """
        初始化函数
        @param net: 用于计算的神经网络，类参考MP_inception_cifar10.py文件
        @param thres: 一个数组，每个退出点的退出阈值
        @param commication_unit: 用于接收请求进行的类，必须继承自CommunicationUnit类
        @param exit_layer: 指定该计算层核心在哪神经网络的哪一层退出
        """
        self.net = net
        self.thres = thres
        self.exit_layer = exit_layer

    def compute(self, x, start_layer):
        """
        执行一次计算
        @param x: 输入矩阵
        @param start_layer: 计算起始层数
        @return 返回值有二：
        第一个值是是否识别成功，如果识别成功，则后面跟识别结果；
        否则跟tuple(<下一层输入x>，<下一个Unit的起始层start_layer=exit_layer+1>)
        """
        return self._compute(x, start_layer, self.exit_layer)


    def _compute(self, x, start_layer, exit_layer):
        """
        执行一次计算
        @param x: 输入矩阵
        @param start_layer: 计算起始层数
        @param exit_layer: 计算截止层数
        @return 返回值有二：
        第一个值是是否识别成功，如果识别成功，则后面跟识别结果；
        否则跟tuple(<下一层输入x>，<下一个Unit的起始层start_layer=exit_layer+1>)
        """

        # 执行推断
        x, outputs = self.net(x, exit_layer, start_layer)
        # TODO: 如果需要更加通用的计算层，最好研究出一个抽象的DDNN网络计算单元（就像torch.nn.Module那样）

        # 取得分最大的类别，所为当前任务推断结果
        prob, category = torch.max(outputs.data, 1)

        # 终端出口小于16且置信度低于阈值则发往云端
        if x is not False and prob.tolist()[0] < self.thres[exit_layer-1]:
            return False, (x, exit_layer + 1)
        # 否则返回识别结果
        return True, category
