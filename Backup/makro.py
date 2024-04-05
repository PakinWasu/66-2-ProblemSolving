import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext  # เพิ่มนี้เพื่อใช้งาน Text Widget
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

def find_path_edge(path):
    src_dest = []
    for sd_edge in range(len(path)-1):
        closest_path = nx.shortest_path(g, path[sd_edge], path[sd_edge+1], weight='weight')
        src_dest.append(closest_path)
    srcdest_edge = []
    for sub in src_dest :
        for res in sub:
            srcdest_edge.append(res)
    # print(srcdest_edge)
    edge = [srcdest_edge[0]]
    for i in range(1, len(srcdest_edge)):
        if srcdest_edge[i] != srcdest_edge[i - 1]:  # ถ้าข้อมูลไม่เท่ากับข้อมูลก่อนหน้า (ไม่ซ้ำ)
            edge.append(srcdest_edge[i])  # เพิ่มข้อมูลเข้าไปใน new_list 
    # print(edge)
    main_dis = db.get_distanc()
    edge_use = []
    for i in range(len(edge)-1):

        for m in main_dis:
            
            if edge[i] == m[0] and edge[i+1] == m[1]:
                edge_use.append(m)
    return edge_use
def total_dis(edge):
    dis = 0
    for i in edge:
        dis += i[2]
    return dis
def find_path(slcnode):    
    path = [slcnode[0]]
    # print(slcnode)
    while(len(path) < len(slcnode)-1):
        sort_i = sort_nodes_by_distance(g,path[len(path)-1])
        # print(sort_i)
        lestes = 9999999
        for k in slcnode:
            # print(sort_i[sort_i.index(k)])
            # print(sort_i.index(k))
            # print(sort_i)
            if sort_i.index(k) <= lestes and sort_i.index(k) != 0 and sort_i[sort_i.index(k)] != 'SV02' and sort_i[sort_i.index(k)] != 'SV01' and sort_i[sort_i.index(k)] not in path :
                lestes = sort_i.index(k)
        # print(lestes)
        path.append(sort_i[lestes])   
    # print(path)
    path.insert(len(path),'SV02')
    # print(path)
    # # path=['FV02', 'FV02','FV01', 'SV02']    
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


def on_select(event=None):
    global selected_items
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(idx) for idx in selected_indices]
    listbox_selection.delete(1.0, tk.END)  # เคลียร์ข้อความทั้งหมดใน Text Widget
    listbox_selection.insert(tk.END, "You selected:\n")  # เพิ่มข้อความ "You selected:" ที่บรรทัดแรก
    for item in selected_items:
        listbox_selection.insert(tk.END, f"{item}\n")  # เพิ่มรายการที่เลือกแต่ละรายการในบรรทัดใหม่
    draw_graph()  

dis = ''
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
    # print('โนดที่เลือก',selected_nodes)
    pathsh = find_path_edge(find_path(selected_nodes))
    # print(pathsh)
    selected_nodes = find_path(selected_nodes)
    # namepro = []
    # for prenode in selected_nodes:
    #     re = (prenode,{'label':str(db.get_productname_by_idshelf(prenode))})
    #     namepro.append(re)
    # print(namepro)   
    global dis
    dis = total_dis(pathsh)
    dis = 'Total Distance : '+ str(dis)
    my_label.config(text=dis)
    # print(dis)
    network.add_nodes_from(selected_nodes)
    network.add_weighted_edges_from(pathsh)
    pos = db.get_pos_node()
    fig, ax = plt.subplots(figsize=(16, 7.14))  # Set the size of the graph
    img = mpimg.imread("BG.png")  # Load the background image
    ax.imshow(img, aspect='auto')  # Set the background image of the graph
    nx.draw(network, pos, ax=ax, with_labels=True, node_size=250, node_color='black', font_size=6, edge_color='blue', font_color='white')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=0, y=0)  # Show the matplotlib canvas at position (0, 0)



def exit_program():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

root = tk.Tk()
root.title('makro')

canvas = tk.Canvas(root, width=1600, height=900, relief='flat')
canvas.pack()

listbox_selection = scrolledtext.ScrolledText(root, width=40, height=5, wrap=tk.WORD)  # ใช้ scrolledtext.ScrolledText แทน Label
listbox_selection.place(x=950, y=750)

listbox_frame = tk.Frame(root)
listbox_frame.place(x=800, y=720)

listbox_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
listbox_scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, yscrollcommand=listbox_scrollbar.set)
listbox.pack(side="left", fill="both", expand=True)

listbox_scrollbar.config(command=listbox.yview)

items = db.get_productname()
for item in items:
    listbox.insert(tk.END, item)
    
listbox.bind("<<ListboxSelect>>", on_select)
my_label = tk.Label(root, text=dis, font=("Arial", 12))
my_label.place(x=960, y=720)
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.place(relx=1, rely=1, anchor="se")
list_product  = tk.Label(root, text='รายการสินค้า', font=("Arial", 12))
list_product.place(x=700, y=720)
on_select()

root.mainloop()
