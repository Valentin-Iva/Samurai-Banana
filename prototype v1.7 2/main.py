from turtle import st
import pygame
import random
import pygame_gui
from pygame.locals import *
from bananas import Banana
from objects import Flower
from objects import Bomb
from objects import Mushroom
from objects import BlueMushroom
from buttons import Button

#moviepy

pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.mixer.music.load('assets/funkytingzOFFICIAL.wav')

#game run constants
clock = pygame.time.Clock()
FPS=50
game_over = False
#screen constants
SCREEN_WIDTH = 700
SCREEN_LENGTH = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
pygame.display.set_caption("Flappy Bird")

#load images
bg = pygame.image.load("assets/background.png")
bg1 = pygame.image.load("assets/background1.png")
bg2 = pygame.image.load("assets/background2.png")
GROUND_IMG = pygame.image.load("assets/ground.png")
logo= pygame.image.load("assets/logo.png")

score=0

def drawText(text,font,textCol,x,y):
        img=font.render(text,True,textCol)
        screen.blit(img,(x,y))

font=pygame.font.SysFont('Impact',50)
MANAGER = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_LENGTH))
TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((150,100),(400, 50)), manager=MANAGER, object_id="#main_text_entry")

def nameLog():
    global current_player
    current_player = "" 
    quit_button= Button(SCREEN_WIDTH/2,410, pygame.image.load("assets/quitbutton.png"))

    run=True

    while run:
        screen.blit(bg1,(0,0))
        font2=pygame.font.SysFont('Display',40)
        drawText("Enter your username and press the ENTER key",font2,(255,255,255),40,50)

        UI_REFRESH_RATE = clock.tick(60)/1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type==pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry": #user input taken and saved as current_player
              current_player+= event.text
              mainGame()  
            
            MANAGER.process_events(event)
        
        MANAGER.update(UI_REFRESH_RATE)

        MANAGER.draw_ui(screen)

        if quit_button.draw(screen)==True:
            run=False

        pygame.display.update()

    pygame.quit()


def mainGame():
    global score
    score = 0
    #scroll constants
    ground_scroll = 0
    SCROLL_SPEED = 7
    #collision const/variable initialised
    
    HIDEPOS = 600
    
    lives = 3
    
    #loading sprites
    sprite_group = pygame.sprite.Group()
    object_sprites = pygame.sprite.Group()
    banana1= Banana()
    speed = 4
    sprite_group.add(banana1)

    lengths=[150,50,325]

    flower1 = Flower(SCREEN_WIDTH, random.choice(lengths), 7)
    bomb1 = Bomb(SCREEN_WIDTH, random.choice(lengths), 7 )
    mushroom1 = Mushroom(SCREEN_WIDTH, random.choice(lengths), 7 )
    mushroom2 = BlueMushroom(SCREEN_WIDTH, random.choice(lengths), 7 )
    
    run = True 

    background=bg
    red_mushroom_mode= False
    blue_mushroom_mode= False
    time_of_mode1=0
    time_of_mode=0
    
    while run:
        movement_choices = [10,-10,5,-5,20,-20]   
        if red_mushroom_mode==True:
            time_of_mode+=1
            object_sprites.remove(mushroom1)
            object_sprites.remove(mushroom2)
            for object in object_sprites:
                object.rect.y= object.rect.y + random.choice(movement_choices)

        elif red_mushroom_mode==False:
            time_of_mode=0
            object_sprites.add(flower1)
            object_sprites.add(bomb1)
            object_sprites.add(mushroom1)
            object_sprites.add(mushroom2)

        if time_of_mode>=150:
            background = bg
            red_mushroom_mode=False
            blue_mushroom_mode = False
        
        #blue mushroom mode
        if blue_mushroom_mode==True:
            time_of_mode1+=1
            banana1.increaseSize()
            object_sprites.remove(mushroom1)
            object_sprites.remove(mushroom2)
        if time_of_mode1==100:
            banana1.decreaseSize()
            blue_mushroom_mode=False
            object_sprites.add(mushroom1)
            object_sprites.add(mushroom2)
        if blue_mushroom_mode==False:
            time_of_mode1 = 0

        
            
        
        
        clock.tick(FPS)
        #draw background
        screen.blit(background, (0,0)) 

        sprite_group.draw(screen)
        sprite_group.update()

        object_sprites.draw(screen)
        object_sprites.update()
        # draw ground
        screen.blit(GROUND_IMG, (ground_scroll,0))

        if game_over == False:
            #generate new objects
            for object in object_sprites:
                object.speed = random.randint(2,30)
                if object.rect.x < -10:
                    object.rect.x = SCREEN_WIDTH
                    height = random.choice(lengths)
                    object.rect.y = height
                    lengths.remove(height)
            lengths=[50,150,237,325]

            # scroll ground
            ground_scroll -= SCROLL_SPEED
            if abs(ground_scroll) > 50:
                ground_scroll=0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #collisions/score
        flower_collect_sound=pygame.mixer.Sound('assets/flowersound.wav')

        if pygame.sprite.collide_rect(banana1,flower1):
            flower_collect_sound.play()
            score+=1
            flower1.rect.y = HIDEPOS

        if pygame.sprite.collide_rect(banana1,bomb1):
            lives-=1
            bomb1.rect.y = HIDEPOS

        if pygame.sprite.collide_rect(banana1,mushroom1):
            mushroom1.rect.y = HIDEPOS
            background = bg2
            red_mushroom_mode=True

        if pygame.sprite.collide_rect(banana1,mushroom2):
            mushroom2.rect.y = HIDEPOS
            blue_mushroom_mode = True

        if lives==0:
            endScreen()
            #run=False

        #display score  
        font=pygame.font.SysFont('Impact',60)
        drawText(str(score),font,(255,255,255),int(SCREEN_WIDTH/2),20)   
        drawText("LIVES:"+str(lives),font,(255,255,255),int(SCREEN_WIDTH/8),20) 

        pygame.display.update()

    pygame.quit() #dont use this in the whole thing


