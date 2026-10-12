import math

cities = {"A": (0, 0), "B": (0, 3), "E": (2, 5), "D": (4, 3), "C": (4, 0)}


def tour_length(route: list[str]) -> float:
    return sum(
        math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]])
        for i in range(len(route))
    )


def two_opt_move(route: list[str], i: int, k: int) -> list[str]:
    return route[:i] + route[i : k + 1][::-1] + route[k + 1 :]


route = ["A", "D", "E", "B", "C"]
new_route = two_opt_move(route, 1, 3)
print(f"Before: {route}  L = {tour_length(route):.2f}")
print(f"After:  {new_route}  L = {tour_length(new_route):.2f}")
