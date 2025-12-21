"""
Final working version that handles OSM data correctly
"""

from graph.osm_parser import load_osm_data, diagnose_osm_file
from graph.graph_builder import build_graph
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar
from graph.geo import haversine
import random
from collections import deque
import sys

# First, run diagnostics to see what we're working with
OSM_FILE = "data/north-eastern.osm.pbf"

print("Running diagnostics on OSM file...")
diagnose_osm_file(OSM_FILE)

print("\n" + "="*60)
print("LOADING AND BUILDING GRAPH")
print("="*60)

# Load OSM data
handler = load_osm_data(OSM_FILE)

# Build graph
graph = build_graph(handler.nodes, handler.ways)

print(f"\nGraph statistics:")
print(f"  Nodes: {len(graph)}")
print(f"  Edges: {sum(len(v) for v in graph.values())}")


def find_components(graph):
    """Find connected components"""
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
    
    components.sort(key=len, reverse=True)
    return components


def pick_distant_pair(nodes_dict, component):
    """Pick two distant nodes"""
    nodes = list(component)
    
    # Sample some pairs and pick the most distant
    best_dist = 0
    best_src = None
    best_dst = None
    
    for _ in range(min(1000, len(nodes))):
        src = random.choice(nodes)
        dst = random.choice(nodes)
        
        if src == dst:
            continue
        
        lat1, lon1 = nodes_dict[src]
        lat2, lon2 = nodes_dict[dst]
        dist = haversine(lat1, lon1, lat2, lon2)
        
        if dist > best_dist:
            best_dist = dist
            best_src = src
            best_dst = dst
    
    return best_src, best_dst, best_dist


# Analyze connectivity
print("\n" + "="*60)
print("CONNECTIVITY ANALYSIS")
print("="*60)

components = find_components(graph)

print(f"\nConnected components: {len(components)}")
print(f"\nTop 10 largest components:")
for i, comp in enumerate(components[:10]):
    print(f"  {i+1}. {len(comp):,} nodes")

largest = components[0]

if len(largest) < 100:
    print(f"\n⚠️  ERROR: Largest component only has {len(largest)} nodes!")
    print("   Your OSM file appears to be severely fragmented or incomplete.")
    print("\nPossible solutions:")
    print("   1. Download a fresh .osm.pbf from https://download.geofabrik.de/")
    print("   2. Try a smaller region (e.g., city extract instead of state)")
    print("   3. Use .osm format instead of .pbf")
    print("\nFor now, testing with available data...")

# Use largest component
subgraph = {node: graph[node] for node in largest}
src, dst, straight_dist = pick_distant_pair(handler.nodes, largest)

print(f"\n" + "="*60)
print("TEST CONFIGURATION")
print(f"="*60)
print(f"Component size: {len(largest):,} nodes")
print(f"Source: {src}")
print(f"Destination: {dst}")
print(f"Straight-line distance: {straight_dist:.0f}m ({straight_dist/1000:.1f}km)")

# Run pathfinding
print(f"\n" + "="*60)
print("RUNNING ALGORITHMS")
print(f"="*60)

print("\nDijkstra...")
result_d = dijkstra(subgraph, src, dst)

print("A*...")
result_a = astar(subgraph, handler.nodes, src, dst)

# Results
print(f"\n" + "="*60)
print("RESULTS")
print(f"="*60)

def format_result(name, result):
    print(f"\n{name}:")
    if result['distance']:
        print(f"  Path distance: {result['distance']:.0f}m ({result['distance']/1000:.1f}km)")
        print(f"  Nodes expanded: {result['nodes_expanded']:,}")
        print(f"  Time: {result['time']*1000:.2f}ms")
    else:
        print(f"  No path found")
        print(f"  Nodes expanded: {result['nodes_expanded']:,}")

format_result("Dijkstra", result_d)
format_result("A*", result_a)

if result_d['distance'] and result_a['distance']:
    print(f"\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print(f"="*60)
    
    node_diff = result_d['nodes_expanded'] - result_a['nodes_expanded']
    node_reduction = (node_diff / result_d['nodes_expanded']) * 100
    
    print(f"\nNode Exploration:")
    print(f"  Dijkstra: {result_d['nodes_expanded']:,} nodes")
    print(f"  A*: {result_a['nodes_expanded']:,} nodes")
    print(f"  Reduction: {node_diff:,} nodes ({node_reduction:.1f}%)")
    
    print(f"\nTime:")
    print(f"  Dijkstra: {result_d['time']*1000:.2f}ms")
    print(f"  A*: {result_a['time']*1000:.2f}ms")
    if result_a['time'] > 0:
        speedup = result_d['time'] / result_a['time']
        print(f"  Speedup: {speedup:.2f}x")
    
    print(f"\nPath Quality:")
    dist_diff = abs(result_d['distance'] - result_a['distance'])
    print(f"  Distance difference: {dist_diff:.2f}m")
    print(f"  Both optimal: {'✓ Yes' if dist_diff < 0.01 else '✗ No'}")
    
    print(f"\n{'='*60}")
    if node_reduction > 30:
        print("✓ A* is significantly more efficient!")
    elif node_reduction > 10:
        print("✓ A* shows moderate improvement")
    else:
        print("⚠️  Limited improvement (path may be too short)")
    print(f"{'='*60}")
else:
    print("\n⚠️  Could not find path between selected nodes")