from graph.geo import haversine

def build_graph(nodes,ways):
    graph={}

    for way in ways:
        for i in range(len(way)-1):
            u=way[i]
            v=way[i+1]
        
            if u not in nodes or v not in nodes:
                continue
            
            lat1, lon1=nodes[u]
            lat2, lon2=nodes[v]

            dist=haversine(lat1,lon1,lat2,lon2)

            graph.setdefault(u,[]).append((v,dist))
            graph.setdefault(v,[]).append((u,dist))

    return graph