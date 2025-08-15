import random
import mm
'''
When detector finds a reason for a change in its sight, it stores the combination of the changes in that tick and its output into mem, which can be used to learn further things
Three main classes of 'why':
1: movement, it moved from one cell to an adjacent
2: appearance/disappearance, just blips in/out, no adjacent changes including the object
3: pushing, pushes one object forward to make room for itself, causing 2 movement classes

setup.class# is memory of previous experiences
'''
#Sees things, and guesses how changes happen based on previous knowledge
class detector:
    def __init__(self,pos=(0,0),dr=90,rnge=3,id='unnamed'):
        things.append(self)
        if dr%90 != 0:
            dr = 0
        self.name=self.__class__.__name__
        self.on_off = True
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.pos = self.x,self.y
        field.remove(self.pos)
        self.direction = dr
        self.range = rnge+1
        self.sight = []
        self.prevsight=[]
        self.insight=[]
        self.changes = memory()
        self.classification=decider(self)
        self.brain=brain(self)
        self.reset_vision()
    def reset_vision(self):
        self.sight=[]
        if self.on_off:
            if self.direction == 0 or self.direction == 360:
                self.direction = 0
                for i in range(1,self.range):
                    for z in range(-i,i+1):
                        self.sight.append((self.x+z,self.y+i))
            if self.direction == 90:
                for i in range(1,self.range):
                    for z in range(-i,i+1):
                        self.sight.append((self.x+i,self.y+z))
            if self.direction == 180: 
                for i in range(1,self.range):
                    for z in range(-i,i+1):
                        self.sight.append((self.x+z,self.y-i))
            if self.direction == 270 or self.direction == -90:
                self.direction == 270
                for i in range(1,self.range):
                    for z in range(-i,i+1):
                        self.sight.append((self.x-i,self.y+z))
            self.detect()
    def detect(self):
        s=0
        self.prevsight=self.insight
        self.insight=[]
        for i in self.sight:
            for x in things:
                if i == x.pos:
                    s=things.index(x)
                    break
            if things[s].pos == i:
                self.insight.append(things[s])
            elif i in field:
                self.insight.append('empty space')
            else:
                self.insight.append('OOB')
        if self.insight != self.prevsight:
            self.findchange()
        else:
            self.changes.memorize('no change')
    def findchange(self):
        if self.prevsight != []:
            for i in range(len(self.prevsight)):
                if self.prevsight[i] != self.insight[i]:
                    self.changes.memorize((self.sight[i],self.prevsight[i],self.insight[i]))
    def eval(self):
        imm=[]
        for i in self.changes.mem:
            if i[1]== 0:
                imm.append(i[0])
        if len(imm) >=2:
            self.classification.find(imm,tck)

    def switch(self):
        if self.on_off:
            self.on_off = False
        else:
            self.on_off = True
#Blocks cells from usage
class Wall:
    def __init__(self,pos=(1,1),movable=False):
        self.name=self.__class__.__name__
        self.on_off = True
        self.x = pos[0]
        self.y = pos[1]
        self.pos = (self.x,self.y)
        walls.append(self)
        positions.remove(self.pos)
        things.append(self)
        self.movable=movable
    def move(self):
        pass
#Goblin, standard creature
class goblin:
    def __init__(self,pos=(0,0),dir=0,id='goblin'):
        things.append(self)
        self.name=self.__class__.__name__
        self.id = id
        if dir%90 != 0:
            dir = 0
        self.direction=dir
        self.x = pos[0]
        self.y = pos[1]
        self.pos = self.x,self.y
        field.remove(self.pos)
        self.brain=brain(self)
    def move(self):
        if self.direction==0 or self.direction==360:
            self.direction=0
            where = self.pos[0],self.pos[1]+1
            if where in field:
                field.append(self.pos)
                self.pos=where
                field.remove(self.pos)
                self.x=self.pos[0]
                self.y=self.pos[1]
            else:
                print("Goblin tried to go somewhere forbidden...")
        if self.direction==90:
            where = self.pos[0]+1,self.pos[1]
            if where in field:
                field.append(self.pos)
                self.pos=where
                field.remove(self.pos)
                self.x=self.pos[0]
                self.y=self.pos[1]
            else:
                print("Goblin tried to go somewhere forbidden...")
        if self.direction==180:
            where = self.pos[0],self.pos[1]-1
            if where in field:
                field.append(self.pos)
                self.pos=where
                field.remove(self.pos)
                self.x=self.pos[0]
                self.y=self.pos[1]
            else:
                print("Goblin tried to go somewhere forbidden...")
        if self.direction==270 or self.direction==-90:
            self.direction=270
            where = self.pos[0]-1,self.pos[1]
            if where in field:
                field.append(self.pos)
                self.pos=where
                field.remove(self.pos)
                self.x=self.pos[0]
                self.y=self.pos[1]
            else:
                print("Goblin tried to go somewhere forbidden...")
    def tp(self):
        where = random.choice(field)
        if where in field:
            field.append(self.pos)
            self.pos=where
            field.remove(self.pos)
            self.x=self.pos[0]
            self.y=self.pos[1]

    def turn(self):
        rand=random.randint(1,100)
        if rand <=40:
            self.direction-= 90
        elif rand >= 60:
            self.direction+= 90
        else:
            pass
