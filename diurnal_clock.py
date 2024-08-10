import math

def draw_circle_with_labels():
    # Define the size of the grid and the radius of the circle
    grid_size = 31
    radius = 14
    center = grid_size // 2
    
    # Create an empty grid
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Labels for the houses and zodiacs
    labels = [
        ("12", "Aries"), ("11", "Taurus"), ("10", "Gemini"),
        ("9", "Cancer"), ("8", "Leo"), ("7", "Virgo"),
        ("6", "Libra"), ("5", "Scorpio"), ("4", "Sagittarius"),
        ("3", "Capricorn"), ("2", "Aquarius"), ("1", "Pisces")
    ]
    
    # Calculate positions around the circle and place labels
    for idx, (house, zodiac) in enumerate(labels):
        # Angle in radians
        angle = 2 * math.pi * idx / 12
        # Calculate x and y positions based on the center and radius
        x = int(center + radius * math.cos(angle))
        y = int(center + radius * math.sin(angle))
        
        # Place house number
        grid[y][x] = house
        
        # Determine label position for zodiac, offsetting to avoid overlap
        label_x = x + (2 if math.cos(angle) >= 0 else -6)
        label_y = y + (1 if math.sin(angle) >= 0 else -1)
        
        # Ensure the label stays within grid boundaries
        if 0 <= label_x < grid_size and 0 <= label_y < grid_size:
            for i, char in enumerate(zodiac):
                if 0 <= label_x + i < grid_size:
                    grid[label_y][label_x + i] = char

    # Draw the circle itself by approximating the points
    for angle in range(360):
        rad = math.radians(angle)
        x = int(center + radius * math.cos(rad))
        y = int(center + radius * math.sin(rad))
        if 0 <= x < grid_size and 0 <= y < grid_size:
            grid[y][x] = '*'

    # Print the grid to display the circle
    for row in grid:
        print(''.join(row))

def draw_chart():
    houses = ["House 12", "House 11", "House 10", "House 9", "House 8", "House 7",
              "House 6", "House 5", "House 4", "House 3", "House 2", "House 1"]
    zodiacs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
               "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    print(f"{'Houses':<10} {'Zodiacs':<10} {'Planets'}")
    print("-" * 30)
    for i in range(12):
        print(f"{houses[i]:<10} {zodiacs[i]:<10} {'':<10}")

if __name__ == "__main__":
    draw_circle_with_labels()
    print("\n")
    draw_chart()
