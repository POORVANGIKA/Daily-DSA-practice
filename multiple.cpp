#include <iostream>
using namespace std;

int main() {
    long long N, M;
    cin >> N >> M;

    if (M % N == 0)
        cout << "YES";
    else
        cout << "NO";

    return 0;
}
