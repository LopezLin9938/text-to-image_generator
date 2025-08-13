#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stable Diffusion 图像生成器
作者: chenhong.lin
"""

import sys
from model_manager import ModelManager
from image_generator import ImageGenerator
from utils import get_user_input, get_generation_params, save_image_safely


def main():
    """主程序入口"""
    print("=== Stable Diffusion 图像生成器 ===")
    print("作者: ch.l")
    print("=" * 40)

    # 初始化模型管理器
    model_manager = ModelManager()

    # 选择并加载模型
    pipeline = model_manager.load_selected_model()
    if pipeline is None:
        print("模型加载失败，程序退出。")
        sys.exit(1)

    # 初始化图像生成器
    generator = ImageGenerator(pipeline)

    # 主循环
    while True:
        user_prompt = get_user_input()
        if user_prompt is None:
            print("程序已取消。")
            break

        # 获取生成参数
        params = get_generation_params()

        try:
            print(f"正在生成图像: {user_prompt}")
            print(f'使用参数: {params}')

            # 生成图像
            generated_image = generator.generate(user_prompt, params)

            # 显示图像
            generator.display_image(generated_image, user_prompt)

            # 保存图像
            filename = save_image_safely(generated_image, user_prompt)
            print(f'图像已保存为: {filename}')

        except Exception as e:
            print(f"生成图像时出错: {e}")
            continue


if __name__ == "__main__":
    main()
