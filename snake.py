from window import Window,Vector,math,remap,clamp
import random


grid = 20
n=0


def draw():
    global n
    if Snake.dead == False:
        keyboard = W.keyboard()
        if keyboard != None:
            key = keyboard[1]
            if key == 119:
                Snake.up()
            if key == 115:
                Snake.dn()
            if key == 100:
                Snake.rt()
            if key == 97:
                Snake.lt()
            

        Snake.update(grid)
        Snake.eat()
        Snake.show(grid)
    else:
        W.stroke(255,255,255)
        W.write(Vector(0,10),"Game Over",3)
        W.write(Vector(0,-30),"score : "+str(Snake.score),3)
        W.stroke()
        if n == 0:
            W.timer(reset,2000)
            n=1

def reset(x):
    global Snake,n
    Snake = snake(food(4,4))
    n=0
    

class snake():
    def __init__(self,f):
        self.head = Vector(9,9)
        self.prev = None
        self.dir = Vector(0,0)
        self.body = []
        self.dead = False
        self.score = 0
        self.stop = 0
        self.food = f
    
    def update(self,grid):
        if self.head.x < 1 and self.dir.x == -1:
            self.dead =  True
        elif self.head.y < 1 and self.dir.y == -1:
            self.dead = True
        elif self.head.x > grid-2 and self.dir.x == 1:
            self.dead = True
        elif self.head.y > grid-2 and self.dir.y == 1:
            self.dead = True

        self.prev = Vector(self.head.x,self.head.y)

        self.head.add(self.dir)

        for i in range(len(self.body)):
            if self.head.dist(self.body[i]) < 0.1:
                self.dead = True

        if len(self.body) > 0:
            for i in range(len(self.body),1,-1):
                self.body[i-1].x = self.body[i-2].x
                self.body[i-1].y = self.body[i-2].y
                
            self.body[0].x=self.prev.x
            self.body[0].y=self.prev.y

        self.head.x = round(self.head.x)
        self.head.y = round(self.head.y)

    def show(self,grid):

        self.food.show(grid)

        x = remap(self.head.x,0,grid-1,-500+1000/grid,500-1000/grid)
        y= remap(self.head.y,0,grid-1,500-1000/grid,-500+1000/grid)

        W.fill(0,255,0)
        W.rect(Vector(x,y),1000/grid,1000/grid)

        for i in range(len(self.body)):
            x = remap(self.body[i].x,0,grid-1,-500+1000/grid,500-1000/grid)
            y= remap(self.body[i].y,0,grid-1,500-1000/grid,-500+1000/grid)

            W.fill(0,255,0)
            W.rect(Vector(x,y),1000/grid,1000/grid)


    def openspots(self,grid):
        a = self.emptyspaces(grid)

        b= []
        for i in range(len(a)-1):
            for j in range(len(a[i])-1):
                if a[i][j] == 0:
                    b.append((j,i))
        return b

    def emptyspaces(self,grid):
        a = []
        for i in range(grid):
            a.append([])
            for j in range(grid):
                a[i].append(0)
        
        a[round(self.head.y)][round(self.head.x)]=1
        for i in range(len(self.body)):
            a[round(self.body[i].y)][round(self.body[i].x)]=1

        return a

    def eat(self):
        f = self.food
        f.pos.x = round(f.pos.x)
        f.pos.y = round(f.pos.y)
        if self.head.dist(f.pos) < 0.1:
            self.score+=1
            spots = self.openspots(grid)
            n = random.randint(0,len(spots)-1)
            self.food = food(round(spots[n][0]),round(spots[n][1]))
            self.body.append(self.prev)

    def up(self):
        if self.dir.y != 1 and self.stop== 0:
            self.dir = Vector(0,-1)
            self.stop = 1
            W.timer(self.n,80)

    def dn(self):
        if self.dir.y != -1 and self.stop== 0:
            self.dir = Vector(0,1)
            self.stop = 1
            W.timer(self.n,80)

    def rt(self):
        if self.dir.x != -1 and self.stop == 0:
            self.dir = Vector(1,0)
            self.stop = 1
            W.timer(self.n,80)

    def lt(self):
        if self.dir.x != 1 and self.stop== 0:
            self.dir = Vector(-1,0)
            self.stop = 1
            W.timer(self.n,80)

    def n(self,x):
        self.stop = 0


class food():
    def __init__(self,x,y):
        self.pos = Vector(x,y)
    
    def show(self,grid):
        x = remap(self.pos.x,0,grid-1,-500+1000/grid,500-1000/grid)
        y= remap(self.pos.y,0,grid-1,500-1000/grid,-500+1000/grid)

        W.fill(255,0,0)
        W.rect(Vector(x,y),1000/grid,1000/grid)

if __name__ == "__main__":
    W = Window(0,0,1000,1000)
    Snake = snake(food(4,4))
    W.bgcolor(0,0,0,0)
    def setup():
        pass

    W.run(setup,draw,10)
