import pygame, sys, random #imports pygame to make the game function, sys to help exit of the application and random to randomize the apple everytime it is eaten
from pygame.math import Vector2 #imports vector2 to make it easier to store x,y values in a list.
 
class SNAKE(pygame.sprite.Sprite): #Snake class to serve as templete for snake one and two.
    def __init__(self, position):
        super().__init__()
        self.body = position #Body is set as position so I can set any vector2 values in the main game class.
        self.direction = Vector2(0,0) #Makes the snakes not move when staring
        self.new_block = False #To make it so snake doesn't infinitly grow without even eating the apple yet.
        
        #Images for snake one, convert_alpha is to prevent any errors in the future.
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha() 
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
            
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
 
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
 
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
 
    def draw_snake(self): #Updates and draws the images on the surface depending on where the snake is looking
        self.update_head_graphics() #function to make vector to 1 and 0 in x,y, this allows us to find the relation with the head and body
        self.update_tail_graphics()#function to make vector to 1 and 0 in x,y, this allows us to find the relation with the tail and body
        
        for index, block in enumerate(self.body): #checkss the number of items in the list and each object inside.
            
            #This makes it so we can change x,y individually
            x_pos = int(block.x * cell_size) #Set x_pos as cell_size
            y_pos = int(block.y * cell_size) #set y_pos as cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size) #Makes a rectangle for the snake and sets it as the size of the cell
 
            if index == 0: #Checks the first object in the list (Head)
                screen.blit(self.head, block_rect) #Sets all the head images on the head
            elif index == len(self.body) -1: #Gets all the elements in the list and goes the the last element to find the tail at all times.
                screen.blit(self.tail, block_rect) #Sets all tail images as a tail
            else:
                previous_block = self.body[index + 1] - block 
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x: #Checks if the x in the x,y coordinates are similar
                    screen.blit(self.body_vertical, block_rect) #If x values are the same, it means it is not changing, therefore we can add a vertical body
                elif previous_block.y == next_block.y: #Checks if the y in the x,y coordinates are similar
                    screen.blit(self.body_horizontal, block_rect) #If y values are the same, it means it is not changing, therefore we can add a horizontal body
                else:
                    #Checks if the blocks before and after it to determine where to place a corner block
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1: #Checks if previous and next blocks are on top and left
                        screen.blit(self.body_tl, block_rect) #If true it is, place rect with corner image to match the movement of snake
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1: #Checks if previous and next blocks are on top and right
                        screen.blit(self.body_tr, block_rect) #If true it is, place rect with corner image to match the movement of snake
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1: #Checks if previous and next blocks are on bottom and left
                        screen.blit(self.body_bl, block_rect) #If true it is, place rect with corner image to match the movement of snake
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1: #Checks if previous and next blocks are on bottom and right
                        screen.blit(self.body_br, block_rect) #If true it is, place rect with corner image to match the movement of snake
 
    def update_head_graphics(self): #Finds relation with head and body to use for images
        head_relation = self.body[1] - self.body[0] #Head relation will equal the element before the head subtracted by the head value.
        if head_relation == Vector2(1, 0): #If it equals 1,0 than execute command under
            self.head = self.head_left #Head will be looking at the left
        elif head_relation == Vector2(-1, 0): #If it equals -1,0 than execute command under
            self.head = self.head_right #Head will be looking at the right
        elif head_relation == Vector2(0, 1): #If it equals 0,1 than execute command under
            self.head = self.head_up #Head will be looking up
        elif head_relation == Vector2(0, -1): #If it equals 0,-1 than execute command under
            self.head = self.head_down #Head will be looking down
 
    def update_tail_graphics(self): #Finds relation with tail and body to use for images
        tail_relation = self.body[-2] - self.body[-1] #tail relation will equal the element after the tail subtracted by the tail value.
        if tail_relation == Vector2(1, 0): #If it equals 1,0 than execute command under
            self.tail = self.tail_left #Tail will look to the left
        elif tail_relation == Vector2(-1, 0): #If it equals -1,0 than execute command under
            self.tail = self.tail_right #Tail will look to the right
        elif tail_relation == Vector2(0, 1): #If it equals 0,1 than execute command under
            self.tail = self.tail_up #Tail will look up
        elif tail_relation == Vector2(0, -1): #If it equals 0,-1 than execute command under
            self.tail = self.tail_down #Tail will look down
 
    def move_snake(self): #Inserts new block in list whenever it eats an apple
        if self.new_block == True: #When ever the new_block is True, execute the command under
            body_copy = self.body[:] #Set a new variable that stores the list of the body
            body_copy.insert(0, body_copy[0] + self.direction) #Insert a new block at the start of the list
            self.body = body_copy[:] #Set the body as the whole of the body_copy to essentially return a new list
            self.new_block = False #Sets as False so doesn't infinitly loop, growing super long
        else: 
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self): #Makes a function for new_block
        self.new_block = True #New_block is True
    
    def reset(self): #When original snake dies, it will reset with these values set
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] #sets the length and location of snake
        self.direction = Vector2(0,0) #makes snake not move at start of respawn
 
    def reset2(self): #When second snake dies, it will reset with these values set
        self.body = [Vector2(11, 10), Vector2(12, 10), Vector2(13, 10)] #sets the length and location of snake
        self.direction = Vector2(0,0) #makes snake not move at start of respawn
        
