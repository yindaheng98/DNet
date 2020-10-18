# -*- coding: utf-8 -*-
# @Author  : Yin Daheng

"""
本文件定义了分支网络组成单元中的计算层队列接口
"""
import abc
import asyncio

class ComputationRequest(metaclass=abc.ABCMeta):
    """
    此类表示一个由传输层输入到计算层的计算请求
    此类是一个抽象类，使用前请先实现fetchNext和response方法
    """
    def __init__(self, x, start_layer, exit_layer):
        self.x = x
        self.start_layer = start_layer
        self.exit_layer = exit_layer

    async def put_result(self, ok, result):
        """
        此方法在ComputationUnit.start的循环中被调用，用于处理ComputationUnit.compute的输出结果
        输入参数同ComputationUnit.compute的返回值
        """
        if not ok:
            result = await self.fetchNext(
                result.x, result.start_layer, result.exit_layer)
        return await self.response(result)

    @abc.abstractmethod
    async def fetchNext(self, x, start_layer, exit_layer):
        """
        将数据输入到下一个神经网络单元中，执行计算并接受返回值
        输入参数同ComputationUnit.compute的输入参数
        由于后续神经网络必然返回一个识别结果，因此返回值格式同ComputationUnit.compute中识别成功时的识别结果
        """
        pass

    @abc.abstractmethod
    async def response(self, category):
        """
        在本层或者后续层识别成功后将识别结果发送回请求方
        @param category: 格式同ComputationUnit.compute中识别成功时的识别结果
        """
        pass


class ComputationQueue(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def pop(self):
        """返回值必须是一个"""
        pass