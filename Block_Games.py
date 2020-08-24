import turtle as t
import random as r
import time
dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]

## 벽돌 클래스
class Brick():
    ## 벽돌을 생성하면 맨 위 가운데 위치하고, 색은 랜덤
    def __init__(self):
        self.y = 0
        self.x = 6
        self.color = r.randint(1,6)
    ## 왼쪽으로 이동
    def mov_left(self, grid):
        if grid[self.y][self.x-1] == 0 and grid[self.y+1][self.x-1]==0: # 왼쪽이 블럭이나 벽이 아니면
            grid[self.y][self.x]=0
            self.x-=1
    ## 오른쪽으로 이동
    def mov_right(self, grid):
        if grid[self.y][self.x+1] == 0 and grid[self.y+1][self.x+1]==0: # 오른쪽이 블럭이나 벽이 아니면
            grid[self.y][self.x]=0
            self.x+=1

"""중요"""
## grid 좌표에 해당하는 그림 그리기
def draw_grid(block, grid):
    block.clear()
    top = 250  # 원점에서 위로 250픽셀인 떨어진 위치를 top으로 정함
    left = -150  # 원점에서 왼쪽으로 150픽셀인 위치를 left로 정함
    # 0번 인덱스가 0, 7번 인덱스가 하얀색
    colors = ['black', 'red', 'blue', 'orange', 'yellow', 'green', 'purple', 'white']

    ## grid 배열의 좌표와, 값에 해당하는 블록을 스크린에 그리기
    for y in range(len(grid)):  # y가 세로
        for x in range(len(grid[0])):  # x가 가로
            sc_x = left + (x * 22)  # 네모하나는 20*20이므로 22로하면 약간 띄어서 생성
            sc_y = top - (y * 22)
            block.goto(sc_x, sc_y)  # grid 배열의 위치에 상응하는 격자위치에 사각형 생성
            if y==15 and grid[y][x] == 7: # 게임오버가 되는 지점 표시
                block.color("red") # 이때는 하얀색이 아닌 빨간색으로 표시
            else:
                block.color(colors[grid[y][x]])  # grid 배열의 값에 따라 네모의 색 변경
            block.stamp()  # 그 위치에 커서 찍음, 선긋기가 아니고

"""중요"""
## 인접한 벽돌 중 색이 같은 벽돌들의 좌표를 알아내기
def DFS(y, x, grid, color):
    global ch, blank
    ch[y][x] = 1
    blank.append((y,x))
    for i in range(4):
        yy = y + dy[i]
        xx = x + dx[i]
        if 0<yy<24 and 0<xx<13:
            if grid[yy][xx] == color and ch[yy][xx] == 0:
                DFS(yy, xx, grid, color)

## 위에서 부터 훑다가 벽돌 발견하면 그 행이 블럭의 최고놓이
def max_height(grid):
    for y in range(1, 24):
        for x in range(1,13):
            if grid[y][x] != 0:
                return y

"""중요"""
## 인접한 벽돌들을 모두 없애고, 그 위에 있던 벽돌들을 중력에 의해 내려오게 함
def grid_update(grid, blank):
    for y, x in blank:
        grid[y][x] = 0

    height = max_height(grid)
    for y in range(23, height, -1): # 아래서부터
        for x in range(1, 13): # 우측으로 훑으며
            if grid[y][x] == 0: # 0을 발견하면
                tmp_y =y
                ## 그 지점위로 0이 아닌 지점(블럭이 있는 지점)을 처음 발견할때까지 올라간다.
                while grid[tmp_y][x] == 0 and tmp_y>0:
                    tmp_y -= 1
                grid[y][x] = grid[tmp_y][x] #
                grid[tmp_y][x] = 0

def continual_remove():
    global blank, ch
    while True:
        flag = 1
        for y in range(23, 15, -1):
            for x in range(1, 13):
                if grid[y][x] != 0:
                    ch = [[0] * 14 for _ in range(25)]
                    blank = []
                    DFS(y, x, grid, grid[y][x])
                    if len(blank) >= 4:
                        grid_update(grid, blank)
                        flag=0
        if flag == 1:
            break