class FRUIT: #Fruit class to create and set inputs for apples, also it will randomizde each time it collides with snake
    def __init__(self, image): #Initializes image and randomize function, also added second argument (image) to 
        self.randomize() #Initializes the randomize function
        self.image = pygame.image.load(image).convert_alpha() #Initializes a general code for both apple images
        
    def draw_fruit(self): #Function to draw rectangle and attach image on it
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size) #Makes apple the size of a cell and sets an x,y as a changeble variable so we can randomize it 
        screen.blit(self.image, fruit_rect) #Sets a general image variable on a rect
    
    def randomize(self): #The randomizing function whenever it collids with snake
        self.x = random.randint(0, cell_number - 1) #Creates a random position within the x range of the screen
        self.y = random.randint(0, cell_number - 1)#Creates a random position within the y range of the screen
        self.pos = Vector2(self.x, self.y) #Because we have a random x, y position, we set it as self.pos and use it when we draw the fruit to randomize its position
 
class MAIN: #Main class where the snake and apple comes together
    def __init__(self): #Initializes fruit snake and second image of snake
        self.snake = SNAKE([Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]) #Original snake takes in different x,y value to start in different place and set length
        self.snake2 = SNAKE([Vector2(11, 10), Vector2(12, 10), Vector2(13, 10)])#Second snake takes in different x,y value to start in different place and set length
        self.fruit = FRUIT('Graphics/apple.png') #Sets fruit class to take in different apple image
        self.fruit2 = FRUIT('Graphics/apple_2.png') #Sets fruit class to take in different apple image
        self.change_color() #Second snake function to take in new images to change color
                          
    def update(self): #updates the collision and movement of snake and apple in the while loop
        self.snake.move_snake() #Move snake function placed in update 
        self.snake2.move_snake() #Move second snake function place in update 
        self.check_fail() #Checks original snake collision against the boundaries of the game and if it hits itself
        self.check_fail2() #Checks second snake collision against the boundaries of the game and if it hits itself
        self.check_collision() #Checks if the snake is colliding with the original apple
        self.check_collision2() #Checks if the second snake is collidiing with the second apple
        self.check_snake() #Checks which of the two snakes are colliding with eatchother
         
    def draw_elements(self): #Draws the green tiles of the game, snake and fruit
        self.draw_grass() #The grass of the game is made of rectangles  so it needs to be drawn
        self.fruit.draw_fruit() #Draws the fruit rectangle 
        self.fruit2.draw_fruit() #Draws the second fruit rectangle
        self.snake.draw_snake() #Draws all the elements in the snake as a rectangle
        self.snake2.draw_snake() #Draws all the elements in the second snake as a rectangle
    
    def check_collision(self): #Checks the collision of the snake against the walls of the game and randomzies when apple spawns on snake itself
        if self.fruit.pos == self.snake.body[0]: #If the apple position is the same as a the snakes head it will initialize the randomizing function and add a new block in the snake list
            self.fruit.randomize() #Randomizes apple position when the if statement is true
            self.snake.add_block() #adds new block in snake list when the if statement is true
 
        for block in self.snake.body[1:]: #Takes all the values of the body and tail but not the head
            if block == self.fruit.pos: #If the apple spawns on top of the snake that is not on the head it will randomize again
                self.fruit.randomize() #Randomizes when if statement is true
    
    def check_collision2(self): #Checks the collision of the second snake against the walls of the game and randomzies when apple spawns on second snake itself
        if self.fruit2.pos == self.snake2.body[0]: #If the apple position is the same as a the second snakes head it will initialize the randomizing function and add a new block in the second snake list
            self.fruit2.randomize() #Randomizes apple position when the if statement is true
            self.snake2.add_block() #adds new block in snake list when the if statement is true
 
        for block in self.snake2.body[1:]: #Takes all the values of the body and tail but not the head
            if block == self.fruit2.pos: #If the apple spawns on top of the second snake that is not on the head it will randomize again
                self.fruit2.randomize() #Randomizes when if statement is true
 
    def check_fail(self): #If the snake touches the boundaries or itself at any point and will game over itself
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: #Checks is the head of the snake.body is toucing the x and y axis of the game it will set as true
            self.game_over() #Snake will die and respawn
        
        for block in self.snake.body[1:]: #Checks all the elements in the list except for the head
            if block == self.snake.body[0]: #If the the list we checked is at any point the same position as the head it will game_over
                self.game_over() #Snake will die and respawn snake
 
    def check_fail2(self): #If the second snake touches the boundaries or itself at any point and will game over itself
        if not 0 <= self.snake2.body[0].x < cell_number or not 0 <= self.snake2.body[0].y < cell_number: #Checks is the head of the second snake.body is toucing the x and y axis of the game it will set as true
            self.game_over2() #Second snake will die and respawn
        
        for block in self.snake2.body[1:]: #Checks all the elements in the list except for the head
            if block == self.snake2.body[0]: #If the the list we checked is at any point the same position as the head it will game_over
                self.game_over2() #Second snake will die and respawn
 
    def check_snake(self): #Checks if the snakes are touching eachother
        for block in self.snake2.body[:]: #Checks all the elements in the second snake
            if block == self.snake.body[0]: #If the list is the same as the original snakes head it will kill the original snake
                self.game_over() #Original snake will die
 
        for block in self.snake.body[:]: #Checks all the elements in the original snake
            if block == self.snake2.body[0]: #If the list is the same as the second snakes head it will kill the second snake
                self.game_over2() #Original second snake will die
                               
            
    def game_over(self): #When ever game_over is called it will reset the original snake
        self.snake.reset() #Original snake resets its position and length
 
    def game_over2(self): #When ever game_over2 is called it will reset the second snake
        self.snake2.reset2() #Second snake resets its position and length
 
    def draw_grass(grass): #Creates the grass of the game
        grass_color = (130, 209, 61) #Sets the grass color to be different from the original screen color
        for row in range(cell_number): #Checks the amount of cell numbers (20) for the row
            if row % 2 == 0: #each number in the list will be divided and will find the remainder and checks if it is equal to 0
                for col in range(cell_number): #Checks the amount of cell numbers (20) for the column
                    if col % 2 == 0: #each number in the list will be divided and will find the remainder and checks if it is equal to 0
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size) #This will create a checkered pattern that is then dislpayed by giving row and col the size of a cell and giving an x,y position
                        pygame.draw.rect(screen, grass_color, grass_rect) #It then draws the them as rectangles
            else: 
                for col in range(cell_number): #Checks the amount of cell numbers (20) for the row
                    if col % 2 != 0: #If numbers are not divisible and is not equal to 0 it will make the if statement true
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size) #
                        pygame.draw.rect(screen, grass_color, grass_rect)
 
    def change_color(self):
        self.snake2.head_up = pygame.image.load('Graphics/head_up_2.png').convert_alpha()
        self.snake2.head_down = pygame.image.load('Graphics/head_down_2.png').convert_alpha()
        self.snake2.head_right = pygame.image.load('Graphics/head_right_2.png').convert_alpha()
        self.snake2.head_left = pygame.image.load('Graphics/head_left_2.png').convert_alpha()
            
        self.snake2.tail_up = pygame.image.load('Graphics/tail_up_2.png').convert_alpha()
        self.snake2.tail_down = pygame.image.load('Graphics/tail_down_2.png').convert_alpha()
        self.snake2.tail_right = pygame.image.load('Graphics/tail_right_2.png').convert_alpha()
        self.snake2.tail_left = pygame.image.load('Graphics/tail_left_2.png').convert_alpha()
 
        self.snake2.body_vertical = pygame.image.load('Graphics/body_vertical_2.png').convert_alpha()
        self.snake2.body_horizontal = pygame.image.load('Graphics/body_horizontal_2.png').convert_alpha()
 
        self.snake2.body_tr = pygame.image.load('Graphics/body_tr_2.png').convert_alpha()
        self.snake2.body_tl = pygame.image.load('Graphics/body_tl_2.png').convert_alpha()
        self.snake2.body_br = pygame.image.load('Graphics/body_br_2.png').convert_alpha()
        self.snake2.body_bl = pygame.image.load('Graphics/body_bl_2.png').convert_alpha()
        
        self.fruit2.apple_2 = pygame.image.load('Graphics/apple_2.png').convert_alpha()
 
         
