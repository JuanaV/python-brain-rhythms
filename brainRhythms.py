""" --Juana Valeria Hurtado Rincon Julio 2015-- 
	Library for GCPDS devices processing
	Python development tool for EEG-based Brain Computer Interface
	Rhythms analysis EEG python module
	python development tool for EEG-based rhythms """


from numpy import fft
import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from emokit import emotiv
import gevent

def readEEG(Fs,time,ch):
	"""Return EEG matrix nxm (n:time,m:channels) from Emotiv
		Parameters: Fs: -int- sampling frequency
					time: -int- time recording
					ch: -int- number of channels
		Returns: EEG: -ndarray- EEG signal
				 headset: -object- emotiv headset -> emotiv.Emotiv()"""
	headset = emotiv.Emotiv()
	gevent.spawn(headset.setup)
	gevent.sleep(1)

	samples = int(Fs*time)
	EEG = np.zeros(shape=(samples, ch))
	for i in xrange(samples):
		packet = headset.dequeue()
		
		EEG[i,0]=value = int(''.join(map(str,list(packet.F3)))) #Tuple to int
		EEG[i,1]=value = int(''.join(map(str,list(packet.F4)))) #Tuple to int
		EEG[i,2]=value = int(''.join(map(str,list(packet.P7)))) #Tuple to int
		EEG[i,3]=value = int(''.join(map(str,list(packet.FC6)))) #Tuple to int
		EEG[i,4]=value = int(''.join(map(str,list(packet.F7)))) #Tuple to int
		EEG[i,5]=value = int(''.join(map(str,list(packet.F8)))) #Tuple to int
		EEG[i,6]=value = int(''.join(map(str,list(packet.T7)))) #Tuple to int
		EEG[i,7]=value = int(''.join(map(str,list(packet.P8)))) #Tuple to int
		EEG[i,8]=value = int(''.join(map(str,list(packet.FC5)))) #Tuple to int
		EEG[i,9]=value = int(''.join(map(str,list(packet.AF4)))) #Tuple to int
		EEG[i,10]=value = int(''.join(map(str,list(packet.T8)))) #Tuple to int
		EEG[i,11]=value = int(''.join(map(str,list(packet.O2)))) #Tuple to int
		EEG[i,12]=value = int(''.join(map(str,list(packet.O1)))) #Tuple to int
		EEG[i,13]=value = int(''.join(map(str,list(packet.AF3)))) #Tuple to int
		
		#gevent.sleep(0)

	#headset.close()
	
	return(EEG, headset)

def readEEG2(Fs,time,ch,headset):
	"""Return EEG matrix nxm (n:time,m:channels) from Emotiv
		Parameters: Fs: -int- sampling frequency
					time: -int- time recording
					ch: -int- number of channels
					headset: -object- emotiv headset -> emotiv.Emotiv()
		Returns: EEG: -ndarray- EEG signal"""
	
	samples = int(Fs*time)
	EEG = np.zeros(shape=(samples, ch))
	for i in xrange(samples):
		packet = headset.dequeue()
		
		EEG[i,0]=value = int(''.join(map(str,list(packet.F3)))) #Tuple to int
		EEG[i,1]=value = int(''.join(map(str,list(packet.F4)))) #Tuple to int
		EEG[i,2]=value = int(''.join(map(str,list(packet.P7)))) #Tuple to int
		EEG[i,3]=value = int(''.join(map(str,list(packet.FC6)))) #Tuple to int
		EEG[i,4]=value = int(''.join(map(str,list(packet.F7)))) #Tuple to int
		EEG[i,5]=value = int(''.join(map(str,list(packet.F8)))) #Tuple to int
		EEG[i,6]=value = int(''.join(map(str,list(packet.T7)))) #Tuple to int
		EEG[i,7]=value = int(''.join(map(str,list(packet.P8)))) #Tuple to int
		EEG[i,8]=value = int(''.join(map(str,list(packet.FC5)))) #Tuple to int
		EEG[i,9]=value = int(''.join(map(str,list(packet.AF4)))) #Tuple to int
		EEG[i,10]=value = int(''.join(map(str,list(packet.T8)))) #Tuple to int
		EEG[i,11]=value = int(''.join(map(str,list(packet.O2)))) #Tuple to int
		EEG[i,12]=value = int(''.join(map(str,list(packet.O1)))) #Tuple to int
		EEG[i,13]=value = int(''.join(map(str,list(packet.AF3)))) #Tuple to int
		
		#gevent.sleep(0)

	#headset.close()
	
	return(EEG)

