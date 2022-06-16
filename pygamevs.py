import pygame
import os
pygame.font.init()
pygame.mixer.init()

FPS = 60
VEL = 5
BULLET_VEL = 10
CANNON_VEL = 7
MAX_BULLET = 40
MAX_CANNON = 5
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
WIDTH, HEIGHT = 900,500

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('SpaceZed')
BORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT)

SSW, SSH = 50, 45
YELLOW_SS_IMG = pygame.image.load(r'C:\Users\meher gandhi\Desktop\SpaceZedGame\Assetsvs\spaceship_yellow.png')
RED_SS_IMG = pygame.image.load(r'C:\Users\meher gandhi\Desktop\SpaceZedGame\Assetsvs\spaceship_red.png')

YELLOW_SS = pygame.transform.rotate(pygame.transform.scale(YELLOW_SS_IMG, (SSW,SSH)), 270)
RED_SS = pygame.transform.rotate(pygame.transform.scale(RED_SS_IMG, (SSW,SSH)), 90)

YELLOW_HIT_BUL = pygame.USEREVENT + 1
RED_HIT_BUL = pygame.USEREVENT + 2

YELLOW_HIT_CAN = pygame.USEREVENT + 3
RED_HIT_CAN = pygame.USEREVENT + 4

YELLOW_HP = 50
RED_HP = 50

BULLET_FIRE_SOUND = pygame.mixer.Sound(r'C:\Users\meher gandhi\Desktop\SpaceZedGame\Assetsvs\Gun+Silencer.mp3')
BULLET_HIT_SOUND  = pygame.mixer.Sound(r'C:\Users\meher gandhi\Downloads\export_ofoct.com.mp3')
CANNON_FIRE_SOUND = pygame.mixer.Sound(r'C:\Users\meher gandhi\Desktop\SpaceZedGame\Assetsvs\14_7s_Tank_Fire_Shot_Sound_Effects_All.mp3')

HP_FONT = pygame.font.SysFont('segoeui', 40)
WINNER_FONT = pygame.font.SysFont('corbel', 80)

SPACE = pygame.transform.scale(pygame.image.load(r'C:\Users\meher gandhi\Desktop\SpaceZedGame\Assetsvs\space2.png'), (WIDTH, HEIGHT))

def draw_window(rrect, yrect, rcan, ycan, rbul, ybul, RED_HP, YELLOW_HP):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    RED_HP_TEXT = HP_FONT.render('Health: ' + str(RED_HP), 1, RED)
    YELLOW_HP_TEXT = HP_FONT.render('Health: ' + str(YELLOW_HP), 1, YELLOW)
    
    WIN.blit(YELLOW_SS, (yrect.x, yrect.y))
    WIN.blit(RED_SS, (rrect.x, rrect.y))
    WIN.blit(YELLOW_HP_TEXT, (WIDTH-RED_HP_TEXT.get_width()-10, 10))
    WIN.blit(RED_HP_TEXT, (10, 10))

    for bullet in rbul:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in ybul:
        pygame.draw.rect(WIN, RED, bullet)

    for cannon in rcan:
        pygame.draw.rect(WIN, RED, cannon)
    for cannon in ycan:
        pygame.draw.rect(WIN, YELLOW, cannon)
    # if RED_HP == 0 or YELLOW_HP == 0: draw_winner()
    pygame.display.update()
    

def draw_winner(winner_text):
    pygame.display.update()
    WIN_TEXT = WINNER_FONT.render(winner_text,1,BLUE,BLACK)
    WIN.blit(WIN_TEXT, (WIDTH/2-150, HEIGHT/2))

    pygame.display.update()
    # pygame.time.delay(5000)

def draw_tie():
    TIE_TEXT = WINNER_FONT.render('Tie Match!',1,BLUE,BLACK)
    WIN.blit(TIE_TEXT, (WIDTH/2-100, HEIGHT/2))

    pygame.display.update()
    # pygame.time.wait(5000)

def rmovement(keys_pressed, rrect):
    if keys_pressed[pygame.K_a] and rrect.x-VEL>0: #LeftRed
       rrect.x -= VEL
    if keys_pressed[pygame.K_d] and rrect.x+VEL+rrect.width<BORDER.x: #RightRed
        rrect.x += VEL
    if keys_pressed[pygame.K_w] and rrect.y-VEL>0: #UpRed
        rrect.y -= VEL
    if keys_pressed[pygame.K_s] and rrect.y+VEL+rrect.height<HEIGHT: #DownRed
        rrect.y += VEL

