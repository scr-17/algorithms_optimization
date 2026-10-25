import math
import random

import matplotlib.pyplot as plt


def get_tour_length(points, tour):
    return sum(
        math.dist(points[tour[i]], points[tour[(i + 1) % len(tour)]])
        for i in range(len(tour))
    )


def two_opt_move(route, i, k):
    return route[:i] + route[i : k + 1][::-1] + route[k + 1 :]


def mst_prim(points):
    best = {v: (math.dist(points[0], points[v]), 0) for v in range(1, len(points))}
    children = {v: [] for v in range(len(points))}
    while best:
        v = min(best, key=lambda u: best[u][0])
        children[best.pop(v)[1]].append(v)
        for u in best:
            d = math.dist(points[v], points[u])
            if d < best[u][0]:
                best[u] = (d, v)
    return children


def preorder(children, root=0):
    return [root] + [c for child in children[root] for c in preorder(children, child)]


def local_search_2opt(points, tour):
    t = tour.copy()
    improved, n = True, len(t)
    while improved:
        improved = False
        for i in range(n - 1):
            for k in range(i + 1, n):
                if i == 0 and k == n - 1:
                    continue
                new_t = two_opt_move(t, i, k)
                if get_tour_length(points, new_t) < get_tour_length(points, t):
                    t, improved = new_t, True
                    break
            if improved:
                break
    return t


def simulated_annealing(points, initial_tour):
    curr = initial_tour.copy()
    curr_len = get_tour_length(points, curr)
    temp = 100.0

    for _ in range(1000):
        if temp <= 0.001:
            break
        i, k = sorted(random.sample(range(len(curr)), 2))
        nxt = two_opt_move(curr, i, k)
        nxt_len = get_tour_length(points, nxt)

        delta = nxt_len - curr_len
        if delta < 0 or random.random() < math.exp(-delta / temp):
            curr = nxt
            curr_len = nxt_len

        temp *= 0.99

    return curr


random.seed(7)
ratios = []
costs_mst, costs_mst_2opt, costs_ls, costs_sa = [], [], [], []

num_instances = 100
num_cities = 9

for _ in range(num_instances):
    pts = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(num_cities)]

    tour_mst = preorder(mst_prim(pts))
    c_mst = get_tour_length(pts, tour_mst)

    tour_mst_2opt = local_search_2opt(pts, tour_mst)
    c_mst_2opt = get_tour_length(pts, tour_mst_2opt)

    random_tour = random.sample(range(num_cities), num_cities)

    tour_ls = local_search_2opt(pts, random_tour)
    c_ls = get_tour_length(pts, tour_ls)

    tour_sa = simulated_annealing(pts, random_tour)
    c_sa = get_tour_length(pts, tour_sa)

    c_best = min(c_mst, c_mst_2opt, c_ls, c_sa)
    ratios.append(c_mst / c_best)

    costs_mst.append(c_mst)
    costs_mst_2opt.append(c_mst_2opt)
    costs_ls.append(c_ls)
    costs_sa.append(c_sa)

avg_ratio = sum(ratios) / num_instances
avg_mst = sum(costs_mst) / num_instances
avg_mst_2opt = sum(costs_mst_2opt) / num_instances
avg_ls = sum(costs_ls) / num_instances
avg_sa = sum(costs_sa) / num_instances

print(f"{"Avg Ratio (MST / Best Found)":<30} = {avg_ratio:.2f}")
print(f"{"Avg Cost - MST":<30} = {avg_mst:.2f}")
print(f"{"Avg Cost - MST + 2-opt":<30} = {avg_mst_2opt:.2f}")
print(f"{"Avg Cost - Local Search":<30} = {avg_ls:.2f}")
print(f"{"Avg Cost - Sim. Annealing":<30} = {avg_sa:.2f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

ax1.hist(ratios, bins=10, color="skyblue")
ax1.axvline(2.0, color="red", linestyle="--", label="Theoretical Limit = 2.0")
ax1.set_title("Approximation Ratio Distribution")
ax1.legend()

labels = ["MST", "MST\n+ 2-opt", "Local\nSearch", "Simulated\nAnnealing"]
averages = [avg_mst, avg_mst_2opt, avg_ls, avg_sa]
colors = ["orange", "green", "purple", "red"]

ax2.bar(labels, averages, color=colors)
ax2.set_title("Cost Comparison")
ax2.set_ylabel("Tour Cost")

plt.tight_layout()
plt.show()
