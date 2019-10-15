import numpy as np

# Deinifimos N=8 muestras de dos senales entrantes
# sabemos que si esto funcional para senales reales tambien funcionara para
#  complejas. Por lo tanto trabajaremos solo para el caso de senales reales
senal0=np.array([1.,2.,3.,4.,5.,6.,7.,8.])
senal1=np.array([2.,2.,2.,2.,2.,2.,2.,2.])

# Las senales entrantes realmente llegan en forma matricial
in_sig= np.array([senal0,senal1])

# la senal saliente tambien es matricial, aun cuando sea una matriz de una sola fila
out_sig=np.array([[0.,0.,0.,0.,0.,0.,0.,0.]])

# Escribimos el codigo a probar, sin usar "self" porque esto no es una clase
escala=0.5
def work(input_items, output_items):
    in0 = input_items[0]
    in1 = input_items[1]
    out0 = output_items[0]
    out0[:]=(in0+in1)*escala
    return len(out0)

# Por fin comprobamos la función
d=work(in_sig,out_sig)
print "senal en la entrada 1: ", in_sig[0]
print "senal en la entrada 2: ", in_sig[1]
print "senal  en  la  salida: ", out_sig[0]