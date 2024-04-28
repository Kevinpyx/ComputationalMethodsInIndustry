import networkx as nx

# BFS
# DG: a directed graph
# s: start node
# t: target node
def BFS(DG, s, t): 
    q = [[s]]
    visited = [s]
    while (len(q) != 0) :
        path = q.pop(0)
        last = path[-1]
        if (last != t):
            for neighbor in DG.successors(last):
                if (neighbor in visited or DG[last][neighbor]['weight'] == 0):
                    pass
                else:
                    newpath = path.copy()
                    newpath.append(neighbor)
                    q.append(newpath)
                    visited.append(neighbor)
        else:
            return path
    return -1

# flow
# DG: weighted directed graph
def flow(DG, path):
    edge_weights = []
    for i in range(len(path)-1):
        edge_weights.append(DG[path[i]][path[i+1]]['weight'])
    return min(edge_weights)



def updateResidual(DG, path, flow):
    for i in range(len(path)-1):
        DG[path[i]][path[i+1]]['weight'] = DG[path[i]][path[i+1]]['weight'] - flow # reduce edge capacity in the direction
        DG[path[i+1]][path[i]]['weight'] = DG[path[i+1]][path[i]]['weight'] + flow # increase edge capacity in the other direction
       
def remerse(DG):
    for (u, v, isReversed) in DG.edges.data('isReversed'):
        if not(isReversed):
            DG[u][v]['weight'] = DG[v][u]['weight']
            DG.remove_edge(v,u)

def findMaxFlow(DG, s, t):
    original_edges = list(DG.edges)
    DG.add_edges_from(original_edges, isReversed = False)
    for (u, v) in original_edges:
        DG.add_edge(v, u, weight=0, isReversed = True)
    
    path = BFS(DG, s, t) 
    while(path != -1):
        flow_value = flow(DG, path)
        updateResidual(DG, path, flow_value)
        path = BFS(DG, s, t) 
    
    remerse(DG)
    flow_sum = 0
    for b in list(DG.successors(s)):
        flow_sum = flow_sum + DG[s][b]['weight']

    return flow_sum


DG = nx.DiGraph()
DG.add_nodes_from(['s', 'a', 'b', 'c', 'd', 't'])
DG.add_weighted_edges_from([('s','a', 5), 
                            ('a','b', 2), 
                            ('b','t', 3), 
                            ('a','d', 1), 
                            ('s','c', 4), 
                            ('c','d', 4), 
                            ('d','t', 9)])



classExample = nx.DiGraph()
classExample.add_nodes_from(['s', 'a', 'b', 'c', 'd', 'e', 't'])
classExample.add_weighted_edges_from([('s','a', 3), 
                            ('b','a', 10), 
                            ('b','d', 1), 
                            ('a','d', 2), 
                            ('s','c', 4), 
                            ('c','e', 5),
                            ('d','c', 1),
                            ('s','b', 3), 
                            ('d','t', 2),
                            ('d','e', 1),
                            ('e','t', 5)])

print(findMaxFlow(classExample, 's', 't'))
for (u, v, wt) in classExample.edges.data('weight'):
    print(f"({u}, {v}, {wt})")