//You are given a non-negative integer N

//Reverse the digits of N and store the result in a variable.

#include <iostream>
using namespace std;

int main() {
    long long N;
    cin >> N;

    long long result = 0;

    while (N > 0) {
        int digit = N % 10;
        result = result * 10 + digit;
        N /= 10;
    }

    cout << result;

    return 0;
}
