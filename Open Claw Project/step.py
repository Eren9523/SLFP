from openai import OpenAI
import os

# ================= 1. 配置区域 (随时切换你的模型) =================

client = OpenAI(
    api_key="你的模型APIKEY",
    base_url="https://api.modelarts-maas.com/v2"  # 如出错可以增删 /chat/completions 。
)
model_name = "deepseek-v3.2"
# ===============================================
# ==================================================================

# 2. 读取基础设定和技能库并拼接，赋予 AI 规则和能力
agentmd = open("Agent.md", "r", encoding="utf-8").read()
skillmd = open("SKILL.md", "r", encoding="utf-8").read()
messages = [{"role": "system", "content": agentmd + "\n\n" + skillmd}]

# 3. 外层循环：负责持续接收用户的新任务
while True:
    user_input = input("\n 【你】 ")
    messages.append({"role": "user", "content": user_input})
    
    # 4. 内层循环：负责 AI 处理单个任务的“思考-执行-反馈”循环
    while True:
        # 注意：这里改成了通用的 chat.completions.create 语法
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        reply = response.choices[0].message.content
        
        messages.append({"role": "assistant", "content": reply})
        
        # 打印 AI 的回复，使用绿色高亮显示
        print(f"\033[32m【AI】 {reply.strip()}\033[0m\n")
        
        # 5. 判断跳出条件：如果 AI 认为任务完成了
        if reply.strip().startswith("完成:"):
            break

        # 6. 执行命令逻辑：如果 AI 回复的是命令
        try:
            # 提取 "命令: " 后面的实际指令内容
            # command_to_run = reply.strip().split("命令:")[1].strip()
            # 修改后的代码：提取"命令:"之后的内容，按换行符切割，只取第一行
            command_to_run = reply.strip().split("命令:")[1].split('\n')[0].strip()
            
            # 5.1 安全机制：提取出命令后，在执行前要求用户按下回车确认
            confirm = input(f"⚠️ 拦截！AI 想要执行命令: [{command_to_run}]\n按回车键允许执行，或输入 'n' 拒绝: ")
            if confirm.lower() == 'n':
                print("🚫 已拒绝执行该命令，正在让 AI 重新思考...")
                messages.append({"role": "user", "content": "用户拒绝执行该命令，请思考替代方案或直接回复完成。"})
                continue 
            
            print(f"⚙️ 正在执行系统命令: {command_to_run}")
            # os.popen 执行命令并读取终端输出结果
            command_result = os.popen(command_to_run).read()
            
            # 将执行结果反馈给 AI
            messages.append({"role": "user", "content": f"执行完毕\n{command_result}"})
            
        except IndexError:
            messages.append({"role": "user", "content": "格式错误，请严格使用 '命令: XXX' 或 '完成: XXX' 的格式。"})