#!/usr/bin/python3

import speech_recognition as sr
import os
from pydub import AudioSegment


'''
/*JS for showing voice messages hrefs from vk*/
var voice_msgs = document.querySelectorAll('[id^="audiomsgpl_"');
for (let i=0; i < voice_msgs.length; i++) {
    console.log(voice_msgs[i].getAttribute('data-mp3'));
}
'''

dir = 'audio_mp3'
mp3_s = os.listdir(dir)


for mp3_file in mp3_s:

    # export mp3 to wav
    sound = AudioSegment.from_mp3(os.path.join(dir, mp3_file))
    wav_path = os.path.join('audio_wav', mp3_file.split('.')[0] + '.wav')
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

