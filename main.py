import pygame
import random
import sys

# Constants
WIDTH = 400
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.reset_pos()
        self.speed = speed

    def reset_pos(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300, -100)

    def update(self):
        self.rect.y += self.speed

def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Car Racing Game")
    clock = pygame.time.Clock()

    while True: # Main Game Loop
        all_sprites = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        obstacle_speed = 5
        for i in range(3):
            obs = Obstacle(obstacle_speed)
            all_sprites.add(obs)
            obstacles.add(obs)

        score = 0
        game_running = True

        # Game session
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            all_sprites.update()

            # Check for avoided obstacles to increase score
            for obs in obstacles:
                if obs.rect.top > HEIGHT:
                    score += 1
                    obs.reset_pos()
                    # Increase speed slightly over time
                    obs.speed += 0.1

            # Collision detection
            if pygame.sprite.spritecollide(player, obstacles, False):
                game_running = False

            screen.fill(GRAY)
            all_sprites.draw(screen)
            draw_text(screen, f"Score: {score}", 32, WIDTH // 2, 10)

            pygame.display.flip()
            clock.tick(FPS)

        # Game Over Screen
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 4)
        draw_text(screen, f"Score: {score}", 32, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "Press any key to restart", 24, WIDTH // 2, HEIGHT * 3 / 4)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

if __name__ == "__main__":
    main()
