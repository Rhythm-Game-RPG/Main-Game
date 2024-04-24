import pygame
import sys
from level import Level
from settings import *


class StartMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.menu_items = ['Start', 'Exit']
        self.current_item = 0
        self.active = True

    def draw(self, screen):
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 255) if i == self.current_item else (128, 128, 128)
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            screen.blit(text, text_rect)


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.current_item = (self.current_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_UP:
                self.current_item = (self.current_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                if self.current_item == 0:  # Start
                    self.active = False
                elif self.current_item == 1:  # Exit
                    pygame.quit()
                    sys.exit()


class Game:
    def __init__(self):
        pygame.init()
        # Template Music
        pygame.mixer.init()
        music = pygame.mixer.music.load('funk.ogg')
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Boogie Bash')
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.menu = StartMenu()

    def display_ui(self):
        for i in range(self.level.player.max_hp):
            img = pygame.image.load("Heart-Empty.png" if i >= self.level.player.max_hp else "Heart.png")
            img = pygame.transform.scale(img, (50, 50))
            self.screen.blit(img, (i * 50 + HEIGHT / 4 - self.level.player.max_hp * 50, 20))

    # Monster HP Display
    #def display_mon_ui(self):
    #    for i in range(self.level.monster.max_hp):
    #        img = pygame.image.load("Heart-Empty.png" if i >= self.level.monster.max_hp else "Heart.png")
    #        img = pygame.transform.scale(img, (20, 20))
    #        self.screen.blit(img, (i * 50 + self.level.monster.pos[0] + self.level.monster.pos[1], 100))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.menu.active:
                    self.menu.handle_event(event)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.level.toggle_menu()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            self.screen.fill('white')

            if self.menu.active:
                self.screen.blit(bg_image, (0, 0))
                self.menu.draw(self.screen)
            else:
                self.level.run()
                self.display_ui()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
