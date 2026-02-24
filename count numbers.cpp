//You are given an integer N followed by N integers. Count how many of the given numbers are:

//Positive
//Negative
//Even
//Odd

#include <iostream>
using namespace std;

int main() {

    int n;
    cin >> n;          // how many numbers

    long long x;       // stores each number

    int pos = 0;       // positive count
    int neg = 0;       // negative count
    int even = 0;      // even count
    int odd = 0;       // odd count

    for (int i = 0; i < n; i++) {
        cin >> x;      // read number

        // positive check
        if (x > 0)
            pos++;

        // negative check
        if (x < 0)
            neg++;

        // even / odd check
        if (x % 2 == 0)
            even++;
        else
            odd++;
    }

    cout << pos << '\n';
    cout << neg << '\n';
    cout << even << '\n';
    cout << odd << '\n';

    return 0;
}
