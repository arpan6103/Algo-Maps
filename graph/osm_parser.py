import osmium

ALLOWED_HIGHWAYS = {
    'motorway', 'trunk', 'primary', 'secondary', 'tertiary',
    'motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link',
    'residential', 'unclassified', 'service', 'living_street', 'road'
}

class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.nodes = {}
        self.ways = []
    
    def node(self, n):
        """Store all nodes (we'll still keep this for any standalone nodes)"""
        self.nodes[n.id] = (n.location.lat, n.location.lon)
    
    def way(self, w):
        """Extract ways and their node coordinates"""
        if "highway" not in w.tags:
            return
        if w.tags["highway"] not in ALLOWED_HIGHWAYS:
            return
        
        node_ids = []
        for n in w.nodes:
            node_id = n.ref
            node_ids.append(node_id)
            
            if node_id not in self.nodes:
                try:
                    if n.location.valid():
                        self.nodes[node_id] = (n.location.lat, n.location.lon)
                except:
                    pass
        
        if len(node_ids) >= 2:
            self.ways.append(node_ids)

# """
# Complete solution for loading OSM data properly
# This handles the node location issue that causes fragmentation
# """

# import osmium
# import sys

# ALLOWED_HIGHWAYS = {
#     'motorway', 'trunk', 'primary', 'secondary', 'tertiary',
#     'motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link',
#     'residential', 'unclassified', 'service', 'living_street', 'road'
# }


# class OSMHandler(osmium.SimpleHandler):
#     """
#     Handler that properly extracts nodes and ways with complete location data
#     """
#     def __init__(self):
#         super().__init__()
#         self.nodes = {}
#         self.ways = []
#         self.nodes_in_ways = set()  # Track which nodes are actually used
#         self.ways_processed = 0
#         self.ways_skipped = 0
    
#     def way(self, w):
#         """Process ways first to know which nodes we need"""
#         # Filter by highway type
#         if "highway" not in w.tags:
#             self.ways_skipped += 1
#             return
            
#         if w.tags["highway"] not in ALLOWED_HIGHWAYS:
#             self.ways_skipped += 1
#             return
        
#         # Extract node IDs
#         node_ids = [n.ref for n in w.nodes]
        
#         if len(node_ids) < 2:
#             self.ways_skipped += 1
#             return
        
#         # Store the way
#         self.ways.append(node_ids)
#         self.nodes_in_ways.update(node_ids)
#         self.ways_processed += 1


# class NodeLocationHandler(osmium.SimpleHandler):
#     """
#     Second pass: extract coordinates for nodes we actually need
#     """
#     def __init__(self, needed_nodes):
#         super().__init__()
#         self.needed_nodes = needed_nodes
#         self.nodes = {}
#         self.found_count = 0
    
#     def node(self, n):
#         if n.id in self.needed_nodes:
#             try:
#                 if n.location.valid():
#                     self.nodes[n.id] = (n.location.lat, n.location.lon)
#                     self.found_count += 1
#             except:
#                 pass


# def load_osm_data_two_pass(filepath):
#     """
#     Load OSM data using two-pass approach
    
#     Pass 1: Extract all ways and collect needed node IDs
#     Pass 2: Extract coordinates only for nodes we actually need
    
#     This is more efficient and ensures we get all required data
#     """
#     print("Loading OSM data (two-pass approach)...")
#     print("Pass 1: Extracting ways...")
    
#     # First pass: get ways
#     way_handler = OSMHandler()
#     way_handler.apply_file(filepath)
    
#     print(f"  Ways processed: {way_handler.ways_processed}")
#     print(f"  Ways skipped: {way_handler.ways_skipped}")
#     print(f"  Unique nodes needed: {len(way_handler.nodes_in_ways)}")
    
#     # Second pass: get node coordinates
#     print("Pass 2: Extracting node coordinates...")
#     node_handler = NodeLocationHandler(way_handler.nodes_in_ways)
#     node_handler.apply_file(filepath)
    
#     print(f"  Nodes found: {node_handler.found_count} / {len(way_handler.nodes_in_ways)}")
    
#     # Check for missing nodes
#     missing = len(way_handler.nodes_in_ways) - node_handler.found_count
#     if missing > 0:
#         print(f"  ⚠️  Warning: {missing} nodes missing from file")
#         print(f"     ({missing / len(way_handler.nodes_in_ways) * 100:.1f}% missing)")
    
