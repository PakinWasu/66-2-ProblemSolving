import tkinter as tk
import DBfunction as db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.image as mpimg
from collections import Counter
selected_items = []  # Initialize a variable to store selected items
selected_nodes = []
g = nx.Graph()
g.add_nodes_from(db.get_node())
g.add_weighted_edges_from(db.get_distanc())
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



        
def find_path(slcnode):    
    path = []
    keep_u = []
    # print(slcnode)
    for i in range(len(slcnode)-1):
        lestes = 9999999
        for k in slcnode :
            if k not in keep_u or k not in path:
                sort_i = sort_nodes_by_distance(g,slcnode[i])
                if sort_i.index(k) <= lestes and sort_i.index(k) != 0 :
                    lestes = sort_i.index(k)
                    
        keep_u.append(slcnode[i])
        path.append(sort_i[lestes]) 
        # (print(keep_u))
        # print(path)
    # print(sort_nodes_by_distance(g,"FV01"))
    path.insert(0,'SV01')
    path = list(Counter(path).keys())
    path.insert(len(path),'SV02')

    # print(path)
    # path=['FV02', 'FV02','FV01', 'SV02']    
    short_path = []
    for shot in range(len(path)-1):
        closest_path = nx.shortest_path(g, path[shot], path[shot+1], weight='weight')
        short_path.append(closest_path)

    # print(short_path)
    
    short_path_use = []
    for sublist in short_path:
        for asd in sublist:
            short_path_use.append(asd)    
    short_path_use = list(Counter(short_path_use).keys())
    return short_path_use

def find_path_edge(path):
    src_dest = []
    for sd_edge in range(len(path)-1):
        closest_path = nx.shortest_path(g, path[sd_edge], path[sd_edge+1], weight='weight')
        src_dest.append(closest_path)
    
    srcdest_edge = []
    for sub in src_dest :
        for res in sub:
            srcdest_edge.append(res)
    print(srcdest_edge)
    edge = [srcdest_edge[0]]
    for i in range(1, len(srcdest_edge)):
        if srcdest_edge[i] != srcdest_edge[i - 1]:  # ถ้าข้อมูลไม่เท่ากับข้อมูลก่อนหน้า (ไม่ซ้ำ)
            edge.append(srcdest_edge[i])  # เพิ่มข้อมูลเข้าไปใน new_list        
    return edge
        
print(find_path(selected_nodes))

print(find_path_edge(find_path(selected_nodes)))
    