from window import Window,Vector,math,remap,clamp
from neutral_network import NeutralNetwork
import random
import time


grid = 20
spacing=300
Screen=spacing*2

num=100
breedpool=[]
bestsnake=None
bestscore=-1

snakes=[]
gen=0
total=0
gen_cap=100
count=1

def draw():
    global gen,snakes,breedpool,total,bestscore,bestsnake,count
    W.fill(0,0,0)
    W.stroke(255,255,255)
    W.rect(Vector(0, 0),(Screen-Screen/grid)+5,(Screen-Screen/grid)+5)
    W.stroke()
    dead=0
    for s in snakes:
        if s.dead == False:
            s.move()
            s.update(grid)
            s.eat()
            #s.show(grid)
        else:
            dead+=1

    if dead>=num:
        if count<10:
            for i in range(num):
                score=snakes[i].score
                snakes[i]=snake(food(4,4),snakes[i].brain)
                snakes[i].score=score
            count+=1
        else:
            if gen<gen_cap:
                snakes.sort(key = lambda x:x.score,reverse=True)
                for i in range(0,int(num/20),1):
                    #select top 40 and put exponentially in breeding pool
                    for j in range(int((num/20)/pow(2,i/10))):
                        breedpool.append(snakes[i].brain)

                total=0
                for s in snakes:
                    total+=s.score/10

                snakes=[]

                for i in range(num):
                    n1=breedpool[random.randint(0,len(breedpool)-1)]
                    n2=breedpool[random.randint(0,len(breedpool)-1)]
                    n3=n1.crossbreed(n2)
                    n3.mutate()
                    s=snake(food(5,5),n3)
                    snakes.append(s)
                breedpool=[]
                gen+=1
                count=1
            else:
                if bestsnake==None:
                    for s in snakes:
                        if s.score>bestscore:
                            bestscore=s.score
                            bestsnake=s
                else:
                    if bestsnake.dead == False:
                        bestsnake.move()
                        bestsnake.update(grid)
                        bestsnake.eat()
                        bestsnake.show(grid)
                        time.sleep(0.1)
                    else:
                        print(bestsnake.score)
                        bestsnake=snake(food(5,5),bestsnake.brain)

                    W.stroke(255,255,255)
                    W.write(Vector(280,-350),"moves: "+str(int(bestsnake.hunger)),2)
                    W.write(Vector(250,350),"score: "+str(bestsnake.score),2)
                    W.write(Vector(-300,-350),'gen trained:'+str(gen_cap),2)
                    W.stroke()


    else:
        i=0
        while snakes[i].dead==True and i<num-1:
            i+=1
            
        snakes[i].show(grid)
        if len(snakes[i].body)>0:
            s=snakes[i]

        W.stroke(255,255,255)
        W.write(Vector(280,-350),"moves: "+str(int(snakes[i].hunger)),2)
        W.write(Vector(250,350),"gen fitness: "+str(round(total/num,3)),2)
        W.write(Vector(-300,-350),'gen:'+str(gen),2)
        W.write(Vector(-300,350),'alive:'+str(num-dead),2)
        W.write(Vector(0,350),'count:'+str(count),2)
        W.stroke()


    

