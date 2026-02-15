import pygame

pygame.init()

font = pygame.font.SysFont("Arial", 30, bold = True)

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))

def hub(): #ONLY USE THIS

        planet_value = "0"
        mass_value = "10"

        #Load Image
        menu_og = pygame.image.load('hub3.png').convert() #HUB
        move_og = pygame.image.load('move2.png').convert() #MOVE


        scale = 0.5

        m_w = int(menu_og.get_width() * scale)
        m_h = int(menu_og.get_height() * scale)

        v_w = int(move_og.get_width() * scale)
        v_h = int(move_og.get_height() * scale)

        menu_og.set_colorkey((255, 255, 255))
        move_og.set_colorkey((255, 255, 255))

        menu = pygame.transform.smoothscale(menu_og, (m_w, m_h))
        move = pygame.transform.smoothscale(move_og, (v_w, v_h))

        menu_rect = menu.get_rect()
        move_rect = move.get_rect()

        #Position
        menu_rect.bottomleft = (0, screen_height)
        move_rect.bottomright = (screen_width, screen_height)

        playing = True

        while playing:

                screen.fill((0, 0, 0))


                screen.blit(menu, menu_rect)
                screen.blit(move, move_rect)

                planet_surf = font.render(planet_value, True, (255, 255, 255))
                mass_surf = font.render(mass_value, True, (255, 255, 255))

                screen.blit(planet_surf, (menu_rect.x + 117, menu_rect.y + 7))
                screen.blit(mass_surf, (menu_rect.x + 100, menu_rect.y + 50))

                pygame.display.flip()


                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                playing = False
        pygame.quit()

hub()
