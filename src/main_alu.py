import json
import networkx as nx
import matplotlib.pyplot as plt
import copy
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
               
      # aristas verdes
      w = math.ceil(s['demand'][0] / trenes['rs_info']['capacity'])
      src = (s['stops'][0]['time'], s['stops'][0]['station'])
      dst = (s['stops'][1]['time'], s['stops'][1]['station'])
      R.add_edge(src, dst, lower_bound=w, upper_bound=trenes['rs_info']['max_rs'], weight=0, color='green')

   # ajusto demandas {sumo/resto demandas de servicios que salen/entran en cierto horario}
   for s in trenes['services'].values():
      w = math.ceil(s['demand'][0] / trenes['rs_info']['capacity'])
      id_dep = (s['stops'][0]['time'], s['stops'][0]['station'])
      id_arr = (s['stops'][1]['time'], s['stops'][1]['station'])
      for n in R.nodes(data="True"):
         if n[0] == id_dep:
            R.nodes[n[0]]['demand'] += w
         if n[0] == id_arr:
            R.nodes[n[0]]['demand'] -= w

   # lista para aristas entre misma estacion; aristas azules y rojas. sé que están en orden creciente segun tiempo porque las creo a partir de services y services está ordenada
   services = list(R.nodes(data=True))
   services.sort(key=lambda x: (x[0][0]))
   station1 = []
   station2 = []
   for nodo in services:
      if nodo[0][1] == cabeceras[0]:
         station1.append(nodo)
      else:
         station2.append(nodo)

   BIG_NUMBER = 1e16
   
   # aristas rojas
   R.add_edge(station1[-1][0], station1[0][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=1, color='red')
   R.add_edge(station2[-1][0], station2[0][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=1, color='red')
   
   # aristas azules
   for i in range(1, len(station1)):
      R.add_edge(station1[i-1][0], station1[i][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=0, color='blue')
   for i in range(1, len(station2)):
      R.add_edge(station2[i-1][0], station2[i][0], lower_bound=0, upper_bound=BIG_NUMBER, weight=0, color='blue')
   
   return R

def costo_min(G:nx.DiGraph):
   R = copy.deepcopy(G)
   
   # redefino aristas
   for e in R.edges():
      R[e[0]][e[1]]['upper_bound'] = R[e[0]][e[1]]['upper_bound'] - R[e[0]][e[1]]['lower_bound']
      R[e[0]][e[1]]['lower_bound'] = 0

   # nodos ficticios de comienzo y fin
   R.add_node('s')
   R.add_node('t')
   # s -> nodo con demanda negativa (generó nuevos trenes)
   # t -> nodo con demanda positiva (manda trenes que recibió)
   for n, d in R.nodes(data=True):
      if 'demand' in d:
         u = abs(d['demand'])
         if d['demand'] < 0:
            R.add_edge('s', n, upper_bound=u, weight=0)
         elif d['demand'] > 0:
            R.add_edge(n, 't', upper_bound=u, weight=0)

   flowDict = nx.min_cost_flow(R, demand='demand', capacity='upper_bound', weight='weight')
   costo = nx.cost_of_flow(R, flowDict, weight='weight')
   return costo
   
def main():
   # filename = "instances/toy_instance.json"
   filename = "instances/retiro-tigre-semana.json"
   # filename = "instances/toy_repetidos.json

   with open(filename) as json_file:
      data = json.load(json_file)

   # test file reading
   R = setear_grafo(data)
   costo = costo_min(R)
   print(f'costo: {costo}')
   
if __name__ == "__main__":
   main()