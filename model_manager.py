#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型管理模块
"""

import torch
from diffusers import DiffusionPipeline

class ModelManager:
    """模型管理器"""
    
    def __init__(self):
        self.models = {
            "1": ("stable-diffusion-v1-5/stable-diffusion-v1-5", "Stable Diffusion 1.5"),
            "2": ("stabilityai/stable-diffusion-2-1", "Stable Diffusion 2.1"),
            "3": ("prompthero/openjourney", "Open Journey (艺术风格)"),
            "4": ("runwayml/stable-diffusion-v1-5", "RunwayML SD 1.5"),
            "5": ("stabilityai/stable-diffusion-xl-base-1.0", "Stable Diffusion XL")
        }
    
    def select_model(self):
        """选择模型"""
        print("=== 模型选择 ===")
        for key, (model_id, model_name) in self.models.items():
            print(f"{key}. {model_name}")

        while True:
            choice = input("请选择模型 (输入数字): ")
            if choice in self.models:
                return self.models[choice][0], self.models[choice][1]
            else:
                print("无效选择，请重新输入。")
    
    def load_pipeline(self, model_id, torch_dtype):
        """加载pipeline"""
        try:
            pipeline = DiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch_dtype,
                resume_download=True,
                max_retries=3
            )
            # 禁用NSFW检查器
            pipeline.safety_checker = None
            return pipeline
        except Exception as e:
            print(f"加载模型失败: {e}")
            return None
    
    def load_selected_model(self):
        """加载用户选择的模型"""
        model_id, model_name = self.select_model()
        print(f"正在加载模型: {model_name}")
        print("提示：首次加载模型需要下载，可能需要几分钟时间，请耐心等待...")
        
        # 尝试加载选中的模型
        pipeline = self.load_pipeline(model_id, torch.float16)
        if pipeline is not None:
            print(f'模型加载成功: {model_name}')
        else:
            print('使用默认模型...')
            pipeline = self.load_pipeline("stable-diffusion-v1-5/stable-diffusion-v1-5", torch.float16)
        
        # 检查CUDA是否可用
        if torch.cuda.is_available():
            pipeline.to("cuda")
            print("使用CUDA加速")
        else:
            # 如果CUDA不可用，切换到CPU并使用float32
            if pipeline is not None:
                pipeline.to("cpu")
            print("使用CPU运行")
        
        return pipeline
