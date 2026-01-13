"""
assistant_ticket_bot-1.py - 门票查询助手

Author: lsy
Date: 2026/1/13
"""
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI
from qwen_agent.tools.base import BaseTool,register_tool
from sqlalchemy import create_engine
import pandas as pd

system_prompt = """
你是一个游乐园门票数据查询和分析专家助手。

## 你的核心能力
你能够理解用户的自然语言查询需求，并将其转化为准确的 SQL 语句，查询名为 `tkt_orders` 的订单表。

## 数据库表结构 (tkt_orders)
请严格基于以下表结构编写 SQL：

字段名 | 类型 | 说明
--- | --- | ---
id | int | 订单主键ID
order_time | datetime | 下单时间
account_id | int | 预订用户ID
gov_id | varchar(18) | 身份证号(使用人)
gender | varchar(10) | 性别
age | int | 年龄
province | varchar(30) | 省份
ticket_type | varchar(100) | 票种(如:成人票/儿童票)
sales_channel | varchar(20) | 销售渠道(小程序/官网/大麦)
status | enum | 订单状态(枚举值: '待支付', '已支付', '已取消', '已出票', '已退款')
order_value | decimal(10, 2) | 订单总金额
quantity | int unsigned | 购买票数

## SQL 编写规范 (严格遵守)
1. **禁止全表扫描**：
   - 绝对禁止编写 `SELECT *`。必须明确写出需要的字段名。
   - 查询统计数据时，必须使用聚合函数（如 `COUNT()`, `SUM()`, `AVG()`），不要把所有数据查出来再统计。

2. **时间范围限制**：
   - 如果用户询问“最近”、“历史”、“某个月”等涉及时间的问题，**必须**在 WHERE 子句中加上 `order_time` 的时间范围过滤。
   - 示例：`WHERE order_time >= '2025-01-01' AND order_time < '2025-02-01'`

3. **枚举值处理**：
   - `status` 字段只能使用以下值：'待支付', '已支付', '已取消', '已出票', '已退款'。不要使用其他状态名称。

4. **统计排序**：
   - 涉及排名、Top N 查询时，必须使用 `ORDER BY ... DESC` 和 `LIMIT`。

## 交互流程
1. 分析用户的自然语言需求。
2. 判断是否需要调用 `exc_sql` 工具。
3. 如果需要调用，生成符合上述规范的 SQL 语句。
4. 等待工具返回数据后，用清晰、自然的中文总结结果，不要直接展示原始的数据库表格。

## 回答示例
用户问："昨天卖了多少张票？"
你的思考：需要统计昨天的销量，用到 SUM(quantity)， WHERE order_time 在昨天。
生成的 SQL：SELECT SUM(quantity) FROM tkt_orders WHERE DATE(order_time) = CURRENT_DATE() - INTERVAL 1 DAY
回答：根据查询结果，昨日共售出门票 [数量] 张。
"""

@register_tool('exc_sql')
class ExcSqlTool(BaseTool):
    """
    SQL查询工具，执行传入的SQL语句并返回结果
    """
    description = '对于生成的SQL，进行SQL查询'
    parameters = [
        {
            'name': 'sql_input',
            'type': 'string',
            'description':'生成的SQL语句',
            'required': True,
        }
    ]

    def call(self,params:str,**kwargs):
        import json
        args = json.loads(params)
        sql_input = args['sql_input']
        # database = args.get('database')
        # 创建数据库连接
        engine = create_engine(
            f'mysql+pymysql://root:123@localhost:3306/ticket_assistant_db'
        )
        try:
            df = pd.read_sql(sql_input, engine)
            return df.head(10).to_markdown(index=False)
        except Exception as e:
            return f'SQL执行出错：{str(e)}'


def init_agent_service():
    """初始化门票助手服务"""
    llm_cfg = {
        'model':'qwen-turbo-latest',
    }

    try:
        # 重点
        bot = Assistant(
            llm=llm_cfg,
            name='门票助手',
            description='门票查询与订单分析',
            system_message=system_prompt,
            function_list=['exc_sql'], # 只传工具名称字符串
        )
        print('助手初始化成功')
        return bot
    except Exception as e:
        print(f'助手初始化失败：{str(e)}')
        raise # 遇到错误直接停止

def app_gui():
    """图形界面模式，提供 Web 图形界面"""
    try:
        print('正在启动 Web 界面')
        bot = init_agent_service()
        # 配置聊天界面，列举三个典型门票查询问题
        chatbot_config = {
            'prompt.suggestions': [
                '今天的总销售额是多少？一共卖了多少张票？',
                '哪个省份的游客最多？请按购票人数降序排列，只看前 5 名。',
                '大麦渠道卖出了多少张‘成人票’？且订单状态必须是‘已支付’的。',
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
    app_gui() # 图形界面模式
