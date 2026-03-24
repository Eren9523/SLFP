from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import json

app = Flask(__name__)

# ================= 1. 配置区域 =================
client = OpenAI(
    api_key="-ZcFXqSRNU650vvxzz5hJEJnX8gpZHa00n6-7QbU8zQIZlESr5Jpm3xI-7OEv-zIIkAqg99EG1-p1QzUmnthUA", # ⚠️ 记得填入你的 Key
    base_url="https://api.modelarts-maas.com/v2"  
)
model_name = "deepseek-v3.2"
HISTORY_FILE = "history.json" # 记忆文件的名字
# ===============================================

# --- 新增记忆管理功能 ---
def load_history():
    """启动时读取记忆，如果没有记忆则初始化系统提示词"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        agentmd = open("Agent.md", "r", encoding="utf-8").read()
        skillmd = open("SKILL.md", "r", encoding="utf-8").read()
        return [{"role": "system", "content": agentmd + "\n\n" + skillmd}]

def save_history(messages):
    """每次聊天后，把最新记忆保存到硬盘"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# 读取记忆！
global_messages = load_history()
# ------------------------

@app.route('/')
def home():
    return render_template('index.html')

# 路由：获取历史记忆
@app.route('/api/history', methods=['GET'])
def get_history():
    chat_history = [msg for msg in global_messages if msg["role"] != "system"]
    return jsonify(chat_history)

# ================= 新增：清空记忆接口 =================
@app.route('/api/clear', methods=['POST'])
def clear_memory():
    global global_messages
    
    # 物理删除
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        
    # 内存重置
    global_messages = load_history()
    
    return jsonify({"status": "success", "message": "记忆已彻底清空！"})
# =====================================================

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    global_messages.append({"role": "user", "content": user_input})
    save_history(global_messages) 
    
    max_loops = 5 
    loop_count = 0
    
    while loop_count < max_loops:
        loop_count += 1
        
        response = client.chat.completions.create(
            model=model_name,
            messages=global_messages
        )
        reply = response.choices[0].message.content
        global_messages.append({"role": "assistant", "content": reply})
        save_history(global_messages)
        
        if reply.strip().startswith("完成:"):
            final_text = reply.replace("完成:", "").strip()
            return jsonify({"reply": final_text})
            
        elif "命令:" in reply:
            try:
                command_to_run = reply.strip().split("命令:")[1].split('\n')[0].strip()
                print(f"⚠️ Web 端触发自动执行命令: {command_to_run}")
                command_result = os.popen(command_to_run).read()
                
                if not command_result.strip():
                    command_result = "命令已执行，无控制台输出。"
                    
                global_messages.append({"role": "user", "content": f"执行完毕\n{command_result}"})
                save_history(global_messages)
            except Exception as e:
                global_messages.append({"role": "user", "content": "格式错误，请严格使用格式。"})
                save_history(global_messages)
                
        else:
            return jsonify({"reply": reply})
            
    return jsonify({"reply": "脑容量超载啦，我在后台尝试了好多次操作都没成功，请换个简单的命令试试哦！😵‍💫"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)