from itemstack import *

class Character:
    def __init__(self,name:str) -> None:
        self.name = name
        self.level = 0
        self.inventory = []
        self.inventory.append(ItemStack("mora",100))
    
    def addInventory(self,itemstack:ItemStack) -> str:
        for i in self.inventory:
            if i.getType() == itemstack.getType():
                i.setAmount(i.getAmount()+itemstack.getAmount())
                return
        self.inventory.append(itemstack)
    
    def setItemStackInventory(self,itemstack:ItemStack) -> str:
        for i in self.inventory:
            if i.getType() == itemstack.getType():
                i.setAmount(itemstack.getAmount())
                return
        self.inventory.append(itemstack)

    def getName(self) -> str:
        return self.name
    
    def getItemByType(self,type:str) -> ItemStack:
        for i in self.inventory:
            if i.getType() == type:
                return i
        return None

