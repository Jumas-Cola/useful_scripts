#!/usr/bin/python3

import speech_recognition as sr
import os
from pydub import AudioSegment
import sys

if not sys.argv[1:]:
    print('\nUsage:\naudiototext.py <path_to_audiofile1> <path_to_audiofile2>...\n')
    sys.exit()

print('\n' + 'Start Recognizing'.center(30, '_') + '\n')

for audio_file in sys.argv[1:]:

    file_path, file_ext = os.path.splitext(audio_file)
    file_ext = file_ext[1:]

    # export audio to wav
    sound = AudioSegment.from_file(audio_file, file_ext)
    wav_path = file_path + '.wav'
    sound.export(wav_path, format="wav")

    r = sr.Recognizer()

    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)

    try:
        s = r.recognize_google(audio, language='ru-RU')
        print('File: {}'.format(audio_file))
        print('Text:')
        print(s + '\n')
        with open('output.txt', 'a') as f:
            f.write('File: {}\n'.format(audio_file))
            f.write('Text:\n')
            f.write(s + '\n\n')
    except Exception as e:
        print('Exception: ' + str(e))

    os.remove(wav_path)

print('Finished'.center(30, '_'))

