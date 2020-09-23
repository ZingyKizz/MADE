#include <iostream>
#include <vector>
 
using namespace std;
 
typedef long long ll;
 
pair<int, int> partition(vector<ll> &arr, int low, int high) {
    /*
    Делим на три части
    меньше base: arr[low: less]
    равно base: arr[less: greater + 1]
    больше base: arr[greater + 1: high + 1]
    */
    int base = arr[low];
    int less = low;
    int greater = high;
 
    int i = low;
    while (i <= greater) {
        if (arr[i] < base) {
            swap(arr[less++], arr[i++]);
        } else if (arr[i] == base) {
            i++;
        } else {
            swap(arr[i], arr[greater--]);
        }
    }
 
    return make_pair(less, greater);
}
 
int kth_statistics_ij(vector<ll> &arr, int i, int j, int k) {
    // Считаем k-ую порядковую статистику
    if (i == j) {
        return arr[i];
    }
 
    auto[less, greater] = partition(arr, i, j);
    int less_length = less - i;
    int equal_length = greater - less + 1;
 
    if (k <= less_length) {
        return kth_statistics_ij(arr, i, less - 1, k);
    } else if (k <= less_length + equal_length) {
        return arr[less];
    } else {
        return kth_statistics_ij(arr, greater + 1, j, k - (less_length + equal_length));
    }
}
 
int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
 
    int n;
    cin >> n;
    vector<ll> array(n);
    for (int i = 0; i < n; i++) {
        cin >> array[i];
    }
 
    int m, i_, j_, k_;
    cin >> m;
    for (int i = 0; i < m; i++){
        vector<ll> array_(array);
        cin >> i_ >> j_ >> k_;
        cout << kth_statistics_ij(array_, i_ - 1, j_ - 1, k_) << "\n";
    }
}
