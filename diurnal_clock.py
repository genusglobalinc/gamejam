def draw_circle_with_labels():
    grid = [[' ' for _ in range(29)] for _ in range(15)]

    labels = [
        ("12", "Aries"), ("11", "Taurus"), ("10", "Gemini"),
        ("9", "Cancer"), ("8", "Leo"), ("7", "Virgo"),
        ("6", "Libra"), ("5", "Scorpio"), ("4", "Sagittarius"),
        ("3", "Capricorn"), ("2", "Aquarius"), ("1", "Pisces")
    ]

    positions = [
        (14, 0), (10, 1), (7, 4), (4, 7), (1, 10), (0, 14),
        (1, 18), (4, 21), (7, 24), (10, 27), (14, 28), (18, 27),
        (21, 24), (24, 21), (27, 18), (28, 14), (27, 10), (24, 7),
        (21, 4), (18, 1)
    ]

    for idx, ((x, y), (house, zodiac)) in enumerate(zip(positions, labels)):
        grid[y][x:x + len(house)] = house
        grid[y + 1][x:x + len(zodiac)] = zodiac

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
