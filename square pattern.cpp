#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    for(int i = 1; i <= n; i++) {      // loop for rows
        for(int j = 1; j <= n; j++) {  // loop for columns
            cout << "*";
        }
        cout << endl;                  // move to next line
    }

    return 0;
}
