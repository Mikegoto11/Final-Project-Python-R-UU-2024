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

# Game state functions
def start_game(difficulty):
    global game_active, deck, cards_on_table, player_score, computer_score, timer_start, timer_limit, current_screen, set_found_time, display_set_message, display_computer_set_message
    game_active = True
    deck = generate_deck()
    cards_on_table = deck[:12]
    deck = deck[12:]
    player_score = 0
    computer_score = 0
    timer_limit = difficulty_levels[difficulty]
    timer_start = pygame.time.get_ticks()
    set_found_time = None  # Reset set found time
    display_set_message = False  # Initialize display_set_message
    display_computer_set_message = False  # Initialize display_computer_set_message
    current_screen = "game"

def pause_game():
    global game_active
    game_active = not game_active

# Main Loop

def main():
    global game_active, deck, cards_on_table, player_score, computer_score, timer_start, images, current_screen, timer_limit, set_found_time, display_set_message, display_computer_set_message

    images = load_images()  # Load images using the dynamically constructed path

    reset_high_scores()  # Reset high scores when the program starts

    game_active = False
    selected_indices = []
    high_score = load_high_scores()
    current_screen = "start"
    display_set_message = False
    display_computer_set_message = False
    set_found_time = 0

    while True:
        screen.fill(black)
        
        if current_screen == "game":
            if game_active:
                # Display the 12 cards
                for i, card in enumerate(cards_on_table):
                    x = (i % 4) * (card_width + card_margin) + card_margin
                    y = (i // 4) * (card_height + card_margin) + card_margin
                    card.draw(screen, x, y, i, highlight=(i in selected_indices))

                # Display high score in the top right corner
                high_score_text = font.render(f'High Score: {high_score}', True, white)
                screen.blit(high_score_text, (screen_width - high_score_text.get_width() - 10, 10))  # Top-right corner

                # Display the player score under the high score
                player_score_text = font.render(f'Score: {player_score}', True, white)
                screen.blit(player_score_text, (screen_width - player_score_text.get_width() - 10, 10 + high_score_text.get_height() + 10))  # Under high score

                # Display the computer score under the player score
                computer_score_text = font.render(f'Computer Score: {computer_score}', True, white)
                screen.blit(computer_score_text, (screen_width - computer_score_text.get_width() - 10, 10 + high_score_text.get_height() + player_score_text.get_height() + 20))  # Under player score

                # Timer display in the middle at the bottom
                elapsed_time = (pygame.time.get_ticks() - timer_start) // 1000
                timer_text = font.render(f'Time: {timer_limit - elapsed_time}', True, white)
                timer_text_rect = timer_text.get_rect(center=(screen_width // 2, screen_height - 40))  # Center at bottom
                screen.blit(timer_text, timer_text_rect)

                # Display selected cards
                selected_text = font.render('Selected Cards: ' + ', '.join(str(idx + 1) for idx in selected_indices), True, white)
                screen.blit(selected_text, (10, screen_height - 80))

                # Draw pause button
                draw_button(screen, screen_width - button_width - 10, screen_height - button_height - 10, button_width, button_height, "Pause", pause_game)

                # Display "SET!" if a set was found
                if display_set_message and pygame.time.get_ticks() - set_found_time < set_display_time:
                    set_text = big_font.render("SET!", True, green)
                    screen.blit(set_text, (screen_width // 2 - set_text.get_width() // 2, screen_height // 2 - set_text.get_height() // 2))
                else:
                    display_set_message = False

                # Display "Computer SET!" if the computer found a set
                if display_computer_set_message and pygame.time.get_ticks() - set_found_time < set_display_time:
                    set_text = big_font.render("Computer SET!", True, red)
                    screen.blit(set_text, (screen_width // 2 - set_text.get_width() // 2, screen_height // 2 - set_text.get_height() // 2))
                else:
                    display_computer_set_message = False

                pygame.display.flip()

                # Check if timer expired
                if elapsed_time >= timer_limit:
                    print("Time's up! Checking for sets.")
                    computer_set = find_one_set(cards_on_table)
                    display_set_message = False  # Reset display_set_message
                    display_computer_set_message = False  # Reset display_computer_set_message
                    if computer_set is not None:
                        computer_score += 1
                        set_found_time = pygame.time.get_ticks()  # Set the time when a set is found
                        display_computer_set_message = True  # Set flag to display "Computer SET!" message
                    timer_start = pygame.time.get_ticks()  # Reset timer
                    cards_on_table = cards_on_table[3:] + deck[:3]
                    deck = deck[3:]

                # Event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save_high_scores(high_score)
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Determine which card is clicked
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for i, card in enumerate(cards_on_table):
                            x = (i % 4) * (card_width + card_margin) + card_margin
                            y = (i // 4) * (card_height + card_margin) + card_margin
                            if x <= mouse_x <= x + card_width and y <= mouse_y <= y + card_height:
                                if i in selected_indices:
                                    selected_indices.remove(i)
                                else:
                                    selected_indices.append(i)
                                if len(selected_indices) == 3:
                                    selected_cards = [cards_on_table[idx] for idx in selected_indices]
                                    if is_set(*selected_cards):
                                        print("It's a SET!")
                                        player_score += 1
                                        set_found_time = pygame.time.get_ticks()  # Set the time when a set is found
                                        display_set_message = True  # Set flag to display "SET!" message
                                        display_computer_set_message = False  # Reset computer set message
                                        for idx in sorted(selected_indices, reverse=True):
                                            cards_on_table.pop(idx)
                                        cards_on_table.extend(deck[:3])
                                        deck = deck[3:]
                                        if player_score > high_score:
                                            high_score = player_score
                                            save_high_scores(high_score)
                                        timer_start = pygame.time.get_ticks()  # Reset timer when set is found
                                    else:
                                        print("Not a SET.")
                                    selected_indices.clear()
                                break
            else:
                # Display pause menu buttons
                draw_button(screen, screen_width // 2 - button_width // 2, screen_height // 2 - 100, button_width, button_height, "Resume", pause_game)
                draw_button(screen, screen_width // 2 - button_width // 2, screen_height // 2, button_width, button_height, "Home", lambda: set_screen("start"))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save_high_scores(high_score)
                        pygame.quit()
                        return

        elif current_screen == "start":
            # Display start button
            draw_button(screen, screen_width // 2 - button_width // 2, screen_height // 2 - 100, button_width, button_height, "Start", lambda: set_screen("difficulty"))

            # Display high score
            high_score_text = font.render(f'High Score: {high_score}', True, white)
            screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height - 100))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_scores(high_score)
                    pygame.quit()
                    return

        elif current_screen == "difficulty":
            # Display difficulty level buttons
            draw_button(screen, screen_width // 2 - button_width // 2, screen_height // 2 - 150, button_width, button_height, "Easy", lambda: start_game('easy'))
            draw_button(screen, screen_width // 2 - button_width // 2, screen_height // 2 - 50, button_width, button_height, "Medium", lambda: start_game('medium'))
            draw_button(screen, screen_width // 2 - button_width // 2, screen_height // 2 + 50, button_width, button_height, "Hard", lambda: start_game('hard'))
            draw_button(screen, screen_width // 2 - button_width // 2, screen_height // 2 + 150, button_width, button_height, "Veteran", lambda: start_game('veteran'))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_scores(high_score)
                    pygame.quit()
                    return

        pygame.display.flip()

def set_screen(screen_name):
    global current_screen
    current_screen = screen_name

if __name__ == "__main__":
    main()
