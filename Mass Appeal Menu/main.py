import pygame, sys
from src.menu import run_menu
from src.game import run_game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Mass Appeal")

    while True:
        choice = run_menu(screen)     # вернёт "play" или "quit"
        if choice == "play":
            run_game(screen)          # запускаем игру в том же окне
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
