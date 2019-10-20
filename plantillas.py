from gnuradio import blocks
from gnuradio import gr
import numpy as np
from gnuradio import filter
from gnuradio.filter import firdes
import math


#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#OOO              Plantilla: clase e_add_cc                              OOO
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

####################################################
##        Recomendaciones Generales               ##
####################################################
# Es conveninte hacer que nombre de una clase finalice con una o dos letras especiales:
# -  nombre_ff: cuando en el bloque sus entradas y salidas son senales reales y de tipo flotante
# -  nombre_f: el bloque solo tiene una entrada o una salida y es una senal real de tipo flotante
# -  En vez de "f" pueden usarse: c (senal compleja),  i (entera), b (binaria), etc.
# -  si el es bloque es vectorial, tambien es importante denotarlo, entonces a las letras
# anteriores le vamos a anteponer las letras vec
# -  No es conveniento antepoler letras distintivas al nombre de un bloque ya que eso
# hace que sea mas dificl de encontrarlo con las ayudas de un IDE com Visual Studio Code
# -  cuando se trate de un bloque jerarquico, los apuntadores a esos bloques los vamos
# a  senalar conmenzando el apuntador con p_, por ejemplo p_fuente=my.e_generador_fun_f()
# Nota: esta plantilla tambien puede ser consultada en la libreria comdig_Lib_Bloques, 
# dentro del bloque b_help
 
class e_add_cc(gr.sync_block):  
    """Aqui debes explicar como funciona el bloque, los parametros usados. En este caso particular el proposito es que esta clase sirva como ejemplo o plantilla para otras clase. La idea es que cada vez que vayas a crear una clase para un bloque GNU Radio vuelvas aqui ya que no es facil memorizar todos los detalles para crear un bloque GNU Radio. En todo caso, el ejemplo consiste en un bloque para una suma escalada de dos senales complejas. Por lo tanto hay dos senales de entrada y una de salida. Si escala=0.5 lo que se logra es promediar las dos senales"""
 
    # Instrucciones:
    # - Dentro de la funcion __init__(), deben definirse los parametros de configuracion del bloque.
    # - A cada parametro se le da un valor por defecto
    # - ejemplo 1, solo hay un parametro de configuracion: def __init__(self, amp=1.0)
    # - ejemplo 2, hay dos parametros: def __init__(self, amp=1.0, samp_rate= 32000)
    # - si el bloque es vectorial hay que incluir la variable que marca el tamaño del vector
    # para reconocerla siempre usaremos Nvec
    # por ejemplo def __init__(self, amp=1.0, samp_rate= 32000, Nvec=128)
    # - a continuacion esta el caso de un solo parametro que hemos llamado escala
    def __init__(self, escala=0.5):
 
        # En la siguiente funcion debes recordar que usaras:
        # - sync: cuando tu bloque sea un bloque de tipo sincrono (por cada muestra entrante habra una saliente)
        # - decim: cuando es un bloque decimador (por cada muestra saliente hay un numero entero de muestras entrantes)
        # - interp: cuando es un bloque interpolador (por cada muestra entrante hay un numero entero de muestras salientes)
        # - basic: cuando no hay relacion entre el numero de muestras entrantes y las salientes
        # self: Es necesario para que la funcion adminita el uso de self en su cuerpo para declarar
        # variables que pueden ser usadas por otras funciones.
        # mas en: https://wiki.gnuradio.org/index.php/Guided_Tutorial_GNU_Radio_in_Python#3.3.1._Choosing_a_Block_Type
        gr.sync_block.__init__(
            self,
 
            # Lo siguiente es para definir el nombre que tendra nuestro bloque para los usuarios de GRC
            name='Plantilla_para_crear_bloques_cc', 
 
            # A continuacion se definen los tipos de senales de entrada y salida. Veamos algunos ejemplos:
            # - [np.complex64]: cuando se tiene una sola senal y es compleja
            # - [np.float32]: cuando se tiene una sola senal y es de tipo real y flotante
            # - [np.float32, np.complex64]: cuando hay dos senales: una de tipo real flotante y la otra es compleja
            # - otros casos: int8 o byte (entero de 8 bits, que en C++ se conoce como char)
            # - No hemos explorado mas casos, pero no es tan sencillo. Uno supondria que otros casos posibles son:
            # int16 (en C++ se conoce como short), int32, int64. Los dos primeros funcionan, pero int64 no.
            # - En el caso de un bloque vectorial aqui hay que indicarlo entre (). Veamos ejemplos:
            #   Ejemplo 1: el bloque tiene una entraga y unsa salida y ambas son reales y vectoriales
            #    y el tamano del vectorr es Nvec, entonces se declara asi:
            #   * in_sig=[(np.float32,Nvec)],
            #   * out_sig=[(np.float32,Nvec)]
            # En el siguiente ejemplo hay dos entradas complejas y una salida real. Todas tipo stream
            in_sig=[np.complex64,np.complex64], 
            out_sig=[np.complex64]
        )
 
        # las variables que entran como parametros del bloque deben ser declaradas nuevamente
        # usando self sobre todo si van a ser usadas dentro de otras funciones de la clase:
        self.escala=escala
 
        # abajo se puede escribir lo que se le antoje al programador, por ejemplo:
        # self.coef=1.0: define la variable global coef y le asigna el valor 1.0
        # self significa que es una variable global, que se puede invocar directamente desde otras funciones.
        # En todo caso, para las cosas que se definan aqui hay que tener en cuenta que:
        # -  esto es parte del constructor de la clase, por lo tanto, por cada bloque que se cree con esta clase
        #    estas cosas se invocaran solo una vez
        # -  Se supone que lo que se cree aqui es para ser usado, de manera que deberia ser usado en work()
        # A continuacion vamos a suponer que necesitamos usar constante  coef=1.0
        self.coef = 1.0
 
    # La funcion work() siempre debe estar presente en un bloque. Es alli donde estara la logica del bloque 
    # Es importante que tengas en cuenta lo siguiente:
    # - Para las senales tipo stream se tiene que:
    #    * input_items: es un arreglo de MxN. M es el numero de entradas, N el numero de muestras de la senal
    #    * in0=input_items[0]: es un vector de longitud N, por lo tanto trae N muestras de una senal
    #    * in1=input_items[1]: es un vector de longitud N, por lo tanto trae N muestras de una segunda senal
    #    * M esta definido por la cantidad de entradas que tiene el bloque, es decir, lo declarado arriba en in_sig
    #    * N va cambiando con cada nueva rafaga de muestras, de modo que es un valor desconocido
    #        se puede calcular como N=len(input_items[0])
    # - Si el bloque es de tipo vectorial, tenemos que el bloque input_items es un array MxLxNvec
    #    * M hace referencia a las senales de entrada (representa el fondo de un cubo)
    #    * L Al numero de paquetes recibidos (representa la altura del cubo)
    #    * Nvec al numero de muestras por vector (representa el ancho del cubo)
    #    * A cada entrada le corresponde una matriz LxNvec, por ejemplo para la entrada cero tenmos
    #    * in0=input_items[0] es una matriz LxNvec, es decir una señal que trae L vectores de Nvec muestras
    #    * Por tanto in0[0] es el primer vector de muestras de la senal, in0[1] el segundo, etc.
    # En el caso de output_items, aplica lo mismo dicho para input_items, pero con las senales
    # de salida y lo definido para out_sig
    # el "self" en la declaracion creo que es para que la funcion acepte el uso de self internamente
    
    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        out0 = output_items[0]
        out0[:]=(in0+in1)*self.escala/self.coef
        return len(out0)

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#OOO                     PALTILLA PARA UN FLUJOGRAM                         OOO
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# Libreria obligatoria
from gnuradio import gr
 
