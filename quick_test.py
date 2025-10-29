#!/usr/bin/env python
"""快速测试RandAugment修复"""

print("测试导入...")
from dataset.randaugment import RandAugment, CutoutDefault
from PIL import Image

print("创建测试图像...")
img = Image.new('RGB', (32, 32), color=(128, 128, 128))

print("测试 RandAugment...")
rand_aug = RandAugment(3, 4)
result = rand_aug(img)
print(f"✅ RandAugment 成功! 输入: {img.size}, 输出: {result.size}")

print("测试 CutoutDefault...")
cutout = CutoutDefault(16)
result = cutout(img)
print(f"✅ CutoutDefault 成功! 输入: {img.size}, 输出: {result.size}")

print("\n✅ 所有测试通过！")

