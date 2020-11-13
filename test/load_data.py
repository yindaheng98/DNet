import torchvision
testset = torchvision.datasets.CIFAR10(root='./data/CIFAR10', train=False, download=True)