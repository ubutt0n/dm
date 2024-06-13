from collections import deque

def main(input):
    visited = set()
    count = 0
    
    def bfs(x, y):
        queue = deque([(x, y)])
        visited.add((x, y))
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x_1, y_1 = queue.pop()
            for dx, dy in directions:
                new_x, new_y = x_1 + dx, y_1 + dy
                if 0 <= new_x < len(input) and 0 <= new_y < len(input[0]) and (new_x, new_y) not in visited and input[new_x][new_y] == 0:
                    queue.append((new_x, new_y))
                    visited.add((new_x, new_y))
    
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == 0 and (i == 0 or j == 0 or i == len(input) - 1 or j == len(input[0]) - 1):
                bfs(i, j)
    
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == 0 and (i, j) not in visited:
                count += 1
                bfs(i, j)
    
    return count

rows = int(input("Количество строк: "))
cols = int(input("Количество столбцов: "))

input_matrix = []
for _ in range(rows):
    row = input()
    if len(row.split(" ")) == cols:
        input_matrix.append([int(i) for i in row.split(" ")])
    else:
        print("Количество столбцов не соотвествует заданному")

print(f'Количество островов: {main(input_matrix)}')