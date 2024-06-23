import pygame
import random
from itertools import combinations
import os

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

# Construct the path to the 'kaarten' directory in the Downloads folder
image_dir = os.path.join(os.path.expanduser("~"), 'Downloads', 'kaarten')

# Verify that the directory exists
if not os.path.isdir(image_dir):
    print("Directory path does not exist. Please ensure the 'kaarten' directory is in the Downloads folder.")
    exit()

# Function to load images
def load_images():
    images = {}
    for filename in os.listdir(image_dir):
        if filename.endswith(".gif"):
            key = filename[:-4]  # Remove the '.gif' extension
            images[key] = pygame.image.load(os.path.join(image_dir, filename)).convert()
    print(f"Loaded image keys: {list(images.keys())}")  # Print loaded image keys for debugging
    return images

# SET Card Class
class SetCard:
    def __init__(self, color, symbol, shading, number):
        self.color = color
        self.symbol = symbol
        self.shading = shading
        self.number = number
        self.image_key = f'{color}{symbol}{shading}{number}'

    def __str__(self):
        return f'Color: {self.color}, Symbol: {self.symbol}, Shading: {self.shading}, Number: {self.number}'

    def draw(self, surface, x, y, index, highlight=False):
        if self.image_key in images:
            image = images[self.image_key]
            # Resize image to fit card dimensions
            image = pygame.transform.scale(image, (card_width, card_height))
            pygame.draw.rect(surface, white, (x, y, card_width, card_height))
            pygame.draw.rect(surface, black, (x, y, card_width, card_height), 2)
            surface.blit(image, (x, y))
            
            # Draw card index
            text = font.render(str(index + 1), True, black)
            surface.blit(text, (x + text_margin, y + text_margin))
        else:
            print(f"Missing image for key: {self.image_key}")  # Log missing images for debugging

# Function to check if three cards form a SET
def is_set(card1, card2, card3):
    attributes = ['color', 'symbol', 'shading', 'number']
    for attribute in attributes:
        attr1 = getattr(card1, attribute)
        attr2 = getattr(card2, attribute)
        attr3 = getattr(card3, attribute)
        if not ((attr1 == attr2 == attr3) or (attr1 != attr2 != attr3 != attr1)):
            return False
    return True

# Function to find all sets from a collection of cards
def find_all_sets(cards):
    all_sets = []
    for combo in combinations(cards, 3):
        if is_set(*combo):
            all_sets.append(combo)
    return all_sets

# Function to find one set from a collection of cards
def find_one_set(cards):
    for combo in combinations(cards, 3):
        if is_set(*combo):
            return combo
    return None

# Generate a random deck of SET cards
def generate_deck():
    deck = []
    colors = ['red', 'green', 'purple']
    symbols = ['diamond', 'squiggle', 'oval']
    shadings = ['empty', 'filled', 'shaded']
    numbers = [1, 2, 3]

    for color in colors:
        for symbol in symbols:
            for shading in shadings:
                for number in numbers:
                    deck.append(SetCard(color, symbol, shading, number))
    random.shuffle(deck)
    return deck

# Save and load high scores
def load_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def save_high_scores(score):
    with open("high_scores.txt", "w") as file:
        file.write(str(score))

def reset_high_scores():
    with open("high_scores.txt", "w") as file:
        file.write("0")

# Draw buttons for the game
def draw_button(surface, x, y, width, height, text, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, button_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(surface, button_color, (x, y, width, height), 2)

    text_surface = font.render(text, True, white)
    surface.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
