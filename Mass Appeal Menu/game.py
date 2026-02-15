import pygame
import random
import os
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def safe_load_image(path):
    if os.path.exists(path):
        return pygame.image.load(path).convert_alpha()
    return None

def load_font(path, size):
    if os.path.exists(path):
        return pygame.font.Font(path, size)
    return pygame.font.SysFont("Arial", size)

class Body:
    def __init__(self, x, y, radius, image=None, name=""):
        self.x = x
        self.y = y
        self.radius = radius
        self.image = image
        self.name = name

    def draw(self, screen):
        if self.image:
            size = int(self.radius * 2)
            img = pygame.transform.smoothscale(self.image, (size, size))
            rect = img.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(img, rect)
        else:
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), int(self.radius), 2)

def circles_collide(a: Body, b: Body):
    dx = a.x - b.x
    dy = a.y - b.y
    return (dx*dx + dy*dy) <= (a.radius + b.radius) ** 2

def run_game(screen):
    clock = pygame.time.Clock()
    w, h = screen.get_size()

    bg = safe_load_image("assets/images/background.png")
    if bg:
        bg = pygame.transform.scale(bg, (w, h))

    # Earth stages (может быть 2-4 картинки — код подстроится)
    earth_paths = [
        "assets/images/earth/earth_1.png",
        "assets/images/earth/earth_2.png",
        "assets/images/earth/earth_3.png",
        "assets/images/earth/earth_4.png",
    ]
    earth_imgs = [safe_load_image(p) for p in earth_paths if safe_load_image(p)]
    if not earth_imgs:
        earth_imgs = [None]

    # planets (5 штук)
    planet_imgs = []
    for i in range(1, 6):
        planet_imgs.append(safe_load_image(f"assets/images/planets/planet_{i}.png"))

    sun_img = safe_load_image("assets/images/sun.png")

    font = load_font("assets/fonts/VT323.ttf", 48)
    font_small = load_font("assets/fonts/VT323.ttf", 28)

    # player
    player = Body(w * 0.5, h * 0.6, radius=28, image=earth_imgs[0], name="earth")

    # 5 planets with increasing sizes
    planets = []
    base_sizes = [18, 24, 32, 44, 60]  # можно менять
    for i, r in enumerate(base_sizes):
        x = random.randint(80, w - 80)
        y = random.randint(80, h - 80)
        planets.append(Body(x, y, r, image=planet_imgs[i], name=f"p{i+1}"))

    # sun (big)
    sun = Body(w * 0.5, h * 0.25, radius=90, image=sun_img, name="sun")

    speed = 5.2

    def update_player_stage():
        # чем больше radius, тем более “большую” Землю показываем
        if len(earth_imgs) == 1:
            player.image = earth_imgs[0]
            return
        # пороги подстраиваются
        thresholds = [35, 50, 70]  # для 2-4 стадий
        idx = 0
        for t in thresholds:
            if player.radius >= t:
                idx += 1
        idx = min(idx, len(earth_imgs) - 1)
        player.image = earth_imgs[idx]

    def show_end(text_main, text_sub):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "menu"   # Enter → back to menu

            if bg:
                screen.blit(bg, (0, 0))
            else:
                screen.fill(BLACK)

            t1 = font.render(text_main, True, WHITE)
            t2 = font_small.render(text_sub, True, WHITE)
            screen.blit(t1, t1.get_rect(center=(w//2, h//2 - 20)))
            screen.blit(t2, t2.get_rect(center=(w//2, h//2 + 40)))

            pygame.display.flip()
            clock.tick(60)

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP])

        # нормализация, чтобы по диагонали не было быстрее
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length

        player.x = max(player.radius, min(w - player.radius, player.x + dx * speed))
        player.y = max(player.radius, min(h - player.radius, player.y + dy * speed))

        # collisions with planets
        for p in planets[:]:
            if circles_collide(player, p):
                if player.radius >= p.radius:
                    # eat → grow
                    player.radius += max(2, int(p.radius * 0.25))
                    planets.remove(p)
                    update_player_stage()
                else:
                    return show_end("You Lose", "Press ENTER to return to menu")

        # collision with sun
        if circles_collide(player, sun):
            if player.radius >= sun.radius:
                return show_end("You Win!", "Press ENTER to return to menu")
            else:
                return show_end("Too Small for the Sun!", "Press ENTER to return to menu")

        # draw
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(BLACK)

        sun.draw(screen)
        for p in planets:
            p.draw(screen)
        player.draw(screen)

        # hint
        hint = font_small.render("ESC → Menu | Eat smaller planets to grow", True, WHITE)
        screen.blit(hint, (20, 20))

        pygame.display.flip()
        clock.tick(60)
