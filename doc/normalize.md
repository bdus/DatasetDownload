[TOC]



# 1. 归一化[^1]

在深度学习模型训练和inference的时候，自然图像帧往往不直接输入模型，而是首先经过归一化。

##  1.1 作用

归一化的功能举例如下：

1. 统一量纲：消去不同特征维度之间的量纲差异
2. 数值方便：归一化能够避免一些数值问题，方便数据处理
3. 方便梯度求解：当特征不同维度归一化之后，整个特征空间、输入空间也归一化了，能够帮助梯度求解算法收敛
4. 避免神经元饱和：当使用如softmax这样的激活函数时，如果数值不在线性区工作，而是在边缘的非线性区，会导致梯度很小，反向传播出现梯度弥散

## 1.2 类型

1. 线性归一化

$$
x^{\prime} = \frac{x-min(x)}{max(x) - min(x)}
$$

​	适用范围：比较适用在数值比较集中的情况。

​	缺点：如果 max 和 min 不稳定，很容易使得归一化结果不稳定，使得后续使用效果也不稳定。

2. 标准差标准化

$$
x^{\prime} = \frac{x-\mu}{\sigma}
$$

​	含义：经过处理的数据符合标准正态分布，即均值为 0，标准差为 1 其中 $ \mu $ 为所有样本数据的均值，$ \sigma $ 为所有样本数据的标准差。

3. 非线性归一化

   适用范围：经常用在数据分化比较大的场景，有些数值很大，有些很小。通过一些数学函数，将原始值进行映射。该方法包括 $ log $、指数，正切等。

## 1.3 拓展阅读

1. Normalization 详解[[artical]](https://zhuanlan.zhihu.com/p/33173246)

2. [[Normalization]](https://blog.csdn.net/yimingsilence/article/details/80322926#)





# 2. 实现

行为识别中输入的图像单独来看都是一帧一帧的RGB图像、或者是光流图像

对于uint8类型的RGB图像，只需要对三个通道的数值分别减去三个通道的均值即可，保证输入是零均值的，对于float类型的数据也一样。

[ref : ](https://github.com/mzolfaghari/ECO-pytorch/blob/b175e7c2449d83af76fbaeebe8a9aa0f44c17972/transforms.py#L63)

```python
class GroupNormalize(object):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def __call__(self, tensor):
        rep_mean = self.mean * (tensor.size()[0]//len(self.mean))
        rep_std = self.std * (tensor.size()[0]//len(self.std))

        # TODO: make efficient
        for t, m, s in zip(tensor, rep_mean, rep_std):
            t.sub_(m).div_(s)

        return tensor
    

```

[para : ](https://github.com/mzolfaghari/ECO-pytorch/blob/b175e7c2449d83af76fbaeebe8a9aa0f44c17972/models.py#L125)

```python

        elif base_model == 'ECO':
            import tf_model_zoo
            self.base_model = getattr(tf_model_zoo, #...
            self.base_model.last_layer_name = 'fc_final'
            self.input_size = 224
            self.input_mean = [104, 117, 128]
            self.input_std = [1]
```







# reference

[^1]: https://github.com/scutan90/DeepLearning-500-questions/tree/master/ch03_%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E5%9F%BA%E7%A1%80 “深度学习500问3.6 归一化”

 