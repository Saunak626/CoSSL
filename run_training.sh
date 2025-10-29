#!/bin/bash
# 训练脚本 - 运行完整的500 epoch训练

echo "=========================================="
echo "开始训练 - CIFAR-10 FixMatch"
echo "=========================================="
echo ""
echo "配置信息："
echo "  - 数据集: CIFAR-10"
echo "  - 模型: WRN-28-2"
echo "  - Epoch数: 500"
echo "  - 标注样本数: ~3500"
echo "  - 未标注样本数: ~10500"
echo "  - 不平衡比例: 150"
echo ""
echo "开始时间: $(date)"
echo "=========================================="
echo ""

# 运行训练
python train_cifar_fix.py \
    --ratio 2 \
    --num_max 1500 \
    --imb_ratio_l 150 \
    --imb_ratio_u 150 \
    --epoch 500 \
    --val-iteration 500 \
    --out ./results/cifar10/fixmatch/baseline/wrn28_N1500_r150_seed1 \
    --manualSeed 1 \
    --gpu 0

echo ""
echo "=========================================="
echo "训练结束时间: $(date)"
echo "=========================================="

