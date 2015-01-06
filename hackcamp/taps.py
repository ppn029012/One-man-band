import numpy as np
#import pyaudio
import struct
import math
# import pylab as pl
import time
import pygame as pg
import pygame.mixer as pm
import alsaaudio, time, audioop


pm.init()
string=['a','b','c','d']
channela=pm.Sound('beat.wav')
channelb=pm.Sound('hihat.wav')
channelc=pm.Sound(string[0]+'.wav')
channeld=pm.Sound(string[1]+'.wav')
channele=pm.Sound(string[2]+'.wav')
channelf=pm.Sound(string[3]+'.wav')
channelg=pm.Sound(string[0]+'b'+'wav')
channelh=pm.Sound(string[1]+'b'+'wav')

INITIAL_TAP_THRESHOLD = 0.510
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
inp.setchannels(1)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
SHORT_NORMALIZE = (1.0/32768.0) 
inp.setrate(44100)
INPUT_BLOCK_TIME = 0.05
#INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
inp.setperiodsize(160)
# inp.setperiodsize(int(44100*INPUT_BLOCK_TIME))
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME 
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

def get_rms( shorts ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.

    # iterate over the block.
    sum_squares = 0.0
    count = len(shorts) /2 
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n
        
    return math.sqrt( sum_squares / count )

class TapTester(object):
    def __init__(self):
        #self.pa = pyaudio.PyAudio()
        #self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount = MAX_TAP_BLOCKS+1 
        self.quietcount = 0 
        self.errorcount = 0

    def stop(self):
        self.stream.close()


    def tapDetected(self):
        print "Tap!"

    def listen(self):
        try:
            # block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
            l,data = inp.read()
            print "DATA:"
            print data
        except IOError, e:
            # dammit. 
            self.errorcount += 1
            #print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return

        # amplitude = get_rms( data )
        amplitude = 10
        if l:
    	    count = len(data)/2
            format = "%dh"%(count)
            shorts = struct.unpack( format, data )
            print shorts
	    amp = np.fft.fft(shorts)
	    N = len(amp)
	    amp = 20*np.log(amp)
	    amp = amp[1:N/2]
	    amp_max = max(amp[1:])
	    thre = 0.8*amp_max 
	    ploc = [i for i in range(1,len(amp)-1) if amp[i]>amp[i-1] and amp[i]>amp[i+1] and amp[i]>thre]
	    if len(ploc)>=4:
		ploc_freq = [i*44100/1024 for i in ploc]
		if ploc_freq[0] <= 258:
			#ceg
		    string[0]='c3'
		    string[1]='e3'
		    string[2]='g3'
		    string[3]='c4'
		    channela.set_volume(0.2)
		elif ploc_freq[0] <= 301:
			#e
		    string[0]='e3'
		    string[1]='ga3'
		    string[2]='b4'
		    string[3]='e4'
		    channela.set_volume(0.3)
		elif ploc_freq[0] <= 344:
			#fg
		    string[0]='fg3'
		    string[1]='ab4'
		    string[2]='cd4'
		    string[3]='fg4'
		    channela.set_volume(0.6)
		elif ploc_freq[0] >= 387:
			#ga
		    string[0]='ga3'
		    string[1]='c4'
		    string[2]='de4'
		    string[3]='ga4'
		    channela.set_volume(1.0)
		pm.music.load(string[0]+'b'+'.wav')
	        pm.music.play() 
		channela.play()
		channelb.play()
		channelc.play()
		channeld.play()
		channelh.play()

if __name__ == "__main__":
   # pl.ion()
   # fig = pl.figure()
    
    pm.init()
    tt = TapTester()
    for i in range(1000):
        tt.listen()
