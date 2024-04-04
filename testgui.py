import tkinter as tk
import DBfunction as db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.image as mpimg
from collections import Counter
selected_items = []  # Initialize a variable to store selected items
selected_nodes = []
def sort_nodes_by_distance(graph, source_node):
    distances = {}  # สร้างพจนานุกรมเพื่อเก็บระยะทางจากโนดที่กำหนดไปยังโนดทุกๆ โนด
    for node in graph.nodes():
        if node == source_node:  # กำหนดระยะทางจากโนดตั้งต้นไปยังตัวเองเป็น 0
            distances[node] = 0
        else:
            try:
                distance = nx.shortest_path_length(graph, source_node, node, weight='weight')  # ใช้น้ำหนักของเส้นเชื่อมเป็นตัวเปรียบเทียบ
                distances[node] = distance
            except nx.NetworkXNoPath:  # หากไม่มีเส้นทางจากโนดตั้งต้นไปยังโนดนี้
                distances[node] = float('inf')  # กำหนดระยะทางเป็น infinity
    sorted_nodes = sorted(distances, key=distances.get)  # เรียงโนดตามระยะทางจากน้อยไปมาก
    return sorted_nodes


selected_nodes = ['SV01', 'FV08', 'FV12', 'NF10','FV11', 'SV02']
def find_path(slcnode):    
    g = nx.Graph()
    g.add_nodes_from(db.get_node())
    g.add_weighted_edges_from(db.get_distanc())
    path = []
    
    
    for i in range(len(slcnode)):
        lestes = 9999999
        for k in slcnode :
            sort_i = sort_nodes_by_distance(g,slcnode[i])
            if sort_i.index(k) <= lestes and sort_i.index(k) != 0 :
                lestes = sort_i.index(k)
        
        
        path.append(sort_i[lestes]) 
        print(lestes)

 
 
        
    print(slcnode)
    print(path)
    
find_path(selected_nodes)
    
