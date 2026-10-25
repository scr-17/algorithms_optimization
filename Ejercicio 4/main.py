import math
import random
import time

import matplotlib.pyplot as plt


def tour_length(points, tour) -> float:
    return sum(
        math.dist(points[tour[i]], points[tour[(i + 1) % len(tour)]])
        for i in range(len(tour))
    )


def two_opt_move(route: list, i: int, k: int) -> list:
    return route[:i] + route[i : k + 1][::-1] + route[k + 1 :]


def simulated_annealing(pts, initial_tour, schedule_type):
    current = initial_tour.copy()
    current_val = tour_length(pts, current)

    history = []
    start_time = time.perf_counter()

    T0 = 100.0
    T = T0

    for t in range(1, 1500):
        if T <= 0.001:
            break

        history.append(current_val)

        i, k = sorted(random.sample(range(len(current)), 2))
        next_tour = two_opt_move(current, i, k)
        next_val = tour_length(pts, next_tour)

        delta_E = next_val - current_val

        if delta_E < 0 or random.random() < math.exp(-delta_E / T):
            current = next_tour
            current_val = next_val

        if schedule_type == "linear":
            T = T0 - (0.07 * t)
        else:
            T = T * 0.995

    return current_val, history, time.perf_counter() - start_time


random.seed(42)
pts = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(20)]
initial_tour = random.sample(range(len(pts)), len(pts))

cal_lin, hist_lin, t_lin = simulated_annealing(pts, initial_tour, "linear")
cal_exp, hist_exp, t_exp = simulated_annealing(pts, initial_tour, "exponential")

print(f"{"Cooling Schedule":<20} | {"Final Cost":<20} | {"Time in seconds"}")
print(f"{"Linear":<20} | {cal_lin:<20.2f} | {t_lin:.4f}")
print(f"{"Exponential":<20} | {cal_exp:<20.2f} | {t_exp:.4f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(hist_lin, label="Linear", color="blue")
ax1.plot(hist_exp, label="Exponential", color="orange")
ax1.set_xlabel("Iterations")
ax1.set_ylabel("Tour Cost")
ax1.legend()

ax2.bar(["Linear", "Exponential"], [t_lin, t_exp], color=["blue", "orange"])
ax2.set_ylabel("Execution Time")

plt.tight_layout()
plt.show()
