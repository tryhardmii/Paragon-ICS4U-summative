import pygame
from battle import battle
from sprites import chest, obstacle, tallgrass, buttons

pygame.init() #main file with the bulk of the code

pygame.mixer.init()
def movement():
    import json
    from sprites import player, npc, background, door, inventory, shop, questinfo, buttons
    from objects import objectgroup, watergroup, grassgroup, doorgroup, lobbygroup, housegroup, bossgroup, doorlist
    from quests import questupdate
    from items import item, weapon
    from monsters import drops
    import random #a
    blockmovement = False
    #global player
    def wincontinue(): #used for when you win
        return "continue"
    def save(): #esc menu
        return "save"
    def quit():#quit
        pygame.quit()
    def controls():
        return "controls"
    game_active = True
    validmovement = True
    screen = pygame.display.set_mode((1216, 960))  # 100,181

    nomobsdefeated = { #mobsdefeated has to be declared here and not in the sprite class so that we can load non-empty mobsdefeated dicts
            #area1monsters
            "ghost": 0,
            "goblin": 0,
            "loser": 0,
            "skeleton": 0,
            #area2monsters
            "crab": 0,
            "frog": 0,
            "redspider": 0,
            "rock": 0,
            #area3monsters
            "circle": 0,
            "iceghost": 0,
            "Creep": 0,
            "skeleton2": 0,

            #questthings
            "npctalk": 0,
            "chestsopened": 0,
            "area2": 0,
            "area3":0,
            "startboss":0,
            "win":0,
            "manfound": 0,
            "womanfound": 0,
            "bossdefeated": 0,
            "wizard":0
        }
    noinventory = {"weapon": [], #same as nomobsdefeated
                    "defence": [],
                    "drops": []}
    with open("playerdata.json","r") as file: #loading data from json file
        jsonfile = json.load(file) #dont need a try-except because to enter def movement you need difficulty
        if "playerinfo" in jsonfile:
            player1 = player.from_dict(jsonfile["playerinfo"])
        else:
            player1 = player(100, 20, 0, 16, 16,0,nomobsdefeated,noinventory,0)
        difficulty = jsonfile["otherinfo"]["difficulty"]
        if "backgroundkey" in jsonfile["otherinfo"]:
            backgroundkey = jsonfile["otherinfo"]["backgroundkey"]
        else:
            backgroundkey = "lobby"

    area2barrier = obstacle(167,130,5,1)
    area3barrier = obstacle(72, 48, 1, 9)
    #bossbarrier = obstacle(5344, 4160, 160, 32)
    objectgroup.add(area2barrier)
    objectgroup.add(area3barrier)
    #npc declarations
    robert = npc("robert",["Answering questions right is the best way to do a lot of damage"], 12, 16,"random","graphics/npcs/npc1.png")
    robert1 = npc("robert1", ["Do quests to get gold, which can be used to buy items at the shopkeeper."],11, 5,"random","graphics/npcs/npc2.png")
    robert2 = npc("robert2",["There are 3 areas in the game, each one increasing in difficulty"], 10, 10,"random","graphics/npcs/npc3.png")
    robert3 = npc("robert3",["As you go farther, the monsters get harder"], 10, 12,"random","graphics/npcs/npc4.png")
    robert4 = npc("robert4",["There's a shady wizard around here", "I wouldn't trust him if I were you."], 9, 23,"shop","graphics/npcs/shopnpc.png")
    robert5 = npc("robert5", ["Here's a wooden sword.", "Wooden Sword was added to your inventory!"], 20, 16, "not random","graphics/npcs/npc5.png")
    oldwoman = npc("oldwoman", ["I need help..."], 14, 16,"not random","graphics/npcs/oldwoman.png")
    oldman = npc("oldman", ["I miss my wife...","I wonder where I am?"], 20, 16,
                  "random",["graphics/npcs/oldman/oldmandown1.png",
    "graphics/npcs/oldman/oldmanright.png",
    "graphics/npcs/oldman/oldmanleft.png",
    "graphics/npcs/oldman/oldmanup.png"]) #oldman is the only one that needs animations bc its the only that follows
    doctor = npc("doctor",["Hey there, do you need healing?","ok here goes...",".",".",".","okay, you're good to go!"],23,23,"not random","graphics/npcs/doctor.png")
    #chest declarations
    chest1 = chest("chest1", 175, 178)
    chest2 = chest("chest1", 140, 150)
    chest3 = chest("chest1", 127, 94)
    areanpc = pygame.sprite.Group()
    areanpc.add(chest1)
    areanpc.add(chest2)
    areanpc.add(chest3)
    questmaster = npc("questmaster",["Hello and welcome to paragon!", "This is the lobby", "Complete quests from me to earn gold and rewards!","For your first quest, get to know the people in the lobby more! Talk to 5 people around the lobby."], 20, 20,"not random","graphics/npcs/questmaster.png")
    lobbynpc = pygame.sprite.Group()
    lobbynpc.add(questmaster)
    questmaster = questupdate(player1,questmaster,"questmasterdialogue.txt","dialoguestart")
    lobbynpc.add(robert)
    lobbynpc.add(robert1)
    lobbynpc.add(robert2)
    lobbynpc.add(robert3) #adding npcs to sprite groups
    lobbynpc.add(robert4)
    lobbynpc.add(robert5)
    lobbynpc.add(doctor)
    wizard = npc("wizard",["You're not allowed to go there yet.","You're not strong enough.","Don't ask who I am, that's not important."], 169, 132,"not random","graphics/npcs/wizard.png")
    wizardnpc = pygame.sprite.Group()
    wizardnpc.add(wizard)
    npcdialogue = ["What's up!",
                "I wouldn't trust the wizard if I were you...", #random voicelines for miscellaneous npcs
                "Heard you can change the difficulty of the questions in the menu",
                "Three men walk into a bar. The fourth ducks.",
                "I really like math!", "The word of the day is: supercalifragilisticexpialidocious. Extraordinarily good, wonderful",
                "My favourite word is 'sigma'!", "get out GET OUT GET OUT GET OUT GET OUT GET OUT GET OUT AHHHHHHHHHHHH",
                "Never back down never what? NEVER GIVE UP!!! Never back down never what? NEVER GIVE UP!!! Never back down never what? NEVER GIVE UP!!! Never back down never what? NEVER GIVE UP!!! Never back down never what? NEVER GIVE UP!!!"]
    housenpc1 = npc("housenpc1", npcdialogue, 15, 13, "random", "graphics/npcs/housenpcs/Male 10-1.png")
    housenpc2 = npc("housenpc2", npcdialogue, 16, 13, "random", "graphics/npcs/housenpcs/Female 01-3.png")
    housenpc3 = npc("housenpc3", npcdialogue, 17, 13, "random", "graphics/npcs/housenpcs/Male 10-2.png")
    housenpc4 = npc("housenpc4", npcdialogue, 13, 14, "random", "graphics/npcs/housenpcs/Female 13-3.png")
    housenpc5 = npc("housenpc5", npcdialogue, 13, 15, "random", "graphics/npcs/housenpcs/Male 10-3.png")
    housenpc6 = npc("housenpc6", npcdialogue, 13, 16, "random", "graphics/npcs/housenpcs/Female 17-4.png")
    housenpc7 = npc("housenpc7", npcdialogue, 16, 16, "random", "graphics/npcs/housenpcs/Male 13-3.png")
    housenpc8 = npc("housenpc8", npcdialogue, 20, 16, "random", "graphics/npcs/housenpcs/Female 18-1.png")
    housenpc9 = npc("housenpc9", npcdialogue, 19, 16, "random", "graphics/npcs/housenpcs/Male 16-4.png")
    housenpc = pygame.sprite.Group()
    housenpcs = [[housenpc1], [housenpc2], [housenpc3], [oldwoman], [housenpc4], [housenpc5], [housenpc6], [housenpc7], [housenpc8], [housenpc9], [wizard], [oldman]]
    #declarations for miscellaneous house npcs
    areanpc.add(wizard)
    #testgrass = tallgrass(0, 0, 32, 32)
    #grassgroup.add(testgrass)
    npcs = {
        "area": areanpc,
        "lobby": lobbynpc,
        "house": housenpc,
        "boss": wizardnpc,
    } #part of why different npcs are shown in different areas.
    buttongroup = pygame.sprite.Group()
    savebutton = buttons(600, 400, 'menugraphics/save.png', save)
    endbutton = buttons(600, 400, 'graphics/winscreen.png', wincontinue)
    quitbutton = buttons(600, 800, 'menugraphics/quitbutton.png', quit)
    controlsbutton = buttons(600,600,'menugraphics/controlsbutton.png',controls)

    background = { #backgrounds by all areas
        "area": background('graphics/area1layer1.png', "graphics/area1layer2.png", 32, 32),
        "lobby": background('graphics/lobby.png', "graphics/blank.png", 32, 32),
        "house": background('graphics/house.png', "graphics/blank.png", 32, 32),
        "boss": background('graphics/bossfight.png', "graphics/blank.png", 32, 32)
    }
    #doors from lobby to area and house to area
    an = door(17, 2, 1, 1, "area")
    lobbydoor = pygame.sprite.Group()
    lobbydoor.add(an)
    ad = door(17, 17, 2, 1, "area")
    housedoor = pygame.sprite.Group()
    housedoor.add(ad)

    #movement keys
    velocities = {
        "": pygame.math.Vector2(0, 0),
        "w": pygame.math.Vector2(0, 1),
        "s": pygame.math.Vector2(0, -1),
        "a": pygame.math.Vector2(1, 0),
        "d": pygame.math.Vector2(-1, 0)
    } #HEnry was here
    keydict = {
        pygame.K_w: "w",
        pygame.K_a: "a",
        pygame.K_s: "s",
        pygame.K_d: "d"
    }
    #used for movement animations for the player
    movementanimations = {
        "w": 0,
        "s": 1,
        "a": 2,
        "d": 3
    }

    #more declarations
    velocity = pygame.math.Vector2(0, 0)
    printfont = pygame.font.Font('minecraft_font.ttf', 20)
    speed = 2
    movementkey = ""
    lastkeypressed = "w"
    dialogueskip = 0
    dialogueend = 0
    stalltimer = 0
    uppedkeys = []
    validmovement = True
    speedmultiplier = 1
    pressedkeys = []
    movementkeys = []
    interactingnpc = False
    lastvelocity = velocities[""]
    bossfight = False
    inventoryrequest = []
    questmaster_reset = 0
    wizard_reset = 0
    oldman_reset = 0
    boxrequest = 0
    questmasterinfo = 0
    if player1.currentquest>0:
        questmasterinfo = questinfo(player1, 1, questmaster,"questmasterdialogue.txt")
    wizardinfo = 0
    oldmaninfo = 0
    
    inventory1 = 0
    interactingdoor = 0
    a = 0
    exit1=False
    controls_view = False

    controls_image = pygame.image.load("menugraphics/TITLESCREEN.png").convert_alpha()
    while game_active == True and exit1==False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                exit1 = True
            if event.type == pygame.quit:
                exit1 = True
                game_active = False
        screen.blit(controls_image,(0,0))
        pygame.display.update()
        pygame.time.Clock().tick(60)
        #intro image
        pygame.display.update()
        pygame.time.Clock().tick(60)
    controls_image = pygame.image.load("menugraphics/TITLESCREEN-2.png").convert_alpha()
    pygame.mixer.music.load("music/PokemonEmeraldMusic.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)
    quest_sound = pygame.mixer.Sound("music/quest_completed.mp3")
    if game_active==False:
        pygame.quit()
    while game_active:
        #print(player1.tilex,player1.tiley)
        #print(player1.currentquest)
        interactingdoor = False
        interact_request = 0
        blockedkeys = []
        blockedkeys.extend(player1.checkcollide(npcs[backgroundkey]))
        if player1.currentquest == 6:
            if player1.tiley<100 and backgroundkey == "area":
                player1.mobsdefeated["area2"] = 1
        if player1.currentquest>5 and len(wizard.dialogue)==3:
            areanpc.remove(wizard)
            housenpcs[10] = [wizard]
            wizard.dialoguenum = 0
            wizard.dialogue = ["im so sad..."]
            wizard.tilex = 20
            wizard.tiley = 16
        if player1.currentquest == 12:
            if player1.tilex<73 and player1.tiley<100 and backgroundkey == "area":
                player1.mobsdefeated["area3"] = 1
        if player1.currentquest == 15 and len(wizard.dialogue)==1:
            wizard.dialoguenum = 0
            wizard.dialogue = ["I can't take it anymore. I will destroy everything in this world.", "Let the mundane tremble, let the ordinary cower in fear, for I am the sigma who shall bring about their downfall!"]
        if player1.currentquest == 7 and len(oldwoman.dialogue)==1:
            oldwoman.dialogue = ["Hello...","What's that? Why am I so sad?","You see, my husband went out for a walk yesterday and hasn't come back.","His memory isn't that good, so he probably forgot where he is.","Would you help me find him? I think he's a house in area 1"]
        if backgroundkey == "area":
            blockedkeys.extend(player1.checkcollide(objectgroup))
            blockedkeys.extend(player1.checkcollide(watergroup))
            blockedkeys.extend(player1.checkcollide(doorgroup))
        elif backgroundkey == "lobby":
            blockedkeys.extend(player1.checkcollide(lobbygroup))
            blockedkeys.extend(player1.checkcollide(lobbydoor))
        elif backgroundkey == "house":
            blockedkeys.extend(player1.checkcollide(housegroup))
            blockedkeys.extend(player1.checkcollide(housedoor))
        elif backgroundkey == "boss":
            blockedkeys.extend(player1.checkcollide(bossgroup))
            if bossfight == False:
                blockedkeys.extend(player1.checkcollide(lobbydoor))
        if player1.currentquest > 5 and area2barrier in objectgroup:
            objectgroup.remove(area2barrier)
        elif player1.currentquest > 11 and area3barrier in objectgroup:
            objectgroup.remove(area3barrier)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            if event.type == pygame.KEYDOWN:
                if event.key in keydict and blockmovement==False:
                    lastkeypressed = event.unicode.lower()
                    if not keydict[event.key] in blockedkeys:
                        validmovement = True
                        #movementkey = keydict[event.key]
                        movementkeys.append(keydict[event.key])
                if event.key == pygame.K_e:
                    try:
                        crashtest = inventory1.dropstitle
                        i=1
                    except:
                        i=0
                    if len(blockedkeys) > 0 and i==0:
                        if interactingnpc == 0 and boxrequest == 0:
                            if questmaster.dialoguenum == len(questupdate(player1,questmaster,"questmasterdialogue.txt","questdialogue")[player1.currentquest+1])-1:
                                try:
                                    if player1.interact(npcs[backgroundkey],lastkeypressed).name == "questmaster":
                                        i = questupdate(player1,questmaster,"questmasterdialogue.txt","player")
                                        if i!=0:
                                            pygame.mixer.music.pause()
                                            pygame.mixer.Sound.play(quest_sound)
                                            pygame.time.wait(2000)
                                            pygame.mixer.music.unpause()
                                            questmaster_reset = 0
                                            player1 = i
                                        questmasterinfo = questinfo(player1, 1, questmaster,"questmasterdialogue.txt")
                                except:
                                    pass
                            interact_request = 1
                        else:
                            i = False
                            try:
                                i1 = boxrequest==1
                                i = interactingnpc.dialoguetype == "random" or interactingnpc.dialoguetype == "not random"
                            except:
                                pass
                            if i1 == True or i == True:
                                if player1.dialogueterm == len(player1.selecteddialogue):
                                    dialogueend = 1
                                    boxrequest = 0
                                else:
                                    dialogueskip = 1
                            else:
                                blockmovement = False
                                inventory1 = 0
                                interactingnpc = 0
                if event.key == pygame.K_b:
                    speedmultiplier = 32
                if event.key == pygame.K_LSHIFT and player1.currentquest >= 3:
                    pressedkeys.append(event.key)
                if event.key == pygame.K_TAB:
                    try:
                        crashtest = inventory1.sellbutton #you cant open inventory while shop is open
                    except:
                        inventoryrequest = 1
                    if blockmovement == True:
                        blockmovement = False
                if event.key == pygame.K_5:
                    for x in player1.mobsdefeated:
                        player1.mobsdefeated[x] += 1
                    player1.inventory["drops"].append(drops[10])
                if event.key == pygame.K_ESCAPE:
                    if savebutton in buttongroup.sprites():
                        del errortext
                        blockmovement = False
                        controls_view = False
                        buttongroup = temp_buttongroup
                        inventory1 = temp_inventory
                    else:
                        errortext = printfont.render("", False, (255, 255, 255))
                        temp_buttongroup = buttongroup.copy()
                        temp_inventory = inventory1
                        blockmovement = True
                        for x in buttongroup:
                            buttongroup.remove(x)
                        inventory1 = 0
                        buttongroup.add(savebutton)
                        buttongroup.add(quitbutton)
                        buttongroup.add(controlsbutton)
            if event.type == pygame.KEYUP:
                if event.key in keydict and keydict[event.key] in movementkeys:
                    uppedkeys.append(keydict[event.key])
                    movementkeys.remove(keydict[event.key])
                    if len(movementkeys)>0:
                        lastkeypresed = movementkeys[0]
                for x in movementkeys:
                    try:
                        if x == keydict[event.key]:
                            movementkeys.remove(x)
                    except:
                        pass
                if event.key == pygame.K_LSHIFT:
                    try:
                        pressedkeys.remove(event.key)
                    except:
                        pass
            for button in buttongroup:
                button.jiggle()
                i = button.checkpressed(event)
                if i=="continue":
                    player1.currentquest+=1
                    questmaster = questupdate(player1,questmaster,"questmasterdialogue.txt","dialogue")
                    questmasterinfo = 0
                    buttongroup.remove(quitbutton)
                    buttongroup.remove(endbutton)
                    bossfight = False
                elif i=="save":
                    if backgroundkey=="house":
                        errortext = printfont.render("You cannot save inside houses", False, (255, 0, 0))
                    else:
                        inventorydict = {"weapon":[],
                                        "defence":[],
                                        "drops":[]}
                        templist = player1.inventory
                        for x in player1.inventory:
                            for y in player1.inventory[x]:
                                inventorydict[x].append(y.convert_dict())
                        player1.inventory = inventorydict
                        playerinfo = player1.convert_dict()
                        otherinfo = {"difficulty":difficulty,
                                    "backgroundkey":backgroundkey}
                        all_data = {"playerinfo":playerinfo,
                                    "otherinfo":otherinfo}
                        with open("playerdata.json","w") as file:
                            json.dump(all_data, file)
                        player1.inventory = templist
                        blockmovement = False
                        buttongroup = temp_buttongroup
                        inventory1 = temp_inventory
                elif i=="controls":
                    controls_view = True
            try:
                inventory1.checkpressed(event)
            except:
                pass
        if player1.movementframe==0:
            if len(movementkeys)>0:
                if movementkeys[-1] not in blockedkeys:
                    movementkey = movementkeys[-1]
                else:
                    movementkey = ""
            else:
                movementkey = ""
        if validmovement == True and interactingnpc == 0:  # movement code
            if player1.movementframe == 0:
                lastmovementkey = lastkeypressed
                if lastvelocity != velocities[movementkey] and movementkey != "":
                    player1.changingdirection = lastvelocity
                else:
                    player1.changingdirection = False
                velocity = velocities[movementkey]
                if pygame.K_LSHIFT in pressedkeys:
                    speedmultiplier = 8 #running speed
                else:
                    speedmultiplier = 4 #walking speed 
                player1.displacedx = 0
                player1.displacedy = 0
            if player1.movementframe <= 32 and movementkey != "":
                player1.movementframe += speedmultiplier
                previousdisplacement = (player1.displacedx, player1.displacedy)
                player1.displacedx += int(velocity[0] * speedmultiplier)
                player1.displacedy += int(velocity[1] * speedmultiplier)
                if player1.movementframe % 8 == 0:
                    player1.movementanimation(movementanimations[lastmovementkey],
                                             (lambda a: int(-1 / 8 * abs(a - 16) + 2))(player1.movementframe))
                    # function that sets the frames to loop in a 0, 1, 2, 1, 0 pattern, with 16 as the vertex.
                if player1.movementframe == 32:
                    for y in grassgroup:
                        i = y.encounter(player1,difficulty) #battle function runs under random chance
                        if i!=0: #if a battle occured
                            player1 = i[0]
                            movementkey = ("")
                            movementkeys.clear()
                            pressedkeys.clear()
                            if i[1]==True:
                                player1.HP = 100
                                backgroundkey = "lobby"
                                player1.tilex = 16
                                player1.tiley = 16
                            pygame.mixer.music.load("music/PokemonEmeraldMusic.mp3")
                            pygame.mixer.music.play(loops=-1)
                    player1.displacedx = 0
                    player1.displacedy = 0
                    player1.changingdirection = False
                    player1.movementframe = 0
                    for x in npcs[backgroundkey]:
                        x.turnterm = 0
                    lastvelocity = velocity
                    player1.previoustilex = player1.tilex
                    player1.previoustiley = player1.tiley
                    player1.tilex -= velocity[0]
                    player1.tiley -= velocity[1]
                    if movementkey in uppedkeys:
                        movementkey = ""
                        uppedkeys.clear()  # makes it, so you keep moving until the end of the tile
                    if len(movementkeys) > 0:
                        movementkey = movementkeys[-1]
                        lastkeypressed = movementkey
        if interact_request == 1:
            if backgroundkey == "area":
                interactingdoor = player1.interact(doorgroup, lastmovementkey)
                interactingnpc = player1.interact(npcs[backgroundkey], lastmovementkey)
            elif backgroundkey == "lobby":
                interactingnpc = player1.interact(npcs[backgroundkey], lastmovementkey)
                i = player1.interact(lobbydoor, lastmovementkey)
                if player1.currentquest>0:
                    interactingdoor = i
                elif i!=0:
                    selecteddialogue = "Complete the first quest to unlock this door!"
                    boxrequest = 1


            elif backgroundkey == "house":
                interactingdoor = player1.interact(housedoor, lastmovementkey)
                interactingnpc = player1.interact(npcs[backgroundkey], lastmovementkey)
            elif backgroundkey == "boss":
                if bossfight == False:
                    interactingdoor = player1.interact(lobbydoor, lastmovementkey)
                interactingnpc = player1.interact(npcs[backgroundkey], lastmovementkey)
            try:
                if interactingnpc.type == "chest":
                    interactingnpc.dialoguenum = 0
                    if interactingnpc.opened:
                        interactingnpc.dialogue = ["You have already opened this chest!"]
                        selecteddialogue = interactingnpc.dialogue
                    else:
                        player1.gold += 250
                        interactingnpc.opened = True
                        player1.mobsdefeated["chestsopened"] += 1
            except:
                pass
            try:
                if interactingnpc.dialoguetype == "random":
                    selecteddialogue = interactingnpc.dialogue[random.randint(0,len(interactingnpc.dialogue)-1)]
                elif interactingnpc.dialoguetype == "shop":
                    blockmovement = True
                    inventory1 = shop(player1)
                elif interactingnpc.name == "doctor":
                    selecteddialogue = interactingnpc.dialogue[interactingnpc.dialoguenum]
                    interactingnpc.dialoguenum += 1
                    if interactingnpc.dialoguenum>=len(doctor.dialogue):
                        doctor.dialoguenum = 0
                        player1.HP = 100
                elif interactingnpc.name == "questmaster":
                    if questmaster_reset==0:
                        i1 = questupdate(player1, questmaster,"questmasterdialogue.txt","dialogue")
                        if i1!=0:
                            questmaster_reset = 1
                            questmaster = i1
                        interactingnpc = questmaster
                    try:
                        selecteddialogue = interactingnpc.dialogue[interactingnpc.dialoguenum]
                        interactingnpc.dialoguenum += 1
                    except:
                        selecteddialogue = interactingnpc.dialogue[-1]
                elif interactingnpc.name == "oldwoman" and player1.currentquest==8:
                    questmaster.dialoguenum = 0 #quest 8 hard coded, bring the old man back
                    try:
                        selecteddialogue = interactingnpc.dialogue[interactingnpc.dialoguenum]
                        interactingnpc.dialoguenum += 1
                    except:
                        selecteddialogue = interactingnpc.dialogue[-1]
                    if interactingnpc.dialoguenum>=len(oldwoman.dialogue):
                        oldman.dialogue = ["???", "She's looking for me? Oh, I suppose I should come back now.", "I forgot to go back..", "Although I can't remember how I got here without fighting any monsters.", "Could you help me back?"]
                        oldman.dialoguetype = "not random"
                        oldman.dialoguenum = 0
                        player1.mobsdefeated["womanfound"] = 1
                        questmaster = questupdate(player1, questmaster,"questmasterdialogue.txt","dialogue")
                        player1 = questupdate(player1, questmaster,"questmasterdialogue.txt","player")
                elif interactingnpc.name == "oldman" and player1.currentquest==9:
                    questmaster.dialoguenum = 0 #quest 9, bring him back (continued)
                    try:
                        selecteddialogue = interactingnpc.dialogue[interactingnpc.dialoguenum]
                        interactingnpc.dialoguenum += 1
                    except:
                        selecteddialogue = interactingnpc.dialogue[-1]
                    if interactingnpc.dialoguenum>=len(oldman.dialogue):
                        player1.mobsdefeated["manfound"] = 1
                        questmaster = questupdate(player1, questmaster,"questmasterdialogue.txt","dialogue")
                        player1 = questupdate(player1, questmaster,"questmasterdialogue.txt","player")
                        oldwoman.dialogue = ["Thank you young man!", "I'm sure the questmaster has something for you, go back to him!",]
                        oldwoman.dialoguenum = 0
                        oldman.following = True
                        areanpc.add(oldman)
                elif interactingnpc.name == "oldwoman" and player1.currentquest == 10:
                    questmaster.dialoguenum = 0 #woo hoo you brought him back!!!
                    try:
                        selecteddialogue = interactingnpc.dialogue[interactingnpc.dialoguenum]
                        interactingnpc.dialoguenum += 1
                    except:
                        selecteddialogue = interactingnpc.dialogue[-1]
                    if interactingnpc.dialoguenum >= len(oldwoman.dialogue):
                        i = questupdate(player1,questmaster,"questmasterdialogue.txt","dialogue")
                        if i!=0:
                            questmaster =i
                        oldman.dialogue = ["I sure am grateful!"] #new dialogue
                        oldman.dialoguetype = "random"
                        player1.mobsdefeated["womanfound"] = 1 #hooray
                        oldman.following = False
                        oldman.tilex = 20 #moving them into the same house
                        oldman.tiley = 16
                        housenpc.add(oldman)
                        housenpcs[3] = [oldwoman, oldman]
                        areanpc.remove(oldman)
                elif interactingnpc.name == "wizard" and player1.currentquest == 16:
                    questmaster.dialoguenum = 0 #bossfight starts
                    try:
                        selecteddialogue = interactingnpc.dialogue[interactingnpc.dialoguenum]
                        interactingnpc.dialoguenum += 1
                    except:
                        selecteddialogue = interactingnpc.dialogue[-1]
                    if interactingnpc.dialoguenum >= len(wizard.dialogue):
                        i = questupdate(player1, questmaster, "questmasterdialogue.txt", "dialogue")
                        if i != 0:
                            questmaster = i
                        #code to start bossfight
                        player1.mobsdefeated["startboss"] += 1
                        bossfight = True
                        track = 0
                        for npc1 in lobbynpc:
                            areanpc.add(npc1)
                            lobbynpc.remove(npc1)
                            npc1.tilex = 97
                            npc1.tiley = 170 + track #code to make npcs line up to help before the boss fight
                            track += 1
                        questmaster.tilex = 100
                        questmaster.tiley = 181
                        bossbarrier = obstacle(96,182,8,1)
                        objectgroup.add(bossbarrier) #bossbarrier up until you talk to the questmaster
                        housenpc.remove(wizard)
                        housenpcs[10] = []
                        wizard.dialoguenum = 0
                elif interactingnpc.name == "wizard" and bossfight == True:
                    wizard.dialogue = ["How dare you challenge me!","Wow I guess you win..."]
                    try:
                        selecteddialogue = interactingnpc.dialogue[interactingnpc.dialoguenum]
                        interactingnpc.dialoguenum += 1
                    except:
                        selecteddialogue = interactingnpc.dialogue[-1]
                    if interactingnpc.dialoguenum >= len(wizard.dialogue):
                        battle(player1, 4,difficulty) #wizard is the only mob here
                        player1.mobsdefeated["win"] = 1
                        dialogueend = 1
                        boxrequest = 0
                        buttongroup.add(quitbutton) #hooray!!!! displays the "you win" textures
                        buttongroup.add(endbutton)
                elif player1.currentquest == 17 and questmaster.tilex!=97:
                    areanpc.remove(questmaster)
                    questmaster.tilex = 97 #allows you to enter the boss room
                    questmaster.tiley = 180
                    areanpc.add(questmaster)
                    objectgroup.remove(bossbarrier)
                        
                else:
                    selecteddialogue = interactingnpc.dialogue[interactingnpc.dialoguenum]
                    interactingnpc.dialoguenum+=1

            except:
                pass
        if inventoryrequest == 1:
            try:
                crashtest = inventory1.posx
                blockmovement = False
                inventory1 = 0
            except:
                blockmovement = True #blocks movement
                inventory1 = inventory(player1.inventory, 608, 480) #displays inventory
            inventoryrequest = 0
        if interactingnpc != 0 or boxrequest==1:  # dialogue code
            try:
                i = interactingnpc.dialoguetype!="shop"
            except:
                i = boxrequest
                interactingnpc = player1.interact(lobbydoor, lastmovementkey)

            if i==True:
                tempbox = player1.dialogue(interactingnpc.image,selecteddialogue, lastkeypressed, dialogueskip)
                if boxrequest==1:
                    interactingnpc = 0
                if dialogueend == 1:
                    if interactingnpc!=0:
                        if interactingnpc.type=="npc":
                            if interactingnpc.name != "questmaster" and interactingnpc.name != "wizard" and interactingnpc.name != "shop" and interactingnpc.talked==0:
                                try:
                                    crashtest = questmasterinfo.questlist #if you have no more quests it "crashes"
                                    interactingnpc.talked = 1
                                    player1.mobsdefeated["npctalk"] += 1
                                except:
                                    pass
                    boxrequest = 0
                    lastkeypressed = player1.predialogue_key
                    movementkey = ""
                    interactingnpc = 0
                    player1.dialogueterm = 0
                    dialogueend = 0
                    dialogueskip = 0

        if interactingdoor != 0:
            previousbackground = backgroundkey
            backgroundkey = interactingdoor.destination
            if backgroundkey == "area":  # changing area
                if previousbackground == "lobby":
                    player1.tilex = 100
                    player1.tiley = 182
                elif previousbackground == "house":
                    player1.tilex = lastplayerpos[0] #doors have a lot of locations
                    player1.tiley = lastplayerpos[1]
                    for npc in housenpc:
                        housenpc.remove(npc) #remove npcs from that house
                else:
                    player1.tilex = 100
                    player1.tiley = 182
            if backgroundkey == "lobby":
                if previousbackground == "area" and bossfight == False:
                    player1.tilex = 17
                    player1.tiley = 3 #send to lobby if you haven't triggered bossfight yet
                else:
                    backgroundkey = "boss"
                    player1.tilex = 17
                    player1.tiley = 3 #scary bossfight
                    wizard.tilex = 17
                    wizard.tiley = 17
            if backgroundkey == "house":
                if interactingdoor in doorlist:
                    for i in range(len(doorlist)):
                        if interactingdoor == doorlist[i]:
                            for npc in housenpcs[i]:
                                housenpc.add(npc)
                            if oldman.following == True: #old man follows you inside the house
                                housenpc.add(oldman)
                            npcs["house"] = housenpc
                lastplayerpos = (player1.tilex, player1.tiley)
                player1.tilex = 16
                player1.tiley = 16
            background[backgroundkey].update()
        robert1.following = False

        if velocity == (0, 0) and interactingnpc == 0:  # direction changing
            stalltimer += 1
            if stalltimer == 8:#idle animation timer (8 ticks)
                player1.movementanimation(movementanimations[lastkeypressed], 3)
                stalltimer = 0

        background[backgroundkey].posx = 608 - (32 * player1.tilex - player1.displacedx) #moves background
        background[backgroundkey].posy = 480 - (32 * player1.tiley - player1.displacedy)
        background[backgroundkey].update()
        screen.fill((0, 0, 0))
        screen.blit(background[backgroundkey].image1, background[backgroundkey].rect)
        for x in npcs[backgroundkey]:
            x.update(player1, speedmultiplier, velocity) if x.type == "npc" else x.updatechest(player1)
        if background[backgroundkey] == "area" and bossfight == False:
            npcs[backgroundkey].draw(screen)
        npcs[backgroundkey].draw(screen)
        screen.blit(pygame.image.load(player1.imagestr).convert_alpha(),(player1.posx - 16, player1.posy - 48)) # (player1.posx - 16, player1.posy - 16), (32, 32)
        #playergroup.draw(screen)
        screen.blit(background[backgroundkey].image2, background[backgroundkey].rect)
        try:
            #if quitbutton in buttons and endbutton in buttons:
            buttongroup.draw(screen)
            screen.blit(errortext,(600-errortext.get_width(),400))
        except:
            pass
        
        
        try:
            inventory1.update()
            inventory1.print(screen)
        except:
            try:
                questmasterinfo.update(screen,player1)
            except:
                pass

        if player1.dialogueterm > 0 and dialogueend == 0:
            try:
                screen.blit(tempbox.image, (64, 656))
                screen.blit(tempbox.spriteimage, (950, 700))
                for textnum in range(len(tempbox.boxtexts)):
                    screen.blit(tempbox.boxtexts[textnum], (72, 664 + 30 * textnum))
            except:
                pass
        if controls_view == True:
            screen.blit(controls_image,(32,32)) #displays controls
        pygame.display.update()
        pygame.time.Clock().tick(60)
    pygame.quit()