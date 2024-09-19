import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
BLOCK_SIZE = 50
INITIAL_BLOCK_FALL_SPEED = 5
PLAYER_SPEED = 7

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Dodge the Blocks")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Define the player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)
        self.shielded = False
        self.shield_start_time = 0

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if direction == "right" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED

    def activate_shield(self):
        self.shielded = True
        self.shield_start_time = time.time()

    def check_shield(self):
        if self.shielded and time.time() - self.shield_start_time > 5:  # Shield lasts 5 seconds
            self.shielded = False

    def draw(self, screen):
        color = GREEN if self.shielded else BLUE
        pygame.draw.rect(screen, color, self.rect)

# Define the block class
class Block:
    def __init__(self, speed):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - BLOCK_SIZE), 0, BLOCK_SIZE, BLOCK_SIZE)
        self.speed = speed

    def fall(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

# Define the power-up class
class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - BLOCK_SIZE), 0, BLOCK_SIZE, BLOCK_SIZE)
        self.type = random.choice(["shield"])  # You can add more power-ups in the future

    def fall(self):
        self.rect.y += 4  # Power-ups fall slower than blocks

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

# Function to detect collision between player and blocks or power-ups
def detect_collision(player, obj):
    return player.rect.colliderect(obj.rect)

# Function to display text on the screen
def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Start screen
def start_screen():
    screen.fill(WHITE)
    draw_text(screen, "Dodge the Blocks", 80, BLACK, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100)
    draw_text(screen, "Press any key to start", 50, BLACK, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 50)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Main game function
def game():
    player = Player()
    blocks = []
    powerups = []
    score = 0
    block_fall_speed = INITIAL_BLOCK_FALL_SPEED
    running = True

    while running:
        screen.fill(WHITE)

        # Create a new block every 20 frames
        if random.randint(1, 20) == 1:
            blocks.append(Block(block_fall_speed))

        # Create a new power-up randomly
        if random.randint(1, 500) == 1:  # Power-up appears rarely
            powerups.append(PowerUp())

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movement control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")

        # Block movement
        for block in blocks[:]:
            block.fall()
            block.draw(screen)

            if block.rect.top > SCREEN_HEIGHT:
                blocks.remove(block)
                score += 1  # Increase score for dodging

            if detect_collision(player, block):
                if player.shielded:
                    blocks.remove(block)
                else:
                    messagebox.showinfo("Game Over", f"Game Over! Your score: {score}")
                    running = False

        # Power-up movement and collection
        for powerup in powerups[:]:
            powerup.fall()
            powerup.draw(screen)

            if powerup.rect.top > SCREEN_HEIGHT:
                powerups.remove(powerup)

            if detect_collision(player, powerup):
                powerups.remove(powerup)
                player.activate_shield()

        # Check if shield is active
        player.check_shield()

        # Increase difficulty
        if score % 10 == 0 and score > 0:
            block_fall_speed += 0.1  # Speed increases as the score increases

        # Draw the player
        player.draw(screen)

        # Draw the score
        draw_text(screen, f"Score: {score}", 40, BLACK, 10, 10)

        # Update display
        pygame.display.update()

        # Frame rate control
        clock.tick(30)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    start_screen()  # Show the start screen
    game()
