# K8S部署示例

k8s部署示例yaml文件位于`example`文件夹。

两种方案中执行测试均可用如下语句：

```sh
python TransmissionUnit.test.py -a localhost:30000
```

或者

```sh
kubectl run -i --tty dnet-testunit --image=yindaheng98/dnet-testunit --restart=Never --command -- python TransmissionUnit.test.py -a dnet:8080
kubectl delete po dnet-testunit
```

或部署一堆测试容器

```sh
kubectl apply -f https://raw.githubusercontent.com/yindaheng98/DNet/main/example/dnet-testunit.yaml
```

## [示例一](./distrib)：每个Pod中都包含计算层、传输层和队列系统各一个

示例yaml文件位于`example/distrib`文件夹。

这种部署方式下，每个Pod中都有计算层、传输层和队列系统，虽然简单易维护但是比较占资源。

一共划分为三种计算单元，退出层分别是8、12、16层，每个计算单元有3个备份。

部署：

```sh
URL=https://raw.githubusercontent.com/yindaheng98/DNet/main/example/distrib
kubectl apply -f $URL/dnet-unit-8.yaml
kubectl apply -f $URL/dnet-unit-12.yaml
kubectl apply -f $URL/dnet-unit-16.yaml
kubectl apply -f $URL/dnet.yaml
```

删除：

```sh
kubectl delete svc dnet
kubectl delete svc dnet-unit-8
kubectl delete deploy dnet-unit-8
kubectl delete svc dnet-unit-12
kubectl delete deploy dnet-unit-12
kubectl delete svc dnet-unit-16
kubectl delete deploy dnet-unit-16
```

## [示例二](./cloud-edge)：计算层、传输层和队列系统部署在不同的Pod中

示例yaml文件位于`example/distrib`文件夹。

这种部署方式比较自由，各部分可以根据负载情况动态地调整部署规模，适合于边缘环境下各设备算力不同的情况，代价是需要运维人员关心各层间的关系，维护起来比较复杂。

在本例中，以最常见的端边云三层架构为例维护各层间的关系。testunit视为端系统，边和云系统退出层分别是10、16层。

边系统中每个计算层单元有4个备份，使用`nodeAffinity`限制只能部署于带有标签`dnet-role=edge`的node上；云系统中每个计算层单元有2个备份，使用`nodeAffinity`限制只能部署于带有标签`dnet-role=cloud`的node上

边和云系统的计算层单元之间使用`podAntiAffinity`限制不能部署在同一个node；边和云系统中各有一个传输层单元，它们都各自与一个队列系统共同构成一个Pod。

注：按照开头介绍的那套系统架构，由于每个计算层单元的3个备份都从同一个队列中执行计算任务，因此传输层单元不可以有多个备份

```sh
kubectl label node `kubectl get nodes | grep edge | awk '{print $1}'` dnet-role=edge
kubectl label node `kubectl get nodes | grep -v edge | awk '{print $1}'` dnet-role=cloud
URL=https://raw.githubusercontent.com/yindaheng98/DNet/main/example/cloud-edge
kubectl apply -f $URL/dnet-transmissionunit-10.yaml
kubectl apply -f $URL/dnet-computationunit-10.yaml
kubectl apply -f $URL/dnet-transmissionunit-16.yaml
kubectl apply -f $URL/dnet-computationunit-16.yaml
kubectl apply -f $URL/dnet.yaml
```

删除：

```sh
kubectl delete svc dnet
kubectl delete deploy dnet-computationunit-10
kubectl delete deploy dnet-computationunit-16
kubectl delete svc dnet-unit-10
kubectl delete deploy dnet-transmissionunit-10
kubectl delete svc dnet-unit-10
kubectl delete deploy dnet-transmissionunit-16
```
