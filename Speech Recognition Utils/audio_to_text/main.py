#!/usr/bin/python3

import speech_recognition as sr
import os
from pydub import AudioSegment


'''
/*JS for showing voice messages hrefs from vk*/
var voice_msgs = document.querySelectorAll('[id^="audiomsgpl_"');
for (let i=0; i < voice_msgs.length; i++) {
    console.log(voice_msgs[i].getAttribute('data-audio'));
}
'''

dir = 'audio'
audio_s = os.listdir(dir)


for audio_file in audio_s:

    file_ext = os.path.splitext(audio_file)[1][1:]

    # export audio to wav
    sound = AudioSegment.from_file(os.path.join(dir, audio_file), file_ext)
    wav_path = os.path.join('audio_wav', audio_file.split('.')[0] + '.wav')
    if not os.path.exists('audio_wav'):
        os.mkdir('audio_wav')
    sound.export(wav_path, format="wav")


    r = sr.Recognizer()

    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)

    try:
        s = r.recognize_google(audio, language='ru-RU')
        print('Text: ' + s)
        print()
        with open('output.txt', 'a') as f:
            f.write('File: {}\n'.format(wav_path))
            f.write('Recognized:\n')
            f.write(s + '\n\n')
    except Exception as e:
        print('Exception: ' + str(e))

