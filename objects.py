import pygame
from sprites import obstacle, water, tallgrass, door

#object declarations
pygame.init()
objectgroup = pygame.sprite.Group()
watergroup = pygame.sprite.Group()
grassgroup = pygame.sprite.Group()
doorgroup = pygame.sprite.Group()
lobbygroup = pygame.sprite.Group()
housegroup = pygame.sprite.Group()
bossgroup = pygame.sprite.Group()
# grass1 = tallgrass(100,160,3,3,1)

# grassgroup.add(grass1)

obstacles = []    #  the way that this works is that we have objects imported from tiled
watertiles = []   #  that we put into text files with the format posx/posy/width/length
doortiles = []    #  these files are read and put into sprite groups which are then
grasstiles = []   #  imported into the movement file
lobbytiles = []
housetiles = []
bosstiles = []

#trees and walls
with open("objects/trees_and_walls_and_houses.txt") as f:
    for line in f:
        line = line.replace("\n", "")
        obstacles.append(line.split("/"))
#
obstaclelist = [
    obstacle(int(int(item[0]) / 32) + 1, int(int(item[1]) / 32) + 1, int(int(item[2]) / 32), int(int(item[3]) / 32)) for
    item in obstacles]
for term in obstaclelist:
    objectgroup.add(term)

#water
with open("objects/water.txt") as f:
    for line in f:
        line = line.replace("\n", "")
        watertiles.append(line.split("/"))

waterlist = [
    water(int(int(item[0]) / 32) + 1, int(int(item[1]) / 32) + 1, int(int(item[2]) / 32), int(int(item[3]) / 32)) for
    item in watertiles]
for term in waterlist:
    watergroup.add(term)

#doors
with open("objects/doors.txt") as f:
    for line in f:
        line = line.replace("\n", "")
        doortiles.append(line.split("/"))

doorlist = [door(int(int(item[0]) / 32) + 1, int(int(item[1]) / 32) + 1, int(int(item[2]) / 32), int(int(item[3]) / 32), "house")
            for item in doortiles]
for term in doorlist:
    doorgroup.add(term)

#door that goes back to lobby
backtolobby = door(100, 185, 1, 1, "lobby")
doorgroup.add(backtolobby)

# grass objects
with open("objects/grassobjects.txt") as f:
    for line in f:
        line = line.replace("\n", "")
        grasstiles.append(line.split("/"))

grasslist = [
    tallgrass(int(int(item[0]) / 32) + 1, int(int(item[1]) / 32) + 1, int(int(item[2]) / 32), int(int(item[3]) / 32), 1)
    for item in grasstiles]
for term in grasslist:
    grassgroup.add(term)

# lobby objects
with open("objects/lobbyobj.txt") as f:  # a
    for line in f:
        line = line.replace("\n", "")
        lobbytiles.append(line.split("/"))

lobbylist = [
    obstacle(int(int(item[0]) / 32) + 1, int(int(item[1]) / 32) + 1, int(int(item[2]) / 32), int(int(item[3]) / 32)) for
    item in lobbytiles]
for term in lobbylist:
    lobbygroup.add(term)

# hosue objects
with open("objects/houseobjects.txt") as f:
    for line in f:
        line = line.replace("\n", "")
        housetiles.append(line.split("/"))

houselist = [
    obstacle(int(int(item[0]) / 32) + 1, int(int(item[1]) / 32) + 1, int(int(item[2]) / 32), int(int(item[3]) / 32)) for item in housetiles]
for term in houselist:
    housegroup.add(term)

#bossfight objects
with open("objects/bossfightobjects.txt") as f:
    for line in f:
        line = line.replace("\n", "")
        bosstiles.append(line.split("/"))

bosslist = [
    obstacle(int(int(item[0]) / 32) + 1, int(int(item[1]) / 32) + 1, int(int(item[2]) / 32), int(int(item[3]) / 32)) for item in bosstiles]
for term in bosslist:
    bossgroup.add(term)
