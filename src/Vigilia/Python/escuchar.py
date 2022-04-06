#!/usr/bin/python
## This is an example of a simple sound capture script.
##
## The script opens an ALSA pcm for sound capture. Set
## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:

import alsaaudio, time, audioop

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
	contador=contador+1
	# Read data from device
	l,data = inp.read()
	if l:
		# Return the maximum of the absolute value of all samples in a fragment.
		#print audioop.max(data, 2)
		lista.append(audioop.max(data, 2))
		time.sleep(.01)
		if contador==100:
			controlsalida=False
			break
	else:
		time.sleep(.01)

suma=0
media=0
contador=0
for i in lista:
	contador=contador+1
	suma+=i
media=suma/contador

txt=str(media)
f=open("/tmp/DatosSonido.txt","w")
f.write(txt)
f.close()

