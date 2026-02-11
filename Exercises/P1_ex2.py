import pygame
import numpy as np
import matplotlib.pyplot as plt
import random


pygame.init()
WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Distribution Identification Game")

font = pygame.font.SysFont(None, 36)

score = 0



# ----- Distributions -----

def generate_data(name):
    rng = np.random.default_rng()
    if name == "Uniform Integers":
        return rng.integers(low=0, high=10, size=1000)
    elif name == "Uniform":
        return rng.uniform(low=-2, high=2, size=1000)
    elif name == "Normal":
        return rng.normal(loc=0, scale=1, size=1000)
    elif name == "Binomial":
        return rng.binomial(n=10, p=0.5, size=1000)
    elif name == "Negative Binomial":
        return rng.negative_binomial(n=5, p=0.5, size=1000)
    elif name == "Gamma":
        return rng.gamma(shape=2, scale=1, size=1000)
    elif name == "Geometric":
        return rng.geometric(p=0.5, size=1000)
    
distributions = ["Uniform Integers", "Uniform", "Normal", "Binomial", "Negative Binomial", "Gamma", "Geometric"]


# ----- Create Histogram Image -----

def create_histogram(data, cum):
    plt.figure(figsize=(6, 4))
    plt.hist(data, bins=30, cumulative = cum)
    plt.title("Identify the Distribution")
    plt.savefig("hist.png")
    plt.close()


# ----- Game Loop -----

running = True
clock = pygame.time.Clock()

current_distribution = random.choice(distributions)
cum = random.choice([True, False])
data = generate_data(current_distribution)
create_histogram(data, cum)
hist_image = pygame.image.load("hist.png")
hist_image = pygame.transform.smoothscale(hist_image, (800, 450))

while running:
    screen.fill((255, 255, 255))
    screen.blit(hist_image, (100, 50))
    answer_start_y = 550
    spacing = 45

    for i, dist in enumerate(distributions):
        text = font.render(f"{i+1}. {dist}", True, (0, 0, 0))
        screen.blit(text, (150, answer_start_y + i*spacing))

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (800, 20))

    hist_type_text = "Cumulative" if cum else "Regular"
    text = font.render(hist_type_text, True, (0, 0, 0))
    screen.blit(text, (120, 510))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]:
                guess = distributions[event.key - pygame.K_1]

                if guess == current_distribution:
                    score += 1

                
                current_distribution = random.choice(distributions)
                cum = random.choice([True, False])
                data = generate_data(current_distribution)
                create_histogram(data, cum)
                hist_image = pygame.image.load("hist.png")
                hist_image = pygame.transform.smoothscale(hist_image, (800, 450))

    clock.tick(30)

pygame.quit()