def endScreen():
    global score
    
    #buttons
    play_again_button= Button(SCREEN_WIDTH/2,100,pygame.image.load("assets/playagainbutton.png"))
    quit_button= Button(SCREEN_WIDTH/2,410, pygame.image.load("assets/quitbutton.png"))
    leaderboard_button= Button(SCREEN_WIDTH/2,255,pygame.image.load("assets/leaderboardbutton.png"))

    run=True

    while run:

        screen.blit(bg1,(0,0))
    
        if play_again_button.draw(screen)==True:
            mainGame()
        if quit_button.draw(screen)==True:
            run=False
        if leaderboard_button.draw(screen)==True:
            leaderboard()
        
        #score display
        drawText("Score="+str(score),font,(255,255,255),20,0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

def startScreen():

    play_button= Button(SCREEN_WIDTH/2,100,pygame.image.load("assets/playbutton.png"))
    quit_button= Button(SCREEN_WIDTH/2,410, pygame.image.load("assets/quitbutton.png"))
    

    run=True

    while run:

        screen.blit(bg1,(0,0))
        screen.blit(logo,(SCREEN_WIDTH/6,SCREEN_LENGTH/4))

        if play_button.draw(screen)==True:
            nameLog()
        if quit_button.draw(screen)==True:
            run=False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

def leaderboard():

    font=pygame.font.SysFont('Impact',60)
    
    leaderboard_rank= pygame.image.load("assets/leaderboardimg.png")

    leaderboard_list=[]

    #appending new score

    file = open("score.txt","a")

    file.write(current_player+";"+str(score)+"\n")

    file.close()

    file = open("score.txt","r")

    for line in file:
        data = line.split(";")
        leaderboard_list.append([data[0],data[1]])

    file.close()

    #sort the list
    swap = True

    while swap==True:
        swap = False
        for i in range(0,len(leaderboard_list)-1):
            if int(leaderboard_list[i][1])>int(leaderboard_list[i+1][1]):
                temp = leaderboard_list[i+1]
                leaderboard_list[i+1]=leaderboard_list[i]
                leaderboard_list[i]=temp
                swap = True
    
    
    
    #delete the lowest score from list and file
    leaderboard_list=leaderboard_list[1:]

    #overwriting the text document

    file = open("score.txt","w")

    file.truncate(0)

    for item in leaderboard_list:
        file.write(item[0]+";"+str(item[1]))

    file.close()

    play_again_button= Button(SCREEN_WIDTH/4,410,pygame.image.load("assets/playagainbutton.png"))
    quit_button= Button(SCREEN_WIDTH*3/4,410, pygame.image.load("assets/quitbutton.png"))
    run=True

    while run:

        screen.blit(bg1,(0,0))
        screen.blit(leaderboard_rank,(190,60))

        if play_again_button.draw(screen)==True:
            mainGame()
        if quit_button.draw(screen)==True:
            run=False
    #leaderboard display
        for i in range(len(leaderboard_list)):
            drawText(leaderboard_list[i][0]+":"+str(leaderboard_list[i][1]),font,(255,255,255),int(250),250-(50*i))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

pygame.mixer.music.play(-1) 

startScreen()