import subprocess

def speak(text, voice="mb-cn1", device="plughw:0,0"):
    cmd = ["espeak-ng", "-v", voice, "--stdout", text]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    subprocess.run(["aplay", "-D", device], stdin=p.stdout)
    p.wait()

speak("测试声音")
