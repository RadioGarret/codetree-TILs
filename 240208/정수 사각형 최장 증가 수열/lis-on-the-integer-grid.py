N = int(input())
gMap = [[0] * N for _ in range(N)]
numbers = []
Dp = [[1] * N for _ in range(N)]
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

for j in range(N):
    letter = list(map(int, input().split()))
    for i in range(N):
        gMap[j][i] = letter[i]
        numbers.append((j, i))

def DpUpdate(y, x):
    # 상하좌우에 움직일곳이 있으면, dp값에 +1을 한다. 
    for k in range(4):
        nx = x + dx[k]
        ny = y + dy[k]
        if 0 <= nx < N and 0 <= ny < N and gMap[y][x] < gMap[ny][nx]:
            Dp[ny][nx] = max(Dp[ny][nx], Dp[y][x] + 1)
            


numbers = sorted(numbers, key = lambda x: gMap[x[0]][x[1]])


for y, x in numbers:
    DpUpdate(y, x)

max_value = 0
for j in range(N):
    for i in range(N):
        max_value = max(max_value, Dp[j][i])

print(max_value)