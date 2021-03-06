import os
# 选择使用0号卡
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from paddlex.det import transforms
import paddlex as pdx

# 下载和解压垃圾分拣数据集
garbage_dataset = 'https://bj.bcebos.com/paddlex/datasets/garbage_ins_det.tar.gz'
pdx.utils.download_and_decompress(garbage_dataset, path='./')

# 定义训练和验证时的transforms
train_transforms = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.Normalize(),
    transforms.ResizeByShort(short_size=800, max_size=1333),
    transforms.Padding(coarsest_stride=32)
])

eval_transforms = transforms.Compose([
    transforms.Normalize(),
    transforms.ResizeByShort(short_size=800, max_size=1333),
    transforms.Padding(coarsest_stride=32)
])

# 定义训练和验证所用的数据集
train_dataset = pdx.datasets.CocoDetection(
    data_dir='garbage_ins_det/JPEGImages',
    ann_file='garbage_ins_det/train.json',
    transforms=train_transforms,
    shuffle=True)
eval_dataset = pdx.datasets.CocoDetection(
    data_dir='garbage_ins_det/JPEGImages',
    ann_file='garbage_ins_det/val.json',
    transforms=eval_transforms)

# 初始化模型，并进行训练
# 可使用VisualDL查看训练指标
# VisualDL启动方式: visualdl --logdir output/mask_rcnn_r50_fpn/vdl_log --port 8001
# 浏览器打开 https://0.0.0.0:8001即可
# 其中0.0.0.0为本机访问，如为远程服务, 改成相应机器IP
# num_classes 需要设置为包含背景类的类别数，即: 目标类别数量 + 1
num_classes = len(train_dataset.labels) + 1
model = pdx.det.MaskRCNN(num_classes=num_classes)
model.train(
    num_epochs=12,
    train_dataset=train_dataset,
    train_batch_size=1,
    eval_dataset=eval_dataset,
    learning_rate=0.00125,
    lr_decay_epochs=[8, 11],
    save_dir='output/mask_rcnn_r50_fpn',
    use_vdl=True)
