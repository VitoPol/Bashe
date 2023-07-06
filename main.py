import pygame
from random import choice

running = True
is_end = False
clock = pygame.time.Clock()
pygame.init()
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Bashe")
font = pygame.font.Font(None, 72)
final_font = pygame.font.Font("fonts/YsabeauInfant-Italic.ttf", 150)

screen = pygame.display.set_mode((1200, 709))
bg = pygame.image.load("images/table.jpg")

player = choice((-1, 1))

count_of_items = 15
item = pygame.image.load("images/item.png")
item = pygame.transform.scale(item, (38, 251))
item_y = 230
speed = 0.1
put_away = 0

sound = pygame.mixer.Sound("sounds/wzshih.mp3")

def get_move(count_of_items: int, move: int) -> int:
    put_away = min(count_of_items, move)
    if put_away:
        sound.play()
    return put_away

while running:
    screen.blit(bg, (0, 0))

    # Отрисовка кнопок
    color_1 = "white"
    color_2 = "white"
    if not is_end:
        if player == 1:
            color_1 = "darkgray"
        elif player == -1:
            color_2 = "darkgray"
    for i in range(3):
        but = pygame.draw.rect(screen, color_1, (100 + (i * 400), 50, 200, 100), 4, border_radius=20)
        text = font.render("I"*(i+1), True, color_1)
        screen.blit(text, text.get_rect(center=(but.center)))

        but = pygame.draw.rect(screen, color_2, (100 + (i * 400), 559, 200, 100), 4, border_radius=20)
        text = font.render("I" * (i + 1), True, color_2)
        screen.blit(text, text.get_rect(center=(but.center)))

    # Отрисовка палочек
    for i in range(count_of_items):
        if count_of_items - i <= put_away:
            if count_of_items - i == put_away:
                item_y += speed * player
                speed *= 1.15
            screen.blit(item, (50 + (76 * i), item_y + speed))
            if (item_y > 710 or item_y < -251) and i == count_of_items - 1:
                count_of_items -= put_away
                put_away = 0
                speed = 0.1
                item_y = 230
                player *= -1
        else:
            screen.blit(item, (50 + (76 * i), 230))

    # Отрисовка результата
    if count_of_items <= 0:
        if player == 1:
            final_text = "↑ WINNER ↑"
        else:
            final_text = "↓ WINNER ↓"
        final_text = final_font.render(final_text, True, "white")
        screen.blit(final_text, final_text.get_rect(center=(screen.get_rect().center)))
        is_end = True

    pygame.display.update()

    # Отслеживание ивентов
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            if not put_away:
                match event.key:
                    case pygame.K_1:
                        put_away = get_move(count_of_items, 1)
                    case pygame.K_2:
                        put_away = get_move(count_of_items, 2)
                    case pygame.K_3:
                        put_away = get_move(count_of_items, 3)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if player == 1:
                but_y = 559
            elif player == -1:
                but_y = 50
            if not put_away:
                if mouse_pos[0] in range(100, 300):
                    if mouse_pos[1] in range(but_y, but_y + 100):
                        put_away = get_move(count_of_items, 1)
                if mouse_pos[0] in range(500, 700):
                    if mouse_pos[1] in range(but_y, but_y + 100):
                        put_away = get_move(count_of_items, 2)
                if mouse_pos[0] in range(900, 1100):
                    if mouse_pos[1] in range(but_y, but_y + 100):
                        put_away = get_move(count_of_items, 3)

    clock.tick(60)
