def main():
    """Main function to initialize the game and start the game loop."""
    import pygame
    import random

    pygame.init()

    # Define colors
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 102)
    BLACK = (0, 0, 0)
    RED = (213, 50, 80)
    GREEN = (0, 255, 0)
    BLUE = (50, 153, 213)

    # Set display dimensions
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600

    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()

    SNAKE_BLOCK_SIZE = 10
    SNAKE_SPEED = 15

    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)

    def draw_snake(block_size, snake_segments):
        """Draw the snake on the display.

        Args:
            block_size (int): The size of each block of the snake.
            snake_segments (list): The segments of the snake.
        """
        for segment in snake_segments:
            pygame.draw.rect(display, BLACK, [segment[0], segment[1], block_size, block_size])

    def display_message(message, color):
        """Display a message on the screen.

        Args:
            message (str): The message to display.
            color (tuple): The color of the message.
        """
        message_surface = font_style.render(message, True, color)
        display.blit(message_surface, [DISPLAY_WIDTH / 6, DISPLAY_HEIGHT / 3])

    def game_loop():
        """Main loop for the game logic."""
        game_over = False
        game_close = False

        x_position = DISPLAY_WIDTH / 2
        y_position = DISPLAY_HEIGHT / 2

        x_change = 0
        y_change = 0

        snake_segments = []
        snake_length = 1

        # Generate initial food position
        food_x = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK_SIZE) / 10.0) * 10.0
        food_y = round(random.randrange(0, DISPLAY_HEIGHT - SNAKE_BLOCK_SIZE) / 10.0) * 10.0

        while not game_over:
            while game_close:
                display.fill(BLUE)
                display_message("You Lost! Press C to Play Again or Q to Quit", RED)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        elif event.key == pygame.K_c:
                            game_loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    # Change direction based on key press
                    if event.key == pygame.K_LEFT:
                        x_change = -SNAKE_BLOCK_SIZE
                        y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x_change = SNAKE_BLOCK_SIZE
                        y_change = 0
                    elif event.key == pygame.K_UP:
                        y_change = -SNAKE_BLOCK_SIZE
                        x_change = 0
                    elif event.key == pygame.K_DOWN:
                        y_change = SNAKE_BLOCK_SIZE
                        x_change = 0

            # Check for collision with boundaries
            if x_position >= DISPLAY_WIDTH or x_position < 0 or y_position >= DISPLAY_HEIGHT or y_position < 0:
                game_close = True

            # Update snake position
            x_position += x_change
            y_position += y_change
            display.fill(BLUE)
            pygame.draw.rect(display, GREEN, [food_x, food_y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])
            snake_head = [x_position, y_position]
            snake_segments.append(snake_head)
            if len(snake_segments) > snake_length:
                del snake_segments[0]

            # Check for collision with itself
            if snake_head in snake_segments[:-1]:
                game_close = True

            draw_snake(SNAKE_BLOCK_SIZE, snake_segments)

            pygame.display.update()

            # Check for food consumption
            if x_position == food_x and y_position == food_y:
                food_x = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK_SIZE) / 10.0) * 10.0
                food_y = round(random.randrange(0, DISPLAY_HEIGHT - SNAKE_BLOCK_SIZE) / 10.0) * 10.0
                snake_length += 1

            clock.tick(SNAKE_SPEED)

        pygame.quit()
        quit()

    game_loop()