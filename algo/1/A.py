from sys import stdin, stdout
 
 
def calc_sum(first: int, second: int) -> int:
    """Суммируем два элемента"""
    return first + second
 
 
if __name__ == '__main__':
    t = int(stdin.readline())
    for _ in range(t):
        a, b = map(int, stdin.readline().split())
        stdout.write(str(calc_sum(a, b)) + '\n')