def ymovement(keys_pressed, yrect):
    if keys_pressed[pygame.K_LEFT] and yrect.x-VEL>BORDER.x+BORDER.width: #LeftYellow
        yrect.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yrect.x+VEL+yrect.width<WIDTH: #RightYellow
        yrect.x += VEL
    if keys_pressed[pygame.K_UP] and yrect.y-VEL>0: #UpYellow
        yrect.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yrect.y+VEL+yrect.height<HEIGHT: #DownYellow
        yrect.y += VEL

def bulmovement(ybul, rbul, rrect, yrect):
    for bullet in rbul:
        bullet.x += BULLET_VEL

        if yrect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT_BUL))
            rbul.remove(bullet)
        elif bullet.x<0:
            rbul.remove(bullet)

    for bullet in ybul:
        bullet.x -= BULLET_VEL

        if rrect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT_BUL))
            ybul.remove(bullet)
        elif bullet.x>WIDTH:
            ybul.remove(bullet)

def canmovement(ycan, rcan, rrect, yrect):
    for cannon in rcan:
        cannon.x += CANNON_VEL
        if yrect.colliderect(cannon):
            pygame.event.post(pygame.event.Event(YELLOW_HIT_CAN))
            rcan.remove(cannon)
        elif cannon.x<0:
            rcan.remove(cannon)

    for cannon in ycan:
        cannon.x -= CANNON_VEL
        if rrect.colliderect(cannon):
            pygame.event.post(pygame.event.Event(RED_HIT_CAN))
            ycan.remove(cannon)
        elif cannon.x>WIDTH:
            ycan.remove(cannon)

def main():
    
    YELLOW_HP = 50
    RED_HP = 50

    rrect = pygame.Rect(100, 300, SSW, SSH)
    yrect = pygame.Rect(700, 300, SSW, SSH)

    rbul = list()
    ybul = list()

    rcan = list()
    ycan = list()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(rbul) < MAX_BULLET:
                    bullet = pygame.Rect(rrect.x+rrect.width, rrect.y+rrect.height//2, 10, 5)
                    rbul.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(ybul) < MAX_BULLET:
                    bullet = pygame.Rect(yrect.x, yrect.y+yrect.height//2, 10, 5)
                    ybul.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_f and len(rcan) < MAX_CANNON:
                    cannon = pygame.Rect(rrect.x+rrect.width, rrect.y+rrect.height//1.3, 20, 10)
                    rcan.append(cannon)
                    CANNON_FIRE_SOUND.play()
                if event.key == pygame.K_SLASH and len(ycan) < MAX_CANNON:
                    cannon = pygame.Rect(yrect.x, yrect.y+yrect.height//1.3, 20, 10)
                    ycan.append(cannon)
                    CANNON_FIRE_SOUND.play()

            if event.type == RED_HIT_BUL:
                RED_HP -=5
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT_BUL:
                YELLOW_HP -=5
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT_CAN:
                RED_HP -=10
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT_CAN:
                YELLOW_HP -=10
                BULLET_HIT_SOUND.play()

        winner_text = ''
        if RED_HP <= 0:
            winner_text = 'Yellow Wins!'
        if YELLOW_HP <=0:
            winner_text = 'Red Wins!'
        if winner_text != '':
            draw_winner(winner_text)
            # for i in rbul:
            #     rbul.remove(i)
            # for i in ybul:
            #     ybul.remove(i)
            # for i in ycan:
            #     ycan.remove(i)
            # for i in rcan:
            #     rcan.remove(i)
            pygame.time.delay(5000)
            break

        if len(rbul) == MAX_BULLET and len(ybul) == MAX_BULLET:
            draw_tie()
            # for i in rbul:
            #     rbul.remove(i)
            # for i in ybul:
            #     ybul.remove(i)
            # for i in ycan:
            #     ycan.remove(i)
            # for i in rcan:
            #     rcan.remove(i)
            pygame.time.delay(5000)
            break

        print(len(rbul), len(ybul))
        keys_pressed = pygame.key.get_pressed()
        ymovement(keys_pressed, yrect)
        rmovement(keys_pressed, rrect)

        bulmovement(ybul, rbul, rrect, yrect)
        canmovement(ycan, rcan, rrect, yrect)
        draw_window(rrect, yrect, ycan, rcan, rbul, ybul, RED_HP, YELLOW_HP)
    main()

if __name__ == '__main__':
    main()
