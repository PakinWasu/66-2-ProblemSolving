import tkinter as tk
import DBfunction as db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.image as mpimg

selected_items = []  # Initialize a variable to store selected items

def on_select():
    global selected_items
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(idx) for idx in selected_indices]
    label.config(text="You selected: " + ", ".join(selected_items))
    draw_graph()  # Redraw the graph when selection changes

def draw_graph():
    network = nx.Graph()
    selected_nodes = set(db.get_idshelf_by_productname(selected_items))  # Convert selected items to a set for faster lookup
    selected_edges = []  # Initialize a list to store selected edges

    for edge in db.get_distanc():
        if edge[0] in selected_nodes and edge[1] in selected_nodes:
            selected_edges.append(edge)

    network.add_nodes_from(selected_nodes)
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

# Create the Button to select items
select_button = tk.Button(root, text="Select", command=on_select)
select_button.place(x=950, y=800)

# Create the Label to display selected items
label = tk.Label(root, text="")
label.place(x=950, y=830)

root.mainloop()
# Now you can use the selected_items variable to access the selected items elsewhere in your code.
