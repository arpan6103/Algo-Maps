***AlgoMaps - A Real-World Routing Engine on OpenStreetMap***

AlgoMaps is a navigation engine prototype that computes shortest routes on real-world road networks using OpenStreetMap (OSM) data.
It implements and benchmarks Dijkstra and A* on a large metropolitan graph and reconstructs the actual driving route as a geographic polyline.


**KeyFeatures:**
- Parses OpenStreetMap (.osm.pbf) data using pyosmium
- Builds a road graph with realistic edge weights (Haversine distance)
- Implements:
    - Dijkstra’s Algorithm
    - A* with admissible geographic heuristic
- Path reconstruction using predecessor pointers
- GeoJSON route export for visualization
- KD-Tree spatial index to map arbitrary GPS coordinates → nearest road node
- Benchmarked on a large city-scale graph (Delhi)


**System Architecture**

(lat, lon)
   ↓
KD-Tree (nearest road node)
   ↓
Graph (OSM road network)
   ↓
A* / Dijkstra
   ↓
Parent pointers
   ↓
Reconstructed path
   ↓
GeoJSON route


**Project Structure**

algomaps/
├── algorithms/
│   ├── dijkstra.py        # Dijkstra shortest path
│   ├── astar.py           # A* search with Haversine heuristic
│   ├── path.py            # Path reconstruction
│
├── graph/
│   ├── osm_parser.py      # OSM parsing (roads only)
│   ├── graph_builder.py   # Graph construction
│   ├── geo.py             # Haversine distance
│   ├── kdtree.py          # KD-Tree for nearest-node lookup
│
├── data/
│   └── delhi.osm.pbf      # OpenStreetMap extract
│
├── main.py                # End-to-end pipeline
└── README.md


**Algorithms Implemented**

- Dijkstra
    - Explores the graph uniformly
    - Guarantees optimal shortest path
    - Used as a correctness and performance baseline

- A*
    - Uses Haversine distance as an admissible heuristic
    - Dramatically reduces node expansions on long routes
    - Returns the same optimal path as Dijkstra

- KD-Tree (Spatial Index)
    - 2D KD-Tree on (latitude, longitude)
    - Enables fast nearest road node lookup from GPS coordinates
    - Average query time: O(log N)


**Real-World Benchmark (Delhi Road Network)**
- Example long-distance route:
    - Route length: ~63.7 km
    - Path nodes: 1467

*Algorithm*	  *Nodes Expanded*	  *Time (s)*
 Dijkstra	   1,038,352	       1.16
 A*	           356,746	           0.66
A* reduced node expansions by ~65% and runtime by ~40% while preserving optimality.


**How to Run**
1. Install dependencies
    pip install osmium

2. Place OSM data
    Put an .osm.pbf file inside the data/ directory.

3. Run the pipeline
    python3 main.py

- The script:
    - Snaps source & destination GPS coordinates to the nearest road
    - Computes the shortest route using A*
    - Exports route.geojson


**Limitations & Future Work**
- No traffic-aware or time-dependent edge weights
- Single-level graph (no contraction hierarchies)
- In-memory graph only

*Possible extensions:*
- Bidirectional A*
- Hierarchical routing
- Traffic modeling
- Web-based UI