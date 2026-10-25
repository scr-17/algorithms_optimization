import multiprocessing as mp
import random
import time

import matplotlib.pyplot as plt


def estimate_pi(seed: int, samples: int = 1_000_000) -> float:
    rng = random.Random(seed)
    inside = sum(rng.random() ** 2 + rng.random() ** 2 <= 1.0 for _ in range(samples))
    return 4 * inside / samples


if __name__ == "__main__":

    seeds = list(range(8))

    t0 = time.perf_counter()
    seq_results = [estimate_pi(s) for s in seeds]
    t_seq = time.perf_counter() - t0

    t0 = time.perf_counter()
    with mp.Pool(processes=mp.cpu_count()) as pool:
        par_results = pool.map(estimate_pi, seeds)
    t_par = time.perf_counter() - t0

    print(f"Sequential wall-clock: {t_seq:.3f} s")
    print(f"Parallel wall-clock:   {t_par:.3f} s (Speedup: {t_seq/t_par:.2f}x)")
    print(
        f"pi estimate (mean of {len(seeds)} runs): {sum(par_results)/len(par_results):.5f}"
    )

    processes_list = [1, 2, 4, 8]
    recorded_times = []

    for proc in processes_list:
        seeds = list(range(proc))
        t0 = time.perf_counter()
        with mp.Pool(processes=proc) as pool:
            pool.map(estimate_pi, seeds)
        t_par = time.perf_counter() - t0
        recorded_times.append(t_par)
        print(f"Processes: {proc}, Time: {t_par:.3f} s")

    plt.figure(figsize=(8, 5))
    plt.plot(processes_list, recorded_times, marker="o", linestyle="-", color="red")
    plt.xlabel("Processes")
    plt.ylabel("Time")
    plt.grid(True)
    plt.xticks(processes_list)
    plt.show()
