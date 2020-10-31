#include <iostream>

typedef long long unsigned llu;

const llu MODULO = 1 << 16;
const llu Q_MODULO = 1 << 30;

llu find_sum(llu* array, llu left, llu right) {
    // Возвращает сумму на отрезке
    if (left == 0) {
        return array[right];
    }
    else {
        return array[right] - array[left - 1];
    }
}

int main() {
    // Считывание, обработка, вывод
    std::ios::sync_with_stdio(false);
    std::cin.tie(0);

    llu size, first, second, last;
    std::cin >> size >> first >> second >> last;
    llu* prefix_sum = new llu[size];
    
    prefix_sum[0] = last;
    for (llu i = 1; i < size; i++) {
        llu cur = (first * last + second) % MODULO;
        prefix_sum[i] = prefix_sum[i - 1] + cur;
        last = cur;
    }

    llu q_size, q_first, q_second, q_last;
    std::cin >> q_size >> q_first >> q_second >> q_last;

    llu res = 0;
    llu previous = q_last % size;
    for (llu i = 1; i < 2 * q_size; i++) {
        q_last = (q_first * q_last + q_second) % Q_MODULO;
        llu current = q_last % size;
        llu left = previous;
        llu right = current;
        if (left > right) {
            std::swap(left, right);
        }
        if (i % 2 == 1) {
            res += find_sum(prefix_sum, left, right);
        }
        previous = current;
    }
    std::cout << res;
    return 0;
}

