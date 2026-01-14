#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
个人理财助手 - 反应式智能体实现

LangChain Agent (ReAct Agent)

基于LangChain Agent逻辑实现的个人理财助手，能够根据用户的查询需求，
自动选择工具来分析记账数据。
"""

import re
import os
from typing import List, Dict, Any
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatTongyi
from langchain.agents import create_agent

# 通义千问API密钥
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# 模拟的个人记账数据库
TRANSACTION_DB = [
    {
        "id": "t001",
        "date": "2023-10-01",
        "category": "餐饮",
        "item": "麦当劳午餐",
        "amount": -35.00,
        "note": "套餐"
    },
    {
        "id": "t002",
        "date": "2023-10-02",
        "category": "交通",
        "item": "地铁充值",
        "amount": -100.00,
        "note": "月卡"
    },
    {
        "id": "t003",
        "date": "2023-10-03",
        "category": "工资",
        "item": "10月工资发放",
        "amount": 15000.00,
        "note": "税前"
    },
    {
        "id": "t004",
        "date": "2023-10-05",
        "category": "购物",
        "item": "优衣库买衣服",
        "amount": -599.00,
        "note": "秋装"
    },
    {
        "id": "t005",
        "date": "2023-10-05",
        "category": "餐饮",
        "item": "周末聚餐",
        "amount": -300.00,
        "note": "火锅"
    },
    {
        "id": "t006",
        "date": "2023-10-02",
        "category": "交通",
        "item": "打车",
        "amount": -10.00,
        "note": "月卡"
    },
]


@tool
def search_transactions_by_keywords(keywords: str) -> str:
    """通过关键词搜索相关的记账记录。输入应为相关关键词，如‘麦当劳’、‘充值’等。"""
    keywords = keywords.strip().lower()
    # 支持逗号、空格分隔多个关键词
    keyword_list = re.split(r'[,，\s]+', keywords)

    matched_records = []
    for record in TRANSACTION_DB:
        # 在类别、项目名、备注中搜索
        record_text = (record["category"] + " " + record["item"] + " " + record["note"]).lower()
        match_count = sum(1 for kw in keyword_list if kw in record_text)
        if match_count > 0:
            matched_records.append((record, match_count))

    # 按匹配度排序
    matched_records.sort(key=lambda x: x[1], reverse=True)

    if not matched_records:
        return f"未找到包含关键词 '{keywords}' 的记录。"

    result = []
    for record, _ in matched_records[:3]: # 只返回最相关的3条
        result.append(f"日期: {record['date']} | 类别: {record['category']} | 项目: {record['item']} | 金额: {record['amount']}元")

    return "\n".join(result)


@tool
def calculate_category_spending(category: str) -> str:
    """根据类别计算该类别的总支出。输入应为类别名称，可选类别：餐饮、交通、购物、工资等。"""
    category = category.strip()
    total_amount = 0
    count = 0

    for record in TRANSACTION_DB:
        # 支持模糊匹配（比如输入“吃”也能匹配“餐饮”）
        if category.lower() in record["category"].lower():
            total_amount += record["amount"]
            count += 1

    if count == 0:
        return f"未找到类别为 '{category}' 的记录。"

    spending_type = "支出" if total_amount < 0 else "收入"
    return f"在 '{category}' 类别下，共找到 {count} 笔记录，总{spending_type}为：{abs(total_amount):.2f} 元。"


@tool
def get_account_summary(query: str) -> str:
    """获取账户的整体收支概况或回答简单余额问题。"""
    total_income = sum(r['amount'] for r in TRANSACTION_DB if r['amount'] > 0)
    total_expense = sum(r['amount'] for r in TRANSACTION_DB if r['amount'] < 0)
    balance = total_income + total_expense

    # 简单的关键词触发
    query = query.lower()
    if "余额" in query or "剩" in query or "总额" in query:
        return f"您的账户当前总余额为：{balance:.2f} 元。\n总收入：{total_income:.2f} 元\n总支出：{abs(total_expense):.2f} 元"
    else:
        return "我可以帮您查询账户余额、总收入和总支出。请问您具体想了解什么？"


def create_finance_agent():
    llm = ChatTongyi(model="qwen-plus", dashscope_api_key=DASHSCOPE_API_KEY)

    tools = [search_transactions_by_keywords, calculate_category_spending, get_account_summary]

    system_prompt = """你是一个个人理财助手，专门帮助用户查询和管理记账数据。

你可以使用以下工具来查询信息：
1. search_transactions_by_keywords: 通过关键词搜索具体的消费记录（如：麦当劳、火锅）
2. calculate_category_spending: 计算某个类别的总花费（如：餐饮、交通）
3. get_account_summary: 查询账户余额或整体收支概况

注意：
1. 如果用户问“一共花了多少”或“余额多少”，请使用 get_account_summary。
2. 如果用户问“餐饮花了多少”，请使用 calculate_category_spending。
3. 如果用户问具体的消费细节（如“有没有买过衣服”），请使用 search_transactions_by_keywords。
4. 回答要简洁明了。"""

    agent = create_agent(llm, tools, system_prompt=system_prompt)

    return agent


if __name__ == "__main__":
    finance_agent = create_finance_agent()

    print("=== 个人理财智能助手（反应式智能体）===\n")
    print("使用模型：qwen-plus")
    print("您可以提问：")
    print(" - '我余额还有多少？'")
    print(" - '我在餐饮上花了多少钱？'")
    print(" - '帮我查一下有没有买过麦当劳'")
    print(" - '这周的收入是多少'")
    print("输入'退出'结束对话\n")

    while True:
        user_input = input("请输入您的问题：")
        if user_input.lower() in ['退出', 'exit', 'quit']:
            print("感谢使用，再见！")
            break

        response = finance_agent.invoke({"messages": [HumanMessage(content=user_input)]})

        # 获取最后一条AI消息作为回答
        for msg in reversed(response["messages"]):
            if isinstance(msg, AIMessage) and msg.content:
                print(f"助手: {msg.content}\n")
                break

        print("-" * 40)
