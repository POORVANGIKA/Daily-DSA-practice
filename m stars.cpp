//You are given two integers n and m Your task is to print a rectangle pattern consisting of n
 //rows and m columns, where each cell contains a star '*'.
#include<iostream>
using namespace std;

int main(){
    int n, m;
    cin >> n >> m;   // Takes two inputs correctly

    for(int i = 1; i <= n; i++){          // Loop for rows
        for(int j = 1; j <= m; j++){      // Loop for columns
            cout << "*";
        }
        cout << endl;   // Move to next line after each row
    }

    return 0;
}
