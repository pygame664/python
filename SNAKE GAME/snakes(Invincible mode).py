import pygame
import random
import time
import sys
from pygame.locals import *


pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 60
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0)
}


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("snakes(Invincible mode)")
        self.clock = pygame.time.Clock()
        self.high_score = self.load_high_score()
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.obstacles = []
        self.score = 0
        self.speed = 0.2
        self.last_move = time.time()
        self.game_over = False
        self.generate_obstacles()
        self.food.generate(self.snake.body, self.obstacles)

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(max(self.score, self.high_score)))

    def generate_obstacles(self):
        self.obstacles = []
        for _ in range(10):
            x = random.randint(3, (WIDTH//CELL_SIZE)-4) * CELL_SIZE
            y = random.randint(3, (HEIGHT//CELL_SIZE)-4) * CELL_SIZE
            width = random.randint(1, 3) * CELL_SIZE
            height = random.randint(1, 3) * CELL_SIZE
            self.obstacles.append(pygame.Rect(x, y, width, height))

class Snake:
    def __init__(self):
        self.body = [pygame.Rect(WIDTH//2, HEIGHT//2, CELL_SIZE, CELL_SIZE)]
        self.direction = (1, 0)
        self.length = 3
        self.speed_boost = 1

    def move(self):
        head = self.body[0].copy()
        head.move_ip(self.direction[0]*CELL_SIZE*self.speed_boost, 
                    self.direction[1]*CELL_SIZE*self.speed_boost)
        self.body.insert(0, head)
        if len(self.body) > self.length:
            self.body.pop()



class Food:
    TYPES = [
        {'color': COLORS['red'], 'score': 1, 'effect': None},
        {'color': COLORS['green'], 'score': 2, 'effect': 'speed_up'},
        {'color': COLORS['blue'], 'score': 3, 'effect': 'slow_down'},
        {'color': COLORS['yellow'], 'score': 5, 'effect': 'wall_pass'}
    ]

    def __init__(self):
        self.type = random.choice(self.TYPES)
        self.rect = pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE)
        self.last_generated = time.time()

    def generate(self, snake_body, obstacles):
        while True:
            self.type = random.choice(self.TYPES)
            self.rect.x = random.randint(0, (WIDTH-CELL_SIZE)//CELL_SIZE) * CELL_SIZE
            self.rect.y = random.randint(0, (HEIGHT-CELL_SIZE)//CELL_SIZE) * CELL_SIZE
            if not any(self.rect.colliderect(segment) for segment in snake_body) and \
               not any(self.rect.colliderect(obstacle) for obstacle in obstacles):
                self.last_generated = time.time()
                break

    def check_expired(self):
        return time.time() - self.last_generated > 5

def draw_text(surface, text, size, color, x, y):
    font = pygame.font.SysFont('arial', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game.save_high_score()
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.save_high_score()
                    pygame.quit()
                    sys.exit()
                elif not game.game_over:
                    new_dir = None
                    if event.key == K_RIGHT and game.snake.direction != (-1, 0):
                        new_dir = (1, 0)
                    elif event.key == K_LEFT and game.snake.direction != (1, 0):
                        new_dir = (-1, 0)
                    elif event.key == K_UP and game.snake.direction != (0, 1):
                        new_dir = (0, -1)
                    elif event.key == K_DOWN and game.snake.direction != (0, -1):
                        new_dir = (0, 1)
                    elif event.key == K_F1:
                        game.speed = 0.2
                    elif event.key == K_F2:
                        game.speed = 0.1
                    elif event.key == K_F3:
                        game.speed = 0.05
                    elif event.key == K_SPACE and game.game_over:
                        game.reset_game()
                    if new_dir:
                        game.snake.direction = new_dir

        if not game.game_over:
            if time.time() - game.last_move > game.speed:
                game.snake.move()
                game.last_move = time.time()

                if game.snake.body[0].colliderect(game.food.rect):
                    game.snake.length += 20
                    game.score += game.food.type['score']
                elif game.food.type['effect'] == 'slow_down':
                    game.snake.speed_boost = 0.5
                        
                    game.food.generate(game.snake.body, game.obstacles)


        game.screen.fill(COLORS['black'])

        for obstacle in game.obstacles:
            pygame.draw.rect(game.screen, COLORS['white'], obstacle)

        for segment in game.snake.body:
            pygame.draw.rect(game.screen, COLORS['green'], segment)
        
        pygame.draw.rect(game.screen, game.food.type['color'], game.food.rect)

        draw_text(game.screen, f"Score: {game.score}", 18, COLORS['white'], WIDTH//2, 10)
        draw_text(game.screen, f"High Score: {game.high_score}", 18, COLORS['white'], WIDTH//2, 30)
        
        if game.game_over:
            draw_text(game.screen, "Game Over!", 50, COLORS['red'], WIDTH//2, HEIGHT//2)
            draw_text(game.screen, "Press SPACE to restart", 24, COLORS['white'], WIDTH//2, HEIGHT//2 + 50)

        pygame.display.flip()
        game.clock.tick(FPS)

if __name__ == "__main__":
    main()
