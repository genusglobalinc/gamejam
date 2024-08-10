import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zodiac and House Circle with Horizon and Meridian")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Define center and radius
center = (width // 2, height // 2)
radius = 200

# Labels for the houses and zodiacs
labels = [
    ("House 12", "Aries"), ("House 11", "Taurus"), ("House 10", "Gemini"),
    ("House 9", "Cancer"), ("House 8", "Leo"), ("House 7", "Virgo"),
    ("House 6", "Libra"), ("House 5", "Scorpio"), ("House 4", "Sagittarius"),
    ("House 3", "Capricorn"), ("House 2", "Aquarius"), ("House 1", "Pisces")
]

# Main loop
running = True
while running:
    screen.fill(white)
    
    # Draw the circle
    pygame.draw.circle(screen, black, center, radius, 2)
    
    # Draw the horizon (horizontal line)
    pygame.draw.line(screen, blue, (center[0] - radius, center[1]), (center[0] + radius, center[1]), 2)
    
    # Draw the meridian (vertical line)
    pygame.draw.line(screen, blue, (center[0], center[1] - radius), (center[0], center[1] + radius), 2)
    
    # Label the horizons
    font = pygame.font.SysFont(None, 24)
    east_text = font.render("East Horizon", True, black)
    west_text = font.render("West Horizon", True, black)
    
    screen.blit(east_text, (center[0] + radius + 10, center[1] - 12))
    screen.blit(west_text, (center[0] - radius - 110, center[1] - 12))
    
    # Calculate positions around the circle and place labels
    for idx, (house, zodiac) in enumerate(labels):
        # Angle in radians
        angle = 2 * math.pi * idx / 12
        # Calculate x and y positions based on the center and radius
        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))
        
        # Render and place house label
        house_text = font.render(house, True, black)
        house_rect = house_text.get_rect(center=(x, y))
        screen.blit(house_text, house_rect)
        
        # Render and place zodiac label (offset to avoid overlap)
        zodiac_x = x + (40 if math.cos(angle) >= 0 else -60)
        zodiac_y = y + (20 if math.sin(angle) >= 0 else -20)
        zodiac_text = font.render(zodiac, True, red)
        zodiac_rect = zodiac_text.get_rect(center=(zodiac_x, zodiac_y))
        screen.blit(zodiac_text, zodiac_rect)
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
