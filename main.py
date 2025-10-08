import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CUP_WIDTH = 100
CUP_HEIGHT = 120
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)

# Шрифты
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 36)

# Класс игры
class CupsGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Наперстки")
        self.clock = pygame.time.Clock()
        self.running = False
        self.points = 0
        self.cups = [
            {"rect": pygame.Rect(200, 300, CUP_WIDTH, CUP_HEIGHT), "has_ball": False},
            {"rect": pygame.Rect(350, 300, CUP_WIDTH, CUP_HEIGHT), "has_ball": False},
            {"rect": pygame.Rect(500, 300, CUP_WIDTH, CUP_HEIGHT), "has_ball": False}
        ]
        self.ball_img = None
        self.logo_img = None
        self.load_images()
        self.load_sounds()

    def load_images(self):
        try:
            self.logo_img = pygame.image.load("logo.png")
            self.logo_img = pygame.transform.scale(self.logo_img, (40, 40))
        except:
            print("Логотип не найден.")
            self.logo_img = None

        try:
            self.ball_img = pygame.image.load("ball.png")
            self.ball_img = pygame.transform.scale(self.ball_img, (30, 30))
        except:
            print("Изображение предмета не найдено.")
            self.ball_img = None

    def load_sounds(self):
        pygame.mixer.init()
        try:
            self.click_sound = pygame.mixer.Sound("sounds/click_sound.wav")
            self.win_sound = pygame.mixer.Sound("sounds/win_sound.wav")
            self.lose_sound = pygame.mixer.Sound("sounds/lose_sound.wav")
        except:
            print("Звуки не найдены.")
            self.click_sound = self.win_sound = self.lose_sound = None

    def start_game(self):
        # Сброс состояния
        for cup in self.cups:
            cup["has_ball"] = False
        # Выбираем случайный стакан
        random_cup = random.choice(self.cups)
        random_cup["has_ball"] = True
        print("Игра началась! Перемещение завершено.")

    def stop_game(self):
        self.running = False
        print("Игра остановлена.")

    def handle_click(self, pos):
        if not self.running:
            return

        # Проигрываем звук клика
        if self.click_sound:
            self.click_sound.play()

        for cup in self.cups:
            if cup["rect"].collidepoint(pos):
                if cup["has_ball"]:
                    self.points += 1
                    print("Правильно! +1 очко.")
                    if self.win_sound:
                        self.win_sound.play()
                else:
                    print("Неправильно!")
                    if self.lose_sound:
                        self.lose_sound.play()
                self.running = False  # После клика игра останавливается
                break

    def draw(self):
        self.screen.fill(WHITE)

        # Рисуем название игры и логотип
        title = title_font.render("THIMBLE RIALO", True, BLACK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
        if self.logo_img:
            self.screen.blit(self.logo_img, (SCREEN_WIDTH // 2 - 20, 60))

        # Счёт
        score = font.render(f"Очки: {self.points}", True, BLACK)
        self.screen.blit(score, (20, 20))

        # Рисуем стаканы
        for cup in self.cups:
            pygame.draw.rect(self.screen, BLUE, cup["rect"])
            pygame.draw.rect(self.screen, BLACK, cup["rect"], 2)

        # Если игра остановлена, показываем предмет под выигрышным стаканом
        if not self.running and any(cup["has_ball"] for cup in self.cups):
            for cup in self.cups:
                if cup["has_ball"]:
                    if self.ball_img:
                        self.screen.blit(self.ball_img, (cup["rect"].centerx - 15, cup["rect"].centery - 15))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.running = True
                        self.start_game()
                    elif event.key == pygame.K_F2:
                        self.stop_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

# Запуск игры
if __name__ == "__main__":
    game = CupsGame()
    game.run()