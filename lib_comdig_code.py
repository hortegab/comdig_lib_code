from gnuradio import blocks
from gnuradio import gr
import numpy as np
from gnuradio import filter
from gnuradio.filter import firdes
import math


####################################################
##     Plantilla: clase e_add_cc                  ##
####################################################
# Nota: para una explicacion bien detallada de lo que significa cada cosa
# abra el archivo plantillas.py

class e_add_cc(gr.sync_block):  
    """Aqui debes explicar como funciona el bloque, los parametros usados. En este caso particular el proposito es que esta clase sirva como ejemplo o plantilla para otras clase. La idea es que cada vez que vayas a crear una clase para un bloque GNU Radio vuelvas aqui ya que no es facil memorizar todos los detalles para crear un bloque GNU Radio. En todo caso, el ejemplo consiste en un bloque para una suma escalada de dos senales complejas. Por lo tanto hay dos senales de entrada y una de salida. Si escala=0.5 lo que se logra es promediar las dos senales"""
    def __init__(self, escala=0.5):
        gr.sync_block.__init__(
            self,
            name='e_add_cc', 
 
            in_sig=[np.complex64,np.complex64], 
            out_sig=[np.complex64]
        )
        self.escala=escala
        self.coef = 1.0
    
    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        out0 = output_items[0]
        out0[:]=(in0+in1)*self.escala/self.coef
        return len(out0)

####################################################
##     clase e_add_ff                             ##
####################################################
class e_add_ff(gr.sync_block):  
    """consiste en un bloque para una suma escalada de dos senales reales. Por lo tanto hay dos senales de entrada y una de salida. Si escala=0.5 lo que se logra es promediar las dos senales"""
     
    def __init__(self, escala=0.5):
 
        gr.sync_block.__init__(
            self,
            name='e_add_ff', 
            in_sig=[np.float32,np.float32], 
            out_sig=[np.float32]
        )
        self.escala=escala
    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        out0 = output_items[0]
        out0[:]=(in0+in1)*self.escala
        return len(out0)

####################################################
##     clase e_vector_fft_ff                      ##
####################################################
class e_vector_fft_ff(gr.sync_block):
    """calcula la fft en magnitud a una senal vectorial de N muestras y emtrega N muestras del espectro. N deber ser potencia de 2"""

    def __init__(self, N=128):  
        gr.sync_block.__init__(
            self,
            name='e_vector_fft_ff',   
            in_sig=[(np.float32,N)],
            out_sig=[(np.float32,N)]
        )
        self.N = N

    def work(self, input_items, output_items):
        in0 = input_items[0]
    	out0 = output_items[0]
    	out0[:]=abs(np.fft.fftshift(np.fft.fft(in0,self.N),1)) 
        return len(output_items[0])


####################################################
##     clase e_vector_average_hob                   ##
####################################################
 
class e_vector_average_hob(gr.sync_block):
    """
    El bloque vector_averager_hob recibe una senal con tramas de tamano fijo de N valores y va entregando una trama del mismo tamano que corresponde a la trama media de todas las tramas que va recibiendo. 
Los parametros usados son:
N:        Es el tamano del vector o trama
Nensayos: Es el umbral que limita el numero maximo de promedios correctamente realizados. Cuando a la funcion se le ha invocado un numero de veces mayor a Nensayos, el promedio continua realizandose, pero considerando que el numero de promedios realizado hasta el momento ya no se incrementa, sino que es igual a Nensayos. 
    """
 
    def __init__(self, N, Nensayos):
        gr.sync_block.__init__(self, name="vector_average_hob", in_sig=[(numpy.float32, N)], out_sig=[(numpy.float32, N)])
 
        # Nuestras variables especificas
        self.N=N
        self.Nensayos=np.uint64=Nensayos
        self.med=np.empty(N,dtype=np.float64)
        self.count=np.uint64=0
 
    def work(self, input_items, output_items):
 
        # Traduccion de matrices 3D a 2D 
        in0 = input_items[0]
        out0=output_items[0]
        
        # El tamano de la matriz in0 es L[0]xL[1]=L[0]xN
        L=in0.shape
 
        # conteo de funciones muestras (filas de matriz) procesadas
        if self.count < self.Nensayos:
            self.count += L[0] 
 
        # La media de las funciones muestras (filas de matriz) que tiene in0
        mean=in0.mean(0)    
 
        # ajuste de la media ya calculada, con la media de in0
        self.med = (self.med*(self.count-L[0])+mean*L[0])/self.count
 
        # Entrega de resultado
        out0[:]=self.med
        return len(out0)

