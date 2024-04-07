import copy

N, M, P, C, D = map(int, input().split())
gMap = [[0] * N for _ in range(N)]
Ryp, Rxp = map(int, input().split())
Ry, Rx = Ryp - 1, Rxp - 1
gMap[Ry][Rx] = 100 # 루돌프 위치는 100
for _ in range(P):
    num, yp, xp = map(int, input().split())
    gMap[yp-1][xp-1] = num
    
gSantaScore = [0 for _ in range(P + 1)]
gSantaStun = [0 for _ in range(P + 1)]
dx = [0, 1, 0, -1, 1, 1, -1, -1] # 0북1동2남3서, 4북동, 5남동, 6남서, 7북서
dy = [-1, 0, 1, 0, -1, 1, 1, -1]

# 거리함수
def Distance(y1, x1, y2, x2):
    result = (x1-x2) ** 2 + (y1 - y2) ** 2
    return result

def Opposite(dir):
    if dir == 0:
        dir = 2
    elif dir == 1:
        dir = 3
    elif dir == 2:
        dir = 0
    elif dir == 3:
        dir = 1
    elif dir == 4:
        dir = 6
    elif dir == 5:
        dir = 7
    elif dir == 6:
        dir = 4
    elif dir == 7:
        dir = 5
    return dir


def NoSanta(): # P명의 산타 모두 탈락 
    for j in range(N):
        for i in range(N):
            if gMap[j][i] != 0 and gMap[j][i] != 100:
                return False
    return True

def Interaction_after_Coll(Sy, Sx, nSy, nSx, dir, tMap): # 충돌후
    # 아무것도 없으면
    nowNum = tMap[Sy][Sx]
    nextNum = tMap[nSy][nSx]

    # S nS nnS
    if nowNum == nextNum: # 한칸만 이동하는 경우.... 좀 이런거 어떻게 생각하냐..
        return 

    if tMap[nSy][nSx] == 0: # 이로써 끝. 
        tMap[nSy][nSx] = nowNum
        tMap[Sy][Sx] = 0 # 이거때문에 루돌프 위치 없애져버리는거 주의

    # 산타가 있으면 DFS
    elif tMap[nSy][nSx] != 0:
        nnSy, nnSx = nSy + dy[dir], nSx + dx[dir]
        if 0 <= nnSy < N and 0 <= nnSx < N:
            Interaction_after_Coll(nSy, nSx, nnSy, nnSx, dir, tMap)
        else: # 튕겨져 나간경우
            gSantaStun[nextNum] = 99999999
        tMap[nSy][nSx] = nowNum
        tMap[Sy][Sx] = 0

# 루돌프 
# 산타 찾고, 1칸 돌진 / 게임 탈락 안한놈
# 활성화, 스턴되어있는 산타. 둘다 박을 수 있음. --> 모든 산타. 
# 거리, r, c순서
# 8방향 
# 산타 기절상태 만들기 - 다음턴까지만 기절시켜야함. Stun배열 : 2를 충전하고, 매 턴당 Stun배열 -1씩
def RudolfMove():
    global Rx, Ry, N, C, D

    # 가장 가까운 산타 찾기 
    list_dist = []
    for j in range(N):
        for i in range(N):
            if gMap[j][i] != 0 and gMap[j][i] != 100:
                list_dist.append((Distance(Ry, Rx, j, i), j, i))

    if len(list_dist) != 0:
        list_dist.sort(key = lambda x : (x[0], -x[1], -x[2]))
        Sy, Sx = list_dist[0][1], list_dist[0][2]
        numSanta = gMap[Sy][Sx]

        # 루돌프가 이동할 자리 찾기(산타랑 가장 가까운 위치)
        list_dist = []
        for k in range(8):
            nRy, nRx = Ry + dy[k], Rx + dx[k]
            if 0 <= nRy < N and 0 <= nRx < N:
                list_dist.append((Distance(nRy, nRx, Sy, Sx), nRy, nRx, k))
        list_dist.sort(key = lambda x : x[0])
        nRy, nRx, ndir = list_dist[0][1], list_dist[0][2], list_dist[0][3]

        # 박치기하는경우
        if nRy == Sy and nRx == Sx:
            nSy, nSx = Sy + C * dy[ndir], Sx + C * dx[ndir]
            if 0 <= nSy < N and 0 <= nSx < N:
                gSantaStun[numSanta] = 2
                Interaction_after_Coll(Sy, Sx, nSy, nSx, ndir, gMap)
            else: # 튕겨져 나가버린경우
                gSantaStun[numSanta] = 999999999
            gSantaScore[numSanta] += C 
            gMap[Sy][Sx] = 0

        # 루돌프 위치 바꾸기
        gMap[Ry][Rx], gMap[nRy][nRx] = 0, gMap[Ry][Rx]
        Ry, Rx = nRy, nRx
            

