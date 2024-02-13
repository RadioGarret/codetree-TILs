N = int(input())
max_number = 100
gMap = [[float('inf')] * N for _ in range(N)]

for j in range(N):
    letter = list(map(int, input().split()))
    for i in range(N):
        gMap[j][i] = letter[i]
# 지나가는데 최댓값이 가장 작아야 하고, 
# 지나가는데 최솟값이 가장 커야 한다.

# 1번 조건은, 위 왼쪽 살폈을 때 가장 작은거 고르는데, 내가 그것보다 크면 어쩔 수 없이 내가 max값이 됨
# 2번 조건은, 위 왼쪽 살폈을 때 가장 큰거 고르는데, 내가 그것보다 작으면 어쩔 수 없이 내가 min 값이 됨
# --> 이런방식으로 하면 1번조건과 2번조건 만족하는 루트가 다르다. 그래서 이러면 안되고, 최솟값을 정해서, 
# 그 최솟값 이하의 숫자로는 지나가지 않도록 하는 방향으로 코딩하자. 

# def MaxUpdate(y, x, Dp): # 이렇게 짜면 안되는게, 막히는 길 지나서는 그대로 또 된다...
#     left = Dp[y][x-1] if 0 <= x-1 else float('inf')
#     up = Dp[y-1][x] if 0 <= y-1 else float('inf')
    
#     if min(left, up) < gMap[y][x] or (left == float('inf') and up == float('inf')):
#         Dp[y][x] = gMap[y][x]
#     else:
#         Dp[y][x] = min(left, up)

def MaxUpdate(y, x, Dp): # 이렇게 짜면 안되는게, 막히는 길 지나서는 그대로 또 된다...
    left = Dp[y][x-1] if 0 <= x-1 else float('inf')
    up = Dp[y-1][x] if 0 <= y-1 else float('inf')
    
    if min(left, up) < gMap[y][x]:
        Dp[y][x] = gMap[y][x]
    else:
        Dp[y][x] = min(left, up)
    if (left == float('inf') and up == float('inf')): # 근데 이거 안해도 되지 않나. 어찻피 둘다 inf면 작은게 inf지
        Dp[y][x] = float('inf')
    

ans = float('inf')

for lower_bound in range(1, max_number + 1):
    Dp = [[float('inf')] * N for _ in range(N)]
    Dp[0][0] = gMap[0][0]
                
    for j in range(N):
        for i in range(N):
            if j == 0 and i == 0: # 첫번째 그냥 지나가
                continue
            if gMap[j][i] < lower_bound:
                Dp[j][i] = float('inf') # 못가는 길은 inf로 만들어라. 
                continue
            MaxUpdate(j, i, Dp)
    upper_bound = Dp[N-1][N-1]
    if upper_bound == float('inf'): # 결국 갈 수 있는 길이 없다.
        continue
    ans = min(ans, upper_bound - lower_bound)
print(ans)