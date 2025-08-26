import pygame
import random
import math
from pygame import surface

from movement import *
global bossfight
pygame.init() #all types of sprite classes to be displayed on screen with functions to print them and update values if necessary


class buttons(pygame.sprite.Sprite):  # buttons sprite
    def __init__(self, posx, posy, image, function):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.original_image = self.image
        self.posx = posx
        self.posy = posy
        self.sizex = self.image.get_width()
        self.sizey = self.image.get_height()
        self.rect = self.image.get_rect(center=(posx, posy))
        self.function = function

    def jiggle(self): #increases size by 10% when hovered over by mosue
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = pygame.transform.scale(self.original_image, (self.sizex * 1.1, self.sizey * 1.1))
            self.rect = self.image.get_rect(center=(self.posx, self.posy))
        else:
            self.image = pygame.transform.scale(self.original_image, (self.sizex, self.sizey))
            self.rect = self.image.get_rect(center=(self.posx, self.posy))

    def checkpressed(self, event): #checking if it's pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                i = self.function()
                if i!=0:
                    return i              
                return True
        return False


class player():
    def __init__(self, HP, damage, defense, tilex, tiley,currentquest,mobsdefeated,inventory,gold):
        self.HP = HP
        self.damage = damage
        self.defense = defense
        self.imagestr = 'graphics/playeranimations/playerdown.png'
        self.tilex = tilex
        self.tiley = tiley
        self.posx = 608
        self.displacedx = 0
        self.previoustilex = 0 #attributes
        self.previoustiley = 0
        self.posy = 480
        self.displacedy = 0
        self.dialogueterm = 0
        self.sizex = pygame.image.load(self.imagestr).convert().get_width()
        self.sizey = pygame.image.load(self.imagestr).convert().get_height()
        self.changingdirection = False
        self.movementframe = 0
        self.gold = gold
        self.inventory = inventory
        #self.rect = pygame.Rect((self.posx - 16, self.posy - 16), (32, 32))
        #self.rect.y -= 32
        self.currentquest = currentquest #used to track quest
        self.mobsdefeated = mobsdefeated
    def convert_dict(self):
        return self.__dict__
    @classmethod #method for that class
    def from_dict(cls, dict_data): #using class values instead of self values to
        from items import item, weapon, defence
        inventory = dict_data["inventory"]
        full_inventory = {"weapon": [],
                          "defence": [],
                          "drops": []}
        for x in inventory:
            for y in inventory[x]: #adding things to your inventory
                if x=="weapon":
                    full_inventory[x].append(weapon(y["name"],y["imagestr"],y["cost"],y["damage"]))
                elif x=="defence":
                    full_inventory[x].append(defence(y["name"],y["imagestr"],y["cost"],y["blockpercentage"]))
                elif x=="drops":
                    full_inventory[x].append(item(y["name"],y["imagestr"],y["cost"]))
        return cls(dict_data['HP'], dict_data['damage'], dict_data['defense'], dict_data['tilex'], dict_data['tiley'], dict_data['currentquest'],dict_data['mobsdefeated'],full_inventory,dict_data['gold'])
    
    def checkcollide(self, objectgroup): #obstacle collision
        blockeddirections = []
        for object in objectgroup:
            i=0
            try:
                if object.following == True:
                    pass
                else:
                   i=1 
            except:
                i=1
            if i==1:
                self.interactingtiles = [(self.tilex, self.tiley - 1), (self.tilex, self.tiley + 1),
                                         (self.tilex - 1, self.tiley), (self.tilex + 1, self.tiley)]
                #check for npc that you're talking to
                keytoblock = {
                    (self.tilex, self.tiley - 1): "w",
                    (self.tilex, self.tiley + 1): "s",
                    (self.tilex - 1, self.tiley): "a",
                    (self.tilex + 1, self.tiley): "d"
                }  # abc

                try:
                    tilestocheck = [(object.tilex + x, object.tiley + y) for x in range(object.tilexspan) for y in
                                    range(object.tileyspan)]
                    for interactingtile in keytoblock:
                        for tile in tilestocheck:
                            if tile == interactingtile:
                                blockeddirections.append(keytoblock[interactingtile])
                except:
                    # blockeddirections = [keytoblock[tilenum] for tilenum in range(len(self.interactingtiles)) if (object.tilex,object.tiley) == self.interactingtiles[tilenum] for object in objectgroup]
                    for tile in keytoblock:
                        if (object.tilex, object.tiley) == tile:
                            blockeddirections.append(keytoblock[tile])
        return blockeddirections

    def interact(self, npcgroup, direction):
        facingtile = { #tile that you're facing
            "w": (self.tilex, self.tiley - 1),
            "s": (self.tilex, self.tiley + 1),
            "a": (self.tilex - 1, self.tiley),
            "d": (self.tilex + 1, self.tiley)
        }
        try:
            for npc in npcgroup:
                if facingtile[direction] in [(x,npc.tiley) for x in range(npc.tilex, npc.tilex + npc.tilexspan)]:
                    return npc
        except: #return the npc that you are interacting with/facing with
            for npc in npcgroup:
                if (npc.tilex, npc.tiley) == facingtile[direction]:
                    return npc
        return 0

    def movementanimation(self, direction, num): #list of movementanimations. syntax is [direction][animation]
        animationlist = [["graphics/playeranimations/playeruprun1.png", "graphics/playeranimations/playeruprun2.png",
                          "graphics/playeranimations/playeruprun3.png", "graphics/playeranimations/playerup.png"],
                         ["graphics/playeranimations/playerdownrun1.png",
                          "graphics/playeranimations/playerdownrun2.png",
                          "graphics/playeranimations/playerdownrun3.png", "graphics/playeranimations/playerdown.png"],
                         ["graphics/playeranimations/playerleftrun1.png",
                          "graphics/playeranimations/playerleftrun2.png",
                          "graphics/playeranimations/playerleftrun3.png", "graphics/playeranimations/playerleft.png"],
                         ["graphics/playeranimations/playerrightrun1.png",
                          "graphics/playeranimations/playerrightrun2.png",
                          "graphics/playeranimations/playerrightrun3.png", "graphics/playeranimations/playerright.png"]]
        self.imagestr = animationlist[direction][num]

    def dialogue(self, image,dialoguestr, predialogue_key, dialogueskip):
        if npc == 0:
            return False
        else:
            if self.dialogueterm == 0:
                self.selecteddialogue = dialoguestr
                self.predialogue_key = predialogue_key #dialogue
            if self.dialogueterm < len(dialoguestr):
                if dialogueskip == 0:
                    self.dialogueterm += 1 #next voiceline
                else:
                    self.dialogueterm = len(dialoguestr)
                text = "".join(dialoguestr[:self.dialogueterm]) #new lines
                self.substrings = []
                if len(text) > 40:
                    for linelength in range(1, math.ceil(len(text) / 40) + 1):
                        self.substrings.append(text[(linelength - 1) * 40:(linelength * 40)])
                else:
                    self.substrings.append(text)
            return textbox(image, self.substrings, 72, 664, 0, 0) #textbox to put the text into

