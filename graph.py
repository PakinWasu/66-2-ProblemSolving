import networkx as nx
import matplotlib.pyplot as plt
import DBfunction as db
network = nx.Graph()

network.add_nodes_from(db.get_node())
print(f"This network has now {network.number_of_nodes()} nodes.")
plt.figure(figsize=(8,6))
plt.title('Example of Graph Representation', size=10)



for edge in db.get_distanc():
    network.add_edge(edge[0],edge[1], weight = edge[2])

source = input("Enter in your current location information: ")
target = input("Enter the destination information where you want to go: ")


shortest_path = nx.shortest_path(network, source, target, weight='weight')

total_weight_decimal_shortest_path = sum(network[shortest_path[i]][shortest_path[i+1]]['weight'] 
                                         for i in range(len(shortest_path)-1) 
                                            if isinstance(network[shortest_path[i]][shortest_path[i+1]]['weight'], float))

format_total_weight = f"{total_weight_decimal_shortest_path:.1f}"

print("Shortest Path:", shortest_path)
print(f"Total Weight (Decimal) in Shortest Path: {format_total_weight} m.")


nx.draw_networkx(network, with_labels=True)

# plt.show()