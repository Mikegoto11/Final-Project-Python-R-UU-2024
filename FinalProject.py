# Constants
screen_width = 800
screen_height = 600
card_width = 100
card_height = 150
card_margin = 20
text_margin = 10
button_width = 150
button_height = 50
set_display_time = 800  # Time to display "SET!" in milliseconds

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SET Card Game')
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 100)

# Colors (R, G, B)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (128, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
highlight_color = (255, 255, 0)
button_color = (0, 128, 255)

# Difficulty levels
difficulty_levels = {
    'easy': 60,
    'medium': 40,
    'hard': 20,
    'veteran': 10
}

