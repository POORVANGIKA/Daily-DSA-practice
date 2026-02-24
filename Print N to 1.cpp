//You are given a positive integer n


//Print the integers from 1
 //to n
// (inclusive), each on a separate line.

#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    for (int i = n; i >= 1; i--)
        cout << i << " ";

    return 0;
}
