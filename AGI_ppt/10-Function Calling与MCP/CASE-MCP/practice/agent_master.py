"""
agent_master - 主控代理，集成多个 MCP 工具

Author: lsy
Date: 2026/1/13
"""
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI


def init_agent_service():
    """初始化agent助手"""

    # LLM 模型配置
    llm_cfg={
        'model':'qwen-turbo-latest',
        'retry_count':1,
    }

    # 系统角色设定
    system=("""
你是一个全能智能助手，可以根据用户需求调用以下工具：

## 你可以使用的工具
1. **旅行规划工具** - 规划自驾游路线、景点推荐
2. **网页抓取工具** - 抓取网页内容并转为 Markdown
3. **新闻搜索工具** - 搜索最新的关税等新闻
4. **文件系统工具** - 读取本地文件、统计文件数量

## 交互规则
- 分析用户意图，判断需要使用哪个工具
- 一次只调用一个工具，避免重复
- 用清晰、自然的中文回复用户
""")

    # MCP工具配置
    tools = [{
        "mcpServers": {
            "txt_counter": {
                "command": "python",
                "args": ["txt_counter.py"],
            },
            "tavily-mcp": {
                "args": [
                    "-y",
                    "tavily-mcp@0.1.4"
                ],
                "autoApprove": [],
                "command": "npx",
                "env": {
                    "TAVILY_API_KEY": ""
                }
            },
            "amap-maps": {
                "args": [
                    "-y",
                    "@amap/amap-maps-mcp-server"
                ],
                "command": "npx",
                "env": {
                    "AMAP_MAPS_API_KEY": ""
                }
            },
            "fetch": {
                "command": "python",
                "args": ["-m", "mcp_server_fetch","--ignore-robots-txt"]
            }
            # "travel-planner": {
            #     "args": [
            #         "@gongrzhe/server-travelplanner-mcp"
            #     ],
            #     "command": "npx",
            #     "env": {
            #         "GOOGLE_MAPS_API_KEY": "your_google_maps_api_key"
            #     }
            # }
        }
    }]

    try:
        # 创建助手实例
        bot = Assistant(
            llm=llm_cfg,
            name='全能助手',
            description='集成旅行规划、网页抓取、新闻搜索和文件管理的全能智能助手',
            system_message=system,
            function_list=tools,
        )
        print('助手初始化成功！')
        return bot
    except Exception as e:
        print(f'助手初始化失败：{str(e)}')
        raise

def app_gui():
    """图形界面模式，提供 Web 图形界面"""
    try:
        print('正在启动 Web 界面...')
        # 初始化助手
        bot = init_agent_service()
        # 初始化聊天界面
        chatbot_config={
            'prompt.suggestions':[
                '规划从南昌到长沙的7天自驾游',
                '获取“https://www.baidu.com/”网页内容，并转化为Markdown格式',
                '检索最新的关税新闻',
                '统计桌面上的 txt的文件数量',
            ]
        }

        print("Web 界面准备就绪，正在启动服务...")
        # 启动 Web 界面
        WebUI(
            bot,
            chatbot_config=chatbot_config,
        ).run(server_port=8080)
    except Exception as e:
        print(f'启动 Web 界面失败：{str(e)}')
        print('请检查网络连接和 API Key 配置')


if __name__ == '__main__':
    app_gui()