#Holds data
class memory:
    def __init__(self,t='data'):
        self.mem=[]

    def memorize(self,obj):
        self.mem.append([obj,0])
    def passage(self):
        for i in range(len(self.mem)):
            self.mem[i][1]+=1
#Does the AI shit
class decider():
    def __init__(self, creature):
        self.identity=creature
    def find(self,gatheredata='???',tick=0):
        for x in gatheredata:
            class1odds=0
            class2odds=0
            class3odds=0
            was = x[1]
            became=x[2]
            nearby=adj(x[0])
            for m in gatheredata:
                if m != x:
                    if m[2] == was:
                        if m[1] == became:
                            if m[0] in nearby:
                                for b in mm.class1:
                                    class1odds+=1
                                gatheredata.remove(x)
                                gatheredata.remove(m)
                                break
                            else:
                                for b in mm.class2:
                                    class2odds+=1
                                gatheredata.remove(x)
                                gatheredata.remove(m)
                                break
                        else:
                            if m[1] != 'empty space':
                                otherwas = m[1]
                                otherbecame=m[2]
                                othernearby = adj[m[0]]
                                for w in gatheredata:
                                    if w[2] == otherwas:
                                        for l in othernearby:
                                            if w[0] == l:
                                                for b in mm.class2:
                                                    class3odds+=1
                                                break
                                            else:
                                                print('Unknown?? this isnt close to any recorded data.')
                                    else:
                                        print('Unknown?? this isnt close to any recorded data.')
            endresult = []
            for i in range(class1odds):
                endresult.append('class1')
            for i in range(class2odds):
                endresult.append('class2')
            for i in range(class3odds):
                endresult.append('class3')
            fin = random.choice(endresult)
            print('end result is '+fin)
            choices.mem.append((fin,[str(x),str(m)],tick))         
#Logical Thinking
class brain:
    def __init__(self,creature):
        self.identity = creature
def adj(space=(0,0)):
    s1 = (space[0]+1,space[1])
    s2 = (space[0]-1,space[1])
    s3 = (space[0],space[1]+1)
    s4 = (space[0],space[1]-1)
    return s1,s2,s3,s4
def wall(x=1,y=1,movable=False):
    block=Wall((x,y),movable)
def tick():
    global tck
    tck+=1
    print('tick '+str(tck))
    for i in things:
        if i.name=='detector':
            if i.on_off:
                i.detect()
                i.eval()
                i.changes.passage()
        if i.name=='goblin':
            moverng=random.randint(1,10)
            if moverng > 5:
                i.move()
            if moverng < 5:
                i.tp()
            i.turn()
        else:
            pass
def save():
    for i in choices.mem:
        with open("mm.py", "a") as f:
            f.write("\n    "+str(i[0])+'.append('+str(i[1])+')')
choices=memory()
walls=[]
things=[]
field = []
positions=[]
tck=0
for x in range(1,101):
    for y in range(1,101):
        field.append((x,y))
        positions.append(field[-1])
d1=detector((1,50),90,50,'D1')
gobby=goblin((50,50),0,'gobby')
mm.setup()
try:
    for i in range(int(input('How many ticks? '))):
        tick()
except:
    tick()
for i in choices.mem:
    print(i)
save()
