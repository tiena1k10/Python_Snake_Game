import pygame, random, time,sys
##
hight_Score = 0
cell_Size = 40
(w,h) = (800, 520)
BLACK = (0, 0, 0)
GLASS = (167, 209, 61)
GLASS2 = (175, 215, 70)
WHITE =(255, 255, 255)
RED  = (255, 0, 0)
GREEN = (0, 200, 0)
TEXT = (150, 150, 141)
fps = 11
pygame.init()
game_Font_Small = pygame.font.Font(r'Font\LePetit.ttf', 20)
game_Font_Big = pygame.font.Font(r'Font\LePetit.ttf', 50)
##
clock = pygame.time.Clock()
class Button:
    def __init__(self, pos_X, pos_Y, str):
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.str = str
        self.color = WHITE
        self.button_Width = 0
        self.button_Height = 0
    def draw(self, SCR):
        rect_Text_Render = game_Font_Big.render(self.str, True, self.color)
        self.button_Width = rect_Text_Render.get_width()
        self.button_Height = rect_Text_Render.get_height()
        SCR.blit(rect_Text_Render,(self.pos_X,self.pos_Y))
    def check_Mouse_In_Button(self):
        mouse_X, mouse_Y = pygame.mouse.get_pos()
        if mouse_X>self.pos_X and mouse_X<self.pos_X + self.button_Width and mouse_Y > self.pos_Y and mouse_Y<self.pos_Y + self.button_Height:
            return True
        else:
            return False
    def set_Color(self):
        if self.check_Mouse_In_Button():
            self.color = RED
        else :
            self.color = WHITE
    def set_Text(self, str):
        self.str = str
