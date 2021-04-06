import pygame
import sys
import random


class Bird(object):

    #初始化小鸟的状态
    def __init__(self):

        self.birdRect = pygame.Rect(65, 50, 40, 40)
        self.birdStatus = [pygame.image.load("pictures/0.png"),       #初始状态
                           pygame.image.load("pictures/1.png"),       #飞行状态
                           pygame.image.load("pictures/dead.png")]    #失败状态
        self.status = 0
        self.birdX = 120
        self.birdY = 350
        self.jump = False
        self.jumpSpeed = 10
        self.gravity = 1
        self.dead = False

    #模拟小鸟飞行的动作
    def birdUpdate(self):
        #上升
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
        #下降
        else:
            self.gravity += 0.1
            self.birdY += self.gravity

        self.birdRect[1] = self.birdY


class Pipeline(object):

    def __init__(self):
        self.wallx = 400
        self.pineUp = pygame.image.load("pictures/top.png")
        self.pineDown = pygame.image.load("pictures/bottom.png")

    #小鸟飞行时管道相对向左移动，模拟管道移动
    def updatePipeline(self):

        self.wallx -= 5
        #小鸟飞越管道之后加一分
        if self.wallx < -80:
            global score
            score += 1
            self.wallx = 400
            #飞越之后随机设置下一次出现的管道的长度
            global num
            num = random.randint(0,200)

#地图保持更新
def createMap():

    #背景
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    #管道
    #screen.blit(Pipeline.pineUp, (Pipeline.wallx, -300 - randnum))   # 上管道坐标位置
    #screen.blit(Pipeline.pineDown, (Pipeline.wallx, 300 + randnum))  # 下管道坐标位置
    screen.blit(Pipeline.pineUp, (Pipeline.wallx, -450 + num ))  #上管道坐标位置
    screen.blit(Pipeline.pineDown, (Pipeline.wallx, 550 - num))  #下管道坐标位置

    #移动管道
    Pipeline.updatePipeline()

    #小鸟
    #小鸟碰撞到管道或飞出界面区域
    if Bird.dead:
        Bird.status = 2
    #振翅
    elif Bird.jump:
        Bird.status = 1

    #更新小鸟的状态
    screen.blit(Bird.birdStatus[Bird.status], (Bird.birdX, Bird.birdY))
    Bird.birdUpdate()

    #记录得分
    screen.blit(font.render('Score:' + str(score), -1, (255, 255, 255)), (100, 50))
    pygame.display.update()


def checkDead():
    #上方管道
    upRect = pygame.Rect(Pipeline.wallx, -450 + num,
                         Pipeline.pineUp.get_width(),
                         Pipeline.pineUp.get_height())

    #下方管道
    downRect = pygame.Rect(Pipeline.wallx, 550 - num,
                           Pipeline.pineDown.get_width(),
                           Pipeline.pineDown.get_height())

    #检测小鸟与管道是否发生碰撞
    if upRect.colliderect(Bird.birdRect) or downRect.colliderect(Bird.birdRect):
        Bird.dead = True
        #Bird.status = 2
        #return True
    #检测小鸟是否飞出界面区域（上下界）
    if not 0 < Bird.birdRect[1] < height:
        Bird.dead = True
        '''
        Bird.status = 2
        screen.blit(Bird.birdStatus[Bird.status], (Bird.birdX, Bird.birdY))
        Bird.birdUpdate()
        '''
        return True
    else:
        return False


def getResutl():
    final_text1 = "Game Over"
    final_text2 = "Your final score is:  " + str(score)
    ft1_font = pygame.font.SysFont("Arial", 70)
    ft1_surf = font.render(final_text1, 1, (242, 3, 36))
    ft2_font = pygame.font.SysFont("Arial", 50)
    ft2_surf = font.render(final_text2, 1, (253, 177, 6))
    screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])
    screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 200])
    pygame.display.flip()


if __name__ == '__main__':
    """主程序"""
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("ziti.ttf", 50)
    size = width, height = 400, 650
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    Pipeline = Pipeline()
    Bird = Bird()
    score = 0
    num = 0
    while True:
        #每秒30次
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #用鼠标或键盘控制小鸟振翅
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not Bird.dead:
                Bird.jump = True
                Bird.gravity = 1
                Bird.jumpSpeed = 10

        background = pygame.image.load("pictures/background.png")

        #若小鸟死亡，结束游戏，显示得分
        if checkDead():
            getResutl()
        else:
            createMap()
    pygame.quit()

