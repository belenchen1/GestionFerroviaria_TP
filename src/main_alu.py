import json
import networkx as nx
import matplotlib.pyplot as plt
import copy
import math

def setear_grafo(trenes):
   
   cabeceras = tuple(trenes['stations'])
   R = nx.DiGraph()
   services = set() # para que no hayan horarios repetidos -> unificamos la demanda de los repetidos en un mismo nodo
   edges = []
   
   for s in trenes['services'].values():
      
      # agrego nodos, en principio con demanda 0
      services.add((s['stops'][0]['time'], 0, s['stops'][0]['station']))
      services.add((s['stops'][1]['time'], 0, s['stops'][1]['station']))
      
      # aristas verdes
      w = math.ceil(s['demand'][0] / trenes['rs_info']['capacity'])
      edges.append((((s['stops'][0]['time'])), ((s['stops'][1]['time'])), {'lower_bound': w, 'upper_bound': trenes['rs_info']['max_rs'], 'weight': 0, 'color': 'green'}))
   
   services = list(services)
   services.sort(key=lambda x: x[0]) 

   # sumo/resto demandas de servicios que salen/entran en cierto horario
   for s in trenes['services'].values():
      w = math.ceil(s['demand'][0] / trenes['rs_info']['capacity'])
      for i in range(len(services)):
         if services[i][0] == s['stops'][0]['time']:
               services[i] = (s['stops'][0]['time'], services[i][1] + w, services[i][2])                  
         elif services[i][0] == s['stops'][1]['time']:
               services[i] = (s['stops'][1]['time'], services[i][1] - w, services[i][2])
   
   station1 = []
   station2 = []
   # lista para aristas entre misma estacion para aristas azules
   for i in range(len(services)):
      if services[i][2] == cabeceras[0]:     # s['stops'][0] <-> type D
         station1.append(services[i][0])
      else:
         station2.append(services[i][0])
   
   # convierto a diccionario los atributos
   for i in range(len(services)):
      w = services[i][1]
      services[i] = (services[i][0], {'demand': w, 'station': services[i][2]})
      
   print(services)
   print(f'cant servicios de tiempo distinto = cant de nodos = {len(services)}\n')
   
   R.add_nodes_from(services)
   R.add_edges_from(edges)
   
   BIG_NUMBER = 1e16
   
   # aristas rojas
   R.add_edge(station1[-1], station1[0], lower_bound=0, upper_bound=BIG_NUMBER, weight=1, color='red')
   R.add_edge(station2[-1], station2[0], lower_bound=0, upper_bound=BIG_NUMBER, weight=1, color='red')
   
   # aristas azules
   for i in range(1, len(station1)):
      R.add_edge(station1[i-1], station1[i], lower_bound=0, upper_bound=BIG_NUMBER, weight=0, color='blue')
      
   for i in range(1, len(station2)):
      R.add_edge(station2[i-1], station2[i], lower_bound=0, upper_bound=BIG_NUMBER, weight=0, color='blue')
      
   '''pos = nx.spring_layout(R)
   nx.draw(R, pos, with_labels=True, font_weight='bold')
   edge_labels = nx.get_edge_attributes(R, 'capacity')
   nx.draw_networkx_edge_labels(R, pos, edge_labels=edge_labels)
   plt.show()'''
   print(f"len(station1): {len(station1)}")
   print(f"len(station2): {len(station2)}")
   
   return R

def costo_min(G:nx.DiGraph):
   R = copy.deepcopy(G)

   # redefino aristas
   for e in R.edges():
      R[e[0]][e[1]]['upper_bound'] = R[e[0]][e[1]]['upper_bound'] - R[e[0]][e[1]]['lower_bound']
      R[e[0]][e[1]]['lower_bound'] = 0

   flowDict = nx.min_cost_flow(R, demand='demand', capacity='upper_bound', weight='weight')
   costo = nx.cost_of_flow(R, flowDict)
   print(f'\nflujo:\n{flowDict}')
   print(f'costo: {costo}')

def main():
   # filename = "instances/toy_instance.json"
   filename = "instances/retiro-tigre-semana.json"
   # filename = "instances/toy_tiempos_repetidos.json"

   with open(filename) as json_file:
      data = json.load(json_file)

   # test file reading
   R = setear_grafo(data)
   
   count_red = 0
   for e in R.edges():
      if R[e[0]][e[1]]['color'] == 'red':
         count_red += 1
   print(f"count_red: {count_red}")
   count_blue=0
   for e in R.edges():
      if R[e[0]][e[1]]['color'] == 'blue':
         count_blue += 1
   print(f"count_blue: {count_blue}")

   costo_min(R)
   
   '''
   for service in data["services"]:
      print(service, data["services"][service]["stops"])
   '''
if __name__ == "__main__":
   main()