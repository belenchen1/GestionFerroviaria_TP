import csv
import json
import os
import random


filename = './instances/csv/moreno-once.csv'
# filename = './instances/csv/moreno-mercedes.csv'
# filename = './instances/csv/maipu-delta.csv'

with open(filename, mode='r', newline='') as archivo_entrada:
   lector_csv = csv.reader(archivo_entrada)
   filas = list(lector_csv)

json_data = {
   "services": {},
   "stations": [
      filas[1][0],
      filas[1][1]
   ],
   "cost_per_unit": {
      filas[1][0]: 1.0,
      filas[1][1]: 1.0
   },
   "rs_info": {
      "capacity": 100,
      "max_rs": 25
   }
}


for i in range(1, len(filas)):  # Saltar el encabezado
   tercera_columna = filas[i][2]
   lista_horarios = tercera_columna.split()
   service_id = i
   if lista_horarios[1] != "----" and lista_horarios[-1] != "----":
      stops = [
         {
            "time": lista_horarios[1].replace(":", ""),
            "station": filas[i][0],
            "type": 'D'
         },
         {
            "time": lista_horarios[-1].replace(":", ""),
            "station": filas[i][1],
            "type": 'A'
         }
      ]
      json_data["services"][service_id] = {
         "stops": stops,
         "demand": [random.randint(1, 2400)]
      }


base = os.path.basename(filename)
res = os.path.splitext(base)[0] + '.json'
output_path = "./instances/" + res
with open(output_path, 'w') as archivo_salida:
   json.dump(json_data, archivo_salida, indent=3)

