from pyaudio import PyAudio, paFloat32

pa = PyAudio()

stream = pa.open(format = paFloat32,
                 channels = 1,
                 rate = 44100,
                 output = True,
                 frames_per_buffer = 1024,
		)
while stream.is_active():
    sleep(0.1)

stream.close()
pa.terminate()
