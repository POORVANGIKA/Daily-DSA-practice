//You are given a positive integer n


//Print a pattern consisting of n
// rows, where each row contains exactly two stars ('**').

#include<iostream>
using namespace std;

int main (){
    int n;
    cin >> n;

    for(int i = 1; i <= n; i++){
        cout << "**" << endl;
    }

    return 0;
}