####################################################
##          e_vector_psd_ff                       ##
####################################################
class e_vector_psd_ff(gr.sync_block):
    """calcula la fft en magnitud a una senal vectorial de N muestras y emtrega N muestras del espectro. N deber ser potencia de 2"""

    def __init__(self, N=128, Nensayos=10000):  
        gr.sync_block.__init__(
            self,
            name='e_vector_fft_ff',   
            in_sig=[(np.float32,N)],
            out_sig=[(np.float32,N)]
        )
        self.N = N
        self.Nensayos=np.uint64=Nensayos
        self.med=np.empty(N,dtype=np.float64)
        self.count=np.uint64=0

    def vec_average(self, in0):
        # El tamano de la matriz in0 es L[0]xL[1]=L[0]xN
        L=in0.shape
 
        # conteo de funciones muestras (filas de matriz) procesadas
        if self.count < self.Nensayos:
            self.count += L[0] 
 
        # La media de las funciones muestras (filas de matriz) que tiene in0
        mean=in0.mean(0)    
 
        # ajuste de la media ya calculada, con la media de in0
        self.med = (self.med*(self.count-L[0])+mean*L[0])/self.count
 
        # Entrega de resultado
        # in0[:]=self.med # asi se entregaria el resultado modificando la misma entrada
        # return self.med

    def work(self, input_items, output_items):
        in0 = input_items[0]
    	out0 = output_items[0]
    	self.vec_average(abs(np.fft.fftshift(np.fft.fft(in0,self.N),1))**2)
        out0[:]=self.med
        return len(output_items[0])

#################################################################
##             Generador de funciones aleatorias               ##
#################################################################
class e_generador_fun_f(gr.hier_block2):

    def __init__(self, Sps=4, h=[1,1,1,1]):
        gr.hier_block2.__init__(
            self, "e_generador_fun_f",
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_float*1),
        )
        ##################################################
        # Parameters
        ##################################################
        self.Sps = Sps
        self.h = h
        ##################################################
        # Blocks
        ##################################################
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(Sps, (h))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((2., ))
        self.blocks_int_to_float_0 = blocks.int_to_float(1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-0.5, ))
        self.analog_random_source_x_0 = blocks.vector_source_i(map(int, np.random.randint(0, 2, 1000000)), True)
        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_int_to_float_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_int_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self, 0))

    def get_Sps(self):
        return self.Sps

    def set_Sps(self, Sps):
        self.Sps = Sps

    def get_h(self):
        return self.h

    def set_h(self, h):
        self.h = h
        self.interp_fir_filter_xxx_0.set_taps((self.h))

from eyediagram.demo_data import demo_data
from eyediagram.mpl import eyediagram
import matplotlib.pyplot as plt

#################################################################
##                         DIAGRAMA DE OJO                     ##
#################################################################

class vec_diagrama_ojo_f(gr.sync_block):  
    """hecho por: Homero Ortega Boada. Permite obtener el diagrama de ojo"""

    def __init__(self, Sps=8, N1=2048):
        gr.sync_block.__init__(self, name='vec_diagrama_ojo_f', in_sig=[(np.float32, N1)], out_sig=None)
        self.Sps = Sps
	self.N1 = N1

    def work(self, input_items, output_items):
        in0 = input_items[0] # in0 es un 2D array (como una matrix)
        y=in0.reshape(-1)    # Esto traduce el 2D array a 1D array (a un vector)
        y=y/(y.max()*2.)     # Esto normaliza los valores de y
                     
        obj_ojo=eyediagram(y, 2*self.Sps, offset=int(self.Sps/2), cmap=plt.cm.coolwarm)
        
        #plt.show()
        plt.pause(0.0000001)
        plt.clf()
        return len(input_items[0])