def normalizeEEG(EEG):
	"""Return EEG normalized matrix
		Parameters: EEG: -ndarray- EEG matrix(time x ch)
		Returns: EEG_n: -ndarray- Normalized EEG signal"""
	
	EEG_n = np.zeros(shape=(EEG.shape))
	for u in range(EEG.shape[1]):
		EEG_n[:,u] = (( EEG[:,u] - np.mean(EEG[:,u]))+100*(u+1)).transpose()
	return(EEG_n)

def getChannels(EEG,ch_list):
	"""Return the EEG data of the given channel list and the new ch number
		Parameters: EEG: -ndarray- EEG matrix(time x ch)
			   		ch_list: -1xn array- contains the numbers that corresponds with the desired channels
			   		0:F3, 1:F4, 2:P7, 3:FC6, 4:F7, 5:F8, 6:T7, 7:P8, 8:FC5, 9:AF4, 10:T8, 11:O2, 12:O1, 13:AF3
		Returns: EEG_c: -ndarray- Normalized EEG signal 
				 ch: -int- New number of channels
		Examples: 1) getChannels(EEG,[0,3,4,5,10,11,12])
				  2)ch_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
				 	getChannels(EEG,ch_list)"""

	EEG_c = np.zeros(shape=(EEG.shape[0], len(ch_list)))
	for c in range(len(ch_list)):
		EEG_c[:,c] = EEG[:,ch_list[c]]
	ch = len(ch_list)

	return EEG_c, ch

def saveEEGTxt(EEG,filename,Header):
	"""Save the EEG signal in a .txt file
		Parameters: EEG: -ndarray- EEG matrix(time x ch)
					filename: -str- Name of the file
					header: -str- Header of the file"""
	m = np.asmatrix(EEG)
	np.savetxt(filename + '.txt', m,fmt='%.d',header=str(Header), comments='')

def rhythmsBasicWaves( fs, dx, EEG):
	"""Return the basic rhythms (delta, theta, alpha, beta) energy mean of the given EEG signal
		Parameters: EEG: -ndarray- EEG matrix(time x ch)
					fs: -int- Sampling frequency
					dx: -int- 1/fs
		Returns: rhythm_mean: -1x4 array- Rhythms energy """
	#fs: Is the sampling frequency
	#dx: Is 1/fs
	#EEG: EEG matrix size: time,ch


	#Ritmos delta 0-4 Hz.
	#Actividad theta: 4-7 Hz.
	#Ritmos alfa: 8-13 Hz.
	#Ritmos beta: 14-60 Hz.

	delta = [0.8,4]
	theta = [4,7]
	alfa  = [8,13]
	beta  = [14,60]

	freq_rhythms=[delta[0],delta[1],theta[0],theta[1],alfa[0],alfa[1],beta[0],beta[1]] # vector con en rango de frecuencia de los ritmos

	X = EEG                                   # Cargar un archivo txt con el EEG

	[m,n] = X.shape                                                         # Tama\no de la matriz cargada

	if (m % 2 != 0):                                                    #Dejando como numero par el tama\no
		X = X[0:m-1,:]                                                  #(evitar problemas al tomar la parte positiva de la transformada)
	
 

	[m,n] = X.shape
	Y = np.zeros(shape=(m,n))                                               # Creando matrices a utilzar
	f = np.zeros(shape=(m,n))
	Yf = np.zeros(shape=(m/2,n))
	ff = np.zeros(shape=(m/2,n))
	prom  = np.zeros(len(freq_rhythms)/2)
	for i in range(n):
		Y[:,i] = fft.fft(X[:,i])                                            # Transformada rapida de Fourier
		Y[:,i]= fft.fftshift(Y[:,i])                                        # Centrando en cero los valores
		Yf[:,i] = Y[len(Y)/2:,i]                                            # Tomando la parte positiva
		
		f[:,i] = fft.fftfreq(len(X[:,i]),0.0078125)                             # Eje de las frecuencias, !!!!!!cuidado con el dx
		f[:,i] = fft.fftshift(f[:,i])                                       # Centrando en cero los valores
		ff[:,i] = f[len(f)/2:,i]                                            # Tomando la parte positiva
		
	Yff = np.sum(Yf,axis=1)                                                 #Sumando en la frecuencia los canales
	ff = ff[:,0]

	posi = []
	for p in range(len(freq_rhythms)): 
		freq_rhythms2 = min(ff, key=lambda x:abs(x-freq_rhythms[p]))        #Encontrando los valores mas cercanos al rango de frec de los ritmos
		posi.append(np.where(ff == freq_rhythms2))                          #en el eje de las frecuencias. Buscando en el eje de las frec las
	                                                                        # posiciones en las que estan los valores ya encontrados


	q = 0
	for j in range(len(freq_rhythms)/2):                                                      # Promedio de la energia en cada rango de frec
		ini = posi[q]
		fin = posi[q+1]
		prom[j] = np.mean(np.square(np.real(Yff[ini[0]:fin[0]])))
		q=q+2

	#print 'delta, theta, alfa, beta'
	rhythm_mean = prom
	return rhythm_mean

