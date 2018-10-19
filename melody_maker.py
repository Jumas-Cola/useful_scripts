import chippy

# class for simple work with chippy
class Synth:
	def __init__(self, temp):
		self.temp = float(temp)
		self.melody = b''
		self.synth = chippy.Synthesizer(framerate=44100)
	def __note_to_freq(note, octave=2):
		note_num = {'C':0, 'C#':1, 'D':2, 'D#':3, 'E':4, 'F':5, 'F#':6, 'G':7, 'G#':8, 'A':9, 'A#':10, 'B':11}
		freq = 440*2**((24+12*int(octave)+note_num[note.upper()]-69)/12)
		return freq
	def parse_melody(self, melody_list):
		for note in melody_list:
			note_list = note.split('/')
			try:
				length = (60/self.temp)*float(note_list[2])
			except:
				length = (60/self.temp)*1
			try:
				freq = Synth.__note_to_freq(note_list[0],note_list[1])
			except:
				freq = Synth.__note_to_freq(note_list[0])
			self.melody+=self.synth.pulse_pcm(length=length, frequency=freq)
	def save(self, name):
		self.synth.save_wave(self.melody, str(name))


S = Synth(180)
S.parse_melody('C C G G A A G//2 F F E E D D C//2 G G F F E E D D G G F F E E D D C C G G A A G//2 F F E E D D C//2'.split())
S.save('wave.wav')