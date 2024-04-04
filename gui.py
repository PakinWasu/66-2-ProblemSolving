import tkinter as tk
import DBfunction as db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.image as mpimg


def on_select():
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(idx) for idx in selected_indices]
    label.config(text="You selected: " + ", ".join(selected_items))
    print(selected_items)
    return selected_items


def draw_graph():
    network = nx.Graph()
    network.add_nodes_from(db.get_node())
    print(f"This network has now {network.number_of_nodes()} nodes.")
    for edge in db.get_distanc():
        network.add_edge(edge[0],edge[1], weight = edge[2])

    pos = db.get_pos_node()

    fig, ax = plt.subplots(figsize=(16,7.14))  # กำหนดขนาดของกราฟ
    img = mpimg.imread("BG.png")  # โหลดภาพเป็นพื้นหลัง
    ax.imshow(img, aspect='auto')  # กำหนดภาพเป็นพื้นหลังของกราฟ

    nx.draw(network, pos, ax=ax, with_labels=True, node_size=250, node_color='black', font_size=6,edge_color='blue', font_color='white')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=0, y=0)  # แสดง Canvas ของ matplotlib ที่ตำแหน่ง (0, 0)


root = tk.Tk()
root.title('makro')

# สร้าง Canvas ให้กับภาพพื้นหลัง
canvas = tk.Canvas(root, width=1600, height=900, relief='flat')
canvas.pack()

# สร้างกราฟ
draw_graph()

# สร้าง Listbox
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
listbox.place(x=800, y=720)

# เพิ่มรายการใน Listbox
items = db.get_productname()
for item in items:
    listbox.insert(tk.END, item)

# สร้าง Button เพื่อเลือกรายการ
select_button = tk.Button(root, text="Select", command=on_select)
select_button.place(x=950, y=800)

# สร้าง Label เพื่อแสดงข้อความของรายการที่เลือก
label = tk.Label(root, text="")
label.place(x=950, y=830)

root.mainloop()
