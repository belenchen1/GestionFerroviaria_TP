import json
import networkx as nx
import matplotlib.pyplot as plt

def setear_grafo(trenes, cabecera):
   R = nx.DiGraph()
   services = []
   edges = []
   station1 = []
   station2 = []
   for s in trenes['services'].values():
      # agrego nodos
      services.append(s['stops'][0]['time'])
      services.append(s['stops'][1]['time'])
      # aristas verdes
      w = (s['demand'][0]) / (trenes['rs_info']['capacity'])
      edges.append((s['stops'][0]['time'], s['stops'][1]['time'], {"capacity": w}))
      
      # lista para aristas entre misma estacion
      if s['stops'][0]['station'] == cabecera[0]:
         station1.append(s['stops'][0]['time'])
      else:
         station2.append(s['stops'][0]['time'])
      if s['stops'][1]['station'] == cabecera[0]:
         station1.append(s['stops'][1]['time'])
      else:
         station2.append(s['stops'][1]['time'])
   
   R.add_nodes_from(services)
   R.add_edges_from(edges)
   
   station1.sort()
   station2.sort()
   # aristas rojas
   print(station1)
   R.add_edge(station1[-1], station1[0], capacity=0)
   R.add_edge(station2[-1], station2[0], capacity=0)
   # aristas azules
   for i in range(1, len(station1)):
      if i == 1:
         w = 0
      else:
         entrada = 0
         salida = 0
         for elem in R.in_edges(station1[i]):
            entrada += R[elem[0]][elem[1]]['capacity']
         for elem in R.out_edges(station1[i]):
            salida += R[elem[0]][elem[1]]['capacity']
         w = entrada - salida
      R.add_edge(station1[i-1], station1[i], capacity=w)
   # for i in range(1, len(station2)):
   #    if i == 1:
   #       w = 0
   #    else:
   #       entrada = 0
   #       salida = 0
   #       for elem in R.in_edges(station2[i]):
   #          entrada += R[elem[0]][elem[1]]['capacity']
   #       for elem in R.out_edges(station2[i]):
   #          salida += R[elem[0]][elem[1]]['capacity']
   #       w = entrada - salida
   #    R.add_edge(station2[i-1], station2[i], capacity=w)
   
   # pos = nx.spring_layout(R)
   # nx.draw(R, pos, with_labels=True, font_weight='bold')
   # edge_labels = nx.get_edge_attributes(R, 'capacity')
   # nx.draw_networkx_edge_labels(R, pos, edge_labels=edge_labels)
   nx.draw(R, with_labels=True, font_weight='bold')
   plt.show()

def main():
	filename = "instances/toy_instance.json"
	# filename = "instances/retiro-tigre-semana.json"

	with open(filename) as json_file:
		data = json.load(json_file)

	# test file reading
	setear_grafo(data, ("Retiro", "Tigre"))

	for service in data["services"]:
		print(service, data["services"][service]["stops"])

if __name__ == "__main__":
	main()