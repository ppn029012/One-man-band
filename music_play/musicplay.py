import pygame as pg
import pygame.mixer as pm
pm.init(frequency=44100)
channela=pm.Sound('b4.wav')
channela.play()

pg.time.delay(10)
