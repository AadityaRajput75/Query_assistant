import sys
import functools

def power_of_four(n: int) -> int:
    return n ** 4

def is_non_positive(n: int) -> bool:
    return n <= 0

def solve(lines: list, index: int, n: int, results: list) -> list:
    if n == 0:
        return results
    x = int(lines[index])
    raw = lines[index + 1].split()
    if len(raw) != x:
        return solve(lines, index + 2, n - 1, results + [-1])
    nums = list(map(int, raw))
    filtered = list(filter(is_non_positive, nums))
    total = functools.reduce(lambda acc, v: acc + power_of_four(v), filtered, 0)
    return solve(lines, index + 2, n - 1, results + [total])

def main():
    data = sys.stdin.read().split('\n')
    n = int(data[0])
    results = solve(data, 1, n, [])
    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    main()