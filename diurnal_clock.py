def draw_circle_with_labels():
    # Define the grid size and create an empty grid
    grid_size = 27
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

    # Labels for the houses and zodiacs
    labels = [
        ("12", "Aries"), ("11", "Taurus"), ("10", "Gemini"),
        ("9", "Cancer"), ("8", "Leo"), ("7", "Virgo"),
        ("6", "Libra"), ("5", "Scorpio"), ("4", "Sagittarius"),
        ("3", "Capricorn"), ("2", "Aquarius"), ("1", "Pisces")
    ]

    # Positions on the grid for each label (approximately circular)
    positions = [
        (13, 0), (17, 2), (20, 6), (22, 12), (20, 18), (17, 22),
        (13, 24), (9, 22), (6, 18), (4, 12), (6, 6), (9, 2)
    ]

    # Place the labels on the grid
    for idx, ((x, y), (house, zodiac)) in enumerate(zip(positions, labels)):
        # Ensure we don't go out of bounds on the grid
        if 0 <= y < grid_size and 0 <= x < grid_size:
            grid[y][x:x + len(house)] = list(house)
            # Ensure the zodiac label fits within the grid
            zodiac_x = max(0, min(x - 2, grid_size - len(zodiac)))
            zodiac_y = y + 1
            if 0 <= zodiac_y < grid_size:
                grid[zodiac_y][zodiac_x:zodiac_x + len(zodiac)] = list(zodiac)

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