class SNAKE:
    def __init__(self):
        self.snakes = [[6,6], [7,6], [8,6]] # giá trị mặc định của rắn
        self.direction = "right" # hướng đi mặc định
        self.checkeat = False
        self.first_Game_Over = 0
        self.head_Up = pygame.image.load("Graphics\head_Up.png")
        self.head_Down = pygame.image.load("Graphics\head_Down.png")
        self.head_Left = pygame.image.load("Graphics\head_Left.png")
        self.head_Right = pygame.image.load("Graphics\head_Right.png")
        self.tail_Up = pygame.image.load(r"Graphics\tail_Up.png")
        self.tail_Down = pygame.image.load(r"Graphics\tail_Down.png")
        self.tail_Left = pygame.image.load(r"Graphics\tail_Left.png")
        self.tail_Right = pygame.image.load(r"Graphics\tail_Right.png")
        self.body_Hori = pygame.image.load(r"Graphics\body_Hori.png")
        self.body_Verti = pygame.image.load(r"Graphics\body_Verti.png")
        self.body_Left_Down = pygame.image.load(r"Graphics\body_Left_Down.png")
        self.body_Left_Up = pygame.image.load(r"Graphics\body_Left_Up.png")
        self.body_Right_Up = pygame.image.load(r"Graphics\body_Right_Up.png")
        self.body_Right_Down = pygame.image.load(r"Graphics\body_Right_Down.png")
        self.eat_Sound = pygame.mixer.Sound(r'Sounds\eat_Sound.wav')
        self.game_Over_Sound = pygame.mixer.Sound(r'Sounds\die_Sound.wav')
    def update_Snake_Positon_Modern(self):
        if self.direction == "right" :
            if self.snakes[-1][0] == 19:
                self.snakes.append([0, self.snakes[-1][1]])
            else:
                self.snakes.append([self.snakes[-1][0]+1, self.snakes[-1][1]])
        if self.direction == "left" :
            if self.snakes[-1][0] == 0:
                self.snakes.append([19, self.snakes[-1][1]])
            else:
                self.snakes.append([self.snakes[-1][0]-1, self.snakes[-1][1]])
        if self.direction == "up" :
            if self.snakes[-1][1] == 0:
                self.snakes.append([self.snakes[-1][0], 12])
            else:
                self.snakes.append([self.snakes[-1][0], self.snakes[-1][1]-1])
        if self.direction == "down" :
            if self.snakes[-1][1] == 12:
                self.snakes.append([self.snakes[-1][0], 0])
            else:
                self.snakes.append([self.snakes[-1][0], self.snakes[-1][1]+1])
    def update_Snake_Positon_Classic(self):
        if self.direction == "right" :
            self.snakes.append([self.snakes[-1][0]+1, self.snakes[-1][1]])
        if self.direction == "left" :
            self.snakes.append([self.snakes[-1][0]-1, self.snakes[-1][1]])
        if self.direction == "up" :
            self.snakes.append([self.snakes[-1][0], self.snakes[-1][1]-1])
        if self.direction == "down" :
            self.snakes.append([self.snakes[-1][0], self.snakes[-1][1]+1])
    def draw_Snake(self, SCR):
        for i in range(len(self.snakes)):
            x_Pos = self.snakes[i][0]
            y_Pos = self.snakes[i][1]
            rect = pygame.Rect(x_Pos*cell_Size, y_Pos*cell_Size, cell_Size, cell_Size)
            if i==len(self.snakes)-1:
                if self.direction == "up":
                    SCR.blit(self.head_Up, rect)
                if self.direction == "down":
                    SCR.blit(self.head_Down, rect)
                if self.direction == "left":
                    SCR.blit(self.head_Left, rect)
                if self.direction == "right":
                    SCR.blit(self.head_Right, rect)
            elif i==0: # sefl.snakes[i] là đuôi, self.snakes[1] là ô ngay trước đuôi
                # ta so sánh x và y của 2 ô này để biết tương quan vị trí giữa ô đuôi và ô ngay trước đuôi
                if self.snakes[i][1]-1 == self.snakes[1][1]:
                    SCR.blit(self.tail_Up, rect)
                if self.snakes[i][1]+1 == self.snakes[1][1]:
                    SCR.blit(self.tail_Down, rect)
                if self.snakes[i][0]+1 == self.snakes[1][0]:
                    SCR.blit(self.tail_Right, rect)
                if self.snakes[i][0]-1 == self.snakes[1][0]:
                    SCR.blit(self.tail_Left, rect)
            else :
                pre_X = self.snakes[i+1][0]
                pre_Y = self.snakes[i+1][1]
                next_X = self.snakes[i-1][0]
                next_Y = self.snakes[i-1][1]
                if pre_X == next_X:
                    SCR.blit(self.body_Verti,rect)
                elif pre_Y==next_Y:
                    SCR.blit(self.body_Hori,rect)
                else:
                    if(self.snakes[i][0]==19):
                        if(next_X==0):
                            next_X=20
                        if(pre_X==0):
                            pre_X=20
                    if(self.snakes[i][0]==0):
                        if(next_X==19):
                            next_X=-1
                        if(pre_X==19):
                            pre_X=-1
                    if(self.snakes[i][1]==0):
                        if(next_Y==12):
                            next_Y=-1
                        if(pre_Y==12):
                            pre_Y=-1
                    if(self.snakes[i][1]==12):
                        if(next_Y==0):
                            next_Y=13
                        if(pre_Y==0):
                            pre_Y=13
                    (a,b) = (pre_X  - self.snakes[i][0],pre_Y  - self.snakes[i][1])
                    #b = pre_Y  - self.snakes[i][1]
                    if a == 0 and b == -1:
                        if self.snakes[i][0] > next_X :
                            SCR.blit(self.body_Left_Up,rect)
                        else:
                            SCR.blit(self.body_Right_Up,rect)
                    if a == 1 and b == 0:
                        if self.snakes[i][1] > next_Y :
                            SCR.blit(self.body_Right_Up,rect)
                        else:
                            SCR.blit(self.body_Right_Down,rect)
                    if a==0 and b == 1 :
                        if self.snakes[i][0] > next_X :
                            SCR.blit(self.body_Left_Down,rect)
                        else:
                            SCR.blit(self.body_Right_Down,rect)
                    if a == -1 and b == 0:
                        if self.snakes[i][1] > next_Y :
                            SCR.blit(self.body_Left_Up,rect)
                        else:
                            SCR.blit(self.body_Left_Down,rect)
    def reset_Snake(self):
        self.direction = "right"
        self.snakes = [[6,6], [7,6], [8,6]]
        self.first_Game_Over = 0
    def play_Eat_Sound(self):
        self.eat_Sound.play()
    def play_Gane_Over_Sound(self):
        self.game_Over_Sound.play()
