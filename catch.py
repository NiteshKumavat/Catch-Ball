import pygame
import random
import sys

pygame.init()

# Game variables
LEVEL = 1
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Basket
basket_width = 80
basket_height = 20
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - 50

# Objects
object_radius = 15
object_speed = 3
objects = []
spawn_rate = 30  # Lower = more frequent

# Special object
special = None
special_time = True
special_radius = 20
special_speed = 2  # slower than normal balls

# Score & lives
score = 0
life = 1
font = pygame.font.SysFont(None, 36)
popup_text = None
popup_timer = 0

clock = pygame.time.Clock()


def spawn_object():
    x = random.randint(object_radius, WIDTH - object_radius)
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    objects.append({"x": x, "y": -object_radius, "color": color})


def draw_basket(x):
    pygame.draw.rect(screen, BLUE, (x, basket_y, basket_width, basket_height))


def draw_objects():
    for obj in objects:
        pygame.draw.circle(screen, obj["color"], (obj["x"], obj["y"]), object_radius)


def update_objects():
    global score, lives
    for obj in objects[:]:
        obj["y"] += object_speed

        if (basket_x <= obj["x"] <= basket_x + basket_width) and \
           (basket_y <= obj["y"] + object_radius <= basket_y + basket_height):
            objects.remove(obj)
            score += 1

        elif obj["y"] > HEIGHT:
            objects.remove(obj)



def show_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))


def show_level():
    level_text = font.render(f"Level: {LEVEL}", True, BLACK)
    screen.blit(level_text, (250, 10))


def special_object():
    global special
    x = random.randint(special_radius, WIDTH - special_radius)
    y = -special_radius
    special = {"x": x, "y": y, "color": GOLD}


def draw_special():
    if special:
        pygame.draw.circle(screen, special["color"], (special["x"], special["y"]), special_radius)


def special_update():
    global special_speed
    global special, score, life, popup_text, popup_timer
    if special:
        special["y"] += special_speed

        if (basket_x <= special["x"] <= basket_x + basket_width) and \
           (basket_y <= special["y"] + special_radius <= basket_y + basket_height):
            score += 5  # Bonus points
            popup_text = font.render("+5", True, GREEN)
            popup_timer = 30
            special = None

        elif special["y"] > HEIGHT:
            special = None
            life -= 1  

def show_popup():
    global popup_timer
    if popup_text and popup_timer > 0:
        screen.blit(popup_text, (basket_x + basket_width // 2 - 10, basket_y - 30))
        popup_timer -= 1


def game_over_screen():
    screen.fill(WHITE)
    over_text = font.render("GAME OVER", True, RED)
    final_score = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    screen.blit(final_score, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
    pygame.display.flip()
    pygame.time.delay(2000)


running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game over check
    if life <= 0:
        game_over_screen()
        break

    # Move basket with mouse
    basket_x = pygame.mouse.get_pos()[0] - basket_width // 2
    basket_x = max(0, min(basket_x, WIDTH - basket_width))

    # Spawn normal objects
    if random.randint(1, spawn_rate) == 1:
        spawn_object()

    # Spawn special occasionally
    if (random.randint(1, 30) > 25 and special is None and special_time) or score > 20:
        special_time = False
        special_object()

    # Update and draw
    update_objects()
    draw_objects()

    special_update()
    draw_special()

    draw_basket(basket_x)
    show_score()
    show_level()
    show_popup()

    # Level progression
    if score >= 30:
        LEVEL += 1
        special_speed += 1
        special_time = True
        score = 0
        object_speed += 1
        spawn_rate = max(10, spawn_rate - 2)

    pygame.display.flip()
    clock.tick(60 * LEVEL)

pygame.quit()
sys.exit()
