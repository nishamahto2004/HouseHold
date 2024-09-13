import speech_recognition as sr

def voiceSearch():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        # convert speech to text
        text = r.recognize_google(audio_data)
        text = str(text).title()
        return text
    
