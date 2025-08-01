n = 4

routers = ['A', 'B', 'C', 'D']

INF = 999

graph = [
    [0,   1,   3, INF],   # A
    [1,   0,   1,   4],   # B
    [3,   1,   0,   1],   # C
    [INF, 4,   1,   0]    # D
]

distance = [row[:] for row in graph]  # Deep copy of graph
next_hop = [[j if graph[i][j] != INF else -1 for j in range(n)] for i in range(n)]

def run_dvr():
    updated = True
    while updated:
        updated = False
        for i in range(n):  # For each router i
            for j in range(n):  # For each destination j
                for k in range(n):  # For each neighbor k
                    if distance[i][j] > distance[i][k] + distance[k][j]:
                        distance[i][j] = distance[i][k] + distance[k][j]
                        next_hop[i][j] = k
                        updated = True

run_dvr()

for i in range(n):
    print(f"\nRouting Table for Router {routers[i]}:")
    print("Destination\tCost\tNext Hop")
    for j in range(n):
        if i == j:
            continue
        cost = distance[i][j]
        nhop = next_hop[i][j]
        nhop_name = routers[nhop] if nhop != -1 else "None"
        print(f"{routers[j]}\t\t{cost}\t{nhop_name}")
