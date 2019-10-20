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
from gnuradio import audio
 
# Librerias para poder incluir graficas tipo QT
from gnuradio import qtgui
from PyQt4 import Qt # si no se acepta PyQt4 cambie PyQt4 por PyQt5
import sys, sip
 
# Ahora debes importar tu libreria. A continuacion suponemos que tu libreria ha sido
# guardada en un archivo llamado lib_comdig_code.py
import lib_comdig_code as misbloques  
#import matplotlib.pyplot as plt
 
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
        samp_rate = 11025
        Sps=16
        N= Sps*256
        ntaps=6*6        
        beta=0
        # respuesta al impulso
        #h=misbloques.rect(Sps) # forma rectangular
        #h=misbloques.nyq(Sps,ntaps) # forma sinc
        #h=misbloques.rcos(Sps,ntaps,beta) # forma coseno alzado
        #h=misbloques.rrcos(Sps,ntaps,beta) # forma raiz coseno alzado
        #h=misbloques.B_NRZ_L(Sps) # forma NRZ_L
        #h=misbloques.RZ(Sps) # forma RZ
        h=misbloques.saw(Sps) # forma saw
        
        # Los bloques
        p_fuente=misbloques.e_generador_fun_f(Sps,h)
        p_pantalla_t = qtgui.time_sink_f(
            512, # numero de muestras en la ventana del osciloscopio
            samp_rate,
            "senal promediada", # nombre que aparece en la grafica
            1 # Nuemero de entradas del osciloscopio
        )
        
        p_chorro_a_vector=blocks.stream_to_vector(gr.sizeof_float*1, N)
        p_nse = analog.noise_source_f(analog.GR_GAUSSIAN, 0.1)
        p_add = misbloques.e_add_ff(1.0)
        p_psd=misbloques.e_vector_psd_ff(N,2000000)
        p_ojo=misbloques.vec_diagrama_ojo_f(Sps,N)
        p_pantalla_vectorial = qtgui.vector_sink_f(
            N,
            -samp_rate/2.,
            samp_rate/N,
            "frecuencia",
            "Magnitud",
            "PSD",
            1 # Number of inputs
        )
        p_pantalla_vectorial.enable_autoscale(True)
        # LAS CONEXIONES
        self.connect(p_fuente, (p_add, 0))
        self.connect(p_nse, (p_add, 1))

        self.connect(p_add, p_pantalla_t)
        #self.connect(p_fuente, p_chorro_a_vector, p_psd, p_pantalla_vectorial)
        self.connect(p_add, p_chorro_a_vector)
        self.connect(p_chorro_a_vector, p_psd, p_pantalla_vectorial)
        self.connect(p_chorro_a_vector, p_ojo)
 
        # La configuracion para graficar
        pyobj = sip.wrapinstance(p_pantalla_vectorial.pyqwidget(), Qt.QWidget)
        pyobj1 = sip.wrapinstance(p_pantalla_t.pyqwidget(), Qt.QWidget)
        pyobj.show()
        pyobj1.show()
         
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