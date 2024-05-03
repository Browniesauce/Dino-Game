import pygame
import os
import random 
import sys

pygame.init()

#Global constants And Program Window Size
Screen_Height = 600
Screen_Width = 1100
Screen = pygame.display.set_mode((Screen_Width,Screen_Height))

#Importing Images Required
Running = [pygame.image.load(os.path.join("Assets/Dino","DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino","DinoRun2.png"))]

Jumping = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

Ducking = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

#Obstacles (Aka Importing Images)
Small_Cactus = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
Large_Cactus = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

Bird = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

#Background (Same)
Clouds = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

Background = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

#Initialization of Position of Dinosaur
class Dino:
    X_Position = 80
    Y_Position = 310
    Y_Position_Duck = 340
    Jump_Velocity = 8.5

    #Dinosaur Initial State
    def __init__(self):
        self.duck_img = Ducking
        self.run_img = Running
        self.jump_img = Jumping

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0 #Is used to cycle through the images so as to animate the object
        self.jump_vel = self.Jump_Velocity
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_Position
        self.dino_rect.y = self.Y_Position

    #Reaction of Dinosuar to User Input
    def update(self , UserInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10: 
            self.step_index = 0

        #Checking The State of the Dinosaur
        if UserInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif UserInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or UserInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        
        #Alternate KeyInput
        if UserInput[pygame.K_SPACE] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif UserInput[pygame.K_RCTRL] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False

    #Reaction to UserInput : Ducking
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_Position
        self.dino_rect.y = self.Y_Position_Duck
        self.step_index += 1 

    #Reaction to UserInput : Running
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_Position
        self.dino_rect.y = self.Y_Position
        self.step_index += 1 

    #Reaction to UserInput : Jumping
    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.Jump_Velocity:
            self.dino_jump = False
            self.jump_vel = self.Jump_Velocity

    #Displays the Image on the Screen
    def draw(self , Screen):
        Screen.blit(self.image , (self.dino_rect.x , self.dino_rect.y))

#Initialization of Cloud
class Cloud:
    def __init__(self):
        self.x = Screen_Width + random.randint(800,1000)
        self.y = random.randint(50 , 100)
        self.image = Clouds
        self.width = self.image.get_width()
    
    #Randomly Generates Clouds
    def update(self):
        self.x -= Game_Speed
        if self.x < -self.width:
            self.x = Screen_Width + random.randint(2500,3000)
            self.y = random.randint(50,100)
    
    #Displays the clouds
    def draw(self,Screen):
        Screen.blit(self.image , (self.x , self.y))

#Obstacles 
class Obstacles:
    def __init__(self, image , type):
        self.image = image
        self.type = type 
        self.rect = self.image[self.type].get_rect()
        self.rect.x = Screen_Width

    def update(self):
        self.rect.x -= Game_Speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()


    def draw(self , Screen):
        Screen.blit(self.image[self.type], self.rect)

#Small Cactus Obstacle
class Small_Cactuses(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325

#Large Cactus Obstacles
class Large_Cactuses(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 300

#Bird Obstacles
class Birds(Obstacles):
    def __init__(self,image):
        self.type = 0
        super().__init__(image , self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, Screen):
        if self.index >=9:
            self.index = 0
        Screen.blit(self.image[self.index//5], self.rect)
        self.index += 1

def main():
    global Game_Speed , X_Position_Background , Y_Position_Background , Points , obstacles
    run = True
    Clock = pygame.time.Clock()
    Player = Dino()
    Cloud_1 = Cloud()
    Game_Speed = 14
    X_Position_Background = 0
    Y_Position_Background = 380
    Points = 0
    font = pygame.font.Font('freesansbold.ttf',20)
    obstacles = []
    Death_Count = 0

    #Keeps a tally on the Scroe
    def Score_Board() :
        global Points , Game_Speed
        Points += 1
        if Points % 100 == 0:
            Game_Speed += 1

        Text = font.render("Ponits: " + str(Points),True, (0,0,0))
        TextRect = Text.get_rect()
        TextRect.center = (1000 , 40)
        Screen.blit(Text , TextRect)

    #Displays the Background
    def background():
        global X_Position_Background , Y_Position_Background
        image_width = Background.get_width()
        Screen.blit(Background , (X_Position_Background , Y_Position_Background))
        Screen.blit(Background , (image_width + X_Position_Background , Y_Position_Background))
        if X_Position_Background <= -image_width:
            Screen.blit(Background , (image_width+ X_Position_Background , Y_Position_Background))
            X_Position_Background = 0
        X_Position_Background -= Game_Speed


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        Screen.fill((255,255,255))
        UserInput = pygame.key.get_pressed()

        Player.draw(Screen)
        Player.update(UserInput)

        if len(obstacles) == 0:
            if random.randint(0,2) == 0:
                obstacles.append(Small_Cactuses(Small_Cactus))
            elif random.randint(0,2) == 1:
                obstacles.append(Large_Cactuses(Large_Cactus))
            elif random.randint(0,2) == 2:
                obstacles.append(Birds(Bird))

        for obstacle in obstacles:
            obstacle.draw(Screen)
            obstacle.update()
            if Player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                Death_Count += 1
                Menu(Death_Count)

        background()

        Cloud_1.draw(Screen)
        Cloud_1.update()

        Score_Board()

        Clock.tick(30)
        pygame.display.update()

#Game Menu
def Menu(Death_Count):
    global Points
    run = True
    while run :
        Screen.fill((255,255,255))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if Death_Count == 0:
            Text = font.render("Press Any Key To Start" , True ,(0,0,0))
        elif Death_Count > 0:
            Text = font.render("Press Any Key to Restart", True , (0,0,0))
            score =font.render("Your Score: "+ str(Points) , True , (0,0,0))
            scorerect = score.get_rect()
            scorerect.center = (Screen_Width // 2 , Screen_Height // 2 + 50)
            Screen.blit(score , scorerect)
        Textrect = Text.get_rect()
        Textrect.center = (Screen_Width // 2 , Screen_Height // 2)
        Screen.blit(Text , Textrect)
        Screen.blit(Running[0] , (Screen_Width // 2 - 20 , Screen_Height // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                main()    

Menu(Death_Count = 0)