def game_over():
    pen.up()
    pen.goto(-120, 38)
    pen.write("GAME OVER", font=("courier", 32, 'bold'))

def you_win():
    pen.up()
    pen.goto(-120, 38)
    pen.write(" YOU WIN ", font=("courier", 32, 'bold'))

if __name__ == "__main__":
    ## 스크린의 객체로 창의 생성과 배경색과 크기 설정
    sc = t.Screen()
    sc.tracer(False) # 빨리 떨어지게 하기
    sc.bgcolor("black")
    sc.setup(width=600, height=700)

    ## 이차원 리스트로 게임정보가 들어있는 격자판을 표현
    ## 벽은 숫자 7, 하얀색으로 생성, 왼,오,아래에 생성
    ## 벽 생성후 격자는 14*25의 사이즈를 가지게 됨
    grid = [[0] * 12 for _ in range(24)]
    for i in range(24):
        grid[i].insert(0, 7)  # 왼쪽
        grid[i].append(7)  # 오른쪽
    grid.append([7] * 14)  # 아래

    ## 랜덤으로 아래에 3줄 채우기
    for y in range(23, 20, -1):
        for x in range(1,13):
            grid[y][x] = r.randint(1,6)


    ## 블록 만들기
    ## 터틀의 객체 클래스로 블록생성 및 초기 세팅
    ## 색, 모양, 속도
    ## 네모는 가로x세로 20x20 pixel이다.
    block = t.Turtle()
    block.penup()  # 펜을 들어올려 거북이가 움직일때 그림을 그리지 않게한다.
    block.speed(0)
    block.shape("square")
    block.color("red")
    block.setundobuffer(None) # 빠르게 떨어지게 하기

    ## 벽돌의 좌표에 그리드 배열에 넣고 그 값을 벽돌의 색으로 설정
    brick = Brick()
    grid[brick.y][brick.x] = brick.color
    draw_grid(block, grid)

    ## 게임 제목 그리기
    pen = t.Turtle()
    pen.ht() # 모양을 숨겨 나타나지 않게 함
    pen.goto(-80, 290)
    pen.color("white")
    pen.write("Block Game", font=("courier", 20, 'bold'))


    ## 왼쪽 오른쪽 키를 누르면 생성한 함수 작동
    ## 클래스의 메소드가 다른 함수의 함수인자로 들어가면 람다함수를써야한다.
    sc.onkeypress(lambda: brick.mov_left(grid), "Left")
    sc.onkeypress(lambda: brick.mov_right(grid), "Right")
    sc.listen()

    """중요"""
    ## 벽돌의  이동
    while True:
        sc.update() # 매번 스크린을 업데이트
        ## 벽돌이 떠있으면 중력작용으로 내려가기
        if grid[brick.y+1][brick.x] == 0:
            grid[brick.y][brick.x] = 0
            brick.y +=1
            grid[brick.y][brick.x] = brick.color
        ## 벽돌이 닿으면 멈추고 인접한 블록이 4개이면 grid_update
        else:
            ch =[[0]*14 for _ in range(25)]
            blank = []
            DFS(brick.y, brick.x, grid, brick.color)
            if len(blank) >= 4:
                grid_update(grid, blank)
                continual_remove()

            draw_grid(block, grid)
            ## 최고 높이가 제한선을 넓으면
            height = max_height(grid)
            if height <= 15:
                game_over()
                break
            ## 최고 높이를 두줄로 만들면
            elif height >= 22:
                you_win()
                break

            brick = Brick()


        #draw_grid(block, grid)
        time.sleep(0.01)  # 게임의 속도 조절








    sc.mainloop()  # 창이 꺼지지 않고 계속 켜져있게 함

    # Hello world!!!!!!!!!!
    # Hello github!!!!!!!!!
    
    # Nice to meet you thank you!!
