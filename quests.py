from items import weaponlist #to give player starting weapon
def questupdate(player1, questmaster1,file,requesttype): #check if quests are completed, requesttype changes what you return (questmaster/dialogue/player)
    class quest:
        def __init__(self,string,currentvalue,totalvalue):
            self.string = string
            self.currentvalue = currentvalue
            self.totalvalue = totalvalue
    player = player1
    questmaster = questmaster1
    with open(file, "r") as f:
        questmasterdialogue = []
        stringlist = []
        for line in f:
            line = line.replace("\n", "")
            for char in line:
                if char == "":
                    del char
            temp = line.split("/")
            temp1 = temp[-1].split("|")
            del temp[-1]
            temp.append(temp1[0])
            questmasterdialogue.append(temp)
            stringlist.append(temp1[1])
    questlist = {
        "questmaster":[
            #area 1 quests
            quest(stringlist[0],player.mobsdefeated["npctalk"],5), #currentvalue is the
            quest(stringlist[1],player.mobsdefeated["ghost"] + player.mobsdefeated["goblin"] + player.mobsdefeated["loser"] + player.mobsdefeated["skeleton"],5),
            quest(stringlist[2],player.mobsdefeated["ghost"] + player.mobsdefeated["goblin"] + player.mobsdefeated["loser"] + player.mobsdefeated["skeleton"],10),
            quest(stringlist[3],player.mobsdefeated["ghost"] + player.mobsdefeated["goblin"] + player.mobsdefeated["loser"] + player.mobsdefeated["skeleton"],5),
            quest(stringlist[4],player.mobsdefeated["chestsopened"],1),
            quest(stringlist[5],player.mobsdefeated["loser"],1),
            quest(stringlist[6],player.mobsdefeated["area2"],1), #talking to wizard
            # AREA 2 quests
            quest(stringlist[7],player.mobsdefeated["rock"] + player.mobsdefeated["crab"] + player.mobsdefeated["frog"] + player.mobsdefeated["redspider"], 5),  # talking to wizard
            quest(stringlist[8], player.mobsdefeated["womanfound"], 1),
            quest(stringlist[9], player.mobsdefeated["manfound"], 1),
            quest(stringlist[10], player.mobsdefeated["womanfound"], 1),
            quest(stringlist[11], player.mobsdefeated["rock"] + player.mobsdefeated["crab"] + player.mobsdefeated["frog"] + player.mobsdefeated["redspider"], 10),
            #AREA 3 quests
            quest(stringlist[12], player.mobsdefeated["area3"], 1),
            quest(stringlist[13], player.mobsdefeated["circle"] + player.mobsdefeated["iceghost"] + player.mobsdefeated["Creep"] + player.mobsdefeated["skeleton2"], 5),
            quest(stringlist[14], len([x for x in player.inventory["drops"] if x.name == "Tooth"]), 5),
            quest(stringlist[15], player.mobsdefeated["circle"] + player.mobsdefeated["iceghost"] + player.mobsdefeated["Creep"] + player.mobsdefeated["skeleton2"], 10),
            #bossfight quests
            quest(stringlist[16], player.mobsdefeated["startboss"],1),
            quest(stringlist[17], player.mobsdefeated["win"],1),
            #placeholder quest that is impossible to complete on pourpose
            quest(stringlist[18], 100,1)
        ],
    }
    if requesttype == "questlist":
        return questlist[questmaster.name]
    elif requesttype == "questdialogue":
        return questmasterdialogue
    else:
        def questcompleted(): #makes it so that you have to talk to the questmaster to get the next quest
            if requesttype == "dialogue":
                questmaster.dialogue = questmasterdialogue[player.currentquest+1]
                questmaster.dialoguenum = 0
                return questmaster
            elif requesttype == "dialoguestart":
                questmaster.dialogue = questmasterdialogue[player.currentquest]
                questmaster.dialoguenum = 0
                return questmaster
            elif requesttype == "player":
                for value in player.mobsdefeated:
                    player.mobsdefeated[value] = 0
                player.currentquest += 1
                player.gold += 100
                return player

        if player.currentquest == 0:
            if player.mobsdefeated["npctalk"] >= 5: #starting quest with special reward of a starting sword
                if not weaponlist[0] in player.inventory["weapon"]:
                    player.inventory["weapon"].append(weaponlist[0])
                return questcompleted()
            elif requesttype == "dialoguestart":
                return questcompleted()
        else:
            #standard 100 gold reward for completing a quest
            if questlist[questmaster.name][player.currentquest].currentvalue >= questlist[questmaster.name][player.currentquest].totalvalue or requesttype=="dialoguestart":
                return questcompleted()
        return 0