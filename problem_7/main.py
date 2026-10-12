def knapsack(values: list[int], weights: list[int], W: int):
    n = len(values)
    K = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        v, w = values[i - 1], weights[i - 1]
        for c in range(W + 1):
            K[i][c] = K[i - 1][c]
            if w <= c:
                K[i][c] = max(K[i][c], v + K[i - 1][c - w])
    chosen, c = [], W
    for i in range(n, 0, -1):
        if K[i][c] != K[i - 1][c]:
            chosen.append(i - 1)
            c -= weights[i - 1]
    return K, K[n][W], chosen[::-1]


items, values, weights = ["A", "B", "C"], [60, 100, 120], [10, 20, 30]

K, best, chosen = knapsack(values, weights, 50)

print("capacity:", *[f"{c:4d}" for c in range(0, 51, 10)])
for i, row in enumerate(K):
    print(
        f"{'-' if i == 0 else '+' + items[i - 1]}:",
        *[f"{row[c]:4d}" for c in range(0, 51, 10)],
    )
print(f"Best value = {best} with items {[items[i] for i in chosen]}")
