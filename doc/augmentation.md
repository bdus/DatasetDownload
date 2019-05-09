[TOC]



# 1. DL中常见的数据增强方法

- Color Jittering：对颜色的数据增强：图像亮度、饱和度、对比度变化（此处对色彩抖动的理解不知是否得当）；
- PCA  Jittering：首先按照RGB三个颜色通道计算均值和标准差，再在整个训练集上计算协方差矩阵，进行特征分解，得到特征向量和特征值，用来做PCA Jittering；
- Random Scale：尺度变换；
- Random Crop：采用随机图像差值方式，对图像进行裁剪、缩放；包括Scale Jittering方法（VGG及ResNet模型使用）或者尺度和长宽比增强变换；
- Horizontal/Vertical Flip：水平/垂直翻转；
- Shift：平移变换；
- Rotation/Reflection：旋转/仿射变换；
- Noise：高斯噪声、模糊处理；
- Label Shuffle：类别不平衡数据的增广；





# 2. 行为识别中的增强方法



使用了尺寸裁剪、随机反转：

[ECO代码](https://github.com/mzolfaghari/ECO-pytorch/blob/b175e7c2449d83af76fbaeebe8a9aa0f44c17972/models.py#L468)



```python
def get_augmentation(self):
    if self.modality == 'RGB':
        return torchvision.transforms.Compose([GroupMultiScaleCrop(self.input_size, [1, .875, .75, .66]),
                                                GroupRandomHorizontalFlip(is_flow=False)])
    elif self.modality == 'Flow':
        return torchvision.transforms.Compose([GroupMultiScaleCrop(self.input_size, [1, .875, .75]),
                                                GroupRandomHorizontalFlip(is_flow=True)])
    elif self.modality == 'RGBDiff':
        return torchvision.transforms.Compose([GroupMultiScaleCrop(self.input_size, [1, .875, .75]),
                                                GroupRandomHorizontalFlip(is_flow=False)])
```

