import pygame
import sys

import level
from level import Level
from player import *
from settings import *


class StartMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.w_font = pygame.font.Font(None, 56)
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


class DeathScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.menu_items = ['Back to Menu', 'Exit Game']
        self.current_item = 0
        self.active = False

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Fill the screen with black
        # Display the background image
        background = pygame.image.load('death.png')
        screen.blit(background, (0, 0))

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
                if self.current_item == 0:  # Back to Menu
                    self.active = False
                elif self.current_item == 1:  # Exit Game
                    pygame.quit()
                    sys.exit()

class WinScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.w_font = pygame.font.Font(None, 56)
        self.menu_items = ['Back to Menu', 'Exit Game']
        self.current_item = 0
        self.active = False

    def draw(self, screen, mon_killed, save_hp):
        screen.fill((0, 0, 0))  # Fill the screen with black
        # Display the background image
        pg = pygame.image.load('win_screen.png')
        background = pygame.transform.scale(pg, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))
        killed_text = self.w_font.render(f'{mon_killed}', True, (0, 0, 0))
        screen.blit(killed_text, (WIDTH / 5 + 10, 530))

        for i in range(3):
            img = pygame.image.load("Heart-Empty.png" if i >= save_hp else "Heart.png")
            img = pygame.transform.scale(img, (50, 50))
            screen.blit(img, (i * 50 + WIDTH - 3 * 100, 525))

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
                if self.current_item == 0:  # Back to Menu
                    self.active = False
                elif self.current_item == 1:  # Exit Game
                    pygame.quit()
                    sys.exit()


class BeatBar(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x.pos_y]


