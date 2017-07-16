import random

p = 0
successes = 0
near = 0
thirds = 0
fourths = 0

while p < 10000:
    p = p + 1
    x = random.randint(0, 360)
    y = random.randint(0, 180)
    # print(str(x) + ', ' + str(y))

    p2 = 0
    distpts = []
    while p2 < 50:
        x2 = random.randint(0, 360)
        y2 = random.randint(0, 180)
        truedist = (x2 - x) * (x2 - x) + (y2 - y) * (y2 - y)
        fakedist = (7 * x2 + y2) * (7 * x2 + y2)
        fakedist = fakedist / (7 * x + y) / (7 * x + y)
        distpts.append({ "point": [x2, y2], "p2": p2, "td": truedist, "fd": fakedist })
        p2 = p2 + 1

    closest = sorted(distpts, key=lambda pt: pt["td"])
    fake_closest = sorted(distpts, key=lambda pt: abs(1 - pt["fd"]))


    if closest[0]["p2"] == fake_closest[0]["p2"]:
        successes = successes + 1
    elif closest[0]["p2"] == fake_closest[1]["p2"]:
        near = near + 1
    elif closest[0]["p2"] == fake_closest[2]["p2"]:
        thirds = thirds + 1
    elif closest[0]["p2"] == fake_closest[3]["p2"]:
        fourths = fourths + 1

print("successes: " + str(successes / 100))
print("2nd: " + str(near / 100))
print("3rd: " + str(thirds / 100))
print("4th: " + str(fourths / 100))
print("top 4:" + str((successes + near + thirds + fourths) / 100))
