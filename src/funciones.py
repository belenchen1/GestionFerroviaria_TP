import networkx as nx
import matplotlib.pyplot as plt
import copy
from math import *
import math

def setear_grafo(trenes):
   
   cabeceras = tuple(trenes['stations'])
   R = nx.DiGraph()

   for s in trenes['services'].values():
      # agrego nodos, en principio con demanda 0
      for i in range(2): # 0 <-> type D (departure)  ^  1 <-> type A (arrival)
         nodo_id = (s['stops'][i]['time'], s['stops'][i]['station'])
         if nodo_id not in R.nodes():
            R.add_node(nodo_id, demand=0)
               
      # aristas verdes -> de tren
      l = math.ceil(s['demand'][0] / trenes['rs_info']['capacity'])
      src = (s['stops'][0]['time'], s['stops'][0]['station'])
      dst = (s['stops'][1]['time'], s['stops'][1]['station'])
      R.add_edge(src, dst, lower_bound=l, upper_bound=trenes['rs_info']['max_rs'], weight=0, color='green')

   # ajusto demandas {sumo/resto demandas de servicios que salen/entran en cierto horario}
   for s in trenes['services'].values():
      d = math.ceil(s['demand'][0] / trenes['rs_info']['capacity'])
      id_dep = (s['stops'][0]['time'], s['stops'][0]['station'])
      id_arr = (s['stops'][1]['time'], s['stops'][1]['station'])
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
   R.add_edge(station1[-1][0], station1[0][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=1, color='red')
   R.add_edge(station2[-1][0], station2[0][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=1, color='red')
   
   # aristas azules -> traspaso
   for i in range(1, len(station1)):
      R.add_edge(station1[i-1][0], station1[i][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=0, color='blue')
   for i in range(1, len(station2)):
      R.add_edge(station2[i-1][0], station2[i][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=0, color='blue')
   
   return R

def costo_min(G:nx.DiGraph):
   R = copy.deepcopy(G)
   
   # redefino aristas
   for e in R.edges(data=True):
      if e[2]['color'] == 'green':
         R[e[0]][e[1]]['upper_bound'] = R[e[0]][e[1]]['upper_bound'] - R[e[0]][e[1]]['lower_bound']
         R[e[0]][e[1]]['lower_bound'] = 0

   flowDict = nx.min_cost_flow(R, demand='demand', capacity='upper_bound', weight='weight')
   
   # calculo costo minimo sumando el flujo de las aristas de trasnoche (rojas)
      # que es equivalente a hacer (flujo * peso) para cada arista, porque las demas aristas tienen peso 0
   costo=0
   for e in R.edges():
      if e[0] == 'z'or e[1] == 'z':
         print(f'flujo arista de {e[0]} a {e[1]}: {flowDict[e[0]][e[1]]}')
         if e[0] == 'z':
            costo += flowDict[e[0]][e[1]]
      if R[e[0]][e[1]]['color'] == 'red':
         print(f'flujo arista de {e[0]} a {e[1]}: {flowDict[e[0]][e[1]]}')
         costo += flowDict[e[0]][e[1]]
   return costo


def costo_max(trenes):
   #sería el costo sin reciclar servicios
   d=0
   for s in trenes['services'].values():
      d+=math.ceil(s['demand'][0] / trenes['rs_info']['capacity'])
   return d

def plata_ahorrada(costo_min,costo_max, cost_vagon):
   return(costo_max-costo_min) * cost_vagon
   


