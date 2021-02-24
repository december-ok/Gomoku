import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

axis_font = pygame.font.Font('arial.ttf',15)  #폰트 설정
normal_font = pygame.font.Font('arial.ttf',40) 

BLACK= ( 0,  0,  0)
WHITE= (255,255,255)
WOOD = (255, 172, 84)

# 90,90 시작
# 각 칸 크기 30 * 30 이 18개씩 해서 19&19 칸 나옴

#돌좌표 90,90

#각 칸의 상태
state = [ [0 for __ in range(0,19)] for _ in range(0,19)]
gui_point = [ [0 for __ in range(0,19)] for _ in range(0,19)]
for i in range(0,19):
  for j in range(0,19):
    gui_point[i][j] = (90+i*30, 90+j*30)

#초기설정
mouse_point = (0,0)
now_color = False # 0=black 1=white

def get_close_point(pt):
  x = (pt[0]-90)//30
  y = (pt[1]-90)//30
  candidate = [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
  dist = [99999999,99999999,99999999,99999999]
  for i in range(0,4):
    if candidate[i][0]>=0 and candidate[i][1]>=0 and candidate[i][0]<=18 and candidate[i][1]<=18:
      a = pt[0]-gui_point[candidate[i][0]][candidate[i][1]][0]
      b = pt[1]-gui_point[candidate[i][0]][candidate[i][1]][1]
      dist[i] = (a*a)+ (b*b)
  print(dist,dist.index(min(dist)),candidate)
  #0은 gui 1은 숫자칸
  return [gui_point[candidate[dist.index(min(dist))][0]][candidate[dist.index(min(dist))][1]], candidate[dist.index(min(dist))]]

while True: #게임 루프
  screen.fill(WOOD) #단색으로 채워 화면 지우기

  pygame.draw.rect(screen, BLACK, [90,90,540,540],2) # 바둑칸 둘레
  #가로세로 칸 그리기
  for i in range(0,18):
    for j in range(0,18):
      pygame.draw.rect(screen, BLACK, [90+j*30,90+i*30,30,30],1)
  # 축 표시
  for i in range(1,20):
    screen.blit(axis_font.render(str(i),True,BLACK), (60,50+i*30))
  for i in range(1,20):
    screen.blit(axis_font.render(chr(64+i),True,BLACK), (55+i*30,60))

  # 놓인 바둑돌 그리기
  for i in range(0,19):
    for j in range(0,19):
      if state[i][j]==1:
        pygame.draw.circle(screen, BLACK, gui_point[i][j],15)
      elif state[i][j]==2:
        pygame.draw.circle(screen, WHITE, gui_point[i][j],15)
      
  # 예상되는 바둑돌 그리기
  if mouse_point[0]>=75 and mouse_point[0]<=645 and mouse_point[1]>=75 and mouse_point[1]<=645:
    temp_point = get_close_point(mouse_point)
    if state[temp_point[1][0]][temp_point[1][1]]==0:
      if now_color:
        pygame.draw.circle(screen, WHITE, get_close_point(mouse_point)[0],15)
      else:
        pygame.draw.circle(screen, BLACK, get_close_point(mouse_point)[0],15)


  #변수 업데이트
  event = pygame.event.poll() #이벤트 처리
  if event.type == pygame.QUIT:
    break
  elif event.type == pygame.MOUSEBUTTONDOWN:#클릭시
    if mouse_point[0]>=75 and mouse_point[0]<=645 and mouse_point[1]>=75 and mouse_point[1]<=645:
      temp_point = get_close_point(mouse_point)
      if state[temp_point[1][0]][temp_point[1][1]]==0:
        if now_color:
          state[temp_point[1][0]][temp_point[1][1]]=2
        else:
          state[temp_point[1][0]][temp_point[1][1]]=1
        now_color = not now_color
  elif event.type == pygame.MOUSEMOTION:
    mouse_point = event.pos

  #화면 그리기

  pygame.display.update() #모든 화면 그리기 업데이트
  # clock.tick(60) #60 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값
  
pygame.quit()

