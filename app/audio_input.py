# 使用 sphinx 来本地识别一句语音

import speech_recognition as sr

# 创建一个识别器对象
recognizer = sr.Recognizer()

# 使用默认的麦克风作为音源
with sr.Microphone() as source:
    print("Please speak now...")
    # 监听一段时间以校准麦克风的噪声水平
    recognizer.adjust_for_ambient_noise(source)
    # 捕获到的音频将存储在audio中
    audio = recognizer.listen(source, timeout=5)

try:
    # 使用 macOS 自带的语音识别器进行语音识别
    print("Ready to recognize...")
    text = recognizer.recognize_sphinx(audio, language='en-US')
    print("You said: " + text)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Recognition request failed; {0}".format(e))


