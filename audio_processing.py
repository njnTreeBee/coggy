import speech_recognition as sr

def process_audio(audio_data):
    # initialize the recognizer
    r = sr.Recognizer()

    # open the file
    with sr.AudioFile(audio_data) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)

    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    return text
