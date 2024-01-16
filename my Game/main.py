import random
import os #вміє працювати з ресурсами системи та може прочитувати теки

import pygame
from pygame.constants import QUIT, HIDDEN, K_DOWN, K_RIGHT, K_LEFT, K_UP

pygame.init()

FPS = pygame.time.Clock() #time.Clock саме Clock задає кількість FPS(frame per second).

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20) #SysFont - знаходить в найшій системі якийсь font за імʼям (в нашому випадку це 'Verdana')

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT)) #transform.scale - допомагає підігнати картинку під потрібний розмір
bg_X1 = 0
bg_X2 = bg.get_width() #get_widt - задає розташування 2гої картинки в кінці першої по ширині екрану
bg_move = 3


IMAGE_PATH = "goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)


#player_size = (20, 20)
player = pygame.transform.scale(pygame.image.load('player.png'), (165, 70)).convert_alpha() #convert_alpha() - для того що б не було лишніх малюнків (квадрату і тд.) #pygame.Surface(player_size)
player_size = player.get_size()
#player.fill(COLOR_WHITE)  #fill - заповнити тіло гравця
#player_rect = pygame.Rect(0, (375), *player_size) #player.get_rect()
player_rect = player.get_rect(center = (165//2, 800//2))
#player_speed = [1, 1] #[1, 1] це список, ми записали ці значення в списку щоб потім їх змінювати(так як список ми змінювати можемо на відміну від tuple значеннь)
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_left = [-4, 0]
player_move_up = [0, -4]



def create_enemy():
     
    #enemy_size = (30, 10)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png'), (100, 40)).convert_alpha() #pygame.Surface(enemy_size)
    enemy_size = enemy.get_size()
    #enemy.fill(COLOR_RED)
    enemy_rect = pygame.Rect(WIDTH, random.randint(50, 750), *enemy_size) #якщо колекція list or tuple ми можемо за допомогою "*" розпакувати її значення на відповідні позиції в параметрах функції або в даому випадку в колекції классу
    enemy_move_left = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move_left] # все що пишеться через кому є tuple (якщо ж в "()" або ж в "[]" то списками які є змінними) і викликатись модуть всі ці змінні через їх індекс
    


def create_bonus():
     #bonus_size = (10, 10)
     bonus = pygame.transform.scale(pygame.image.load('bonus.png'), (100, 150)).convert_alpha() #pygame.Surface(bonus_size)
     bonus_size = bonus.get_size()
     #bonus.fill(COLOR_YELLOW)
     bonus_rect = bonus.get_rect()
     bonus_rect = pygame.Rect(random.randint(100, 1100), 0, *bonus_size) #paygame.Rect(x, y) - простий вигляд того що і в якій послідовності має бути в ()
     #bonus_rect.midbottom = (random.randint(bonus.get_width(), WIDTH-bonus.get_height()), -bonus.get_height())
     bonus_move_down = [0, random.randint(3, 6)]
     return [bonus, bonus_rect, bonus_move_down]



CREATE_ENEMY = pygame.USEREVENT + 1 #все що написано КАПСОМ являється константами
pygame.time.set_timer(CREATE_ENEMY, 1500) #pygame.time.set_timer(перше значення це ІВЕНТ, друге це мілісекунди з яким він буде знову зʼявлятись)
CREATE_BONUS = pygame.USEREVENT +  2
pygame.time.set_timer(CREATE_BONUS, 2500)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

bonuses = []
enemies =[]

score = 0

image_index = 0

playing = True


while playing:
    FPS.tick(240)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == HIDDEN:
             playing = True
        if event.type == CREATE_ENEMY:
             enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
             bonuses.append(create_bonus())

        if event.type == CHANGE_IMAGE:
             player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
             image_index += 1
             if image_index >= len(PLAYER_IMAGES):
                  image_index = 0 

   # main_display.fill(COLOR_BLACK) 
    bg_X1 -= bg_move # '-' щоб картинка йшла в протилежний бік руху героя
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width(): #якщо bg_X1 меньше ширини нашої картинки то ми будемо її оновлювати 
         bg_X1 = bg.get_width()
    if bg_X2 < -bg.get_width():
         bg_X2 = bg.get_width()


    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    #main_display.blit(emy, enemy)


    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT: #and відповідає за те що якщо ми в діапазоні ВИСОТИ то ми рухаємось якщо ні то зупинимось
           player_rect = player_rect.move(player_move_down)  
    if keys[K_RIGHT] and player_rect.right < WIDTH:
         player_rect = player_rect.move(player_move_right)   
    if keys[K_LEFT] and player_rect.left > 0:
         player_rect = player_rect.move(player_move_left)
    if keys[K_UP] and player_rect.top > 0:
         player_rect = player_rect.move(player_move_up)

    for enemy in enemies: #for - цикл
        enemy[1] = enemy[1].move(enemy[2]) # всі цифри в дужках "()", "[]" є індексами які викликаються з "return enemy, enemy_rect, enemy_move_left"
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]): #colliderect - коли pygame розуміє що іде пересічення 2х обʼєктів це потрапляє саме в colliderect
            playing = pygame.quit()

    for bonus in bonuses:
         bonus[1] = bonus[1].move(bonus[2])

         main_display.blit(bonus[0], bonus[1])

         if player_rect.colliderect(bonus[1]):
              score += 1
              bonuses.pop(bonuses.index(bonus))
   # enemy_rect = enemy_rect.move(enemy_move_left)
    #print(player_rect.bottom) # player_rect відповідає за рух тому він має такі значення як bottom, Top, bottomleft, bottomright, center, ітд.          
#ІНВЕРСІЯ
   # if player_rect.bottom >= HEIGHT:
        #player_speed[1] = -player_speed[1] # player_speed[1] - в данному випадку швидкість знаходиться за індексом тобто [x, y] index 'x' = 0, index 'y' = 1
    #if player_rect.top < 0: 
       # player_speed[1] = -player_speed[1]
    
   # if player_rect.right >= WIDTH:
        #player_speed[0] = -player_speed[0]
    #if player_rect.left < 0:
        #player_speed[0] = -player_speed[0]
#ІНВЕРСІЯ
     
    #if player_rect.bottom >= HEIGHT:
    #    player_speed = random.choice(([1, -1], [-1, -1]))
    #if player_rect.top <= 0:
    #    player_speed = random.choice (([-1, 1], [1, 1]))
    #if player_rect.right >= WIDTH:
    #    player_speed = random.choice(([-1, -1], [-1, 1]))
    #if player_rect.left <= 0:
    #    player_speed = random.choice (([1, 1], [1, -1]))
    main_display.blit(FONT.render(str(score), True, COLOR_YELLOW), (WIDTH-50, 30)) #render - код, що описує мою форму, або шаблон, що описує мою сторінку, відображається в остаточній формі HTML

    main_display.blit(player, player_rect) #blit задає координати на екрані (який гравець, (x, y))
    #main_display.blit(enemy, enemy_rect)
    #print(len(bonuses))
    #player_rect = player_rect.move(player_speed)

    pygame.display.flip() #flip щоб він зʼявлявся на екрані

    for enemy in enemies:
         if enemy[1].left < 0:
              enemies.pop(enemies.index(enemy)) #функція pop приймає індекс та видаляє значення з циклу

    for bonus in bonuses:
         if bonus[1].bottom > HEIGHT:
              bonuses.pop(bonuses.index(bonus))