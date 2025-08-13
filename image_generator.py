#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像生成模块
"""

import matplotlib.pyplot as plt
import torch

class ImageGenerator:
    """图像生成器"""
    
    def __init__(self, pipeline):
        self.pipeline = pipeline
    
    def generate(self, prompt, params):
        """生成图像"""
        result = self.pipeline(
            prompt,
            num_inference_steps=params['num_inference_steps'],
            guidance_scale=params["guidance_scale"],
            height=params["height"],
            width=params["width"]
        )
        return result.images[0]
    
    def display_image(self, image, prompt):
        """显示图像"""
        plt.imshow(image)
        plt.axis('off')
        plt.title(f'Generated: {prompt}')
        plt.show()