def rhythmsAllWaves( fs, dx, EEG):
	"""Return the rhythms  energy mean of the given EEG signal
		Parameters: EEG: -ndarray- EEG matrix(time x ch)
					fs: -int- Sampling frequency
					dx: -int- 1/fs
		Returns: rhythm_mean: -1x4 array- Rhythms energy
				 delta, theta, low_alpha, high_alpha, low_beta, high_beta, low_gamma, high_gamma"""
	
	#fs: Is the sampling frequency
	#dx: Is 1/fs
	#EEG: EEG matrix size: time,ch


	#Ritmos delta 0-4 Hz.
	#Actividad theta: 4-7 Hz.
	#Ritmos alfa: 8-13 Hz.
	#Ritmos beta: 14-60 Hz.

	delta = [1.5,3]
	theta = [4,7]
	low_alpha = [7.5,12.5]
	high_alpha = [8,15]
	low_beta = [12.5, 18]
	high_beta = [18,30]
	low_gamma = [30,40]
	high_gamma = [35,60]

	freq_rhythms=[delta[0],delta[1],theta[0],theta[1],low_alpha[0],low_alpha[1],high_alpha[0],high_alpha[1],low_beta[0],low_beta[1],high_beta[0],high_beta[1],low_gamma[0],low_gamma[1],high_gamma[0],high_gamma[1]] # vector con en rango de frecuencia de los ritmos

	X = EEG                                   # Cargar un archivo txt con el EEG

	[m,n] = X.shape                                                         # Tama\no de la matriz cargada

	if (m % 2 != 0):                                                    #Dejando como numero par el tama\no
		X = X[0:m-1,:]                                                  #(evitar problemas al tomar la parte positiva de la transformada)
	                                                                        #(evitar problemas al tomar la parte positiva de la transformada)
	[m,n] = X.shape
	Y = np.zeros(shape=(m,n))                                               # Creando matrices a utilzar
	f = np.zeros(shape=(m,n))
	Yf = np.zeros(shape=(m/2,n))
	ff = np.zeros(shape=(m/2,n))
	prom  = np.zeros(len(freq_rhythms)/2)
	for i in range(n):
		Y[:,i] = fft.fft(X[:,i])                                            # Transformada rapida de Fourier
		Y[:,i]= fft.fftshift(Y[:,i])                                        # Centrando en cero los valores
		Yf[:,i] = Y[len(Y)/2:,i]                                            # Tomando la parte positiva
		
		f[:,i] = fft.fftfreq(len(X[:,i]),0.0078125)                             # Eje de las frecuencias, !!!!!!cuidado con el dx
		f[:,i] = fft.fftshift(f[:,i])                                       # Centrando en cero los valores
		ff[:,i] = f[len(f)/2:,i]                                            # Tomando la parte positiva
		
	Yff = np.sum(Yf,axis=1)                                                 #Sumando en la frecuencia los canales
	ff = ff[:,0]

	posi = []
	for p in range(len(freq_rhythms)): 
		freq_rhythms2 = min(ff, key=lambda x:abs(x-freq_rhythms[p]))        #Encontrando los valores mas cercanos al rango de frec de los ritmos
		posi.append(np.where(ff == freq_rhythms2))                          #en el eje de las frecuencias. Buscando en el eje de las frec las
	                                                                        # posiciones en las que estan los valores ya encontrados


	q = 0
	for j in range(len(freq_rhythms)/2):                                                      # Promedio de la energia en cada rango de frec
		ini = posi[q]
		fin = posi[q+1]
		prom[j] = np.mean(np.square(np.real(Yff[ini[0]:fin[0]])))
		q=q+2

	#print 'delta, theta, alfa, beta'

	return prom

