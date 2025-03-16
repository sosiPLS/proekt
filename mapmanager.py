class Mapmanager():
    def __init__(self):
        self.model = 'block' # модель кубика лежит в файле block.egg
        # # используются следующие текстуры:
        self.texture = 'block.png'         
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ] #rgba
        # создаём основной узел карты:
        self.startNew()
        # self.addBlock((0,10, 0))


    def startNew(self):
        self.land = render.attachNewNode("Land") # узел, к которому привязаны все блоки карты


    def getColor(self, z):
        return self.colors[z % len(self.colors)]

    def addBlock(self, position):
        # создаём строительные блоки
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)

        self.block.setTag('at', str(position))

        self.block.reparentTo(self.land)


    def clear(self):
        """обнуляет карту"""
        self.land.removeNode()
        self.startNew()


    def loadLand(self, filename):
        """создаёт карту земли из текстового файла, возвращает её размеры"""
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
            return x, y
    def findBlock(self, pos):
        return self.land.findAllMatches('=at', + str(pos))
    
    def isEmpty(self, pos):
        blocks = self.findBlock(pos)
        if blocks:
            return False
        else:
            return True
    
    def findHighesEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return(x, y, z)
    
    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighesEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlockFrom(self, position):
        x, y, z = self.findHighesEmpty(position)
        pos = x, y, z - 1
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()