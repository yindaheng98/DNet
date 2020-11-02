# DNet：一种级联的DDNN推断框架

## 整体结构

## 单元结构

* 计算层（包括神经网络+分支退出阈值）
  * 单线程执行，不允许抢占（避免GPU换入换出耗时）
  * 输入前一个单元传来的矩阵和起始层数
  * 执行神经网络计算，比较退出阈值
  * 输出
    * 阈值满足要求时：识别结果
    * 阈值不满足要求时：下一个单元的输入
* 传输层（包括下一个单元的请求地址）
  * 并发，需要端口复用
  * 接收前一个单元传来的矩阵和起始层数
  * 输入到计算层执行计算，等待计算结果
  * 输出
    * 如果计算层返回了识别结果，则返回
    * 如果计算层返回了下一个单元的输入，则请求下一个单元，等待并返回下一个单元的返回值
  * 计算层输出计算结果后立即开始计算下一个输入
* 中间层（基于队列的RPC系统）
  * 负责计算层和传输层之间的通信
  * 此层的存在只是因为多语言编程的需要，如果计算层和传输层由同种语言实现，则不需要传输层
  * 传输层将收到的数据传到中间层队列中，并等待返回
  * 计算层从中间层队列中接收数据，执行计算，返回结果

## 运行计算层单元

```shell
$ python ComputationUnit -h
Usage: ComputationUnit [options]

Options:
  -h, --help            show this help message and exit
  -a ADDRESS, --address=ADDRESS
                        要连接的RabbitMQ服务器地址和端口
  -q QUEUENAME, --queuename=QUEUENAME
                        接收计算请求的RabbitMQ队列名
  -e EXITLAYER, --exitlayer=EXITLAYER
                        出口位置
```

示例

```shell
python ComputationUnit -a 192.168.1.2 -q q8 -e 8 # 连到192.168.1.2、队列名q8、从第8层退出
python ComputationUnit -a 192.168.1.2 -q q12 -e 12 # 连到192.168.1.2、队列名q12、从第12层退出
python ComputationUnit -a 192.168.1.2 -q q16 -e 16 # 连到192.168.1.2、队列名q16、从第16层退出
```

## 运行传输层单元

```shell
$ cd TransmissionUnit
$ npm run start -- -h

Usage: index [options]

Options:
  -V, --version                          output the version number
  -l, --listen-address <listen-address>  gRPC服务器将要监听的IP地址和端口 (default: "0.0.0.0:8080")
  -a, --amqp-address <amqp-address>      与计算层通讯的RabbitMQ服务器接口地址 (default: "amqp://localhost")
  -q, --queue-name <queue-name>          与计算层通讯的RabbitMQ队列名称 (default: "ComputationQueue")
  -n, --next-address <next-address>      如果此服务器运行在边缘，此处指定下一套模型（云端）的gRPC服务器位置 (default: "")
  -h, --help                             display help for command
```

示例

```shell
npm run start -- -l 0.0.0.0:8082 -a amqp://192.168.1.2 -q q16
npm run start -- -l 0.0.0.0:8081 -a amqp://192.168.1.2 -q q12 -n localhost:8082
npm run start -- -l 0.0.0.0:8080 -a amqp://192.168.1.2 -q q8 -n localhost:8081
```