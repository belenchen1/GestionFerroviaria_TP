import json
import networkx as nx
import matplotlib.pyplot as plt
import copy

def setear_grafo(trenes, cabecera):
   R = nx.DiGraph()
   services = []
   edges = []
   station1 = []
   station2 = []
   for s in trenes['services'].values():
      # agrego nodos (nombre = (hora, imbalance))

      services.append((s['stops'][0]['time'], {'demand':-s['demand'][0]}))
      services.append(((s['stops'][1]['time']),{'demand':s['demand'][0]}))
      
      # aristas verdes
      w = (s['demand'][0]) / (trenes['rs_info']['capacity'])
      edges.append((((s['stops'][0]['time'])), ((s['stops'][1]['time'])), {'lower_bound': w, 'upper_bound': trenes['rs_info']['max_rs'], 'weight': 0,'color': 'green'}))
      
      # lista para aristas entre misma estacion
      if s['stops'][0]['station'] == cabecera[0]:
         station1.append(((s['stops'][0]['time'])))
      else:
         station2.append(((s['stops'][0]['time'])))
      if s['stops'][1]['station'] == cabecera[0]:
         station1.append(((s['stops'][1]['time'])))
      else:
         station2.append(((s['stops'][1]['time'])))
   
   R.add_nodes_from(services)
   R.add_edges_from(edges)
   
   station1.sort()
   station2.sort()
   
   BIG_NUMBER = 1e16
   # BIG_NUMBER = 25
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
   
   return R

def costo_min(G:nx.DiGraph):
   R = copy.deepcopy(G)
   # imbalance
   # for i in R.nodes():
   #       entrada = 0
   #       salida = 0
   #       for elem in R.in_edges(i):
   #          entrada += R[elem[0]][elem[1]]['lower_bound'] 
   #       for elem in R.out_edges(i):
   #          salida += R[elem[0]][elem[1]]['lower_bound']
   #       i = (i[0], salida - entrada)


   # redefino aristas
   for e in R.edges():
      R[e[0]][e[1]]['upper_bound'] = R[e[0]][e[1]]['upper_bound'] - R[e[0]][e[1]]['lower_bound']
      R[e[0]][e[1]]['lower_bound'] = 0
   
   # flowDict = nx.max_flow_min_cost(R, s, t, capacity='upper_bound', weight='weight')
   flowDict = nx.min_cost_flow(R, demand='demand', capacity='upper_bound', weight='weight')
   print(flowDict)

def main():
   filename = "instances/toy_instance.json"
   # filename = "instances/retiro-tigre-semana.json"

   with open(filename) as json_file:
      data = json.load(json_file)

   # test file reading
   R = setear_grafo(data, ("Retiro", "Tigre"))
   costo_min(R)
   for service in data["services"]:
      print(service, data["services"][service]["stops"])

if __name__ == "__main__":
   main()