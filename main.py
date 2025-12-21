# from graph.osm_parser import OSMHandler
# from graph.graph_builder import build_graph
# from algorithms.dijkstra import dijkstra
# from algorithms.astar import astar
# from graph.geo import haversine
# import osmium
# import random
# from collections import deque


# handler=OSMHandler()
# handler.apply_file("data/delhi.osm.pbf")

# # print("Total nodes: ", len(handler.nodes))
# # print("Total ways: ", len(handler.ways))

# graph=build_graph(handler.nodes, handler.ways)

# # print("Graph Nodes: ", len(graph))
# # edge_count=sum(len(v) for v in graph.values())
# # print("Edges: ", edge_count)

# def pick(nodes_dict, graph):
#     nodes=list(graph.keys())
#     src=random.choice(nodes)
#     lat1,lon1=nodes_dict[src]

#     max_dist=-1
#     dst=None

#     for _ in range(2000):
#         n=random.choice(nodes)
#         lat2,lon2=nodes_dict[n]
#         d=haversine(lat1,lon1,lat2,lon2)
#         if d>max_dist:
#             max_dist=d
#             dst=n

#     return src,dst

# src,dist=pick(handler.nodes,graph)

# result_d=dijkstra(graph,src,dist)
# result_a=astar(graph,handler.nodes,src,dist)

# print("Dijkstra")
# print("Distance(m)", result_d["distance"])
# print("Nodes expanded", result_d["nodes_expanded"])
# print("Time Taken (s)", result_d["time"])

# print("A*")
# print("Distance(m)", result_a["distance"])
# print("Nodes expanded", result_a["nodes_expanded"])
# print("Time Taken (s)", result_a["time"])

from graph.osm_parser import OSMHandler
from graph.graph_builder import build_graph
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar
from graph.geo import haversine
import osmium
import random
from collections import deque

handler = OSMHandler()
handler.apply_file("data/delhi.osm.pbf")
graph = build_graph(handler.nodes, handler.ways)

print(f"Total nodes in graph: {len(graph)}")
print(f"Total edges: {sum(len(v) for v in graph.values())}")

def find_largest_component(graph):
    """Find the largest connected component in the graph"""
    visited = set()
    components = []
    
    for node in graph:
        if node not in visited:
            component = set()
            queue = deque([node])
            
            while queue:
                current = queue.popleft()
                if current in visited:
                    continue
                visited.add(current)
                component.add(current)
                
                for neighbor, _ in graph.get(current, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
            
            components.append(component)
    
    # Return the largest component
    largest = max(components, key=len)
    print(f"Largest connected component has {len(largest)} nodes")
    print(f"Total components: {len(components)}")
    return largest

def pick_from_component(nodes_dict, component):
    """Pick two distant nodes from the same connected component"""
    nodes = list(component)
    src = random.choice(nodes)
    lat1, lon1 = nodes_dict[src]
    
    max_dist = -1
    dst = None
    
    # Try more samples to find a distant pair
    for _ in range(min(5000, len(nodes))):
        n = random.choice(nodes)
        lat2, lon2 = nodes_dict[n]
        d = haversine(lat1, lon1, lat2, lon2)
        if d > max_dist:
            max_dist = d
            dst = n
    
    print(f"\nSelected nodes:")
    print(f"Source: {src} at ({lat1:.6f}, {lon1:.6f})")
    print(f"Destination: {dst} at ({nodes_dict[dst][0]:.6f}, {nodes_dict[dst][1]:.6f})")
    print(f"Straight-line distance: {max_dist:.2f} meters ({max_dist/1000:.2f} km)")
    
    return src, dst

# Find largest connected component
largest_component = find_largest_component(graph)

# Create a subgraph with only the largest component
subgraph = {node: graph[node] for node in largest_component}

# Pick nodes from the same component
src, dst = pick_from_component(handler.nodes, largest_component)

print("\n" + "="*60)
print("Running Dijkstra...")
result_d = dijkstra(subgraph, src, dst)

print("\n" + "="*60)
print("Running A*...")
result_a = astar(subgraph, handler.nodes, src, dst)

print("\n" + "="*60)
print("COMPARISON RESULTS")
print("="*60)

print("\nDijkstra:")
print(f"  Distance (m): {result_d['distance']:.2f}" if result_d['distance'] else "  Distance: No path found")
print(f"  Nodes expanded: {result_d['nodes_expanded']}")
print(f"  Time taken (s): {result_d['time']:.6f}")

print("\nA*:")
print(f"  Distance (m): {result_a['distance']:.2f}" if result_a['distance'] else "  Distance: No path found")
print(f"  Nodes expanded: {result_a['nodes_expanded']}")
print(f"  Time taken (s): {result_a['time']:.6f}")

if result_d['distance'] and result_a['distance']:
    print("\nPerformance Comparison:")
    print(f"  A* explored {result_d['nodes_expanded'] - result_a['nodes_expanded']} fewer nodes")
    print(f"  A* was {result_d['time'] / result_a['time']:.2f}x faster")
    print(f"  Distance difference: {abs(result_d['distance'] - result_a['distance']):.2f}m")