//You are given two integers N
 //and M
// Your task is to compute and print the results of the following operations:

//N+M
//N-M
//N×M
//N÷M
 //(integer division)
//NmodM
#include<iostream>
using namespace std;

int main(){
	cout <<"enter two numbers N and M"<<endl;
	int N ,M ;
	cin>>N>>M;
	cout<< N <<" + "<< M <<" = " <<N+M<<endl;
	cout<< N <<" - "<< M <<" = " <<N-M<<endl;
	cout<< N <<" * "<< M <<" = " <<N*M<<endl;
	cout<< N <<" / "<< M <<" = " <<N/M<<endl;
	cout<< N <<" % "<< M <<" = " <<N%M<<endl;
	
	
}
