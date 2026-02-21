//Your task is to print the letter Z using asterisks (*) as shown below.

//Input
//There is no input for this problem.

//Output
//Print the following pattern exactly as shown:


//*****
//   *
//  *
// *
//*****
#include<iostream>
using namespace std;

#include <iostream>
using namespace std;

int main(){
    for (int i = 1; i <= 5; i++){
        for (int j = 1; j <= 5; j++){
            if (i == 1 || i == 5){
                cout << "*";
            }
            else if (j == 6 - i){
                cout << "*";
            }
            else{
                cout << " ";
            }
        }
        cout << endl;
    }
    return 0;
}