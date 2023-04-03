import pygame
from random import randint, shuffle, choice
import menu as fm
import time

### SETTINGS ###
pygame.init()
size_1 = 1020, 700
screen = pygame.display.set_mode(size_1)
end_game_flag = False
FPS = 60
MOVE = 30
SOUND = 31
HEIGHT = 7
WIDTH = 20
MAX_BONUS = 3
BIG_PLAT_TIMER = -1
BIG_PLAT_LIMIT = 5
CLOCK = pygame.time.Clock()
all_sprites_group = pygame.sprite.Group()
h_borders_group = pygame.sprite.Group()
v_borders_group = pygame.sprite.Group()
plate_group = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()
score = 0
counter = WIDTH * HEIGHT
cords_p = [500, 570]  # starting plate coords

### PREPAIRING PACKAGE ###
icon = pygame.image.load("icon.jpg").convert()
pygame.display.set_icon(icon)
image_font = pygame.image.load('font.jpg').convert()
image_cr = pygame.image.load('yellow.jpg').convert()
image_cr = pygame.transform.scale(image_cr, (49, 29))
image_nr = pygame.image.load('orange.jpg').convert()
image_nr = pygame.transform.scale(image_nr, (49, 29))
image_str = pygame.image.load('red.jpg').convert()
image_str = pygame.transform.scale(image_str, (49, 29))
image_bonus = pygame.image.load('bonus+2.jpg').convert()
image_bonus = pygame.transform.scale(image_bonus, (49, 29))
image_bonus_p = pygame.image.load('bonus_big.jpg').convert()
image_bonus_p = pygame.transform.scale(image_bonus_p, (49, 29))
sounds = {'fail': 'lost_sound.wav', 'break': 'bouns_sound.wav',
          'bouns': 'bouns_sound.wav', 'click': 'click.wav'}
composes = ["BackGroundSoundtrack.mp3"]

### CHECING FOR SCORE ###
file = open('score.txt', 'r')
try:
    score_best = int(file.readline().strip())
except:
    score_best = 0
file.close()

### GENERATING FIELD MASK ###
types_of_fields = [-3, -2, -1, 1, 2, 3]
bonuses = 0

def choose(a):
    global bonuses
    if bonuses >= MAX_BONUS:
        return choice(a[:4])
    ret = choice(a)
    if ret > 1:
        bonuses += 1
    return ret

field = [[0] * WIDTH for i in range(HEIGHT)]
options = [[0 for j in range(WIDTH)]
           for i in range(HEIGHT)]
for i in range(HEIGHT):
    bonuses = 0
    for j in range(WIDTH):
        options[i][j] = choose(types_of_fields)
        field[i][j] = pygame.sprite.Sprite()


class Field(pygame.sprite.Sprite):

    bonuses = {2: lambda x: x + 1}

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cell_size = (50, 30)
        self.left = 10
        self.top = 20
        self.height = HEIGHT
        self.width = WIDTH

    def render(self, scr):
        global counter
        cords = [self.left, self.top]
        for i in range(self.height):
            for j in range(self.width):
                if options[i][j] < 0 or options[i][j] > 1:
                    field[i][j].image = pygame.Surface(
                        [self.cell_size[0] - 1, self.cell_size[1] - 1])
                    if options[i][j] == -1:
                        field[i][j].image = image_cr
                    elif options[i][j] == -2:
                        field[i][j].image = image_nr
                    elif options[i][j] == 2:
                        field[i][j].image = image_bonus
                    elif options[i][j] == 3:
                        field[i][j].image = image_bonus_p
                    else:
                        field[i][j].image = image_str
                    field[i][j].rect = field[i][j].image.get_rect()
                    field[i][j].rect.x = cords[0]
                    field[i][j].rect.y = cords[1]
                    bricks_group.add(field[i][j])
                    all_sprites_group.add(field[i][j])
                elif options[i][j] == 0:
                    options[i][j] += 1
                    field[i][j].kill()
                    counter -= 1
                    print(counter)
                cords[0] += self.cell_size[0]
            cords[0] = self.left
            cords[1] += self.cell_size[1]
        cords[1] = self.top

