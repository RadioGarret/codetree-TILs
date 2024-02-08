N = int(input())
gMap = [[0] * N for _ in range(N)]
Dp = [[[0, 0] for _ in range(N)] for _ in range(N)]

for j in range(N):
    letter = list(map(int, input().split()))
    for i in range(N):
        gMap[j][i] = letter[i]
# 지나가는데 최댓값이 가장 작아야 하고, 
# 지나가는데 최솟값이 가장 커야 한다.

# 1번 조건은, 위 왼쪽 살폈을 때 가장 작은거 고르는데, 내가 그것보다 크면 어쩔 수 없이 내가 max값이 됨
# 2번 조건은, 위 왼쪽 살폈을 때 가장 큰거 고르는데, 내가 그것보다 작으면 어쩔 수 없이 내가 min 값이 됨

def MaxUpdate(y, x):
    left = Dp[y][x-1][0] if 0 <= x-1 else float('inf')
    up = Dp[y-1][x][0] if 0 <= y-1 else float('inf')
    
    if min(left, up) < gMap[y][x]:
        Dp[y][x][0] = gMap[y][x]
    else:
        Dp[y][x][0] = min(left, up)
# 2번 조건은, 위 왼쪽 살폈을 때 가장 큰거 고르는데, 내가 그것보다 작으면 어쩔 수 없이 내가 min 값이 됨
def MinUpdate(y, x):
    left = Dp[y][x-1][1] if 0 <= x-1 else 0
    up = Dp[y-1][x][1] if 0 <= y-1 else 0
    
    if max(left, up) > gMap[y][x]:
        Dp[y][x][1] = gMap[y][x]
    else:
        Dp[y][x][1] = max(left, up)

Dp[0][0][0], Dp[0][0][1] = gMap[0][0], gMap[0][0]

for j in range(N):
    for i in range(N):
        if (j == 0 and i == 0):
            continue
        MaxUpdate(j, i)
        MinUpdate(j, i)

print(abs(Dp[N-1][N-1][0] - Dp[N-1][N-1][1]))