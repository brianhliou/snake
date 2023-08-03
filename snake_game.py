import pygame
import random

class SnakeGame:
    def __init__(self, width=200, height=200, snake_size=10):  # Increase snake_size to make the grid larger
        pygame.init()
        
        self.snake_size = snake_size
        self.speed = pygame.time.Clock()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Snake Game')

        # Initialize game state
        self.snake_pos = [[50, 40], [40, 40], [30, 40]]
        self.snake_speed = [snake_size, 0]  # Moving right
        self.food_pos = [random.randrange(1, (self.surface.get_width() // self.snake_size) - 1) * self.snake_size, 
                 random.randrange(1, (self.surface.get_height() // self.snake_size) - 1) * self.snake_size]  # Food position
        self.food_spawn = True
        self.score = 0

    def run(self):
        running = True
        game_started = False  # Game starts when this variable is True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # The player clicked the window's close button
                    running = False

                elif event.type == pygame.KEYDOWN and not game_started and event.key in [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]:  # The player pressed an arrow key
                    game_started = True

                if game_started:  # Only respond to keys if the game has started
                    if event.type == pygame.KEYDOWN:  # The player pressed a key
                        if event.key in [pygame.K_UP, ord('w')] and self.snake_speed[1] != self.snake_size:  # Up arrow or 'w'
                            self.snake_speed = [0, -self.snake_size]
                        if event.key in [pygame.K_DOWN, ord('s')] and self.snake_speed[1] != -self.snake_size:  # Down arrow or 's'
                            self.snake_speed = [0, self.snake_size]
                        if event.key in [pygame.K_LEFT, ord('a')] and self.snake_speed[0] != self.snake_size:  # Left arrow or 'a'
                            self.snake_speed = [-self.snake_size, 0]
                        if event.key in [pygame.K_RIGHT, ord('d')] and self.snake_speed[0] != -self.snake_size:  # Right arrow or 'd'
                            self.snake_speed = [self.snake_size, 0]
                            
            if game_started:
                # Update game state
                new_head = list(map(sum, zip(self.snake_pos[0], self.snake_speed)))
                
                # Check if snake has hit the boundary of the screen
                if (new_head[0] >= self.surface.get_width() or new_head[0] < 0 or
                    new_head[1] >= self.surface.get_height() or new_head[1] < 0 or
                    new_head in self.snake_pos):  # Check if snake is colliding with itself
                    running = False  # Game over

                self.snake_pos.insert(0, new_head)

                # If the snake has eaten food
                if self.snake_pos[0] == self.food_pos:
                    self.score += 1
                    self.food_spawn = False
                else:
                    self.snake_pos.pop()  # Remove last segment of snake

                # Spawn new food if needed
                if not self.food_spawn:
                    self.food_pos = [random.randrange(1, (self.surface.get_width() // self.snake_size) - 1) * self.snake_size,
                                    random.randrange(1, (self.surface.get_height() // self.snake_size) - 1) * self.snake_size]
                self.food_spawn = True

            # Draw everything
            self.surface.fill((0, 0, 0))  # Clear the screen
            for pos in self.snake_pos:
                pygame.draw.rect(self.surface, (0, 255, 0), pygame.Rect(pos[0], pos[1], self.snake_size, self.snake_size))  # Draw the snake
            pygame.draw.rect(self.surface, (255, 0, 0), pygame.Rect(self.food_pos[0], self.food_pos[1], self.snake_size, self.snake_size))  # Draw the food

            pygame.display.flip()
            self.speed.tick(15)  # Cap the game speed to 30 frames per second
            
            # print(f"Snake position: {self.snake_pos[0]}, Food position: {self.food_pos}")

        pygame.quit()