#     # Create a handler-like object to return
#     class Result:
#         def __init__(self, nodes, ways):
#             self.nodes = nodes
#             self.ways = ways
    
#     return Result(node_handler.nodes, way_handler.ways)


# def load_osm_data_single_pass(filepath):
#     """
#     Alternative: Single pass with location cache
#     Try this if two-pass doesn't work
#     """
#     print("Loading OSM data (single-pass with cache)...")
    
#     handler = osmium.SimpleHandler()
#     handler.nodes = {}
#     handler.ways = []
    
#     # We'll manually process the file with location index
#     try:
#         # Create a location handler that caches node positions
#         idx = osmium.index.create_map("sparse_mem_array")
#         lh = osmium.NodeLocationsForWays(idx)
        
#         # First pass: build location index
#         lh.apply_file(filepath)
        
#         # Second pass: process ways with locations
#         class WayHandler(osmium.SimpleHandler):
#             def __init__(self, nodes, ways):
#                 super().__init__()
#                 self.nodes = nodes
#                 self.ways = ways
            
#             def way(self, w):
#                 if "highway" not in w.tags:
#                     return
#                 if w.tags["highway"] not in ALLOWED_HIGHWAYS:
#                     return
                
#                 node_ids = []
#                 for n in w.nodes:
#                     try:
#                         if n.location.valid():
#                             self.nodes[n.ref] = (n.location.lat, n.location.lon)
#                             node_ids.append(n.ref)
#                     except:
#                         pass
                
#                 if len(node_ids) >= 2:
#                     self.ways.append(node_ids)
        
#         way_handler = WayHandler(handler.nodes, handler.ways)
#         way_handler.apply_file(filepath, locations=True, idx=lh)
        
#         print(f"  Loaded {len(handler.nodes)} nodes and {len(handler.ways)} ways")
        
#     except Exception as e:
#         print(f"  Error with location cache: {e}")
#         print("  Falling back to two-pass approach...")
#         return load_osm_data_two_pass(filepath)
    
#     return handler


# # Main loading function - tries best method
# def load_osm_data(filepath):
#     """
#     Load OSM data - automatically chooses best method
#     """
#     try:
#         # Try single-pass with location cache first (faster)
#         return load_osm_data_single_pass(filepath)
#     except Exception as e:
#         print(f"Single-pass failed: {e}")
#         print("Trying two-pass approach...")
#         return load_osm_data_two_pass(filepath)


# # Diagnostic function
# def diagnose_osm_file(filepath):
#     """
#     Run diagnostics on an OSM file to see what's wrong
#     """
#     print("\n" + "="*60)
#     print("OSM FILE DIAGNOSTICS")
#     print("="*60)
    
#     class DiagHandler(osmium.SimpleHandler):
#         def __init__(self):
#             super().__init__()
#             self.node_count = 0
#             self.way_count = 0
#             self.highway_ways = 0
#             self.nodes_with_location = 0
#             self.highway_types = {}
        
#         def node(self, n):
#             self.node_count += 1
#             try:
#                 if n.location.valid():
#                     self.nodes_with_location += 1
#             except:
#                 pass
        
#         def way(self, w):
#             self.way_count += 1
#             if "highway" in w.tags:
#                 self.highway_ways += 1
#                 ht = w.tags["highway"]
#                 self.highway_types[ht] = self.highway_types.get(ht, 0) + 1
    
#     handler = DiagHandler()
#     handler.apply_file(filepath)
    
#     print(f"\nFile contents:")
#     print(f"  Total nodes: {handler.node_count}")
#     print(f"  Nodes with valid locations: {handler.nodes_with_location}")
#     print(f"  Total ways: {handler.way_count}")
#     print(f"  Highway ways: {handler.highway_ways}")
    
#     print(f"\nTop highway types:")
#     for ht, count in sorted(handler.highway_types.items(), key=lambda x: x[1], reverse=True)[:10]:
#         in_allowed = "✓" if ht in ALLOWED_HIGHWAYS else "✗"
#         print(f"  {in_allowed} {ht}: {count}")
    
#     print("\n" + "="*60)