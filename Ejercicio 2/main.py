import matplotlib.pyplot as plt


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


def knapsack_greedy(values: list[int], weights: list[int], W: int):
    order = sorted(range(len(weights)), key=lambda i: weights[i])
    val, c, chosen = 0, W, []
    for i in order:
        if weights[i] <= c:
            chosen.append(i)
            val += values[i]
            c -= weights[i]
    return val, chosen


for cases in range(2):
    items = ["A", "B", "C", "D"]
    values = [100, 5, 5, 5] if cases == 0 else [10, 15, 25, 12]
    weights = [10, 4, 4, 2] if cases == 0 else [2, 3, 5, 8]

    K, best, chosen = knapsack(values, weights, 10)
    best_gr, chosen_gr = knapsack_greedy(values, weights, 10)

    print(f"\nGreedy {"Worst" if cases == 0 else "Equal"} case\n")

    print(f"{"Item":<10} | {"Weight":<10} | {"Value"}")
    for i in range(len(items)):
        print(f"{items[i]:<10} | {weights[i]:<10} | {values[i]}")
    print(
        f"Optimal: Value = {best} with items {[items[i] for i in chosen]} and used weight = {sum([weights[i] for i in chosen])}"
    )
    print(
        f"Greedy: Value = {best_gr} with items {[items[i] for i in chosen_gr]} and used weight = {sum([weights[i] for i in chosen_gr])}"
    )

    cap = sum(weights[i] for i in chosen)
    cap_gr = sum(weights[i] for i in chosen_gr)

    labels = ["Best", "Greedy"]
    valores = [best, best_gr]
    capacities = [cap, cap_gr]

    plt.bar(
        [pos - 0.35 / 2 for pos in [0, 1]],
        valores,
        width=0.35,
        label="Total Value",
        color="blue",
    )
    plt.bar(
        [pos + 0.35 / 2 for pos in [0, 1]],
        capacities,
        width=0.35,
        label="Used Weight",
        color="orange",
    )

    plt.xticks([0, 1], labels)
    plt.legend()
    plt.show()