class snake():

    def __init__(self,f,brain):
        self.head = Vector(9,9)
        self.prev = None
        self.dir = Vector(0,-1)
        self.body = []
        self.dead = False
        self.food = f
        self.brain=brain
        self.hunger=int((grid*grid)/4)
        self.score=0
    
    def update(self,grid):
        self.hunger-=1
        self.prev = Vector(self.head.x,self.head.y)
        self.head.add(self.dir)

        if self.head.x < 0 :
            self.dead = True
        elif self.head.y < 0:
            self.dead = True
        elif self.head.x > grid-1 :
            self.dead = True
        elif self.head.y > grid-1 :
            self.dead = True

        if self.hunger<1:
            self.dead=True

        if self.dead==True:
            return

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

    def show(self,grid,debug=False):
        if self.dead==True:
            return

        if debug== True:
            W.fill(0,0,255)
            W.stroke(0,0,255)
            for s in self.sight:
                if self.head.x+s.x>-1 and self.head.x+s.x<grid and self.head.y+s.y>-1 and self.head.y+s.y<grid:
                    x = remap(self.head.x+s.x,0,grid-1,-spacing+Screen/grid,spacing-Screen/grid)
                    y= remap(self.head.y+s.y,0,grid-1,spacing-Screen/grid,-spacing+Screen/grid)
                    W.rect(Vector(x,y),Screen/grid,Screen/grid)
                

        W.fill(0,0,0)
        W.stroke()

        self.food.show(grid)

        x = remap(self.head.x,0,grid-1,-spacing+Screen/grid,spacing-Screen/grid)
        y= remap(self.head.y,0,grid-1,spacing-Screen/grid,-spacing+Screen/grid)

        W.fill(0,255,0)
        W.rect(Vector(x,y),Screen/grid,Screen/grid)

        for i in range(len(self.body)):
            x = remap(self.body[i].x,0,grid-1,-spacing+Screen/grid,spacing-Screen/grid)
            y= remap(self.body[i].y,0,grid-1,spacing-Screen/grid,-spacing+Screen/grid)

            W.fill(0,255,0)
            W.rect(Vector(x,y),Screen/grid,Screen/grid)


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
        for i in range(grid+1):
            a.append([])
            for j in range(grid+1):
                a[i].append(0)
        
        a[round(self.head.y)][round(self.head.x)]=1
        for i in range(len(self.body)):
            a[round(self.body[i].y)][round(self.body[i].x)]=1

        return a

    def eat(self):
        if self.dead==True:
            return
        f = self.food
        f.pos.x = round(f.pos.x)
        f.pos.y = round(f.pos.y)
        if self.head.dist(f.pos) < 0.1:
            self.hunger+=int((grid*grid)/4)
            self.score+=1
            spots = self.openspots(grid)
            n = random.randint(0,len(spots)-1)
            self.food = food(round(spots[n][0]),round(spots[n][1]))
            self.body.append(self.prev)

    def up(self):
        if self.dir.y != 1:
            self.dir = Vector(0,-1)

    def dn(self):
        if self.dir.y != -1:
            self.dir = Vector(0,1)

    def rt(self):
        if self.dir.x != -1:
            self.dir = Vector(1,0)


    def lt(self):
        if self.dir.x != 1 :
            self.dir = Vector(-1,0)


    def move(self):
        a=[]

        if self.food.pos.x<self.head.x:
            a.append(1)
        else:
            a.append(0)

        if self.food.pos.y<self.head.y:
            a.append(1)
        else:
            a.append(0)

        if self.food.pos.x>self.head.x:
            a.append(1)
        else:
            a.append(0)

        if self.food.pos.y>self.head.y:
            a.append(1)
        else:
            a.append(0)

        #check walls

        if round(self.head.x)==0:
            a.append(1)
        else:
            a.append(0)

        if round(self.head.y)==0:
            a.append(1)
        else:
            a.append(0)

        if round(self.head.x)==grid-1:
            a.append(1)
        else:
            a.append(0)

        if round(self.head.y)==grid-1:
            a.append(1)
        else:
            a.append(0)

        #check body

        up=False
        down=False
        right=False
        left=False
        for i in range(len(self.body)): #need minimum 4 to touch body
            if round(self.head.x-1)==round(self.body[i].x):
                left=True

            if round(self.head.x+1)==round(self.body[i].x):
                right=True

            if round(self.head.y-1)==round(self.body[i].y):
                up=True

            if round(self.head.y+1)==round(self.body[i].y):
                down=True

        if up:
            a.append(1)
        else:
            a.append(0)

        if down:
            a.append(1)
        else:
            a.append(0)

        if right:
            a.append(1)
        else:
            a.append(0)

        if left:
            a.append(1)
        else:
            a.append(0)

        a.append(remap(len(self.body),0,grid*grid,0,1)**2)

        self.brain.input(a)
        
        self.brain.update()
        guess=self.brain.guess()

        up=guess[0]
        rt=guess[1]
        lt=guess[2]
        dn=guess[3]
        

        if up > rt and up > lt and up > dn:
            self.up()
        else:
            if lt > rt and lt > dn:
                self.lt()
            else:
                if rt>dn:
                    self.rt()
                else:
                    self.dn()

class food():
    def __init__(self,x,y):
        self.pos = Vector(x,y)
    
    def show(self,grid):
        x = remap(self.pos.x,0,grid-1,-spacing+Screen/grid,spacing-Screen/grid)
        y= remap(self.pos.y,0,grid-1,spacing-Screen/grid,-spacing+Screen/grid)

        W.fill(255,0,0)
        W.rect(Vector(x,y),Screen/grid,Screen/grid)

if __name__ == "__main__":
    W = Window(0,0,800,800)
    for i in range(num):
        s=snake(food(5,5),NeutralNetwork(13,10,10,4,0.01))
        snakes.append(s)
    W.bgcolor(0,0,0,0)

    def setup():
        pass

    W.run(setup,draw,120)
