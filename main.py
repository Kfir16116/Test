from pygame.locals import *
import pygame, sys, time

pygame.init()

clock = pygame.time.Clock()
MAX_FPS = 60

screen_width, screen_height = 1200,700
flags = DOUBLEBUF
screen = pygame.display.set_mode((screen_width, screen_height), flags, 16)
screen.set_alpha(None)
pygame.display.set_caption("Idiots")


def fps_display():
    fps = clock.get_fps()
    fps_font = pygame.font.SysFont('arial', 25)
    fps_text = fps_font.render(f"{int(fps)}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))


# player 1 settings
player1_img = pygame.image.load("Images/player_1.png").convert()
player1_img = pygame.transform.scale(player1_img, (player1_img.get_width()/2,player1_img.get_height()/2))
player1_img.set_colorkey(player1_img.get_at((0,0)))
player1_img_flipped = pygame.transform.flip(player1_img, 90, 0)
player1_rect = pygame.Rect(140,480, 100,125)
player1_speed = 7
player1_dir = "right"
# player1_img = pygame.image.load("Images/")

# player 2 settings
player2_img = pygame.image.load("Images/player_2.png").convert()
player2_img = pygame.transform.scale(player2_img, (player2_img.get_width()/2,player2_img.get_height()/2))
player2_img.set_colorkey(player2_img.get_at((0,0)))
player2_img_flipped = pygame.transform.flip(player2_img, 90, 0)
player2_rect = pygame.Rect(540,480, 140,160)
player2_speed = 7
player2_dir = "right"
# player2_img = pygame.image.load("Images/")

class Players:

    def updatePlayer1(self, key):
        global player1_rect, player2_rect, player1_speed, player1_img, player2_img, player1_dir
        
        # draw rect (if needed)
        #pygame.draw.rect(screen, (0, 0, 0), player1_rect)

        # draw player
        if player1_dir == "right":
            screen.blit(player1_img, (player1_rect.x, player1_rect.y))
        if player1_dir == "left":
            screen.blit(player1_img_flipped, (player1_rect.x, player1_rect.y))

        # movement
        if not transitioning:
            if key[pygame.K_a]:
                if player1_rect.x > 0:
                    player1_rect.x -= player1_speed
                player1_dir = "left"
            if key[pygame.K_d]:
                if player1_rect.x < (screen_width-100):
                    player1_rect.x += player1_speed
                player1_dir = "right"

            if key[pygame.K_w]:
                if player1_rect.y > 0:
                    player1_rect.y -= player1_speed
            if key[pygame.K_s]:
                if player1_rect.y < (screen_height-100):
                    player1_rect.y += player1_speed

    def updatePlayer2(self, key):
        global player1_rect, player2_rect, player2_speed, player2_dir

        # draw rect (if needed)
        #pygame.draw.rect(screen, (0, 0, 0), player2_rect)

        # draw player
        if player2_dir == "right":
            screen.blit(player2_img, (player2_rect.x, player2_rect.y))
        if player2_dir == "left":
            screen.blit(player2_img_flipped, (player2_rect.x, player2_rect.y))

        # movement
        if not transitioning:
            if key[pygame.K_LEFT]:
                if player2_rect.x > 0:
                    player2_rect.x -= player2_speed
                player2_dir = "left"
            if key[pygame.K_RIGHT]:
                if player2_rect.x < (screen_width - 100):
                    player2_rect.x += player2_speed
                player2_dir = "right"

            if key[pygame.K_UP]:
                if player2_rect.y > 0:
                    player2_rect.y -= player2_speed
            if key[pygame.K_DOWN]:
                if player2_rect.y < (screen_height - 100):
                    player2_rect.y += player2_speed

players = Players()

button_color = (255,0,0)
button_pressed = False
button_rect = pygame.Rect(0,0,50,50)
def button(x,y):
    global button_color, button_pressed, button_rect

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
door_close_img = pygame.transform.scale(door_close_img, (door_close_img.get_width()/2, door_close_img.get_height()/2))
door_close_img.set_colorkey(door_close_img.get_at((0,0)))
door_open_img = pygame.image.load("Images/door_opened.png").convert_alpha()
door_open_img = pygame.transform.scale(door_open_img, (door_open_img.get_width(), door_open_img.get_height()))
door_open_img.set_colorkey(door_close_img.get_at((0,0)))
door_cover_x, door_cover_y = 0,0
origin_x,origin_y=0,0
change_cover_loc = False
def door(x,y):
    global door_open, level, door_cover_x, door_cover_y, change_cover_loc, origin_x, origin_y
    origin_x,origin_y=x,y
    if not change_cover_loc:
        change_cover_loc=True
        door_cover_x, door_cover_y = x-22, y

    door_rect = pygame.Rect(x,y,door_open_img.get_width(),door_open_img.get_height())

    # functionality
    if button_pressed:
        door_open = True
    else:
        door_open = False

    screen.blit(door_open_img, (x, y))
    screen.blit(door_close_img, (door_cover_x, door_cover_y))
    if door_open:
        if door_cover_y > origin_y-250:
            door_cover_y -= 4
    else:
        if door_cover_y < origin_y:
            door_cover_y += 4

    # next level
    if player1_rect.colliderect(door_rect) and player2_rect.colliderect(door_rect):
        if door_open:
            if level == 2:
                level = 3
            if level == 1:
                updateLevel()
            updateLevel()

def startingDoor():
    global level, transitioning
    screen.blit(door_open_img, ((screen_width - door_open_img.get_width()),100))
    door_rect = pygame.Rect(1000, 10, door_open_img.get_width(), door_open_img.get_height())
    if player1_rect.colliderect(door_rect) and player2_rect.colliderect(door_rect):
        updateLevel()
        transitioning = True
        if transition_rect_x >= 0:
            level = 1
        #updateLevel()

player1_cube_pick_timer = False
player2_cube_pick_timer = False
player1_cube_pick_timer_value = 0
player2_cube_pick_timer_value = 0
class cube:
    def __init__(self,x,y):
        self.cube_picked = ""
        self.cube_x, self.cube_y = x,y
        self.cube_rect = pygame.Rect(x,y,50,50)
    def update(self,key):
        global player1_cube_pick_timer, player2_cube_pick_timer, button_pressed, button_color
        global player1_cube_pick_timer_value, player2_cube_pick_timer_value

        # Rendering Cube
        if self.cube_picked == "p1":
            if player1_dir == "right":
                self.cube_rect = pygame.Rect(player1_rect.x+72,player1_rect.y+45, 50, 50)
            if player1_dir == "left":
                self.cube_rect = pygame.Rect(player1_rect.x-10,player1_rect.y+45, 50, 50)
        elif self.cube_picked == "p2":
            if player2_dir == "right":
                self.cube_rect = pygame.Rect(player2_rect.x+117, player2_rect.y+52, 50, 50)
            if player2_dir == "left":
                self.cube_rect = pygame.Rect(player2_rect.x-32, player2_rect.y+52, 50, 50)
        else:
            self.cube_rect = pygame.Rect(self.cube_x,self.cube_y,50,50)
        pygame.draw.rect(screen, (50,50,50), self.cube_rect)

        # Pick and Drop
        if player1_rect.colliderect(self.cube_rect):
            if pygame.KEYDOWN:
                if key[pygame.K_f]:
                    if not player1_cube_pick_timer:
                        player1_cube_pick_timer_value = 0
                        if not self.cube_picked == "p1":
                            self.cube_picked = "p1"
                        else:
                            if player1_dir == "right":
                                self.cube_x, self.cube_y = player1_rect.x+72, player1_rect.y+45
                            if player1_dir == "left":
                                self.cube_x, self.cube_y = player1_rect.x-10, player1_rect.y+45
                            self.cube_picked = ""
                    if player1_cube_pick_timer_value < 1:
                        player1_cube_pick_timer_value = time.time()
                        player1_cube_pick_timer = True
        if player2_rect.colliderect(self.cube_rect):
            if pygame.KEYDOWN:
                if key[pygame.K_RSHIFT]:
                    if not player2_cube_pick_timer:
                        player2_cube_pick_timer_value = 0
                        if not self.cube_picked == "p2":
                            self.cube_picked = "p2"
                        else:
                            if player2_dir == "right":
                                self.cube_x, self.cube_y = player2_rect.x+117, player2_rect.y+52
                            if player2_dir == "left":
                                self.cube_x, self.cube_y = player2_rect.x-32, player2_rect.y+52
                            self.cube_picked = ""
                    if player2_cube_pick_timer_value < 1:
                        player2_cube_pick_timer_value = time.time()
                        player2_cube_pick_timer = True

        # Pick and Drop Timers
        if player1_cube_pick_timer:
            if (time.time() - player1_cube_pick_timer_value) > 0.5:
                player1_cube_pick_timer = False
        if player2_cube_pick_timer:
            if (time.time() - player2_cube_pick_timer_value) > 0.5:
                player2_cube_pick_timer = False

        # button
        if self.cube_rect.colliderect(button_rect):
            if self.cube_picked == "":
                button_pressed=True
                button_color = (0, 255, 0)

background_img = pygame.image.load("Images/background.png").convert()
def background():
    screen.blit(pygame.transform.scale(background_img, (screen_width,screen_height)), (0,0))

def borders():
    global player1_rect, player2_rect
    if level == 0:
        if player1_rect.y < 350-player1_rect.height+15:
            player1_rect.y = 350-player1_rect.height+15
        if player2_rect.y < 350-player2_rect.height+15:
            player2_rect.y = 350-player2_rect.height+15

level = 0
def updateLevel():
    global cube1
    if level == 0:
        cube1 = cube(100,100)

transitioning = False
transition_rect_x, transition_rect_y = -screen_width*2,0
transition_rect = pygame.Rect((transition_rect_x,transition_rect_y,screen_width*2,screen_height))
def levelTransition():
    global transition_rect,transition_rect_x,transition_rect_y, transitioning
    #transition_rect = pygame.Rect((-screen_width, -screen_height, screen_width, screen_height))
    transition_rect = pygame.Rect((transition_rect_x, transition_rect_y, screen_width*2, screen_height))
    pygame.draw.rect(screen, (0, 0, 0), transition_rect)
    if transition_rect_x < screen_width+250:
        transition_rect_x += 20
    if transition_rect_x >= screen_width+250:
        transitioning=False
        transition_rect_x, transition_rect_y = -screen_width, -screen_height
    print(transition_rect_x)


cube1 = ""
while 1:
    if level == 0:
        background()
    if level > 0:
        screen.fill((255, 255, 255))
    key = pygame.key.get_pressed()
    #mouseClick = pygame.mouse.get_pressed()
    #mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    borders()

    if level == 0:
        startingDoor()
        screen.blit(player1_sprites[0], (0,0))
        players.updatePlayer1(key)
        players.updatePlayer2(key)

    if transition_rect_x > 0 or not transitioning:
        if level == 1:
            door(1000, 100)
            players.updatePlayer1(key)
            players.updatePlayer2(key)
            button(450, 450)
            cube1.update(key)

    if transitioning:
        print('transition')
        levelTransition()

    fps_display()
    clock.tick(MAX_FPS)
    pygame.display.update()
