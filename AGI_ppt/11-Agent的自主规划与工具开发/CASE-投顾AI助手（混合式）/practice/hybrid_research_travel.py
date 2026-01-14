"""
hybrid_research_travel - 智能旅行助理

基于LangGraph实现的混合型智能体，结合反应式架构的即时响应能力和深思熟虑架构的长期规划能力，
通过协调层动态切换处理模式，提供智能旅行助理服务。

Author: lsy
Date: 2026/1/14
"""
import os
from typing import TypedDict, Literal, Optional, Dict, Any

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_community.chat_models import ChatTongyi

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

llm = ChatTongyi(model_name='qwen-turbo-latest', dashscope_api_key=DASHSCOPE_API_KEY)

# 定义状态类型
class TravelAdvisorState(TypedDict):
    """旅行助理智能体的状态"""
    # 输入
    user_query: str

    # 处理状态
    query_type: Optional[Literal["reactive", "deliberative"]]
    travel_data: Optional[Dict[str, Any]]

    # 输出
    final_response: Optional[str]

    # 控制流
    current_phase: Optional[str] # phase 阶段

ASSESSMENT_PROMPT = """你是一个智能旅行AI助手的路由协调层，负责分析用户意图并分发请求。

【用户查询】
{user_query}

【任务说明】
请判断该查询应该采用哪种处理模式：

1. reactive（反应式）
   - 特征：查询客观事实或已有数据，无需复杂推理或规划。
   - 适用场景：查天气、查地点、查交通时刻表、查景点开放时间、查汇率。
   - 处理方式：直接调用工具获取数据并返回。

2. deliberative（深思式）
   - 特征：需要生成方案、进行多步推理、整合多个信息来源。
   - 适用场景：制定旅行计划、推荐行程、攻略优化、预算规划。
   - 处理方式：进入 LangGraph 工作流，分步骤思考并生成报告。

【边界案例处理】
如果查询同时包含两种性质（如“武汉今天天气怎么样，适合去哪玩？”）：
- 优先判断为 deliberative，因为后续的“适合去哪玩”更关键。

【输出要求】
请严格按照以下 JSON 格式输出，不要包含任何其他解释或前言。

{{
    "query_type": "reactive 或 deliberative 二选一",
    "reasoning": "用一句话说明为什么选择该模式"
}}

【示例】
输入："明天北京会下雨吗？"
输出：{{"query_type": "reactive", "reasoning": "这是对客观天气数据的直接查询，无需规划步骤。"}}

输入："帮我规划一个 3 天的北京亲子游"
输出：{{"query_type": "deliberative", "reasoning": "这是一个需要生成多日行程方案的复杂任务，需要深思熟虑。"}}
"""

def assess_query(state: TravelAdvisorState) -> Dict[str, Any]:
    """评估查询类型，决定使用反应式还是深思熟虑模式"""
    print('[DEBUG] 进入节点: assess_query')

    prompt = ChatPromptTemplate.from_template(ASSESSMENT_PROMPT)
    chain = prompt | llm | JsonOutputParser()
    result = chain.invoke({"user_query": state["user_query"]})
    
    query_type = result.get("query_type", "reactive")
    if query_type not in ["reactive", "deliberative"]:
        query_type = "reactive"
    
    print(f'[DEBUG] 查询类型判断: {query_type}')
    print(f"原因：{result.get('reasoning','暂时没有原因')}")
    
    return {
        "query_type": query_type,
    }

# 反应式处理节点 - 快速响应简单查询
def reactive_agent(state: TravelAdvisorState) -> Dict[str, Any]:
    """反应式处理：直接回答简单查询"""
    print('[DEBUG] 进入节点: reactive_agent')
    
    # 写死的简单响应逻辑
    user_query = state["user_query"].lower()
    
    response = '根据查询，今天天气晴朗，温度25°C，适合出行。'
    
    print(f'[DEBUG] 反应式响应: {response}')
    
    return {
        "final_response": response,
        "current_phase": "respond"
    }

