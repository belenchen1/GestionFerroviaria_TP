import json
from funciones import *
from ejercicio_5 import *
   
def main():
   filename = "instances/toy_instance.json"
   #filename = "instances/retiro-tigre-semana.json"
   # filename = "instances/toy_repetidos.json"
   # filename = "instances/moreno-once.json"
   # filename = 'instances/moreno-mercedes.json'
   # filename = 'instances/maipu-delta.json'
   
   with open(filename) as json_file:
      data = json.load(json_file)

   # test file reading
   # R = setear_grafo(data)
   # costo_minimo = costo_min(R)
   # print(f'costo_minimo: {costo_minimo}')
   costo_maximo = costo_max(data)
   print(f'costo_maximo: {costo_maximo}')
   # #Tomamos data de un artículo de infobae 2018 donde se decía que cada vagón para el Roca costaban 1.580.000 dólares
   # ahorro= plata_ahorrada(costo_minimo,costo_maximo, cost_vagon=1500000)
   # print(f'plata_ahorrada: {ahorro}')
   R = setear_grafo(data)
   costo_minimo = costo_min(R)
   print(f'costo_minimo: {costo_minimo}')
   

if __name__ == "__main__":
   main()