def main(graph):
    visited = set()
    packages_in_right_order = []

    def dfs(package):
        if package not in visited:
            visited.add(package)
            for neighbor in graph[package]:
                dfs(neighbor)
            packages_in_right_order.append(package)
    
    for node in graph:
        dfs(node)
    print(packages_in_right_order)


n = int(input("Количество пакетов: "))
arr = []
for i in range(n):
    arr.append(input())

keys = [i.split(" ")[0].replace("'", "") for i in arr]
dependencies = [i.replace("'", "").split("(")[1].split(")")[0].split(", ") for i in arr]
for i in range(len(dependencies)):
    if not dependencies[i][0]:
        dependencies[i] = []
graph = dict(zip(keys, dependencies))

main(graph)