# Librerias particulares
from gnuradio import analog
from gnuradio import blocks
from gnuradio.filter import firdes

# Librerias para poder incluir graficas tipo QT
from gnuradio import qtgui
from PyQt4 import Qt # si no se acepta PyQt4 cambie PyQt4 por PyQt5
import sys, sip
 
# Ahora debes importar tu libreria. A continuacion suponemos que tu libreria ha sido
# guardada en un archivo llamado lib_comdig_code.py
# import lib_comdig_code as misbloques  
 
 
###########################################################
###           LA CLASE DEL FLUJOGRAMA                   ###
###########################################################
class flujograma(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)
 
        ################################################
        ###   EL FLUJOGRAMA                          ###
        ################################################
 
        # Las variables
        samp_rate = 1e6
        fftsize = 2048
 
        # Los bloques
        self.src = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, 0.1, 1, 0)
        self.nse = analog.noise_source_c(analog.GR_GAUSSIAN, 0.1)
        self.add = e_add_cc(0.5)
        self.thr = blocks.throttle(gr.sizeof_gr_complex, samp_rate, True)
        self.snk = qtgui.sink_c(
            fftsize, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
        )
 
        # Las conexiones
        self.connect(self.src, (self.add, 0))
        self.connect(self.nse, (self.add, 1))
        self.connect(self.add, self.thr, self.snk)
 
        # La configuracion para graficar
        self.pyobj = sip.wrapinstance(self.snk.pyqwidget(), Qt.QWidget)
        self.pyobj.show()
 
###########################################################
###                LA CLASE PRINCIPAL                   ###
###########################################################
def main():
    # Para que lo nuestro sea considerado una aplicación tipo QT GUI
    qapp = Qt.QApplication(sys.argv)
    simulador_de_la_envolvente_compleja = flujograma()
    simulador_de_la_envolvente_compleja.start()
    # Para arranque la parte grafica
    qapp.exec_()
 
# como el main lo hemos puesto como una funcion, ahora hay que llamarla
# podriamos escibir simplemete main(), pero es mas profesional asi:
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass