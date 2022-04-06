#!/usr/bin/python3
## This is an example of a simple sound capture script.
##
## The script opens an ALSA pcm for sound capture. Set
## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:
'''
import alsaaudio, time, audioop
import sys
# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
# importante!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# necesario instalar
# sudo apt-get install python-alsaaudio
inp.setperiodsize(160)
lista=[1]
controlsalida= True
contador=0
for i in range(1,100):
  print(f'{i}')
  contador=contador+1
  # Read data from device
  l,data = inp.read()
  if l:
    # Return the maximum of the absolute value of all samples in a fragment.
    #print audioop.max(data, 2)
    lista.append(audioop.max(data, 2))
    time.sleep(.01)
    if contador==25:
      controlsalida=False
      break
  else:
    time.sleep(.01)
print('a')
suma=0
media=0
contador=0
print('{}'.format(lista))
for i in lista:
  contador=contador+1
  suma+=i
media=suma/contador
print('b')
txt=str(media)
f=open("/tmp/DatosSonido.txt","w")
f.write(txt)
f.close()

print('end')

sys.exit(0)
'''
import pyaudio, audioop, sys
# import wave

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 1


p = pyaudio.PyAudio()  # Create an interface to PortAudio

stream = p.open(format=sample_format,
                  channels=channels,
                  rate=fs,
                  frames_per_buffer=chunk,
                  input=True)

nframes=int(fs / chunk * seconds)
s=0
for i in range(0, nframes):
    data = stream.read(chunk)
    s+=audioop.max(data,2)

with open("/tmp/DatosSonido.txt","w") as fp:
  fp.write(str(int(s/nframes)))

# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

sys.exit(0)
