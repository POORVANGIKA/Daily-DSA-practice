//You are given an integer N Find the sum:
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    long long sum = 0;

    for (int i = 1; i <= n; i++) {
        sum += i;
    }

    cout << sum;

    return 0;
}
