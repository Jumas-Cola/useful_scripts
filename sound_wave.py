import math
import numpy
import pygame

size = (100, 100)

bits = 16

pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
pygame.display.set_caption('YAHOOOO')
clock = pygame.time.Clock()
_display_surf = pygame.display.set_mode(
    size, pygame.HWSURFACE | pygame.DOUBLEBUF)


def square(frequency):
    sample_rate = 44100
    n_samples = sample_rate*10
    buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
    max_sample = 2**(bits - 1) - 1
    for s in range(n_samples):
        t = float(s) / sample_rate
        buf[s][0] = int(round(max_sample * (frequency * t)))  # left
        buf[s][1] = int(round(max_sample * (frequency * t)))  # right
    return pygame.sndarray.make_sound(buf)


def sin(frequency):
    sample_rate = 44100
    n_samples = sample_rate*10
    buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
    max_sample = 2**(bits - 1) - 1
    for s in range(n_samples):
        t = float(s)/sample_rate
        buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency*t)))  # left
        buf[s][1] = int(round(max_sample*math.sin(2*math.pi*frequency*t)))  # right
    return pygame.sndarray.make_sound(buf)


signal_form = square

key_note = {pygame.K_z: signal_form(523.25),  # C2
            pygame.K_s: signal_form(554.36),  # C#2
            pygame.K_x: signal_form(587.32),  # D2
            pygame.K_d: signal_form(622.26),  # D#2
            pygame.K_c: signal_form(659.26),  # E2
            pygame.K_v: signal_form(698.46),  # F2
            pygame.K_g: signal_form(739.98),  # F#2
            pygame.K_b: signal_form(784.00),  # G2
            pygame.K_h: signal_form(830.60),  # G#2
            pygame.K_n: signal_form(880.00),  # A2
            pygame.K_j: signal_form(932.32),  # A#2
            pygame.K_m: signal_form(987.75),  # B2
            pygame.K_k: signal_form(1046.50),  # C3
            }

while True:
    dt = clock.tick(60) / 1000.0

    for key, note in key_note.items():
        if pygame.key.get_pressed()[key] and (not pygame.mixer.get_busy()):
            note.play(loops=-1)
        elif (not pygame.key.get_pressed()[key]) and pygame.mixer.get_busy():
            note.stop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
