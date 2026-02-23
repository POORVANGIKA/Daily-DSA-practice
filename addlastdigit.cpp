//You are given two integers N
 //and M
// Your task is to find the sum of the last digits of N
 //and M


#include<iostream>
using namespace std;

int main (){
	cout<<"Enter the two numbers"<<endl;
	int N,M;
	cin>>N>>M;
	N = N%10;
	M = M%10;
	cout<<"the additon of the last digits of N and M is "<<N+M;
}