class textbox(pygame.sprite.Sprite):
    def __init__(self, spriteimage, textlist, posx, posy, fontsize, fontcolor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('graphics/textframe.png')
        self.spriteimage = pygame.transform.scale(spriteimage, (128, 128))
        printfont = pygame.font.Font('minecraft_font.ttf', 25)
        self.boxtexts = [printfont.render(substring, False, (255, 255, 255)) for substring in textlist]
        # self.rect = self.boxtext.get_rect(topleft = (posx,posy))
        self.posx = posx
        self.posy = posy
        self.fontsize = fontsize
        self.fontcolor = fontcolor


class npc(pygame.sprite.Sprite): #npcs
    def __init__(self, name, dialogue, tilex, tiley, dialoguetype,image):
        pygame.sprite.Sprite.__init__(self)
        self.type = "npc"
        self.name = name
        self.dialogue = []
        self.dialoguetype = dialoguetype
        self.dialoguenum = 0
        for x in range(len(dialogue)):
            self.dialogue.append([*dialogue[x]])
        self.tilex = tilex
        self.tiley = tiley
        self.posx = self.tilex * 32
        self.posy = self.tiley * 32
        if type(image) == list:
            self.image = pygame.image.load(image[0]).convert_alpha()
            self.imagelist = {(0,1):pygame.image.load(image[0]).convert_alpha(),
                              (1, 0): pygame.image.load(image[1]).convert_alpha(), #just for old man following animations
                              (-1, 0): pygame.image.load(image[2]).convert_alpha(),
                              (0, -1): pygame.image.load(image[3]).convert_alpha()}
        else:
            self.image = pygame.image.load(image).convert_alpha()
        self.sizex = self.image.get_width()
        self.sizey = self.image.get_height()
        self.rect = self.image.get_rect(center=(self.posx, self.posy))
        self.following = False
        self.turnterm = 0  # used for following
        self.type = "npc"
        self.talked = 0
    def update(self, player, speed, velocity):

        if self.following == False:
            try:
                self.image = self.imagelist[(0,1)] #just for old man following you
            except:
                pass
            self.posx = int(608 - (player.tilex - self.tilex) * 32 + player.displacedx)
            self.posy = int(480 - (player.tiley - self.tiley) * 32 + player.displacedy)
            self.rect = self.image.get_rect(center=(self.posx, self.posy))
        else:

            if player.changingdirection == False:
                self.rect = self.image.get_rect(center=(
                608 - (player.tilex - player.previoustilex) * 32, 480 - (player.tiley - player.previoustiley) * 32))
            else:
                # because player is centered on screen, we need to move opposite the player whenever it turns
                self.turnterm += speed
                tempdisplacement = [x * self.turnterm for x in player.changingdirection]
                if abs(velocity[0]) == abs(tempdisplacement[0]) or abs(velocity[1]) == abs(
                        tempdisplacement[1]):  # check if you're turning 180deg
                    self.rect = self.image.get_rect(center=(
                    608 - (player.tilex - player.previoustilex) * 32 - tempdisplacement[0] * 2,
                    480 - (player.tiley - player.previoustiley) * 32 - tempdisplacement[1] * 2))
                else:
                    self.rect = self.image.get_rect(center=(
                    608 - (player.tilex - player.previoustilex) * 32 - tempdisplacement[0] + self.turnterm * velocity[
                        0],
                    480 - (player.tiley - player.previoustiley) * 32 - tempdisplacement[1] + self.turnterm * velocity[
                        1]))
            try:
                self.image = self.imagelist[((player.posx - self.rect.centerx) / 32, (player.posy - self.rect.centery) / 32)]
            except:
                pass
class chest(pygame.sprite.Sprite):
    def __init__(self, name, tilex, tiley):
        pygame.sprite.Sprite.__init__(self)
        self.type = "chest"
        self.name = name
        self.tilex = tilex
        self.tiley = tiley
        self.dialoguetype = "not random"
        a = ["You found 250 gold in the chest!"]
        self.dialogue = []
        for x in a: #dialogue is one letter at a time
            self.dialogue.append([*x])
        self.dialoguenum = 0
        self.posx = self.tilex * 32
        self.posy = self.tiley * 32
        self.image = pygame.image.load('graphics/chest.png').convert_alpha()
        self.sizex = self.image.get_width()
        self.sizey = self.image.get_height()
        #self.image.fill("red")
        self.rect = self.image.get_rect(center=(self.posx, self.posy))
        self.opened = False #only can be opened once

    def updatechest(self, player):
        self.posx = int(608 - (player.tilex - self.tilex) * 32 + player.displacedx)
        self.posy = int(480 - (player.tiley - self.tiley) * 32 + player.displacedy)
        self.rect = self.image.get_rect(center=(self.posx, self.posy))


class obstacle(pygame.sprite.Sprite):
    def __init__(self, tilex, tiley, tilexspan, tileyspan):
        pygame.sprite.Sprite.__init__(self)
        self.type = "obstacle"
        self.tilex = tilex
        self.tilexspan = tilexspan
        self.tileyspan = tileyspan
        self.tiley = tiley
        self.posx = 0
        self.posy = 0

    def update(self, player):
        pass
        # code to display surfaces for bug testing if necessary
        # displacements = [player.displacedx,player.displacedy]
        # differences = [-1 if x<0 else 1 if x>0 else 0 for x in displacements]
        # self.posx = int(608 - (player.tilex-self.tilex) * 32 - player.displacedx-16)
        # self.posy = int(480 - (player.tiley - self.tiley) * 32 - player.displacedy-16)
        # self.rect = pygame.Rect(self.posx, self.posy, self.tilexspan*32, self.tileyspan*32)


class water(obstacle): #water obstacle
    def __init__(self, tilex, tiley, tilexspan, tileyspan):
        super().__init__(tilex, tiley, tilexspan, tileyspan)  #
        self.type = "water"


class door(obstacle): #door obstacle
    def __init__(self, tilex, tiley, tilexspan, tileyspan, destination):
        super().__init__(tilex, tiley, tilexspan, tileyspan)
        self.type = "door"
        self.destination = destination
        self.image = pygame.surface.Surface((32,32))
        self.image.set_alpha(0)


class tallgrass(obstacle):#grass
    def __init__(self, tilex, tiley, tilexspan, tileyspan, area):
        super().__init__(tilex, tiley, tilexspan, tileyspan)
        self.type = "tallgrass"
        #finding area based on position to find out what monsters to spawn
        if self.tilex < 70 or self.tiley < 45:
            self.area = 3
        elif self.tiley > 95 and self.tiley < 130:
            self.area = 2
        else:
            self.area = 1
        self.image = pygame.Surface((tilexspan * 32, tileyspan * 32))
        self.image.fill((255, 255, 255))

    def encounter(self, player,difficulty): #return random chance of going into a battle, only is called on 32nd movement frame (once per every tile you move)
        from battle import battle
        import random
        if player.tilex >= self.tilex and player.tilex <= self.tilex + self.tilexspan - 1 and player.tiley >= self.tiley and player.tiley <= self.tiley + self.tileyspan - 1 and player.movementframe == 32:
            if random.randint(0, 10) == 1:
                return battle(player, self.area,difficulty)
        return 0

    def update(self, player):  # use for bug testing
        self.posx = int(608 - (player.tilex - self.tilex) * 32 + player.displacedx - 16)
        self.posy = int(480 - (player.tiley - self.tiley) * 32 + player.displacedy - 16)
        self.rect = pygame.Rect(self.posx, self.posy, self.tilexspan * 32, self.tileyspan * 32)


class background(pygame.sprite.Sprite): #class because we have multiple backgrounds to display
    def __init__(self, image1,image2, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load(image1).convert_alpha()
        self.image2 = pygame.image.load(image2).convert_alpha() #2 layers for overlap (tops of trees/houses etc)
        self.posx = posx
        self.posy = posy
        self.rect = self.image1.get_rect(topleft=(self.posx + 16, self.posy + 16))

    def update(self):
        self.rect = self.image1.get_rect(topleft=(self.posx + 16, self.posy + 16))


class selectionbutton(pygame.sprite.Sprite): #used in battle for selecting weapon/defence, also attack and defend buttons
    def __init__(self, posx, posy, item, type):
        self.item = item
        pygame.sprite.Sprite.__init__(self)
        self.originalimage = pygame.image.load(item.imagestr).convert_alpha()
        self.originalimage = pygame.transform.scale(self.originalimage,(64,64))
        self.imagesizex = self.originalimage.get_width()
        self.imagesizey = self.originalimage.get_height()
        self.posx = posx
        self.posy = posy
        self.selected = 0
        self.hovering = 0
        self.size = 1
        self.frameimage = pygame.Surface((288, 128))
        self.frameimage.fill((255, 255, 255)) 
        self.framerect = self.frameimage.get_rect(center=(self.posx, self.posy))

        self.bgcolours = [(0, 0, 0), (9, 176, 70)]
        self.bg = pygame.Surface((320, 86))
        self.bg.fill((0, 0, 0))
        if type == 0:
            self.text = item.name
        else:
            self.text = type

    def place(self, screen):
        self.image = pygame.transform.scale(self.originalimage,
                                            (self.imagesizex * self.size, self.imagesizey * self.size))
        printfont = pygame.font.Font('minecraft_font.ttf', round(20 * self.size))
        self.printtext = printfont.render(self.text, False, (255, 255, 255))
        self.frameimage = pygame.Surface((round(320 * self.size), round(96 * self.size)))
        self.frameimage.fill((255, 255, 255))
        self.framerect = self.frameimage.get_rect(center=(self.posx, self.posy))
        self.bg = pygame.Surface((round(310 * self.size), round(86 * self.size)))
        self.bg.fill(self.bgcolours[self.selected])

        screen.blit(self.frameimage, self.framerect)
        screen.blit(self.bg, (self.posx - (self.bg.get_width() / 2), self.posy - (self.bg.get_height() / 2)))
        screen.blit(self.image,
                    (self.posx - self.image.get_width() / 2 - 105 * self.size, self.posy - self.image.get_height() / 2))
        screen.blit(self.printtext,
                    (self.posx - self.printtext.get_width() / 2 + 10 * self.size, self.posy - self.printtext.get_height() / 2))

    def jiggle(self):
        if self.framerect.collidepoint(pygame.mouse.get_pos()):
            self.size = 1.1
        else:
            self.size = 1

    def checkpressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.framerect.collidepoint(event.pos):
            return True
        return False


class textbutton(pygame.sprite.Sprite): #generic button for displaying text (used for answers in questions)
    def __init__(self, text, posx, posy):
        self.size = 1
        pygame.sprite.Sprite.__init__(self)
        self.printfont = pygame.font.SysFont('minecraft_font.ttf', 25)
        self.text = text
        self.posx = posx
        self.posy = posy
        printfont = pygame.font.Font('minecraft_font.ttf', round(15 * self.size))
        self.rect = printfont.render(self.text, False, (255, 255, 255)).get_rect(center=(posx, posy))
        self.frameimage = pygame.Surface((self.rect.width + 42, self.rect.height + 16))
        self.colour = (255,255,255)
        self.frameimage.fill(self.colour)
        self.framerect = self.frameimage.get_rect(center=(self.posx, self.posy))
        self.bg = pygame.Surface((self.rect.width + 32, self.rect.height))
        self.bg.fill((0, 0, 0))

    def jiggle(self):
        self.frameimage.fill(self.colour)
        if self.framerect.collidepoint(pygame.mouse.get_pos()):
            self.size = 1.1
        else:
            self.size = 1

    def checkpressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.framerect.collidepoint(event.pos):
            return True
        return False

    def place(self, screen):
        printfont = pygame.font.Font('minecraft_font.ttf', round(15 * self.size))
        self.printtext = printfont.render(self.text, False, (255, 255, 255))
        self.frameimage = pygame.Surface(
            (round(self.rect.width + 36 * self.size), round(self.rect.height + 14 * self.size)))
        self.frameimage.fill((255, 255, 255))
        self.framerect = self.frameimage.get_rect(center=(self.posx, self.posy))
        self.bg = pygame.Surface((round(self.rect.width + 32 * self.size), round(self.rect.height + 10 * self.size)))
        self.bg.fill((0, 0, 0))

        screen.blit(self.frameimage, self.framerect)
        screen.blit(self.bg, (self.posx - (self.bg.get_width() / 2), self.posy - (self.bg.get_height() / 2)))
        screen.blit(self.printtext, (
        self.posx - self.printtext.get_width() / 2 * self.size, self.posy - self.printtext.get_height() / 2))


class question(pygame.sprite.Sprite):
    def __init__(self, difficulty, posx, posy):
        self.posx = posx
        self.posy = posy
        with open("questions.txt", "r") as file:
            allquestions = file.read().split("\n-\n")
            selecteddiff = allquestions[difficulty].split("\n")
            self.question = selecteddiff[random.randint(0, len(selecteddiff) - 1)].split("|")
        self.attackboximg = pygame.image.load("graphics/attackbox.png")
        self.attackboxrect = self.attackboximg.get_rect(center=(posx, posy))
        printfont = pygame.font.Font("minecraft_font.ttf", 20)

        temptexts = [self.question[0][x-65:x]  for x in [65*y for y in range(1,10)] if len(self.question[0])>(x-65)]
        self.questiontexts = [printfont.render(temptexts[text], True, (255, 255, 255)) for text in range(len(temptexts))]

        if len(self.question) > 2:
            self.answertexts = [x for x in self.question[1:]]
            self.answertexts[-1] = self.answertexts[-1].split(":")[0]
            self.answers = [textbutton(self.answertexts[x], 616, 706 + x * 36) for x in range(len(self.answertexts))]
            self.answergroup = pygame.sprite.Group()
            for x in self.answers:
                self.answergroup.add(x)
        self.correct = self.question[-1].split(":")[1]

    def update(self, screen, event):
        if len(self.question) > 2:
            self.response = "2.2'3;.4'fmv#$#$@#$"
            for x in range(len(self.answers)):
                self.answers[x].jiggle()
                if self.answers[x].checkpressed(event) == True:
                    self.response = str(x)
            if self.response == self.correct:
                returnvalue = True
            elif self.response == "2.2'3;.4'fmv#$#$@#$":
                returnvalue = "unanswered"
            else:
                returnvalue = False
            return returnvalue

    def place(self, screen):
        # screen.blit(self.attackboximg,self.attackboxrect)
        try:
            for x in self.answergroup:
                x.place(screen)
            for text in range(len(self.questiontexts)):
                screen.blit(self.questiontexts[text], (616 - self.questiontexts[text].get_width() / 2, 600+text*25))
        except:
            pass

class inventoryItem(pygame.sprite.Sprite): #items displayed in inventory
    def __init__(self,item,posx,posy,quantity):
        self.quantity = quantity
        self.posx = posx
        self.posy = posy
        self.item = item
        self.itemimage = pygame.image.load(item.imagestr).convert_alpha()
        self.itemimage = pygame.transform.scale(self.itemimage,(64,64))
        printfont = pygame.font.Font('minecraft_font.ttf', 15)
        self.itemtext = printfont.render(item.name + " x" + str(self.quantity),False,(255,255,255))
        self.frame = pygame.Surface((128,128))
        self.frame.fill((0,0,0))
        self.rect = self.frame.get_rect(center=(self.posx,self.posy))
        self.colour = (0,0,0)
        self.selected = 0
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()): #hovering has priority over selected
            self.colour = (143,143,143)
        elif self.selected == 1:
            self.colour = (100,100,100)
        else:
            self.colour = (0,0,0)
    def checkpressed(self,event):
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
            return self.item
        return 0
    def print(self,screen):
        self.frame.fill(self.colour)
        screen.blit(self.frame,self.rect)
        screen.blit(self.itemimage,(self.posx-self.itemimage.get_width()/2,self.posy))
        screen.blit(self.itemtext,(self.posx-self.itemtext.get_width()/2,self.posy-48))



class inventory(pygame.sprite.Sprite): #inventory (used in shop and when you click tab)
    def __init__(self,list1,posx,posy):
        pygame.sprite.Sprite.__init__(self)
        self.posx = posx
        self.posy = posy
        printfont = pygame.font.Font('minecraft_font.ttf', 15)
        self.bg = pygame.image.load("graphics/inventorybg.png").convert()
        self.rect = self.bg.get_rect(center=(self.posx,self.posy))
        inventoryitems = {"weapon":[],
                          "defence":[],
                          "drops":[]}
        for x in list1:
            for y in list1[x]:
                if not y in inventoryitems[x]:
                    inventoryitems[x].append(y)
        inventorycounts = {"weapon": [],
                          "defence": [],
                          "drops": []}
        for x in inventorycounts:
            inventorycounts[x] = [0 for y in range(len(inventoryitems[x]))]
        for x in list1:
            for z in list1[x]:
                for y in range(len(inventoryitems[x])):
                    if z.name==inventoryitems[x][y].name:
                        inventorycounts[x][y]+=1
        self.weapontitle = printfont.render('WEAPONS:',False,(255,255,255)) #titles for items
        self.weaponitems = [inventoryItem(inventoryitems["weapon"][x],x*164+192,200,inventorycounts["weapon"][x]) for x in range(len(inventoryitems["weapon"]))]
        self.defencetitle = printfont.render('DEFENCE:',False,(255,255,255))
        self.defenceitems = [inventoryItem(inventoryitems["defence"][x],x*164+192,400,inventorycounts["defence"][x]) for x in range(len(inventoryitems["defence"]))]
        self.dropstitle = printfont.render('DROPS:',False,(255,255,255))
      #  for x in range(len(inventoryitems["drops"])):
       #     if 
       #     self.dropsitems.append(inventoryItem(inventoryitems["drops"][x],x*164+192,600,inventorycounts["drops"][x]))
        self.dropsitems = [inventoryItem(inventoryitems["drops"][x],x*164+192,600,inventorycounts["drops"][x]) if x<=5 else inventoryItem(inventoryitems["drops"][x],(x-6)*164+192,750,inventorycounts["drops"][x]) for x in range(len(inventoryitems["drops"]))]
        self.allitems = self.weaponitems + self.defenceitems + self.dropsitems
    def update(self): #updates whether or not youre hovering over items
        for y in self.weaponitems:
            y.update()
        for y in self.defenceitems:
            y.update()
        for y in self.dropsitems:
            y.update()
    def checkpressed(self,event): #check if an item is selected
        for y in self.weaponitems:
            i = y.checkpressed(event)
            if i!=0:
                for x in self.allitems:

                    if x!=y:
                        x.selected=0
                y.selected = (y.selected+1)%2
                return i
        for y in self.defenceitems:
            i = y.checkpressed(event)
            if i!=0:
                for x in self.allitems:
                    if x!=y:
                        x.selected=0
                y.selected = (y.selected+1)%2
                return i
        for y in self.dropsitems:
            i = y.checkpressed(event)
            if i!=0:
                for x in self.allitems:
                    if x!=y:
                        x.selected=0
                y.selected = (y.selected+1)%2
                return i
        return False
    def print(self,screen): #blitting to screen
        screen.blit(self.bg,self.rect)
        screen.blit(self.weapontitle,(self.posx-self.weapontitle.get_width()/2, 100))
        screen.blit(self.defencetitle,(self.posx-self.defencetitle.get_width()/2, 300))
        screen.blit(self.dropstitle,(self.posx-self.dropstitle.get_width()/2, 500))
        for y in self.weaponitems:
            y.print(screen)
        for y in self.defenceitems:
            y.print(screen)
        for y in self.dropsitems:
            y.print(screen)

class shop(pygame.sprite.Sprite): #shop
    def __init__(self,player): #declarations
        from items import shopitems
        self.shopitems = shopitems
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.inventory1 = inventory(self.player.inventory, 608, 480)
        self.shop = inventory(self.shopitems,608,480)
        self.selectedmenu = self.shop
        self.shopbutton = textbutton("SHOP",128,96)
        self.inventorybutton = textbutton("INVENTORY",256,96)
        self.buybutton = textbutton("BUY",900,96)
        self.sellbutton = textbutton("SELL",1000,96)
        self.printfont = pygame.font.Font("minecraft_font.ttf",20)
        self.errortext = self.printfont.render("",False,(255,0,0))
        self.goldtext = self.printfont.render("gold: " + str(player.gold),False,(255,255,255))
        self.selecteditem = False
    def update(self):
        self.selectedmenu.update() #checks for buttons being hovered over
        for x in [self.shopbutton,self.inventorybutton,self.buybutton,self.sellbutton]:
            x.jiggle() #makes the button bigger
    def checkpressed(self,event):
        i = self.selectedmenu.checkpressed(event)
        if self.selecteditem == False or (i!=False and self.selecteditem!=i):
            self.selecteditem = i
        elif self.selecteditem == i:
            self.selecteditem = False
        if self.selecteditem!=False: #if item selected, show the cost and sell values
            self.iteminfo1 = self.printfont.render("cost: " + str(self.selecteditem.cost), False, (255, 255, 255))
            self.iteminfo2 = self.printfont.render("sell value:" + str(self.selecteditem.cost/2),False,(255,255,255))
        else:
            self.iteminfo1 = self.printfont.render("",False,(255,255,255))
            self.iteminfo2 = self.printfont.render("",False,(255,255,255))
        if self.shopbutton.checkpressed(event) == True:
            try:
                for x in self.inventory1.allitems:
                    x.selected = 0
                self.selecteditem.selected = 0
                self.selecteditem = False
            except:
                pass
            self.errortext = self.printfont.render("",False,(255,0,0))
            self.selectedmenu = self.shop
        if self.inventorybutton.checkpressed(event) == True:
            try:
                for x in self.shop.allitems:
                    x.selected = 0
                self.selecteditem.selected = 0
                self.selecteditem = False
            except:
                pass
            self.errortext = self.printfont.render("",False,(255,0,0))
            self.selectedmenu = self.inventory1
        if self.buybutton.checkpressed(event) == True:
            self.errortext = self.printfont.render("",False,(255,0,0))
            if self.selecteditem in self.player.inventory["weapon"] + self.player.inventory["defence"]:
                self.errortext = self.printfont.render("you already own this item",False,(255,0,0)) #if you own item
            else:
                if self.selecteditem!=0: #else buy it if you have enough gold
                    if self.selecteditem.cost<=self.player.gold:
                        self.selecteditem.buy(self.player)
                        self.selecteditem.selected = 0
                        self.selecteditem = False
                        self.shop = inventory(self.shopitems, 608, 480)
                        self.inventory1 = inventory(self.player.inventory, 608, 480)
                        self.selectedmenu = self.shop
                    else:
                        self.errortext = self.printfont.render("insufficient gold", False, (255, 0, 0))
                else:
                    self.errortext = self.printfont.render("no item selected", False, (255, 0, 0))
        if self.sellbutton.checkpressed(event) == True:
            self.errortext = self.printfont.render("",False,(255,0,0))
            if self.selecteditem!=False:
                if self.selecteditem.itemtype == "weapon" and len(self.player.inventory["weapon"])==1:
                    self.errortext = self.printfont.render("you need one weapon", False, (255, 0, 0)) #cannot sell all weapons
                else:
                    self.selecteditem.sell(self.player)
                    self.selecteditem.selected = 0
                    self.selecteditem = False #selling item back to shop
                    self.shop = inventory(self.shopitems, 608, 480)
                    self.inventory1 = inventory(self.player.inventory, 608, 480)
                    self.selectedmenu = self.inventory1
            else:
                self.errortext = self.printfont.render("no item selected", False, (255, 0, 0))
    def print(self,screen): #blitting shop buttons and textures to screen
        self.selectedmenu.print(screen)
        self.shopbutton.place(screen)
        if self.selectedmenu == self.shop:
            self.buybutton.place(screen)
            self.shopbutton.colour=(100,100,100)
            self.buybutton.colour = (255, 255, 255)
        else:
            self.shopbutton.colour = (255, 255, 255)
            self.buybutton.colour = (100, 100, 100)
            self.sellbutton.place(screen)
        self.goldtext = self.printfont.render("gold: " + str(self.player.gold), False, (255, 255, 255))
        screen.blit(self.errortext,(250, 850))
        screen.blit(self.goldtext, (100, 850))
        screen.blit(self.iteminfo1, (700, 850))
        screen.blit(self.iteminfo2, (900, 850))
        self.inventorybutton.place(screen)

class questinfo(pygame.sprite.Sprite): #quest information, little box in top left that shows progress
    def __init__(self,player,position,npc,file):
        from quests import questupdate
        self.questlist = questupdate(player,npc,file,"questlist") #declarations
        pygame.sprite.Sprite.__init__(self)
        self.file = file
        self.printfont = pygame.font.Font('minecraft_font.ttf', 25)
        self.position = position
        self.type = self.printfont.render(npc.name,False,(9, 204, 6))
        self.player = player
        self.npc = npc #allows other npcs to potentially give quests even though only the questmaster does
        if self.questlist[player.currentquest].currentvalue >= self.questlist[self.player.currentquest].totalvalue:
            self.status = self.printfont.render("Complete!",False,(9, 204, 6))
        else:
            self.status = self.printfont.render("%i/%i"%(int(self.questlist[player.currentquest].currentvalue),int(self.questlist[self.player.currentquest].totalvalue)),False,(255,255,255))
        self.queststr = self.printfont.render(self.questlist[player.currentquest].string,False,(255,255,255))
        self.bg = pygame.image.load("graphics/questframe.png").convert()
    def update(self,screen,player): #change values
        from quests import questupdate
        self.player = player
        self.questlist = questupdate(self.player,self.npc,self.file,"questlist")
        self.queststr = self.printfont.render(self.questlist[player.currentquest].string,False,(255,255,255))
        if self.questlist[self.player.currentquest].currentvalue >= self.questlist[self.player.currentquest].totalvalue:
            self.status = self.printfont.render("Complete!",False,(9, 204, 6)) # if the quest progress is complete, show a green "Complete!"
        else:                                                                  # otherwise displays the current quest progress
            self.status = self.printfont.render("%i/%i"%(int(self.questlist[self.player.currentquest].currentvalue),int(self.questlist[self.player.currentquest].totalvalue)),False,(255,255,255))
        screen.blit(self.bg,(32,32+(164*(self.position-1))))
        screen.blit(self.type,(32+386/2-self.type.get_width()/2,40+(164*(self.position-1))))
        screen.blit(self.queststr,(32+386/2-self.queststr.get_width()/2,40+self.type.get_height()+16+(164*(self.position-1))))
        screen.blit(self.status,(32+386/2-self.status.get_width()/2,40+self.queststr.get_height()*2+16+(164*(self.position-1))))
