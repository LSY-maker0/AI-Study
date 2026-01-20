"""
qwen-agent-multi-files-gui - 

Author: lsy
Date: 2026/1/20
"""
import pprint
import urllib.parse
import json5
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool
import os
from qwen_agent.gui import WebUI

# 步骤 1（可选）：添加一个名为 `my_image_gen` 的自定义工具。
@register_tool('my_image_gen')
class MyImageGen(BaseTool):
    # `description` 用于告诉智能体该工具的功能。
    description = 'AI 绘画（图像生成）服务，输入文本描述，返回基于文本信息绘制的图像 URL。'
    # `parameters` 告诉智能体该工具有哪些输入参数。
    parameters = [{
        'name': 'prompt',
        'type': 'string',
        'description': '期望的图像内容的详细描述',
        'required': True
    }]

    def call(self, params: str, **kwargs) -> str:
        # `params` 是由 LLM 智能体生成的参数。
        prompt = json5.loads(params)['prompt']
        prompt = urllib.parse.quote(prompt)
        return json5.dumps(
            {'image_url': f'https://image.pollinations.ai/prompt/{prompt}'},
            ensure_ascii=False)

def init_agent_service():
    """初始化 Agent"""
    llm_cfg = {
        # 使用 DashScope 提供的模型服务：
        'model': 'deepseek-v3',
        'model_server': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'api_key': os.getenv('DASHSCOPE_API_KEY'),  # 从环境变量获取API Key
        'generate_cfg': {
            'top_p': 0.8
        }
    }

    system_instruction = '''你是一个乐于助人的AI助手。
    在收到用户的请求后，你应该：
    - 首先绘制一幅图像，得到图像的url，
    - 然后运行代码`request.get`以下载该图像的url，
    - 最后从给定的文档中选择一个图像操作进行图像处理。
    用 `plt.show()` 展示图像。
    你总是用中文回复用户。'''
    tools = ['my_image_gen', 'code_interpreter']  # `code_interpreter` 是框架自带的工具，用于执行代码。
    # 获取文件夹下所有文件
    file_dir = os.path.join('./', 'docs')
    files = []
    if os.path.exists(file_dir):
        # 遍历目录下的所有文件
        for file in os.listdir(file_dir):
            file_path = os.path.join(file_dir, file)
            if os.path.isfile(file_path):  # 确保是文件而不是目录
                files.append(file_path)
    print('files=', files)

    try:
        bot = Assistant(llm=llm_cfg,
                        system_message=system_instruction,
                        function_list=tools,
                        files=files)
        print("助手初始化成功！")
        return bot
    except Exception as e:
        print(f"助手初始化失败: {str(e)}")
        raise

def app_gui():
    """图形界面模式，提供 Web 图形界面"""
    try:
        print("正在启动 Web 界面...")
        # 初始化助手
        bot = init_agent_service()
        # 配置聊天界面，列举3个关于保险的问题
        chatbot_config = {
            'prompt.suggestions': [
                '画一只在写代码的猫',
                '介绍下雇主责任险',
                '帮我画一个宇宙飞船，然后把它变成黑白的'
            ]
        }
        print("Web 界面准备就绪，正在启动服务...")
        # 启动 Web 界面
        WebUI(
            bot,
            chatbot_config=chatbot_config
        ).run()
    except Exception as e:
        print(f"启动 Web 界面失败: {str(e)}")
        print("请检查网络连接和 API Key 配置")



if __name__ == '__main__':
    # 运行模式选择
    app_gui()          # 图形界面模式（默认）
