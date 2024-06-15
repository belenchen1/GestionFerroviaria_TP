import json
from funciones import *
   
def main():
   # filename = "instances/toy_instance.json"
   # filename = "instances/retiro-tigre-semana.json"
   # filename = "instances/toy_repetidos.json"
   filename = "instances/moreno-once.json"
   # filename = 'instances/moreno-mercedes.json'
   # filename = 'instances/maipu-delta.json'
   
   with open(filename) as json_file:
      data = json.load(json_file)

   # test file reading
   R = setear_grafo(data)
   costo = costo_min(R)
   print(f'costo: {costo}')
   
if __name__ == "__main__":
   main()