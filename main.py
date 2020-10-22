import torch
import pika
import os
from MP_inception_cifar10 import Inception_v3_cifar10
from unit.ComputationCore import ComputationCore
from unit.ComputationUnit import ComputationUnit

conn_params = pika.ConnectionParameters(host='192.168.1.2')

print('Loading model........')
net = Inception_v3_cifar10()
print('Inception is ready..........')
SAVE_PATH = os.path.join(os.path.split(__file__)[0], 'multi-exit-inception-v3-cifar10-epoch53.pkl')
net.load_state_dict(torch.load(SAVE_PATH, map_location='cpu'))

# thres：各出口退出阈值，共15个出口
thres = [0.85, 0.90, 0.90, 0.90, 0.90,
         0.90, 0.90, 0.90, 0.90, 0.90,
         0.92, 0.90, 0.90, 0.90, 0.90]
cu = ComputationUnit(ComputationCore(net, thres, 10), conn_params)
cu.start()