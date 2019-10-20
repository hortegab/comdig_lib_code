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
        N= 1024
        # Los bloques
        #p_fuente=blocks.wavfile_source('/home/uis-e3t/MisGits/backup_pruebas_gnuradio/programacionconcodigo/lab4/bush-clinton_debate_waffle.wav', True)
        p_fuente = audio.source(samp_rate, '', True)
        p_pantalla_t = qtgui.time_sink_f(
            512, # numero de muestras en la ventana del osciloscopio
            samp_rate,
            "senal promediada", # nombre que aparece en la grafica
            1 # Nuemero de entradas del osciloscopio
        )
        p_chorro_a_vector=blocks.stream_to_vector(gr.sizeof_float*1, N)
        p_psd=misbloques.e_vector_psd_ff(N,2000000)
        p_pantalla_vectorial = qtgui.vector_sink_f(
            N,
            -samp_rate/2.,
            samp_rate/N,
            "frecuencia",
            "Magnitud",
            "FT en Magnitud",
            1 # Number of inputs
        )
        # p_pantalla_vectorial.enable_autoscale(True)
        self.connect(p_fuente, p_pantalla_t)
        self.connect(p_fuente, p_chorro_a_vector, p_psd, p_pantalla_vectorial)
 
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