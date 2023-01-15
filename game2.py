import pygame
import random

#initialize the game
pygame.init()

#Game Board Size
size = [600,1000]
boardHalfX = size[0] / 2
boardHalfY = size[1] / 2
boardX = size[0] 
boardY = size[1] 
borderMargin = 5
gameFramePerSecond = 60
screen = pygame.display.set_mode(size)

title = "Space Battle 1.0"
pygame.display.set_caption(title)

#3. game setting
clock = pygame.time.Clock()
black = (0,0,0)
white = (255,255,255)
secondCounter = 0
frameCounter = 0

class obj:
    def __init__(self, speed):
        self.positionX = 0
        self.positionY = 0
        self.speed = speed
        self.sizeX = 0
        self.sizeY = 0
        self.sizeHalfX = 0
        self.sizeHalfY = 0
    def load_img(self,imgName):
        if imgName[-3:] == "png":
            self.img = pygame.image.load(imgName).convert_alpha()
        else:
            self.img = pygame.image.load(imgName)
    def change_size(self, sizeX, sizeY):
        self.img = pygame.transform.scale(self.img, (sizeX, sizeY))
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeHalfX = sizeX/2
        self.sizeHalfY = sizeY/2
    def change_positionX(self, positionX):
        self.positionX = positionX
    def change_positionY(self, positionY):
        self.positionY = positionY
    def change_position(self, positionX, positionY):
        self.positionX = positionX
        self.positionY = positionY
    def get_Left(self):
        return self.positionX
    def get_Right(self):
        return self.positionX + self.sizeX
    def get_Up(self):
        return self.positionY
    def get_Down(self):
        return self.positionY + self.sizeY
    def show(self):
        screen.blit(self.img, (self.positionX, self.positionY))

class spaceship(obj):
    def __init__(self, sizeX, sizeY, speed):
        super().__init__(sizeX, sizeY, speed)

class ourship(spaceship):
    def __init__(self, sizeX, sizeY, speed):
        super().__init__(sizeX, sizeY, speed)

class enemyship(spaceship):
    def __init__(self, sizeX, sizeY, speed):
        super().__init__(sizeX, sizeY, speed)

class weapon(obj):
    def __init__(self, sizeX, sizeY, speed):
        super().__init__(sizeX, sizeY, speed)

class addon(obj):
    def __init__(self, sizeX, sizeY, speed):
        super().__init__(sizeX, sizeY, speed)

def bulletCollide(bullet,enemy):
    if(bullet.get_Left() >= enemy.get_Left() and bullet.get_Right() <= enemy.get_Right()):
        if(bullet.get_Up() <= enemy.get_Down()):
            return True
    return False

def collide(a, b):
    if(a.get_Left() == b.get_Right() or a.get_Right() == b.get_Left()):
        if(a.get_Up() == b.get_Down() or a.get_Down() == b.get_Up()):
            return True
    return False

# Initilization Parameter
# (self, sizeX, sizeY, speed):
myship = obj(5)
myship.load_img("img/spaceship4.png")
myship.change_size(60,60)
myship.change_position(round(boardHalfX)-myship.sizeHalfX,boardY - myship.sizeY - borderMargin)

#Boolean for movement
move_left = False
move_right= False
move_up = False
move_down = False
move_mybullet = False
move_enemybullet = False

mybullet_list = []
enemybullet_list = []
enemyUnit_list = []

#4. main event
SB = 0
while SB == 0:

    #4-1 FPS setting
    clock.tick(gameFramePerSecond)
    # 60 frames in 1 second

    #4-2 event detection
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
            elif event.key == pygame.K_SPACE:
                move_mybullet = True
                frameCounter=0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False
            elif event.key == pygame.K_SPACE:
                move_mybullet = False
    #4-3 move
    if move_left == True:
        myship.change_positionX(myship.positionX - myship.speed)
        if(myship.positionX <= 0 + borderMargin):
            myship.positionX = borderMargin
    elif move_right == True:
        myship.change_positionX(myship.positionX + myship.speed)
        #myship.positionX += myship.speed
        if(myship.positionX + myship.sizeX >= boardX - borderMargin):
            myship.positionX = boardX - borderMargin - myship.sizeX 
    elif move_up == True:
        myship.change_positionY(myship.positionY - myship.speed)
        if(myship.positionY <= 0 + borderMargin):
            myship.positionY = borderMargin
    elif move_down == True:
        myship.change_positionY(myship.positionY + myship.speed)
        if(myship.positionY + myship.sizeY >= boardY - borderMargin):
            myship.positionY = boardY - borderMargin - myship.sizeY
    
    #mybullet movement
    if move_mybullet == True and frameCounter % 6 == 0:
        mybullet = obj(15)
        mybullet.load_img("img/bullet1.png")
        mybullet.change_size(2,6)
        mybullet.change_position(myship.positionX + myship.sizeHalfX - mybullet.sizeHalfX, myship.positionY - mybullet.sizeY - 10)
        mybullet_list.append(mybullet)
    
    #increment frameCounter
    frameCounter += 1

    removeBullet_list = []
    removeEnemy_list = []

    for i in range(len(mybullet_list)):
        bullet = mybullet_list[i]
        bullet.change_positionY(bullet.positionY - bullet.speed)
        #delete the bullet that is out of the game board to save memory
        if bullet.positionY <= -bullet.sizeY:
            removeBullet_list.append(i)
    removeBullet_list.reverse()
    for d in removeBullet_list:
        del mybullet_list[d]
    

    if random.random() > 0.98:
        enemy = obj(1)
        if random.random() > 0.50:
            enemy.load_img("img/enemy1.png")
        else:
            enemy.load_img("img/enemy2.png")
        enemy.change_size(40,40)
        enemy.positionX = random.randrange(0, boardX - enemy.sizeX-round(myship.sizeX/2))
        enemyUnit_list.append(enemy)
        removeEnemy_list = []
    for i in range(len(enemyUnit_list)):
        sampleEnemy = enemyUnit_list[i]
        sampleEnemy.change_positionY(sampleEnemy.positionY + sampleEnemy.speed)
        if sampleEnemy.positionY >= boardY:
            removeEnemy_list.append(i)
    removeEnemy_list.reverse()
    for enemyToRemove in removeEnemy_list:
        del enemyUnit_list[enemyToRemove]


    removeBullet_list = []
    removeEnemy_list = []
    for i in range(len(mybullet_list)):
        for j in range(len(enemyUnit_list)):
            m = mybullet_list[i]
            a = enemyUnit_list[j]
            if bulletCollide(m,a) == True:
                print("Hello World")
                removeBullet_list.append(i)
                removeEnemy_list.append(j)
    removeBullet_list = list(set(removeBullet_list))
    removeEnemy_list = list(set(removeEnemy_list))
    removeBullet_list.reverse()
    removeEnemy_list.reverse()
    try:
        for bullet in removeBullet_list:
            del mybullet_list[bullet]
        for enemy in removeEnemy_list:
            del enemyUnit_list[enemy]
    except:
        pass

     #4-4 draw
    screen.fill(black)
    myship.show()
    for m in mybullet_list:
        m.show()
    for e in enemyUnit_list:
        e.show()
    print(myship.get_Left())
    #4-5 update
    pygame.display.flip()

#5 end 
pygame.QUIT       






