import itertools
import math
import random


def mst_prim(points: list[tuple[float, float]]) -> dict[int, list[int]]:
    """Prim’salgorithmfromcity0;returnsthetree
    as{node:children}."""
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


def preorder(children: dict[int, list[int]], root: int = 0) -> list[int]:
    """Walkaroundthetree;visitingeachcityonce=
    shortcuttingrepeatedcities."""
    return [root] + [c for child in children[root] for c in preorder(children, child)]


def tour_length(points, tour) -> float:
    return sum(
        math.dist(points[tour[i]], points[tour[(i + 1) % len(tour)]])
        for i in range(len(tour))
    )


random.seed(7)
points = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(9)]
approx = preorder(mst_prim(points))
optimal = min(
    ((0,) + p for p in itertools.permutations(range(1, len(points)))),
    key=lambda t: tour_length(points, t),
)

print(f"MST approximation: {approx}  L = {tour_length(points,approx):.2f}")
print(f"Optimal (brute):   {list(optimal)}  L = {tour_length(points,optimal):.2f}")
print(
    f"Ratio = {tour_length(points,approx)/tour_length(points,optimal):.3f}  (guaranteed <= 2)"
)
