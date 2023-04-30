import pygame
import random
from Fenwick import FenwickTree

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Median Finder")
pygame.font.init()
SCORE_FONT = pygame.font.SysFont("Times New Roman", 20)

# Set the font and colors
font = pygame.font.SysFont(None, 30)
LIGHTPINK = (255, 182, 193)
RED = (255, 0, 0)

# Initialize variables
numbers = []
choices = []
score = 0

def find_list_median(lst):
    max_value = max(lst)
    fenwick_tree = FenwickTree(max_value)

    for num in lst:
        fenwick_tree.update(num, 1)

    return fenwick_tree.find_median()

# Quiz functions
def generate_choices(median):
    choices = [int(median),random.choice(numbers), random.choice(numbers) ]
    random.shuffle(choices)
    return choices

def render_quiz():
    global numbers, choices, score
    # Generate the numbers
    numbers = [random.randint(1, 100) for i in range(5)]
    # Find the median
    median = find_list_median(numbers)
    # Generate the choices
    choices = generate_choices(median)
    # Render the quiz
    screen.fill(LIGHTPINK)
    text = font.render(f"Select the median of: {numbers}", True, RED)
    screen.blit(text, (50, 50))
    text = font.render(f"A) {choices[0]}  B) {choices[1]}  C) {choices[2]}", True, RED)
    screen.blit(text, (50, 100))
    text = font.render(f"Score: {score}", True, RED)
    screen.blit(text, (50, 150))
    pygame.display.update()

def check_answer(choice):
    global score
    median = find_list_median(numbers)
    if choice == "A" and choices[0] == median:
        score += 1
        text = font.render("Correct!!", True, RED)
        screen.blit(text, (50, 200))
    elif choice == "B" and choices[1] == median:
        score += 1
        text = font.render("Correct!!", True, RED)
        screen.blit(text, (50, 200))
    elif choice == "C" and choices[2] == median:
        score += 1
        text = font.render("Correct!!", True, RED)
        screen.blit(text, (50, 200))
    else:
        text = font.render("Wrong!!", True, RED)
        screen.blit(text, (50, 200))
    pygame.display.update()
    # Wait for 1 second before rendering the next quiz
    pygame.time.delay(1000)
    render_quiz()

def main():
    # Set the initial score to 0 and the number of rounds to 5
    global score
    score = 0

    # Render the first quiz
    render_quiz()
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    check_answer("A")
                elif event.key == pygame.K_b:
                    check_answer("B")
                elif event.key == pygame.K_c:
                    check_answer("C")

    # Game over screen
    game_over = True
    while game_over:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False

        # Draw the game over screen
        screen.fill((255, 182, 193))
        game_over_text = SCORE_FONT.render("Quiz Over !", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - 50, screen_height // 2 - 20))
        final_score_text = SCORE_FONT.render(f"Final Score: {score}", True, (255, 0, 0))
        screen.blit(final_score_text, (screen_width // 2 - 70, screen_height // 2 + 10))
        pygame.display.flip()

if __name__ == "__main__":
    main()