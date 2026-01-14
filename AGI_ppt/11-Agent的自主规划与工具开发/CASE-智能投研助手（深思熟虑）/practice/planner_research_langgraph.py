"""
planner_research_langgraph - 深思熟虑智能体 - 活动策划助手

Author: lsy
Date: 2026/1/14
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Literal, TypedDict, Optional
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Tongyi
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langgraph.graph import StateGraph, END

# 设置API密钥
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# 创建LLM实例
llm = Tongyi(model_name="qwen-turbo", dashscope_api_key=DASHSCOPE_API_KEY)

class PlannerState(TypedDict):
    """策划智能体的状态"""
    # 输入
    participants: str  # 参与人员
    core_goal: str  # 核心目标
    budget: str  # 预算限制
    atmosphere: str  # 期望氛围

    # 中间状态
    analysis: Optional[str]  # 需求分析结果
    options: Optional[List[Dict]]  # 候选方案列表
    best_option: Optional[Dict]  # 选中的最佳方案

    # 输出
    final_plan: Optional[str]

    # 控制流
    current_step: Literal["analyze", "generate", "decide", "plan"]
    error: Optional[str]

# ====== 提示模板优化 ======

ANALYZE_PROMPT = """你是一个活动策划专家。请分析以下需求：
参与人员: {participants}
核心目标: {core_goal}
预算限制: {budget}
期望氛围: {atmosphere}

请深入分析：在这个预算和氛围下，如何满足核心需求？

请用一句话总结分析结果，不要包含任何其他解释或前言。
"""

GENERATE_PROMPT = """你是一个活动点子王。根据以下需求，生成 3 个完全不同的活动方案。
需求详情：
参与人员: {participants}
核心目标: {core_goal}
预算限制: {budget}
期望氛围: {atmosphere}
需求分析：{analysis}

请生成 3 个方案的 JSON 列表，每个方案包含：
- id: 方案编号 (1, 2, 3)
- name: 活动名称
- reason: 推荐理由
- cost_estimate: 预估花费

只输出 JSON 数组，不要其他内容。
"""

DECIDE_PROMPT = """你是决策者。根据用户的核心目标，从 3 个方案中选出最好的一个。
需求详情：
参与人员: {participants}
核心目标: {core_goal}
预算限制: {budget}
期望氛围: {atmosphere}
需求分析：{analysis}
候选方案: {options}

请选择最符合"核心目标"且在"预算"范围内体验最好的方案。
输出格式：JSON {{"selected_id": 1, "reason": "..." }}
"""

PLAN_PROMPT = """你是执行秘书。请把选定的活动方案，结合用户的原始需求，细化成具体的执行清单（TODO List）。

【用户原始需求】
参与人员: {participants}
核心目标: {core_goal}
预算限制: {budget}
期望氛围: {atmosphere}
需求分析：{analysis}

【选定的方案】
{best_option}

请根据以上信息，生成包含以下内容的清单：
1. 准备物品（必须考虑预算限制）
2. 具体行程安排（时间轴形式）
3. 注意事项

