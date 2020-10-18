# -*- coding: utf-8 -*-
# @Author  : Yin Daheng

"""
本文件定义了在分支网络组成单元中的计算层传输计算请求的队列接口
"""
import abc


class ComputationRequest(metaclass=abc.ABCMeta):
    """
    此类表示一个由传输层输入到计算层的计算请求接口
    此类是一个抽象类，使用前请先实现push_result方法
    """

    def __init__(self, x, start_layer, exit_layer):
        self.x = x
        self.start_layer = start_layer
        self.exit_layer = exit_layer

    @abc.abstractmethod
    def push_result(self, ok, result):
        """
        此方法在ComputationUnit.start的循环中被调用
        用于将ComputationUnit.compute的输出结果传回传输层
        输入参数同ComputationUnit.compute的返回值
        """
        pass


class ComputationQueue(metaclass=abc.ABCMeta):
    """
    此类表示一个向计算层传输计算请求的计算队列接口
    """
    @abc.abstractmethod
    def pop(self):
        """
        此方法在ComputationUnit.start的循环中被调用
        用于从计算队列中阻塞式地取出一个计算请求
        返回值必须是一个ComputationRequest
        """
        pass
