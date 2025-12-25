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