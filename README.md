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

<img width="260" height="293" alt="Screenshot 2026-01-28 at 13 30 58" src="https://github.com/user-attachments/assets/1861c55d-8216-4d1a-a4e6-c660f725f99b" />


**Project Structure**

<img width="539" height="370" alt="Screenshot 2026-01-28 at 13 20 06" src="https://github.com/user-attachments/assets/d52bd102-4cc1-4c7f-9620-2f0746f799bd" />


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
 

<img width="635" height="122" alt="Screenshot 2026-01-29 at 11 20 45 AM" src="https://github.com/user-attachments/assets/aa60710b-9965-4de5-80b5-0598308ab6df" />

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
