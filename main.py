from pygame.locals import *
import pygame
import sys

pygame.init()

clock = pygame.time.Clock()
MAX_FPS = 60

screen_width, screen_height = 1200,700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Idiots")


def fps_display():
    fps = clock.get_fps()
    fps_font = pygame.font.SysFont('arial', 25)
    fps_text = fps_font.render(f"{int(fps)}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))


# player 1 settings
player1_rect = pygame.Rect(250,250, 100,100)
player1_speed = 7
# player1_img = pygame.image.load("Images/")

# player 2 settings
player2_rect = pygame.Rect(750,250, 100,100)
player2_speed = 7
# player2_img = pygame.image.load("Images/")

class Players:

    def updatePlayer1(self, key):
        global player1_rect, player2_rect, player1_speed
        
        # draw rect (if needed)
        pygame.draw.rect(screen, (0, 0, 0), player1_rect)

        # movement
        if key[pygame.K_a]:
            if player1_rect.x > 0:
                player1_rect.x -= player1_speed
        if key[pygame.K_d]:
            if player1_rect.x < (screen_width-100):
                player1_rect.x += player1_speed

        if key[pygame.K_w]:
            if player1_rect.y > 0:
                player1_rect.y -= player1_speed
        if key[pygame.K_s]:
            if player1_rect.y < (screen_height-100):
                player1_rect.y += player1_speed

    def updatePlayer2(self, key):
        global player1_rect, player2_rect, player2_speed

        # draw rect (if needed)
        pygame.draw.rect(screen, (255, 0, 0), player2_rect)

        if key[pygame.K_LEFT]:
            if player2_rect.x > 0:
                player2_rect.x -= player2_speed
        if key[pygame.K_RIGHT]:
            if player2_rect.x < (screen_width - 100):
                player2_rect.x += player2_speed

        if key[pygame.K_UP]:
            if player2_rect.y > 0:
                player2_rect.y -= player2_speed
        if key[pygame.K_DOWN]:
            if player2_rect.y < (screen_height - 100):
                player2_rect.y += player2_speed

players = Players()

button_color = (255,0,0)
button_pressed = False
def button(x,y):
    global button_color, button_pressed

    button_rect = pygame.Rect(x,y,50,50)
    pygame.draw.rect(screen, (button_color), button_rect)

    # player collision
    if player1_rect.colliderect(button_rect) or player2_rect.colliderect(button_rect):
        button_pressed = True
        button_color = (0, 255, 0)
    else:
        button_pressed = False
        button_color = (255, 0, 0)

door_open = False
door_close_img = pygame.image.load("Images/door_closed.png").convert_alpha()
door_close_img.set_colorkey(door_close_img.get_at((0,0)))
door_close_img.
door_open_img = pygame.image.load("Images/door_opened.png").convert_alpha()
door_open_img.set_colorkey(door_close_img.get_at((0,0)))
def door(x,y):
    global door_open, level
    door_rect = pygame.Rect(x,y,door_open_img.get_width(),door_open_img.get_height())

    # functionality
    if button_pressed:
        door_open = True
    else:
        door_open = False

   # screen.blit(door_open_img, (x, y))
    if door_open:
        screen.blit(door_open_img, (x, y))
    else:
        screen.blit(door_close_img, (x,y))

    if player1_rect.colliderect(door_rect) or player2_rect.colliderect(door_rect):
        if door_open:
            level = 2

class cube:
    def __init__(self,x,y):
        self.cube_picked = ""
        self.cube_x, self.cube_y = x,y
        self.cube_rect = pygame.Rect(x,y,50,50)
    def update(self,key):
        if self.cube_picked == "p1":
            self.cube_rect = pygame.Rect(player1_rect.x,player1_rect.y, 50, 50)
        elif self.cube_picked == "p2":
            self.cube_rect = pygame.Rect(player2_rect.x, player2_rect.y, 50, 50)
        else:
            self.cube_rect = pygame.Rect(self.cube_x,self.cube_y,50,50)
        pygame.draw.rect(screen, (50,50,50), self.cube_rect)

        if player1_rect.colliderect(self.cube_rect):
            if key[pygame.K_f]:
                self.cube_picked = "p1"
        if player2_rect.colliderect(self.cube_rect):
            if key[pygame.K_RSHIFT]:
                self.cube_picked = "p2"
        print(self.cube_picked)


level = 1
cube1 = cube(100,100)
while True:
    key = pygame.key.get_pressed()
    mouseClick = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if level == 1:
        door(1000, 100)
        button(450, 450)

    players.updatePlayer1(key)
    players.updatePlayer2(key)

    cube1.update(key)

    fps_display()
    clock.tick(MAX_FPS)
    pygame.display.update()