#################################################################
##                         DIAGRAMA DE OJO OPCION 2            ##
#################################################################

class vec_diagrama_ojo2_f(gr.sync_block):  
    """hecho por: Homero Ortega Boada. Permite obtener el diagrama de ojo"""

    def __init__(self, Sps=8, N2=2048):
        gr.sync_block.__init__(self, name='vec_diagrama_ojo_f', in_sig=[(np.float32, N2)], out_sig=None)
        self.Sps = Sps
        self.N2 = N2

    def work(self, input_items, output_items):
        in0 = input_items[0] # in0 es un 2D array (como una matrix)
        s=in0[0]    # Esto traduce el 2D array a 1D array (a un vector)
        L=len(s)
        L2=L/2.
        t = np.linspace(-L2,L2-1, L)
        plt.plot(t,s)             
        plt.pause(0.0000001)
        return len(input_items[0])
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!                    FUNCIONES PURAS                         !!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#######################################################
##               Forma rectangular                   ##
#######################################################                       
def rect(Sps):
    return Sps*[1.,]

#######################################################
##               Forma de Nyquist                    ##
#######################################################                       
def nyq(Sps,ntaps):
    n=np.linspace(-int(ntaps/2), int(ntaps/2-1),ntaps)
    h=np.sinc(n/Sps)
#    return h/numpy.amax(h)
    return h
#######################################################
##               Forma Coseno Alzado                 ##
#######################################################                       
def rcos(Sps,ntaps,beta):
    if beta==0:
        h=nyq(Sps,ntaps)
    else:
        h=ntaps*[0,]
        for n in range(ntaps):
            k=n-ntaps/2. # esto es para que h[n] quede centrada en la mitad del vector
            if abs(k)==Sps/(2.*beta):
                h[n]=np.sinc(1./(2.*beta))*math.pi/4.
            else:
                h[n]=np.sinc(k/Sps)*math.cos(beta*k*math.pi/Sps)/(1.-(2.*beta*k/Sps)**2)                
    Amp=np.amax(h)
    return h/Amp
#######################################################
##            Forma Raiz de Coseno Alzado            ##
#######################################################                       

def rrcos(Sps,ntaps,beta):
    if beta==0:
        h=nyq(Sps,ntaps)
    else:
        h=ntaps*[0,]
        beta4=4.*beta
        for n in range(ntaps):
            k=n-ntaps/2. # esto es para que h[n] quede centrada en la mitad del vector
            if k==0:
                h[n]=1+beta*(4./math.pi-1.)
            elif abs(k)==Sps/beta4:
                ha=(1.+2./math.pi)*math.sin(math.pi/beta4)
                hb=(1.-2./math.pi)*math.cos(math.pi/beta4)
                h[n]=(ha+hb)*beta/math.sqrt(2.)
            else:
                ks=k/Sps
                kspi=math.pi*ks
                Num=math.sin(kspi*(1-beta))+beta4*ks*math.cos(kspi*(1+beta))
                Den=kspi*(1.-(beta4*ks)**2)
                h[n]=Num/Den                
    Amp=np.amax(h)
    return h/Amp
########################################################
##     Bipolar non return to zero level signal        ##
########################################################
def B_NRZ_L(Sps):
    return Sps*[1.,]

########################################################
##  Forma sinc . Es la misma nyq() que aparece arriba ##
########################################################
def sinc(Sps,ntaps):
    n=np.linspace(-int(ntaps/2), int(ntaps/2-1),ntaps)
    h=np.sinc(n/Sps)
    return h
########################################################
##              forma diente se sierra                ##
########################################################
def saw(Sps):
    return np.linspace(0,Sps-1,Sps)/Sps	
########################################################
#         Bipolar non return to zero signal           ##
########################################################
def RZ(Sps):
    h=Sps*[1.,]
    Sps_m=int(Sps/2)
    h[Sps_m+1:Sps:1]=np.zeros(Sps-Sps_m)
    return h
