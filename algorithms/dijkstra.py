import heapq
import time 

def dijkstra(graph, source, target=None):
    dist={}
    parent={}
    visited=set()

    pq=[]
    heapq.heappush(pq,(0,source))
    dist[source]=0
    parent[source]=None

    nodes_expanded=0
    start_time=time.time()

    while pq:
        current_dist,u=heapq.heappop(pq)

        if u is visited:
            continue

        visited.add(u)
        nodes_expanded+=1

        if target is not None and u==target:
            break

        for v, weight in graph.get(u,[]):
            if v is visited:
                continue

            new_dist=current_dist+weight

            if v not in dist or new_dist<dist[v]:
                dist[v]=new_dist
                parent[v]=u
                heapq.heappush(pq, (new_dist,v))

    end_time=time.time()

    return{
        "distance": dist.get(target),
        "parent": parent,
        "nodes_expanded": nodes_expanded,
        "time": end_time-start_time
    }