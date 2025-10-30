#!/usr/bin/env python3
"""
批量优化训练脚本的进度条输出
移除冗余时间信息，添加打印间隔控制
"""

import re
import sys
from pathlib import Path

def optimize_annotate_function(content):
    """优化annotate函数中的进度条"""
    # 查找 bar = Bar('Annotating 模式
    pattern = r"(    bar = Bar\('Annotating[^']+', max=len\(loader\)\)\n)"
    replacement = r"\1    \n    # 打印间隔：每N个batch打印一次\n    print_interval = max(1, len(loader) // 10)  # 每个epoch打印约10次\n"
    
    content = re.sub(pattern, replacement, content)
    
    # 优化打印逻辑 - 查找annotate函数中的bar.suffix
    # 这个比较复杂，需要手动处理
    return content

def check_file_status(filepath):
    """检查文件是否已经优化过"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有打印间隔控制
    has_print_interval = 'print_interval = max(1,' in content
    has_epoch_summary = '打印epoch统计信息' in content or '打印验证集统计信息' in content
    has_gm_fix = 'isinstance(GM, torch.Tensor)' in content
    
    return {
        'has_print_interval': has_print_interval,
        'has_epoch_summary': has_epoch_summary,
        'has_gm_fix': has_gm_fix,
        'optimized': has_print_interval and has_epoch_summary
    }

def main():
    """主函数"""
    files_to_check = [
        'train_cifar_fix_cossl.py',
        'train_cifar_mix.py',
        'train_cifar_mix_cossl.py',
        'train_cifar_remix.py',
        'train_cifar_remix_cossl.py',
        'train_cifar_remix_crest.py',
        'train_food_fix.py',
        'train_food_fix_cossl.py',
        'train_small_imagenet127_fix.py',
        'train_small_imagenet127_fix_cossl.py',
    ]
    
    print("=" * 80)
    print("进度条优化状态检查")
    print("=" * 80)
    
    optimized_count = 0
    partial_count = 0
    not_optimized_count = 0
    
    for filename in files_to_check:
        filepath = Path(filename)
        if not filepath.exists():
            print(f"❌ {filename:45s} - 文件不存在")
            continue
        
        status = check_file_status(filepath)
        
        if status['optimized']:
            print(f"✅ {filename:45s} - 已完全优化")
            optimized_count += 1
        elif status['has_print_interval']:
            print(f"⏳ {filename:45s} - 部分优化 (打印间隔: {status['has_print_interval']}, "
                  f"Epoch摘要: {status['has_epoch_summary']}, GM修复: {status['has_gm_fix']})")
            partial_count += 1
        else:
            print(f"📝 {filename:45s} - 未优化")
            not_optimized_count += 1
    
    print("=" * 80)
    print(f"统计: ✅ 已优化: {optimized_count} | ⏳ 部分优化: {partial_count} | 📝 未优化: {not_optimized_count}")
    print("=" * 80)
    
    return optimized_count, partial_count, not_optimized_count

if __name__ == '__main__':
    main()

