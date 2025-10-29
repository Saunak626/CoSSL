# 数据集路径修复总结

## 修复内容

已成功将所有训练脚本中的硬编码数据集路径修改为相对路径。

### 修改的文件列表（共12个文件）

#### CIFAR数据集相关（8个文件）
1. ✅ `train_cifar_fix.py`
2. ✅ `train_cifar_fix_cossl.py`
3. ✅ `train_cifar_fix_crest.py`
4. ✅ `train_cifar_mix.py`
5. ✅ `train_cifar_mix_cossl.py`
6. ✅ `train_cifar_remix.py`
7. ✅ `train_cifar_remix_cossl.py`
8. ✅ `train_cifar_remix_crest.py`

**路径修改：**
- `/BS/databases00/cifar-10` → `./data/cifar-10`
- `/BS/databases00/cifar-100` → `./data/cifar-100`

#### Food-101数据集相关（2个文件）
9. ✅ `train_food_fix.py`
10. ✅ `train_food_fix_cossl.py`

**路径修改：**
- `/BS/yfan/nobackup/food-101/` → `./data/food-101`

#### ImageNet127数据集相关（2个文件）
11. ✅ `train_small_imagenet127_fix.py`
12. ✅ `train_small_imagenet127_fix_cossl.py`

**路径修改：**
- `/BS/yfan/nobackup/ImageNet127_32` → `./data/ImageNet127_32`
- `/BS/yfan/nobackup/ImageNet127_64` → `./data/ImageNet127_64`

## 验证结果

运行 `python3 test_path_fix.py` 验证结果：
```
✅ 所有文件路径修改完成！
```

所有12个训练脚本均已成功修改，不再包含硬编码的 `/BS/` 路径。

## 数据集存储位置

修改后，所有数据集将自动下载到项目根目录下的 `data` 文件夹：

```
CoSSL/
├── data/
│   ├── cifar-10/          # CIFAR-10 数据集
│   ├── cifar-100/         # CIFAR-100 数据集
│   ├── food-101/          # Food-101 数据集
│   ├── ImageNet127_32/    # ImageNet127 32x32
│   └── ImageNet127_64/    # ImageNet127 64x64
├── train_cifar_fix.py
├── train_cifar_fix_cossl.py
└── ...
```

## 下一步操作

### 1. 安装依赖

在运行训练脚本之前，请确保已安装所需的Python依赖：

```bash
# 激活conda环境（根据您的环境名称）
conda activate base  # 或您的环境名称

# 安装依赖
pip install torch==1.0.0 torchvision==0.2.2.post3
pip install numpy progressbar2
```

### 2. 运行测试命令

```bash
python train_cifar_fix.py --ratio 2 --num_max 1500 --imb_ratio_l 150 --imb_ratio_u 150 --epoch 500 --val-iteration 500 --out ./results/cifar10/fixmatch/baseline/wrn28_N1500_r150_seed1 --manualSeed 1 --gpu 0
```

### 3. 预期行为

- 首次运行时，CIFAR-10数据集将自动下载到 `./data/cifar-10/` 目录
- 下载完成后，训练将自动开始
- 后续运行将直接使用已下载的数据集

## 注意事项

1. **数据集下载**：CIFAR-10/100 数据集会自动从官方源下载，Food-101 和 ImageNet127 需要手动准备
2. **磁盘空间**：确保有足够的磁盘空间存储数据集
3. **网络连接**：首次运行需要网络连接以下载数据集
4. **权限问题**：确保对 `./data/` 目录有读写权限

## 问题排查

如果遇到权限错误，请检查：
1. 当前用户对项目目录有写权限
2. WSL2环境下，确保在Linux文件系统中运行（而非 `/mnt/` 挂载的Windows目录）

如果数据集下载失败，可以：
1. 手动下载数据集并放置到对应的 `./data/` 子目录
2. 检查网络连接和防火墙设置

