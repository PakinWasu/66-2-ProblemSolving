import networkx as nx
# import matplotlib.pyplot as plt
import DBfunction as db

network = nx.Graph()
network.add_nodes_from(db.get_node())
print(f"This network has now {network.number_of_nodes()} nodes.")
for edge in db.get_distanc():
    network.add_edge(edge[0],edge[1], weight = edge[2])


# def find_bestpath(source,target):
#     source = db.get_idshelf_by_productname(source)
#     target = db.get_idshelf_by_productname(target)
#     shortest_path = nx.shortest_path(network, source, target, weight='weight')
#     return(shortest_path)

def find_total_weigth(shortest_path):
    total_weight_decimal_shortest_path = sum(network[shortest_path[i]][shortest_path[i+1]]['weight'] 
                                            for i in range(len(shortest_path)-1) 
                                                if isinstance(network[shortest_path[i]][shortest_path[i+1]]['weight'], float))
    format_total_weight = f"{total_weight_decimal_shortest_path:.1f}"
    return(format_total_weight)






def find_shortest_path_through_node(graph, start_node, end_node, required_nodes):
    """
    หาเส้นทางที่สั้นที่สุดที่ผ่านโหนดที่กำหนด
    :param graph: กราฟ NetworkX
    :param start_node: โหนดเริ่มต้น
    :param end_node: โหนดปลายทาง
    :param required_nodes: โหนดที่ต้องการให้เส้นทางผ่าน (list)
    :return: เส้นทางที่สั้นที่สุดที่ผ่านโหนดที่กำหนด
    """
    # หาเส้นทางที่สั้นที่สุด
    shortest_path = nx.shortest_path(graph, source=start_node, target=end_node)
    # กรองเส้นทางที่ผ่านโหนดที่กำหนดออก
    shortest_path_through_required_nodes = [node for node in shortest_path if node in required_nodes]
    # ตรวจสอบว่าเส้นทางที่ได้ผ่านโหนดที่กำหนดหรือไม่
    if all(node in required_nodes for node in shortest_path_through_required_nodes):
        return shortest_path_through_required_nodes
    else:
        return "ไม่พบเส้นทางที่ผ่านโหนดที่กำหนด"


start_node = 'SV01'
end_node = 'SV02'
# โหนดที่ต้องผ่าน (ลิสต์ของโหนด)
intermediate_nodes = ['FV01','FV09']
shortest_path = find_shortest_path_through_node(network, start_node, end_node, intermediate_nodes)
print("Shortest path:", shortest_path)
print(find_total_weigth(shortest_path))