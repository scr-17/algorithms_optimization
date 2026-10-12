import multiprocessing as mp
import random
import time


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

    print("\nSpeedup")
    i, times = 1, []
    while i <= 8:
        print(f"{i} processes")
        t0 = time.perf_counter()
        with mp.Pool(processes=i) as pool:
            results = pool.map(estimate_pi, list(range(i)))
        t_plot = time.perf_counter() - t0
        print(f"Time: {t_plot:.3f}")
        i *= 2
