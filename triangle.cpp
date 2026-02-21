//our task is to print a right-angled triangle pattern using asterisks (*).

//Input
//There is no input for this problem.

//Output
//Print the following pattern exactly as shown:


//*****
//****
//***
//**
//*
#include <iostream>
using namespace std;

int main() {
    for (int i = 5; i >= 1; i--) {
        for (int j = 1; j <= i; j++) {
            cout << "*";
        }
        cout << "\n";
    }
    return 0;
}