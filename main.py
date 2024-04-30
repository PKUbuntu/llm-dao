# entry

import speech_recognition as sr

# 创建一个识别器对象
recognizer = sr.Recognizer()

# 使用默认的麦克风作为音源
with sr.Microphone() as source:
    print("Please speak now...")
    # 监听一段时间以校准麦克风的噪声水平
    recognizer.adjust_for_ambient_noise(source)
    # 捕获到的音频将存储在audio中
    audio = recognizer.listen(source)

try:
    # 使用Google的免费Web API进行语音识别
    text = recognizer.recognize_google(audio, language='zh-CN')  # 使用中文语言模式
    print("You said: " + text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

