import pygame #store all item lists and classes for easy access
class item():
    def __init__(self,name,imagestr,cost):
        self.name = name
        self.itemtype = "drops"
        self.imagestr = imagestr
        self.cost = cost
    def buy(self,player):
        player.gold -= self.cost
        player.inventory[self.itemtype].append(self)
    def sell(self,player):
        player.gold += self.cost/2
        player.inventory[self.itemtype].remove(self)
    def convert_dict(self):
        return self.__dict__


class weapon(item):
    def __init__(self, name, imagestr, cost, damage):
        super().__init__(name,imagestr,cost)
        self.itemtype = "weapon"
        self.damage = damage

class defence(item):
    def __init__(self, name, imagestr, cost, blockpercentage):
        super().__init__(name,imagestr,cost)
        self.itemtype = "defence"
        self.blockpercentage = blockpercentage

#weapons
weaponlist = [weapon("Starter Sword","graphics/weapons/falchion.png",100,20),
              weapon("Emerald Blade","graphics/weapons/emerald_blade.png",500,30),
              weapon("Scythe","graphics/weapons/scythe.png",700,40),
              weapon("Silver Fang","graphics/weapons/silver_fang.png",1000,50),
              weapon("Aspect of the Dragon","graphics/weapons/aotd.png",1500,60)]

#defences
defencelist = [defence("Cheap Tuxedo","graphics/defences/cheap_jacket.png",500,0.3),
              defence("Elegant Tuxedo","graphics/defences/elegant_jacket.png",800,0.6),
              defence("Superior Dragon","graphics/defences/supdc.png",1500,0.8)]
#items
shopitems = {"weapon":weaponlist,
            "defence":defencelist,
             "drops":[]} #nothing in drops to buy but it breaks for whatever reason if there's no drops here