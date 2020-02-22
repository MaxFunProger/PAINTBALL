import pygame

pygame.init()
size = 1020, 700
screen = pygame.display.set_mode(size)
FPS = 60


class Field(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cell_size = (50, 30)
        self.left = 10
        self.top = 20
        self.height = 10
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


class Plat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = (50, 5)
        self.left = 600
        self.prev = 600
        self.top = 600
        self.flag = False
        self.dir = None

    def render(self, scr):
        cords = [self.left, self.top]
        pygame.draw.rect(scr, pygame.Color('black'), (self.prev, cords[1], self.size[0], self.size[1]), 0)
        pygame.draw.rect(scr, pygame.Color('purple'), (cords[0], cords[1], self.size[0], self.size[1]), 0)

    def pl_move(self, k):
        if k == 'l':
            if self.left - 2 >= 0:
                self.prev = self.left
                self.left -= 2
            else:
                self.prev = self.left
        elif k == 'r':
            if self.left + 2 <= 1020:
                self.prev = self.left
                self.left += 2
            else:
                self.prev = self.left


f = Field()
pl = Plat()
running = True
screen.fill((0, 0, 0))
f.render(screen)
pl.render(screen)
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            f.get_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pl.pl_move('l')
            elif event.key == pygame.K_RIGHT:
                pl.pl_move('r')
    clock.tick(FPS)
    pygame.event.pump()

    f.render(screen)
    pl.render(screen)
    pygame.display.flip()

