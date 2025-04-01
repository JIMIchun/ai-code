import speech_recognition as sr


def list_microphones():
    """列出系统中的所有可用麦克风设备"""
    mic_list = sr.Microphone.list_microphone_names()
    if not mic_list:
        print("⚠️ 没有找到任何可用的麦克风设备！")
        return []

    print("可用的麦克风设备：")
    for i, mic in enumerate(mic_list):
        print(f"{i}: {mic}")
    return mic_list


def get_microphone_index(mic_list):
    """让用户选择一个麦克风设备"""
    while True:
        try:
            index = int(input(f"请选择麦克风设备（0 - {len(mic_list) - 1}）: "))
            if 0 <= index < len(mic_list):
                return index
            else:
                print("⚠️ 选择的设备索引无效，请重新输入。")
        except ValueError:
            print("⚠️ 请输入有效的数字索引。")


def callback(recognizer, audio):
    """处理音频输入并进行语音识别"""
    try:
        text = recognizer.recognize_google(audio, language='zh-CN')
        print(f"📝 识别结果: {text}")
    except sr.UnknownValueError:
        print("⚠️ 无法识别音频")
    except sr.RequestError as e:
        print(f"❌ 请求错误: {e}")


def listen_and_recognize(device_index):
    """启动麦克风并监听音频"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=device_index)

    with mic as source:
        # 根据环境噪音调整能适当提高识别准确率
        print("🎙️ 正在准备麦克风...")
        recognizer.adjust_for_ambient_noise(source)
        print("🎙️ 麦克风已开启，请开始讲话！")

    # 后台监听，并传入回调函数处理音频
    stop_listening = recognizer.listen_in_background(mic, callback)

    print("按 Ctrl+C 停止监听")
    try:
        while True:
            pass  # 保持程序运行，等待识别
    except KeyboardInterrupt:
        stop_listening()  # 停止后台监听
        print("👋 已停止监听")


if __name__ == "__main__":
    # 获取并列出所有麦克风设备
    mic_list = list_microphones()

    if mic_list:
        # 获取用户选择的设备索引
        device_index = get_microphone_index(mic_list)
        # 开始监听并进行语音识别
        listen_and_recognize(device_index)
