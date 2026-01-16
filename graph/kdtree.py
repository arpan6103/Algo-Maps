from graph.geo import haversine

class KDNode:
    def __init__(self,point,node_id,axis,left=None,right=None):
        self.point=point
        self.node_id=node_id
        self.axis=axis
        self.left=left
        self.right=right

def build_tree(points,depth=0):
    if not points:
        return None
    
    axis=depth%2
    points.sort(key=lambda x:x[axis])
    median=len(points)//2

    return KDNode(
        point=(points[median][0],points[median][1]),
        node_id=points[median][2],
        axis=axis,
        left=build_tree(points[:median],depth+1),
        right=build_tree(points[median+1:],depth+1)
    )

def nearest_neighbor(root,target_point,best=None):
    if root is None:
        return best
    
    lat,lon=target_point
    root_lat,root_lon=root.point
    d=haversine(lat,lon,root_lat,root_lon)
    if best is None or d<best[1]:
        best=(root,d)

    axis=root.axis
    diff=(lat-root_lat) if axis==0 else (lon-root_lon)

    first=root.left if diff<0 else root.right
    second=root.right if diff<0 else root.left

    best=nearest_neighbor(first,target_point,best)

    if abs(diff)<best[1]:
        best=nearest_neighbor(second,target_point,best)

    return best