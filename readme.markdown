# Stable Diffusion 图像生成器

一个基于Stable Diffusion的交互式图像生成工具，支持多种模型和参数调整。

## 功能特性

- 🎨 支持多种Stable Diffusion模型
- ⚙️ 可自定义生成参数（推理步数、引导系数等）
- 🖼️ 实时显示生成进度
- 💾 自动保存生成图像
- 🌐 中文界面支持


## 安装要求

- Python 3.8+
- CUDA支持（推荐，可选）

## 安装步骤

1. 克隆仓库：
#####
bash 
- git clone https://github.com/yourusername/stable-diffusion-gui.git 
- cd stable-diffusion-gui
2. 安装依赖
#####
bash 
- pip install -r requirements.txt
## 使用方法
bash 
- python src/main.py
## 支持的模型

1. Stable Diffusion 1.5
2. Stable Diffusion 2.1
3. Open Journey (艺术风格)
4. RunwayML SD 1.5
5. Stable Diffusion XL

待后续添加更多模型。

## 参数说明

- **推理步数**：生成质量与时间的平衡，推荐20-100
- **引导系数(CFG Scale)**：控制与提示词的匹配程度，推荐7-12
- **图像尺寸**：生成图像的高宽，需为64的倍数

## 许可证

MIT License
##
- 当前为V0版本 2025.08.13

---------------------------------------------------------