class FOOD :
    def __init__(self): # khởi tạo
        self.x = random.randint(0,19)
        self.y = random.randint(0,12)
        self.food = pygame.image.load(r"Graphics\apple.png").convert_alpha()
    def draw_Food(self,SCR): # hiển thị food lên màn hình
        rect_ = pygame.Rect(self.x*cell_Size,self.y*cell_Size,cell_Size,cell_Size)
        SCR.blit(self.food, rect_)
    def reset_Food_Positon(self): # reset vị trí food
        self.x = random.randint(0,19)
        self.y = random.randint(0,12)
class MAIN :
    def __init__(self):
        f = open('data\data.txt', 'r')
        global hight_Score # khai báo biến điểm cao là biến toàn cục
        hight_Score = int(f.read())
        f.close()
        self.index_SCR = "menuScreen"  # màn hình mặc định là màn hình menu
        self.Snake = SNAKE()        # khởi tạo 1 đối tượng rắn
        self.Food = FOOD()          # khởi tạo 1 đối tượng thức ăn
        self.pause = False
        self.score = 0
        self.category = "classic"
        self.level = "normal"       # level
        self.bg_SCR1 = pygame.image.load(r"Graphics\bg_SCR1.png").convert_alpha() # background
        # một vài button cần sử dụng
        self.button_Start = Button(250,35,"Start")
        self.button_Try_Again = Button(250,200,"Try Again !!!")
        self.button_Height_Score = Button(150,125,"Hight Score: "+str(hight_Score))
        self.button_Menu = Button(300,300,"Menu")
        self.button_Easy = Button(100,215,"Easy")
        self.button_Normal = Button(230,215,"Normal")
        self.button_Hard = Button(430,215,"Hard")
        self.button_Modern = Button(330,305,"Modern")
        self.button_Classic = Button(150,305,"Classic")
        self.button_Quit = Button(260,385,"Quit")
    def get_event(self):
        if self.index_SCR == "playScreen" :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_UP) and self.Snake.direction != 'down' :
                        self.Snake.direction = "up"
                    if(event.key == pygame.K_DOWN)and self.Snake.direction != 'up':
                        self.Snake.direction = "down"
                    if(event.key == pygame.K_LEFT)and self.Snake.direction != 'right':
                        self.Snake.direction = "left"
                    if(event.key == pygame.K_RIGHT)and self.Snake.direction != 'left':
                        self.Snake.direction = "right"
                    if event.key == pygame.K_SPACE and self.pause==True:
                        self.reset()
                    ###
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_Try_Again.check_Mouse_In_Button() == True and self.pause ==True :
                        self.reset()
                    if self.button_Menu.check_Mouse_In_Button() == True and self.pause ==True :
                        self.index_SCR = "menuScreen"
        elif self.index_SCR == "menuScreen":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_Start.check_Mouse_In_Button():
                        self.index_SCR = "playScreen"
                        self.reset()
                    if self.button_Easy.check_Mouse_In_Button():
                        self.level = "easy"
                    elif self.button_Normal.check_Mouse_In_Button():
                        self.level = "normal"
                    elif self.button_Hard.check_Mouse_In_Button():
                        self.level = "hard"
                    elif self.button_Quit.check_Mouse_In_Button():
                        pygame.quit()
                    elif self.button_Classic.check_Mouse_In_Button():
                        self.category = "classic"
                    elif self.button_Modern.check_Mouse_In_Button():
                        self.category = "modern"   
    def handle_Eat_Food(self):
        if(self.Snake.snakes[-1]==[self.Food.x,self.Food.y]):
            self.score+=1
            self.Snake.play_Eat_Sound()
            self.Snake.checkeat = True
            while  [self.Food.x,self.Food.y] in self.Snake.snakes :
                self.Food.reset_Food_Positon()
        else :
            self.Snake.snakes.pop(0)
            self.Snake.checkeat = False
    def handle_GameOver(self):
        if self.Snake.snakes[-1][0] < 0 or  self.Snake.snakes[-1][0] > 19 or self.Snake.snakes[-1][1] < 0 or self.Snake.snakes[-1][1] > 12 :
            self.pause = True
        for i in range(len(self.Snake.snakes)-1):
            if (self.Snake.snakes[-1]==self.Snake.snakes[i]):
                self.pause = True
        pass
    def set_Level(self):
        global fps
        if self.level == "easy":
            self.button_Easy.color = RED
            self.button_Normal.color = WHITE
            self.button_Hard.color = WHITE
            fps = 8
        elif self.level == "normal":
            self.button_Easy.color = WHITE
            self.button_Normal.color = RED
            self.button_Hard.color = WHITE
            fps = 11
        elif self.level == "hard":
            self.button_Easy.color = WHITE
            self.button_Normal.color = WHITE
            self.button_Hard.color = RED
            fps = 15
    def set_Category(self):
        if self.category =="classic":
            self.button_Classic.color = RED
            self.button_Modern.color = WHITE
        elif self.category =="modern":
            self.button_Classic.color = WHITE
            self.button_Modern.color = RED
    def reset(self):
        self.pause=False
        self.Snake.reset_Snake()
        self.Food.reset_Food_Positon()
        self.score=0
    def draw_Score(self,SCR):
        score_Text = game_Font_Small.render("Score: " + str(self.score), True, RED)
        SCR.blit(score_Text, (5, 5))
    def draw_Grass(self, SCR):
        for i in range(20):
            for j in range(13):
                if i% 2 == 0 :
                    if j % 2 == 0 :
                        rect = pygame.Rect(i * cell_Size, j* cell_Size,cell_Size,cell_Size)
                        pygame.draw.rect(SCR, GLASS, rect)
                    else:
                        rect = pygame.Rect(i * cell_Size,j* cell_Size,cell_Size,cell_Size)
                        pygame.draw.rect(SCR, GLASS2, rect)
                else:
                    if j % 2 == 0 :
                        rect = pygame.Rect(i * cell_Size,j* cell_Size,cell_Size,cell_Size)
                        pygame.draw.rect(SCR, GLASS2, rect)
                    else:
                        rect = pygame.Rect(i * cell_Size,j* cell_Size,cell_Size,cell_Size)
                        pygame.draw.rect(SCR, GLASS, rect)
    def draw_GameOver(self,SCR):
        global hight_Score
        text = game_Font_Big.render("Game Over, Score : "+str(self.score)+" !!",True,RED)
        self.button_Try_Again.set_Color()
        self.button_Menu.set_Color()
        self.button_Try_Again.draw(SCR)
        self.button_Menu.draw(SCR)
        SCR.blit(text,(160,100))
        if self.Snake.first_Game_Over == 0:
            self.Snake.play_Gane_Over_Sound()
            self.Snake.first_Game_Over += 1
        if(self.score>hight_Score):
            hight_Score = self.score
            f = open("data\data.txt",'w')
            f.write(str(hight_Score))
            f.close()
    def update_Enything(self):
        if self.category == "classic":
            self.Snake.update_Snake_Positon_Classic()
        else:
            self.Snake.update_Snake_Positon_Modern()
        self.handle_Eat_Food()
        self.handle_GameOver()
    def draw_Play_Screen(self,SCR):
        if self.pause == False:
            self.draw_Grass(SCR)
            self.draw_Score(SCR)
            self.Food.draw_Food(SCR)
            self.Snake.draw_Snake(SCR)
        else:
            self.draw_GameOver(SCR)
        pygame.display.flip()
    def draw_Menu_Screen(self,SCR):
        rect = pygame.Rect(0,0,w,h) 
        SCR.blit(self.bg_SCR1,rect) # vẽ background
        self.button_Start.set_Color() # đổ mầu cho nút
        self.button_Quit.set_Color()
        self.button_Start.draw(SCR)# vẽ các nút
        self.button_Height_Score.set_Text("Hight Score: " + str(hight_Score)) 
        self.button_Height_Score.draw(SCR)
        self.button_Easy.draw(SCR)
        self.button_Normal.draw(SCR)
        self.button_Hard.draw(SCR)
        self.button_Classic.draw(SCR)
        self.button_Modern.draw(SCR)
        self.button_Quit.draw(SCR)
        pygame.display.flip()
    def run(self,SCR):
        if self.index_SCR == "playScreen" :
            self.get_event()
            self.update_Enything()
            self.draw_Play_Screen(SCR)
        elif self.index_SCR == "menuScreen" :
            self.get_event()
            self.set_Level()
            self.set_Category()
            self.draw_Menu_Screen(SCR)

# main
if __name__ == "__main__":
    SCR = pygame.display.set_mode((w,h))
    pygame.display.set_caption("Snake Game")
    main = MAIN()
    while True:
        main.run(SCR)
        clock.tick(fps)