# 数据收集节点 - 收集旅行相关信息
def collect_data(state: TravelAdvisorState) -> Dict[str, Any]:
    """收集旅行规划所需的数据"""
    print('[DEBUG] 进入节点: collect_data')
    
    # 写死的数据收集逻辑
    travel_data = {
        "destination": "北京",
        "duration": "3天",
        "budget_range": "中等",
        "travel_type": "亲子游",
        "attractions": ["故宫", "天安门", "颐和园", "北京动物园"],
        "weather": "晴朗，温度20-25°C",
        "transportation": "地铁+公交",
        "accommodation": "市中心酒店"
    }
    
    print(f'[DEBUG] 收集到的旅行数据: {travel_data}')
    
    return {
        "travel_data": travel_data,
        "current_phase": "recommend"
    }

# 生成推荐节点 - 基于收集的数据生成旅行建议
def generate_recommendations(state: TravelAdvisorState) -> Dict[str, Any]:
    """生成旅行推荐和建议"""
    print('[DEBUG] 进入节点: generate_recommendations')
    
    travel_data = state.get("travel_data", {})
    user_query = state["user_query"]
    
    # 写死的推荐生成逻辑
    response = f"""基于您的查询"{user_query}"，我为您制定了以下旅行方案：

【目的地】{travel_data.get('destination', '待确定')}
【行程天数】{travel_data.get('duration', '待确定')}
【预算范围】{travel_data.get('budget_range', '待确定')}

【推荐景点】
{chr(10).join(f"- {attr}" for attr in travel_data.get('attractions', []))}

【天气情况】
{travel_data.get('weather', '待查询')}

【交通建议】
建议使用{travel_data.get('transportation', '公共交通')}，方便快捷且经济实惠。

【住宿建议】
推荐选择{travel_data.get('accommodation', '市中心酒店')}，交通便利，周边设施完善。

【温馨提示】
1. 请提前预订门票和酒店
2. 注意天气变化，携带合适的衣物
3. 保持手机电量充足，下载离线地图
4. 注意安全，保管好个人物品

祝您旅途愉快！"""
    
    print(f'[DEBUG] 生成的推荐: {response[:100]}...')
    
    return {
        "final_response": response,
        "current_phase": "respond"
    }

# 创建智能体工作流
def create_travel_advisor_workflow():
    """创建智能旅行智能体工作流"""
    workflow = StateGraph(TravelAdvisorState)

    # 添加节点
    workflow.add_node("assess", assess_query)
    workflow.add_node("reactive_mode", reactive_agent)
    workflow.add_node("collect_data", collect_data)
    workflow.add_node("recommend", generate_recommendations)

    # 设置入口点
    workflow.set_entry_point("assess")

    # 评估后的分支路由：根据query_type决定走反应式还是深思熟虑模式
    workflow.add_conditional_edges(
        "assess",
        lambda x: "reactive_mode" if x.get("query_type") == "reactive" else "collect_data",
        {
            "reactive_mode": "reactive_mode",
            "collect_data": "collect_data"
        }
    )

    # 反应式模式直接结束
    workflow.add_edge("reactive_mode", END)

    # 深思熟虑模式的流程：收集数据 -> 生成推荐 -> 结束
    workflow.add_edge("collect_data", "recommend")
    workflow.add_edge("recommend", END)

    return workflow.compile()


# 运行智能体
def run_travel_advisor(user_query: str) -> Dict[str, Any]:
    """运行智能旅行助手智能体并返回结果"""
    agent = create_travel_advisor_workflow()

    initial_state = {
        "user_query": user_query,
        "query_type": None,
        "travel_data": None,
        "final_response": None,
        "current_phase": "assess"
    }

    print("LangGraph Mermaid流程图：")
    print(agent.get_graph().draw_mermaid())

    result = agent.invoke(initial_state)
    return result

if __name__ == "__main__":
    print("=== 混合智能体 - 智能旅行AI助手 ===\n")
    print("使用模型：Qwen-Turbo-Latest\n")
    print("\n" + "-"*50 + "\n")

    print('您可以尝试以下查询示例：\n')
    print('问题一（反应式）：今天天气怎么样？')
    print('问题二（深思熟虑式）：帮我规划一个 3 天的北京亲子游。')

    user_query = input("请输入您的查询：")

    result = run_travel_advisor(user_query)
    if result['query_type'] == 'reactive':
        print(f'反应式响应：{result["final_response"]}')
    else:
        print(f'深思熟虑式响应：{result["final_response"]}')

