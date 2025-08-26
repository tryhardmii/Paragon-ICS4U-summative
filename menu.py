import pygame
import random

from pygame import mouse
from movement import movement
from difficulty import difficulty

pygame.init()
bgx = 0
def quit():
    pygame.quit()

def mainmenu():
    import json
    global bgx
    from sprites import buttons
    def movementrequest():
        with open("playerdata.json","r") as file:
            try:
                jsonfile = json.load(file) #loads data frmo json file
            except:
                jsonfile = {}
                printfont = pygame.font.Font('minecraft_font.ttf', 25)
                errortext = printfont.render("select a difficulty",False,(255,0,0))
                return errortext
            if "otherinfo" in jsonfile:
                movement()
    def reset():
        filecheck=0 #check if theres any info other than difficulty in the file that needs to be deleted
        tempdifficulty = 0
        printfont = pygame.font.Font('minecraft_font.ttf', 25)
        with open("playerdata.json","r") as file:
            try:
                jsonfile = json.load(file)
                if "otherinfo" in jsonfile:
                    filecheck = 1
                    if "difficulty" in jsonfile["otherinfo"]:
                        tempdifficulty = jsonfile["otherinfo"]["difficulty"]
                if "playerdata" in jsonfile:
                    filecheck = 1
            except:
                pass
        if filecheck == 1:
            with open("playerdata.json","w") as file:
                if tempdifficulty!=0:
                    json.dump({"otherinfo": {"difficulty": tempdifficulty}},file)
                else:
                    json.dump({},file)
        return printfont.render("Game Reset!", False, (0, 255, 0)) #resetting game
    printfont = pygame.font.Font('minecraft_font.ttf', 25)
    errortext = printfont.render("",False,(255,0,0))
    menuactive = True
    Screen1 = pygame.display.set_mode((1200, 800))
    color = (0, 0, 255)  # initializing the RGB color blue
    Screen1.fill(color)  # Changing surface color

    #button declarations
    storybutton = buttons(600,300,'menugraphics/story.png', movementrequest)
    resetbutton = buttons(600,450,'menugraphics/resetbutton.png', reset)
    quitbutton = buttons(600,600,'menugraphics/quitbutton.png', quit)
    difficultybutton = buttons(1000,700,'menugraphics/difficulty.png',difficulty)
    #adding buttons to groups
    buttons = pygame.sprite.Group()
    buttons.add(storybutton) 
    buttons.add(resetbutton)
    buttons.add(quitbutton)
    buttons.add(difficultybutton)

    title1 = pygame.image.load('menugraphics/paragon.png').convert_alpha()
    title = pygame.image.load('menugraphics/paragon.png').convert_alpha()
    titlerect = title1.get_rect(center = (600,150))
    pygame.Surface.set_alpha(title,255)
    titlex = title.get_width()#a
    titley = title.get_height()
    bg = pygame.image.load('menugraphics/scrollingbackground.png').convert()
    #bg = pygame.transform.scale(bg, (1400,800))
    pulse = pygame.USEREVENT + 1
    pygame.time.set_timer(pulse, 100)
    x = 0
    def titlescale(x): #makes the title move
        if x%20>10:
            return 1 + (-0.1*(((x%10)-10)**2) + 10)/500
        else:
            return 1 - (-0.1*(((x%10)-10)**2) + 10) /500

    while menuactive == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuactive = False
            if event.type == pulse:
                x+=1
                titlex *= titlescale(x)
                titley *= titlescale(x) #make the title grow and shrink in a loop
                title = pygame.transform.scale(title1, (titlex, titley))
                titlerect = title.get_rect(center = (600,150))
                bgx+=2
                pygame.time.set_timer(pulse, 100)
            for button in buttons:
                button.jiggle()
                i = button.checkpressed(event)
                if i!=0 and button.posx==1000:
                    bgx = i[0]
                    difficulty1 = i[1]
                    with open("playerdata.json","r") as file:
                        try:
                            jsonfile = json.load(file) #loading data
                        except:
                            jsonfile = {}
                        if "otherinfo" in jsonfile:
                            if "difficulty" in jsonfile["otherinfo"]:
                                jsonfile["otherinfo"]["difficulty"] = difficulty1
                        else:
                            jsonfile = {}
                            jsonfile["otherinfo"] = {}
                            jsonfile["otherinfo"]["difficulty"] = difficulty1
                    errortext = printfont.render("",False,(255,0,0))
                    with open("playerdata.json","w") as file:
                        json.dump(jsonfile, file) # writes data onto json
                elif i!=0 and (button.posy == 300 or button.posy == 450):
                    errortext = i
                    

            if bgx==bg.get_width():
                bgx=0

            Screen1.blit(bg,(bgx,0))
            Screen1.blit(bg,(bgx-bg.get_width(),0))

            Screen1.blit(title, titlerect)
            buttons.draw(Screen1)
            Screen1.blit(errortext,(600-errortext.get_width()/2,325))
            pygame.display.update()
            pygame.time.Clock().tick(60)
    pygame.quit()
