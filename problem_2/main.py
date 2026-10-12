def knapsack(values: list[int], weights: list[int], W: int):
    n = len(values)

    items_info = [(i, values[i], weights[i], values[i] / weights[i]) for i in range(n)]

    items_info.sort(key=lambda x: x[3], reverse=True)

    chosen, best_value, current_weight = [], 0, 0

    for i, v, w, ratio in items_info:
        if current_weight + w <= W:
            chosen.append(i)
            best_value += v
            current_weight += w

    # Ordenar los índices elegidos para mantener el orden original
    chosen.sort()
    return best_value, chosen


items, values, weights = ["A", "B", "C"], [60, 100, 120], [10, 20, 30]

best, chosen = knapsack(values, weights, 50)

print(f"Best value = {best} with items {[items[i] for i in chosen]}")
