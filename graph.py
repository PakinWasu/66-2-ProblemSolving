import tkinter as tk
import DBfunction as db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.image as mpimg
from collections import Counter
selected_items = []  
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

def find_path(slcnode):    
    g = nx.Graph()
    g.add_nodes_from(db.get_node())
    g.add_weighted_edges_from(db.get_distanc())
    path = []
    keep_u = []

    for i in range(len(slcnode)-1):
        lestes = 9999999
        for k in slcnode :
            if k not in keep_u:
                sort_i = sort_nodes_by_distance(g,slcnode[i])
                if sort_i.index(k) <= lestes and sort_i.index(k) != 0 :
                    lestes = sort_i.index(k)
        keep_u.append(slcnode[i])
        path.append(sort_i[lestes]) 

    path.insert(0,'SV01')
    short_path = []
    for shot in range(len(path)-1):
        closest_path = nx.shortest_path(g, path[shot], path[shot+1], weight='weight')
        short_path.append(closest_path)
   
    short_path_use = []
    for sublist in short_path:
        for asd in sublist:
            short_path_use.append(asd)    
    return short_path_use

def on_select(event=None):
    global selected_items
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(idx) for idx in selected_indices]
    label.config(text="You selected: " + ", ".join(selected_items))
    draw_graph()  # Redraw the graph when selection changes

def draw_graph():
    global selected_nodes
    network = nx.Graph()
    selected_nodes.append('SV01')
    selected_nodes.append('SV02') 
    if selected_items != []:
        selected_nodes.clear()
        selected_nodes.append('SV01')
        for i in db.get_idshelf_by_productname(selected_items):
            selected_nodes.append (i)  # Convert selected items to a set for faster lookup
        selected_nodes.append('SV02')    
    selected_nodes = list(Counter(selected_nodes).keys())

    print('โนดที่เลือก',selected_nodes)
    path = find_path(selected_nodes)   
    path = list(Counter(path).keys())
    # selected_nodes = path
    print(selected_nodes)
    selected_edges = []  # Initialize a list to store selected edges
    
    for edge in db.get_distanc():
        if (edge[0] in selected_nodes and edge[1] in selected_nodes) or (edge[1] in selected_nodes and edge[0] in selected_nodes):
            selected_edges.append(edge)

    network.add_nodes_from(selected_edges)
    network.add_weighted_edges_from(selected_edges)

    pos = db.get_pos_node()

    fig, ax = plt.subplots(figsize=(16, 7.14))  # Set the size of the graph
    img = mpimg.imread("BG.png")  # Load the background image
    ax.imshow(img, aspect='auto')  # Set the background image of the graph

    nx.draw(network, pos, ax=ax, with_labels=True, node_size=250, node_color='black', font_size=6, edge_color='blue', font_color='white')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=0, y=0)  # Show the matplotlib canvas at position (0, 0)

g = nx.Graph()
g.add_nodes_from(db.get_node())
g.add_weighted_edges_from(db.get_distanc())

root = tk.Tk()
root.title('makro')

# Create a Canvas for the background image
canvas = tk.Canvas(root, width=1600, height=900, relief='flat')
canvas.pack()

# Create the graph
draw_graph()

# Create the Listbox
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
listbox.place(x=800, y=720)

# Add items to the Listbox
items = db.get_productname()
for item in items:
    listbox.insert(tk.END, item)

# Bind the selection event to the Listbox
listbox.bind("<<ListboxSelect>>", on_select)

# Create the Label to display selected items
label = tk.Label(root, text="")
label.place(x=950, y=830)

root.mainloop()
