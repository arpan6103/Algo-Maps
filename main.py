from graph.osm_parser import OSMHandler
from graph.graph_builder import build_graph
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar
from algorithms.path import reconstruct_path
from graph.geo import haversine
import osmium
import random
from collections import deque


handler=OSMHandler()
handler.apply_file("data/delhi.osm.pbf")

# print("Total nodes: ", len(handler.nodes))
# print("Total ways: ", len(handler.ways))

graph=build_graph(handler.nodes, handler.ways)

# print("Graph Nodes: ", len(graph))
# edge_count=sum(len(v) for v in graph.values())
# print("Edges: ", edge_count)

def pick(nodes_dict, graph):
    nodes=list(graph.keys())
    src=random.choice(nodes)
    lat1,lon1=nodes_dict[src]

    max_dist=-1
    dst=None

    for _ in range(2000):
        n=random.choice(nodes)
        lat2,lon2=nodes_dict[n]
        d=haversine(lat1,lon1,lat2,lon2)
        if d>max_dist:
            max_dist=d
            dst=n

    return src,dst

src,dest=pick(handler.nodes,graph)

result_d=dijkstra(graph,src,dest)
result_a=astar(graph,handler.nodes,src,dest)
path=reconstruct_path(result_a["parent"], src, dest)
if path is None:
    print("No path found")
else: 
    print("Path length (nodes)", len(path))

print("Dijkstra")
print("distance(m)", result_d["distance"])
print("Nodes expanded", result_d["nodes_expanded"])
print("Time Taken (s)", result_d["time"])

print("A*")
print("distance(m)", result_a["distance"])
print("Nodes expanded", result_a["nodes_expanded"])
print("Time Taken (s)", result_a["time"])

print("source: ", src)
print("destination", dest)


