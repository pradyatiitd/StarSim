"""
    @ author Ayush Verma and Pradyumna meena
"""
import random           # FOR RANDOM BEGINNINGS
from Tkinter import *   # ALL VISUAL EQUIPMENT


""" Initialisation of Constant
"""
WIDTH = 800
HEIGHT = 600            # OF SCREEN IN PIXELS 600
BOIDS = int(raw_input("Enter no of birds = "))             # IN SIMULATION
WALL = random.randint(50, 100)              # FROM SIDE IN PIXELS
WALL_FORCE = random.randint(5, 15)        # ACCELERATION PER MOVE
SPEED_LIMIT = 500       # FOR BOID VELOCITY
BOID_RADIUS = 5        # FOR BOIDS IN PIXELS
OFFSET_START = random.randint(10, 50)      # FROM WALL IN PIXELS

################################################################################



""" TWO DIMENTIONAL VECTOR CLASS
"""
class TwoD:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return 'TwoD(%s, %s)' % (self.x, self.y)

    def __add__(self, other):
        return TwoD(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return TwoD(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return TwoD(self.x * other, self.y * other)

    def __div__(self, other):
        return TwoD(self.x / other, self.y / other)

    def mag(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

################################################################################

def build_gui():
    """ Build GUI environment """
    global graph
    root = Tk()
    root.title("BOID SIMULATION")
    root.geometry('%dx%d' % (WIDTH, HEIGHT))
    b = Button(root, text ="Add Boid", command = build_boids)
    b.pack() 
    graph = Canvas(root, width=WIDTH, height=HEIGHT, background='SkyBlue')
    graph.after(4, update)
    
    graph.pack()

def update():
    """ Main simulation loop."""
    draw()
    move()
    graph.after(4, update)

def draw():
    """ Draw all boids"""
    graph.delete(ALL)
    for boid in boids:
        x1 = boid.position.x - BOID_RADIUS
        y1 = boid.position.y - BOID_RADIUS
        x2 = boid.position.x + BOID_RADIUS + 5
        y2 = boid.position.y + BOID_RADIUS + 5
        
        graph.create_arc((x1, y1, x2, y2), fill='black')
    graph.update()

def move():
    """ Move all boids"""
    for boid in boids:
        simulate_wal(boid)
    for boid in boids:
        boid.update_velocity(boids)
    for boid in boids:
        boid.move()

def simulate_wal(boid):
    """ Create viewing boundaries."""
    if boid.position.x < WALL:
        boid.velocity.x += WALL_FORCE
    elif boid.position.x > WIDTH - WALL:
        boid.velocity.x -= WALL_FORCE
    if boid.position.y < WALL:
        boid.velocity.y += WALL_FORCE
    elif boid.position.y > HEIGHT - WALL:
        boid.velocity.y -= WALL_FORCE

def limit_speed(boid):
    """ Limit boid speed."""
    if boid.velocity.mag() > SPEED_LIMIT:
        boid.velocity /= boid.velocity.mag() / SPEED_LIMIT

def build_boid_button():
    """create boid vaiable on button event"""
    global boids
    
    b = tuple(Boid(WIDTH, HEIGHT, OFFSET_START)) 
    boids = (boids,b)

def build_boids():
    """ Create boids variable."""
    global boids
    global BOIDS
    BOIDS +=1
    boids = tuple(Boid(WIDTH, HEIGHT, OFFSET_START) for boid in xrange(BOIDS-1))



################################################################################


""" BOID RULE IMPLEMENTATION CLASS
"""
class Boid:

    def __init__(self, width, height, offset):
        """initializing boids"""
        self.velocity = TwoD(0, 0)
        self.position = TwoD(*self.random_start(width, height, offset))

    def random_start(self, width, height, offset):
        """initializing boid positions"""
        y = random.randint(1, height)
        x = -offset
        
        
        return x, y


    def update_velocity(self, boids):
        v1 = self.rule1(boids)
        v2 = self.rule2(boids)
        v3 = self.rule2(boids)
        self.__temp = v1 + v2 + v3

    def move(self):
        self.velocity += self.__temp
        limit_speed(self)
        self.position += self.velocity / 50  #vv

##############################################

    # def limit_speed(self):
    #     """Limiting the boid's speed
    #     """
    #     if self.velocity == 0:
    #         self.velocity *= 0
    #         return
    #     if self.velocity.mag() > self.velocity_max:
    #         self.velocity /= self.velocity.mag() / self.velocity_max
##############################################
    def rule1(self, boids):
        
        """cohesion"""
        vector = TwoD(0, 0)
        for boid in boids:
            if boid is not self:
                vector += boid.position
        vector /= len(boids) - 1
        return (vector - self.position) / 2

    def rule2(self, boids):
        """separation"""
        vector = TwoD(0, 0)
        for boid in boids:
            if boid is not self:
                if (self.position - boid.position).mag() < 15:
                    vector -= (boid.position - self.position)
        return vector

    def rule3(self, boids):
        """Alignment"""
        vector = TwoD(0, 0)
        for boid in boids:
            if boid is not self:
                vector += boid.velocity
        vector /= len(boids) - 1
        return (vector - self.velocity)
    
    # def stay_in_boundary(self):
    #     """Returns the vector to push the boid back insde the boundary if it's
    #     outside. Otherwise, returns Vec3D(0, 0, 0).
    #     """
    #     bound = Vec3D(0, 0, 0)
    #     if self.boundary is not None:
    #         bound = self.boundary.correction(self)
    #     return bound

    # def avoid_obstacles(self):
    #     """Compile the correctoin from all the obstacles."""
    #     compiled = Vec3D(0, 0, 0)
    #     for obstacle in self.obstacles:
    #         compiled += obstacle.correction(self)
    #     return compiled 

################################################################################
"""Starting the program"""
build_boids()
build_gui()
mainloop()

