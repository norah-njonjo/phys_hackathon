import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mass Appeal")


background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


logo = pygame.image.load("assets/game_logo.png")
logo_rect = logo.get_rect(center=(WIDTH//2, HEIGHT//2 - 150))


font = pygame.font.Font("assets/VT323.ttf", 60)


button_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 50, 300, 80)

def draw_button():
    pygame.draw.rect(screen, (235, 164, 217), button_rect)
    text = font.render("PLAY", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

def menu():
    while True:
        screen.blit(background, (0, 0))
        screen.blit(logo, logo_rect)
        draw_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  

        pygame.display.update()

menu()
