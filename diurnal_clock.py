import math

def draw_circle():
    radius = 12
    labels = [
        ("House 12", "Aries"), ("House 11", "Taurus"), ("House 10", "Gemini"),
        ("House 9", "Cancer"), ("House 8", "Leo"), ("House 7", "Virgo"),
        ("House 6", "Libra"), ("House 5", "Scorpio"), ("House 4", "Sagittarius"),
        ("House 3", "Capricorn"), ("House 2", "Aquarius"), ("House 1", "Pisces")
    ]

    # Calculate points for the circle
    points = []
    for i in range(12):
        angle = 2 * math.pi * i / 12
        x = int(radius * math.cos(angle))
        y = int(radius * math.sin(angle))
        points.append((x, y))

    # Create an empty grid
    grid_size = radius * 2 + 3
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

    # Mark points on the grid with house numbers and zodiac names
    for idx, (x, y) in enumerate(points):
        label = f"{labels[idx][0]} {labels[idx][1]}"
        for char_idx, char in enumerate(label):
            grid[y + radius][x + radius + char_idx] = char

    # Print the circle
    for row in grid:
        print(''.join(row))

def draw_chart():
    houses = ["House " + str(i) for i in range(12, 0, -1)]
    zodiacs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
               "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    print(f"{'Houses':<10} {'Zodiacs':<10} {'Planets'}")
    print("-" * 30)
    for i in range(12):
        print(f"{houses[i]:<10} {zodiacs[i]:<10} {'':<10}")

if __name__ == "__main__":
    draw_circle()
    print("\n")
    draw_chart()
