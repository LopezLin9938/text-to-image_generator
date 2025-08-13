#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
"""

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def get_user_input():
    """
    获取用户输入的高级交互函数
    """
    print("\n=== 图像生成器 ===")
    while True:
        prompt = input("请输入您想要生成的图像描述 (输入 'quit' 退出): \n> ")
        if prompt.lower() == 'quit':
            return None
        if not prompt.strip():
            print("提示词不能为空，请重新输入。")
            continue
        return prompt

def get_generation_params():
    """
    获取生成参数
    """
    print("\n=== 参数设置 (直接回车使用默认值) ===")
    print("提示：引导系数控制图像与提示词的匹配程度")
    print("       值越高越贴合提示词，但可能过于生硬")
    print("       推荐范围：7-12")
    
    # 获取推理步数
    try:
        steps_input = input("推理步数 (默认50): ").strip()
        num_inference_steps = int(steps_input) if steps_input else 50
    except ValueError:
        num_inference_steps = 50

    # 获取引导系数
    try:
        cfg_input = input("引导系数CFG Scale (推荐7-12，默认7.5): ").strip()
        guidance_scale = float(cfg_input) if cfg_input else 7.5
    except ValueError:
        guidance_scale = 7.5

    # 获取图像尺寸
    try:
        height_input = input("图像高度 (默认512): ").strip()
        height = int(height_input) if height_input else 512
    except ValueError:
        height = 512

    try:
        width_input = input("图像宽度 (默认512): ").strip()
        width = int(width_input) if width_input else 512
    except ValueError:
        width = 512

    return {
        "num_inference_steps": num_inference_steps,
        "guidance_scale": guidance_scale,
        "height": height,
        "width": width
    }

def save_image_safely(image, prompt):
    """
    安全地保存图像文件
    """
    # 创建安全的文件名
    safe_filename = "".join(c for c in prompt[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_filename = safe_filename.replace(" ", "_") + ".png"

    # 确保文件名唯一
    counter = 1
    original_filename = safe_filename
    while os.path.exists(safe_filename):
        name, ext = os.path.splitext(original_filename)
        safe_filename = f"{name}_{counter}{ext}"
        counter += 1

    image.save(safe_filename)
    return safe_filename
