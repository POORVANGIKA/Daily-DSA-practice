//You are given the length and breadth of a rectangle. Your task is to calculate its area and perimeter.
#include <iostream>
using namespace std;

#include <iostream>
using namespace std;

#include <iostream>
using namespace std;

int main() {
    int length, breadth;
    cin >> length >> breadth;

    int area = length * breadth;
    int perimeter = 2 * (length + breadth);

    cout << "Area = " << area << "\n";
    cout << "Perimeter = " << perimeter;

    return 0;
}