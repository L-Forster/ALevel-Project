import noise
import pygame as pg # pg is easier to write than pygame
import random
import math
import menus
from constants import *
from validation import *


##SPOILED OIL##

#validates the values in highScores.txt
validate_scores()


        
# loads the main menu
menus.menu_create()


level_dimensions = [1500,1000] # x and y dimensions of the generated level
level_dimensions_mid =[int(level_dimensions[0]/2),int(level_dimensions[1]/2)] # the mid point of those dimensions 


#CLASSES

class Characters_class(pg.sprite.Sprite): # the character has to be in the centre of the window
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        x = random.randint(0,level_dimensions[0]) #spawns at random coordinates 
        y = random.randint(0,level_dimensions[1])
        self.rect.x = x
        self.rect.y = y



class Entities_class(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        x = random.randint(0,level_dimensions[0]) #spawns at random coordinates 
        y = random.randint(0,level_dimensions[1])
        self.rect.x = x
        self.rect.y = y

        
        
class Level_class(pg.sprite.Sprite): # class of the level 
    def __init__(self):
        self.seed=random.randint(0,99) #random value which determines the seed used for the noise
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([level_dimensions[0],level_dimensions[1]]) #creates a surface with dimensions the same as the level.
        self.rect = self.image.get_rect()
        self.speed = 5*2**0.5 # the maximum amount the level can move in a frame
        self.vel = pg.Vector2(0,0) 
        self.colour_threshold = 0.0825 # If noise values are greater than this it will be coloured.
        self.image.fill(BG) 
        self.rect.center = (DIMENSIONS[0]//2 , DIMENSIONS[1]//2) # the rect coordinates refer to the centre of the level

    #generating the level noise values.  
    def level_generate(self):


        self.level_noise = []
        self.image.fill(BG)
        # level_noise = [[0]*level_dimensions[0]]*level_dimensions[1] will copy the digit '0' for each index 
      #instead of creating an empty 2D list.
        for x in range(0,level_dimensions[0]-1): # creating the 2d list which will store the noise values
            row = []
                
            for y in range(0,level_dimensions[1]-1):
                row.append(0)
                self.level_noise.append(row)
                    
        for x in range(0,level_dimensions[0]-1): #for every x pixel
            for y in range(0,level_dimensions[1]-1): #for every y pixel
                # creating the noise for each pixel.
                self.level_noise[x][y] = noise.pnoise2(x/100, y/100, octaves=8,persistence = 0.25, lacunarity = 1.7, repeatx = level_dimensions[0], repeaty = level_dimensions[1],base=self.seed)  
            
                if not(((x - level_dimensions_mid[0])**2)**0.5 < 40 and ((y - level_dimensions_mid[1])**2)**0.5 < 40): # if distance
                            #between centre and coordinate is larger than "a value" fill in normally

                    if self.level_noise[x][y]>self.colour_threshold: #if the generated noise value at the coordinates is greater than this, then it will be coloured in
                        self.image.set_at((x,y), LEVEL_COLOUR)
                else: #otherwise create spawn platform
                    self.image.set_at((x,y), SPAWN_COLOUR)
                
        # Creating the walls around the level        
        for x in range(0,level_dimensions[0]): # Creates the vertical border walls on the left and right sides of the level.
            for y in range (0,level_dimensions[1]):
                if x < 17 or x > level_dimensions[0]-18:
                    self.image.set_at((x,y), LEVEL_COLOUR) # sets it to the same colour as the impassable areas
                    
        for y in range(0,level_dimensions[1]):   # Creates the horizontal border walls on the top and bottom edges of the level.  
            for x in range (0,level_dimensions[0]):
                if y < 17 or y > level_dimensions[1]-18:
                    self.image.set_at((x,y), LEVEL_COLOUR) # sets it to the same colour as the impassable areas


        # Creating the border around the walls, so the background of the game is the same as 'BG'      
        for x in range(0,level_dimensions[0]): # Creates the vertical border on the left and right sides of the level.
            for y in range (0,level_dimensions[1]):
                if x < 9 or x > level_dimensions[0]-10:
                    self.image.set_at((x,y), BG) 
                    
        for y in range(0,level_dimensions[1]): # Creates the horizontal border on the top and bottom edges of the level.      
            for x in range (0,level_dimensions[0]):
                if y < 9 or y > level_dimensions[1]-10:
                    self.image.set_at((x,y), BG) 



    #keys that are not defined in the below methods do nothing when pressed.                  
    def check_key_type(self):# checks whether the key is pressed down or released
        
        for event in pg.event.get():
            if event.type == pg.QUIT: #if the user presses the 'x', the program will close
                pg.quit()
                
            elif event.type == pg.KEYDOWN: # if a key is pressed down
                self.down_keys(event) # run down_keys method
                
            elif event.type == pg.KEYUP: # if a key is let go
                self.up_keys(event) # run up_keys method
                

    def down_keys(self,event): #when a key is presssed down..
        if event.key == pg.K_ESCAPE:
            pass

        if event.key == pg.K_w: #if they press down w
            self.vel.y -= (self.speed) # level moves down

        if event.key == pg.K_s: # if they press down s
            self.vel.y += (self.speed) # level moves up

        if event.key == pg.K_d: # if they press down d
            self.vel.x += (self.speed) #level moves to the left
            
        if event.key == pg.K_a: #if they press down a
            self.vel.x -= (self.speed) # level moves to the right
            
                #These values are negative of what to be expected because the level is being moved - not the player
    def up_keys(self,event): #when the key is let go..
        
        if event.key == pg.K_w:
            self.vel.y = 0 #sets velocity to zero
            if self.vel.x > 0: #if the player was moving diagonally 
                self.vel.x = self.speed # the x speed should be increased back to self.speed
                
            if self.vel.x < 0: #if the player was moving diagonally
                self.vel.x = -self.speed
                
        if event.key == pg.K_s:
            self.vel.y =0
            if self.vel.x > 0:#x velocity is returned to its original value
                self.vel.x = self.speed
                
            if self.vel.x < 0:
                self.vel.x = -self.speed     
                       
        if event.key == pg.K_d:
            self.vel.x =0
            if self.vel.y > 0:#y velocity is returned to its original value
                self.vel.y = self.speed
                
            if self.vel.y < 0:
                self.vel.y = -self.speed 
                          
        if event.key == pg.K_a:
            self.vel.x =0
            if self.vel.y > 0:#y velocity is returned to its original value
                self.vel.y = self.speed
                
            if self.vel.y < 0:
                self.vel.y = -self.speed            
            
            
    def update(self): #collision checking and updating position of level
        
        self.collision_new_x = level_dimensions_mid[0] 
        self.collision_new_y = level_dimensions_mid[1]
        self.temp_x = self.rect.x  # temporarily stores the current position of the level
        self.temp_y = self.rect.y
        if self.vel.x !=0 and self.vel.y != 0: #Only vectors with both x and y components not equal to zero, can be normalised
            
            self.vel = self.vel.normalize()*self.speed  # so that the player travels at the same speed diagonally as laterally

            
            
        if self.vel.x > 0:
            self.collision_new_x = int(DIMENSIONS[0]//2 + OBJECT_SIZE//2 +1) #sets the coordinate where the player will be colliding
          #with to be the pixel just to the right of the player.
            
        elif self.vel.x < 0:
            self.collision_new_x = int(DIMENSIONS[0]//2 - OBJECT_SIZE//2 -1) # the pixel adjacent to the player in the direction
          #that they are travelling
            
            
        if self.vel.y > 0:
            self.collision_new_y = int(DIMENSIONS[1]//2  + OBJECT_SIZE//2 +1)
            
        elif self.vel.y <0:
            self.collision_new_y = int(DIMENSIONS[1]//2 - OBJECT_SIZE//2 -1)
            
            
        if canvas.get_at((self.collision_new_x,DIMENSIONS[1]//2)) != LEVEL_COLOUR: #collision checking
            #if the colour of the pixel in the direction 
            #if the player's movement is not the colour of the background of the level 
            self.rect.x -= self.vel.x


        if canvas.get_at((DIMENSIONS[0]//2 ,self.collision_new_y)) != LEVEL_COLOUR: # when the player is travelling vertically
            self.rect.y -= self.vel.y
          
        self.position = pg.Vector2(level_dimensions_mid[0] - self.rect.x, level_dimensions_mid[1] - self.rect.y)



      
 
#subclasses
class Computer_class(Entities_class):
    
    def __init__(self,edge_distance,level):
        
        self.direction = "right"
        self.image = pg.Surface([OBJECT_SIZE,OBJECT_SIZE])
        self.rect = self.image.get_rect()
        super().__init__() # inheriting attributes from Entities_class()
        self.image.fill(COMPUTER_COLOUR) # fills it red
        self.speed = 3 #redefines the attributes inherited
        self.rect.x = edge_distance
        self.rect.y =edge_distance
        # if the edge distance is an odd number, the enemy will spawn on the other side of the level
        if edge_distance % 2 == 1: 
            self.rect.x = level_dimensions_mid[0] + edge_distance 
            self.rect.y = level_dimensions_mid[1] + edge_distance
        self.position = pg.Vector2(self.rect.x,self.rect.y)
        self.rect.x = self.position.x + level.rect.x
        self.rect.y = self.position.y + level.rect.y
        self.not_see = False
        
        
    #Computer_class methods    
    
    def target(self,level,player): # True if far from player, false if close to player
        
        self.x_distance_to_player = player.rect.x - self.rect.x
        self.y_distance_to_player = player.rect.y - self.rect.y #calculating the distance from the Computer_class to the player.
        self.player_target = pg.Vector2(self.x_distance_to_player,self.y_distance_to_player) # vector of components distance to player
        
        if math.hypot(self.player_target.x,self.player_target.y) > OBJECT_SIZE * 10  : # if the distance between the player and enemy is greater than vision
            self.not_see = True# player_target vector normalised to have magnitude of 1
            
        elif pg.Rect.colliderect(self.rect, player.rect): # if the enemy is touching the player
            return True # lets the main program know that it needs to create a new level.      
            
    def patrol(self,edge_distance,level): # the square movement of the enemy patrolling, making it move with the level.
        self.position.x = self.rect.x # updates the position to use in this method so it is constant with the rect.
        self.position.y = self.rect.y
        if self.not_see == True: #If the player is not within the enemy's field of view
            level.dx = -level.rect.x +  level.temp_x # assigned the change in level position
            level.dy = -level.rect.y + level.temp_y 
                # Moving right. If the x position is not at the rightmost boundary and it is at the topmost boundary and the last direction travelled was not left
            if (self.position.x < level_dimensions[0] - edge_distance  + level.rect.x) and (self.position.y <= edge_distance + level.rect.y + level.dy) and self.direction != "left":  
                
                self.position.x =  self.speed +self.position.x - level.dx
                self.position.y = self.position.y - level.dy 
                self.direction = "right"
                
                # Moving down. If the y position is less than the boundary and the x position is at the right boundary and it was not previously moving up.
            elif (self.position.y < level_dimensions[1] - edge_distance - level.position.y + level_dimensions[1]//2) and self.direction != "up" and (self.position.x > edge_distance + level_dimensions[0] - level.position.x - level_dimensions[0]//2):
                self.position.y = self.speed + self.position.y - level.dy
                self.position.x = self.position.x - level.dx
                self.direction = "down"
                
            # Moving left. If the x position is not at the leftmost boundary and the last direction travelled was not up or right
            elif (self.position.x > edge_distance  + level_dimensions[0]//2 - level.position.x ) and self.direction != "right" and self.direction != "up" : 
                self.position.x = - self.speed + self.position.x - level.dx
                self.position.y = self.position.y - level.dy
                self.direction = "left"

            # Moving up. If the y position is greater than the boundary and the x position is at the left boundary and it was not previously moving down.
            elif (self.position.y > edge_distance + level_dimensions[1]//2 - level.position.y) and self.direction != "down" and (self.position.x <= level_dimensions[0] - edge_distance - level.position.x + level_dimensions[0]//2):  
                self.position.y =  - self.speed + self.position.y - level.dy 
                self.position.x = self.position.x -level.dx
                self.direction = "up"



    def update(self,level): 
        level.dx = -level.rect.x +  level.temp_x # makes the enemy move with the level when targeting the player
        level.dy = -level.rect.y + level.temp_y 

        if math.hypot(self.player_target.x,self.player_target.y) < OBJECT_SIZE * 10: # if the distance between the player and the enemy is less than..

          
            self.velocity = self.player_target.normalize() * self.speed   # sets the velocity to the distance travelled in that frame
            self.not_see =  False
            self.position.x += self.velocity.x   # updates the position of the enemy
            self.position.y += self.velocity.y 
            self.rect.x += self.velocity.x - level.dx
            self.rect.y += self.velocity.y - level.dy

        else: # if the distance between the player is not less than..
            self.rect.x = self.position.x
            self.rect.y = self.position.y
        
        

class Key_class(Level_class):
 
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([OBJECT_SIZE,OBJECT_SIZE])
        self.rect = self.image.get_rect()
        self.total_keys = 0
        self.rect.x =10000 # the default position is far out of the level
        self.rect.y=10000
        self.collected_keys = 0
        
   #the method for placing the key     
    def key_set_pos(self): # creates a new key
        self.image = pg.Surface([OBJECT_SIZE,OBJECT_SIZE])
        self.rect = self.image.get_rect()
        self.total_keys = 0
        self.rect.x =10000
        self.rect.y=10000        
        self.key_pos = level_dimensions_mid
        # a 2d list of the coordinates of all the adjacent pixels to the key.
        self.adj = [[self.key_pos[0],self.key_pos[1]-1],[self.key_pos[0]+1,self.key_pos[1]],[self.key_pos[0],self.key_pos[1]+1],[self.key_pos[0]-1,self.key_pos[1]]]      
        self.max_attempts = 150
        self.attempt_number = 0
        self.placed = False # 
        #largest distance between centre and the key
        self.greatest_distance = math.hypot(level_dimensions_mid[0], level_dimensions_mid[1]) 

   
    def key_add(self,level): # assigning and creating the position of the key in the level
        if self.total_keys < 1:  # determines the key's position by navigating the level, changing direction each time it collides with a wall.
            self.direction = random.randint(0,3) # The direction corresponds to the adjacencies array 0 = up, 1 = right, etc.
            self.attempt_number += 1 # adds 1 to attempt each time the item changes direction
            
            if self.attempt_number < self.max_attempts: # if has not exceeded max attempts
                 #sets the new position to be the adjacent pixel that is in the direction of travel
                self.key_pos = [self.adj[self.direction][0],self.adj[self.direction][1]]
                self.key_distance = [self.key_pos[0] - level_dimensions_mid[0], self.key_pos[1] - level_dimensions_mid[1]]
                 # the pixel has to not be of the same colour as the level and the key is not place
                while level.image.get_at((self.adj[self.direction][0],self.adj[self.direction][1])) != LEVEL_COLOUR and self.placed == False:
                     #sets the new position to be the adjacent pixel that is in the direction of travel
                    self.key_pos = [self.adj[self.direction][0],self.adj[self.direction][1]]
                  #distance from the centre
                    self.key_distance = [self.key_pos[0] - level_dimensions_mid[0], self.key_pos[1] - level_dimensions_mid[1]]
                  
                    self.adj = [[self.key_pos[0],self.key_pos[1]-1],[self.key_pos[0]+1,self.key_pos[1]],[self.key_pos[0],self.key_pos[1]+1],[self.key_pos[0]-1,self.key_pos[1]]]
                    # The distance from the centre divided by the greatest distance will always be < 1 and >0
                    # This value is at its greatest when the distance is greatest       
                    if (random.expovariate(0.01+(math.hypot(self.key_distance[0],self.key_distance[1])/(self.greatest_distance)))**0.5) < 0.02 and (self.key_distance[0]**2)**0.5 < level_dimensions_mid[0]-30 and (self.key_distance[1]**2)**0.5 < level_dimensions_mid[1]-30  :    
                        # exponential distribution has to be greater than zero. proportional to the distance from centre. 

                        
                        
                        self.key_pos[0] -= OBJECT_SIZE//2
                        self.key_pos[1] -= OBJECT_SIZE//2
                        self.rect.x = self.key_pos[0]
                        self.rect.y = self.key_pos[1]
                        self.image.fill(KEY_COLOUR) 
                        self.placed = True
                        self.total_keys = 1  
                        
                if self.placed == False:   
                    self.key_add(level)
                    
            else:
                       
                  
                self.key_pos[0] -= OBJECT_SIZE//2
                self.key_pos[1] -= OBJECT_SIZE//2
                self.rect.x = self.key_pos[0]
                self.rect.y = self.key_pos[1] 
                self.image.fill(KEY_COLOUR) 
                self.placed = True
                self.total_keys = 1  
                

        
        
    def remove_key(self,player): # for hiding the key
        if pg.Rect.colliderect(player.rect,self.rect):
            self.total_keys =0
            self.rect.x = 10000 # sends the square far away. so that what is below it is shown
            self.rect.y = 10000
            self.collected_keys += 1 # incremented the number of collected keys by one
            return True
        
        else:
            return False    
        
        
    def update(self,level): # makes the key move with the level.
        if self.rect.x != 10000:
            self.rect.x = level.rect.x + self.key_pos[0]
            self.rect.y = level.rect.y + self.key_pos[1]       

            
class Player_class(Characters_class):
    
    def __init__(self):
        self.image = pg.Surface([OBJECT_SIZE,OBJECT_SIZE])
        self.rect = self.image.get_rect() #creates a rectangle for the player
        super().__init__()
        self.image.fill(CHARACTER_COLOUR) # fills the player's rectangle in green
        self.rect.center = (DIMENSIONS[0]//2, DIMENSIONS[1]//2)




##MAIN CODE

pg.init()

canvas = pg.display.set_mode(DIMENSIONS)
        
pg.display.set_caption("Spoiled Oil") #name of the title
        
clock = pg.time.Clock()
        
#CREATING THE OBJECTS TO BE USED IN THE GAME      
allSpriteGroup = pg.sprite.Group()

canvas.fill(BG)
pg.Surface((DIMENSIONS[0],DIMENSIONS[1]), flags=0, depth=8)
            
            
level = Level_class()
level.level_generate()
allSpriteGroup.add(level)
            
player = Player_class()
allSpriteGroup.add(player)
            
key_to_get = Key_class()
key_to_get.key_set_pos()
key_to_get.key_add(level)
allSpriteGroup.add(key_to_get)
            
allSpriteGroup.draw(canvas)
        
enemy = Computer_class(E1_EDGE_DISTANCE,level )
allSpriteGroup.add(enemy)
enemy_2 = Computer_class(E2_EDGE_DISTANCE,level )
allSpriteGroup.add(enemy_2)

level.rect.x = - level_dimensions[0] + DIMENSIONS[0] + (level_dimensions[0] - DIMENSIONS[0])//2
level.rect.y = - level_dimensions[1] + DIMENSIONS[1] + (level_dimensions[1] - DIMENSIONS[1])//2
running = True
    
while running:

    level.check_key_type()
    level.update()
    
    enemy.target(level,player)
    if enemy.target(level,player):
        running = False    
    enemy.patrol(E1_EDGE_DISTANCE,level)
    enemy.update(level)
    
    enemy_2.target(level,player)
    if enemy_2.target(level,player):
        running = False    
    enemy_2.patrol(E2_EDGE_DISTANCE,level)
    enemy_2.update(level)    
    
    key_to_get.key_add(level)
    key_to_get.update(level)
    if key_to_get.remove_key(player):
        key_to_get.key_set_pos()
    allSpriteGroup.draw(canvas)
    
    score_font = pg.font.SysFont("Gadugi",52, True) # Font used in everything else. creates a font with bold True
    
    #score text
    score = key_to_get.collected_keys * 100 
    score_text = score_font.render("SCORE: "+str(score),True, "#000000", "#FFFFFF")
    canvas.blit(score_text,(920,0))  
    pg.display.update()
    clock.tick(60)
    
    

##managing high scores

sorted = False
#files
highScores = open("highScores.txt","r")
lines = highScores.readlines()

if score > int(lines[4]):
    highScores = open("highScores.txt","w")
    for i in range(len(lines)-1): # writes the first 4 items and  the new score
        highScores.write(lines[i])
    highScores.write(str(score))
    
highScores = open("highScores.txt","r+")
#sort new scores
lines = highScores.readlines()

while not(sorted):
    passes= 0
    for i in range(len(lines)-1):
        if int(lines[i]) < int(lines[i+1][0:]) or int(lines[i]) < int(lines[i+1]):
            temp=lines[i]
            lines[i] = lines[i+1]
            lines[i+1]=temp
            passes += 1
    if passes == 0:
        sorted = True
        
highScores = open("highScores.txt", "w")

for i in range(len(lines)):  #putting the new scores into the file.
    if lines[i] == str(score):
        lines[i] = "#"+str(lines[i]) +str("\n")
        
    highScores.write(lines[i])   
    
highScores.close()

##
key_to_get.collected_keys = 0
menus.menu_running = True  # guarantees that the menu will be run 
menus.intermission(lines)


highScores = open("highScores.txt", "r+") #This guarantees that the most recent version of the file is used.
lines = highScores.readlines()
highScores.close()
highScores = open("highScores.txt", "w")
for i in range(5): 
    if str(lines[i].strip("\n")[1:]) == str(score):
        lines[i] = str(lines[i][1:])
    else:      
        lines[i] = str(lines[i])
    highScores.write(lines[i])  
    
highScores.close()


def mainloop():
    canvas = pg.display.set_mode(DIMENSIONS)
        
    pg.display.set_caption("Spoiled Oil") #name of the title
            
    clock = pg.time.Clock()
            
            #defining the objects and adding them to the sprite group
            
    allSpriteGroup = pg.sprite.Group()
    
    canvas.fill(BG)
    pg.Surface((DIMENSIONS[0],DIMENSIONS[1]), flags=0, depth=8)
                
                
    level = Level_class()
    level.level_generate()
    allSpriteGroup.add(level)
                
    player = Player_class()
    allSpriteGroup.add(player)
                
    key_to_get = Key_class()
    key_to_get.key_set_pos()
    key_to_get.key_add(level)
    allSpriteGroup.add(key_to_get)
                
    allSpriteGroup.draw(canvas)
            
    enemy = Computer_class(E1_EDGE_DISTANCE,level )
    allSpriteGroup.add(enemy)
    enemy_2 = Computer_class(E2_EDGE_DISTANCE,level )
    allSpriteGroup.add(enemy_2)
    
    level.rect.x = - level_dimensions[0] + DIMENSIONS[0] + (level_dimensions[0] - DIMENSIONS[0])//2
    level.rect.y = - level_dimensions[1] + DIMENSIONS[1] + (level_dimensions[1] - DIMENSIONS[1])//2
    running = True
        
    while running:

        level.check_key_type()
        level.update()
        

        enemy.target(level,player)
        if enemy.target(level,player):
            running = False    
        enemy.patrol(E1_EDGE_DISTANCE,level)
        enemy.update(level)
        
        enemy_2.target(level,player)
        if enemy_2.target(level,player):
            running = False    
        enemy_2.patrol(E2_EDGE_DISTANCE,level)
        enemy_2.update(level)    
        
        key_to_get.key_add(level)
        key_to_get.update(level)
        if key_to_get.remove_key(player):
            key_to_get.key_set_pos()

        allSpriteGroup.draw(canvas)
        #score text
        score = key_to_get.collected_keys * 100 
        score_text = score_font.render("SCORE: "+str(score),True, "#000000", "#FFFFFF")
        canvas.blit(score_text,(920,0))     
        pg.display.update()
        clock.tick(60)
        
    ##managing high scores COPIED CODE FROM FIRST LEVEL


    ##managing high scores
    
    sorted = False
    #files
    highScores = open("highScores.txt","r")
    lines = highScores.readlines()
    
    if score > int(lines[4]):
        highScores = open("highScores.txt","w")
        for i in range(len(lines)-1): # writes the first 4 items and  the new score
            highScores.write(lines[i])
        highScores.write(str(score))
        
    highScores = open("highScores.txt","r+")
    #sort new scores
    lines = highScores.readlines()
    
    while not(sorted):
        passes= 0
        for i in range(len(lines)-1):
            if int(lines[i]) < int(lines[i+1][0:]) or int(lines[i]) < int(lines[i+1]):
                temp=lines[i]
                lines[i] = lines[i+1]
                lines[i+1]=temp
                passes += 1
        if passes == 0:
            sorted = True
                
    highScores = open("highScores.txt", "w")
    
    for i in range(len(lines)):  #putting the new scores into the file.
        if lines[i] == str(score):
            lines[i] = "#"+str(lines[i]) +str("\n")
            
        highScores.write(lines[i])   
        
    highScores.close()
    key_to_get.collected_keys = 0    
        

    menus.menu_running = True # guarantees that the button is still not pressed when each menu is up
    menus.intermission(lines)
    
    highScores = open("highScores.txt", "r+")
    lines = highScores.readlines()
    highScores.close()
    highScores = open("highScores.txt", "w")
    for i in range(5): 
        if str(lines[i].strip("\n")[1:]) == str(score):
            lines[i] = str(lines[i][1:])
        else:      
            lines[i] = str(lines[i])
        highScores.write(lines[i])  
    highScores.close()



        
        
while pg.event != pg.QUIT: # MAIN LOOP
    mainloop()  



pg.quit()