# 산타 : 순서대로 움직이기, 기절은 못움직임
# 다른산타 있으면 못움직임.  
# 못움직이면 안움직임. --> #########반례 : 산타들에 둘러쌓여있는 경우. 
# 4방향
# 움직일 수 있는 칸 있더라도 가까워질 방법 없으면 안감 : ### 4방향 탐색하는데, 거리 최소인곳으로만 가야함!!
# 밀려난칸 다른산타 : 상호작용
def SantaMove():
    global Ry, Rx, gMap
    tMap = copy.deepcopy(gMap)
    for numSanta in range(1, P + 1):

        if gSantaStun[numSanta] == 0: # 스턴안걸린산타

            # 맵서칭
            for j in range(N):
                for i in range(N):
                    if gMap[j][i] == numSanta:
                        list_dist = []
                        now_dist = Distance(Ry, Rx, j, i)
                        for k in range(4):
                            ny, nx = j + dy[k], i + dx[k]
                            
                            if 0 <= ny < N and 0 <= nx < N and (tMap[ny][nx] == 0 or tMap[ny][nx] == 100):
                                dist = Distance(Ry, Rx, ny, nx)
                                # min_dist = min(dist, min_dist)  #### 이게 아니라, 움직이는 곳이 기존 거리보다 작아지면 list에 넣으면 되는거다.
                                if dist < now_dist:
                                    list_dist.append((Distance(Ry, Rx, ny, nx), ny, nx, k))

                        if len(list_dist) != 0: 
                            list_dist.sort(key = lambda x : (x[0], x[3])) # 상우하좌 우선순위
                            nSy, nSx, dir = list_dist[0][1], list_dist[0][2], list_dist[0][3]
                            
                            # 루돌프 부딪히는경우
                            if nSy == Ry and nSx == Rx:
                                ndir = Opposite(dir)
                                nnSy, nnSx = j + (D-1) * dy[ndir], i + (D-1) * dx[ndir]
                                if 0 <= nnSy < N and 0 <= nnSx < N:
                                    gSantaStun[numSanta] = 2
                                    Interaction_after_Coll(j, i, nnSy, nnSx, ndir, tMap) # 이렇게 해야 루돌프 위치 안바뀜. 
                                
                                else: # 튕겨져 나가버린경우
                                    gSantaStun[numSanta] = 999999999
                                    tMap[j][i] = 0
                                gSantaScore[numSanta] += D

                            else:
                                tMap[nSy][nSx] = tMap[j][i]
                                tMap[j][i] = 0
    gMap = tMap

# M개의 턴 다 돌면 끝나야함. 
# 턴당 Stun배열 -1씩. 
# 턴 끝당 산타 + 1점씩
for cnt in range(M):
    
    if NoSanta():
        break
    RudolfMove()
    SantaMove()

    for i in range(1, (P+1)):
        if gSantaStun[i] != 0:
            gSantaStun[i] -= 1
    for i in range(1, (P+1)):
        if gSantaStun[i] < 10:
            gSantaScore[i] += 1

for i in range(1, (P+1)):
    print(gSantaScore[i], end = ' ')