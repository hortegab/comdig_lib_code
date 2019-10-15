#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Lo de arriba es para que los IDE conozcan en que esta escrito este codigo 
###########################################################
# Puedes encontrar este codigo como objeto_ej4.py en:    ##
# https://sites.google.com/saber.uis.edu.co/comdig/sw    ##
###########################################################
###           IMPORTACION DE LIBRERIAS                  ###
###########################################################
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
import lib_comdig_code as misbloques  
 
 
###########################################################
###           LA CLASE DEL FLUJOGRAMA                   ###
###########################################################
class flujograma(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)
 
        ################################################
        ###   EL FLUJOGRAMA                          ###
        ################################################
 
        # Las variables usadas en el flujograma
        samp_rate = 32000
        f=1000
        N= 128
        # Los bloques
        src = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, f, 1, 0)
        nse = analog.noise_source_f(analog.GR_GAUSSIAN, 0.1)
        add = misbloques.e_add_ff(1.0)
        snk = qtgui.time_sink_f(
            512, # numero de muestras en la ventana del osciloscopio
            samp_rate,
            "senal promediada", # nombre que aparece en la grafica
            1 # Nuemero de entradas del osciloscopio
        )
       

        str2vec=blocks.stream_to_vector(gr.sizeof_float*1, N)
        e_fft=misbloques.e_vector_fft_ff(N)
        vsnk = qtgui.vector_sink_f(
            N,
            -samp_rate/2.,
            samp_rate/N,
            "frecuencia",
            "Magnitud",
            "FT en Magnitud",
            1 # Number of inputs
        )
        vsnk.enable_autoscale(True)
        # Las conexiones
        self.connect(src, (add, 0))
        self.connect(nse, (add, 1))
        self.connect(add, snk)
        self.connect(add, str2vec, e_fft, vsnk)
 
        # La configuracion para graficar
        pyobj = sip.wrapinstance(vsnk.pyqwidget(), Qt.QWidget)
        pyobj.show()
 
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