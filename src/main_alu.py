import json
from funciones import *
from escenario_adicional import *
   
def main():
   ''' '''
   filename = "instances/toy_instance.json"
   # filename = "instances/retiro-tigre-semana.json"
   ''' '''
   # filename = "instances/toy_repetidos.json"
   # filename = "instances/moreno-once.json"
   # filename = 'instances/moreno-mercedes.json'
   # filename = 'instances/maipu-delta.json'
   ''' '''
   # filename = "instances/i-chica_d-chica.json" 
   # filename = "instances/i-chica_d-grande.json" # lim 2300
   # filename = "instances/i-grande_d-chica.json" 
   # filename = "instances/i-grande_d-grande.json" # lim 2300
   # filename = "instances/i-media_d-chica.json"
   # filename = "instances/i-media_d-grande.json" # lim 2400
   # filename = "instances/i-chica2_d-chica.json"
   # filename = "instances/i-chica2_d-grande.json" # lim 1200
   # filename = "instances/i-chica_d-random.json" 

   with open(filename) as json_file:
      data = json.load(json_file)

   R = setear_grafo(data)
   # R = setear_grafo_roto(data, 3, 'mercedes')
   
   # costo_minimo = costo_min(R)
   # print(f'costo_minimo: {costo_minimo}')
   costo_maximo = costo_max(data)
   print(f'costo_maximo: {costo_maximo}')
   
   # ahorro = plata_ahorrada(costo_minimo,costo_maximo, cost_vagon=1500000)
   # print(f'plata_ahorrada: {ahorro}')
   
   costo_minimo = costo_min(R)
   print(f'costo_minimo: {costo_minimo}')
   
if __name__ == "__main__":
   main()