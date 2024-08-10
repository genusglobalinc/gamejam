def draw_circle_with_labels():
    # Define the grid size and create an empty grid
    grid_size = 25
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
        (12, 0), (16, 2), (19, 6), (21, 12), (19, 18), (16, 22),
        (12, 24), (8, 22), (5, 18), (3, 12), (5, 6), (8, 2)
    ]

    # Place the labels on the grid
    for idx, ((x, y), (house, zodiac)) in enumerate(zip(positions, labels)):
        grid[y][x:x + len(house)] = house
        grid[y + 1][x - 2:x - 2 + len(zodiac)] = zodiac

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