class Plat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites_group)
        self.size = (70, 20)
        cords_p[0] += self.size[0] // 2
        self.flag = False
        self.dir = None
        self.mv = False
        self.u = 10
        self.image = pygame.image.load('plat2.jpg')
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        plate_group.add(self)
        self.is_big = False
    

    def set_size(self, sz):
        self.size = sz
        self.image = pygame.transform.scale(self.image, self.size)
        #self.rect.scale_by(self.image.get_rect())
        self.rect.size = self.image.get_rect().size


    def update(self):
        global BIG_PLAT_TIMER, BIG_PLAT_LIMIT
        print(time.time() - BIG_PLAT_TIMER)
        if BIG_PLAT_TIMER != -1 and time.time() - BIG_PLAT_TIMER < BIG_PLAT_LIMIT and not self.is_big:
            self.set_size((self.size[0] * 3, self.size[1]))
            self.is_big = True
        elif BIG_PLAT_TIMER != -1 and time.time() - BIG_PLAT_TIMER >= BIG_PLAT_LIMIT:
            self.set_size((self.size[0] // 3, self.size[1]))
            BIG_PLAT_TIMER = -1
            self.is_big = False
        if pl.mv:
            if self.dir == 'l':
                if self.rect.x - self.u >= 1:
                    cords_p[0] -= self.u
                    self.rect = self.rect.move(-self.u, 0)
            else:
                if self.rect.x + self.u <= size_1[0] - self.size[0] - 1:
                    cords_p[0] += self.u
                    self.rect = self.rect.move(self.u, 0)
        else:
            pass


class Ball(pygame.sprite.Sprite):

    count = 0

    def __init__(self, x, y, on_plat=True):
        super().__init__(all_sprites_group)
        Ball.count += 1
        self.rad = 10
        self.fly = False
        self.u_b = 5
        self.direct = [(-1)**(Ball.count % 2) * self.u_b, -self.u_b]
        self.image = pygame.Surface(
            (2 * self.rad, 2 * self.rad), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color(
            'white'), (self.rad, self.rad), self.rad)
        self.rect = pygame.Rect(x, y, 1.9 * self.rad, 1.9 * self.rad)
        if on_plat:
            self.rect.x = cords_p[0] - self.rad
            self.rect.y = cords_p[1] - self.rad * 2
        else:
            self.rect.x = x
            self.rect.y = y

    def release(self):
        self.fly = True
    
    def summon_bonus(self, type):
        global BIG_PLAT_TIMER
        if type == 2:
            for i in range(2):
                Ball(self.rect.x, self.rect.y, False).release()
        elif type == 3:
            BIG_PLAT_TIMER = time.time()

    def update(self):
        global score, end_game_flag
        if self.fly:
            if pygame.sprite.spritecollideany(self, h_borders_group):
                if self.rect.y > cords_p[1] - self.rad * 2 + 2:
                    if Ball.count <= 1:
                        file = open('score.txt', 'w')
                        file.write(str(max(score, score_best)))
                        file.close()
                        end_game_flag = True
                        pygame.mixer.music.stop()
                        sound = pygame.mixer.Sound(sounds['fail'])
                        sound.play()
                    Ball.count -= 1
                    self.kill()
                else:
                    sound = pygame.mixer.Sound(sounds['bouns'])
                    sound.play()
                    self.direct[1] = -self.direct[1]
            if pygame.sprite.spritecollideany(self, v_borders_group):
                self.direct[0] = -self.direct[0]
                sound = pygame.mixer.Sound(sounds['bouns'])
                sound.play()
            if pygame.sprite.spritecollideany(self, plate_group):
                self.direct[1] = -self.direct[1]
                sound = pygame.mixer.Sound(sounds['bouns'])
                sound.play()
            if pygame.sprite.spritecollideany(self, bricks_group):
                sound = pygame.mixer.Sound(sounds['break'])
                sound.play()
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if options[i][j] < 0 or options[i][j] > 1:
                            if field[i][j].rect.collidepoint(self.rect.x + self.rad, self.rect.y):
                                self.direct[1] = -self.direct[1]
                                if options[i][j] < 0:
                                    options[i][j] += 1
                                else:
                                    self.summon_bonus(options[i][j])
                                    options[i][j] = 0
                            elif field[i][j].rect.collidepoint(self.rect.x, self.rect.y + self.rad):
                                self.direct[0] = -self.direct[0]
                                if options[i][j] < 0:
                                    options[i][j] += 1
                                else:
                                    self.summon_bonus(options[i][j])
                                    options[i][j] = 0
                            elif field[i][j].rect.collidepoint(self.rect.x + self.rad, self.rect.y + 2 * self.rad):
                                self.direct[1] = -self.direct[1]
                                if options[i][j] < 0:
                                    options[i][j] += 1
                                else:
                                    self.summon_bonus(options[i][j])
                                    options[i][j] = 0
                            elif field[i][j].rect.collidepoint(self.rect.x + 2 * self.rad, self.rect.y + self.rad):
                                self.direct[0] = -self.direct[0]
                                if options[i][j] < 0:
                                    options[i][j] += 1
                                else:
                                    self.summon_bonus(options[i][j])
                                    options[i][j] = 0
                            if not options[i][j]:
                                score += 1
            self.rect = self.rect.move(self.direct[0], self.direct[1])
        else:
            self.rect.x = cords_p[0] - self.rad
            self.rect.y = cords_p[1] - self.rad * 2


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites_group)
        if x1 == x2:
            self.add(v_borders_group)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(h_borders_group)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Text:
    def __init__(self):
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render(
            "Score: {}".format(score), 1, (pygame.Color('red')))
        self.text_x = 10
        self.text_y = size_1[1] - 80

    def drawer(self):
        self.text = self.font.render(
            "Score: {}".format(score), 1, (pygame.Color('red')))
        screen.blit(self.text, (self.text_x, self.text_y))
        self.text = self.font.render("Best score: {}".format(
            max(score_best, score)), 1, (pygame.Color('red')))
        screen.blit(self.text, (size_1[0] - 500, self.text_y))


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0, 0)


