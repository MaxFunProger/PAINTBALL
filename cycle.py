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


class Field(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cell_size = (50, 30)
        self.left = 10
        self.top = 20
        self.height = 7
        self.width = 20
        self.field = [[-1] * self.width for i in range(self.height)]

    def render(self, scr):
        cords = [self.left, self.top]
        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j] == 1:
                    pygame.draw.rect(scr, pygame.Color('white'), (cords[0], cords[1],
                                                                     self.cell_size[0], self.cell_size[1]), 0)
                elif self.field[i][j] == -1:
                    pygame.draw.rect(scr, pygame.Color('white'), (cords[0], cords[1],
                                                                     self.cell_size[0], self.cell_size[1]), 1)
                else:
                    pygame.draw.rect(scr, pygame.Color('black'), (cords[0] + 1, cords[1] + 1,
                                                                  self.cell_size[0] - 2, self.cell_size[1] - 2), 0)
                cords[0] += self.cell_size[0]
            cords[0] = self.left
            cords[1] += self.cell_size[1]
        cords[1] = self.top

    def on_click(self, x, y):
        if x is not None:
            if self.field[y][x] == -1:
                self.field[y][x] = 1
            else:
                self.field[y][x] = not self.field[y][x]

    def get_cell(self, x, y):
        cords = [self.left, self.top]
        for i in range(self.height):
            for j in range(self.width):
                if cords[0] + self.cell_size[0] >= x >= cords[0] and cords[1] + self.cell_size[1] >= y >= cords[1]:
                    return j, i
                cords[0] += self.cell_size[0]
            cords[0] = self.left
            cords[1] += self.cell_size[1]
        cords[1] += self.top
        return None, None

    def get_click(self, p):
        x, y = p[0], p[1]
        x, y = self.get_cell(x, y)
        self.on_click(x, y)


left = 600
top = 650
size = (70, 10)


class Plat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = (70, 10)
        self.prev = 600
        self.top = 650
        self.flag = False
        self.dir = None
        self.mv = False
        self.u = 10
        self.cords = [left, self.top]

    def render(self, scr):
        self.cords = [left, self.top]
        pygame.draw.rect(scr, pygame.Color('black'), (self.prev, self.cords[1], self.size[0], self.size[1]), 0)
        pygame.draw.rect(scr, pygame.Color('purple'), (self.cords[0], self.cords[1], self.size[0], self.size[1]), 0)

    def pl_move(self, k):
        global left
        if k == 'l':
            if left - self.u >= 0:
                self.prev = left
                left -= self.u
            else:
                self.prev = left
                self.mv = False
        elif k == 'r':
            if left + self.u + self.size[0] <= 1020:
                self.prev = left
                left += self.u
            else:
                self.prev = left
                self.mv = False


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.left_b = 600
        self.top_b = 600
        self.rad = 10
        self.fly = False
        self.prev_b = [left, top]
        self.cords_b = [self.left_b, self.top_b, self.rad]
        self.u_b = 2
        self.direct = [-self.u_b, -self.u_b]
        self.image = pygame.Surface((2 * self.rad, 2 * self.rad), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color('blue'), (self.rad, self.rad), self.rad)
        self.rect = pygame.Rect(x, y, 2 * self.rad, 2 * self.rad)

    def update(self):
        self.rect = self.rect.move(self.direct[0], self.direct[1])
        if pygame.sprite.spritecollideany(self, h_borders):
            self.direct[1] = -self.direct[1]
        if pygame.sprite.spritecollideany(self, v_borders):
            self.direct[0] = -self.direct[0]

    def render_ball(self, scr):
        if not self.fly:
            pygame.draw.circle(scr, pygame.Color('black'), (self.prev_b[0],
                                                          self.prev_b[1]), self.cords_b[2], 0)
            pygame.draw.circle(scr, pygame.Color('red'), (left + size[0] // 2,
                                                          top - size[1]), self.cords_b[2], 0)
            self.prev_b = [left + size[0] // 2, top - size[1]]
        else:
            pygame.draw.circle(scr, pygame.Color('black'), (self.prev_b[0], self.prev_b[1]), self.cords_b[2], 0)
            pygame.draw.circle(scr, pygame.Color('red'), (self.cords_b[0], self.cords_b[1]), self.cords_b[2], 0)
            self.prev_b = self.cords_b.copy()

    def release(self):
        if self.fly:
            pass
        else:
            self.left_b = left + size[0] // 2
            self.top_b = top - size[1] // 2
            self.fly = True
            self.cords_b = [self.left_b, self.top_b, self.rad]
            pygame.time.set_timer(MOVE, 20)

    def mover(self):
        if self.cords_b[0] - self.rad <= 2:
            self.direct[0] = self.u_b
        elif self.cords_b[0] + self.rad >= 1018:
            self.direct[0] = -self.u_b
        if self.cords_b[1] - self.rad <= 2:
            self.direct[1] = self.u_b
        elif self.cords_b[1] + self.rad >= 698:
            self.direct[1] = -self.u_b
        self.cords_b[0] += self.direct[0]
        self.cords_b[1] += self.direct[1]


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
pl = Plat()
Border(5, 5, size_1[0] - 5, 5)
Border(5, size_1[1] - 5, size_1[0] - 5, size_1[1] - 5)
Border(5, 5, 5, size_1[1] - 5)
Border(size_1[0] - 5, 5, size_1[0] - 5, size_1[1] - 5)
running = True
screen.fill((0, 0, 0))
f.render(screen)
pl.render(screen)
b.render_ball(screen)
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            f.get_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pl.dir = 'l'
                pl.mv = True
            elif event.key == pygame.K_RIGHT:
                pl.dir = 'r'
                pl.mv = True
            elif event.key == pygame.K_SPACE:
                b.release()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pl.mv = False
        elif event.type == MOVE:
            b.mover()
    if pl.mv:
        pl.pl_move(pl.dir)
    clock.tick(FPS)
    f.render(screen)
    pl.render(screen)
    all_sprites.draw(screen)
    all_sprites.update()
    h_borders.draw(screen)
    h_borders.update()
    v_borders.draw(screen)
    v_borders.update()
    b.render_ball(screen)
    pygame.display.flip()
    screen.fill([255, 255, 255])
