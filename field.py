import pygame

pygame.init()
size = (1020, 700)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
FPS = 60


font = pygame.font.Font(None, 50)
text = font.render("Play", 1, (100, 255, 100))
text_x = size[0] // 2 - text.get_width() // 2
text_y = size[1] // 2 - text.get_height() // 2
text_w = text.get_width()
text_h = text.get_height()
screen.blit(text, (text_x, text_y))
pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                       text_w + 20, text_h + 20), 1)


def check_pos(p):
    x = p[0]
    y = p[1]
    if text_x - 10 <= x <= text_x + text_w + 10 and text_y - 10 <= y <= text_y + text_h + 10:
        import cycle


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            check_pos(pos)
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
    pygame.display.flip()
