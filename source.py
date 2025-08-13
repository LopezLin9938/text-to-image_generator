import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import torch
import os

from diffusers import DiffusionPipeline

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

#定义选择模型函数，后面初始化的时候调用
def select_model():
    """
    选择要使用的模型的cmd line view
    预设键值对:12345678等等去应对pipeline里pretrained的模型。
    generate dict named:''models''
    """
    models = {
        "1": ("stable-diffusion-v1-5/stable-diffusion-v1-5", "Stable Diffusion 1.5"),
        "2": ("stabilityai/stable-diffusion-2-1", "Stable Diffusion 2.1"),
        "3": ("prompthero/openjourney", "Open Journey (艺术风格)"),
        "4": ("runwayml/stable-diffusion-v1-5", "RunwayML SD 1.5"),
        "5": ("stabilityai/stable-diffusion-xl-base-1.0", "Stable Diffusion XL")
    }

    print("=== 模型选择 ===")#由于上方已经生成了models的dict 且键值对形式为x,(line_value,title).
    for key, (model_id, model_name) in models.items():#遍历models字典中的所有键值对
        print(f"{key}. {model_name}")#对于每个模型条目，打印格式为"键. 模型名称"的选项列表，供用户选择

    while True:
        choice = input("请选择模型 (输入数字): ")
        if choice in models:
            return models[choice][0], models[choice][1]
        else:
            print("无效选择，请重新输入。")#
#定义参数生成函数，后面初始化的时候调用
def get_generation_params():
    """
    获取生成参数
    """
    print("\n=== 参数设置 (直接回车使用默认值) ===")

    # 获取推理步数
    try:
        steps_input = input("推理步数 (默认50): ").strip()
        num_inference_steps = int(steps_input) if steps_input else 50
    except ValueError:
        num_inference_steps = 50

    # 获取引导系数
    try:
        cfg_input = input("引导系数CFG Scale (默认7.5): ").strip()
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
def get_user_input():
    """
    获取用户输入的高级交互函数
    """
    print("===image generalizer with sd_module by ch.l===")

    while True:
        prompt = input("请输入您想要生成的图像描述 (输入 'quit' 退出): \n> ")

        if prompt.lower() == 'quit':
            return None

        if not prompt.strip():
            print("提示词不能为空，请重新输入。")
            continue

        return prompt
#舒适保存函数
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
'''
# 初始化pipeline 当前使用的是sd1.5模型
pipeline = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", torch_dtype=torch.float16)
'''
#select model
model_id, model_name = select_model()
print(f"正在加载模型: {model_name}")
print("提示：首次加载模型需要下载，可能需要几分钟时间，请耐心等待...")

#优化pipeline initialization.select the module by user input.
try:
    pipeline = DiffusionPipeline.from_pretrained(model_id,
                                                 torch_dtype=torch.float16,
                                                 resume_download=True,
                                                 max_retries=3
                                                 )
    print(f'loading succeeded:{model_name}')
except Exception as e:
    print(f'loading failed:{model_name}')
    print('using the default module')
    pipeline = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", torch_dtype=torch.float16)
#disable NSFW CHECKER
pipeline.safety_checker = None



# 检查CUDA是否可用
if torch.cuda.is_available():
    pipeline.to("cuda")
else:
    # 如果CUDA不可用，切换到CPU并使用float32
    pipeline = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", torch_dtype=torch.float32)
    pipeline.to("cpu")

###########################################上方为能力集以及自定义函数###########################################################
# mainstream
while True:
    user_prompt = get_user_input() #grab the user input data.
    if user_prompt is None:
        print("program cancelled.")
        break
    params = get_generation_params()
    try:
        print(f"generating image:{user_prompt}")#输出提示词
        print(f'current using parameters:{params}')
        result = pipeline(
            user_prompt,
            num_inference_steps=params['num_inference_steps'],
            guidance_scale=params["guidance_scale"],
            height=params["height"],
            width=params["width"]
        )
        generated_image = result.images[0]

        #directly show the generated image.
        plt.imshow(generated_image)
        plt.axis('off')
        plt.title(f'Generated:{user_prompt}')
        plt.show()

        #save the image
        filename = save_image_safely(generated_image,user_prompt)
        print(f'image already saved as {filename}')

    except Exception as e:
        print(f"An error occurred: {e}")
        continue












'''result = pipeline("An image of a tank in hitler style")
Image = result.images[0]
generated_image = Image

# 保存图像
Image.save("22.png")

plt.imshow(generated_image)
plt.axis('off')  # 不显示坐标轴
plt.show()
'''