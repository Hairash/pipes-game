import pygame

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 30)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (218, 218, 218)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.display.set_caption("Text test")

window_size = 100
window = pygame.display.set_mode((window_size, window_size))

info_list = [
    'One', 'Two'
]
idx = 0

# info_text = 'One'
# text_img = FONT.render(info_text, False, BLUE)
# # window.fill(WHITE)
# window.blit(text_img, (0, 0))
# pygame.display.update()
#
info_text = 'Two'
# window.fill(BLACK)
text_img = FONT.render(info_text, False, BLUE)
# window.blit(text_img, (0, 0))
# pygame.display.update()
# global text_img


def change_info():
    global idx, text_img
    idx = (idx + 1) % len(info_list)
    info_text = info_list[idx]
    # window.fill(BLACK)
    rect = text_img.get_rect()
    pygame.draw.rect(window, BLACK, rect)
    text_img = FONT.render(info_text, False, BLUE)
    window.blit(text_img, (0, 0))
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                change_info()
