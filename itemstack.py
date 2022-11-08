class ItemStack:
    def __init__(self,type:str,amount:int) -> None:
        self.type = type
        self.amount = amount
    
    def getType(self) -> str:
        return self.type
    
    def getAmount(self) -> int:
        return self.amount
    
    def setType(self,type) -> None:
        self.type = type
    
    def setAmount(self,amount) -> None:
       self.amount = amount