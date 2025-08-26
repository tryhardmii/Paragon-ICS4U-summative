import pygame
#from movement import movement
pygame.init() #battle function to return all drops and player hp changes and if you die or not
def confirm():
    return 0
def battle(player,area,difficulty):
    import random
    from monsters import monsterlist
    from sprites import buttons, selectionbutton, question
    pygame.mixer.init()
    #from items import weaponlist,defencelist
    screen = pygame.display.set_mode((1216, 960))
    for x in monsterlist:
        for y in x:
            y.HP = y.maxHP
    area -= 1
    difficulty -=1
    spawnchances = [[] for x in range(len(monsterlist[area]))] #random monster based on spawnrate
    num = 0
    listnum = 0
    while listnum<len(monsterlist[area]):
        print(num,listnum,spawnchances)
        for x in range(monsterlist[area][listnum].spawnrate):
            spawnchances[listnum].append(x+num)
        print(num,listnum,spawnchances)
        num = spawnchances[listnum][-1]+1
        listnum+=1
    randomnum = random.randint(0,spawnchances[-1][-1])
    print(spawnchances)
    for listnum in range(len(spawnchances)):
        if randomnum in spawnchances[listnum]:
            selectedmonster = monsterlist[area][listnum]
    selectionscreen = 1
    battlebackground = [pygame.image.load("graphics/battlegraphics/area1battle.png").convert(),pygame.image.load("graphics/battlegraphics/area2battle.png").convert(),pygame.image.load("graphics/battlegraphics/area3battle.png").convert(),pygame.image.load("graphics/battlegraphics/area4battle.png").convert()]
    weaponbuttons = pygame.sprite.Group()
    defencebuttons = pygame.sprite.Group()
    weaponbuttonstemp = [selectionbutton(200,560-len(player.inventory["weapon"])/2*150+150*num,player.inventory["weapon"][num],0) for num in range(len(player.inventory["weapon"]))]
    for weapon in weaponbuttonstemp:
        weaponbuttons.add(weapon)
    defencebuttonstemp = [selectionbutton(600,560-len(player.inventory["defence"])/2*150+150*num,player.inventory["defence"][num],0) for num in range(len(player.inventory["defence"]))]
    for defence in defencebuttonstemp:
        defencebuttons.add(defence)
    confirmbutton = buttons(1000,480,"graphics/confirmbutton.png", confirm)
    HPframe = pygame.image.load("graphics/HPframe.png").convert()
    printfont = pygame.font.Font("minecraft_font.ttf",25)
    game_active = True
    #pygame.mixer.music.stop()
    pygame.mixer.music.load('music/pokemon_battle_music.mp3')
    pygame.mixer.music.play(loops=-1)
    while selectionscreen == 1:
        for event in pygame.event.get():
            if event.type == pygame.quit:
                selectionscreen = False
                game_active = False
            confirmbutton.jiggle()
            if confirmbutton.checkpressed(event) == True:
                selectedweapon = 0
                selecteddefence = 0
                for weapon in weaponbuttons:
                    if weapon.selected==1:
                        selectedweapon = weapon.item
                for defence in defencebuttons:
                    if defence.selected==1:
                        selecteddefence = defence.item
                if player.inventory["defence"] == []:
                    selecteddefence = "nodefence"
                if selectedweapon != 0 and selecteddefence != 0:
                    selectionscreen = 0
                else:
                    confirmbutton.original_image=pygame.image.load("graphics/confirmred.png").convert()
            for group in [weaponbuttons,defencebuttons]:
                for item in group:
                    item.jiggle()
                    item.checkpressed(event)
                    if item.checkpressed(event) == True:
                        for item1 in group:
                            if item1!=item:
                                item1.selected = 0
                            else:
                                item1.selected = 1
        screen.blit(battlebackground[area],(0,0))
        for weapon in weaponbuttons:
            weapon.place(screen)
        for defence in defencebuttons:
            defence.place(screen)
        screen.blit(confirmbutton.image,confirmbutton.rect)
        pygame.display.update()
        pygame.time.Clock().tick(60)
    if game_active == False:
        pygame.quit()
    addedstatus = 0
    attackboximg = pygame.image.load("graphics/attackbox.png")
    attackboxrect = attackboximg.get_rect(center=(616, 544))
    
    screen.blit(battlebackground[area],(0,0))
    animationframe = 0
    while animationframe<90 and game_active == True:
        for event in pygame.event.get():
            if event.type == pygame.quit:
                game_active = False
        selectedmonster.posy = (100*animationframe)**0.6
        selectedmonster.move(0,0)

        attackboxrect = attackboximg.get_rect(center=(616, 960-(animationframe*512)**0.5))
        screen.blit(battlebackground[area],(0,0))
        screen.blit(selectedmonster.image,selectedmonster.rect)
        screen.blit(attackboximg,attackboxrect)

        animationframe += 1
        pygame.display.update()
        pygame.time.Clock().tick(60)
        
        stage = 1
        changestage = 1
    exit_down = 0
    
    while game_active==True:
        if stage==5:
            infotext = printfont.render("%s dealt %i damage to the player!"%(selectedmonster.name,takendamage),True,(255,255,255))
            stage=1
        if stage == 3 and changestage==1 and selecteddefence == "nodefence":
            stage = 1
            infotext = printfont.render("Player dealt %i damage to %s, and it dealt %i damage to the player!"%(dealtdamage,selectedmonster.name,takendamage),True,(255,255,255))
        if stage == 1 and changestage==1:
            question1 = selectionbutton(616, 745,selectedweapon,"ATTACK")
            changestage = 0
        elif stage == 3 and changestage==1:
            infotext = printfont.render("Player dealt %i damage to %s"%(dealtdamage,selectedmonster.name),True,(255,255,255))
            question1 = selectionbutton(616, 745,selecteddefence,"DEFEND")
            changestage = 0
        elif (stage == 2 or stage == 4) and changestage==1:
            infotext = printfont.render("",True,(255,255,255))
            takendamage = 0
            question1 = question(difficulty, 616, 745)
            changestage = 0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and stage>5:
                exit_down = 1
            if event.type == pygame.MOUSEBUTTONUP and exit_down == 1:
                game_active = False
            if event.type == pygame.quit:
                game_active = False
            if (stage == 1 or stage == 3) and changestage==0:
                question1.jiggle()
                if question1.checkpressed(event) == True:
                    stage+=1
                    changestage = 1
            elif changestage==0:
                i = question1.update(screen,event)
                if i != "unanswered":
                    if i==True:
                        if stage==2:
                            dealtdamage = selectedweapon.damage
                            selectedmonster.HP -= selectedweapon.damage
                            if selectedmonster.HP<=0:
                                stage = 6
                                del question1
                            if selecteddefence == "nodefence":
                                takendamage = selectedmonster.damage
                                player.HP -= takendamage
                                if player.HP <= 0:
                                    print("dead")
                                    stage = 7
                        if stage==4:
  
                            if selecteddefence == "nodefence":
                                takendamage = selectedmonster.damage
                            else:
                                takendamage = selectedmonster.damage*(1-selecteddefence.blockpercentage)
                            player.HP -= round(takendamage,1)
                            if player.HP<=0:
                                print("dead")
                                stage = 7
                                del question1
                        stage+=1
                        changestage = 1
                    else:
                        if stage==2: #after player attack
                            dealtdamage = 0
                            if selecteddefence == "nodefence":
                                takendamage = selectedmonster.damage
                                player.HP -= takendamage
                                if player.HP <= 0:
                                    print("dead")
                                    stage = 7
                        if stage==4: #after player defence
                            takendamage = selectedmonster.damage
                            player.HP -= takendamage
                            if player.HP<=0:
                                print("dead")
                                stage = 7
                        stage+=1
                        changestage = 1
        playerHPtext = printfont.render("Player HP: " + str(player.HP), True, (255, 255, 255))
        monsterHPtext = printfont.render("Monster HP: " + str(selectedmonster.HP), True, (255, 255, 255))

        
        
        screen.blit(battlebackground[area],(0,0))
        screen.blit(selectedmonster.image,selectedmonster.rect)
        screen.blit(HPframe,(32,32))
        screen.blit(playerHPtext,(48,48))
        screen.blit(monsterHPtext,(48,80))
        screen.blit(attackboximg,attackboxrect)
        try:
            screen.blit(infotext,(608-infotext.get_width()/2,576))
        except:
            pass
        if stage<6:
            question1.place(screen)
        else:
            if stage==7: #monster died
                infotext = printfont.render("Player dealt %i damage to %s, it is now dead!"%(dealtdamage,selectedmonster.name),True,(255,255,255))
                resulttext = printfont.render("%s was added to the player's inventory"%(selectedmonster.dropstring),True,(255,255,255))
                if addedstatus != 1:
                    for x in selectedmonster.drops:
                        player.inventory["drops"].append(x)
                    addedstatus=1
                defeated = True
                deadcheck = False
            elif stage == 8:#player died
                infotext = printfont.render("%s dealt %i damage to the player, the player is now dead!"%(selectedmonster.name,takendamage),True,(255,255,255))
                resulttext = printfont.render("Player is transported to the lobby...",True,(255,255,255))
                deadcheck = True
                defeated = False
            screen.blit(resulttext,(608-resulttext.get_width()/2,608))
            clicktext = printfont.render("Click anywhere to continue", True, (255, 255, 255))
            screen.blit(clicktext,(608-clicktext.get_width()/2,640))

        pygame.display.update()
        pygame.time.Clock().tick(60)
    if game_active == False:
        if defeated == True:
            player.mobsdefeated[selectedmonster.name] += 1
        pygame.mixer.music.stop()
        return [player,deadcheck]
        pygame.quit()