请生成一段清晰的自然文本计划，语气要贴心且专业。
"""

# ====== 节点函数 ======

def analyze_node(state: PlannerState) -> PlannerState:
    """第一步：基于结构化数据进行分析"""
    print("1. 正在基于您的需求进行分析...")

    prompt = ChatPromptTemplate.from_template(ANALYZE_PROMPT)
    input_data = {
        "participants": state["participants"],
        "core_goal": state["core_goal"],
        "budget": state["budget"],
        "atmosphere": state["atmosphere"],
    }

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke(input_data)

    print(f"   -> 分析结果: {result}")

    return {
        **state,
        "analysis": result,
        "current_step": "generate"
    }

def generate_node(state: PlannerState) -> PlannerState:
    """第2步：生成方案"""
    print("2. 正在头脑风暴生成方案...")

    prompt = ChatPromptTemplate.from_template(GENERATE_PROMPT)
    input_data = {
        "participants": state["participants"],
        "core_goal": state["core_goal"],
        "budget": state["budget"],
        "atmosphere": state["atmosphere"],
        "analysis": state["analysis"],
    }

    chain = prompt | llm | JsonOutputParser()
    result = chain.invoke(input_data)

    print(f"   -> 生成了 {len(result)} 个方案")
    for opt in result:
        print(f"      - 方案{opt['id']}: {opt['name']} (理由: {opt['reason']}, 花费: {opt['cost_estimate']})")

    return {
        **state,
        "options": result,
        "current_step": "decide"
    }

def decide_node(state: PlannerState) -> PlannerState:
    """第3步：决策方案"""
    print("3. 正在评估并选择最佳方案...")

    prompt = ChatPromptTemplate.from_template(DECIDE_PROMPT)
    input_data = {
        "participants": state["participants"],
        "core_goal": state["core_goal"],
        "budget": state["budget"],
        "atmosphere": state["atmosphere"],
        "analysis": state["analysis"],
        "options": json.dumps(state["options"], ensure_ascii=False),
    }

    chain = prompt | llm | JsonOutputParser()
    result = chain.invoke(input_data)

    selected_id = result["selected_id"]
    best_opt = next((opt for opt in state["options"] if opt["id"] == selected_id), None)

    print(f"   -> 决定采用方案 {selected_id}: {best_opt['name']}")

    return {
        **state,
        "best_option": best_opt,
        "current_step": "plan"
    }

def plan_node(state: PlannerState) -> PlannerState:
    """第4步：生成执行计划（优化节点）"""
    print("4. 正在生成具体执行计划...")

    prompt = ChatPromptTemplate.from_template(PLAN_PROMPT)

    # 【关键优化】：这里把所有原始需求都传进去，而不仅仅是 best_option
    input_data = {
        "participants": state["participants"],
        "core_goal": state["core_goal"],
        "budget": state["budget"],
        "atmosphere": state["atmosphere"],
        "analysis": state["analysis"],
        "best_option": json.dumps(state["best_option"], ensure_ascii=False, indent=2)
    }

    chain = prompt | llm | StrOutputParser()
    final_plan = chain.invoke(input_data)

    return {
        **state,
        "final_plan": final_plan,
        "current_step": "end"
    }

# ====== 工作流构建 ======

def create_planner_agent_workflow():
    """创建深思熟虑规划智能体工作流图"""
    workflow = StateGraph(PlannerState)

    # 添加节点
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("decide", decide_node)
    workflow.add_node("plan", plan_node)

    # 设置入口点
    workflow.set_entry_point("analyze")

    # 设置边 (线性流程)
    workflow.add_edge("analyze", "generate")
    workflow.add_edge("generate", "decide")
    workflow.add_edge("decide", "plan")
    workflow.add_edge("plan", END)

    # 编译工作流
    return workflow.compile()

def run_research_agent(participants, core_goal, budget, atmosphere):
    """运行智能体并返回结果"""
    # 创建工作流
    agent = create_planner_agent_workflow()

    # 准备初始状态
    initial_state = {
        "participants": participants,
        "core_goal": core_goal,
        "budget": budget,
        "atmosphere": atmosphere,
        "analysis": None,
        "options": None,
        "best_option": None,
        "final_plan": None,
        "current_step": "analyze",
        "error": None  # 补全字段
    }
    print("LangGraph Mermaid流程图：")
    print(agent.get_graph().draw_mermaid())

    # 运行智能体
    result = agent.invoke(initial_state)
    return result


def generate_full_report(result: Dict[str, Any], output_path: str):
    """【新增函数】将智能体的所有过程结果写入文件，生成完整报告"""
    report_lines = []
    report_lines.append("=" * 50)
    report_lines.append("         📅 活动策划完整报告")
    report_lines.append("=" * 50)
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # 1. 原始需求
    report_lines.append("【一、用户原始需求】")
    report_lines.append(f"  📍 参与人员: {result.get('participants', 'N/A')}")
    report_lines.append(f"  🎯 核心目标: {result.get('core_goal', 'N/A')}")
    report_lines.append(f"  💰 预算限制: {result.get('budget', 'N/A')}")
    report_lines.append(f"  🌟 期望氛围: {result.get('atmosphere', 'N/A')}")
    report_lines.append("")

    # 2. 需求分析
    report_lines.append("【二、需求分析】")
    report_lines.append(f"  {result.get('analysis', 'N/A')}")
    report_lines.append("")

    # 3. 候选方案
    report_lines.append("【三、候选方案列表】")
    options = result.get('options', [])
    if options:
        for opt in options:
            report_lines.append(f"  方案 {opt['id']}: {opt['name']}")
            report_lines.append(f"    - 推荐理由: {opt.get('reason', 'N/A')}")
            report_lines.append(f"    - 预估花费: {opt.get('cost_estimate', 'N/A')}")
            report_lines.append("")
    else:
        report_lines.append("  (未生成候选方案)")
        report_lines.append("")

    # 4. 决策结果
    report_lines.append("【四、最终决策】")
    best_option = result.get('best_option')
    if best_option:
        report_lines.append(f"  ✅ 选定方案: {best_option['name']}")
        report_lines.append(f"  💡 决策理由: {result.get('decision_reason', 'N/A')}")
        report_lines.append("")
    else:
        report_lines.append("  (未选定方案)")
        report_lines.append("")

    # 5. 执行计划
    report_lines.append("【五、执行计划（TODO清单）】")
    final_plan = result.get('final_plan')
    if final_plan:
        # 将长段落分行显示，保持格式
        for line in final_plan.split('\n'):
            report_lines.append(f"  {line}")
    else:
        report_lines.append("  (未生成执行计划)")

    report_lines.append("")
    report_lines.append("=" * 50)
    report_lines.append("         报告结束")
    report_lines.append("=" * 50)

    # 写入文件
    report_text = '\n'.join(report_lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\n✅ 完整报告已保存为: {output_path}")

# ====== 主程序入口 ======

if __name__ == "__main__":
    print("=== 周末活动策划助手 ===\n")

    # 1. 获取结构化数据
    participants = input("1. 谁去？(例如: 女朋友，一个人): ")
    core_goal = input("2. 干嘛去？(例如: 纪念日约会，周末出行): ")
    budget = input("3. 预算多少？(例如: 500元，不差钱): ")
    atmosphere = input("4. 想要什么氛围？(例如: 浪漫、安静、热闹): ")

    try:
        # 运行智能体
        result = run_research_agent(participants, core_goal, budget, atmosphere)

        # 处理结果
        if result.get("error"):
            print(f"\n发生错误: {result['error']}")
        else:
            print("\n=== 最终研究报告 ===\n")
            print(result.get("final_plan", "未生成报告"))

            # 保存报告
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"research_plan_{timestamp}.txt"
            generate_full_report(result, filename)

            print(f"\n报告已保存为: {filename}")

    except Exception as e:
        print(f"\n运行过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
