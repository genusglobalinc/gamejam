import pygame
import math
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zodiac and House Circle with Sections, Roman Numerals, and Planet Labels")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

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

# Roman numerals and corresponding planets
roman_numerals = ["I - Sun", "II - Moon", "III - Mars", "IV - Mercury", "V - Jupiter", "VI - Venus", "VII - Saturn"]

# Planet to house association
planet_house_association = {
    "I - Sun": "House 1",
    "II - Moon": "House 2",
    "III - Mars": "House 3",
    "IV - Mercury": "House 4",
    "V - Jupiter": "House 5",
    "VI - Venus": "House 6",
    "VII - Saturn": "House 7",
}

# Font settings
font = pygame.font.SysFont(None, 20)
big_font = pygame.font.SysFont(None, 24)

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
    
    # Draw the two additional lines to create 8 sections
    # First diagonal line
    pygame.draw.line(screen, green, (center[0] - radius, center[1] - radius), (center[0] + radius, center[1] + radius), 2)
    # Second diagonal line
    pygame.draw.line(screen, green, (center[0] - radius, center[1] + radius), (center[0] + radius, center[1] - radius), 2)
    
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

    # Number the 8 sections with Roman numerals and planet labels counter-clockwise starting from House 1
    for i in range(8):
        # Calculate the angle for numbering, starting from House 1 (top) and rotating counter-clockwise
        angle = 2 * math.pi * (i + 0.5) / 8
        # Calculate position for the section number
        x = int(center[0] + (radius / 2) * math.cos(angle))
        y = int(center[1] + (radius / 2) * math.sin(angle))
        # Render and place the Roman numeral with planet label
        numeral_index = (7 - i) % 7  # Reversed order, so that House 1 starts with "I"
        numeral_text = big_font.render(roman_numerals[numeral_index], True, black)
        numeral_rect = numeral_text.get_rect(center=(x, y))
        screen.blit(numeral_text, numeral_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

# Create the chart
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(planet_house_association.keys(), planet_house_association.values(), color='skyblue')
ax.set_xlabel('Planets')
ax.set_ylabel('Houses')
ax.set_title('Planet and House Association')

# Display the chart
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