pygame.init()
cell_size = 40
cell_number = 20
FPS = 60
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
start = pygame.image.load('Graphics/start.png').convert_alpha()
start = pygame.transform.smoothscale(start, (200, 50))
 
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 110) 
main_game = MAIN()
 
def main_menu():
    while True:
 
        screen.fill((0,0,0))
        mx, my = pygame.mouse.get_pos()
 
        button_rect = pygame.Rect(0, 0, 200, 50)
        button_rect.center = (cell_number * cell_size / 2, cell_number * cell_size / 2)
        screen.blit(start, button_rect)
        
        if button_rect.collidepoint((mx, my)):
            if click:
                game()
                
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        clock.tick(FPS)
 
def game():
    running = True
    while running:
 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                #player1
                if event.key == pygame.K_w:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_s:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_a:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)
                if event.key == pygame.K_d:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)
                #Player2
                if event.key == pygame.K_UP:
                    if main_game.snake2.direction.y != 1:
                        main_game.snake2.direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if main_game.snake2.direction.y != -1:
                        main_game.snake2.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake2.direction.x != 1:
                        main_game.snake2.direction = Vector2(-1,0)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake2.direction.x != -1:
                        main_game.snake2.direction = Vector2(1,0)
     
        screen.fill((175,215,70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(FPS)
 
main_menu()
 
 

