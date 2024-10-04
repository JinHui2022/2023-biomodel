# 小鼠CA3脑区涟漪状动作电位发放的模拟
该项目为2023年USTC生物系统数学建模课程的小组作业，主要思路来源于[Hippocampal sharp wave-ripples and the associated sequence replay emerge from structured synaptic interactions in a network model of area CA3](https://elifesciences.org/articles/71850)，在此基础上进行一定的创新。

## 项目框架
该项目可以分为模型建立和模型分析两个部分，有关文件存储在project文件夹中。而建模得到的分析结果存储在result文件夹中。在建模过程中有关的参考文献放在reference文件夹中。此外，在该项目开展过程中开展了数次组会，部分工作记录对于了解本项目的原理和逻辑框架式比较重要的，这部分文件被存储在meeting文件夹中。

### project
模型建立有关函数主要为下面三个函数：
* generate_spike_trains.py：让模拟小鼠通过通道，根据位置细胞和非位置的兴奋规律，模拟出两类PC细胞（位置和非位置）平均状态下的spike train
* network_learn.py：利用spike train，基于给定的STDP规则，进行神经元突触权重矩阵的学习
* network_simulate.py：通过突触权重矩阵，模拟出神经元在小鼠通过通道后，神经元在静息状态下随时间的兴奋情况

模型分析有关的函数大致有：

* wmx_modify.py：提供了本项目进行权重矩阵调整有关的函数

此外，还有部分辅助文件：
* plots.py：提供本项目所有作图有关的支持
* parameter.py：存储本项目使用的可以泛化的参数
* classes.py：存储本项目使用的各种类
* file_management：负责数据的存储和文件的读取

## 项目特色
本项目使用全新的库函数brainpy编写了有关程序，代码更加浅显易懂，也便于使用者进行参数的调整。

此外对于原论文为了解决的replay现象一旦发生必然到头的现象，我们在查阅了文献后，发现在网络模拟中加入STD现象可以帮助replay提前终止，从而与真实的神经网络行为更为接近。
