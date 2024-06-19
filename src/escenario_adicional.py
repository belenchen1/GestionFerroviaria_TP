import networkx as nx
from math import *
import math

def setear_grafo_roto(trenes, u, rota:str):
   
   rota = rota.upper()
   cabeceras = (trenes['stations'][0].upper(), trenes['stations'][1].upper())
   
   R = nx.DiGraph()

   for s in trenes['services'].values():
      # agrego nodos, en principio con demanda 0
      for i in range(2): # 0 <-> type D (departure)  ^  1 <-> type A (arrival)
         nodo_id = (s['stops'][i]['time'], s['stops'][i]['station'].upper())
         if nodo_id not in R.nodes():
            R.add_node(nodo_id, demand=0)            
      # aristas verdes -> de tren
      l = math.ceil(s['demand'][0] / trenes['rs_info']['capacity'])
      src = (s['stops'][0]['time'], s['stops'][0]['station'].upper())
      dst = (s['stops'][1]['time'], s['stops'][1]['station'].upper())
      R.add_edge(src, dst, lower_bound=l, upper_bound=trenes['rs_info']['max_rs'], weight=0, color='green')
   
   # ajusto demandas {sumo/resto demandas de servicios que salen/entran en cierto horario}
   for s in trenes['services'].values():
      d = math.ceil(s['demand'][0] / trenes['rs_info']['capacity'])
      id_dep = (s['stops'][0]['time'], s['stops'][0]['station'].upper())
      id_arr = (s['stops'][1]['time'], s['stops'][1]['station'].upper())
      for n in R.nodes(data="True"):
         if n[0] == id_dep:
            R.nodes[n[0]]['demand'] += d
         if n[0] == id_arr:
            R.nodes[n[0]]['demand'] -= d

   # lista para aristas entre misma estacion; aristas azules y rojas. sé que están en orden creciente segun tiempo porque las creo a partir de services y services está ordenada
   services = list(R.nodes(data=True))
   services.sort(key=lambda service: (service[0][0]))
   station1 = []
   station2 = []
   for nodo in services:
      if nodo[0][1] == cabeceras[0]:
         station1.append(nodo)
      else:
         station2.append(nodo)

   BIG_NUMBER = float(inf)
   
   # aristas rojas -> trasnoche
   if rota==cabeceras[0]:
      R.add_edge(station1[-1][0], station1[0][0], lower_bound=0, upper_bound=u, weight=1, color='red')
      R.add_edge(station2[-1][0], station2[0][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=1, color='red')
      d = R.nodes[station1[0][0]]['demand']
   elif rota==cabeceras[1]:
      R.add_edge(station1[-1][0], station1[0][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=1, color='red')
      R.add_edge(station2[-1][0], station2[0][0], lower_bound=0, upper_bound=u, weight=1, color='red')
      d = R.nodes[station2[0][0]]['demand']
   else:
      raise Exception(f'Station not found. Must be {cabeceras[0]} or {cabeceras[1]}')
   
   # aristas azules -> traspaso
   for i in range(1, len(station1)):
      R.add_edge(station1[i-1][0], station1[i][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=0, color='blue')
   for i in range(1, len(station2)):
      R.add_edge(station2[i-1][0], station2[i][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=0, color='blue')
   
   # agregamos el nodo z para que almacene las unidades adicionales de la cabecera rota
   R.add_node('z')

   if rota==cabeceras[0]:
      R.add_edge( station1[-1][0],'z', lower_bound=0, upper_bound=BIG_NUMBER, weight=2, color='blue')
      R.add_edge('z',station1[0][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=2, color='blue')
   else:
      R.add_edge( station2[-1][0],'z', lower_bound=0, upper_bound=BIG_NUMBER, weight=2, color='blue')
      R.add_edge('z',station2[0][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=2, color='blue')
   return R





