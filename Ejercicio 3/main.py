import math
import random

import matplotlib.pyplot as plt


def tour_length(points, tour) -> float:
    return sum(
        math.dist(points[tour[i]], points[tour[(i + 1) % len(tour)]])
        for i in range(len(tour))
    )


def two_opt_move(route: list, i: int, k: int) -> list:
    return route[:i] + route[i : k + 1][::-1] + route[k + 1 :]


def nearest_neighbour(pts):
    tour, unvisited = [0], set(range(1, len(pts)))
    while unvisited:
        next_c = min(unvisited, key=lambda c: math.dist(pts[tour[-1]], pts[c]))
        tour.append(next_c)
        unvisited.remove(next_c)
    return tour


def count_2opt_improvements(pts, t):
    improvements, improved, n = 0, True, len(t)
    while improved:
        improved = False
        for i in range(n - 1):
            for k in range(i + 1, n):
                if i == 0 and k == n - 1:
                    continue
                new_t = two_opt_move(t, i, k)
                if tour_length(pts, new_t) < tour_length(pts, t):
                    t, improved = new_t, True
                    improvements += 1
                    break
            if improved:
                break
    return improvements, tour_length(pts, t)


random.seed(67)
pts = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(15)]

imp_rand, cal_rand = [], []
imp_nn, cal_nn = [], []

for _ in range(30):
    t_rand = random.sample(range(len(pts)), len(pts))
    m_r, c_r = count_2opt_improvements(pts, t_rand)
    imp_rand.append(m_r)
    cal_rand.append(c_r)

    t_nn = nearest_neighbour(pts)
    m_n, c_n = count_2opt_improvements(pts, t_nn)
    imp_nn.append(m_n)
    cal_nn.append(c_n)

avg_imp_rand = sum(imp_rand) / len(imp_rand)
avg_cal_rand = sum(cal_rand) / len(cal_rand)
avg_imp_nn = sum(imp_nn) / len(imp_nn)
avg_cal_nn = sum(cal_nn) / len(cal_nn)

print(f"{"Initialization":<20} | {"Avg Improvements":<16} | {"Final Distance"}")
print(f"{"Random Start":<20} | {avg_imp_rand:<16.2f} | {avg_cal_rand:.2f}")
print(f"{"Nearest Neighbour":<20} | {avg_imp_nn:<16.2f} | {avg_cal_nn:.2f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
labels = ["Random\nStart", "Nearest\nNeighbour"]
colours = ["blue", "orange"]
ax1.bar(labels, [avg_imp_rand, avg_imp_nn], color=colours)
ax1.set_ylabel("Improvements")
ax1.set_title("Average Improvements")
ax2.bar(labels, [avg_cal_rand, avg_cal_nn], color=colours)
ax2.set_ylabel("Distance")
ax2.set_title("Optimum Quality")
plt.tight_layout()
plt.show()
