from flask import Flask, render_template, request, jsonify
import requests
import json
import PyPDF2

app = Flask(__name__)

# 模拟缓存对话历史（实际应用中可以用数据库或缓存系统）
conversation_history = []
pdf_text_cache = None  # PDF 内容缓存

# 加载 PDF 内容（只在首次加载时读取）
def load_default_pdf_content(pdf_path):
    global pdf_text_cache
    if pdf_text_cache is None:  # 仅当缓存为空时加载 PDF
        text = ""
        try:
            with open(pdf_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            pdf_text_cache = text
        except Exception as e:
            print(f"加载 PDF 出现异常: {e}")
            return ""
    return pdf_text_cache

# 与模型进行对话
def send_message(messages):
    url = "http://localhost:11434/api/chat"  # 模型的 API 地址
    payload = {
        "model": "deepseek-r1:14b",
        "messages": messages
    }
    try:
        response = requests.post(url, json=payload)
        ndjson_lines = response.text.strip().splitlines()
        parsed_data = [json.loads(line) for line in ndjson_lines if line.strip()]
        return parsed_data
    except Exception as e:
        print(f"请求异常: {e}")
        return None

# 提取模型响应的内容
def extract_content(parsed_response):
    if not parsed_response:
        return ""
    content = ""
    for item in parsed_response:
        if "message" in item and "content" in item["message"]:
            content += item["message"]["content"]
    return content

@app.route('/')
def home():
    return render_template('index.html')  # 渲染前端 HTML

@app.route('/send_input', methods=['POST'])
def send_input():
    user_input = request.form['input_text']  # 获取前端传来的数据
    print(f"用户输入: {user_input}")  # 打印用户输入，确保接收正确

    # 加载 PDF 内容
    pdf_path = "knowledge.pdf"
    pdf_text = load_default_pdf_content(pdf_path)

    # 清空对话历史（确保每次请求都是从新的上下文开始）
    conversation_history.clear()

    # 添加系统身份设定和参考资料

    conversation_history.append(
        {"role": "system", "content": f"以下是参考资料，请在回答问题时参考这部分内容：\n{pdf_text}"}
    )
    conversation_history.append(
        {"role": "system", "content": "你是IMRIS所开发的智能医学助手VV，擅长医学诊断和治疗分析。"}
    )

    # 添加用户输入和任务描述
    task_description = f"用户提出了问题：{user_input}。请根据提供的参考资料，作为IMRIS所开发的智能医学助手VV的身份，回答用户的问题。"
    conversation_history.append({"role": "system", "content": task_description})
    conversation_history.append({"role": "user", "content": user_input})

    # 发送消息到模型
    parsed_response = send_message(conversation_history)

    # 如果没有返回模型响应
    if parsed_response is None:
        print("无法获取模型响应")
        return jsonify(response="无法获取模型响应")

    assistant_reply = extract_content(parsed_response)
    print(f"模型回复: {assistant_reply}")

    # 将模型回复添加到对话上下文中
    conversation_history.append({"role": "assistant", "content": assistant_reply})

    # 返回模型的回答
    return jsonify(response=assistant_reply)

if __name__ == '__main__':
    app.run(debug=True)
