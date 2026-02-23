#include <iostream>
using namespace std;

int main() {
    long long X, Y;
    cin >> X >> Y;

    if (X == 0 && Y == 0)
        cout << "Origin";
    else if (Y == 0)
        cout << "X axis";
    else if (X == 0)
        cout << "Y axis";
    else if (X > 0 && Y > 0)
        cout << "1st Quadrant";
    else if (X < 0 && Y > 0)
        cout << "2nd Quadrant";
    else if (X < 0 && Y < 0)
        cout << "3rd Quadrant";
    else
        cout << "4th Quadrant";

    return 0;
}
