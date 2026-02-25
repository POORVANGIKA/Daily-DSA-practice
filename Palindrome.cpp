//You are given a non-negative integer N Check whether this is a palindrome or not.

//A number is called a palindrome if it reads the same forwards and backwards.

#include <iostream>
using namespace std;

int main() {
    long long N;
    cin >> N;

    long long original = N;
    long long reversed = 0;

    while (N > 0) {
        int digit = N % 10;
        reversed = reversed * 10 + digit;
        N /= 10;
    }

    if (original == reversed)
        cout << "YES";
    else
        cout << "NO";

    return 0;
}
