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

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
