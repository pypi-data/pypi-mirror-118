import numpy as np
from copy import copy
from numpy.linalg import inv
from scipy.linalg import expm
from numpy.linalg import pinv
from scipy import signal
import matplotlib.pyplot as plt

def GL(f, fl, n):
    return ( (f/fl)**(2*n)/(1 + (f/fl)**(2*n)))**0.5

def GH(f, fh, n):
    return ( 1/(1 + (f/fh)**(2*n)) )**0.5

def GB(f, fl, fh, n):
    return GL(f, fl, n)*GH(f, fh, n)

def ins_resp(data, dt, periods, ζ = 0.05):

	'''  
	The function generates pseudo-spectral acceleration (PSA), pseudo-spectral velocity (PSV) and spectral displacement (SD) spectra for given damping ratio (xi).
	Spectral ordinates are for linear-elastic single-degree-of-freedom system with unit mass. 


	Reference:
	Wang, L.J. (1996). Processing of near-field earthquake accelerograms: Pasadena, California Institute of Technology.

	This code is converted from Matlab code of Dr. Erol Kalkan, P.E.
	Link:
	https://www.mathworks.com/matlabcentral/fileexchange/57906-pseudo-spectral-acceleration--velocity-and-displacement-spectra?s_tid=prof_contriblnk

	  INPUTS
	  
	data    = numpy array type object (in acceleration (cm/s^2))
	dt      = sampling rate
	periods = spectral periods 
	ζ       = damping factor (Default: 0.05)

	  OUTPUTS
	  
	PSA = Pseudo-spectral acceleration ordinates
	PSV = Pseudo-spectral velocity ordinates
	SD  = spectral displacement ordinates

	REQUIREMENTS:
	scipy, numpy, os, matplotlib
	'''

	A = [];Ae = [];AeB = [];  
	displ_max = np.empty((len(periods)))
	veloc_max = np.empty((len(periods)))
	absacc_max = np.empty((len(periods)))
	foverm_max = np.empty((len(periods)))
	pseudo_acc_max = np.empty((len(periods)))
	pseudo_veloc_max = np.empty((len(periods)))
	PSA = np.empty((len(periods)))
	PSV = np.empty((len(periods)))
	SD = np.empty((len(periods)))

	acc = data
	#vel = data[0].integrate(method='cumtrapz')
	#dist = data[0].integrate(method='cumtrapz')

	''' Spectral solution '''

	for num,val in enumerate(periods):
		omegan = 2*np.pi/val # Angular frequency
		C = 2*ζ*omegan # Two time of critical damping and angular freq.
		K = omegan**2
		y = np.zeros((2,len(acc)))
		A = np.array([[0, 1], [-K, -C]])
		Ae = expm(A*dt)
		temp_1 = Ae-np.eye(2, dtype=int)
		temp_2 = np.dot(Ae-np.eye(2, dtype=int),pinv(A))
		AeB = np.dot(temp_2,np.array([[0.0],[1.0]]))

		for k in np.arange(1,len(acc)):
		  y[:,k] = np.reshape(np.add(np.reshape(np.dot(Ae,y[:,k-1]),(2,1)), np.dot(AeB,acc[k])),(2))

		displ = np.transpose(y[0,:])	# Relative displacement vector (cm)
		veloc = np.transpose(y[1,:])	# Relative velocity (cm/s)
		foverm = (omegan**2)*displ		# Lateral resisting force over mass (cm/s2)
		absacc = -2*ζ*omegan*veloc-foverm	# Absolute acceleration from equilibrium (cm/s2)

		''' Extract peak values '''
		displ_max[num] = max(abs(displ))	# Spectral relative displacement (cm)
		veloc_max[num] = max(abs(veloc))	# Spectral relative velocity (cm/s)
		absacc_max[num] = max(abs(absacc))	# Spectral absolute acceleration (cm/s2)

		foverm_max[num] = max(abs(foverm))			# Spectral value of lateral resisting force over mass (cm/s2)
		pseudo_acc_max[num] = displ_max[num]*omegan**2	# Pseudo spectral acceleration (cm/s2)
		pseudo_veloc_max[num] = displ_max[num]*omegan	# Pseudo spectral velocity (cm/s)

		PSA[num] = pseudo_acc_max[num]	# PSA (cm/s2)
		PSV[num] = pseudo_veloc_max[num]	# PSV (cm/s)
		SD[num] = displ_max[num]		# SD  (cm)

	return PSA, PSV, SD

def Window_parzen(L):
	"""
	L: longitud de la ventana parzen

	return w: Ventada parzen simétrica respecto a 0 y normalizado a 1.
	"""

	n = np.arange(-(L - 1) / 2.0, (L - 1) / 2.0 + 0.5, 1.0)
	w = np.zeros(L)
	for i in range(len(n)):
		if abs(n[i])<=(L-1)/4.0:
			w[i]= (1 - 6 * (abs(n[i]) / (L / 2.0)) ** 2.0 + 6 * (abs(n[i]) / (L / 2.0)) ** 3.0)
		if (((L-1)/4.0 < abs(n[i])) & (abs(n[i])<=(L-1)/2.0)):
			w[i]= 2 * (1 - abs(n[i]) / (L / 2.0)) ** 3.0

	return w

def smoothing(x, L=100):
    w = Window_parzen(L)
    return signal.fftconvolve(x, w, mode='same')/np.sum(w)

def Butterworth_Bandpass(signal, dt, fl, fh, n):
    """
    Hace un Butterworth Bandpass a las frecuencias de la señal

    inputs:                                         examples:
        signal      : señal (array)                         | array de aceleraciones
        dt          : delta de tiempo de la señal           | para itk = 0.01 seg
        fl          : low cut frecuency                     | fl = 0.10 Hz
        fh          : high cut frecuency                    | hf = 40.0 Hz
        n           : orden de corte                        | n = 15
    output:
        filter      : señal filtrada (array)
    """
    FFT = np.fft.rfft(signal)
    f = np.fft.rfftfreq(len(signal), d = dt)
    FFT_filtered = GL(f, fl, n)*FFT*GH(f, fh, n)

    return np.fft.irfft(FFT_filtered)

def integration(y, dt):
	nx = y.shape[0]
	y1 = np.zeros(nx)
	y1[0] = y[0]*dt*0.5
	
	for i in range(1,nx):
		y1[i] = y1[i-1] + (y[i-1] + y[i])*dt*0.5

	return y1 - np.mean(y1)

if __name__ == '__main__':

	dt = 0.01
	tf =3.1416*5 # s
	t = np.arange(0., tf+dt, dt)
	y = np.sin(t)

	yp = integration(y, dt)

	plt.plot(t,y)
	plt.plot(t,yp)
	plt.show()