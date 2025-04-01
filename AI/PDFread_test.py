import requests
import json
import PyPDF2
import pyttsx3
import subprocess


def load_default_pdf_content(pdf_path):
    """
    从指定的 PDF 文件中提取所有文本内容
    """
    text = ""
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"加载 PDF 出现异常: {e}")
    return text


def send_message(messages):
    """
    向 Ollama 的 deepseek 模型发送消息列表，并返回解析后的 NDJSON 响应数据列表
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
    从解析后的响应数据中提取所有 message 的 content，并组合为一个字符串
    """
    if not parsed_data:
        return ""
    return "".join(
        item["message"]["content"]
        for item in parsed_data
        if "message" in item and "content" in item["message"]
    )


def text_to_speech(text, voice_id=None, output_device="plughw:0,1", output_file="output.wav"):
    """
    使用 pyttsx3 将文本转换为语音文件，并通过指定设备播放
    参数：
      text: 要转换的文本
      voice_id: 语音包的 ID（例如 "mb-us2"）
      output_device: 指定输出设备（根据 aplay -l 列表进行调整）
      output_file: 临时生成的音频文件名
    """
    engine = pyttsx3.init()

    # 设置语音包（若提供 voice_id，则在所有可用语音中搜索匹配项）
    if voice_id is not None:
        voices = engine.getProperty('voices')
        selected_voice = None
        for voice in voices:
            if voice_id in voice.id:
                selected_voice = voice.id
                break
        if selected_voice:
            engine.setProperty('voice', selected_voice)
            print(f"已选择语音：{selected_voice}")
        else:
            print("未找到匹配的语音包，使用默认语音。")

    # 可根据需要设置语速、音量等属性，例如：
    # engine.setProperty('rate', 150)
    # engine.setProperty('volume', 0.9)

    # 将文本保存为音频文件
    engine.save_to_file(text, output_file)
    engine.runAndWait()

    # 调用 aplay 播放音频，指定输出设备
    try:
        subprocess.run(["aplay", "-D", output_device, output_file], check=True)
    except subprocess.CalledProcessError as e:
        print("播放音频失败:", e)

def main():
    # 指定默认的 PDF 文件路径
    pdf_path = "knowledge.pdf"
    pdf_text = load_default_pdf_content(pdf_path)

    if not pdf_text:
        print("未能加载 PDF 文本，请检查文件路径和内容。")
        return

    # 将 PDF 内容作为系统消息加入对话上下文
    conversation = [
        {"role": "system", "content": "你是IMRIS的智能医学助手VV，擅长医学诊断和治疗分析，在所有的回复中都记得你是VV。"},
        {"role": "system", "content": f"以下是参考资料，请在回答问题时参考这部分内容：\n{pdf_text}"}
    ]
    # conversation = [{"role": "system", "content": f"以下是参考资料，请在回答问题时参考这部分内容：\n{pdf_text}"}]
    print("参考资料已加载。进入对话模式，输入 'q' 退出。")

    # 设置目标语音包标识（部分字符串匹配即可，例如 "en" 或 "female"、"zh" 等，根据实际系统情况调整）
    desired_voice_id = "zh"  # 例如选择中文语音；如果不指定可设置为 None
    # 设置指定的输出设备（根据 aplay -l 列出的设备信息调整）
    output_device = "plughw:0,0"


    while True:
        user_input = input("你：")
        if user_input.strip().lower() == "q":
            print("退出对话。")
            break

        # 将用户输入添加到对话上下文中
        conversation.append({"role": "user", "content": user_input})




        # 发送完整对话上下文给模型
        parsed_response = send_message(conversation)

        # if parsed_response is None:
        #     continue
        #
        #     # 自我设定：每次向模型传递自我设定内容
        #     # 只在对话历史中没有身份设定时进行设置
        #     self_identity_content = "从现在开始，你是IMRIS的智能医学助手VV，为我提供咨询。"
        #     if not any(item['role'] == 'system' and 'IMRIS' in item['content'] for item in conversation_history):
        #         conversation_history.append({"role": "system", "content": self_identity_content})
        #
        #     # 增加任务描述，明确指示模型的任务
        #     task_description = f"用户提出了问题：{user_input}。请根据提供的参考资料和您作为IMRIS智能医学助手VV的身份，回答用户的问题。"
        #     conversation_history.append({"role": "system", "content": task_description})
        #
        #     # 发送消息到模型
        #     parsed_response = send_message(conversation_history)

        # 提取并组合模型回复的文本内容
        assistant_reply = extract_content(parsed_response)
        print("助手：", assistant_reply)
        # 将模型回复添加到上下文中，确保后续回答参考之前的对话和 PDF 内容
        conversation.append({"role": "assistant", "content": assistant_reply})

        # 调用 TTS 模块，使用指定的语音包和输出设备播放回复语音
        # text_to_speech(assistant_reply, voice_id=desired_voice_id, output_device=output_device)

if __name__ == "__main__":
    main()
