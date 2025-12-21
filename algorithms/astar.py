import heapq
import time
from graph.geo import haversine

def astar(graph, nodes, source, target):
    g_score={source: 0}
    parent={source: None}
    visited=set()

    pq=[]
    heapq.heappush(pq, (0,source))

    nodes_expanded=0
    start_time=time.time()

    tgt_lat, tgt_lon=nodes[target]

    while pq:
        _, u=heapq.heappop(pq)
        
        if u is visited:
            continue

        visited.add(u)
        nodes_expanded+=1

        if u==target:
            break

        for v, weight in graph.get(u,[]):
            if v in visited:
                continue

            tentative_g=g_score[u]+weight

            if v not in g_score or tentative_g<g_score[v]:
                g_score[v]=tentative_g
                parent[v]=u

                h=haversine(nodes[v][0], nodes[v][1], tgt_lat, tgt_lon)

                f=tentative_g+h
                heapq.heappush(pq, (f,v))

    end_time=time.time()

    return{
        "distance": g_score.get(target),
        "parent": parent,
        "nodes_expanded": nodes_expanded,
        "time": end_time-start_time
    }