def rhythmsFromFile( fs, dx,filename):
	#fs: Is the sampling frequency
	#dx: Is 1/fs
	#filename: Is the name (String type) that Corresponds to a .txt file wich contains the EEG data during a t time


	#Ritmos delta 0-4 Hz.
	#Actividad theta: 4-7 Hz.
	#Ritmos alfa: 8-13 Hz.
	#Ritmos beta: 14-60 Hz.

	delta = [0,4]
	theta = [4,7]
	alfa  = [8,13]
	beta  = [14,60]

	freq_rhythms=[delta[0],delta[1],theta[0],theta[1],alfa[0],alfa[1],beta[0],beta[1]] # vector con en rango de frecuencia de los ritmos

	X = np.loadtxt(filename, skiprows=1)                                   # Cargar un archivo txt con el EEG

	XT = X.transpose()

	[m,n] = XT.shape                                                         # Tama\no de la matriz cargada
	X = XT

	number= 4
	if n % 2 != 0:
		X = X[0:m-1,:]                                                      #Dejando como numero par el tama\no 
	                                                                        #(evitar problemas al tomar la parte positiva de la transformada)
	[m,n] = X.shape
	Y = np.zeros(shape=(m,n))                                               # Creando matrices a utilzar
	f = np.zeros(shape=(m,n))
	Yf = np.zeros(shape=(m/2,n))
	ff = np.zeros(shape=(m/2,n))
	prom  = np.zeros(shape=(1,4))
	for i in range(n):
		Y[:,i] = fft.fft(X[:,i])                                            # Transformada rapida de Fourier
		Y[:,i]= fft.fftshift(Y[:,i])                                        # Centrando en cero los valores
		Yf[:,i] = Y[len(Y)/2:,i]                                            # Tomando la parte positiva
		
		f[:,i] = fft.fftfreq(len(X[:,i]),0.004)                             # Eje de las frecuencias, !!!!!!cuidado con el dx
		f[:,i] = fft.fftshift(f[:,i])                                       # Centrando en cero los valores
		ff[:,i] = f[len(f)/2:,i]                                            # Tomando la parte positiva
		
	Yff = np.sum(Yf,axis=1)                                                 #Sumando en la frecuencia los canales
	ff = ff[:,0]

	posi = []
	for p in range(len(freq_rhythms)): 
		freq_rhythms2 = min(ff, key=lambda x:abs(x-freq_rhythms[p]))        #Encontrando los valores mas cercanos al rango de frec de los ritmos
		posi.append(np.where(ff == freq_rhythms2))                          #en el eje de las frecuencias. Buscando en el eje de las frec las
	                                                                        # posiciones en las que estan los valores ya encontrados


	q = 0
	for j in range(4):                                                      # Promedio de la energia en cada rango de frec
		ini = posi[q]
		fin = posi[q+1]
		prom[0,j] = np.mean(np.square(np.real(Yff[ini[0]:fin[0]])))
		q=q+2

	#print 'delta, theta, alfa, beta'
	#print prom

	return prom[0]

def normalizeRhythms(rhy):
	"""Return normalized rhythms 
		Parameters: rhy: -1xn array- Rhythms energy
		Returns: rhy_n: -1xn array- Normalized Rhythms"""

	rhy_n = (rhy - min(rhy))/max(rhy)*100
	return(rhy_n)

def GraphBar(win,y,c):
	"""	Plot a Bar graphic for each value of y(n array) with its respective color c(n array)"""
	bg1 = pg.BarGraphItem(x=[0], height=[y[0]], width=0.5, brush=c[0])
	bg2 = pg.BarGraphItem(x=[1], height=[y[1]], width=0.5, brush=c[1])
	bg3 = pg.BarGraphItem(x=[2], height=[y[2]], width=0.5, brush=c[2])
	bg4 = pg.BarGraphItem(x=[3], height=[y[3]], width=0.5, brush=c[3])

	win.addItem(bg1)
	win.addItem(bg2)
	win.addItem(bg3)
	win.addItem(bg4)

	win.getAxis('bottom').setTicks([[(0, 'Delta'), (1, 'Theta'), (2, 'Alpha'), (3, 'Beta')]])
	win.setLabel('left', 'Energy', units='%')

def wavesDiagram(E,Deg):
	"""Return the points to plot the Waves Diagram
		Parameters: E: -1xn array- Energy of each rhythm
			   		Deg: -1xn array- Plot angle for each rhythm
		Returns: x: -1xn array- plot points in x axis
				 y: -1xn array- plot points in y axis
		Examples: 1) Deg = [90., 45., 330., 300., 240., 210., 150., 120.]
				  	 xr,yr = mn.wavesDiagram(r,Deg)
				  2)Deg = [90., 45., 0. ,315., 270. , 225., 180., 135.]
				  	 xr,yr = mn.wavesDiagram(r,Deg)"""

	x = np.zeros(len(E)+1)
	y = np.zeros(len(E)+1)
	for i in range(len(E)):
		toDeg = np.pi / 180.
		x[i] = E[i]* np.cos(Deg[i]*toDeg)
		y[i] = E[i]* np.sin(Deg[i]*toDeg)
	x[-1] = x[0]
	y[-1] = y[0]
	
	return x,y
	