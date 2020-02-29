import pygame

pygame.init()
size_1 = 1020, 700
screen = pygame.display.set_mode(size_1)
screen.fill([0, 0, 0])
FPS = 60
MOVE = 30
all_sprites = pygame.sprite.Group()
h_borders = pygame.sprite.Group()
v_borders = pygame.sprite.Group()
plate = pygame.sprite.Group()
bricks = pygame.sprite.Group()
height = 7
width = 20
field = [[0] * width for i in range(height)]
for i in range(height):
    for j in range(width):
        field[i][j] = pygame.sprite.Sprite()

options = [[-1] * width for i in range(height)]


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
                if options[i][j] == -1:
                    field[i][j].image = pygame.Surface([self.cell_size[0] - 1, self.cell_size[1] - 1])
                    field[i][j].image.fill(pygame.Color('green'))
                    field[i][j].rect = field[i][j].image.get_rect()
                    field[i][j].rect.x = cords[0]
                    field[i][j].rect.y = cords[1]
                    bricks.add(field[i][j])
                    all_sprites.add(field[i][j])
                    options[i][j] = 1
                elif options[i][j] == 0:
                    field[i][j].rect.x = 100000
                    field[i][j].rect.y = 100000
                cords[0] += self.cell_size[0]
            cords[0] = self.left
            cords[1] += self.cell_size[1]
        cords[1] = self.top


left = 600
top = 650
size = (70, 10)


class Plat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.size = (70, 10)
        self.prev = 600
        self.top = 650
        self.flag = False
        self.dir = None
        self.mv = False
        self.u = 10
        self.cords = [left, self.top]
        self.image = pygame.Surface([self.size[0], self.size[1]])
        self.image.fill(pygame.Color('orange'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flag = False
        plate.add(self)

    def update(self):
        if pl.mv:
            if self.dir == 'l':
                if self.rect.x - self.u >= 1:
                    self.rect = self.rect.move(-self.u, 0)
            else:
                if self.rect.x + self.u <= size_1[0] - self.size[0] - 1:
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

    def update(self):
        if pygame.sprite.spritecollideany(self, h_borders):
            self.direct[1] = -self.direct[1]
        if pygame.sprite.spritecollideany(self, v_borders):
            self.direct[0] = -self.direct[0]
        if pygame.sprite.spritecollideany(self, plate):
            self.direct[1] = -self.direct[1]
        if pygame.sprite.spritecollideany(self, bricks):
            for i in range(height):
                for j in range(width):
                    if options[i][j] == 1:
                        if field[i][j].rect.collidepoint(self.rect.x + self.rad, self.rect.y):
                            self.direct[1] = -self.direct[1]
                            print(1)
                            options[i][j] = 0
                        elif field[i][j].rect.collidepoint(self.rect.x, self.rect.y + self.rad):
                            self.direct[0] = -self.direct[0]
                            print(1)
                            options[i][j] = 0
                        elif field[i][j].rect.collidepoint(self.rect.x + self.rad, self.rect.y + 2 * self.rad):
                            self.direct[1] = -self.direct[1]
                            print(1)
                            options[i][j] = 0
                        elif field[i][j].rect.collidepoint(self.rect.x + 2 * self.rad, self.rect.y + self.rad):
                            self.direct[0] = -self.direct[0]
                            print(1)
                            options[i][j] = 0
        self.rect = self.rect.move(self.direct[0], self.direct[1])


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


f = Field()
b = Ball(600, 600)
pl = Plat(500, 500)
Border(5, 5, size_1[0] - 5, 5)
Border(5, size_1[1] - 5, size_1[0] - 5, size_1[1] - 5)
Border(5, 5, 5, size_1[1] - 5)
Border(size_1[0] - 5, 5, size_1[0] - 5, size_1[1] - 5)
running = True
screen.fill((255, 255, 255))
f.render(screen)
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pl.dir = 'l'
                pl.mv = True
            elif event.key == pygame.K_RIGHT:
                pl.dir = 'r'
                pl.mv = True
            elif event.key == pygame.K_SPACE:
                pass
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pl.mv = False
    clock.tick(FPS)
    f.render(screen)
    all_sprites.draw(screen)
    all_sprites.update()
    h_borders.draw(screen)
    h_borders.update()
    v_borders.draw(screen)
    v_borders.update()
    pygame.display.flip()
    screen.fill([255, 255, 255])
