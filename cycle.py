import pygame
from random import randint
import field as fm

pygame.init()
size_1 = 1020, 700
screen = pygame.display.set_mode(size_1)
screen.fill([255, 255, 255])
flag = False
FPS = 60
MOVE = 30
all_sprites = pygame.sprite.Group()
h_borders = pygame.sprite.Group()
v_borders = pygame.sprite.Group()
plate = pygame.sprite.Group()
bricks = pygame.sprite.Group()
height = 7
width = 20
score = 0
file = open('score.txt', 'r')
try:
    score_best = int(file.readline().strip())
except:
    score_best = 0
file.close()
field = [[0] * width for i in range(height)]
for i in range(height):
    for j in range(width):
        field[i][j] = pygame.sprite.Sprite()

options = [[randint(-3, -1)] * width for i in range(height)]


class Field(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cell_size = (50, 30)
        self.left = 10
        self.top = 20
        self.height = 7
        self.width = 20

    def render(self, scr):
        cords = [self.left, self.top]
        for i in range(self.height):
            for j in range(self.width):
                if options[i][j] < 0:
                    field[i][j].image = pygame.Surface([self.cell_size[0] - 1, self.cell_size[1] - 1])
                    if options[i][j] == -1:
                        field[i][j].image.fill(pygame.Color('green'))
                    elif options[i][j] == -2:
                        field[i][j].image.fill(pygame.Color('yellow'))
                    else:
                        field[i][j].image.fill(pygame.Color('red'))
                    field[i][j].rect = field[i][j].image.get_rect()
                    field[i][j].rect.x = cords[0]
                    field[i][j].rect.y = cords[1]
                    bricks.add(field[i][j])
                    all_sprites.add(field[i][j])
                elif options[i][j] == 0:
                    field[i][j].rect.x = 1000000
                    field[i][j].rect.y = 1000000
                cords[0] += self.cell_size[0]
            cords[0] = self.left
            cords[1] += self.cell_size[1]
        cords[1] = self.top


left = 600
top = 650
size = (70, 10)
cords_p = [500, 570]


class Plat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.size = (70, 20)
        cords_p[0] += self.size[0] // 2
        self.flag = False
        self.dir = None
        self.mv = False
        self.u = 10
        self.image = pygame.image.load('plat.jpg')
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flag = False
        plate.add(self)

    def update(self):
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
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.left_b = 600
        self.top_b = 600
        self.rad = 10
        self.fly = False
        self.prev_b = [left, top]
        self.cords_b = [self.left_b, self.top_b, self.rad]
        self.u_b = 5
        self.direct = [-self.u_b, -self.u_b]
        self.image = pygame.Surface((2 * self.rad, 2 * self.rad), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color('blue'), (self.rad, self.rad), self.rad)
        self.rect = pygame.Rect(x, y, 2 * self.rad, 2 * self.rad)
        self.rect.x = cords_p[0] - self.rad
        self.rect.y = cords_p[1] - self.rad * 2

    def release(self):
        self.fly = True

    def update(self):
        global score, flag
        if self.fly:
            if pygame.sprite.spritecollideany(self, h_borders):
                if self.rect.y > cords_p[1] - self.rad * 2 + 2:
                    file = open('score.txt', 'w')
                    file.write(str(max(score, score_best)))
                    file.close()
                    flag = True

                self.direct[1] = -self.direct[1]
            if pygame.sprite.spritecollideany(self, v_borders):
                self.direct[0] = -self.direct[0]
            if pygame.sprite.spritecollideany(self, plate):
                self.direct[1] = -self.direct[1]
            if pygame.sprite.spritecollideany(self, bricks):
                for i in range(height):
                    for j in range(width):
                        if options[i][j] != 0:
                            if field[i][j].rect.collidepoint(self.rect.x + self.rad, self.rect.y):
                                self.direct[1] = -self.direct[1]
                                options[i][j] += 1
                            elif field[i][j].rect.collidepoint(self.rect.x, self.rect.y + self.rad):
                                self.direct[0] = -self.direct[0]
                                options[i][j] += 1
                            elif field[i][j].rect.collidepoint(self.rect.x + self.rad, self.rect.y + 2 * self.rad):
                                self.direct[1] = -self.direct[1]
                                options[i][j] += 1
                            elif field[i][j].rect.collidepoint(self.rect.x + 2 * self.rad, self.rect.y + self.rad):
                                self.direct[0] = -self.direct[0]
                                options[i][j] += 1
                            if not options[i][j]:
                                score += 1
            self.rect = self.rect.move(self.direct[0], self.direct[1])
        else:
            self.rect.x = cords_p[0] - self.rad
            self.rect.y = cords_p[1] - self.rad * 2


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(v_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(h_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Text:
    def __init__(self):
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render("Score: {}".format(score), 1, (pygame.Color('red')))
        self.text_x = 10
        self.text_y = size_1[1] - 80

    def drawer(self):
        self.text = self.font.render("Score: {}".format(score), 1, (pygame.Color('red')))
        screen.blit(self.text, (self.text_x, self.text_y))
        self.text = self.font.render("Best score: {}".format(max(score_best, score)), 1, (pygame.Color('red')))
        screen.blit(self.text, (size_1[0] - 500, self.text_y))


f = Field()
pl = Plat(500, 570)
b = Ball(500, 570)
t = Text()
Border(5, 5, size_1[0] - 5, 5)
Border(5, size_1[1] - 5, size_1[0] - 5, size_1[1] - 5)
Border(5, 5, 5, size_1[1] - 5)
Border(size_1[0] - 5, 5, size_1[0] - 5, size_1[1] - 5)
Border(5, 600, size_1[0] - 5, 600)
running = True
screen.fill((255, 255, 255))
f.render(screen)
clock = pygame.time.Clock()
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
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pl.mv = False
    if flag:
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
            pygame.display.flip()
            for event1 in pygame.event.get():
                if event1.type == pygame.QUIT:
                    exit(0)
                elif event1.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if text_x - 10 <= x <= text_x + text_w + 10 and text_y - 10 <= y <= text_y + text_h + 10:
                        exit(0)
    clock.tick(FPS)
    f.render(screen)
    t.drawer()
    all_sprites.draw(screen)
    all_sprites.update()
    h_borders.draw(screen)
    h_borders.update()
    v_borders.draw(screen)
    v_borders.update()
    pygame.display.flip()
    screen.fill([255, 255, 255])
