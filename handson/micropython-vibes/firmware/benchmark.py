import requests
import time
import statistics
import argparse

SERVER_URL = "http://localhost:5000/stream"
TEST_SIZES = [1024, 2048, 4096, 8192, 16384, 32768, 65536]


def benchmark_chunk_size(chunk_size, num_requests=3):
    """Benchmark throughput for a given chunk size."""
    times = []
    total_bytes = 0

    for _ in range(num_requests):
        start = time.perf_counter()
        response = requests.get(SERVER_URL, params={"chunk": chunk_size}, timeout=60)
        end = time.perf_counter()

        elapsed = end - start
        bytes_received = len(response.content)
        total_bytes = bytes_received

        throughput = bytes_received / elapsed if elapsed > 0 else 0
        times.append(elapsed)

        print(
            f"Chunk: {chunk_size:>6} B | Time: {elapsed:.3f}s | "
            f"Throughput: {throughput / 1024 / 1024:.2f} MB/s | "
            f"Bytes: {bytes_received:,}"
        )

    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    throughput = total_bytes / avg_time / 1024 / 1024

    return {
        "chunk_size": chunk_size,
        "avg_time": avg_time,
        "min_time": min_time,
        "max_time": max_time,
        "throughput_mbps": throughput,
        "bytes": total_bytes,
    }


def main():
    print("=" * 70)
    print("Streaming Throughput Benchmark")
    print("=" * 70)
    print(f"Server: {SERVER_URL}")
    print(f"Testing chunk sizes: {TEST_SIZES}")
    print("=" * 70)
    print()

    results = []
    for chunk_size in TEST_SIZES:
        print(f"\n--- Testing chunk size: {chunk_size} bytes ---")
        result = benchmark_chunk_size(chunk_size, num_requests=3)
        results.append(result)
        print()

    print("=" * 70)
    print("Summary")
    print("=" * 70)

    # Sort by throughput
    results_by_throughput = sorted(
        results, key=lambda x: x["throughput_mbps"], reverse=True
    )

    for r in results_by_throughput:
        marker = " <-- BEST" if r == results_by_throughput[0] else ""
        print(
            f"Chunk: {r['chunk_size']:>6} B | Avg: {r['avg_time']:.3f}s | "
            f"Max: {r['throughput_mbps']:.2f} MB/s{marker}"
        )

    best = results_by_throughput[0]
    print(
        f"\nOptimal chunk size: {best['chunk_size']} bytes ({best['throughput_mbps']:.2f} MB/s)"
    )


if __name__ == "__main__":
    main()
