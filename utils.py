import tempfile
import logging

from gtts import gTTS
from pydub import AudioSegment

import speech_recognition as sr

recognizer = sr.Recognizer()


def tts(text, lang):
    audio = gTTS(text, lang=lang)
    file = tempfile.NamedTemporaryFile()
    audio.save(file.name)
    AudioSegment.from_mp3(file.name).export(file.name, format="ogg", codec="libopus")
    return file


def stt(file, lang):
    try:
        AudioSegment.from_ogg(file.name).export(file.name, format="wav")
        with sr.AudioFile(file.name) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language=lang)
    except sr.UnknownValueError:
        raise ValueError
    except sr.RequestError as er:
        logging.error(er)
