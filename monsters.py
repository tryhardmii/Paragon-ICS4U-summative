
import pygame
from items import item
pygame.init() #store monster class and list of monsters and items they drop
class monster:
    def __init__(self,name,image,HP,damage,spawnrate,drops):
        self.drops = drops
        self.dropstring = "".join([x.name for x in drops])
        self.name = name
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image,(128,128))
        self.posx = 608
        self.posy = 0
        self.rect = self.image.get_rect(center=(self.posx,self.posy))
        self.spawnrate = spawnrate #lower number = lower spawnrate
        self.maxHP = HP
        self.HP = HP
        self.damage = damage
    def move(self,displacedx,displacedy):
        self.posx+=displacedx
        self.posy+=displacedy
        self.rect = self.image.get_rect(center=(self.posx,self.posy))

#drops, cost is for the sell value
#drops sorted as list to make monsters list more readable
drops = [item("Egg","graphics/drops/bridge_egg.png",50),
         item("String","graphics/drops/melody_hair.png",50),
         item("Pearl","graphics/drops/silent_pearl.png",500),
         item("Diamond","graphics/drops/diamond_spreading.png",50),
         item("Essence","graphics/drops/true_essence.png",200),
         item("Crystal","graphics/drops/crystal_frag.png",200),
         item("Star","graphics/drops/catalyst.png",200),
         item("Night Star","graphics/drops/night_crystal.png",200),
         item("Web","graphics/drops/tarantula_silk.png",300),
         item("Golden Tooth","graphics/drops/golden_tooth.png",300),
         item("Tooth","graphics/drops/tooth.png",300),
         item("Day Star","graphics/drops/day_crystal.png",300),
         item("Crown","graphics/drops/tarantula_silk.png",1000),
         ]

#monsters, each list is a different area
monsterlist = [[monster("ghost","graphics/area1monsters/ghost.png",50,15,6,[drops[0]]),
                monster("goblin","graphics/area1monsters/goblin.png",70,15,6, [drops[1]]),
                monster("legendary loser","graphics/area1monsters/loser.png",100,10,1,[drops[2]]),
                monster("skeleton","graphics/area1monsters/skeleton.png",120,10,6,[drops[3]])],
               [monster("crab","graphics/area2monsters/crab.png",100,20,1,[drops[4]]),
                monster("frog","graphics/area2monsters/frog.png",150,5,1,[drops[5]]),
                monster("redspider","graphics/area2monsters/redspider.png",70,25,1,[drops[6]]),
                monster("rock","graphics/area2monsters/rock.png",300,1,1,[drops[7]])],
               [monster("circle","graphics/area3monsters/circle.png",150,25,1,[drops[8]]),
                monster("iceghost","graphics/area3monsters/iceghost.png",120,20,1,[drops[9]]),
                monster("Creep","graphics/area3monsters/redweirdo.png",140,20,1,[drops[10]]),
                monster("skeleton2","graphics/area3monsters/skeleton2.png",130,20,1,[drops[11]])],
               [monster("wizard","graphics/npcs/wizard.png", 350, 20, 1, [drops[12]])]]
                # wizard is the final boss and has its own area