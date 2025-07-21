
from flask import Blueprint, request, jsonify
import sounddevice as sd
import wavio
import tempfile
from threading import Lock
import numpy as np
import whisper
import os

voice_bp = Blueprint("voice", __name__)

# whisper 控制语音输入/输出

# 全局录音控制变量
recording = False
stream = None
audio_frames = []
lock = Lock()
def audio_callback(indata, frames, time, status):
    global audio_frames
    if recording:
        with lock:
            audio_frames.append(indata.copy())

@voice_bp.route('/start_record', methods=['POST'])
def start_record():
    global recording, stream, audio_frames
    # 停止之前的录音流并重置状态
    if recording:
        try:
            stream.stop()
            stream.close()
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    # 重新初始化录音状态和音频帧列表
    recording = True
    audio_frames = []
    
    try:
        stream = sd.InputStream(
            samplerate=16000,
            channels=1,
            dtype='int16',
            callback=audio_callback
        )
        stream.start()
        return jsonify({'status': 'success'})
    except Exception as e:
        recording = False
        return jsonify({'status': 'error', 'message': str(e)})

@voice_bp.route('/stop_record', methods=['POST'])
def stop_record():
    global recording, stream, audio_frames
    if recording:
        recording = False
        stream.stop()
        stream.close()
        
        try:
            with lock:
                if not audio_frames:
                    return jsonify({'status': 'error', 'message': '未检测到录音内容'})
                audio_data = np.concatenate(audio_frames, axis=0)
            
            # 写入临时文件并识别
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                wavio.write(f.name, audio_data, 16000, sampwidth=2)
                
                model = whisper.load_model("base")
                result = model.transcribe(f.name, language="zh", initial_prompt="请使用简体中文转写,并使用标准中文标点符号：，。！？；：")
                    
            os.unlink(f.name)
            return jsonify({'status': 'success', 'result': result})
        
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    return jsonify({'status': 'error', 'message': '没有进行中的录音'})

