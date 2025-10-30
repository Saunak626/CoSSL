#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
训练历史查看和可视化工具

用法:
    # 查看最近20个epoch的统计
    python view_training_history.py --log ./results/cifar10/fixmatch/baseline/wrn28_N1500_r150_seed1/log.txt

    # 查看所有epoch
    python view_training_history.py --log ./results/cifar10/fixmatch/baseline/wrn28_N1500_r150_seed1/log.txt --all

    # 生成可视化图表
    python view_training_history.py --log ./results/cifar10/fixmatch/baseline/wrn28_N1500_r150_seed1/log.txt --plot

    # 比较多个训练日志
    python view_training_history.py --log log1.txt log2.txt --plot
"""

import argparse
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
from pathlib import Path


def parse_log_file(log_path):
    """解析log.txt文件"""
    if not os.path.exists(log_path):
        print(f"错误: 找不到日志文件 {log_path}")
        return None
    
    data = {
        'epoch': [],
        'train_loss': [],
        'train_loss_x': [],
        'train_loss_u': [],
        'mask': [],
        'total_acc': [],
        'used_acc': [],
        'test_loss': [],
        'test_acc': [],
        'test_gm': []
    }
    
    with open(log_path, 'r') as f:
        lines = f.readlines()

    # 跳过标题行
    epoch_num = 1
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 9:
            continue

        try:
            # 日志文件没有epoch列，需要手动计数
            data['epoch'].append(epoch_num)
            data['train_loss'].append(float(parts[0]))
            data['train_loss_x'].append(float(parts[1]))
            data['train_loss_u'].append(float(parts[2]))
            data['mask'].append(float(parts[3]))
            data['total_acc'].append(float(parts[4]))
            data['used_acc'].append(float(parts[5]))
            data['test_loss'].append(float(parts[6]))
            data['test_acc'].append(float(parts[7]))
            data['test_gm'].append(float(parts[8]))
            epoch_num += 1
        except (ValueError, IndexError):
            continue
    
    return data


def print_statistics(data, last_n=20, show_all=False):
    """打印训练统计信息"""
    if not data or len(data['epoch']) == 0:
        print("没有可用的数据")
        return
    
    total_epochs = len(data['epoch'])
    
    if show_all:
        start_idx = 0
        print(f"\n{'='*80}")
        print(f"训练历史统计 - 所有 {total_epochs} 个epoch")
        print(f"{'='*80}\n")
    else:
        start_idx = max(0, total_epochs - last_n)
        print(f"\n{'='*80}")
        print(f"训练历史统计 - 最近 {min(last_n, total_epochs)} 个epoch")
        print(f"{'='*80}\n")
    
    # 打印表头
    print(f"{'Epoch':>6} | {'Train Loss':>10} | {'Loss_x':>8} | {'Loss_u':>8} | "
          f"{'Mask':>6} | {'Use_acc':>8} | {'Test Acc':>9} | {'Test GM':>8}")
    print(f"{'-'*80}")
    
    # 打印数据
    for i in range(start_idx, total_epochs):
        print(f"{data['epoch'][i]:>6} | {data['train_loss'][i]:>10.4f} | "
              f"{data['train_loss_x'][i]:>8.4f} | {data['train_loss_u'][i]:>8.4f} | "
              f"{data['mask'][i]:>6.4f} | {data['used_acc'][i]:>8.4f} | "
              f"{data['test_acc'][i]:>9.4f} | {data['test_gm'][i]:>8.4f}")
    
    # 打印摘要统计
    print(f"\n{'='*80}")
    print(f"摘要统计 (最近 {min(last_n, total_epochs)} 个epoch)")
    print(f"{'='*80}")
    
    recent_data = {k: v[start_idx:] for k, v in data.items()}
    
    print(f"\n训练指标:")
    print(f"  平均训练损失:     {np.mean(recent_data['train_loss']):.4f} ± {np.std(recent_data['train_loss']):.4f}")
    print(f"  平均标签损失:     {np.mean(recent_data['train_loss_x']):.4f} ± {np.std(recent_data['train_loss_x']):.4f}")
    print(f"  平均无标签损失:   {np.mean(recent_data['train_loss_u']):.4f} ± {np.std(recent_data['train_loss_u']):.4f}")
    print(f"  平均Mask率:       {np.mean(recent_data['mask']):.4f} ± {np.std(recent_data['mask']):.4f}")
    print(f"  平均伪标签准确率: {np.mean(recent_data['used_acc']):.4f} ± {np.std(recent_data['used_acc']):.4f}")
    
    print(f"\n测试指标:")
    print(f"  平均测试准确率:   {np.mean(recent_data['test_acc']):.4f} ± {np.std(recent_data['test_acc']):.4f}")
    print(f"  最佳测试准确率:   {np.max(recent_data['test_acc']):.4f} (Epoch {data['epoch'][start_idx + np.argmax(recent_data['test_acc'])]})")
    print(f"  平均几何平均(GM): {np.mean(recent_data['test_gm']):.4f} ± {np.std(recent_data['test_gm']):.4f}")
    print(f"  最佳GM:           {np.max(recent_data['test_gm']):.4f} (Epoch {data['epoch'][start_idx + np.argmax(recent_data['test_gm'])]})")
    print()


def plot_training_curves(log_paths, output_dir=None):
    """绘制训练曲线"""
    if output_dir is None:
        output_dir = os.path.dirname(log_paths[0]) if len(log_paths) == 1 else '.'
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 解析所有日志文件
    all_data = []
    labels = []
    for log_path in log_paths:
        data = parse_log_file(log_path)
        if data:
            all_data.append(data)
            # 使用目录名作为标签
            label = os.path.basename(os.path.dirname(log_path))
            labels.append(label)
    
    if not all_data:
        print("没有可用的数据用于绘图")
        return
    
    # 创建图表
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('训练历史曲线', fontsize=16, fontproperties='SimHei')
    
    # 1. 训练损失
    ax = axes[0, 0]
    for data, label in zip(all_data, labels):
        ax.plot(data['epoch'], data['train_loss'], label=label, linewidth=2)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('训练损失')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. 标签损失 vs 无标签损失
    ax = axes[0, 1]
    for data, label in zip(all_data, labels):
        ax.plot(data['epoch'], data['train_loss_x'], label=f'{label} (labeled)', linewidth=2, linestyle='-')
        ax.plot(data['epoch'], data['train_loss_u'], label=f'{label} (unlabeled)', linewidth=2, linestyle='--')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('标签损失 vs 无标签损失')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Mask率
    ax = axes[0, 2]
    for data, label in zip(all_data, labels):
        ax.plot(data['epoch'], data['mask'], label=label, linewidth=2)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Mask Rate')
    ax.set_title('伪标签选择率')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. 伪标签准确率
    ax = axes[1, 0]
    for data, label in zip(all_data, labels):
        ax.plot(data['epoch'], data['used_acc'], label=label, linewidth=2)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Accuracy')
    ax.set_title('伪标签准确率')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 5. 测试准确率
    ax = axes[1, 1]
    for data, label in zip(all_data, labels):
        ax.plot(data['epoch'], data['test_acc'], label=label, linewidth=2)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('测试准确率')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 6. 几何平均(GM)
    ax = axes[1, 2]
    for data, label in zip(all_data, labels):
        ax.plot(data['epoch'], data['test_gm'], label=label, linewidth=2)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('GM')
    ax.set_title('几何平均 (类别平衡性)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图表
    output_path = os.path.join(output_dir, 'training_curves.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✅ 训练曲线已保存到: {output_path}")
    
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='查看和可视化训练历史')
    parser.add_argument('--log', nargs='+', required=True, help='日志文件路径 (可以指定多个)')
    parser.add_argument('--all', action='store_true', help='显示所有epoch (默认只显示最近20个)')
    parser.add_argument('--last', type=int, default=20, help='显示最近N个epoch (默认: 20)')
    parser.add_argument('--plot', action='store_true', help='生成可视化图表')
    parser.add_argument('--output', type=str, help='图表输出目录 (默认: 日志文件所在目录)')
    
    args = parser.parse_args()
    
    # 打印统计信息
    for log_path in args.log:
        print(f"\n{'#'*80}")
        print(f"# 日志文件: {log_path}")
        print(f"{'#'*80}")
        
        data = parse_log_file(log_path)
        if data:
            print_statistics(data, last_n=args.last, show_all=args.all)
    
    # 生成图表
    if args.plot:
        plot_training_curves(args.log, output_dir=args.output)


if __name__ == '__main__':
    main()

