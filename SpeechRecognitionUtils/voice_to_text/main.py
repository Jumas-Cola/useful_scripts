import speech_recognition as sr
import pyperclip
from pynput.keyboard import Key, Controller
import winsound

options = {
    'write_alias': ('напиши', 'пиши', 'запиши'),
}


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language='ru-RU').lower()
        print('[log] Recognized: "{}"'.format(voice))

        if voice.startswith(options['write_alias']):
            for alias in options['write_alias']:
                if voice.startswith(alias):
                    voice = voice.replace(alias, '', 1).lstrip()
                    if not voice:
                        break
                    voice = voice[0].upper() + voice[1:]
                    break
            write_text(voice)
            print('[log] Text writed')
            winsound.Beep(294, 300)
        else:
            print('[log] Command not found')
            winsound.Beep(262, 200)
            winsound.Beep(220, 200)

    except sr.UnknownValueError:
        print('[log] Voice not recognized!')
    except sr.RequestError as e:
        print('[log] {}'.format(e))


def write_text(text):
    pyperclip.copy(text)
    keyboard = Controller()
    keyboard.press(Key.ctrl.value)
    keyboard.press('v')
    keyboard.release('v')
    keyboard.release(Key.ctrl.value)


# запуск
rec = sr.Recognizer()
mic = sr.Microphone(device_index=2)
rec.dynamic_energy_adjustment_damping = 0.08
rec.dynamic_energy_adjustment_ratio = 2
rec.pause_threshold = 0.5

# with mic as source:
#     rec.adjust_for_ambient_noise(source)
# stop_listening = rec.listen_in_background(mic, callback)
# while True:
#     time.sleep(0.1)

while True:
    with mic as source:
        try:
            rec.adjust_for_ambient_noise(source, duration=1)
            audio = rec.listen(source)
            callback(rec, audio)
        except Exception as e:
            with open('error.log', 'a') as err_log:
                err_log.write('[log] Crash! {}\n'.format(str(e)))
            print('[log] Crash! {}'.format(str(e)))
