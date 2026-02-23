
//You are given two integers A
// and B
//Your task is to find the minimum and maximum among them.

#include<iostream>
using namespace std;

int main(){
	cout<<"enter two numbers A and B";
	int A,B;
	cin>>A>>B;
	if(A>B){
		cout<<"max ="<< A <<endl;
	}
	else{
		cout<<"min ="<< A <<endl;
	}
	if(B>A){
		cout<<"max ="<< B <<endl;
	}
	else{
		cout<<"min ="<< B <<endl;
	}
}