### GAME CYCLE ###
f = Field()
b = Ball(500, 570)
pl = Plat(500, 570)
t = Text()
back = Background('font.jpg')
Border(5, 5, size_1[0] - 5, 5)
Border(5, size_1[1] - 5, size_1[0] - 5, size_1[1] - 5)
Border(5, 5, 5, size_1[1] - 5)
Border(size_1[0] - 5, 5, size_1[0] - 5, size_1[1] - 5)
Border(5, 600, size_1[0] - 5, 600)
running = True
screen.fill((255, 255, 255))
f.render(screen)
pygame.mixer.music.load(composes[0])
pygame.mixer.music.play(-1)
fm.main()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pl.dir = 'l'
                pl.mv = True
            elif event.key == pygame.K_RIGHT:
                pl.dir = 'r'
                pl.mv = True
            elif event.key == pygame.K_SPACE:
                b.release()
            elif event.key == pygame.K_ESCAPE:
                fm.main()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pl.mv = False
    if not counter:
        pygame.mixer.music.load('win.wav')
        pygame.mixer.music.play(-1)
        while True:
            screen.fill([255, 255, 255])
            font = pygame.font.Font(None, 50)
            text = font.render("You won!!!", 1, (100, 255, 100))
            text_x = size_1[0] // 2 - text.get_width() // 2
            text_y = size_1[1] // 2 - text.get_height() // 2
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)
            pygame.display.flip()
            for event1 in pygame.event.get():
                if event1.type == pygame.QUIT:
                    exit(0)
                elif event1.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if text_x - 10 <= x <= text_x + text_w + 10 and text_y - 10 <= y <= text_y + text_h + 10:
                        pygame.mixer.music.stop()
                        sound = pygame.mixer.Sound(sounds['click'])
                        sound.play()
                        time.sleep(0.5)
                        exit(0)
    if end_game_flag:
        flag_mus = False
        while True:
            screen.fill([255, 255, 255])
            font = pygame.font.Font(None, 50)
            text = font.render("Quit", 1, (100, 255, 100))
            text_x = size_1[0] // 2 - text.get_width() // 2
            text_y = size_1[1] // 2 - text.get_height() // 2
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)
            font = pygame.font.Font(None, 50)
            text1 = font.render("Your score: {}".format(
                score), 1, (100, 255, 100))
            text_x1 = size_1[0] // 2 - text1.get_width() // 2
            text_y1 = size_1[1] // 2 - text1.get_height() // 2 + 100
            text_w1 = text.get_width()
            text_h1 = text.get_height()
            screen.blit(text1, (text_x1, text_y1))
            pygame.display.flip()
            if not flag_mus:
                flag_mus = True
            for event1 in pygame.event.get():
                if event1.type == pygame.QUIT:
                    exit(0)
                elif event1.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if text_x - 10 <= x <= text_x + text_w + 10 and text_y - 10 <= y <= text_y + text_h + 10:
                        pygame.mixer.music.stop()
                        sound = pygame.mixer.Sound(sounds['click'])
                        sound.play()
                        time.sleep(0.5)
                        exit(0)
    CLOCK.tick(FPS)
    screen.blit(back.image, back.rect)
    f.render(screen)
    t.drawer()
    all_sprites_group.draw(screen)
    all_sprites_group.update()
    h_borders_group.draw(screen)
    h_borders_group.update()
    v_borders_group.draw(screen)
    v_borders_group.update()
    pygame.display.flip()
    screen.fill([255, 255, 255])
