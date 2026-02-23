//You are given two integers N
 //and M
// Your task is to compute and print the results of the following operations:

//N+M
//N-M
//N×M
//N÷M
//NmodM
#include <iostream>
using namespace std;

int main() {
    int N, M;
    cin >> N >> M;

    cout << N << " + " << M << " = " << N + M << endl;
    cout << N << " - " << M << " = " << N - M << endl;
    cout << N << " * " << M << " = " << N * M << endl;
    cout << N << " / " << M << " = " << N / M << endl;   // integer division
    cout << N << " % " << M << " = " << N % M << endl;

    return 0;
}