class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        # Template Music
        self.sprites = []
        self.sprites.append(pygame.image.load('m_idle.png'))
        self.sprites.append(pygame.image.load('m_1.png'))
        self.sprites.append(pygame.image.load('m_2.png'))
        self.sprites.append(pygame.image.load('m_3.png'))
        self.sprites.append(pygame.image.load('m_4.png'))
        self.sprites.append(pygame.image.load('m_hit.png'))
        self.sprites.append(pygame.image.load('m_5.png'))
        self.sprites.append(pygame.image.load('m_6.png'))
        self.sprites.append(pygame.image.load('m_7.png'))
        self.sprites.append(pygame.image.load('m_8.png'))
        self.sprites.append(pygame.image.load('m_hit_1.png'))
        self.sprites.append(pygame.image.load('m_hit_2.png'))
        self.scroll = 0

        self.hp_left = 0
        self.mon_killed = 0
        pygame.mixer.init()
        music = pygame.mixer.music.load('menu.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.50)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Boogie Bash')
        self.clock = pygame.time.Clock()
        self.val = 0
        self.level = Level()
        self.death_screen = DeathScreen()
        self.save_hp = 0
        self.menu = StartMenu()
        self.win_screen = WinScreen()
        self.mon_left = len(self.level.player.monster_list)
        self.k_count = self.level.player.kill_count
        self.win_was_active = False

    def display_ui(self):
        pic = pygame.image.load("health-cover.png")
        self.screen.blit(pic, (0, 10))
        for i in range(self.level.player.max_hp):
            img = pygame.image.load("Heart-Empty.png" if i >= self.level.player.curr_hp else "Heart.png")
            img = pygame.transform.scale(img, (50, 50))
            self.screen.blit(img, (i * 50 + HEIGHT / 4 - 3 * 50, 20))
        enemy_text = font.render(f'Monsters Left: {self.mon_left}', True, (0, 0, 0))
        self.screen.blit(enemy_text, (enemy_text.get_width() / 7, 85))

    def BoogieBar(self):
        if 5 <= self.level.player.move_counter < 10:
            self.screen.blit(self.sprites[1], (200, 500))
        elif 10 <= self.level.player.move_counter < 15:
            self.screen.blit(self.sprites[3], (200, 500))
        elif 15 <= self.level.player.move_counter < 20:
            self.screen.blit(self.sprites[6], (200, 500))
        elif 20 <= self.level.player.move_counter < 25:
            self.screen.blit(self.sprites[7], (200, 500))
        elif 25 <= self.level.player.move_counter < 28:
            self.screen.blit(self.sprites[9], (200, 500))
        elif self.level.player.move_counter == 28:
            # HIT!
            self.screen.blit(self.sprites[10], (200, 500))
        elif self.level.player.move_counter == 29:
            # HIT!
            self.screen.blit(self.sprites[11], (200, 500))
        elif self.level.player.move_counter == 30:
            self.screen.blit(self.sprites[10], (200, 500))
        else:
            self.screen.blit(self.sprites[0], (200, 500))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.menu.active:
                    self.menu.handle_event(event)
                elif self.death_screen.active:
                    self.death_screen.handle_event(event)
                    if not self.death_screen.active:
                        self.menu.active = True
                elif self.win_screen.active:
                    self.win_screen.handle_event(event)
                    if not self.win_screen.active:
                        self.menu.active = True
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.level.toggle_menu()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            self.screen.fill('black'
                             '')

            if self.menu.active:
                if self.val == 0:
                    self.play_menu_music()
                    self.val += 1
                for i in range(0, tiles):
                    self.screen.blit(bg_image, (i * bg_width + self.scroll, 0))
                self.scroll -= 1
                if abs(self.scroll) > bg_width:
                    self.scroll = 0
                self.screen.blit(bg_text, (0, 0))
                self.menu.draw(self.screen)

            elif self.death_screen.active:
                self.death_screen.draw(self.screen)

            elif self.win_screen.active:
                self.win_screen.draw(self.screen, self.mon_killed, self.save_hp)

            else:
                debug(self.level.counter, 10, 500)
                if self.level.moved_level:
                    self.mon_left = len(self.level.player.monster_list)
                    self.level.moved_level = False
                if self.level.m_val == 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('level1track.ogg')
                    pygame.mixer.music.play(-1, 1)
                    self.level.m_val = -1
                elif self.level.m_val == 1:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('level2.ogg')
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                    self.level.m_val = -1
                elif self.level.m_val == 2:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('music3.ogg')
                    pygame.mixer.music.play(-1)
                    self.level.m_val = -1
                    # play level 3 track
                elif self.level.m_val == 3:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('music4.ogg')
                    pygame.mixer.music.set_volume(5)
                    pygame.mixer.music.play(-1)
                    self.level.m_val = -1
                    # play level 4 track
                if self.win_was_active:
                    self.level = Level()
                    self.mon_left = len(self.level.player.monster_list)
                    self.win_was_active = False
                self.level.run()
                if self.level.player.Win:
                    self.save_hp = self.level.player.curr_hp
                    self.mon_killed = self.level.kill_count
                    self.unload_level()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("menu.ogg")
                    pygame.mixer.music.play(-1)
                    self.win_screen.active = True
                    self.win_was_active = True
                    continue
                self.BoogieBar()
                if self.level.player.mon_killed:
                    self.mon_left -= 1

                if self.level.player.curr_hp <= 0:
                    self.mon_killed = self.level.kill_count
                    self.unload_level()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('death.ogg')
                    pygame.mixer.music.play(-1, 10, 5000)
                    self.death_screen.active = True
                    self.level = Level()
                    self.mon_left = len(self.level.player.monster_list)
                self.display_ui()
            pygame.display.update()
            self.clock.tick(FPS)

    def play_menu_music(self):
        # put shit here MAN
        pygame.mixer.music.load('menu.ogg')
        pygame.mixer.music.play(-1)

    def unload_level(self):
        self.save_hp = self.level.player.curr_hp
        self.level.visible_sprites.empty()
        self.level.obstacles_sprites.empty()
        self.level.monster_list.clear()
        self.level.player = None
        self.level.monster = None
        self.val = 0


if __name__ == '__main__':
    game = Game()
    game.run()
