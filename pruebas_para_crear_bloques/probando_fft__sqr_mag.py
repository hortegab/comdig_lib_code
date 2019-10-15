import numpy as np
import math
from matplotlib import pyplot as plt

# Parametros de la senal analiada
f=1378.
Fsamp= 8000. # la frecuencia de muestreo
# La senal discreta 
N=128 
n=np.linspace(0,N-1,N)
t=n/Fsamp
signal=np.cos(2.*math.pi*f*t)
fourier=np.abs(np.fft.fft(signal))
fourier_mejor=np.fft.fftshift(fourier**2)
 
# calculos para relacional la senal discreta con el mundo real
Fmin=-Fsamp/2.
Fresol=Fsamp/N
Fmax=-Fmin-Fresol
f=np.linspace(Fmin,Fmax,N)
 
plt.plot(f,fourier_mejor)
plt.show()
