//Given an integer N find the sum of its digits.

#include <iostream>
using namespace std;

int main() {
    long long N;
    cin >> N;

    int result = 0;

    while (N > 0) {
        int digit = N % 10;   // get last digit
        result += digit;      // add to sum
        N = N / 10;           // remove last digit
    }

    cout << result;

    return 0;
}
