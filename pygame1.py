import pygame, random, sys

pygame.init()

screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Flappy Square")

WHITE = pygame.Color(255,255,255)
BLACK = pygame.Color(0,0,0)
RED   = pygame.Color(255,0,0)
SPEED = 0.5

ADDBLOCK = pygame.USEREVENT + 1

pygame.time.set_timer(ADDBLOCK, 1000)

SCORE = 0

font = pygame.font.Font("freesansbold.ttf", 32)


class square:
        def __init__(self, x, y):
                self.x = x
                self.y = y
                self.w = 10
                self.h = 10
                self.up = False
        description = "This is a square"
        author = "Shems Eddine"
        def draw(self, screen):
                pygame.draw.rect(screen, RED, (self.x, self.y, self.w, self.h))
        def move(self):
                self.moveUp()
                self.gravity()
        def moveUp(self):
                if(self.up):
                    self.y = self.y - 1
                else:
                    self.up = False
                    
        def jump(self):
                self.up = True
        def gravity(self):
                if(not self.up and self.y <= 235):
                    self.y = self.y +(9.8*0.1)
                else:
                    self.up = False

class block:
    def __init__(self, x):
        self.w = random.randint(10,25)
        self.h = random.randint(10,70)
        self.x = x
        self.y = 245 - self.h
        self.done = False
    def draw(self, screen):
        if(self.x < 320 and not self.done):
            global SCORE
            SCORE = SCORE + 1
            self.done = True
        pygame.draw.rect(screen, BLACK, (self.x,self.y, self.w, self.h))
        pygame.draw.rect(screen, BLACK, (self.x, 0, self.w, self.y - 100))
    def move(self):
        self.x = self.x - SPEED
    def collision(self, ob1):    
        if(ob1.x >= self.x+self.w):
            return False
        if(self.x >= ob1.x+ob1.w):
            return False
        if(ob1.y >= self.y+self.h or 0 >= ob1.y+ob1.h):
            return False
        if(self.y >= ob1.y+ob1.h and ob1.y >= self.y-100):
            return False
        return True



player = square(315,235)
bl = [block(640)]

RUNNING = True
    
while True: 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == ADDBLOCK:
            bl.append(block(640))


    keystate = pygame.key.get_pressed()

    if keystate[pygame.K_SPACE]:
        player.jump()

    if keystate[pygame.K_r]:
        bl = [block(640)]
        player = square(315,235)
        pygame.time.set_timer(ADDBLOCK, 1000)
        RUNNING = True

    if(RUNNING):
        player.move()
        for x in bl:
            if(x.collision(player)):
                RUNNING = False
            x.move()
            if(x.x < 0):
                bl.remove(x)
            


        message = font.render("Score: "+str(SCORE), False, RED)
            
        rect = message.get_rect()
        rect.topleft = (260,300)

    else:
        message = font.render("Game Over! Score: " + str(SCORE), False, RED)
            
        rect = message.get_rect()
        rect.topleft = (170,300)

    
    screen.fill(WHITE)   
    player.draw(screen)
    pygame.draw.line(screen, BLACK, (0,245), (640, 245), 1)
    for x in bl:
        x.draw(screen)
        
    screen.blit(message, rect)

    pygame.display.update()
