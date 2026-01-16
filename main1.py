from graph.osm_parser import OSMHandler
from graph.graph_builder import build_graph
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar
from algorithms.path import reconstruct_path
from graph.geo import haversine
from graph.kdtree import build_tree, nearest_neighbor
import osmium
import random
import json
from collections import deque


handler=OSMHandler()
handler.apply_file("data/delhi.osm.pbf")

# print("Total nodes: ", len(handler.nodes))
# print("Total ways: ", len(handler.ways))

graph=build_graph(handler.nodes, handler.ways)

# print("Graph Nodes: ", len(graph))
# edge_count=sum(len(v) for v in graph.values())
# print("Edges: ", edge_count)

def path_to_coordinates(path,nodes_dict):
    return [nodes_dict[node] for node in path]

def export_route_geojson(coords, filename="route.geojson"):
    """
    Exports route coordinates to a GeoJSON LineString
    """
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [lon, lat] for lat, lon in coords
                    ]
                },
                "properties": {
                    "name": "Shortest Path Route"
                }
            }
        ]
    }

    with open(filename, "w") as f:
        json.dump(geojson, f, indent=2)

print("KDTree Building...")
points=[
    (lat,lon,node_id) 
    for node_id,(lat,lon) in handler.nodes.items() 
    if node_id in graph
]
kdtree_root=build_tree(points)
src_lat, src_lon = 28.6139, 77.2090   # Connaught Place
dst_lat, dst_lon = 28.4595, 77.0266   # Gurgaon side

src_node,src_dist=nearest_neighbor(kdtree_root,(src_lat, src_lon))
dst_node,dst_dist=nearest_neighbor(kdtree_root,(dst_lat, dst_lon))

src=src_node.node_id
dest=dst_node.node_id

print("Snapped source distance (m):",src_dist)
print("Snapped destination distance (m):",dst_dist)


result_d=dijkstra(graph,src,dest)
result_a=astar(graph,handler.nodes,src,dest)
path=reconstruct_path(result_a["parent"], src, dest)
if path is None:
    print("No path found")
else: 
    print("Path length (nodes)", len(path))

coords=path_to_coordinates(path,handler.nodes)
print("first 5 coords", coords[:5])

export_route_geojson(coords)
print("Route exported to route.geojson")

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