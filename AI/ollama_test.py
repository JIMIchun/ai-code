import requests
import json


def send_message(messages):
    """
    向 Ollama 的 deepseek 模型发送消息列表，并返回解析后的 NDJSON 响应数据列表。
    """
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "deepseek-r1:14b",
        "messages": messages
    }
    try:
        response = requests.post(url, json=payload)
        # 将返回的 NDJSON 数据按行解析
        ndjson_lines = response.text.strip().splitlines()
        parsed_data = [json.loads(line) for line in ndjson_lines if line.strip()]
        return parsed_data
    except Exception as e:
        print(f"请求异常: {e}")
        return None


def extract_content(parsed_data):
    """
    从解析后的响应数据中提取所有 message 中的 content，并组合为一个字符串返回。
    """
    if not parsed_data:
        return ""
    return "".join(
        item["message"]["content"]
        for item in parsed_data
        if "message" in item and "content" in item["message"]
    )


def main():
    # 用于存储对话上下文，包含用户和助手的消息
    conversation = []
    print("进入对话模式，输入 'q' 退出。")

    while True:
        user_input = input("你：")
        if user_input.strip().lower() == "q":
            print("退出对话。")
            break

        # 将用户输入添加到对话上下文中
        conversation.append({"role": "user", "content": user_input})

        # 发送当前对话上下文给模型
        parsed_response = send_message(conversation)
        if parsed_response is None:
            continue

        # 提取模型回复的内容
        assistant_reply = extract_content(parsed_response)
        print("助手：", assistant_reply)

        # 将助手回复添加到对话上下文中，形成持续对话
        conversation.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    main()
