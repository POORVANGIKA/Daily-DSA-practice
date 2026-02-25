//You are given a non-negative integer N

//Reverse the digits of N and store the result in a variable.

#include<iostream>
using namespace std;

int main(){
	long long N;
	cin>>N;
	
	long long result =0;
	
	if (N==0){
		cout<<0;
	}
	
	while(N>0){
		result=N%10;
		cout<<result;
		N=N/10;
	}
}
