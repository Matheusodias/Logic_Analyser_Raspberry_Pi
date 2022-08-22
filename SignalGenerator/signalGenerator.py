#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pigpio

GPIO=18

wave = []

#                          ON       OFF    MICROS
wave.append(pigpio.pulse(1<<GPIO, 0,       300))  
wave.append(pigpio.pulse(0,       1<<GPIO, 300))

pi = pigpio.pi() # connect to local Pi
pi.wave_clear()
pi.set_mode(GPIO, pigpio.OUTPUT)
#pi.write(GPIO,0) #Desliga o pino
pi.wave_add_generic(wave)

def periodicSignal(pi, GPIO, delay, duration, period):
    wave = []
    #                          ON       OFF    MICROS
    wave.append(pigpio.pulse(1<<GPIO, 0,       period))  
    wave.append(pigpio.pulse(0,       1<<GPIO, period))
    pi.wave_clear()
    pi.wave_add_generic(wave)
    wid = pi.wave_create()
    time.sleep(delay) #Tempo antes do inicio do sinal
    if wid >= 0:
        pi.wave_send_repeat(wid) #Envia o sinal repetidamente
        time.sleep(duration) #Tempo de duração do sinal
        pi.wave_tx_stop()
        pi.wave_delete(wid)
        pi.write(GPIO,0) #Desliga o pino

def pulseSignal(GPIO, delay, duration, type):
    time.sleep(delay) #Tempo antes do inicio do sinal
    if type == "high":
        pi.write(GPIO,1) #Liga o pino
        time.sleep(duration) #Tempo de duração do sinal
        pi.write(GPIO,0) #Desliga o pino
    else:
        pi.write(GPIO,0)
        time.sleep(duration)
        pi.write(GPIO,1)

def edgeSignal(GPIO, delay, type):
    time.sleep(delay) #Tempo antes do inicio do sinal
    if type == "high":
        pi.write(GPIO,1) #Liga o pino
    else:
        pi.write(GPIO,0)

def patternSignal(GPIO, delay, duration, period, pattern):
    time.sleep(delay) #Tempo antes do inicio do sinal
    wave = []
    for i in range(len(pattern)):
        if pattern[i] == "1":
            wave.append(pigpio.pulse(1<<GPIO, 0,       period))
        else:
            wave.append(pigpio.pulse(0,       1<<GPIO, period))
    wave.append(pigpio.pulse(0,       1<<GPIO, 1000))
    pi.wave_clear()
    pi.wave_add_generic(wave)
    wid = pi.wave_create()
    time.sleep(delay) #Tempo antes do inicio do sinal
    if wid >= 0:
        pi.wave_send_repeat(wid) #Envia o sinal repetidamente
        time.sleep(duration) #Tempo de duração do sinal
        pi.wave_tx_stop()
        pi.wave_delete(wid)
        pi.write(GPIO,0) #Desliga o pino


# periodicSignal(pi, GPIO, 0, 1, 300) #Inicia o sinal periodicamente
# pulseSignal(18,1,0.001,"high")
# edgeSignal(GPIO,1,0.001123,"high")
patternSignal(GPIO ,1, 5, 150, "01010101")