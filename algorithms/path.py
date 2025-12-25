def reconstruct_path(parent,src,dest):
    if dest not in parent:
        return None
    
    path=[]
    curr=dest

    while curr is not None:
        path.append(curr)
        curr=parent[curr]

    path.reverse()

    if path[0]!=src:
        return None

    return path