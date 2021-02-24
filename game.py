import pygame
from pygame.locals import *


BLACK= ( 0,  0,  0)
WHITE= (255,255,255)
WOOD = (255, 172, 84)

class Gomoku:
  def __init__(self):
    pygame.init()
    self.axis_font = pygame.font.Font('arial.ttf',15)  #폰트 설정
    self.normal_font = pygame.font.Font('arial.ttf',40) 
    self.screen = pygame.display.set_mode((1280, 720))
    self.clock = pygame.time.Clock()


    # 90,90 시작
    # 각 칸 크기 30 * 30 이 18개씩 해서 19&19 칸 나옴

    #돌좌표 90,90

    #각 칸의 상태
    self.state = [ [0 for __ in range(0,19)] for _ in range(0,19)]
    self.gui_point = [ [0 for __ in range(0,19)] for _ in range(0,19)]
    for i in range(0,19):
      for j in range(0,19):
        self.gui_point[i][j] = (90+i*30, 90+j*30)

    #초기설정
    self.mouse_point = (0,0)
    self.now_color = False # 0=black 1=white

  def get_close_point(self, pt):
    x = (pt[0]-90)//30
    y = (pt[1]-90)//30
    candidate = [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
    dist = [99999999,99999999,99999999,99999999]
    for i in range(0,4):
      if candidate[i][0]>=0 and candidate[i][1]>=0 and candidate[i][0]<=18 and candidate[i][1]<=18:
        a = pt[0]-self.gui_point[candidate[i][0]][candidate[i][1]][0]
        b = pt[1]-self.gui_point[candidate[i][0]][candidate[i][1]][1]
        dist[i] = (a*a)+ (b*b)
    # print(dist,dist.index(min(dist)),candidate)
    #0은 gui 1은 숫자칸
    return [self.gui_point[candidate[dist.index(min(dist))][0]][candidate[dist.index(min(dist))][1]], candidate[dist.index(min(dist))]]

  def put_stone(self,temp_point):
    if self.now_color:
      self.state[temp_point[1][0]][temp_point[1][1]]=2
    else:
      self.state[temp_point[1][0]][temp_point[1][1]]=1
    self.now_color = not self.now_color

  def play_step(self):
    self.screen.fill(WOOD) #단색으로 채워 화면 지우기

    pygame.draw.rect(self.screen, BLACK, [90,90,540,540],2) # 바둑칸 둘레
    #가로세로 칸 그리기
    for i in range(0,18):
      for j in range(0,18):
        pygame.draw.rect(self.screen, BLACK, [90+j*30,90+i*30,30,30],1)
    # 화점
    pygame.draw.circle(self.screen, BLACK, (180,180),4)
    pygame.draw.circle(self.screen, BLACK, (360,180),4)
    pygame.draw.circle(self.screen, BLACK, (540,180),4)
    pygame.draw.circle(self.screen, BLACK, (180,360),4)
    pygame.draw.circle(self.screen, BLACK, (360,360),4)
    pygame.draw.circle(self.screen, BLACK, (540,360),4)
    pygame.draw.circle(self.screen, BLACK, (180,540),4)
    pygame.draw.circle(self.screen, BLACK, (360,540),4)
    pygame.draw.circle(self.screen, BLACK, (540,540),4)
    # 축 표시
    for i in range(1,20):
      self.screen.blit(self.axis_font.render(str(i),True,BLACK), (60,50+i*30))
    for i in range(1,20):
      self.screen.blit(self.axis_font.render(chr(64+i),True,BLACK), (55+i*30,60))

    # 놓인 바둑돌 그리기
    for i in range(0,19):
      for j in range(0,19):
        if self.state[i][j]==1:
          pygame.draw.circle(self.screen, BLACK, self.gui_point[i][j],15)
        elif self.state[i][j]==2:
          pygame.draw.circle(self.screen, WHITE, self.gui_point[i][j],15)
        
    # 예상되는 바둑돌 그리기
    if self.mouse_point[0]>=75 and self.mouse_point[0]<=645 and self.mouse_point[1]>=75 and self.mouse_point[1]<=645:
      temp_point = self.get_close_point(self.mouse_point)
      if self.state[temp_point[1][0]][temp_point[1][1]]==0:
        if self.now_color:
          pygame.draw.circle(self.screen, WHITE, self.get_close_point(self.mouse_point)[0],15)
        else:
          pygame.draw.circle(self.screen, BLACK, self.get_close_point(self.mouse_point)[0],15)

    # 글자들
    if self.now_color:
      self.screen.blit(self.normal_font.render('White Turn',True,BLACK), (0,0))
    else:
      self.screen.blit(self.normal_font.render('Black Turn',True,BLACK), (0,0))


    #본격적 진행
    event = pygame.event.poll() #이벤트 처리
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
    #착수
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if self.mouse_point[0]>=75 and self.mouse_point[0]<=645 and self.mouse_point[1]>=75 and self.mouse_point[1]<=645:
        temp_point = self.get_close_point(self.mouse_point)
        if self.state[temp_point[1][0]][temp_point[1][1]]==0:
          self.put_stone(temp_point)
          #5줄 완성되는지 확인

    #돌 두기전에
    elif event.type == pygame.MOUSEMOTION:
      self.mouse_point = event.pos

    #화면 그리기

    pygame.display.update() #모든 화면 그리기 업데이트
    # clock.tick(60) #60 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값
    

if __name__ == '__main__':
  game = Gomoku()
  
  while True:
    game.play_step()